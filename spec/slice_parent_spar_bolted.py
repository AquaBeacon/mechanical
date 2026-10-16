"""Offline Bambu Studio verification. Does NOT send jobs to a printer."""
from pathlib import Path
import json,subprocess,sys,os
import trimesh,numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'print_jobs/parent_spar_bolted'
WORK=OUT/'slice_validation';WORK.mkdir(exist_ok=True)
PROFILES=Path(r'C:\Program Files\Bambu Studio\resources\profiles\BBL')
CLI=r'C:\Program Files\Bambu Studio\bambu-studio.exe'
index={p.stem:p for p in PROFILES.rglob('*.json')}
def resolve(name):
 data=json.loads(index[name].read_text(encoding='utf-8')); result={}
 if data.get('inherits'):result.update(resolve(data['inherits']))
 for inc in data.get('include',[]):result.update(resolve(inc))
 result.update(data)
 for k in ['inherits','include']:result.pop(k,None)
 return result
configs=[resolve('Bambu Lab X1 Carbon 0.4 nozzle'),resolve('0.20mm Standard @BBL X1C'),resolve('Generic PETG')]
configs[0]['curr_bed_type']='Textured PEI Plate'
configs[1].update(wall_loops='6',top_shell_layers='6',bottom_shell_layers='6',sparse_infill_density='40%',sparse_infill_pattern='gyroid',brim_type='outer_only',brim_width='5',enable_support='1',support_type='normal(auto)',support_on_build_plate_only='0')
paths=[]
for name,data in zip(['machine','process','filament'],configs):
 p=WORK/(name+'.json');p.write_text(json.dumps(data,indent=2),encoding='utf-8');paths.append(p)
results={}
files=list(OUT.glob('*.stl'))
if len(sys.argv)>1:files=[p for p in files if sys.argv[1] in p.stem]
for p in files:
 dest=WORK/p.stem;dest.mkdir(exist_ok=True)
 mesh=trimesh.load(p,force='mesh')
 mesh.apply_translation([138-mesh.bounds[:,0].mean(),128-mesh.bounds[:,1].mean(),-mesh.bounds[0,2]])
 staged=dest/'placed.stl';mesh.export(staged)
 cmd=[CLI,'--debug','3','--datadir',str(WORK/'studio_data'),'--load-settings',str(paths[0])+';'+str(paths[1]),'--load-filaments',str(paths[2]),'--arrange','0','--orient','0','--slice','0','--outputdir',str(dest),str(staged)]
 r=subprocess.run(cmd,capture_output=True,text=True)
 log=r.stdout+r.stderr;(dest/'slice.log').write_text(log,encoding='utf-8')
 results[p.stem]={'returncode':r.returncode,'result':str(dest/'result.json')}
 print(p.stem,r.returncode,flush=True)
 if r.returncode:print(log[-2200:],flush=True)
(WORK/('results_'+(sys.argv[1] if len(sys.argv)>1 else 'all')+'.json')).write_text(json.dumps(results,indent=2),encoding='utf-8')
if any(v['returncode'] for v in results.values()):sys.exit(1)
