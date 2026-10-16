"""Audit steep downward faces in the packaged print orientation (mm).

This geometric audit identifies short bridges; it is not a slicer simulation.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parents[2]
PRINT = ROOT / "assemblies/camera_housing_clasp/parts"
OUT = ROOT / "assemblies/camera_housing_clasp/_work/analysis/print_support"
OUT.mkdir(parents=True, exist_ok=True)

manifest = json.loads((PRINT / "manifest.json").read_text(encoding="utf-8"))
results = {}
for entry in manifest["parts"]:
    mesh = trimesh.load(PRINT / entry["file"], force="mesh")
    centers = mesh.triangles_center
    normals = mesh.face_normals
    areas = mesh.area_faces
    # More than 45 degrees past self-supporting. Exclude faces at the bed.
    mask = (normals[:, 2] < -0.72) & (centers[:, 2] > mesh.bounds[0, 2] + 0.4)
    face_ids = np.flatnonzero(mask)
    adjacency = mesh.face_adjacency
    connected = np.isin(adjacency[:, 0], face_ids) & np.isin(adjacency[:, 1], face_ids)
    groups = trimesh.graph.connected_components(adjacency[connected], nodes=face_ids, min_len=1)
    patches = []
    for group in sorted(groups, key=lambda g: areas[g].sum(), reverse=True):
        triangles = mesh.triangles[np.asarray(group)].reshape(-1, 3)
        bounds = np.vstack((triangles.min(axis=0), triangles.max(axis=0)))
        patches.append({
            "area_mm2": round(float(areas[group].sum()), 3),
            "bounds_mm": bounds.round(3).tolist(),
            "short_xy_span_mm": round(float(min(bounds[1, :2] - bounds[0, :2])), 3),
        })
    results[entry["file"]] = {
        "quantity": entry["quantity"],
        "print_rotation_deg": entry["rotation_deg"],
        "steep_downward_area_mm2": round(float(areas[mask].sum()), 3),
        "patches": patches,
    }

report = {
    "method": "Triangles steeper than 45 degrees below horizontal in packaged STL; bed faces omitted. Bridges and slicer support paths are not simulated.",
    "parts": results,
}
(OUT / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({k: [(p["area_mm2"], p["short_xy_span_mm"]) for p in v["patches"][:3]] for k, v in results.items()}, indent=2))
