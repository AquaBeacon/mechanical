"""Verify actual generated meshes, locating contacts and tool envelopes."""
from pathlib import Path
import json, sys, hashlib
import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT / "scad/lib"))
from check_asm_contacts import matrix
OUT = ROOT / "assemblies/parent_oneplate/_work/analysis/repeatable_mount"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def intersection(a,b):
    if np.any(np.minimum(a.bounds[1],b.bounds[1])-np.maximum(a.bounds[0],b.bounds[0]) <= 1e-7):
        return 0.0
    mesh=trimesh.boolean.intersection([a,b],engine="manifold",check_volume=False)
    return 0.0 if mesh is None else float(abs(mesh.volume))

def cylinder(p0,p1,diameter):
    mesh=trimesh.creation.cylinder(radius=diameter/2,sections=48,segment=np.array([p0,p1]))
    return mesh

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    path=ROOT / "assemblies/parent_oneplate/placement.json"
    data=json.loads(path.read_text(encoding="utf-8"))
    items={}
    meshes={}
    source_checks=[]
    for item in data["items"]:
        label=item["label"]
        # Floats/lid/pads and historic simplified rods are not precision interfaces.
        selected=(item["group"]=="exterior" or label in ("camera_mount","box_bcas212310g","td04a_actual_shape_reference","camera_case_reference") or label.startswith("locating_"))
        if not selected:
            continue
        source=ROOT / item["part"] / ((item.get("file") or Path(item["part"]).name)+".stl")
        mesh=trimesh.load(source,force="mesh")
        if "printed" in Path(item["part"]).parts:
            source_checks.append(dict(label=label,file=str(source.relative_to(ROOT)),sha256=sha(source),bounds_mm=mesh.bounds.tolist(),volume_mm3=float(mesh.volume),watertight=bool(mesh.is_watertight),winding_consistent=bool(mesh.is_winding_consistent),components=len(mesh.split(only_watertight=False)),zero_area_faces=int(np.count_nonzero(mesh.area_faces<1e-15))))
        mesh.apply_transform(matrix(item.get("ops",[])))
        meshes[label]=mesh
        items[label]=item
    collisions=[]
    names=list(meshes)
    for n,a in enumerate(names):
        for b in names[n+1:]:
            if items[a]["group"]=="hardware" and items[b]["group"]=="hardware":
                continue
            if not any(items[k]["group"]=="exterior" for k in (a,b)):
                continue
            volume=intersection(meshes[a],meshes[b])
            if volume > 0.02:
                collisions.append(dict(a=a,b=b,volume_mm3=volume))
    frame=meshes["open_frame"]
    bores=[]
    for x in (-60,-20):
        for y in (-20,20):
            obstruction=intersection(frame,cylinder([x,y,-25],[x,y,1],3.5))
            bores.append(dict(x=x,y=y,diameter_mm=3.5,obstruction_mm3=obstruction,through=obstruction<0.01))
    # Hard contact points lie in the flat centre of a face, not on a chamfer.
    contact_points={
        "bottom_datum_1":("open_frame",[-96,-55,0]),
        "bottom_datum_2":("open_frame",[-96,55,0]),
        "bottom_datum_3":("open_frame",[96,0,0]),
        "left_datum_1":("locating_side_left",[-105,-38,8]),
        "left_datum_2":("locating_side_left",[-105,38,8]),
        "end_datum":("locating_end_fixed",[94,115,8]),
        "camera_end_1":("open_frame",[-60,44.5,-26]),
        "camera_end_2":("open_frame",[-20,44.5,-26]),
        "camera_right":("open_frame",[2,39,-26]),
        "td_left":("sensor_carrier",[43,1,-35]),
        "td_end":("sensor_carrier",[55,1,-27]),
    }
    contacts=[]
    for label,(host,p) in contact_points.items():
        distance=float(trimesh.proximity.closest_point(meshes[host],np.array([p]))[1][0])
        contacts.append(dict(label=label,host=host,point_mm=p,surface_distance_mm=distance,on_surface=distance<0.02))
    # Check new fastener access; old camera M3 axes retain their existing routes.
    tools=[]
    def tool(label,probe,exclude):
        hits=[]
        for name,m in meshes.items():
            if name in exclude or items[name]["group"]=="hardware" or name=="camera_case_reference":
                continue
            volume=intersection(probe,m)
            if volume>0.02:
                hits.append(dict(part=name,volume_mm3=volume))
        tools.append(dict(label=label,diameter_mm=6,collisions=hits))
    for y in (-38,38):
        tool(f"right_pressure_locknut_{y}",cylinder([121,y,12],[151,y,12],6),set())
    tool("end_pressure_locknut",cylinder([-94,-151,9],[-94,-133,9],6),set())
    for x in (-110,110):
        for y in (-8,8):
            tool(f"side_stop_head_{x}_{y}",cylinder([x,y,5.5],[x,y,30],6),set())
    # Under-arm heads remain accessible with the box installed.
    for s in (-1,1):
        for y in (52,62):
            tool(f"end_arm_head_{s}_{y}",cylinder([s*94,s*y,-45],[s*94,s*y,-18.5],6),set())
    ok=(not collisions and all(c["watertight"] and c["winding_consistent"] and c["components"]==1 and c["zero_area_faces"]==0 for c in source_checks) and all(b["through"] for b in bores) and all(c["on_surface"] for c in contacts) and not any(t["collisions"] for t in tools))
    report=dict(placement_sha256=sha(path),method="Manifold triangle-mesh Boolean intersection, exact nominal contact samples, 48-sided cylindrical tool envelopes",passed=ok,printed_meshes=source_checks,collisions=collisions,camera_through_bores=bores,locating_contacts=contacts,tool_paths=tools,limitations=["Nominal COTS geometry: real box taper, TD metal bracket and camera-case dimensions need fitting.","This is geometric validation, not a load test, a print trial or proof of repeatability.","Existing float straps, actual cable bend radius, seals and omitted historic hardware envelopes are not certified."])
    (OUT / "geometry_checks.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"passed":ok,"collisions":collisions,"failed_meshes":[m["label"] for m in source_checks if not m["watertight"] or m["zero_area_faces"]],"failed_contacts":[c for c in contacts if not c["on_surface"]],"failed_tools":[t for t in tools if t["collisions"]]},indent=2))
    raise SystemExit(0 if ok else 1)

if __name__=="__main__":
    main()
