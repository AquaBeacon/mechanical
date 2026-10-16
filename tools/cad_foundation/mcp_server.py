"""Local stdio MCP interface for the repository's FreeCAD review service."""
from __future__ import annotations

import argparse
import asyncio
from typing import Annotated, Any

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError
from mcp.types import ToolAnnotations
from pydantic import Field

from cli import ROOT
from service import CadService


READ_ONLY = ToolAnnotations(readOnlyHint=True, destructiveHint=False,
                            idempotentHint=True, openWorldHint=False)
MUTATION = ToolAnnotations(readOnlyHint=False, destructiveHint=False,
                           idempotentHint=False, openWorldHint=False)


def create_server(service: CadService) -> FastMCP:
    """Bind a single service instance to the ten public FreeCAD tools."""
    mcp = FastMCP(
        "freecad_mcp",
        instructions=("Review and create FreeCAD documents inside the configured workspace. "
                       "The service writes generated results to new run folders. Native generators are trusted "
                       "project code, not sandboxed, and must have no writes outside the supplied document. "
                       "Imported STEP geometry has no recovered parametric feature history. "
                       "Only use open_document when the user asks to view a CAD document."),
        log_level="WARNING",
    )

    async def invoke(method: str, *args, **kwargs):
        try:
            return await asyncio.to_thread(getattr(service, method), *args, **kwargs)
        except ToolError:
            raise
        except Exception as exc:
            raise ToolError(str(exc)) from exc

    @mcp.tool(name="freecad_status", description="Report FreeCADCmd availability and configured workspace.", annotations=READ_ONLY)
    async def freecad_status() -> dict[str, Any]:
        return await invoke("status")

    @mcp.tool(name="freecad_plan_assembly", description="Read-only assembly plan with component pagination; does not run CAD or modify files.", annotations=READ_ONLY)
    async def freecad_plan_assembly(
        placement: Annotated[str, Field(description="Repository-relative placement.json path or assembly directory.")],
        offset: Annotated[int, Field(ge=0, description="First component index to return.")] = 0,
        limit: Annotated[int, Field(ge=1, le=100, description="Maximum components to return.")] = 40,
    ) -> dict[str, Any]:
        return await invoke("plan_assembly", placement, offset, limit)

    @mcp.tool(name="freecad_export_assembly", description="Create and verify a review copy from an assembly plan. Original sources are never overwritten.", annotations=MUTATION)
    async def freecad_export_assembly(
        placement: Annotated[str, Field(description="Repository-relative placement.json path or assembly directory.")],
        max_components: Annotated[int, Field(ge=1, le=500, description="Safety limit for planned components.")] = 40,
        timeout: Annotated[int, Field(ge=1, le=240, description="FreeCAD process timeout in seconds.")] = 120,
    ) -> dict[str, Any]:
        return await invoke("export_assembly", placement, max_components, timeout)

    @mcp.tool(name="freecad_create_demo", description="Create and verify the illustrative editable native-feature plate demo in a new run folder.", annotations=MUTATION)
    async def freecad_create_demo(
        timeout: Annotated[int, Field(ge=1, le=240, description="FreeCAD process timeout in seconds.")] = 120,
    ) -> dict[str, Any]:
        return await invoke("create_demo", timeout)

    @mcp.tool(name="freecad_build_native", description="Run a reviewed Python generator inside the workspace to create editable native FreeCAD features; generator must expose build(doc, parameters) and return objects.", annotations=MUTATION)
    async def freecad_build_native(
        generator: Annotated[str, Field(description="Repository-relative path to a reviewed trusted Python generator.")],
        parameters: Annotated[dict[str, float] | None, Field(description="Optional numeric generator parameters.")] = None,
        dependencies: Annotated[list[str] | None, Field(description="Optional repository-relative input files to snapshot with this run.")] = None,
        timeout: Annotated[int, Field(ge=1, le=240, description="FreeCAD process timeout in seconds.")] = 120,
    ) -> dict[str, Any]:
        return await invoke("build_native", generator, parameters, dependencies, timeout)

    @mcp.tool(name="freecad_inspect_document", description="Read-only inspection of an existing FreeCAD document with object pagination.", annotations=READ_ONLY)
    async def freecad_inspect_document(
        path: Annotated[str, Field(description="Workspace path to .FCStd, .step/.stp, or .stl for inspection.")],
        offset: Annotated[int, Field(ge=0, description="First object index to return.")] = 0,
        limit: Annotated[int, Field(ge=1, le=100, description="Maximum objects to return.")] = 40,
        timeout: Annotated[int, Field(ge=1, le=240, description="FreeCAD process timeout in seconds.")] = 120,
    ) -> dict[str, Any]:
        return await invoke("inspect_document", path, offset, limit, timeout)

    @mcp.tool(name="freecad_edit_parameters", description="Update named spreadsheet cells in a copied document, recompute, and save to a new run folder; original remains unchanged.", annotations=MUTATION)
    async def freecad_edit_parameters(
        path: Annotated[str, Field(description="Repository-relative .FCStd document path.")],
        updates: Annotated[dict[str, float], Field(description="Existing spreadsheet aliases (not cell addresses) mapped to numeric values in their current unit.")],
        sheet: Annotated[str, Field(description="Spreadsheet object name.")] = "Parameters",
        object_names: Annotated[list[str] | None, Field(description="Optional objects to include in verification/export.")] = None,
        timeout: Annotated[int, Field(ge=1, le=240, description="FreeCAD process timeout in seconds.")] = 120,
    ) -> dict[str, Any]:
        return await invoke("edit_parameters", path, updates, sheet, object_names, timeout)

    @mcp.tool(name="freecad_export_document", description="Export selected objects from an existing document into a new review run; source document is never overwritten.", annotations=MUTATION)
    async def freecad_export_document(
        path: Annotated[str, Field(description="Workspace path to .FCStd or .step/.stp. STL mesh inputs are not converted to solids.")],
        object_names: Annotated[list[str], Field(description="Names of document objects to export.")],
        timeout: Annotated[int, Field(ge=1, le=240, description="FreeCAD process timeout in seconds.")] = 120,
    ) -> dict[str, Any]:
        return await invoke("export_document", path, object_names, timeout)

    @mcp.tool(name="freecad_open_document", description="Open a saved FreeCAD document in the desktop GUI. Call only when the user asks to see or open it.", annotations=MUTATION)
    async def freecad_open_document(
        path: Annotated[str, Field(description="Workspace path to .FCStd, .step/.stp, or .stl to open in FreeCAD GUI.")],
    ) -> dict[str, Any]:
        return await invoke("open_document", path)

    @mcp.tool(name="freecad_read_report", description="Read-only retrieval of a prior CAD foundation run report by run ID.", annotations=READ_ONLY)
    async def freecad_read_report(
        run_id: Annotated[str, Field(description="Run ID returned by a FreeCAD operation.")],
    ) -> dict[str, Any]:
        return await invoke("read_report", run_id)

    return mcp


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=str(ROOT), help="Workspace root (defaults to this repository).")
    parser.add_argument("--freecad", help="Optional FreeCADCmd path; otherwise use the service's normal discovery.")
    args = parser.parse_args(argv)
    service = CadService(args.workspace, freecad=args.freecad)
    create_server(service).run(transport="stdio")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
