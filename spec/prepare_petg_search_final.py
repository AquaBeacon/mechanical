from pathlib import Path
import json,subprocess,os,sys
R=Path(__file__).resolve().parents[1];O=R/'assemblies/child_petg100_design';C=O/'cad'
os.environ['PYTHONIOENCODING']='utf-8'
for n in ['child_jaw_gate','child_core_frame']:
 p=C/(n+'.scad');s=p.read_text(encoding='utf-8')
 s=s.replace('union(){obstacle_all();scene_voids();}','union(){obstacle_all();bore_void();scene_voids();}')
 p.write_text(s,encoding='utf-8')
 d=O/'search_final'/n;d.mkdir(parents=True,exist_ok=True)
 for part in ['preserve','obstacle','design_space']:
  with (d/(part+'.log')).open('w') as log:
   subprocess.run(['C:/Program Files/OpenSCAD/openscad.exe','-o',str(d/(part+'.stl')),'-D',f'part="{part}"',str(p)],stdout=log,stderr=log,check=True)
 st=json.loads((O/n/'search_coarse.json').read_text(encoding='utf-8'))
 for k in list(st):
  if k.startswith('_'):del st[k]
 st['_scope']='Exploratory topology map only; final manufactured CAD is checked separately. Full vessel bore excluded including preserved band levels. Gravity omitted in search because solver freezes density-dependent body load.'
 (d/'study.json').write_text(json.dumps(st,indent=2),encoding='utf-8')
 with (d/'setup.log').open('w') as log:
  rc=subprocess.run([sys.executable,'-m','topopt','setup',str(d/'study.json'),'--out',str(d/'setup'),'--iters','60'],stdout=log,stderr=log).returncode
 print(n,rc,flush=True)
