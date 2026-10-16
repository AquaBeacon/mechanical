"""Reduce the oversized screening CAD and correct adapter interface clearance."""
from pathlib import Path
import json,os,subprocess,sys
import trimesh
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assemblies/child_petg100_design'
os.environ['PYTHONIOENCODING']='utf-8'
names=['child_jaw_gate','child_core_frame','child_cam_bridge']
metrics={}
for n in names:
 f=OUT/n;p=f/f'{n}.scad';s=p.read_text(encoding='utf-8')
 if n=='child_jaw_gate':s=s.replace('structural_radius=78;','structural_radius=72;')
 if n=='child_core_frame':
  s=s.replace('structural_radius=78;','structural_radius=70;').replace('back_halfwidth=40;','back_halfwidth=30;').replace('back_front=-58;','back_front=-75;')
 if n=='child_cam_bridge':
  # HP bosses reach one mm outside the nominal 50mm square. Keep the
  # machined-equivalent mounting plane at74.35, but clear everything behind it.
  s=s.replace('for(z=hp_z)box([-25,62.35,z-25],[25,hp_y,z+25]);','for(z=hp_z)box([-27,60,z-27],[27,hp_y,z+27]);')
  # The original8mm through-hole depth was insufficient after thickening the rear.
  s=s.replace('cylinder(d=5.4,h=8);','cylinder(d=5.4,h=12);')
 p.write_text(s,encoding='utf-8')
 for part in ['manufactured','preserve','obstacle','design_space','preserve_cuts']:
  with (f/f'{part}.log').open('w',encoding='utf-8') as log:
   subprocess.run(['C:/Program Files/OpenSCAD/openscad.exe','-o',str(f/f'{part}.stl'),'-D',f'part="{part}"',str(p)],stdout=log,stderr=log,check=True)
 m=trimesh.load(f/'manufactured.stl',force='mesh')
 metrics[n]={'volume_cm3':float(m.volume/1000),'mass_kg':float(m.volume*1.27e-6),'watertight':bool(m.is_watertight),'bounds_mm':m.bounds.tolist(),'shell_volumes_cm3':[float(c.volume/1000) for c in m.split()]}
 print(n,metrics[n],flush=True)
(OUT/'geometry_metrics.json').write_text(json.dumps(metrics,indent=2),encoding='utf-8')
bm=metrics['child_cam_bridge']['mass_kg'];gm=metrics['child_jaw_gate']['mass_kg']
for n in names:
 f=OUT/n
 for fn in ['fea.json','search.json']:
  p=f/fn;d=json.loads(p.read_text(encoding='utf-8'))
  if n=='child_jaw_gate':
   for ld in d['cases'][0]['loads']:ld['force']=[0,0,-(bm+.35)*9.81*3/2]
  if n=='child_core_frame':
   for ld in d['cases'][0]['loads']:
    if ld['region'] in ['latch_lo','latch_hi']:ld['force']=[0,0,-(gm+bm+.35)*9.81*3/2]
  p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
 dest=f/'validation_2mm';dest.mkdir(exist_ok=True)
 with (dest/'run.log').open('w',encoding='utf-8') as log:
  result=subprocess.run([sys.executable,'-m','topopt','fea',str(f/'fea.json'),'--out',str(dest),'--voxel','2','--no-png'],stdout=log,stderr=log)
 print('FEA2',n,result.returncode,flush=True)
