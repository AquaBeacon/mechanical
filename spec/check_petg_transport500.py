from pathlib import Path
import json,subprocess,sys,os
os.environ['PYTHONIOENCODING']='utf-8';O=Path('assemblies/child_petg100_design');S=O/'verification/studies'
for n in ['child_core_frame','child_jaw_gate']:
 d=json.loads((S/(n+'.json')).read_text(encoding='utf-8'));d['cases']=[c for c in d['cases'] if c['name'].startswith('L2')]
 for c in d['cases']:
  c['name']='Transport 500N (10kg at5g rounded up): '+c['name']
  for l in c['loads']:l['force']=[x*5/3 for x in l['force']]
 p=S/(n+'_transport500.json');p.write_text(json.dumps(d,indent=2),encoding='utf-8');dest=O/'verification'/(n+'_transport500');dest.mkdir(exist_ok=True)
 with (dest/'run.log').open('w') as f:subprocess.run([sys.executable,'-m','topopt','fea',str(p),'--out',str(dest),'--voxel','1.33','--no-png'],stdout=f,stderr=f)
