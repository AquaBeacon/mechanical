import json,subprocess,math,zipfile
from pathlib import Path
import trimesh
R=Path(__file__).resolve().parents[1];O=R/'assemblies/parent_light';P=O/'prints';P.mkdir(exist_ok=True)
a=json.loads((R/'assemblies/parent_open/placement.json').read_text(encoding='utf-8'))
a['name']='parent_light';a['note']='Integrated downward float lugs and lightened members. Camera mount is existing hardware, not a new print.'
items=[]
replace={'parent_open_frame':'parent_light_frame','parent_clamp_bar':'parent_light_bar','parent_compact_carrier':'parent_light_carrier','parent_td_bracket_jaw':'parent_light_jaw'}
for i in a['items']:
    if i['label'].startswith(('float_lug_','lug_screw_','lug_washer_','lug_nut_')):continue
    old=i.get('file') or Path(i['part']).name
    if old in replace:
        new=replace[old];i['part']='parts/parent/exterior/printed/'+new;i['file']=new
    if i['label']=='camera_mount':i['group']='envelope';i['note']='Existing mount; do not print again.'
    if i['label'].startswith('carrier_screw_'):
        i['file']='screw_M5_30_countersunk';i['part']='assemblies/parent_light/reference'
        i['ops'][0]['translate'][2]=0
    items.append(i)
a['items']=items
ref=O/'reference';ref.mkdir(exist_ok=True)
trimesh.creation.revolve([[0,0],[5,0],[2.5,-2.5],[2.5,-30],[0,-30]]).export(ref/'screw_M5_30_countersunk.stl')
(O/'placement.json').write_text(json.dumps(a,indent=2),encoding='utf-8')
subprocess.run(['python',str(R/'scad/lib/asm_gen.py'),str(O/'placement.json'),str(O/'parent_light_view.scad')],check=True)
for name,cam,defs in [('preview','0,0,0,65,0,30,0',[]),('structure','0,0,0,65,0,210,0',['-D','show_floats=false','-D','show_vessel=false','-D','show_envelope=false'])]:
    r=subprocess.run([r'C:\Program Files\OpenSCAD\openscad.exe','-o',str(O/(name+'.png')),'--imgsize=1200,1000','--viewall','--autocenter','--projection=o','--camera='+cam,*defs,str(O/'parent_light_view.scad')],capture_output=True,text=True)
    (O/(name+'.log')).write_text(r.stdout+r.stderr,encoding='utf-8');r.check_returncode()
manifest=[]
for name,n,angle in [('parent_light_frame',1,180),('parent_light_bar',2,0),('parent_light_carrier',1,-90),('parent_light_jaw',1,90)]:
    m=trimesh.load(R/f'parts/parent/exterior/printed/{name}/{name}.stl',force='mesh')
    assert m.is_watertight and len(m.split())==1,name
    m.apply_transform(trimesh.transformations.rotation_matrix(math.radians(angle),[1,0,0]));m.apply_translation(-m.bounds[0]);m.export(P/(name+'.stl'))
    manifest.append(dict(part=name,quantity=n,print_extents_mm=m.extents.tolist(),volume_mm3=float(m.volume),watertight=True))
old=json.loads((R/'assemblies/parent_open/print_manifest.json').read_text())
before=sum(i['quantity']*i['volume_mm3'] for i in old if i['part']!='parent_camera_mount')
after=sum(i['quantity']*i['volume_mm3'] for i in manifest)
report=dict(before_same_scope_mm3=before,after_mm3=after,reduction_percent=100*(1-after/before),note='CAD solid volume only; actual filament depends on slicing, shells, infill and supports. Existing camera mount excluded from both sides.')
(O/'volume_comparison.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
(O/'print_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
with zipfile.ZipFile(O/'parent_light_prints.zip','w',zipfile.ZIP_DEFLATED) as z:
    for i in manifest:z.write(P/(i['part']+'.stl'),'prints/'+i['part']+'.stl')
    z.write(O/'print_manifest.json','print_manifest.json')
    if (O/'README.md').exists():z.write(O/'README.md','README.md')
print(json.dumps(report,indent=2))
