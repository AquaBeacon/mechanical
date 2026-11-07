"""Real-mesh checks for Rev.7 and compatibility with the already printed parts."""
from pathlib import Path
import json,hashlib
import numpy as np
import trimesh
from verify_parent_exterior_qr import intersection,probe,matrix,main as assembly_checks
from verify_parent_exterior_bolt_on import check_fixtures

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'assemblies/parent_exterior'
OUT=A/'_work/analysis/removable_locators_20261022'

def check(rows,meshes):
    common=check_fixtures(rows,meshes,integrated=True)
    checks=[];frame=meshes['open_frame']
    def clearance(name,shape,hosts):
        hits=[dict(part=n,mm3=v) for n in hosts if (v:=intersection(shape,meshes[n]))>.04]
        checks.append(dict(feature=name,collisions=hits,passed=not hits))
    def contact(name,xyz):
        d=float(trimesh.proximity.closest_point(meshes[name],[xyz])[1][0])
        checks.append(dict(feature='seat',host=name,point_mm=xyz,distance_mm=d,passed=d<.02))
    for side in (True,False):
        for s in (-1,1):
            for y in ((-8,8) if side else (52,62)):
                x=s*(110 if side else 94);y=y if side else s*y
                host='bolt_on_'+(('side_left' if s<0 else 'side_right') if side else ('end_push' if s<0 else 'end_fixed'))
                suffix=f'side_{s*110}_{y}' if side else f'end_{s}_{abs(y)}'
                bn='bolt_on_'+('side_bolt_'+f'{s*110}_{y}' if side else 'end_bolt_'+f'{s}_{abs(y)}')
                nn='bolt_on_'+('side_nut_'+f'{s*110}_{y}' if side else 'end_nut_'+f'{s}_{abs(y)}')
                seat=1.3 if side else -27.3
                floor=-15.5 if side else -7.3
                clearance('bore_'+suffix,probe([x,y,min(-20,seat)],[x,y,max(-.8,seat)],4.4),[host,'open_frame'])
                contact(host,[x+3,y,seat]);contact(bn,[x+3,y,seat])
                contact('open_frame',[x+3,y,-12.3 if side else floor])
                contact(nn,[x+3,y,-12.3 if side else floor])
                contact(host,[x+3,y,-.8 if side else -20]);contact('open_frame',[x+3,y,-.8 if side else -20])
                start,end=([x,y,seat+.01],[x,y,45]) if side else ([x,y,-100],[x,y,seat-.01])
                clearance('driver_'+suffix,probe(start,end,3.5),[n for n in meshes if rows[n]['group'] not in ('hardware','pads')])
                b=meshes[bn].bounds;n=meshes[nn].bounds
                tip=float(b[0 if side else 1,2]);protrusion=float(n[0,2]-tip if side else tip-n[1,2])
                checks.append(dict(feature='screw_tip_'+suffix,tip_z_mm=tip,protrusion_mm=protrusion,
                                   skid_gap_mm=tip+20 if side else None,vessel_gap_mm=-tip if not side else None,
                                   passed=protrusion>1.39 and (tip>-19 if side else tip<-1.5)))
    for x in (-111.5,111.5):
        for y in (-23,23):
            clearance('rope',probe([x,y,-43],[x,y,22],10.4),list(meshes))
    pattern=json.loads((ROOT/'spec/parent_oneplate_mounting_pattern.json').read_text())
    screw=trimesh.load(ROOT/'parts/common/interior/cots/screw/screw_m4x25_socket.stl',force='mesh')
    nut=trimesh.load(ROOT/'parts/common/interior/cots/screw/screw_nut_m4.stl',force='mesh')
    fixed=[n for n in meshes if rows[n].get('removal_group') not in ('camera','td04a')]
    for row in pattern['rows']:
        for x in row['x']:
            y=row['y'];b=screw.copy();b.apply_transform(matrix([{'translate':[x,y,-27]},{'rotate':[180,0,0]}]))
            n=nut.copy();n.apply_translation([x,y,-7.3])
            pad=trimesh.creation.annulus(r_min=2.3,r_max=6,height=7,sections=48);pad.apply_translation([x,y,-23.5])
            for label,shape in [('spare_bore',probe([x,y,-20],[x,y,-.8],4.4)),('spare_screw',b),('spare_nut',n),
                                ('spare_fixture',pad),('spare_driver',probe([x,y,-100],[x,y,-27.01],3.5))]:
                clearance(label+f'_{x}_{y}',shape,fixed)
    printed=[]
    for stem in ('parent_oneplate_bar','parent_oneplate_stand'):
        old=trimesh.load(OUT/'history/printed_parts'/(stem+'.stl'),force='mesh')
        new=trimesh.load(ROOT/'parts/parent/exterior/printed'/stem/(stem+'.stl'),force='mesh')
        if stem.endswith('stand'):new.apply_transform(trimesh.transformations.euler_matrix(0,np.pi/2,0))
        new.apply_translation(-new.bounds[0])
        delta=float(np.max(abs(new.bounds-old.bounds)))
        diff=sum(abs(trimesh.boolean.difference([a,b],engine='manifold',check_volume=False).volume) for a,b in [(new,old),(old,new)])
        printed.append(dict(part=stem,bounds_delta_mm=delta,symmetric_difference_mm3=float(diff),
                            passed=bool(delta<.001 and diff<.05)))
    result=dict(common=common,checks=checks,already_printed_compatibility=printed,
                passed=common['passed'] and all(c['passed'] for c in checks+printed))
    return result

if __name__=='__main__':raise SystemExit(assembly_checks(OUT,bolt_on=True,fixture_checker=check))
