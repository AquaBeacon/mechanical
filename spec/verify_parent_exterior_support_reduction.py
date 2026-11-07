"""Rev.6: retain the Rev.5 fixture checks and verify flat-bed rope tabs."""
import json
import math
import numpy as np
from pathlib import Path
from verify_parent_exterior_qr import intersection,probe
from verify_parent_exterior_universal import check_revision

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assemblies/parent_exterior/_work/analysis/support_reduction'

def check_support_revision(rows,meshes):
    result=check_revision(rows,meshes)
    frame=meshes['open_frame'];checks=[]
    for x in (-111.5,111.5):
        for y in (-23,23):
            # Actual 10.5 mm passage plus the route through the existing skid
            # window; flexible rope exits beyond the vessel's X=+/-105 sides.
            route=probe([x,y,-43],[x,y,22],10.4)
            hits=[dict(part=n,mm3=v) for n,m in meshes.items()
                  if (v:=intersection(m,route))>0.04]
            wall=120-abs(x)-10.5/2/math.cos(math.pi/32)
            mouth_walls=[]
            for z in (-19.99,-10,-0.81):
                direction=1 if x>0 else -1
                locations,_,_=frame.ray.intersects_location([[x+direction*.1,y,z]],[[direction,0,0]],multiple_hits=True)
                crossings=np.unique(np.round(locations[:,0]*direction,6))
                assert len(crossings)==2,(x,y,z,crossings)
                mouth_walls.append(float(crossings[1]-crossings[0]))
            checks.append(dict(feature='vertical_rope_passage',xy_mm=[x,y],
                               diameter_mm=10.4,collisions=hits,outer_wall_mm=wall,
                               box_gap_mm=abs(x)-105-10.5/2/math.cos(math.pi/32),
                               sampled_wall_mm=mouth_walls,minimum_sampled_mouth_wall_mm=min(mouth_walls),
                               passed=not hits and wall>3 and min(mouth_walls)>2.45))
    for s in (-1,1):
        p=probe([s*94,s*80,-19.9],[s*94,s*80,-8.1],4)
        fill=float(intersection(frame,p)/p.volume)
        checks.append(dict(feature='flat_bottom_end_arm_12mm',solid_fraction=fill,passed=fill>0.99))
    checks.append(dict(feature='no_geometry_below_bed_face',minimum_z_mm=float(frame.bounds[0,2]),
                       passed=bool(abs(frame.bounds[0,2]+20)<0.01)))
    result['support_reduction_geometry']=checks
    result['passed']=result['passed'] and all(c['passed'] for c in checks)
    return result

if __name__=='__main__':
    import verify_parent_exterior_qr as base
    OUT.mkdir(parents=True,exist_ok=True)
    raise SystemExit(base.main(OUT,bolt_on=True,fixture_checker=check_support_revision))
