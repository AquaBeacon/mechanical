"""Correct load-path discontinuities exposed at2mm; preserve previous results."""
from pathlib import Path
import os,json,subprocess,sys
import trimesh
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assemblies/child_petg100_design'
os.environ['PYTHONIOENCODING']='utf-8'
for name in ['child_jaw_gate','child_core_frame']:
 f=OUT/name;p=f/f'{name}.scad';s=p.read_text(encoding='utf-8')
 if name=='child_jaw_gate':
  s=s.replace('translate([-60,64.35,44.95])cube([120,80,150.05]);','''difference(){
    translate([-60,64.35,44.95])cube([120,80,150.05]);
    // Adapter has matching HP-seat recesses; allow solid backing to the seats.
    for(z=[100,170])translate([-27,60,z-27])cube([54,14.35,54]);
  }''')
 else:
  s=s.replace('back_halfwidth=30;','back_halfwidth=40;')
  s=s.replace('box3([-75,-30,190],[75,0,ds_z1]);','''box3([-75,-30,190],[75,0,ds_z1]);
    for(s=[-1,1])box3([s>0?26:-44,-90,ds_z0],[s>0?44:-26,-50,ds_z1]);''')
  s=s.replace('module allowed_obstacles(){union(){obstacle_all();scene_voids();}}','module allowed_obstacles(){intersection(){design_space();union(){obstacle_all();scene_voids();}}}')
 p.write_text(s,encoding='utf-8')
 for part in ['manufactured','obstacle']:
  with (f/f'{part}.log').open('w',encoding='utf-8') as log:
   subprocess.run(['C:/Program Files/OpenSCAD/openscad.exe','-o',str(f/f'{part}.stl'),'-D',f'part="{part}"',str(p)],stdout=log,stderr=log,check=True)
 print('CAD',name,flush=True)
metrics={}
for n in ['child_jaw_gate','child_core_frame','child_cam_bridge']:
 m=trimesh.load(OUT/n/'manufactured.stl',force='mesh')
 metrics[n]={'mass_kg':float(m.volume*1.27e-6),'volume_cm3':float(m.volume/1000),'bounds_mm':m.bounds.tolist(),'watertight':bool(m.is_watertight),'shell_volumes_cm3':[float(c.volume/1000) for c in m.split()]}
(OUT/'geometry_metrics.json').write_text(json.dumps(metrics,indent=2),encoding='utf-8')
for n in metrics:
 f=OUT/n
 for fn in ['fea.json','search.json']:
  p=f/fn;d=json.loads(p.read_text(encoding='utf-8'))
  d['_camera_mass_allowance']='0.35kg camera plus0.10kg for its mounting bracket and fasteners.'
  downstream=metrics['child_cam_bridge']['mass_kg']+.45
  if n=='child_jaw_gate':
   for ld in d['cases'][0]['loads']:ld['force']=[0,0,-downstream*9.81*3/2]
  elif n=='child_core_frame':
   for ld in d['cases'][0]['loads']:
    if ld['region'] in ['latch_lo','latch_hi']:ld['force']=[0,0,-(downstream+metrics['child_jaw_gate']['mass_kg'])*9.81*3/2]
  elif n=='child_cam_bridge':d['cases'][0]['loads']=[{'region':'mount_C','force':[0,0,-.45*9.81*3]}]
  p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
 dest=f/'connected_2mm';dest.mkdir(exist_ok=True)
 with (dest/'run.log').open('w',encoding='utf-8') as log:
  code=subprocess.run([sys.executable,'-m','topopt','fea',str(f/'fea.json'),'--out',str(dest),'--voxel','2','--no-png'],stdout=log,stderr=log).returncode
 print('FEA2',n,code,flush=True)
