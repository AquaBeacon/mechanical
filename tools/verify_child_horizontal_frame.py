"""Verify actual manufactured solids, fastener envelopes and cage hole axes.

CAD clearance checks only. This does not qualify loads, joints or unselected
equipment attachment hardware. Reference cage geometry is never modified.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import trimesh
import manifold3d as mf

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assemblies/child_exterior_horizontal'
PART=ROOT/'parts/child/exterior/printed/child_exterior_open_frame'


def transform(ops):
    result=np.eye(4)
    for op in ops:
        for k,v in op.items():
            a=np.eye(4)
            if k=='translate':a[:3,3]=v
            elif k=='rotate':a=trimesh.transformations.euler_matrix(*np.radians(v))
            elif k=='mirror':
                n=np.asarray(v,dtype=float);n/=np.linalg.norm(n);a[:3,:3]-=2*np.outer(n,n)
            elif k=='scale':a[:3,:3]=np.diag(v)
            else:raise ValueError(k)
            result=result@a
    return result


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--skip-hardware',action='store_true');args=ap.parse_args()
    data=json.loads((OUT/'placement.json').read_text(encoding='utf-8'))
    meshes={};solids={};sources={};rows={};local={};errors=[]
    for it in data['items']:
        name=it['label'];src=ROOT/it['part']/(it['file']+'.stl')
        if src not in local:local[src]=trimesh.load(src,force='mesh')
        m=local[src].copy();m.apply_transform(transform(it.get('ops',[])))
        meshes[name]=m;rows[name]=it;sources[str(src.relative_to(ROOT))]=hashlib.sha256(src.read_bytes()).hexdigest()
    printed=[n for n,it in rows.items() if it.get('print')]
    reference=[n for n,it in rows.items() if it['group'] in ['vessel','clamps','equipment','ballast','foam']]
    def solid(name):
        if name not in solids:
            m=meshes[name]
            solids[name]=mf.Manifold(mf.Mesh(vert_properties=np.asarray(m.vertices,dtype=np.float32),
                                            tri_verts=np.asarray(m.faces,dtype=np.uint32)))
            if solids[name].is_empty():raise RuntimeError('Boolean solid rejected '+name)
        return solids[name]
    def overlap(a,b):
        ba,bb=meshes[a].bounds,meshes[b].bounds
        if np.any(np.minimum(ba[1],bb[1])-np.maximum(ba[0],bb[0])<=1e-4):return 0.
        return abs((solid(a)^solid(b)).volume())
    collisions=[];count=0
    pairs=[(a,b) for i,a in enumerate(printed) for b in printed[i+1:]]
    pairs += [(a,b) for a in printed for b in reference]
    for a,b in pairs:
        volume=overlap(a,b);count+=1
        if volume>.05:collisions.append(dict(a=a,b=b,intersection_mm3=volume))
    hardware_collisions=[];hardware_count=0
    if not args.skip_hardware:
        for n,it in rows.items():
            if it['group']!='hardware':continue
            for b in printed+([] if n.startswith('existing_') else reference):
                volume=overlap(n,b);hardware_count+=1
                if volume>.05:hardware_collisions.append(dict(a=n,b=b,intersection_mm3=volume))
    if collisions:errors.append('Printed geometry overlaps occupied reference/other printed geometry')
    if hardware_collisions:errors.append('Hardware intersects material outside its bore/seat')
    # Cylinder envelopes verify each original cage hole with a true 3 mm shaft.
    hole_results=[]
    for h in data['clamp_attachment']['holes']:
        p=np.asarray(h['axis_point_mm']);s=h['normal'][0]
        start=abs(p[0])-20;stop=abs(p[0])+9
        cyl=trimesh.creation.cylinder(radius=1.5,height=stop-start,sections=24)
        mat=trimesh.transformations.rotation_matrix(np.pi/2,[0,1,0]);mat[:3,3]=[s*(start+stop)/2,p[1],p[2]]
        cyl.apply_transform(mat)
        shaft=mf.Manifold(mf.Mesh(np.asarray(cyl.vertices,dtype=np.float32),np.asarray(cyl.faces,dtype=np.uint32)))
        volumes={n:abs((shaft^solid(n)).volume()) for n in [h['cage_label'],h['label']]}
        good=all(v<.01 for v in volumes.values())
        hole_results.append(dict(**h,shaft_intersection_mm3=volumes,pass_shaft=good))
        if not good:errors.append('Cage shaft obstructed '+str(p))
    # OD8 driver through each adapter's axial tool channel, measured as solid.
    tools=[]
    for h in data['clamp_attachment']['holes']:
        p=np.asarray(h['axis_point_mm']);s=h['normal'][0]
        a=abs(p[0])+14.1;b=180
        cyl=trimesh.creation.cylinder(radius=4,height=b-a,sections=32)
        mat=trimesh.transformations.rotation_matrix(np.pi/2,[0,1,0]);mat[:3,3]=[s*(a+b)/2,p[1],p[2]];cyl.apply_transform(mat)
        tool=mf.Manifold(mf.Mesh(np.asarray(cyl.vertices,dtype=np.float32),np.asarray(cyl.faces,dtype=np.uint32)))
        obstruction={}
        for n in printed:
            if np.any(np.minimum(cyl.bounds[1],meshes[n].bounds[1])-np.maximum(cyl.bounds[0],meshes[n].bounds[0])<=1e-4):continue
            v=abs((tool^solid(n)).volume())
            if v>.05:obstruction[n]=v
        tools.append(dict(axis=p.tolist(),obstruction_mm3=obstruction,pass_tool=not obstruction))
        if obstruction:errors.append('Cage driver blocked '+str(p))
    # Assembly fastener length must pass through the entire modelled M3 nut.
    schedule=json.loads((PART/'spec/fastener_schedule.json').read_text(encoding='utf-8'))
    engagement=[]
    for j in schedule['joints']:
        n=np.asarray(j['axis_outward']);head=np.asarray(j['head_seat_mm']);nut=np.asarray(j['nut_seat_mm'])
        near=float((head-nut)@n);far=near+2.4
        engagement.append(dict(label=j['label'],nut_depth_range_mm=[near,far],length_mm=j['length_mm'],
                               full_nut_engagement=j['length_mm']>=far-.001))
    if not all(j['full_nut_engagement'] for j in engagement):errors.append('Insufficient full nut engagement')
    bounds=np.array([m.bounds for m in meshes.values()]);extent=(bounds[:,1,:].max(axis=0)-bounds[:,0,:].min(axis=0)).tolist()
    report=dict(status='fit_prototype',pass_cad=not errors,errors=sorted(set(errors)),
                collisions=collisions,hardware_collisions=hardware_collisions,
                clearance_pairs_tested=count,hardware_pairs_tested=hardware_count,
                clamp_holes=hole_results,clamp_tools=tools,fastener_engagement=engagement,
                assembly_extents_mm=extent,printed_instances=len(printed),source_sha256=sources,
                limitations='No actual connectors, cable bend radius, straps, foam retention, split-joint/strength qualification')
    p=OUT/'_work/logs/cad_fit_checks.json';p.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('CAD clearance',report['pass_cad'],'printed clashes',len(collisions),'hardware clashes',len(hardware_collisions),
          'holes',sum(h['pass_shaft'] for h in hole_results),'/24','tools',sum(h['pass_tool'] for h in tools),'/24',flush=True)
    for v in collisions[:8]+hardware_collisions[:8]:print(v)
    if errors:raise SystemExit(1)


if __name__=='__main__':main()
