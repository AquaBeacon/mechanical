"""Offline slice of the current rear-support mount. Does not contact a printer."""
from pathlib import Path
import json,subprocess,zipfile,shutil,hashlib
import trimesh
ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/dji_osmo_action6_mount_m3'
OUT=ROOT/'assemblies/parent_exterior/print_jobs/camera_mount_rear_support'
OUT.mkdir(parents=True,exist_ok=True)
PRE=ROOT/'print_jobs/child_simple/slice_validation'
CLI=r'C:\Program Files\Bambu Studio\bambu-studio.exe'
records={}
for name,source in [('camera_mount',PART/'camera_mount.stl')]:
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
 records[name]={'source':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'seconds':plate['total_predication'],'grams':sum(f['total_used_g'] for f in plate['filaments']),'warning':plate.get('warning_message',''),'support_feature_sections':len(features),'material':'Generic PETG','layer_mm':0.2,'walls':6,'infill':'15% gyroid','orientation':'base down, +Z up','physical_fit':'unverified'}
 assert not features,features
 assert not records[name]['warning'],records[name]['warning']
 (OUT/'validation.json').write_text(json.dumps(records,indent=2))
 print(name,records[name],flush=True)
 shutil.copy2(dest/(name+'.3mf'),OUT/(name+'_x1c_petg.3mf'))

# Review actual first/detail-layer extrusion, using the existing G-code parser.
from review_parent_exterior_slices import paths
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
segments=paths(dest/'plate_1.gcode')
layers=sorted({z for z,f,p in segments if f=='Outer wall'})
selected=[layers[0]]+[min(layers,key=lambda z:abs(z-target)) for target in (28,32,36.4)]
fig,axes=plt.subplots(2,2,figsize=(10,9))
for ax,z in zip(axes.flat,selected):
 for bridge,color in [(False,'#247895'),(True,'#d88714')]:
  lines=[p[:,:2] for zz,f,p in segments if zz==z and ('bridge' in f.lower())==bridge and f!='Custom']
  if lines:ax.add_collection(LineCollection(lines,colors=color,linewidths=0.45))
 ax.autoscale();ax.set_aspect('equal');ax.set_title(f'Z={z:g} mm');ax.set_xlabel('bed X / mm');ax.set_ylabel('bed Y / mm')
fig.suptitle('Rear supports: actual extrusion (blue) and bridges (amber)')
fig.tight_layout();fig.savefig(PART/'_work/images/rear_support_layers.png',dpi=140);plt.close(fig)
extrusion=np.array([p[:,:2] for z,f,p in segments if f!='Custom'])
lo=extrusion.min(axis=(0,1));hi=extrusion.max(axis=(0,1))
with zipfile.ZipFile(dest/(name+'.3mf')) as z:settings=json.loads(z.read('Metadata/project_settings.config'))
audit=dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),three_mf_sha256=hashlib.sha256((dest/(name+'.3mf')).read_bytes()).hexdigest(),
           extrusion_bounds_xy_mm=[lo.tolist(),hi.tolist()],support_enable=settings['enable_support'],wall_loops=settings['wall_loops'],infill=settings['sparse_infill_density'],layer_mm=settings['layer_height'],
           passed=bool(np.all(lo>=28.25) and np.all(hi<=255.75) and str(settings['enable_support'])=='0'),limits=['Physical print/adhesion and case fit unverified; G2/G3 paths plotted as chords.'])
(OUT/'slice_audit.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
assert audit['passed'],audit
