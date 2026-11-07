"""Rev.5 real-mesh validation of spare holes and monolithic locator joints."""
from pathlib import Path
import json
import numpy as np
import trimesh
from verify_parent_exterior_qr import intersection,probe,matrix
from verify_parent_exterior_bolt_on import check_fixtures

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assemblies/parent_exterior/_work/analysis/universal_plate'
PATTERN=ROOT/'spec/parent_oneplate_mounting_pattern.json'

def check_revision(rows,meshes):
    result=check_fixtures(rows,meshes,integrated=True)
    spec=json.loads(PATTERN.read_text(encoding='utf-8'))
    points=[[x,r['y']] for r in spec['rows'] for x in r['x']]
    assert len(points)==15 and len({tuple(p) for p in points})==15
    assert all(np.allclose((np.array(p)-spec['grid_origin_mm'])/spec['pitch_mm'],np.round((np.array(p)-spec['grid_origin_mm'])/spec['pitch_mm'])) for p in points)
    assert not any(n.startswith('bolt_on_') for n in rows),'Separate green locators/hardware remain'
    frame=meshes['open_frame'];checks=[];joints=[]
    example=spec['example_attachment']
    part=ROOT/'parts/common/interior/cots/screw'
    bolt=trimesh.load(part/(example['screw']+'.stl'),force='mesh')
    nut=trimesh.load(part/(example['nut']+'.stl'),force='mesh')
    fixed={n:m for n,m in meshes.items() if rows[n].get('removal_group') not in ('camera','td04a')}
    for x,y in points:
        bore=intersection(frame,probe([x,y,-20.1],[x,y,-0.7],4.4))
        b=bolt.copy();b.apply_transform(matrix([{'translate':[x,y,example['head_seat_z_mm']]},{'rotate':[180,0,0]}]))
        n=nut.copy();n.apply_translation([x,y,example['nut_bottom_z_mm']])
        # Seven-millimetre reference mounting pad, flat underside of the deck.
        pad=trimesh.creation.annulus(r_min=2.3,r_max=6,height=7,sections=48)
        pad.apply_translation([x,y,-23.5])
        driver=probe([x,y,-100],[x,y,-27.01],3.5)
        hits=[]
        for name,host in fixed.items():
            for label,m in [('screw',b),('nut',n),('fixture_pad',pad),('driver',driver)]:
                v=intersection(host,m)
                if v>0.04:hits.append(dict(host=name,probe=label,mm3=v))
        # Check actual nut and head seats, rather than only nominal hole centres.
        dnut=float(trimesh.proximity.closest_point(frame,[[x+3,y,-7.3]])[1][0])
        dpad=float(trimesh.proximity.closest_point(frame,[[x+5,y,-20]])[1][0])
        tip=float(b.bounds[1,2]);protrusion=float(tip-n.bounds[1,2])
        checks.append(dict(xy_mm=[x,y],bore_diameter_mm=4.4,bore_obstruction_mm3=bore,
                           example_screw=example['screw'],tip_z_mm=tip,box_bottom_gap_mm=-tip,
                           protrusion_beyond_nut_mm=protrusion,nut_floor_distance_mm=dnut,
                           fixture_seat_distance_mm=dpad,collisions=hits,
                           passed=bore<0.02 and not hits and max(dnut,dpad)<0.02 and tip<=-1.5 and protrusion>=1.4))
    # Old side/end screw voids must be filled, not hidden beneath integrated parts.
    for x in (-110,110):
        for y in (-8,8):
            p=probe([x,y,-19.5],[x,y,4],4)
            fill=float(intersection(frame,p)/p.volume)
            joints.append(dict(feature='filled_old_side_hole',xy_mm=[x,y],solid_fraction=fill,passed=fill>0.99))
    for s in (-1,1):
        for y in (52,62):
            p=probe([s*94,s*y,-19.5],[s*94,s*y,-1.3],4)
            fill=float(intersection(frame,p)/p.volume)
            joints.append(dict(feature='filled_old_end_hole',xy_mm=[s*94,s*y],solid_fraction=fill,passed=fill>0.99))
        p=probe([s*94,s*80,-17.9],[s*94,s*80,-8.1],4)
        fill=float(intersection(frame,p)/p.volume)
        joints.append(dict(feature='integral_end_arm_10mm',xy_mm=[s*94,s*80],solid_fraction=fill,passed=fill>0.99))
    result['spare_mounting_holes']=checks
    result['integral_joints']=joints
    result['spare_hole_count']=len(points)
    result['passed']=result['passed'] and all(c['passed'] for c in checks+joints)
    result['limits']='Example fixture diameter 12/thickness 7 with M4x25 only. Remove moving camera/TD units for driver access; fit nuts before vessel. Future fixture envelopes, loads and physical strength require their own checks.'
    return result

if __name__=='__main__':
    import verify_parent_exterior_qr as base
    raise SystemExit(base.main(OUT,bolt_on=True,fixture_checker=check_revision))
