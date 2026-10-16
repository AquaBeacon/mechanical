"""Parametric structural rebuild, enlarged search spaces, explicit solid PETG.
No solver code modifications. Search studies omit the known fixed-domain gravity;
manufactured-CAD validation studies include actual-geometry distributed gravity.
"""
from pathlib import Path
import json, os, re, shutil, subprocess, sys
import trimesh
ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/'assemblies/child_single_camera_topopt'
OUT=ROOT/'assemblies/child_petg100_design'
OUT.mkdir(exist_ok=True)
shutil.copytree(OLD/'scene',OUT/'scene',dirs_exist_ok=True)
os.environ['PYTHONIOENCODING']='utf-8'

def replace_module(s,name,new):
    i=s.index('module '+name+'(');j=s.index('{',i);depth=1;k=j+1
    while depth:
        depth+=(s[k]=='{')-(s[k]=='}');k+=1
    return s[:i]+new+s[k:]

def render(source,target,part):
    args=['C:/Program Files/OpenSCAD/openscad.exe','-o',str(target),'-D',f'part="{part}"',str(source)]
    with target.with_suffix('.log').open('w',encoding='utf-8') as log:
        subprocess.run(args,stdout=log,stderr=log,check=True)

common='''
/* [Structural rebuild - PETG 100 percent infill] */
structural_radius=78;
back_halfwidth=40;
back_front=-58;
bridge_deck_thickness=18;
// The following bodies are editable cylinders and extruded polygons/boxes.
module box3(a,b){translate(a)cube(b-a);}
module scene_voids(){
  for(n=["cameras","light_vertical","td04a","td04a_socket","hand_clearance","cables"])
    import(str("../scene/",n,".stl"));
}
'''
metrics={}
for name in ['child_jaw_gate','child_core_frame','child_cam_bridge']:
    folder=OUT/name;folder.mkdir(exist_ok=True)
    source=(OLD/name/'inputs/geometry.scad').read_text(encoding='utf-8')
    if name!='child_cam_bridge':
        source=source[:source.index('// ---- 出力')]
        source=re.sub(r'ds_x0\s*=\s*-80;', 'ds_x0 = -96;',source)
        source=re.sub(r'ds_x1\s*=\s*72;', 'ds_x1 = 96;',source)
        if name=='child_jaw_gate':
            source=re.sub(r'ds_y1\s*=\s*74\.35;', 'ds_y1 = 90;',source)
            source=re.sub(r'obs_y1\s*=\s*77\.35;', 'obs_y1 = 93;',source)
            source=replace_module(source,'bridge_zone','''module bridge_zone(){
                // Current single-camera adapter envelope, with 2.65mm rear gap.
                // Outside x+-60 the obsolete stereo-camera reservations are gone.
                translate([-60,64.35,44.95])cube([120,80,150.05]);
            }''')
            extra='''
module structure(){
    intersection(){translate([0,0,ds_z0])cylinder(r=structural_radius,h=ds_z1-ds_z0);box3([-96,0,ds_z0],[96,90,ds_z1]);}
    box3([-72,10,ds_z0],[-50,30,ds_z1]);
    box3([50,0,ds_z0],[84,24,ds_z1]);
    for(hp=front_hp)box3([-25,40,hp[2]-25],[25,hp_seat_y,hp[2]+25]);
}
'''
        else:
            extra='''
module structure(){
    intersection(){translate([0,0,ds_z0])cylinder(r=structural_radius,h=ds_z1-ds_z0);box3([-96,-110,ds_z0],[96,0,ds_z1]);}
    box3([-back_halfwidth,-101,ds_z0],[back_halfwidth,back_front,ds_z1]);
    box3([-88,-25,ds_z0],[-50,19,ds_z1]);
    box3([50,-24,ds_z0],[84,0,ds_z1]);
    box3([-75,-30,190],[75,0,ds_z1]);
}
'''
        extra+='''
module fixed_interfaces(){difference(){preserve_all();scene_voids();}}
module allowed_obstacles(){union(){obstacle_all();scene_voids();}}
module manufactured(){
  difference(){
    union(){fixed_interfaces();difference(){intersection(){structure();design_space();}allowed_obstacles();}}
    small_holes();scene_voids();
    if(is_undef(gr_cx)==false){grooves();tie_slots();tie_backspace();cable_cavity();hand_room();}
  }
}
if(part=="manufactured")manufactured();
else if(part=="preserve")fixed_interfaces();
else if(part=="obstacle")allowed_obstacles();
else if(part=="design_space")design_space();
else if(part=="preserve_cuts"){small_holes();scene_voids();}
else {color("green")fixed_interfaces();color("red",.2)allowed_obstacles();%design_space();}
'''
    else:
        source=source[:source.index('if(part=="preserve")')]
        extra='''
module structure(){
    box([-wing,67,deck_bot],[wing,lens_y+8,deck_bot+bridge_deck_thickness]);
    box([-wing,67,deck_bot],[wing,82.35,195]);
    for(s=[-1,1])box([s>0?48:-60,67,deck_bot],[s>0?60:-48,lens_y+8,82.95]);
}
module manufactured(){difference(){union(){structure();preserve();}cuts();}}
if(part=="manufactured")manufactured();
else if(part=="preserve")preserve();
else if(part=="obstacle")difference(){intersection(){forbidden();box([-wing-3,64,deck_bot-3],[wing+3,lens_y+11,198]);}preserve();}
else if(part=="design_space")design_space();
else if(part=="preserve_cuts")cuts();
else {color("green")preserve();color("red",.2)forbidden();%design_space();}
'''
    source=source.replace('part = "reference"','part = "manufactured"').replace('part="reference"','part="manufactured"')
    path=folder/f'{name}.scad';path.write_text(source+common+extra,encoding='utf-8')
    for kind in ['manufactured','preserve','obstacle','design_space','preserve_cuts']:
        print('RENDER',name,kind,flush=True)
        render(path,folder/f'{kind}.stl',kind)
    mesh=trimesh.load(folder/'manufactured.stl',force='mesh')
    metrics[name]={'volume_cm3':float(mesh.volume/1000),'mass_kg_at_density_1_27':float(mesh.volume*1.27e-6),
                   'bounds_mm':mesh.bounds.tolist(),'watertight':bool(mesh.is_watertight),'components':len(mesh.split())}
    if not mesh.is_watertight:raise RuntimeError(f'{name}: mesh not watertight')
    d=json.loads((OLD/name/'study.json').read_text(encoding='utf-8'))
    d['infill']=1.0;d['walls']=6;d['material']='PETG';d['voxel_mm']=2.0
    d['_print']='User specified PETG100% infill. Orthotropic solid material remains anisotropic.'
    d['_what']='Expanded domain and editable structural CAD, current single camera and vertical light.'
    d['geometry']['voxel_mm']=2.0
    d['geometry']['design_space']='design_space.stl'
    d['geometry']['preserve']={'interfaces':{'stl':'preserve.stl','attach':['join_free_space']}}
    d['geometry']['obstacle']={'keep_out':'obstacle.stl'}
    bounds=trimesh.load(folder/'design_space.stl',force='mesh').bounds
    d['regions']['join_free_space']={'type':'box','min':bounds[0].tolist(),'max':bounds[1].tolist()}
    d['finish']={'voxel_mm':0.5,'add':{'interfaces':'preserve.stl'},'cut':{'features':'preserve_cuts.stl'}}
    d['design'].update(volfrac=0.35,filter_mm=6.0)
    for case in d['cases']:
        if case.get('gravity'):case['gravity']['fill_factor']=1.0
        if case['name'].startswith('L6') and name=='child_core_frame':
            case['name']='L6 grip lift +300N: provisional handling envelope up to10kg at3g'
            case['loads'][0]['force']=[0,0,300]
    # Full-CAD validation uses its actual occupied cells for self weight.
    fea={k:v for k,v in d.items() if k not in ['geometry','design','finish','required_cases']}
    fea['part']='manufactured.stl'
    (folder/'fea.json').write_text(json.dumps(fea,ensure_ascii=False,indent=2),encoding='utf-8')
    # The known fixed-domain gravity bug cannot affect these search studies.
    for case in d['cases']:case.pop('gravity',None)
    d['_gravity_policy']='Topology search uses external loads only. Mandatory fea.json on manufactured CAD includes self weight at100% infill; no fixed-domain gravity during search.'
    (folder/'search.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')

