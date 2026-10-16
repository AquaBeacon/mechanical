"""Analysis-only surface remesh of the verified faceted STEP using Gmsh.

Canonical print STL is unchanged. No FEM or meshing algorithm is implemented
here: FreeCAD removeSplitter and Gmsh Mesh are existing CAD commands. Validate the
remeshed envelope before passing it to the installed topopt CLI.
"""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import numpy as np
import trimesh
import argparse

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT / "parts/child/exterior/printed/child_wte4_suspension_clamp"
SRC = PART / "child_wte4_suspension_clamp_half.stl"
WORK = PART / "_work/analysis/surface_remesh"


def main():
    global SRC, WORK
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stl', type=Path, help='analysis candidate STL; original print CAD remains unchanged')
    parser.add_argument('--out', type=Path, help='analysis output directory')
    args = parser.parse_args()
    if args.stl:
        SRC = args.stl.resolve()
    if args.out:
        WORK = args.out.resolve()
    WORK.mkdir(parents=True, exist_ok=True)
    dst = WORK / SRC.name
    geo = WORK / "surface.geo"
    env = os.environ.copy()
    env["ASM_ROOT"] = str(ROOT)
    env["CLAMP_ANALYSIS_WORK"] = str(WORK)
    if args.stl:
        env["CLAMP_ANALYSIS_STL"] = str(SRC)
    cad = subprocess.run([r"C:\Users\ryupc\AppData\Local\Programs\FreeCAD 1.0\bin\freecadcmd.exe",
                          str(ROOT / "tools/refine_child_clamp_step.py")], env=env,
                         capture_output=True, text=True)
    (WORK / "freecad.log").write_text(cad.stdout + cad.stderr, encoding="utf-8")
    if cad.returncode or not (WORK / "refined.step").exists():
        raise RuntimeError("FreeCAD STEP refinement failed")
    geo.write_text(f'''// Gmsh tutorial t20: mesh the verified faceted CAD boundary.
SetFactory("OpenCASCADE");
Merge "{(WORK / 'refined.step').as_posix()}";
Mesh.MeshSizeMin = 0.35;
Mesh.MeshSizeMax = 8;
Mesh.MeshSizeFromCurvature = 24;
Mesh.Algorithm = 6;
Mesh.Optimize = 1;
Mesh 2;
Save "{dst.as_posix()}";
''', encoding="utf-8")
    run = subprocess.run([r"C:\Users\ryupc\Tools\gmsh-4.15.2-Windows64\gmsh.exe",
                          str(geo), "-0"], capture_output=True, text=True)
    (WORK / "gmsh.log").write_text(run.stdout + run.stderr, encoding="utf-8")
    if run.returncode or not dst.exists():
        raise RuntimeError("Gmsh surface remesh failed: see gmsh.log")
    src, mesh = [trimesh.load(p, force="mesh") for p in (SRC, dst)]
    mesh.fix_normals()
    points = np.vstack([mesh.vertices, mesh.triangles_center])
    distances = trimesh.proximity.closest_point(src, points)[1]
    delta_v = abs(mesh.volume / src.volume - 1)
    delta_b = float(np.max(np.abs(mesh.bounds - src.bounds)))
    result = dict(source_sha256=hashlib.sha256(SRC.read_bytes()).hexdigest(),
                  triangles=len(mesh.faces), watertight=bool(mesh.is_watertight),
                  bodies=int(mesh.body_count), volume_relative_error=float(delta_v),
                  bounds_max_error_mm=delta_b, surface_max_error_mm=float(distances.max()),
                  pass_check=bool(mesh.is_watertight and mesh.body_count == 1 and
                                  delta_v < 0.005 and delta_b < 0.05 and distances.max() < 0.08))
    mesh.export(dst)
    result["remeshed_sha256"] = hashlib.sha256(dst.read_bytes()).hexdigest()
    (WORK / "geometry_comparison.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["pass_check"] else 1)


if __name__ == "__main__":
    main()
