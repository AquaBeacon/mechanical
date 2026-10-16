"""Prepare supported warm starts. No modification of the optimizer or verdicts."""
from pathlib import Path
import json,subprocess,os,sys,hashlib
O=Path(__file__).resolve().parents[1]/'assemblies/child_petg100_design'
os.environ['PYTHONIOENCODING']='utf-8';os.environ['PYTHONUNBUFFERED']='1'
for n in ['child_jaw_gate','child_core_frame']:
 base=O/'search_final'/n;dst=base/'continuation';dst.mkdir(exist_ok=True)
 d=json.loads((base/'study.json').read_text(encoding='utf-8'))
 d['geometry']['design_space']='../design_space.stl'
 d['geometry']['preserve']['interfaces']['stl']='../preserve.stl'
 d['geometry']['obstacle']['keep_out']='../obstacle.stl'
 d['geometry']['optional_starting_shape']='../opt/study_final.stl'
 # Use the final continuation parameters reached by the previous run.
 d['design']['penal']=3.0
 d['design']['beta']=16.0
 d['design']['overhang']['ramp']=0.0
 d['_continuation']='Warm-start from prior thresholded shape; NOT exact checkpoint resume. Same geometry, loads, material, volume and convergence tolerances. 240-iteration cap with final penal=3/beta=16 and fully active overhang filter.'
 if 'finish' in d:del d['finish']
 p=dst/'study.json';p.write_text(json.dumps(d,indent=2),encoding='utf-8')
 with (dst/'setup.log').open('w',encoding='utf-8') as log:
  rc=subprocess.run([sys.executable,'-m','topopt','setup',str(p),'--out',str(dst/'setup'),'--iters','240'],stdout=log,stderr=log).returncode
 print(n,'setup',rc,flush=True)
