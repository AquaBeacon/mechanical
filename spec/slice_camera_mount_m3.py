"""Offline equal-settings original/new comparison. Does not contact a printer."""
from pathlib import Path
import json,subprocess,zipfile,shutil
import trimesh
ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/dji_osmo_action6_mount_m3'
OUT=ROOT/'print_jobs/dji_osmo_action6_mount_m3'
OUT.mkdir(exist_ok=True)
PRE=ROOT/'print_jobs/child_simple/slice_validation'
CLI=r'C:\Program Files\Bambu Studio\bambu-studio.exe'
records={}
for name,source in [('original',ROOT/'parts/child/exterior/printed/dji_osmo_action6_mount/dji_osmo_action6_mount.stl'),('camera_mount',PART/'camera_mount.stl')]:
 dest=OUT/name;dest.mkdir(exist_ok=True)
 process=json.loads((PRE/'process.json').read_text())
 process.update(print_settings_id='Camera direct M3 PETG 0.20 6 walls 15 percent no support',wall_loops='6',top_shell_layers='6',bottom_shell_layers='6',sparse_infill_density='15%',sparse_infill_pattern='gyroid',enable_support='0',brim_width='3')
 (dest/'process.json').write_text(json.dumps(process,indent=2))
 m=trimesh.load(source,force='mesh');assert m.is_watertight
 m.apply_translation([128-m.bounds[:,0].mean(),128-m.bounds[:,1].mean(),-m.bounds[0,2]])
 m.export(dest/'placed.stl')
 cmd=[CLI,'--debug','2','--datadir',str(dest/'studio_data'),'--load-settings',str(PRE/'machine.json')+';'+str(dest/'process.json'),'--load-filaments',str(PRE/'filament.json'),'--arrange','0','--orient','0','--slice','0','--export-3mf',name+'.3mf','--outputdir',str(dest),str(dest/'placed.stl')]
 print('Slicing',name,flush=True)
 r=subprocess.run(cmd,capture_output=True,text=True,errors='replace',cwd=dest)
 (dest/'slice.log').write_text(r.stdout+r.stderr,encoding='utf-8')
 result=json.loads((dest/'result.json').read_text())
 assert r.returncode==0 and result['return_code']==0,(name,result)
 plate=result['sliced_plates'][0]
 with zipfile.ZipFile(dest/(name+'.3mf')) as z:
  assert z.testzip() is None
  gc=z.read('Metadata/plate_1.gcode').decode()
 features=[ln for ln in gc.splitlines() if ln.startswith('; FEATURE:') and 'Support' in ln]
 records[name]={'seconds':plate['total_predication'],'grams':sum(f['total_used_g'] for f in plate['filaments']),'warning':plate.get('warning_message',''),'support_feature_sections':len(features)}
 (OUT/'comparison.json').write_text(json.dumps(records,indent=2))
 print(name,records[name],flush=True)
 if name!='original':shutil.copy2(dest/(name+'.3mf'),OUT/(name+'_x1c_petg.3mf'))
