"""Prepare authorised single-camera / vertical-light topology studies."""
from pathlib import Path
import json, shutil, subprocess, sys, os, re
import numpy as np
import trimesh

ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/'assemblies/child_frame2_assembly/topopt_review_20260910_v2'
OUT=ROOT/'assemblies/child_single_camera_topopt'
SCENE=OUT/'scene';SCENE.mkdir(parents=True,exist_ok=True)
os.environ['PYTHONIOENCODING']='utf-8'
names=['child_core_frame','child_jaw_gate','child_cam_bridge']
def module_replace(text,name,replacement):
    start=text.index('module '+name+'(');brace=text.index('{',start);depth=1;end=brace+1
    while depth:
        depth+=(text[end]=='{')-(text[end]=='}');end+=1
    return text[:start]+replacement+text[end:]
def render(source,target,part=None):
    args=['C:/Program Files/OpenSCAD/openscad.exe','-o',str(target)]
    if part:args+=['-D',f'part="{part}"']
    with target.with_suffix('.log').open('w',encoding='utf-8') as log:
        subprocess.run(args+[str(source)],stdout=log,stderr=log,check=True)
for name in names:
    (OUT/name).mkdir(exist_ok=True)
    shutil.copytree(OLD/name/'inputs',OUT/name/'inputs',dirs_exist_ok=True)

scene=(OLD/'scene/exclusions.scad').read_text(encoding='utf-8')
scene=scene.replace((OLD/'child_core_frame/inputs/geometry.scad').as_posix(),(OUT/'child_core_frame/inputs/geometry.scad').as_posix())
scene=module_replace(scene,'cameras','module cameras(){box([-47.35,83.1,82.95],[47.35,129,167.05]);}')
scene=module_replace(scene,'light_forward','module light_forward(){} // Removed by user request.')
scene=module_replace(scene,'light_vertical','''module light_vertical(){
    box([44,-100,75],[80,-50,125]);
    translate([80,-75,50])cylinder(d=light_d+2,h=light_length);
}''')
scene=scene.replace('route([[0,78,15],[0,78,-40],[18,55,-40],[18,-65,-40],[18,-97,-40]],cable_d/2+cable_clearance);',
'''route([[80,-75,50],[80,-75,28],[42,-79,28],[34,-79,75],[18,-97,75]],cable_d/2+cable_clearance);''')
scene=scene.replace('Front-light lead runs below the pressure end cap and below the bridge.','Vertical-light lead returns to the right-side cable channel; bend radius remains provisional.')
scene='// AUTHORISED: one central camera, one +X vertical light. 2026-09-10.\n'+scene
scene_path=SCENE/'exclusions.scad';scene_path.write_text(scene,encoding='utf-8')
cats=['pressure_vessel','cameras','light_vertical','td04a','td04a_socket','hand_clearance','cables']
for cat in cats:
    render(scene_path,SCENE/f'{cat}.stl',cat);print('SCENE',cat,flush=True)

# Re-cut the original reserved channels for the updated single-light harness.
pres=OUT/'child_core_frame/inputs/preserve.stl'
source=pres.with_name('preserve_before_cable_passages.stl')
cut=pres.with_name('preserve_with_cable_passages.scad')
cut.write_text(f'difference(){{import("{source.as_posix()}");import("{(SCENE/"cables.stl").as_posix()}");}}',encoding='utf-8')
render(cut,pres)

