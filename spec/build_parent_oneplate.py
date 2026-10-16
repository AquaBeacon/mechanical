"""Build canonical parent_oneplate views and repeatable mount print plates.

Reads only the current assembly placement and its synchronized parts manifest.
It never edits placement.json or replaces the historic root-level 3MF.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path

import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parents[1]
ASSEMBLY = ROOT / "assemblies" / "parent_oneplate"
WORK = ASSEMBLY / "_work" / "analysis" / "repeatable_mount"
IMAGES = ASSEMBLY / "_work" / "images"
OUT = ASSEMBLY / "print_jobs" / "repeatable_mount"
BED = (256.0, 256.0)
BRIM = 5.0
EXCLUDED = (0.0, 0.0, 18.0, 28.0)


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render_views():
    placement = ASSEMBLY / "placement.json"
    view = ASSEMBLY / "parent_oneplate_view.scad"
    subprocess.run(["python", str(ROOT / "scad/lib/asm_gen.py"), str(placement), str(view)], check=True)
    openscad = Path(r"C:\Program Files\OpenSCAD\openscad.exe")
    if not openscad.is_file():
        raise FileNotFoundError(openscad)
    IMAGES.mkdir(parents=True, exist_ok=True)
    camera = ["--imgsize=1400,1050", "--viewall", "--autocenter", "--projection=o",
              "--camera=0,0,0,65,0,210,0", "--colorscheme=Tomorrow"]
    common = [str(openscad), "-o"]
    subprocess.run(common + [str(IMAGES / "parent_oneplate_overview.png")] + camera +
                   ["-D", "show_floats=false", "-D", "show_vessel=false", str(view)], check=True)
    subprocess.run(common + [str(IMAGES / "parent_oneplate_box_locating.png")] + camera +
                   ["-D", "show_floats=false", "-D", "show_vessel=true", "-D", "show_hardware=false",
                    "-D", "show_pads=false", str(view)], check=True)


def excluded_overlap(rect):
    return (min(rect[2], EXCLUDED[2]) - max(rect[0], EXCLUDED[0]) > 1e-6 and
            min(rect[3], EXCLUDED[3]) - max(rect[1], EXCLUDED[1]) > 1e-6)


def overlaps(a, b):
    return min(a[2], b[2]) - max(a[0], b[0]) > 1e-6 and min(a[3], b[3]) - max(a[1], b[1]) > 1e-6


def place_on_plates(instances):
    """Bottom-left rectangle packing; margins include the requested brim."""
    plates = []
    for item in sorted(instances, key=lambda x: x["rect"][0] * x["rect"][1], reverse=True):
        w, h = item["rect"]
        # A combined STL is one slicer object. Its object hull must also clear
        # X1C's front-left exclusion, even if individual islands avoid it.
        candidates = {(BRIM, 33.0)}
        for plate in plates:
            for row in plate:
                candidates.add((row["rect"][2] + BRIM, row["rect"][1]))
                candidates.add((row["rect"][0], row["rect"][3] + BRIM))
        candidates = sorted(candidates, key=lambda p: (p[1], p[0]))
        chosen = None
        for idx, plate in enumerate(plates):
            for x, y in candidates:
                rect = [x, y, x + w, y + h]
                if rect[2] <= BED[0] - BRIM + 1e-6 and rect[3] <= BED[1] - BRIM + 1e-6 and not excluded_overlap(rect) and all(not overlaps(rect, row["rect"]) for row in plate):
                    chosen = (idx, rect)
                    break
            if chosen:
                break
        if chosen is None:
            rect = [BRIM, 33.0, BRIM + w, 33.0 + h]
            if rect[2] > BED[0] - BRIM + 1e-6 or rect[3] > BED[1] - BRIM + 1e-6 or excluded_overlap(rect):
                raise ValueError(f"part does not fit X1C bed with brim: {item['file']} ({w:g}x{h:g})")
            plates.append([dict(item=item, rect=rect)])
        else:
            idx, rect = chosen
            plates[idx].append(dict(item=item, rect=rect))
    return plates


def main():
    placement = read(ASSEMBLY / "placement.json")
    manifest = read(ASSEMBLY / "parts" / "manifest.json")
    placement_items = placement.get("items", placement.get("parts", []))
    valid_sources = set()
    for row in placement_items:
        if row.get("print", True) and ("printed" in Path(row["part"]).parts or "jigs" in Path(row["part"]).parts):
            valid_sources.add((row["part"], row.get("file") or Path(row["part"]).name))

    instances = []
    skipped = []
    for entry in manifest.get("parts", []):
        key = (entry["part"], entry["stem"])
        if key not in valid_sources:
            continue
        if entry["stem"] == "camera_mount":
            skipped.append({"part": entry["stem"], "reason": "shared existing mount excluded from new print job"})
            continue
        source = ASSEMBLY / "parts" / entry["file"]
        if not source.is_file():
            raise FileNotFoundError(f"synced print STL missing: {source}")
        mesh = trimesh.load(source, force="mesh")
        if not mesh.is_watertight or not mesh.is_winding_consistent or len(mesh.split(only_watertight=False)) != 1:
            raise ValueError(f"print STL must be one closed mesh: {source}")
        extents = mesh.extents.astype(float)
        if len(extents) != 3 or not np.isfinite(extents).all():
            raise ValueError(f"invalid bounds: {source}")
        for n in range(entry["quantity"]):
            instances.append({"file": entry["file"], "source": source, "source_sha256": sha(source),
                              "part": entry["part"], "stem": entry["stem"], "instance": n + 1,
                              "quantity": entry["quantity"], "material": "PETG", "rotation_deg": entry["rotation_deg"],
                              "extents_mm": extents.tolist(), "rect": [float(extents[0] + 2 * BRIM), float(extents[1] + 2 * BRIM)],
                              "mesh": mesh.copy()})
    if not instances:
        raise ValueError("no eligible print parts found in placement and synchronized manifest")

    plates = place_on_plates(instances)
    OUT.mkdir(parents=True, exist_ok=True)
    plate_rows = []
    for number, rows in enumerate(plates, 1):
        meshes, parts = [], []
        for row in rows:
            item, rect = row["item"], row["rect"]
            mesh = item["mesh"].copy()
            mesh.apply_translation([rect[0] + BRIM - mesh.bounds[0, 0],
                                    rect[1] + BRIM - mesh.bounds[0, 1], -mesh.bounds[0, 2]])
            meshes.append(mesh)
            parts.append({k: item[k] for k in ("part", "stem", "file", "instance", "quantity", "material", "rotation_deg", "extents_mm", "source_sha256")}
                         | {"plate_xy_mm": [rect[0] + BRIM, rect[1] + BRIM], "brim_envelope_xy_mm": rect})
        combined = trimesh.util.concatenate(meshes)
        if len(combined.split(only_watertight=False)) != len(parts):
            raise ValueError(f"plate {number} has unexpected connected-component count")
        mesh_path = OUT / f"plate_{number}.stl"
        source_zero_faces = sum(int(np.count_nonzero(item["mesh"].area_faces == 0)) for item in (r["item"] for r in rows))
        combined.export(mesh_path, file_type="stl_ascii")
        saved = trimesh.load(mesh_path, force="mesh")
        saved_min, saved_max = saved.bounds
        if (not saved.is_watertight or not saved.is_winding_consistent or
                np.count_nonzero(saved.area_faces == 0) > source_zero_faces or
                len(saved.split(only_watertight=False)) != len(parts)):
            raise ValueError(f"invalid exported plate mesh: {mesh_path}")
        if (np.any(saved_min[:2] < -1e-5) or np.any(saved_max[:2] > np.asarray(BED) + 1e-5) or
                saved_min[2] < -1e-5 or saved_max[2] < -1e-5):
            raise ValueError(f"exported plate exceeds bed bounds: {mesh_path}; bounds={saved.bounds.tolist()}")
        plate_rows.append({"plate": number, "stl": mesh_path.name, "sha256": sha(mesh_path),
                           "bbox_min_mm": saved_min.round(4).tolist(), "bbox_max_mm": saved_max.round(4).tolist(),
                           "bbox_mm": saved.extents.round(4).tolist(), "closed_mesh": bool(saved.is_watertight),
                           "winding_consistent": bool(saved.is_winding_consistent),
                           "zero_area_faces": int(np.count_nonzero(saved.area_faces == 0)),
                           "part_count": len(parts), "parts": parts})
    result = {"schema_version": 1, "assembly": "parent_oneplate", "job": "repeatable_mount",
              "material": "PETG", "layer_height_mm": 0.20, "walls": 6, "top_layers": 6, "bottom_layers": 6,
              "infill_percent": 40, "supports": True, "brim_mm": BRIM, "bed_mm": list(BED),
              "excluded_zone_mm": list(EXCLUDED), "placement_sha256": sha(ASSEMBLY / "placement.json"),
              "source_manifest_sha256": sha(ASSEMBLY / "parts/manifest.json"), "skipped": skipped, "plates": plate_rows}
    (OUT / "manifest.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    render_views()
    print(json.dumps({"plates": len(plates), "instances": len(instances), "output": str(OUT), "manifest": result}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
