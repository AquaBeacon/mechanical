"""Slice repeatable_mount plate STLs with Bambu Studio and preserve per-plate jobs."""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSEMBLY = ROOT / "assemblies" / "parent_oneplate"
WORK = ASSEMBLY / "_work" / "analysis" / "repeatable_mount"
JOBS = ASSEMBLY / "print_jobs" / "repeatable_mount"
CONFIG = ROOT / "print_jobs" / "parent_spar_bolted" / "slice_validation"
PROCESS_TEMPLATE = ROOT / "assemblies" / "parent_direct" / "slice_validation" / "parent_direct_frame" / "process.json"
STUDIO = Path(r"C:\Program Files\Bambu Studio\bambu-studio.exe")


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def digest(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    required = [STUDIO, CONFIG / "machine.json", CONFIG / "filament.json", PROCESS_TEMPLATE,
                JOBS / "manifest.json"]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError("required slicing inputs are missing: " + ", ".join(missing))
    source_manifest = read(JOBS / "manifest.json")
    source_hash = digest(JOBS / "manifest.json")
    process_template = read(PROCESS_TEMPLATE)
    process_template.update({"print_settings_id": "Parent repeatable mount PETG 0.20 supports", "layer_height": "0.2",
                             "wall_loops": "6", "top_shell_layers": "6", "bottom_shell_layers": "6",
                             "sparse_infill_density": "40%", "enable_support": "1", "brim_width": "5",
                             "print_sequence": "by layer"})
    plate_reports = []
    for plate in source_manifest["plates"]:
        number = plate["plate"]
        work = WORK / f"slice_plate_{number}"
        work.mkdir(parents=True, exist_ok=True)
        process = work / "process.json"
        process.write_text(json.dumps(process_template, indent=2) + "\n", encoding="utf-8")
        source = JOBS / plate["stl"]
        if digest(source) != plate["sha256"]:
            raise ValueError(f"plate STL hash differs from build manifest: {source}")
        filename = f"plate_{number}_X1C.3mf"
        command = [str(STUDIO), "--debug", "2", "--datadir", str(work / "studio_data"),
                   "--load-settings", str(CONFIG / "machine.json") + ";" + str(process),
                   "--load-filaments", str(CONFIG / "filament.json"), "--arrange", "0", "--orient", "0",
                   "--slice", "0", "--export-3mf", filename, "--outputdir", str(work), str(source)]
        run = subprocess.run(command, capture_output=True, text=True, errors="replace", cwd=work)
        (work / "slice.log").write_text(run.stdout + run.stderr, encoding="utf-8")
        result_path = work / "result.json"
        if not result_path.is_file():
            raise RuntimeError(f"Bambu Studio did not write result.json for plate {number}; see {work / 'slice.log'}")
        result = read(result_path)
        if run.returncode != 0 or result.get("return_code") != 0:
            raise RuntimeError(f"Bambu Studio failed for plate {number}: {result}")
        sliced = result.get("sliced_plates", [])
        if len(sliced) != 1:
            raise RuntimeError(f"expected exactly one sliced plate for plate {number}, got {len(sliced)}")
        produced = work / filename
        if not produced.is_file():
            raise RuntimeError(f"3MF export missing: {produced}")
        with zipfile.ZipFile(produced) as archive:
            names = set(archive.namelist())
            gcode_name = "Metadata/plate_1.gcode"
            if gcode_name not in names:
                raise RuntimeError(f"3MF missing sliced plate G-code: {produced}")
            gcode = archive.read(gcode_name).decode("utf-8", errors="replace")
            supports = [line for line in gcode.splitlines() if line.startswith("; FEATURE:") and "Support" in line]
        plate_result = sliced[0]
        target = JOBS / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(produced, target)
        plate_reports.append({"plate": number, "stl": plate["stl"], "stl_sha256": digest(source),
                              "three_mf": target.name, "three_mf_sha256": digest(target),
                              "part_count": plate["part_count"], "support_enabled": True,
                              "support_feature_sections": len(supports),
                              "grams": sum(f.get("total_used_g", 0) for f in plate_result.get("filaments", [])),
                              "seconds": plate_result.get("total_predication"),
                              "warnings": plate_result.get("warning_message", ""),
                              "process_json": str(process.relative_to(ASSEMBLY)).replace("\\", "/"),
                              "slice_log": str((work / "slice.log").relative_to(ASSEMBLY)).replace("\\", "/")})
    report = {"schema_version": 1, "assembly": "parent_oneplate", "job": "repeatable_mount",
              "source_manifest_sha256": source_hash, "plates": plate_reports}
    (JOBS / "slice_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
