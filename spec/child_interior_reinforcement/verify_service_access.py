"""Volume-intersection checks of service clearance and floor release motion."""
import json,sys
from pathlib import Path
import numpy as np
import trimesh
sys.path.insert(0,str(Path('scad/lib').resolve()))
from check_asm_contacts import load
np.random.seed(27)
items=json.loads(Path('assemblies/child_interior/placement.json').read_text(encoding='utf-8'))['items']
meshes={it['label']:load(Path('.'),it) for it in items}
for m in meshes.values():m.fix_normals()
errors=[];result=[]
def check(label,a,b):
 if np.any(a.bounds[0]>=b.bounds[1]-0.001) or np.any(b.bounds[0]>=a.bounds[1]-0.001):return
 c=trimesh.boolean.intersection([a,b],engine='manifold',check_volume=False)
 v=abs(c.volume) if c is not None and len(c.faces) else 0
 result.append({'pair':label,'overlap_mm3':round(v,6)})
 if v>0.01:errors.append(result[-1])
changed=('vtray_deck','vtray_batt_box','vtray_batt_floor','flange_brace','vtray_rib_top')+tuple(it['label'] for it in items if it['part'].endswith('/child_rx_edge_clamp'))
for n in changed:
 m=meshes[n];assert m.is_volume and len(m.split())==1,n
 for it in items:
  other=it['label']
  if other==n or '/cots/screw' in it['part'] or '/cots/hex_spacer' in it['part'] or 'harness' in other:continue
  check(f'{n}/{other}',m,meshes[other])
wire=trimesh.load('spec/child_interior_reinforcement/service_wire_keepout.stl',force='mesh')
for n in changed:check(f'wire_reserve/{n}',wire,meshes[n])
# 6 mm diameter straight tool shank, from outside to the countersunk seat.
bit=trimesh.creation.cylinder(radius=3,height=57,sections=48)
bit.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[1,0,0]));bit.apply_translation([22.5,-71.5,36])
for n,m in meshes.items():
 if n in ('batt_floor_screw','acrylic_tube_200') or 'harness' in n:continue
 check(f'tool/{n}',bit,m)
# Floor: slide toward cap 2 mm, then withdraw along -Y. Remove screw beforehand.
fixed=['vtray_batt_box','lipo','vtray_deck','flange_bot','flange_top','end_cap_bottom','dome_top','rx_improved_mini']+[x for x in meshes if x.startswith(('penetrator_','lipo_foam'))]
for dz,dy in [(float(z),0) for z in np.linspace(0,-2,9)]+[(-2,float(y)) for y in np.linspace(-0.5,-45,20)]:
 m=meshes['vtray_batt_floor'].copy();m.apply_translation([0,dy,dz])
 for n in fixed:
  if n in meshes:check(f'floor_move_z{dz:.2f}_y{dy:.2f}/{n}',m,meshes[n])
report={'errors':errors,'checks':result,'wire_envelope_d_mm':9,'floor_release_z_mm':-2,'tool_d_mm':6}
Path('spec/child_interior_reinforcement/service_checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('errors',errors,'tested intersections',len(result),flush=True)
sys.exit(bool(errors))
