"""Export placement.json as one STL without expensive mesh booleans.

Each source STL is transformed exactly like asm_gen.py/asm_to_step.py and its
triangles are appended to the output mesh.  Disconnected watertight shells are
valid in an assembly STL and avoid OpenSCAD re-tessellating detailed PCB meshes.
"""

import json
import os
import sys

import FreeCAD
import Mesh


def log(*args):
    print("[asm2stl]", *args)
    sys.stdout.flush()


asm_json = os.environ["ASM_JSON"]
root = os.environ["ASM_ROOT"]
dst = os.environ["STL_OUT"]
group_filter = os.environ.get("ASM_GROUP", "").strip()

with open(asm_json, encoding="utf-8") as handle:
    asm = json.load(handle)


def m_translate(v):
    matrix = FreeCAD.Matrix()
    matrix.move(FreeCAD.Vector(*[float(x) for x in v]))
    return matrix


def m_rotate(v):
    return FreeCAD.Rotation(float(v[2]), float(v[1]), float(v[0])).toMatrix()


def m_mirror(v):
    n = [float(x) for x in v]
    denom = sum(x * x for x in n)
    if denom == 0:
        return FreeCAD.Matrix()
    values = [[(1.0 if i == j else 0.0) - 2.0 * n[i] * n[j] / denom for j in range(3)] for i in range(3)]
    return FreeCAD.Matrix(
        values[0][0], values[0][1], values[0][2], 0,
        values[1][0], values[1][1], values[1][2], 0,
        values[2][0], values[2][1], values[2][2], 0,
        0, 0, 0, 1,
    )


def m_scale(v):
    return FreeCAD.Matrix(
        float(v[0]), 0, 0, 0,
        0, float(v[1]), 0, 0,
        0, 0, float(v[2]), 0,
        0, 0, 0, 1,
    )


builders = {"translate": m_translate, "rotate": m_rotate, "mirror": m_mirror, "scale": m_scale}


def total_matrix(ops):
    matrix = FreeCAD.Matrix()
    for op in ops or []:
        for kind, value in op.items():
            matrix = matrix.multiply(builders[kind](value))
    return matrix


assembly = Mesh.Mesh()
made = 0
missing = []
for item in asm.get("items", asm.get("parts", [])):
    if group_filter and item.get("group", "") != group_filter:
        continue
    part = item["part"].strip("/").replace("/", os.sep)
    stem = item.get("file") or os.path.basename(part)
    path = os.path.join(root, part, stem + ".stl")
    if not os.path.exists(path):
        missing.append(os.path.relpath(path, root))
        continue
    component = Mesh.Mesh(path)
    component.transform(total_matrix(item.get("ops")))
    assembly.addMesh(component)
    made += 1

if made == 0:
    raise SystemExit("no source STL files were found")

assembly.write(dst)
log("wrote", dst, "parts=", made, "missing=", len(missing), "facets=", assembly.CountFacets)
for path in missing:
    log("MISSING", path)
if missing:
    sys.exit(1)