bridge='''// Single-camera adapter: GENERATIVE SETUP, not a finished component.
// HP4/HP5 interfaces retained; central camera shifted +9 mm to clear column.
part="reference";
lens_x=0; lens_y=129; lens_z=125;
case_w=94.7; case_d=45.9; case_h=84.1;
wing=60; deck_bot=44.95; deck_top=52.95; hp_y=74.35;
column_front=80.35; hp_z=[100,170]; $fn=48;
module box(lo,hi){translate(lo)cube(hi-lo);}
module preserve(){
    box([-25,hp_y,75],[25,column_front,195]);
    box([-17,lens_y-case_d/2-22,deck_bot],[17,lens_y-case_d/2+22,deck_top]);
    for(s=[-1,1]){
        box([s>0?54:-60,67,deck_bot],[s>0?60:-54,lens_y+8,80]);
        box([s>0?30:-60,lens_y+2,deck_bot],[s>0?60:-30,lens_y+8,80]);
    }
}
module forbidden(){
    box([-case_w/2,lens_y-case_d,82.95],[case_w/2,lens_y,82.95+case_h]);
    box([-17,lens_y-case_d/2-22,deck_top],[17,lens_y-case_d/2+22,82.95]);
    translate([lens_x,lens_y,lens_z])rotate([-90,0,0])cylinder(r1=0,r2=12*tan(77.5),h=12);
    for(z=hp_z)box([-25,62.35,z-25],[25,hp_y,z+25]);
    for(x=[-20,20],z=[80,120,150,190])translate([x,column_front,z])rotate([-90,0,0])cylinder(d=12,h=lens_y+10-column_front);
}
module design_space(){box([-wing,67,deck_bot],[wing,lens_y+8,195]);}
module cuts(){
    forbidden();
    for(x=[-20,20],zc=hp_z,dz=[-20,20])translate([x,hp_y-1,zc+dz])rotate([-90,0,0])cylinder(d=5.4,h=8);
    for(x=[-11,11],dy=[-16,16]){
        translate([x,lens_y-case_d/2+dy,deck_bot-1])cylinder(d=5.4,h=10);
        translate([x,lens_y-case_d/2+dy,deck_bot-1])cylinder(d=8.2/cos(30),h=5,$fn=6);
    }
    for(s=[-1,1],y=[80,125])translate([s*(wing+1),y,65])rotate([0,-90*s,0])cylinder(d=5.4,h=8);
}
assert(lens_y-case_d-column_front>=2.7,"Camera back must clear adapter column");
assert(lens_y+8+110<=250,"Operating depth exceeds 250 mm");
assert(lens_z-80>8*tan(77.5),"Bumper clips optical field");
if(part=="preserve")preserve();
else if(part=="obstacle")difference(){intersection(){forbidden();box([-wing-3,64,deck_bot-3],[wing+3,lens_y+11,198]);}preserve();}
else if(part=="design_space")design_space();
else if(part=="preserve_cuts")cuts();
else{color("green")preserve();color("red",.25)forbidden();%design_space();}
'''
bp=OUT/'child_cam_bridge/inputs/geometry.scad';bp.write_text(bridge,encoding='utf-8')
for kind in ['preserve','obstacle','design_space','preserve_cuts']:
    render(bp,bp.with_name(f'{kind}.stl'),kind)

