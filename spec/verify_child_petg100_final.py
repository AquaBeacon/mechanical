"""Validate the actual, STEP-verified print meshes, with100% PETG self weight."""
from pathlib import Path
import json,subprocess,sys,os,hashlib
import trimesh
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assemblies/child_petg100_design';CAD=OUT/'cad'
V=OUT/'verification';V.mkdir(exist_ok=True);S=V/'studies';S.mkdir(exist_ok=True)
os.environ['PYTHONIOENCODING']='utf-8'
names=['child_jaw_gate','child_core_frame','child_cam_bridge']
mass={p.stem.removesuffix('_print'):trimesh.load(p).volume*1.27e-6 for p in CAD.glob('*_print.stl')}
light_weight=(.3+mass['vertical_light_saddle']+mass['vertical_light_cap'])*9.81*3
td_weight=(.32+mass['td04a_socket'])*9.81*3
for name in names:
 d=json.loads((OUT/name/'fea.json').read_text(encoding='utf-8'))
 d['part']='../../cad/'+name+'_print.stl';d['infill']=1.;d['voxel_mm']=1.33
 d['_what']='Validation of actual STEP-verified print mesh, solid PETG.'
 if name=='child_jaw_gate':
  for ld in d['cases'][0]['loads']:ld['force']=[0,0,-(mass['child_cam_bridge']+.45)*9.81*3/2]
 if name=='child_core_frame':
  for ld in d['cases'][0]['loads']:
   if ld['region'] in ['latch_lo','latch_hi']:ld['force']=[0,0,-(mass['child_jaw_gate']+mass['child_cam_bridge']+.45)*9.81*3/2]
   if ld['region']=='td04a_hp1':ld['force']=[0,0,-td_weight]
  light_loads=[{'region':'light_hp','force':[0,0,-light_weight]},
      {'region':'light_hp_upper','force':[light_weight*42/38,0,0]},
      {'region':'light_hp_lower','force':[-light_weight*42/38,0,0]}]
  d['cases'][-1]['loads']=light_loads
  d['cases'][-1]['name']='L7 vertical light0.30kg plus actual clamp mass at3g, with conservative eccentric moment'
  d['cases'][0]['loads']+=light_loads
 if name=='child_cam_bridge':d['cases'][0]['name']='L1 camera0.35kg plus mounting/fasteners0.10kg at3g and actual adapter self-weight'
 d['_fixture_masses_kg']=mass
 study=S/(name+'.json');study.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
 mesh=CAD/(name+'_print.stl')
 (S/(name+'_input_hash.json')).write_text(json.dumps({'stl_sha256':hashlib.sha256(mesh.read_bytes()).hexdigest(),'study_sha256':hashlib.sha256(study.read_bytes()).hexdigest()},indent=2))
 dest=V/name;dest.mkdir(exist_ok=True)
 with (dest/'run.log').open('w',encoding='utf-8') as log:
  code=subprocess.run([sys.executable,'-m','topopt','fea',str(study),'--out',str(dest),'--voxel','1.33','--no-png'],stdout=log,stderr=log).returncode
 print(name,code,flush=True)
