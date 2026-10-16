"""Derive lower clamp tool keepouts from the canonical assembly and real screws."""
from pathlib import Path
import hashlib,json,sys
import numpy as np
import trimesh

PART=Path(__file__).resolve().parents[1]
ROOT=PART.parents[4]
sys.path.insert(0,str(ROOT/'tools'))
from prepare_child_horizontal_plate_frame import matrix,load_world

def main():
    path=ROOT/'assemblies/child_horizontal_plate_frame/placement.json'
    placement=json.loads(path.read_text(encoding='utf-8'))
    world=load_world(placement)
    lower=next(row for row,_ in world if row['label']=='clamp_linked_lower')
    inverse=np.linalg.inv(matrix(lower['ops']))
    cylinders=[];records=[]
    for row,mesh in world:
        if not row['label'].startswith('ballast_join_') or not row['label'].endswith('_screw'): continue
        seat=np.array(row['ops'][0]['translate']);axis=matrix(row['ops'][1:])[:3,2]
        head_height=np.max((mesh.vertices-seat)@axis)
        tool=trimesh.creation.cylinder(radius=4.5,height=70,sections=64)
        pose=matrix(row['ops']);pose[:3,3]=seat+axis*(head_height+.2+35)
        tool.apply_transform(inverse@pose)
        cylinders.append(tool)
        records.append(dict(screw=row['label'],driver_diameter_mm=8,radial_clearance_mm=.5,length_mm=70,
            local_centre_mm=tool.centroid.tolist()))
    envelope=trimesh.load(PART/'_work/analysis/topology_print/lower_design_space.stl',force='mesh')
    # Only material inside the allowed envelope matters. Keeps the old grid bbox.
    union=trimesh.boolean.union(cylinders,engine='manifold')
    keepout=trimesh.boolean.intersection([union,envelope],engine='manifold')
    preserve=trimesh.load(PART/'_work/analysis/topology_print/lower_preserve.stl',force='mesh')
    collision=trimesh.boolean.intersection([preserve,keepout],engine='manifold')
    if not collision.is_empty and abs(collision.volume)>.1: raise RuntimeError('Tool keepout intersects functional preserve')
    out=PART/'_work/analysis/topology_print/lower_access_tool_obstacles.stl'
    out.write_text(trimesh.exchange.stl.export_stl_ascii(keepout),encoding='ascii')
    report=dict(status='exploration_only',tools=records,volume_mm3=float(keepout.volume),
        placement_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
        note='Same 70 mm driver paths as the assembly validator, with 0.5 mm radial clearance; vessel removed before servicing C retainers.')
    out.with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    study_path=PART/'spec/lower_print_topology_study.json'
    study=json.loads(study_path.read_text(encoding='utf-8'))
    snapshot=PART/'_work/intermediate/topology_print/study_run03_lower.json'
    if not snapshot.exists(): snapshot.write_text(json.dumps(study,indent=2)+'\n',encoding='utf-8')
    study['geometry']['obstacle']['C_retainer_driver_access']=str(out)
    study['finish']['cut']['C_retainer_driver_access']=str(out)
    study['_tool_access']='Actual C-retainer 8 mm driver paths +0.5 mm radial clearance from assembly placement; no manual guessed positions.'
    study_path.write_text(json.dumps(study,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__': main()
