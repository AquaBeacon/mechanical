"""Real stdio MCP/FreeCAD integration, using only isolated generated fixtures."""
import argparse
import asyncio
from datetime import timedelta
import json
import os
from pathlib import Path
import sys
import tempfile
import tomllib

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from cli import ROOT, digest, write_json


async def main(from_config=False):
    runs = ROOT / "tools/_work/analysis/cad_foundation"
    runs.mkdir(parents=True, exist_ok=True)
    scratch = Path(tempfile.mkdtemp(prefix="stdio_", dir=runs))
    if from_config:
        config = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "config.toml"
        settings = tomllib.loads(config.read_text(encoding="utf-8"))["mcp_servers"]["freecad"]
        command, args = settings["command"], settings["args"]
    else:
        command, args = sys.executable, ["-X", "utf8", str(Path(__file__).with_name("mcp_server.py")), "--workspace", str(ROOT)]
    params = StdioServerParameters(command=command, args=args, env=os.environ.copy())
    cases = []
    with (scratch / "server.log").open("w", encoding="utf-8") as error_log:
        async with stdio_client(params, errlog=error_log) as (reader, writer):
            async with ClientSession(reader, writer, read_timeout_seconds=timedelta(seconds=270)) as session:
                init = await session.initialize()
                listing = await session.list_tools()
                assert len(listing.tools) == 10
                assert all(t.annotations is not None and t.outputSchema for t in listing.tools)
                cases.append("initialize and list 10 typed tools")

                async def call(name, arguments=None, error=False):
                    response = await session.call_tool(name, arguments or {})
                    if error:
                        assert response.isError, response
                        return None
                    assert not response.isError, response
                    assert response.structuredContent is not None, response
                    return response.structuredContent

                status = await call("freecad_status")
                assert status["freecadcmd"] and status["workspace"] == str(ROOT)
                await call("freecad_plan_assembly", {"placement": "../outside"}, error=True)
                cases.append("status and workspace boundary error")
                demo = await call("freecad_create_demo")
                original_hash = digest(demo["model"])
                info = await call("freecad_inspect_document", {"path": demo["model"]})
                assert info["document"]["output_names"] == ["Pocket"]
                sheet = next(row for row in info["objects"]["items"] if row["name"] == "Parameters")
                assert "length" in sheet["parameters"]
                page = await call("freecad_inspect_document", {"path": demo["model"], "limit": 1})
                assert len(page["objects"]["items"]) == 1 and page["objects"]["next_offset"] == 1
                cases.append("create native demo, inspect aliases, paginate")
                edited = await call("freecad_edit_parameters", {"path": demo["model"], "updates": {"length": 100}})
                report = await call("freecad_read_report", {"run_id": edited["run_id"]})
                box = report["components"]["Pocket"]["bbox_mm"]
                assert abs(box[3] - box[0] - 100) < 1e-6
                assert digest(demo["model"]) == original_hash
                await call("freecad_edit_parameters", {"path": demo["model"], "updates": {"unknown_alias": 10}}, error=True)
                cases.append("edit dimension via MCP; original unchanged; reject unknown alias")
                exported = await call("freecad_export_document", {"path": edited["model"], "object_names": ["Pocket"]})
                assert Path(exported["exports"]["Pocket"]["step"]).exists()
                assert exported["exports"]["Pocket"]["stl_closed"]
                await call("freecad_export_document", {"path": demo["model"], "object_names": ["Body", "Pad"]}, error=True)
                cases.append("STEP/STL export and reject duplicate feature history")
                native = await call("freecad_build_native", {
                    "generator": "tools/cad_foundation/recipes/plate.py", "parameters": {"length": 90},
                    "dependencies": ["tools/cad_foundation/native_template.py"]})
                native_report = await call("freecad_read_report", {"run_id": native["run_id"]})
                native_box = native_report["components"]["Pocket"]["bbox_mm"]
                assert abs(native_box[3] - native_box[0] - 90) < 1e-6
                cases.append("trusted native generator and dependency snapshot")
                folder = Path(native["run_dir"]).relative_to(ROOT).as_posix()
                layout = scratch / "placement.json"
                write_json(layout, {"units": "mm", "items": [
                    {"part": folder, "file": "Pocket", "label": "left"},
                    {"part": folder, "file": "Pocket", "label": "right", "ops": [{"translate": [120, 0, 0]}, {"mirror": [1, 0, 0]}]}
                ]})
                plan = await call("freecad_plan_assembly", {"placement": str(layout), "limit": 1})
                assert plan["component_count"] == 2 and plan["entries"]["next_offset"] == 1
                assembly = await call("freecad_export_assembly", {"placement": str(layout)})
                assembly_report = await call("freecad_read_report", {"run_id": assembly["run_id"]})
                assert assembly_report["component_count"] == 2
                cases.append("plan and export a two-part mirrored assembly")
    result = {"status": "passed", "server": init.serverInfo.model_dump(), "from_registered_config": from_config,
              "cases": cases, "demo": demo, "native": native, "edited": edited, "assembly": assembly,
              "gui": "not launched; open command tested separately with mocked process"}
    write_json(scratch / "smoke-report.json", result)
    print(json.dumps({"status": "passed", "cases": len(cases), "report": str(scratch / "smoke-report.json")}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--from-config", action="store_true")
    asyncio.run(main(parser.parse_args().from_config))
