"""Check actual positive-extrusion paths cross all eight necks in two layers."""
from pathlib import Path
import json,zipfile,re,math,sys
import trimesh
R=Path(__file__).resolve().parents[1];O=R/'assemblies/parent_hand_service';P=R/'parts/common/interior/printed/stack_spacers';W=O/'_work/analysis/simple_stack_20261010/after/parent_stack_spacer_set'
if '--case-correction' in sys.argv:W=O/'_work/analysis/case_cad_correction_20261010/slicing/after/parent_stack_spacer_set'
if '--corner-mounts' in sys.argv:W=O/'_work/analysis/corner_mounts_20261011/slicing/after/parent_stack_spacer_set'
if '--fixed-plates' in sys.argv:W=O/'_work/analysis/fixed_plates_20261011/slicing/after/parent_stack_spacer_set'
source=trimesh.load(P/'parent_stack_spacer_set.stl',force='mesh');placed=trimesh.load(W/'placed.stl',force='mesh');offset=placed.bounds[0]-source.bounds[0]
machine=json.loads((W.parents[1]/'machine.json').read_text(encoding='utf-8'))
# Bambu's X1C profile uses a (0,2) nozzle offset; emitted G-code subtracts it.
nozzle=[float(q) for q in machine['extruder_offset'][0].split('x')]
offset[:2]-=nozzle
members=json.loads((P/'set_members.json').read_text(encoding='utf-8'))['members'];hits={it['label']:set() for it in members}
with zipfile.ZipFile(W/'parent_stack_spacer_set.3mf') as z:
 code=z.read(next(n for n in z.namelist() if n.startswith('Metadata/plate_') and n.endswith('.gcode'))).decode('utf-8')
pos=[0.,0.,0.];last_e=0;relative=False;feature=''
def intersects(a,b,lo,hi):
 t0=0.;t1=1.
 for axis in range(2):
  delta=b[axis]-a[axis]
  if abs(delta)<1e-10:
   if not lo[axis]<=a[axis]<=hi[axis]:return False
  else:
   u,w=sorted([(lo[axis]-a[axis])/delta,(hi[axis]-a[axis])/delta]);t0=max(t0,u);t1=min(t1,w)
 return t0<=t1
for line in code.splitlines():
 if line.startswith('; FEATURE: '):feature=line[11:].strip()
 if line.startswith('M83'):relative=True
 if line.startswith('M82'):relative=False
 values={a:float(n) for a,n in re.findall(r'\b([XYZEIJ])(-?[0-9.]+)',line.split(';')[0])}
 if line.startswith('G92 '):last_e=values.get('E',last_e);continue
 if not line.startswith(('G0 ','G1 ','G2 ','G3 ')):continue
 target=[values.get(a,pos[i]) for i,a in enumerate('XYZ')]
 extrusion=values.get('E',0.) if relative else values.get('E',last_e)-last_e
 if 'E' in values and not relative:last_e=values['E']
 layer=round(target[2],3)
 path=[pos,target]
 if line.startswith(('G2 ','G3 ')):
  cx=pos[0]+values.get('I',0);cy=pos[1]+values.get('J',0)
  radius=math.hypot(pos[0]-cx,pos[1]-cy);start=math.atan2(pos[1]-cy,pos[0]-cx);end=math.atan2(target[1]-cy,target[0]-cx)
  angle=(end-start)%(2*math.pi) if line.startswith('G3 ') else -((start-end)%(2*math.pi))
  if abs(angle)<1e-9:angle=2*math.pi if line.startswith('G3 ') else -2*math.pi
  n=max(1,math.ceil(abs(angle)*radius/.05))
  path=[[cx+radius*math.cos(start+angle*i/n),cy+radius*math.sin(start+angle*i/n),target[2]] for i in range(n+1)]
 if extrusion>0 and layer in [.2,.4] and not any(q in feature.lower() for q in ['brim','skirt','support']):
  for it in members:
   x,y=it['neck_xy_mm'];x+=offset[0];y+=offset[1]
   hw=it['neck_width_mm']/2
   if any(intersects(a,b,[x-hw,y-.2],[x+hw,y+.2]) for a,b in zip(path,path[1:])):hits[it['label']].add(layer)
 pos=target
rows=[dict(label=n,extrusion_layers_mm=sorted(z),pass_=z=={.2,.4}) for n,z in hits.items()]
out=dict(status='PASS' if all(q['pass_'] for q in rows) else 'FAIL',checks=rows,limitation='Toolpaths establish printed neck presence, not physical break force or adhesion.')
(O/'stack_spacer_slice_checks.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print(out);assert out['status']=='PASS'