for name in names:
    folder=OUT/name
    data=json.loads((OLD/name/'study.json').read_text(encoding='utf-8'))
    data['_review_status']='Authorised by user on 2026-09-10: one camera, vertical light; run topopt.'
    data['_new_assumptions']='One central camera lens (0,129,125); one vertical D40x100 light at (80,-75), z50..150; D6 cable +1mm radial clearance. COTS dimensions remain provisional.'
    data['_attach_policy']='Interface surfaces may connect wherever design_space permits, except explicit obstacle volumes and assembly/tool clearances. Composite preserve is retained; no additional face restriction is claimed.'
    ds=trimesh.load(folder/'inputs/design_space.stl',force='mesh').bounds
    data['regions']['join_free_space']={'type':'box','min':ds[0].tolist(),'max':ds[1].tolist()}
    data['geometry']['preserve']={'interfaces':{'stl':'inputs/preserve.stl','attach':['join_free_space']}}
    data['geometry']['obstacle']={'keep_out':'inputs/obstacle.stl'}
    outside=[]
    for cat in cats:
        bbox=trimesh.load(SCENE/f'{cat}.stl',force='mesh').bounds
        if (np.minimum(ds[1],bbox[1])-np.maximum(ds[0],bbox[0])>1e-5).all():
            data['geometry']['obstacle'][cat]=f'../scene/{cat}.stl'
        else:outside.append(cat)
    data['_scene_outside_design_space']=outside
    if name=='child_core_frame':
        data['regions']['td04a_hp1']={'type':'box','min':[-30,-110,214.5],'max':[30,-60,219]}
        data['cases'][0]['loads'].append({'region':'td04a_hp1','force':[0,0,-9.4]})
        data['_td04a_load']='Existing provisional TD04A + fastening mass 0.32kg at 3g, rounded 9.4N, applied directly to HP1 in L1.'
        data['regions']['light_hp']={'type':'box','min':[39,-100,75],'max':[44.5,-50,125]}
        data['regions']['light_hp_upper']={'type':'box','min':[39,-100,114],'max':[44.5,-50,126]}
        data['regions']['light_hp_lower']={'type':'box','min':[39,-100,74],'max':[44.5,-50,86]}
        data['cases'].append({'name':'L7 vertical light 3g: provisional 0.3kg, 9N weight plus 324Nmm offset moment',
          'supports':[{'region':'pocket_bot','fix':'xyz'},{'region':'pocket_top','fix':'xyz'}],
          'loads':[{'region':'light_hp','force':[0,0,-9]},{'region':'light_hp_upper','force':[8.1,0,0]},{'region':'light_hp_lower','force':[-8.1,0,0]}]})
        data['required_cases'].append('L7')
    elif name=='child_jaw_gate':
        data['cases'][0]['loads']=[{'region':'hp4','force':[0,0,-10]},{'region':'hp5','force':[0,0,-10]}]
        data['cases'][0]['name']='L1 hoist 3g: single camera + smaller adapter, 20N total on HP4/HP5 plus gate self-weight'
    else:
        data['_geometry_source']='inputs/geometry.scad, newly authored central single-camera adapter. Camera back shifted from y74.1 to83.1 to clear HP column.'
        data['_preserve']='Continuous HP4/HP5 adapter plate; ONE central mount pad; side and front bumper seats within width120.'
        data['_obstacle']='One central camera, its mount body, optical field, gate HP seats, tool access.'
        data['_design_space']='120 x 70 x 150.05 mm (x+-60, y67..137).'
        data['_loads']='One 0.35kg camera, frontal/lateral impact150N, camera handling100N.'
        data['design']['volfrac']=.20
        data['regions']={k:v for k,v in data['regions'].items() if not k.startswith(('mount_','fbump_','endp_'))}
        data['regions'].update({'mount_C':{'type':'box','min':[-17,84.05,44.95],'max':[17,128.05,52.95]},
          'fbump_R':{'type':'box','min':[30,131,44.95],'max':[60,137,80]},
          'endp_R':{'type':'box','min':[54,67,44.95],'max':[60,137,80]}})
        for c in data['cases']:
            for load in c['loads']:
                if load['region'].startswith('mount_'):load['region']='mount_C'
        data['cases'][0]['loads']=[{'region':'mount_C','force':[0,0,-10.3]}]
        data['cases'][0]['name']='L1 single 0.35kg camera at 3g, adapter self-weight at 3g'
        data['cases'][3]['name']='L6 unit handled by central camera, 100N +Z on single mounting seat'
    data['_loads_updated']='Single camera and vertical light selected by user; existing transport/landing envelopes retained conservatively.'
    study=folder/'study.json';study.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print('SETUP',name,flush=True)
    with (folder/'setup.log').open('w',encoding='utf-8') as log:
        res=subprocess.run([sys.executable,'-m','topopt','setup',str(study),'--out',str(folder/'setup'),'--iters','80'],stdout=log,stderr=log)
    print('SETUP EXIT',name,res.returncode,flush=True)
    if res.returncode:raise RuntimeError(f'{name} setup invalid; see setup.log')
print('All single-camera studies prepared and setup checked.',flush=True)
