"""Slice changed STLs on X1 Carbon; hash-check unchanged prior slice evidence."""
from pathlib import Path
import subprocess,json,hashlib,sys
import trimesh
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assemblies/parent_bottom_sensors';PRINT=ROOT/'print_jobs/parent_bottom_sensors'
checks=json.loads((OUT/'print_checks.json').read_text())
old=json.loads((ROOT/'assemblies/parent_rope_float/print_checks.json').read_text())
older=json.loads((ROOT/'assemblies/parent_spar_bolted/print_checks.json').read_text())
cfg=ROOT/'print_jobs/parent_spar_bolted/slice_validation'
for name,d in checks.items():
 p=PRINT/(name+'.stl');sha=hashlib.sha256(p.read_bytes()).hexdigest()
 if name in old and sha==old[name]['sha256']:
  d['slice_evidence']='SHA256 matches verified parent_rope_float STL'
  if name in older:
   g=older[name]['filament_g_including_support_and_brim'];sec=older[name]['estimated_seconds']
  else:
   result=json.loads((ROOT/'print_jobs/parent_rope_float/adapter_slice/result.json').read_text())
   assert result['return_code']==0
   plate=result['sliced_plates'][0];g=sum(f['total_used_g'] for f in plate['filaments']);sec=plate['total_predication']
 else:
  work=PRINT/'slice_validation'/name;work.mkdir(parents=True,exist_ok=True)
  m=trimesh.load(p);m.apply_translation([138-m.bounds[:,0].mean(),128-m.bounds[:,1].mean(),-m.bounds[0,2]])
  m.export(work/'placed.stl')
  a=[r'C:\Program Files\Bambu Studio\bambu-studio.exe','--debug','2','--datadir',str(work/'studio_data'),'--load-settings',str(cfg/'machine.json')+';'+str(cfg/'process.json'),'--load-filaments',str(cfg/'filament.json'),'--arrange','0','--orient','0','--slice','0','--outputdir',str(work),str(work/'placed.stl')]
  r=subprocess.run(a,capture_output=True,text=True)
  (work/'slice.log').write_text(r.stdout+r.stderr,encoding='utf-8')
  result=json.loads((work/'result.json').read_text());assert result['return_code']==0,result
  plate=result['sliced_plates'][0];g=sum(f['total_used_g'] for f in plate['filaments']);sec=plate['total_predication']
  d['slice_evidence']=str((work/'result.json').relative_to(ROOT))
 d.update(sha256=sha,slice_return_code=0,filament_g_including_support_and_brim=g,estimated_seconds=sec)
 print(name,'PASS',round(g,1),'g',flush=True)
(OUT/'print_checks.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
print('Total',sum(d['quantity'] for d in checks.values()),'printed parts;',round(sum(d['quantity']*d['filament_g_including_support_and_brim'] for d in checks.values())),'g',flush=True)
