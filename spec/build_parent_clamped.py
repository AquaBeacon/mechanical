"""Build clamp preview with explicitly simplified purchased hardware references."""
import json, subprocess
from pathlib import Path
import trimesh
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assemblies/parent_clamped'
REF=OUT/'reference'; REF.mkdir(parents=True,exist_ok=True)
layout=json.loads((ROOT/'assemblies/parent_simple/placement.json').read_text(encoding='utf-8'))
layout['name']='parent_clamped'
layout['note']='External rod clamp. Hardware, rubber pads and lid are schematic references. Remove upper bars to open lid.'
layout['groups'].update(hardware=True,pads=True)
items=layout['items']
items[0].update(label='clamped_deck',part='parts/parent/exterior/printed/parent_clamped_deck')
box=next(i for i in items if i['label']=='box_bcas212310g')
box.update(part='parts/parent/exterior/cots/bcas212310g',file='bcas212310g',alpha=0.65)
for sx in [-1,1]:
    for y in [-85,85]:
        ops=[dict(translate=[0,y,0])]
        if sx<0:ops.append(dict(mirror=[1,0,0]))
        items.append(dict(label=f'float_lug_{sx}_{y}',part='parts/parent/exterior/printed/parent_float_lug',ops=ops,group='exterior',color='Orange'))
def ref(name,mesh):
    mesh.export(REF/(name+'.stl'))
def centered_box(size):
    m=trimesh.creation.box(size);m.apply_translation([0,0,size[2]/2]);return m
ref('rod_M5_150',trimesh.creation.cylinder(radius=2.5,height=150,transform=trimesh.transformations.translation_matrix([0,0,75])))
ref('washer_M5',trimesh.creation.annulus(r_min=2.75,r_max=5,height=1,transform=trimesh.transformations.translation_matrix([0,0,0.5])))
ref('nut_M5',trimesh.creation.annulus(r_min=2.5,r_max=8/3**0.5,height=5,sections=6,transform=trimesh.transformations.translation_matrix([0,0,2.5])))
ref('rubber_pad',centered_box([14,24,2]))
ref('lid_envelope',centered_box([210,230,3]))
ref('screw_M5_30',trimesh.util.concatenate([
    trimesh.creation.cylinder(radius=2.5,height=30,transform=trimesh.transformations.translation_matrix([0,0,-15])),
    trimesh.creation.cylinder(radius=4.25,height=5,transform=trimesh.transformations.translation_matrix([0,0,2.5]))]))
def item(label,name,pos,group,color):
    items.append(dict(label=label,part='assemblies/parent_clamped/reference',file=name,ops=[dict(translate=pos)],group=group,color=color))
item('lid_schematic','lid_envelope',[0,0,97.3],'vessel','LightSteelBlue')
for x in [-112,112]:
    for cy in [-85,85]:
        for dy in [-8,8]:
            y=cy+dy
            item(f'lug_screw_{x}_{y}','screw_M5_30',[x,y,0],'hardware','Silver')
            item(f'lug_washer_{x}_{y}','washer_M5',[x,y,-21],'hardware','Silver')
            item(f'lug_nut_{x}_{y}','nut_M5',[x,y,-26],'hardware','Silver')
for y in [-55,55]:
    items.append(dict(label=f'upper_bar_{y}',part='parts/parent/exterior/printed/parent_clamp_bar',ops=[dict(translate=[0,y,102.3])],group='exterior',color='Orange'))
    for x in [-98,98]:item(f'pad_{x}_{y}','rubber_pad',[x,y,100.3],'pads','DimGray')
    for x in [-112,112]:
        item(f'rod_{x}_{y}','rod_M5_150',[x,y,-20],'hardware','Silver')
        for z in [-13,114.3]:item(f'washer_{x}_{y}_{z}','washer_M5',[x,y,z],'hardware','Silver')
        for z in [-18,115.3]:item(f'nut_{x}_{y}_{z}','nut_M5',[x,y,z],'hardware','Silver')
(OUT/'placement.json').write_text(json.dumps(layout,indent=2),encoding='utf-8')
subprocess.run(['python',str(ROOT/'scad/lib/asm_gen.py'),str(OUT/'placement.json'),str(OUT/'parent_clamped_view.scad')],check=True)
for name,cam in [('preview','0,0,40,65,0,30,0'),('front','0,0,40,90,0,0,0')]:
    r=subprocess.run([r'C:\Program Files\OpenSCAD\openscad.exe','-o',str(OUT/(name+'.png')),'--imgsize=1200,900','--viewall','--autocenter','--projection=o','--camera='+cam,str(OUT/'parent_clamped_view.scad')],capture_output=True,text=True)
    (OUT/(name+'.log')).write_text(r.stdout+r.stderr,encoding='utf-8');r.check_returncode()
checks={}
for name,expected in [('parent_clamped_deck',[236,236,12]),('parent_clamp_bar',[236,24,12]),('parent_float_lug',[24,32,44])]:
    mesh=trimesh.load(ROOT/f'parts/parent/exterior/printed/{name}/{name}.stl',force='mesh')
    checks[name]=dict(watertight=bool(mesh.is_watertight),components=len(mesh.split()),extents_mm=mesh.extents.tolist())
    assert mesh.is_watertight and len(mesh.split())==1
    assert all(abs(a-b)<0.01 for a,b in zip(mesh.extents,expected))
checks['clearances_mm']=dict(rod_to_box=112-2.5-105,washer_to_deck_edge=118-112-5,lug_to_clamp_rod=85-16-55-2.5,lug_to_box=118-105,lug_to_float_envelope=178-50-126,bar_to_lid_screw_y=106-(55+12),top_bar_to_lid=2)
assert min(checks['clearances_mm'].values())>0
checks['limitations']='Nominal envelope checks only. Real lid profile, wet slip resistance, clamp load and slicing unverified.'
(OUT/'checks.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
print(json.dumps(checks,indent=2))
