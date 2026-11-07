"""Check the generated mount's contact patches and screw/tool clearances."""
from pathlib import Path
import sys, json, hashlib
import numpy as np
import trimesh
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'spec'))
from verify_parent_exterior_qr import intersection, probe
P=ROOT/'parts/child/exterior/printed/dji_osmo_action6_mount_m3'
if 'rear_bottom_keepout=' in (P/'camera_mount.scad').read_text(encoding='utf-8'):
    from verify_camera_bottom_clearance import main
    raise SystemExit(main())
OUT=P/'_work/analysis/compact_front_20261021'
m=trimesh.load(P/'camera_mount.stl',force='mesh')
checks=[]
# The 0.5 mm rear gap is not treated as contact. Sample the actual support flats
# at three depths and both transverse edges, entirely under the nominal case.
points=[[s*x,y,36.5] for s in (-1,1) for x in (28,32,36) for y in (-21,-12,-2)]
dist=trimesh.proximity.closest_point(m,points)[1]
checks.append(dict(name='two_case_bottom_contact_patches',max_distance_mm=float(max(dist)),passed=bool(max(dist)<0.01)))
case=trimesh.creation.box([95,45.9,75]);case.apply_translation([0,0,36.5+37.5])
v=intersection(m,case)
checks.append(dict(name='provisional_case_no_penetration',intersection_mm3=v,passed=v<0.01))
for s in (-1,1):
    # New shelves reserve a D12 straight tool passage. The central M5 fingers
    # are excluded from this large probe and checked separately below.
    v=intersection(m,probe([s*25,0,24],[s*50,0,24],12))
    checks.append(dict(name=f'side_tool_D12_{s}',intersection_mm3=v,passed=v<0.01))
v=intersection(m,probe([-60,0,24],[60,0,24],5))
checks.append(dict(name='M5_axis_through',intersection_mm3=v,passed=v<0.01))
for x in (-20,20):
    for z in (20,60):
        v=intersection(m,probe([x,-32,z],[x,-23,z],3.45))
        checks.append(dict(name=f'M3_hole_{x}_{z}',intersection_mm3=v,passed=v<0.01))
        v=intersection(m,probe([x,-19.85,z],[x,60,z],3))
        checks.append(dict(name=f'M3_driver_{x}_{z}',intersection_mm3=v,passed=v<0.01))
checks.append(dict(name='single_closed_solid',passed=bool(m.is_watertight and m.is_winding_consistent and len(m.split())==1)))
checks.append(dict(name='front_wall_removed_and_floor_shortened',max_y_mm=float(m.bounds[1,1]),
                   passed=bool(abs(m.bounds[1,1]-9)<.01 and abs(m.extents[0]-88)<.01)))
# Compare actual old/new surfaces only where functional material is retained.
old=P/'_work/analysis/compact_front_20261021/history/parts/child/exterior/printed/dji_osmo_action6_mount_m3/camera_mount.stl'
if old.exists():
    baseline=trimesh.load(old,force='mesh')
    for label,bounds in [('M5_fingers',[[-16,-8,8.01],[16,8,31.1]]),
                         ('left_rear_support',[[-38,-25.45,8.01],[-26,-.45,36.51]]),
                         ('right_rear_support',[[26,-25.45,8.01],[38,-.45,36.51]])]:
        lo,hi=np.array(bounds);region=trimesh.creation.box(hi-lo);region.apply_translation((lo+hi)/2)
        a=trimesh.boolean.intersection([baseline,region],engine='manifold',check_volume=False)
        b=trimesh.boolean.intersection([m,region],engine='manifold',check_volume=False)
        delta=max(0,abs(a.volume)+abs(b.volume)-2*intersection(a,b))
        checks.append(dict(name='unchanged_'+label,symmetric_difference_mm3=float(delta),passed=bool(delta<.05)))
result=dict(revision='compact_no_front_stop_20261021',source_sha256=hashlib.sha256((P/'camera_mount.stl').read_bytes()).hexdigest(),checks=checks,
    limits=['Case profile and bottom height are provisional, not a physical fit measurement.',
            'D12 straight driver envelope only: large thumbscrews/knobs are not certified.',
            'No load, creep or layer-strength certification.'],passed=all(c['passed'] for c in checks))
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'contact_checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
raise SystemExit(0 if result['passed'] else 1)
