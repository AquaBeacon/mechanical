"""Shared local operations for the FreeCAD MCP; originals are never overwritten."""
from contextlib import contextmanager
import math
import os
from pathlib import Path
import re
import subprocess
import sys

from cli import ROOT, digest, find_freecad, make_plan, read_json, run_job, within


class CadService:
    def __init__(self, root=ROOT, freecad=None):
        self.root = Path(root).resolve()
        if not self.root.is_dir():
            raise ValueError("workspace does not exist")
        self.freecad = freecad
        self.runs = self.root / "tools/_work/analysis/cad_foundation"

    def _path(self, value, suffixes=None):
        path = within(self.root, self.root / value)
        if not path.is_file():
            raise ValueError("file not found: %s" % path)
        if suffixes and path.suffix.lower() not in suffixes:
            raise ValueError("unsupported format: %s" % path.suffix)
        return path

    def _relative(self, path):
        return path.relative_to(self.root).as_posix()

    @contextmanager
    def _lock(self):
        """OS releases lock after crashes; no stale PID files to delete."""
        self.runs.mkdir(parents=True, exist_ok=True)
        with (self.runs / "cad.lock").open("a+b") as stream:
            stream.seek(0, 2)
            if stream.tell() == 0:
                stream.write(b"0")
                stream.flush()
            stream.seek(0)
            try:
                if os.name == "nt":
                    import msvcrt
                    msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError as exc:
                raise RuntimeError("FreeCAD batch is busy in this workspace; retry after it finishes") from exc
            try:
                yield
            finally:
                stream.seek(0)
                if os.name == "nt":
                    msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    fcntl.flock(stream.fileno(), fcntl.LOCK_UN)

    def _run(self, plan, timeout):
        if not 1 <= timeout <= 240:
            raise ValueError("timeout must be between 1 and 240 seconds")
        with self._lock():
            return run_job(self.root, plan, self.freecad, timeout)

    @staticmethod
    def _page(rows, offset, limit):
        if offset < 0 or not 1 <= limit <= 100:
            raise ValueError("offset >= 0 and 1 <= limit <= 100 required")
        end = offset + limit
        return {"items": rows[offset:end], "total": len(rows), "offset": offset,
                "next_offset": end if end < len(rows) else None}

    def status(self):
        try:
            executable = find_freecad(self.freecad)
            error = None
        except ValueError as exc:
            executable, error = None, str(exc)
        return {"workspace": str(self.root), "freecadcmd": executable, "error": error,
                "python": sys.executable, "runs": str(self.runs), "units": "mm",
                "mode": "isolated CLI processes; no connection to an open GUI session",
                "capabilities": ["assembly", "native_generator", "inspect", "spreadsheet_edit", "step_stl_export", "open_gui"]}

    def plan_assembly(self, placement, offset=0, limit=40):
        plan = make_plan(self.root, self.root / placement)
        return dict(plan, entries=self._page(plan["entries"], offset, limit))

    def export_assembly(self, placement, max_components=40, timeout=120):
        plan = make_plan(self.root, self.root / placement)
        if plan["missing"]:
            raise ValueError("missing components: " + ", ".join(plan["missing"]))
        if not 1 <= max_components <= 500 or plan["component_count"] > max_components:
            raise ValueError("component limit exceeded; review plan and set max_components explicitly (1..500)")
        return self._run(plan, timeout)

    def create_demo(self, timeout=120):
        return self._run({"schema_version": 1, "kind": "demo", "units": "mm", "name": "EditablePlateDemo"}, timeout)

    def build_native(self, generator, parameters=None, dependencies=None, timeout=120):
        path = self._path(generator, {".py"})
        relative = self._relative(path)
        if not (relative.startswith(("parts/", "spec/", "tools/cad_foundation/recipes/"))):
            raise ValueError("generator must be under parts/, spec/, or tools/cad_foundation/recipes/")
        # Generator code is trusted executable project code, not an untrusted recipe DSL.
        files = [relative] + [self._relative(self._path(p)) for p in (dependencies or [])]
        import json
        if parameters is not None and not isinstance(parameters, dict):
            raise ValueError("parameters must be an object")
        if len(json.dumps(parameters or {}, allow_nan=False)) > 65536:
            raise ValueError("parameters exceed 64 KiB")
        return self._run({"schema_version": 1, "kind": "native", "name": path.stem, "units": "mm",
                          "generator": relative, "parameters": parameters or {}, "input_files": files}, timeout)

    def _document_plan(self, path, kind, object_names=None):
        source = self._path(path, {".fcstd", ".step", ".stp", ".stl"})
        return {"schema_version": 1, "kind": kind, "units": "mm", "name": source.stem,
                "source": self._relative(source), "input_files": [self._relative(source)],
                "object_names": object_names}

    def inspect_document(self, path, offset=0, limit=40, timeout=120):
        self._page([], offset, limit)
        result = self._run(self._document_plan(path, "inspect"), timeout)
        report = read_json(result["report"])
        return dict(result, document=report["document"], objects=self._page(report["objects"], offset, limit))

    def edit_parameters(self, path, updates, sheet="Parameters", object_names=None, timeout=120):
        self._path(path, {".fcstd"})
        if not updates or len(updates) > 100:
            raise ValueError("provide 1..100 named numeric spreadsheet aliases")
        for key, value in updates.items():
            if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key) or isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value):
                raise ValueError("updates require named aliases and finite numbers; units are preserved")
        plan = self._document_plan(path, "edit", object_names)
        plan.update(updates=updates, sheet=sheet)
        return self._run(plan, timeout)

    def export_document(self, path, object_names, timeout=120):
        self._path(path, {".fcstd", ".step", ".stp"})
        if not object_names:
            raise ValueError("select output object names from inspect_document; do not export intermediate features")
        return self._run(self._document_plan(path, "export", object_names), timeout)

    def read_report(self, run_id):
        if not re.fullmatch(r"\d{8}T\d{6}Z_[0-9a-f]{8}", run_id):
            raise ValueError("invalid run_id")
        path = within(self.root, self.runs / run_id / "report.json")
        return read_json(path)

    def open_document(self, path):
        source = self._path(path, {".fcstd", ".step", ".stp", ".stl"})
        executable = Path(find_freecad(self.freecad))
        gui = executable.with_name("FreeCAD.exe" if os.name == "nt" else "FreeCAD")
        if not gui.is_file():
            raise ValueError("FreeCAD GUI executable was not found next to FreeCADCmd")
        # Explicit user-facing action. Batch tools never call this method.
        process = subprocess.Popen([str(gui), str(source)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return {"status": "launch_requested", "path": str(source), "pid": process.pid,
                "note": "Opening was requested; GUI rendering is not verified. Source file was not written."}
