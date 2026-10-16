"""Assemble sparse parent frame and package only the required print meshes."""
import json, subprocess, math, zipfile
from pathlib import Path
import trimesh
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assemblies/parent_open';OUT.mkdir(exist_ok=True)
PRINT=OUT/'prints';PRINT.mkdir(exist_ok=True)
layout=json.loads((ROOT/'assemblies/parent_clamped/placement.json').read_text(encoding='utf-8'))
layout.update(name='parent_open',note='Open lower frame with downward camera and TD04A metal-bracket sandwich mount. TD geometry remains provisional.')
layout['groups']['envelope']=True
items=layout['items']; items[0].update(label='open_frame',part='parts/parent/exterior/printed/parent_open_frame')
def add(label,name,pos=(0,0,0),rot=None,group='exterior',color='Orange',part=None):
    ops=[dict(translate=list(pos))]
    if rot is not None:ops.append(dict(rotate=rot))
    items.append(dict(label=label,part=part or f'parts/parent/exterior/printed/{name}',file=name,ops=ops,group=group,color=color))
add('sensor_carrier','parent_compact_carrier')
add('camera_mount','parent_camera_mount',(-48,0,-66),[-90,0,0],color='SteelBlue')
add('td_bracket_jaw','parent_td_bracket_jaw',(55,2,-35))
add('td04a_actual_shape_reference','td04a_transducer',(55,0,-100),group='envelope',color='DimGray',part='parts/common/exterior/cots/td04a_transducer')
add('camera_case_reference','camera_case_envelope',(-48,36.5,-66),[-90,0,0],group='envelope',color='DimGray',part='assemblies/parent_spar_bolted/reference')
# M5 carrier bolts and camera fasteners reuse purchased hardware display geometry.
def hardware(label,file,pos,rot=None):
    add(label,file,pos,rot,group='hardware',color='Silver',part='assemblies/parent_clamped/reference')
for x in [-85,-65,65,85]:
    # M5x30 reference projects farther than selected M5x25; create exact display below.
    hardware(f'carrier_screw_{x}','screw_M5_25',(x,-55,-6))
    hardware(f'carrier_washer_{x}','washer_M5',(x,-55,-21))
    hardware(f'carrier_nut_{x}','nut_M5',(x,-55,-26))
REF=ROOT/'assemblies/parent_clamped/reference'
def screw(name,r,length,head_r,head_h):
    trimesh.util.concatenate([trimesh.creation.cylinder(radius=r,height=length,transform=trimesh.transformations.translation_matrix([0,0,-length/2])),trimesh.creation.cylinder(radius=head_r,height=head_h,transform=trimesh.transformations.translation_matrix([0,0,head_h/2]))]).export(REF/(name+'.stl'))
screw('screw_M5_25',2.5,25,4.25,5)
screw('screw_M4_30',2,30,3.5,4)
for x in [-59,-37]:
    for z in [-82,-50]:
        hardware(f'camera_screw_{x}_{z}','screw_M5_25',(x,8,z),[-90,0,0])
        hardware(f'camera_washer_{x}_{z}','washer_M5',(x,-9,z),[-90,0,0])
        hardware(f'camera_nut_{x}_{z}','nut_M5',(x,-14,z),[-90,0,0])
for x in [37,73]:
    hardware(f'td_screw_{x}','screw_M4_30',(x,10,-35),[-90,0,0])
# M4 washers/nuts deliberately not substituted with M5 visual references.
(OUT/'placement.json').write_text(json.dumps(layout,indent=2),encoding='utf-8')
subprocess.run(['python',str(ROOT/'scad/lib/asm_gen.py'),str(OUT/'placement.json'),str(OUT/'parent_open_view.scad')],check=True)
for name,cam,defs in [('preview','0,0,0,65,0,30,0',[]),('underside','0,0,-20,125,0,30,0',['-D','show_floats=false','-D','show_vessel=false'])]:
    r=subprocess.run([r'C:\Program Files\OpenSCAD\openscad.exe','-o',str(OUT/(name+'.png')),'--imgsize=1200,1000','--viewall','--autocenter','--projection=o','--camera='+cam,*defs,str(OUT/'parent_open_view.scad')],capture_output=True,text=True)
    (OUT/(name+'.log')).write_text(r.stdout+r.stderr,encoding='utf-8');r.check_returncode()
manifest=[]
for name,count,angle in [('parent_open_frame',1,180),('parent_clamp_bar',2,0),('parent_float_lug',4,0),('parent_compact_carrier',1,-90),('parent_camera_mount',1,0),('parent_td_bracket_jaw',1,90)]:
    m=trimesh.load(ROOT/f'parts/parent/exterior/printed/{name}/{name}.stl',force='mesh')
    assert m.is_watertight and len(m.split())==1,name
    m.apply_transform(trimesh.transformations.rotation_matrix(math.radians(angle),[1,0,0]))
    m.apply_translation(-m.bounds[0]);m.export(PRINT/(name+'.stl'))
    manifest.append(dict(part=name,quantity=count,print_extents_mm=m.extents.tolist(),watertight=True,volume_mm3=float(m.volume)))
(OUT/'print_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
with zipfile.ZipFile(OUT/'parent_open_prints.zip','w',zipfile.ZIP_DEFLATED) as z:
    for f in PRINT.glob('*.stl'):z.write(f,'prints/'+f.name)
    z.write(OUT/'print_manifest.json','print_manifest.json')
    if (OUT/'README.md').exists():z.write(OUT/'README.md','README.md')
print(json.dumps(manifest,indent=2))
