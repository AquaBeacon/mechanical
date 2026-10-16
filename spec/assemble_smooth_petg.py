from pathlib import Path
import json,sys,shutil,subprocess,zipfile
import numpy as np,trimesh
R=Path(__file__).resolve().parents[1];O=R/'assemblies/child_petg100_design';A=O/'smooth_assembly';M=A/'meshes';M.mkdir(exist_ok=True)
sys.path.insert(0,str(R/'scad/lib'));from check_asm_contacts import load
records=[];sc=[];all_mesh=[]
def add(name,mesh,color,group='assembly',source=None):
 mesh.export(M/(name+'.stl'));all_mesh.append(mesh)
 records.append(dict(name=name,source=source,group=group,triangles=len(mesh.faces),watertight=bool(mesh.is_watertight),signed_volume_mm3=float(mesh.volume),bounds_mm=mesh.bounds.tolist()))
 c=json.dumps(color) if isinstance(color,str) else str(color)
 text=f'color({c})import("meshes/{name}.stl");'
 sc.append(('if(show_transport) ' if group=='transport' else '')+text)
for n,color in [('child_core_frame','SteelBlue'),('child_jaw_gate','SeaGreen')]:
 p=A/'extraction'/n/'study_t50_smooth.stl';add(n+'_smooth',trimesh.load(p),color,source=str(p.relative_to(R)))
for n,color in [('child_cam_bridge','Goldenrod'),('vertical_light_saddle','Gold'),('vertical_light_cap','Gold'),('td04a_socket','Plum')]:
 p=O/'cad'/(n+'_print.stl');add(n,trimesh.load(p),color,source=str(p.relative_to(R)))
old=json.loads((R/'assemblies/child_frame2_assembly/placement.json').read_text(encoding='utf-8'))
keep={'acrylic_tube_200','flange_bot','flange_top','end_cap_bottom','dome_top','guard_ring','cable_cover','cable_cover_clamp','top_crown','dome_cap_transport'}
for item in old['items']:
 if item['label'] not in keep:continue
 color=item.get('color','Gray')
 if item['label']=='acrylic_tube_200':color=[.6,.75,.85,.3]
 add(item['label'],load(R,item),color,item['group'],item['part'])
# Keep the existing central camera's actual mounting part, at the approved transform.
item=next(i.copy() for i in old['items'] if i['label']=='cam_mount_stbd')
item['ops']=[{'translate':[0,106.05,52.95]},{'rotate':[0,-90,0]}]
add('camera_mount_C',load(R,item),'DarkSlateGray',source=item['part'])
for n,color in [('cameras','DimGray'),('light_vertical','Khaki'),('td04a','DarkMagenta'),('cables','FireBrick')]:
 add(n+'_envelope',trimesh.load(O/'scene'/(n+'.stl')),color,source='Dimensional envelope; provisional where noted')
# Existing side-bumper module, parameterized for the current single-camera bridge.
src=R/'parts/child/exterior/printed/child_side_bumper/child_side_bumper.scad'
shutil.copy2(src,A/'side_bumper_single_camera.scad')
args=['C:/Program Files/OpenSCAD/openscad.exe','-o',str(A/'bumper_left.stl')]
settings=['lens_x=0','wing_x1=60','case_gap=17','cam_y_shift=23','y0=69.1','bump_bolt_y=[80,125]']
for setting in settings:args+=['-D',setting]
with (A/'bumper.log').open('w') as f:subprocess.run(args+[str(src)],stdout=f,stderr=f,check=True)
left=trimesh.load(A/'bumper_left.stl');add('side_bumper_left',left,'SlateGray',source='Existing SCAD; single camera parameters '+str(settings))
right=left.copy();right.apply_transform(np.diag([-1,1,1,1]));add('side_bumper_right',right,'SlateGray',source='Mirrored left bumper')
# Capture parameter overrides in the delivered editable source too.
with (A/'side_bumper_single_camera.scad').open('a',encoding='utf-8') as f:f.write('\n// Single camera assembly overrides\n'+';\n'.join(settings)+';\n')
(A/'assembly.scad').write_text('show_transport=false;\n'+'\n'.join(sc),encoding='utf-8')
(A/'manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
visible=[m for m,r in zip(all_mesh,records) if r['group']!='transport']
trimesh.util.concatenate(visible).export(A/'assembly_preview.stl')
for suffix,cam in [('front','450,600,390,0,0,110'),('rear','-450,-600,390,0,0,110')]:
 subprocess.run(['C:/Program Files/OpenSCAD/openscad.exe','-o',str(A/(suffix+'.png')),'--imgsize=1300,1100','--viewall','--autocenter','--camera='+cam,'--projection=o',str(A/'assembly.scad')],check=True,capture_output=True)
print('Assembly records:',len(records))
