"""Run with FreeCADCmd. Exact solid contacts for the simple child enclosure.

Only reads model sources and writes assemblies/child_simple_assembly/cad_checks.json.
Vessel/vessel contacts are outside this check; the new frame/vessel pairs are all checked.
"""
import json
import math
from pathlib import Path
import FreeCAD as App
import Part

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assemblies/child_simple_assembly"
data = json.loads((OUT / "placement.json").read_text(encoding="utf-8"))

def transform(ops):
    mat = App.Matrix()
    for op in ops:
        key, value = next(iter(op.items()))
        if key == "translate":
            m = App.Matrix()
            m.move(App.Vector(*value))
        elif key == "rotate":
            m = App.Rotation(value[2], value[1], value[0]).toMatrix()
        else:
            raise ValueError(key)
        mat = mat.multiply(m)
    return mat

shapes = {}
groups = {}
for item in data["items"]:
    name = item["label"]
    path = ROOT / item["part"] / ((item.get("file") or Path(item["part"]).name) + ".step")
    shape = Part.Shape()
    shape.read(str(path))
    shape = shape.transformGeometry(transform(item.get("ops", [])))
    shapes[name] = shape
    groups[name] = item["group"]

results = {"revision": "r3_rear_light", "parts": {}, "contacts": [], "hardware": [], "bearing_seats": [], "scope": "New frame against vessel; exposed bolts, nuts, tool access and four bearing shoulders. Includes rear light M3 40x40 interface. No actual cables or future mounts."}
for name, shape in shapes.items():
    if groups[name] == "frame":
        results["parts"][name] = {"valid": shape.isValid(), "solids": len(shape.Solids), "volume_mm3": shape.Volume}

names = list(shapes)
for i, a in enumerate(names):
    for b in names[i+1:]:
        if groups[a] != "frame" and groups[b] != "frame":
            continue
        common = shapes[a].common(shapes[b]).Volume
        distance = shapes[a].distToShape(shapes[b])[0]
        results["contacts"].append({"a": a, "b": b, "intersection_mm3": common, "gap_mm": distance, "pass": common < 0.01})

def check_envelope(name, shape, targets):
    volume = sum(shape.common(shapes[t]).Volume for t in targets)
    results["hardware"].append({"name": name, "intersection_mm3": volume, "pass": volume < 0.01})

all_names = list(shapes)
for side, zc, frame in [(1,100,"child_simple_front"),(-1,190,"child_simple_rear"),(-1,100,"child_simple_rear")]:
    for x in [-20,20]:
        for z in [zc-20,zc+20]:
            # M3 shaft in the full 8 mm pad, and through-nut side clearance.
            check_envelope(f"mount_shaft_{side}_{x}_{z}",Part.makeCylinder(1.5,14,App.Vector(x,side*68,z),App.Vector(0,side,0)),all_names)
            # Socket wrench envelope, 10 mm OD, stopping at the pad inner face.
            check_envelope(f"mount_nut_tool_{side}_{x}_{z}",Part.makeCylinder(5,5,App.Vector(x,side*69,z),App.Vector(0,side,0)),all_names)

for x in [-77,77]:
    for z in [20,180]:
        check_envelope(f"split_bolt_{x}_{z}",Part.makeCylinder(1.5,30,App.Vector(x,-15,z),App.Vector(0,1,0)),all_names)
        for side in [-1,1]:
            check_envelope(f"split_tool_{x}_{z}_{side}",Part.makeCylinder(5,15,App.Vector(x,side*10,z),App.Vector(0,side,0)),all_names)

for x in [-100,100]:
    for side in [-1,1]:
        for z in [-7,5]:
            check_envelope(f"guard_M3x35_{x}_{side}_{z}",Part.makeCylinder(1.5,35,App.Vector(x,side*10.5,z),App.Vector(0,side,0)),all_names)
            # 4 mm nut envelope includes common locking nuts; no pocket required.
            check_envelope(f"guard_nut_{x}_{side}_{z}",Part.makeCylinder(3.3,4,App.Vector(x,side*12.5,z),App.Vector(0,side,0)),all_names)
            check_envelope(f"guard_washer_inner_{x}_{side}_{z}",Part.makeCylinder(3.5,0.5,App.Vector(x,side*16.5,z),App.Vector(0,side,0)),all_names)
            check_envelope(f"guard_washer_outer_{x}_{side}_{z}",Part.makeCylinder(3.5,0.5,App.Vector(x,side*45,z),App.Vector(0,side,0)),all_names)
            # Entire straight tool approach remains open with vessel installed.
            check_envelope(f"guard_nut_tool_{x}_{side}_{z}",Part.makeCylinder(5,16.5,App.Vector(x,0,z),App.Vector(0,side,0)),all_names)
            check_envelope(f"guard_head_tool_{x}_{side}_{z}",Part.makeCylinder(5,20,App.Vector(x,side*45,z),App.Vector(0,side,0)),all_names)
        frame = 'child_simple_front' if side==1 else 'child_simple_rear'
        # A 0.04 mm slab straddles the shoulder. Both halves must be filled.
        probe=Part.makeBox(20,16,0.04,App.Vector(x-10,17 if side==1 else -33,-19.02))
        fv=probe.common(shapes[frame]).Volume
        gv=probe.common(shapes['child_simple_guard']).Volume
        results['bearing_seats'].append(dict(x=x,side=side,area_mm2=320,frame_volume=fv,guard_volume=gv,**{'pass': abs(fv-6.4)<0.01 and abs(gv-6.4)<0.01}))

results["pass"] = all(p["valid"] and p["solids"] == 1 for p in results["parts"].values()) and all(c["pass"] for c in results["contacts"]) and all(h["pass"] for h in results["hardware"]) and all(s['pass'] for s in results['bearing_seats'])
(OUT / "cad_checks.json").write_text(json.dumps(results,indent=2),encoding="utf-8")
print(json.dumps(results,indent=2),flush=True)
if not results["pass"]:
    raise RuntimeError("Simple child enclosure CAD verification failed; inspect cad_checks.json")
