from pathlib import Path
import json,subprocess,sys,os
os.environ['PYTHONIOENCODING']='utf-8';O=Path('assemblies/child_petg100_design')
for n in ['child_core_frame','child_jaw_gate']:
 p=O/'search_final'/n/'continuation_mma';out=O/'smooth_assembly'/'extraction'/n;out.mkdir(parents=True,exist_ok=True)
 with (out/'extract.log').open('w',encoding='utf-8') as f:r=subprocess.run([sys.executable,'-m','topopt','extract',str(p/'opt'),'--study',str(p/'study.json'),'--out',str(out),'--levels','0.5','--pick','0.5','--no-fea'],stdout=f,stderr=f)
 print(n,r.returncode,flush=True)