(OUT/'geometry_metrics.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding='utf-8')
# Update component weights conservatively using the actual new CAD volumes.
bridge_mass=metrics['child_cam_bridge']['mass_kg_at_density_1_27']
gate_mass=metrics['child_jaw_gate']['mass_kg_at_density_1_27']
for file in ['fea.json','search.json']:
    p=OUT/'child_jaw_gate'/file;d=json.loads(p.read_text(encoding='utf-8'))
    force=(bridge_mass+0.35)*9.81*3
    d['cases'][0]['loads']=[{'region':'hp4','force':[0,0,-force/2]},{'region':'hp5','force':[0,0,-force/2]}]
    d['cases'][0]['name']='L1 hoist3g: actual rebuilt adapter mass +0.35kg camera on HP4/HP5'
    d['_camera_adapter_mass_kg']=bridge_mass+0.35
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
    p=OUT/'child_core_frame'/file;d=json.loads(p.read_text(encoding='utf-8'))
    # Apply the full downstream weight to latch side, intentionally conservative
    # for latch vertical transfer; other hinge transport cases remain independent.
    downstream=(gate_mass+bridge_mass+0.35)*9.81*3
    for ld in d['cases'][0]['loads']:
        if ld['region'] in ['latch_lo','latch_hi']:ld['force']=[0,0,-downstream/2]
    d['_downstream_mass_kg']=gate_mass+bridge_mass+0.35
    d['_load_transfer_limit']='L1 downstream vertical weight on latch side; full contact reaction/moment transfer remains to verify.'
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(metrics,indent=2),flush=True)
