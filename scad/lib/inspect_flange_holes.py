"""Extract axial circular features from the WTE4 flange STEP.

Run with FreeCADCmd.  The report is intentionally machine-readable JSON so the
mount coordinates used by the printed tray can be checked without relying on a
rendered view.
"""

import json
import math
import os

import Part


step_path = os.environ["FLANGE_STEP"]
shape = Part.read(step_path)


def r6(value):
    return round(float(value), 6)


circles = []
for edge in shape.Edges:
    curve = edge.Curve
    if not hasattr(curve, "Radius") or not hasattr(curve, "Center"):
        continue
    axis = getattr(curve, "Axis", None)
    if axis is None or abs(abs(float(axis.z)) - 1.0) > 1e-5:
        continue
    center = curve.Center
    circles.append(
        {
            "x": r6(center.x),
            "y": r6(center.y),
            "z": r6(center.z),
            "radius": r6(curve.Radius),
            "closed": bool(edge.isClosed()),
        }
    )

# Deduplicate seam/shared edges while preserving distinct Z levels.
unique = {}
for item in circles:
    key = tuple(item[k] for k in ("x", "y", "z", "radius"))
    unique[key] = item
circles = sorted(unique.values(), key=lambda c: (c["radius"], c["z"], c["x"], c["y"]))

# The manufacturer model is centred at the outer cylinder centre.  Infer that
# centre from the largest axial circle rather than baking in 57.15 mm.
outer = max(circles, key=lambda c: c["radius"])
cx, cy = outer["x"], outer["y"]

for item in circles:
    dx = item["x"] - cx
    dy = item["y"] - cy
    item["dx"] = r6(dx)
    item["dy"] = r6(dy)
    item["bcd_radius"] = r6(math.hypot(dx, dy))
    item["raw_angle_deg"] = r6(math.degrees(math.atan2(dy, dx)) % 360.0)
    # Bottom flange placement includes rotate([180,0,0]); X is unchanged and
    # Y is inverted.  This is the angle seen by the tray assembly.
    item["bottom_world_angle_deg"] = r6((-item["raw_angle_deg"]) % 360.0)

cylinders = []
for face in shape.Faces:
    surf = face.Surface
    if not hasattr(surf, "Radius") or not hasattr(surf, "Axis"):
        continue
    axis = surf.Axis
    if abs(abs(float(axis.z)) - 1.0) > 1e-5:
        continue
    pos = surf.Center if hasattr(surf, "Center") else surf.Position
    zs = [v.Point.z for v in face.Vertexes]
    cylinders.append(
        {
            "x": r6(pos.x),
            "y": r6(pos.y),
            "radius": r6(surf.Radius),
            "z_min": r6(min(zs)) if zs else None,
            "z_max": r6(max(zs)) if zs else None,
        }
    )

# The actual M3 thread axes have a 1.25 mm root-radius edge at Z=0.4 and
# lie exactly on the documented 47 mm pitch radius.  Nearby engraved symbols
# also contain small circles, so do not classify by diameter alone.
m3_edges = [
    c for c in circles
    if abs(c["radius"] - 1.25) <= 1e-4
    and abs(c["bcd_radius"] - 47.0) <= 1e-4
    and c["z"] <= 6.2
]
m3_centres = {}
for item in m3_edges:
    key = (item["x"], item["y"])
    rec = m3_centres.setdefault(
        key,
        {
            "raw_x": item["x"],
            "raw_y": item["y"],
            "dx": item["dx"],
            "dy": item["dy"],
            "bcd_radius": item["bcd_radius"],
            "raw_angle_deg": item["raw_angle_deg"],
            "bottom_world_angle_deg": item["bottom_world_angle_deg"],
            "edge_levels": [],
        },
    )
    rec["edge_levels"].append({"z": item["z"], "radius": item["radius"]})

for rec in m3_centres.values():
    axial_faces = [
        f for f in cylinders
        if abs(f["x"] - rec["raw_x"]) <= 1e-4
        and abs(f["y"] - rec["raw_y"]) <= 1e-4
        and 1.2 <= f["radius"] <= 1.3
        and f["z_min"] is not None
        and f["z_max"] is not None
        and f["z_min"] <= 6.2
    ]
    rec["thread_model_z_min"] = min(f["z_min"] for f in axial_faces)
    rec["thread_model_z_max"] = max(f["z_max"] for f in axial_faces)
    rec["modelled_thread_depth"] = r6(rec["thread_model_z_max"] - rec["thread_model_z_min"])

report = {
    "source": step_path,
    "bounds": {
        "x_min": r6(shape.BoundBox.XMin),
        "x_max": r6(shape.BoundBox.XMax),
        "y_min": r6(shape.BoundBox.YMin),
        "y_max": r6(shape.BoundBox.YMax),
        "z_min": r6(shape.BoundBox.ZMin),
        "z_max": r6(shape.BoundBox.ZMax),
    },
    "inferred_axis": {"x": cx, "y": cy},
    "m3_centres": sorted(m3_centres.values(), key=lambda c: c["bottom_world_angle_deg"]),
}
if os.environ.get("FLANGE_VERBOSE") == "1":
    report["axial_cylindrical_faces"] = sorted(
        cylinders, key=lambda c: (c["radius"], c["x"], c["y"], c["z_min"] or 0)
    )
    report["all_axial_circles"] = circles
print(json.dumps(report, indent=2, ensure_ascii=False))
