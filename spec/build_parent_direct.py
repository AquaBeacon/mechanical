import json,subprocess,math,zipfile
from pathlib import Path
import trimesh
R=Path(__file__).resolve().parents[1];O=R/'assemblies/parent_direct';P=O/'prints';P.mkdir(exist_ok=True)
a=json.loads((R/'assemblies/parent_light/placement.json').read_text(encoding='utf-8'));a['name']='parent_direct'
a['note']='Confirmed M3 40x40 rear-face camera mount attached directly below frame. Only TD04A retains an angle support.'
items=[]
for i in a['items']:
 if i['label'].startswith(('camera_screw_','camera_washer_','camera_nut_')):continue
 if i['label'].startswith(('carrier_screw_','carrier_washer_','carrier_nut_')) and float(i['label'].split('_')[-1])<0:continue
 name=i.get('file') or Path(i['part']).name
 if name in ['parent_light_frame','parent_light_carrier']:
  new={'parent_light_frame':'parent_direct_frame','parent_light_carrier':'parent_td_support'}[name]
  i.update(part='parts/parent/exterior/printed/'+new,file=new)
 if i['label']=='camera_mount':
  i.update(part='parts/child/exterior/printed/dji_osmo_action6_mount_m3',file='camera_mount',ops=[dict(translate=[-40,-40,-55.45]),dict(rotate=[-90,0,0])],note='Existing confirmed rear M3 mount; not a new print.')
 if i['label']=='camera_case_reference':i['ops']=[dict(translate=[-40,-3.5,-55.45]),dict(rotate=[-90,0,0])]
 items.append(i)
a['items']=items
(O/'placement.json').write_text(json.dumps(a,indent=2),encoding='utf-8')
subprocess.run(['python',str(R/'scad/lib/asm_gen.py'),str(O/'placement.json'),str(O/'parent_direct_view.scad')],check=True)
for name,cam,defs in [('preview','0,0,0,65,0,210,0',['-D','show_floats=false','-D','show_vessel=false']),('structure','0,0,0,125,0,210,0',['-D','show_floats=false','-D','show_vessel=false','-D','show_envelope=false'])]:
 r=subprocess.run([r'C:\Program Files\OpenSCAD\openscad.exe','-o',str(O/(name+'.png')),'--imgsize=1200,1000','--viewall','--autocenter','--projection=o','--camera='+cam,*defs,str(O/'parent_direct_view.scad')],capture_output=True,text=True)
 (O/(name+'.log')).write_text(r.stdout+r.stderr,encoding='utf-8');r.check_returncode()
manifest=[]
for name,n,angle in [('parent_direct_frame',1,180),('parent_light_bar',2,0),('parent_td_support',1,-90),('parent_light_jaw',1,90)]:
 m=trimesh.load(R/f'parts/parent/exterior/printed/{name}/{name}.stl',force='mesh');assert m.is_watertight and len(m.split())==1,name
 m.apply_transform(trimesh.transformations.rotation_matrix(math.radians(angle),[1,0,0]));m.apply_translation(-m.bounds[0]);m.export(P/(name+'.stl'))
 manifest.append(dict(part=name,quantity=n,print_extents_mm=m.extents.tolist(),volume_mm3=float(m.volume),watertight=True))
(O/'print_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
with zipfile.ZipFile(O/'parent_direct_prints.zip','w',zipfile.ZIP_DEFLATED)as z:
 for i in manifest:z.write(P/(i['part']+'.stl'),'prints/'+i['part']+'.stl')
 z.write(O/'print_manifest.json','print_manifest.json')
 if (O/'README.md').exists():z.write(O/'README.md','README.md')
