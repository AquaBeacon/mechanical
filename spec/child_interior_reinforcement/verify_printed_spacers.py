"""Geometric acceptance checks for the connected print set and installed bodies."""
import json
import sys
from pathlib import Path
import numpy as np
import trimesh

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scad/lib'))
from check_asm_contacts import load
from sync_printed_spacers import SPEC, PART

OUT=ROOT/'assemblies/child_interior/_work/analysis/printed_spacers_clearance'
OUT.mkdir(parents=True,exist_ok=True)
report={'meshes':{},'sections':{},'installed':[],'errors':[]}


def require(condition,message):
    if not condition:report['errors'].append(message)


def overlap(a,b):
    if np.any(a.bounds[0]>=b.bounds[1]-1e-5) or np.any(b.bounds[0]>=a.bounds[1]-1e-5):return 0.
    result=trimesh.boolean.intersection([a,b],engine='manifold',check_volume=False)
    return abs(float(result.volume)) if len(result.faces) else 0.


for stem,height in [('body10',10),('body12',12),('body30',30),('set',30)]:
    mesh=trimesh.load(ROOT/PART/f'child_spacer_set_{stem}.stl',force='mesh')
    components=len(mesh.split(only_watertight=False))
    report['meshes'][stem]=dict(watertight=bool(mesh.is_watertight),components=components,
        bounds_mm=mesh.bounds.tolist(),volume_mm3=float(mesh.volume))
    require(mesh.is_watertight and components==1,f'{stem}: not a single closed solid')
    require(abs(mesh.extents[2]-height)<.001,f'{stem}: wrong height')
    if stem!='set':
        require(abs(mesh.extents[1]-5.5)<.001 and 6.1<mesh.extents[0]<6.36,f'{stem}: wrong hex envelope')
        for diameter in (3.0,3.5):
            gauge=trimesh.creation.cylinder(radius=diameter/2,height=height+2,sections=192)
            gauge.apply_translation([0,0,height/2])
            volume=overlap(mesh,gauge)
            require(volume<.001,f'{stem}: diameter {diameter} gauge is obstructed')
        section=mesh.section(plane_origin=[0,0,height/2],plane_normal=[0,0,1])
        planar,_=section.to_2D()
        holes=planar.polygons_full[0].interiors
        # to_2D may shift the origin; measure the bore about its own centroid.
        from shapely.geometry import Polygon
        bore=Polygon(holes[0]); center=bore.centroid
        inscribed=2*center.distance(bore.boundary)
        report['meshes'][stem]['minimum_bore_diameter_mm']=inscribed
        require(inscribed>=3.499,f'{stem}: through-hole is smaller than 3.5 mm')
        old=trimesh.load(ROOT/f'parts/common/interior/cots/hex_spacer/hex_spacer_m3_mf{height}.stl',force='mesh')
        extra=trimesh.boolean.difference([mesh,old],engine='manifold')
        added=abs(float(extra.volume)) if len(extra.faces) else 0.
        report['meshes'][stem]['outside_original_hex_mm3']=added
        require(added<.001,f'{stem}: exceeds original purchased-body envelope')
    else:
        # Confirm the breakaway webs survive as geometry in both 0.2 mm layers.
        for z,expected in [(.1,1),(.3,1),(.5,5),(.7,4)]:
            section=mesh.section(plane_origin=[0,0,z],plane_normal=[0,0,1])
            planar,_=section.to_2D()
            count=len(planar.polygons_full)
            report['sections'][str(z)]=dict(regions=count,expected=expected)
            require(count==expected,f'set: wrong regions at Z{z}: {count}')

data=json.loads((ROOT/'assemblies/child_interior/placement.json').read_text(encoding='utf-8'))
rows={i['label']:i for i in data['items']}
meshes={label:load(ROOT,row) for label,row in rows.items()}
for label,(length,stud_length,projection) in SPEC.items():
    if label.startswith('flange_'):
        screw_label='flange_screw_'+label[-1]
        body=meshes[label];screw=meshes[screw_label]
        require(overlap(body,screw)<.001,f'{label}: M3 screw does not slide through spacer')
        unexpected=[]
        for name,m in meshes.items():
            if name in (label,screw_label,'flange_bot'):continue
            for kind,new in [('body',body),('screw',screw)]:
                volume=overlap(new,m)
                if volume>.01:unexpected.append(dict(kind=kind,other=name,volume_mm3=volume))
        require(not unexpected,f'{label}: unexpected intersections {unexpected}')
        report['installed'].append(dict(label=label,length_mm=length,through_screw_mm=26,
            flange_engagement_mm=4,unexpected_intersections=unexpected))
        continue
    body=meshes[label]; stud_label='spacer_stud_'+label;stud=meshes[stud_label]
    nut_label='spacer_nut_'+label;nut=meshes[nut_label]
    seat=12 if label.startswith('flange_') else 5.5
    beyond_nut=stud_length-projection-length-seat-2.4
    require(beyond_nut>=1,f'{label}: stud does not pass through the whole nut')
    require(overlap(body,stud)<.001,f'{label}: M3 stud does not slide through spacer')
    intentional={label,stud_label,nut_label}
    if label.startswith('flange_'):intentional.add('flange_bot') # metal M3 stud enters tapped flange
    else:intentional.add('vtray_deck') # metal M3 stud enters existing printed deck pilot
    unexpected=[]
    for name,m in meshes.items():
        if name in intentional:continue
        for kind,new in [('body',body),('stud',stud),('nut',nut)]:
            volume=overlap(new,m)
            if volume>.01:unexpected.append(dict(kind=kind,other=name,volume_mm3=volume))
    from verify_child_interior import matrix
    socket=trimesh.creation.annulus(r_min=3.3,r_max=4,height=50,sections=48)
    socket.apply_translation([0,0,25])
    socket.apply_transform(matrix(rows[nut_label]['ops']))
    socket_blockers=[]
    for name,m in meshes.items():
        if name in intentional or rows[name]['group'] in ('vessel','shell','camera'):continue
        volume=overlap(socket,m)
        if volume>.01:socket_blockers.append(dict(other=name,volume_mm3=volume))
    require(not socket_blockers,f'{label}: 8 mm socket blocked {socket_blockers}')
    report['installed'].append(dict(label=label,length_mm=length,stud_projection_mm=projection,
        thread_beyond_nut_mm=beyond_nut,socket_blockers=socket_blockers,unexpected_intersections=unexpected))
    require(not unexpected,f'{label}: unexpected intersections {unexpected}')

other=json.loads((ROOT/'assemblies/child_vertical_assembly/placement.json').read_text(encoding='utf-8'))
a={i['label']:i for i in data['items'] if i['group']=='interior'}
b={i['label']:i for i in other['items'] if i['group']=='interior'}
require(a==b,'The two interior placements differ')
report['pass']=not report['errors']
(OUT/'geometry.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
sys.exit(bool(report['errors']))
