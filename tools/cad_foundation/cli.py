"""Read-only planning and isolated, never-overwriting FreeCAD exports."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import uuid
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write_json(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def within(root, path):
    root, path = Path(root).resolve(), Path(path).resolve()
    if not path.is_relative_to(root):
        raise ValueError("path leaves repository: %s" % path)
    return path


def validate_ops(ops):
    if not isinstance(ops, list):
        raise ValueError("ops must be an array")
    for op in ops:
        if not isinstance(op, dict) or len(op) != 1:
            raise ValueError("each operation must have exactly one key")
        kind, vector = next(iter(op.items()))
        if kind not in {"translate", "rotate", "mirror", "scale"}:
            raise ValueError("unknown operation: %s" % kind)
        if not isinstance(vector, list) or len(vector) != 3 or any(
            isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) for x in vector
        ):
            raise ValueError("operation requires three finite numbers")
        if kind == "scale" and any(abs(x) < 1e-9 for x in vector):
            raise ValueError("singular scale")
        if kind == "mirror" and sum(x * x for x in vector) == 0:
            raise ValueError("zero mirror normal")


def make_plan(root, placement):
    """Inspect filenames and JSON only. No CAD imports, writes or subprocesses."""
    root = Path(root).resolve()
    placement = within(root, placement)
    if placement.is_dir():
        placement /= "placement.json"
    placement_bytes = placement.read_bytes()
    data = json.loads(placement_bytes.decode("utf-8-sig"))
    if data.get("units", "mm") != "mm":
        raise ValueError("only mm is supported")
    if "items" in data and "parts" in data:
        raise ValueError("ambiguous placement: both items and parts")
    rows = data.get("items", data.get("parts"))
    if not isinstance(rows, list) or not rows:
        raise ValueError("placement requires nonempty items or parts")
    entries, missing = [], []
    for index, row in enumerate(rows):
        folder = within(root, root / row["part"])
        stem = row.get("file") or folder.name
        if not isinstance(stem, str) or stem in {".", ".."} or any(c in stem for c in "/\\:"):
            raise ValueError("file must be a variant stem, without a path")
        ops = row.get("ops", [])
        validate_ops(ops)
        candidates = [within(root, folder / (stem + ext)) for ext in (".step", ".stp", ".STEP", ".STP", ".stl", ".STL")]
        source = next((p for p in candidates if p.is_file()), None)
        reference = next((p for p in candidates[-2:] if p.is_file()), None)
        if source is None:
            missing.append(str(folder.relative_to(root) / stem))
        entries.append({"index": index, "label": row.get("label") or stem,
                        "part": folder.relative_to(root).as_posix(), "file": stem,
                        "group": row.get("group", "components"), "ops": ops,
                        "source": source.relative_to(root).as_posix() if source else None,
                        "stl_reference": reference.relative_to(root).as_posix() if reference else None,
                        "editability": "mesh_reference" if source and source.suffix.lower() == ".stl" else "imported_brep"})
    return {"schema_version": 1, "kind": "assembly", "units": "mm",
            "placement": placement.relative_to(root).as_posix(),
            "placement_sha256": hashlib.sha256(placement_bytes).hexdigest(),
            "name": data.get("name", placement.parent.name), "entries": entries,
            "component_count": len(entries), "missing": missing,
            "warnings": ["Review copy only: does not certify source freshness, fit or strength.",
                         "STEP has no original feature history; STL stays a mesh reference.",
                         "All placement rows are included, including hidden preview groups."]}


def find_freecad(explicit=None):
    candidates = [explicit, os.environ.get("FREECADCMD"), shutil.which("freecadcmd"),
                  str(Path(os.environ.get("LOCALAPPDATA", "")) / "Programs/FreeCAD 1.0/bin/freecadcmd.exe")]
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return str(Path(candidate).resolve())
    raise ValueError("FreeCADCmd not found; set FREECADCMD or --freecad")


def snapshot_inputs(root, run, plan):
    """Copy selected inputs and detect concurrent edits before CAD starts."""
    names = {plan["placement"]}
    for row in plan["entries"]:
        names.update(p for p in (row["source"], row["stl_reference"]) if p)
    snapshots = {}
    for i, relative in enumerate(sorted(names)):
        source = within(root, root / relative)
        target = run / "intermediate" / ("input_%04d" % i + source.suffix)
        before = digest(source)
        shutil.copyfile(source, target)
        if digest(target) != before or digest(source) != before:
            raise ValueError("input changed during snapshot: %s" % relative)
        snapshots[relative] = {"path": str(target), "sha256": before}
    if snapshots[plan["placement"]]["sha256"] != plan["placement_sha256"]:
        raise ValueError("placement changed since planning")
    # Do not pair a parsed old layout with a newer snapshot.
    fresh = make_plan(root, root / plan["placement"])
    if fresh != plan:
        raise ValueError("placement/source selection changed while planning")
    return snapshots


def snapshot_files(root, run, paths):
    """Preserve relative paths so declared generator dependencies still resolve."""
    result = {}
    for relative in sorted(set(paths)):
        source = within(root, root / relative)
        relative = source.relative_to(root).as_posix()
        target = within(run, run / "intermediate/sources" / relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        before = digest(source)
        shutil.copyfile(source, target)
        if digest(target) != before or digest(source) != before:
            raise ValueError("input changed during snapshot: %s" % relative)
        result[relative] = {"path": str(target), "sha256": before}
    return result


def run_job(root, plan, freecad=None, timeout=120):
    root = Path(root).resolve()
    executable = find_freecad(freecad)
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "_" + uuid.uuid4().hex[:8]
    run = within(root, root / "tools/_work/analysis/cad_foundation" / run_id)
    run.mkdir(parents=True, exist_ok=False)
    for child in ("intermediate", "logs"):
        (run / child).mkdir()
    job = dict(plan, run_id=run_id, run_dir=str(run))
    try:
        job["snapshots"] = (snapshot_inputs(root, run, plan) if plan["kind"] == "assembly"
                            else snapshot_files(root, run, plan.get("input_files", [])))
    except (ValueError, OSError, KeyError) as error:
        write_json(run / "report.json", {"schema_version": 1, "run_id": run_id, "kind": plan["kind"],
                                        "status": "failed", "stage": "snapshot", "error": str(error)})
        raise RuntimeError("input snapshot failed: %s; see %s" % (error, run)) from error
    write_json(run / "job.json", job)
    env = os.environ.copy()
    env.update(ASM_ROOT=str(root), CAD_FOUNDATION_JOB=str(run / "job.json"), PYTHONIOENCODING="utf-8")
    if plan["kind"] == "assembly":
        env["ASM_JSON"] = job["snapshots"][plan["placement"]]["path"]
    # Private config files prevent writes to the running user's FreeCAD settings.
    command = [executable, "-u", str(run / "intermediate/user.cfg"), "-s", str(run / "intermediate/system.cfg"),
               str(Path(__file__).with_name("freecad_worker.py"))]
    flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    with (run / "logs/freecad.log").open("w", encoding="utf-8") as log:
        try:
            completed = subprocess.run(command, env=env, stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT,
                                       timeout=timeout, creationflags=flags)
        except subprocess.TimeoutExpired:
            write_json(run / "report.json", {"schema_version": 1, "run_id": run_id, "kind": plan["kind"],
                                            "status": "failed", "stage": "timeout", "timeout_seconds": timeout})
            raise RuntimeError("CAD timed out; outputs are not accepted. See %s" % run)
    report_file = run / "report.json"
    if not report_file.exists():
        write_json(report_file, {"schema_version": 1, "run_id": run_id, "kind": plan["kind"],
                                "status": "failed", "stage": "process", "exit_code": completed.returncode,
                                "error": "FreeCAD produced no verification receipt"})
        raise RuntimeError("CAD produced no verification receipt. See %s" % run)
    report = read_json(report_file)
    if completed.returncode or report.get("status") != "passed" or report.get("run_id") != run_id:
        raise RuntimeError("CAD verification failed. See %s" % report_file)
    changed = [p for p, s in job["snapshots"].items() if not (root / p).is_file() or digest(root / p) != s["sha256"]]
    report["source_changed_during_run"] = changed
    if changed:
        report["status"] = "source_changed"
    write_json(report_file, report)
    if changed:
        raise RuntimeError("source changed during export; review copy is stale. See %s" % report_file)
    result = {"status": "passed", "run_dir": str(run), "report": str(report_file), "run_id": run_id}
    if (run / "model.FCStd").exists():
        result["model"] = str(run / "model.FCStd")
    if report.get("exports"):
        result["exports"] = report["exports"]
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("plan", "assembly"):
        sub = commands.add_parser(name)
        sub.add_argument("placement", help="assembly directory or placement.json")
        if name == "assembly":
            sub.add_argument("--max-components", type=int, default=40)
            sub.add_argument("--freecad")
            sub.add_argument("--timeout", type=int, default=120)
    demo = commands.add_parser("demo")
    demo.add_argument("--freecad")
    demo.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args(argv)
    try:
        if args.command == "demo":
            plan = {"schema_version": 1, "kind": "demo", "units": "mm", "name": "EditablePlateDemo"}
        else:
            plan = make_plan(ROOT, ROOT / args.placement)
        if args.command == "plan":
            result = plan
        else:
            if args.timeout < 1:
                raise ValueError("timeout must be positive")
            if plan.get("missing"):
                raise ValueError("missing components: " + ", ".join(plan["missing"]))
            if args.command == "assembly" and plan["component_count"] > args.max_components:
                raise ValueError("component limit exceeded; review plan and explicitly raise --max-components")
            result = run_job(ROOT, plan, args.freecad, args.timeout)
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        return 1 if result.get("missing") else 0
    except (ValueError, OSError, RuntimeError, KeyError, TypeError) as error:
        print(json.dumps({"status": "failed", "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
