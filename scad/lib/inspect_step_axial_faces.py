r"""Dump every Z-axial cylindrical face of a STEP as JSON (holes, bosses, bores).

Generic companion to inspect_flange_holes.py: used 2026-09-03 to prove that the
WTE4 end cap (BR-102993-005) has no interior tapped holes and that the 4x M3
BCD94 tray holes are on the flange (BR-101040). Run with FreeCADCmd:

    $env:STEP = "parts\child\exterior\cots\wte4_end_cap_5xm10\WTE4-M-END-CAP-5XM10-R2.step"
    & "$FC" scad\lib\inspect_step_axial_faces.py

bcd_r / ang are measured from the bounding-box centre. Group the output by
(r, bcd_r) to read hole circles; see wte4_flange/ref/BR-101040_hole_map.png.
"""
import json, math, os
import Part

shape = Part.read(os.environ["STEP"])
bb = shape.BoundBox
cx, cy = (bb.XMin + bb.XMax) / 2, (bb.YMin + bb.YMax) / 2
faces = []
for f in shape.Faces:
    s = f.Surface
    if not hasattr(s, "Radius") or not hasattr(s, "Axis"):
        continue
    if abs(abs(float(s.Axis.z)) - 1.0) > 1e-5:
        continue
    p = s.Center if hasattr(s, "Center") else s.Position
    zs = [v.Point.z for v in f.Vertexes]
    faces.append({
        "x": round(p.x, 3), "y": round(p.y, 3), "r": round(s.Radius, 3),
        "zmin": round(min(zs), 3) if zs else None, "zmax": round(max(zs), 3) if zs else None,
        "bcd_r": round(math.hypot(p.x - cx, p.y - cy), 3),
        "ang": round(math.degrees(math.atan2(p.y - cy, p.x - cx)) % 360, 2),
    })
uniq = {}
for f in faces:
    uniq[(f["x"], f["y"], f["r"], f["zmin"], f["zmax"])] = f
faces = sorted(uniq.values(), key=lambda f: (f["r"], f["bcd_r"], f["ang"], f["zmin"] or 0))
print(json.dumps({"bounds": [round(v, 3) for v in (bb.XMin, bb.XMax, bb.YMin, bb.YMax, bb.ZMin, bb.ZMax)],
                  "centre": [round(cx, 3), round(cy, 3)], "faces": faces}, indent=1))
