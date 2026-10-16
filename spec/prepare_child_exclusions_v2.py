"""Named exclusion bodies and handle load: setup only, no optimisation."""
from pathlib import Path
import json, shutil, subprocess, sys, os
import trimesh

ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/'assemblies/child_frame2_assembly/topopt_review_20260910'
OUT=ROOT/'assemblies/child_frame2_assembly/topopt_review_20260910_v2'
SCENE=OUT/'scene'; SCENE.mkdir(parents=True,exist_ok=True)
os.environ['PYTHONIOENCODING']='utf-8'
names=['child_core_frame','child_jaw_gate','child_cam_bridge']
for name in names:
    folder=OUT/name; folder.mkdir(exist_ok=True)
    shutil.copytree(OLD/name/'inputs',folder/'inputs',dirs_exist_ok=True)

core=(OUT/names[0]/'inputs/geometry.scad').as_posix()
scene='''// Setup review: solid exclusion envelopes, not production parts.
// World frame: mm; X right, Y front, Z up. Provisional component sizes.
use <CORE>
$fn=48;
part="all";
light_d=40; light_length=100; cable_d=6; cable_clearance=1;
module box(lo,hi){translate(lo)cube(hi-lo);}
module link(a,b,r){hull(){translate(a)sphere(r=r,$fn=16);translate(b)sphere(r=r,$fn=16);}}
module route(points,r){for(i=[0:len(points)-2])link(points[i],points[i+1],r);}
module pressure_vessel(){
    translate([0,0,-8])cylinder(r=57.15,h=216);
    translate([0,0,-13.8])cylinder(r=60.15,h=5.8);
    translate([0,0,208])cylinder(r=60.15,h=6.5);
    translate([0,0,214])intersection(){sphere(r=47.25);box([-50,-50,0],[50,50,50]);}
}
module cameras(){
    for(s=[-1,1])box([s>0?27.65:-122.35,74.1,82.95],[s>0?122.35:-27.65,120,167.05]);
}
module light_forward(){
    // HP-L: adapter reservation and 40x100 provisional barrel, aimed +Y.
    box([-25,74.35,-10],[25,78,40]);
    translate([0,78,15])rotate([-90,0,0])cylinder(d=light_d+2,h=light_length);
}
module light_vertical(){
    // Alternative HP2/HP3 poses; reserved together, not a three-light BOM.
    for(s=[-1,1]){
        box([s>0?44:-80,-100,75],[s>0?80:-44,-50,125]);
        translate([s*80,-75,50])cylinder(d=light_d+2,h=light_length);
    }
}
module td04a(){
    // Body seated on socket floor: 218.5 + 6, not placed on socket rim.
    translate([0,-85,224.5])cylinder(d=26.4,h=55);
}
module td04a_socket(){box([-25,-110,218.5],[25,-60,256.5]);}
module hand_clearance(){
    hand_room();
    // Approach from the rear through the 52x30 finger opening.
    box([-26,-150,115],[26,-103,145]);
}
module cables(){
    // Swept routing corridors. Bend radius and service loops remain to be sized.
    for(s=[-1,1])route([[s*18,-97,-40],[s*18,-97,75],
        [s*34,-79,105],[s*34,-79,187],[s*18,-92,202],[s*18,-92,228]],cable_d/2+cable_clearance);
    // TD04A feed to its bottom opening; follow the left-side reserved bypass.
    route([[-18,-92,202],[-18,-85,214],[0,-85,224]],cable_d/2+cable_clearance);
    // Front-light lead runs below the pressure end cap and below the bridge.
    route([[0,78,15],[0,78,-40],[18,55,-40],[18,-65,-40],[18,-97,-40]],cable_d/2+cable_clearance);
    // Five penetrators and the lower wiring volume (provisional 20mm protrusion).
    for(a=[-90,-18,54,126,198])translate([28*cos(a),28*sin(a),-33.8])cylinder(d=14,h=20);
    box([-38,-45,-48],[38,38,-34]);
}
if(part=="pressure_vessel")pressure_vessel();
else if(part=="cameras")cameras();
else if(part=="light_forward")light_forward();
else if(part=="light_vertical")light_vertical();
else if(part=="td04a")td04a();
else if(part=="td04a_socket")td04a_socket();
else if(part=="hand_clearance")hand_clearance();
else if(part=="cables")cables();
else {color([.25,.65,.95,.3])pressure_vessel();color("orange")cameras();
color("gold",.5){light_forward();light_vertical();}color("purple")td04a();
color("red")cables();color("cyan",.4)hand_clearance();}
'''.replace('CORE',core)
scad=SCENE/'exclusions.scad'; scad.write_text(scene,encoding='utf-8')
categories=['pressure_vessel','cameras','light_forward','light_vertical','td04a','td04a_socket','hand_clearance','cables']
def render(source,target,part=None):
    args=['C:/Program Files/OpenSCAD/openscad.exe','-o',str(target)]
    if part: args+=['-D',f'part="{part}"']
    with target.with_suffix('.log').open('w',encoding='utf-8') as log:
        subprocess.run(args+[str(source)],stdout=log,stderr=log,check=True)
for cat in categories:
    render(scad,SCENE/f'{cat}.stl',cat)
    print('SCENE',cat,flush=True)

# Explicitly introduce cable pass-throughs into the reserved channel walls.
# This is a geometry change, not deleting overlapping obstacle voxels silently.
preserve=OUT/names[0]/'inputs/preserve.stl'
shutil.copy2(preserve,preserve.with_name('preserve_before_cable_passages.stl'))
cutscad=preserve.with_name('preserve_with_cable_passages.scad')
cutscad.write_text(f'difference(){{import("{preserve.with_name("preserve_before_cable_passages.stl").as_posix()}");import("{(SCENE/"cables.stl").as_posix()}");}}',encoding='utf-8')
render(cutscad,preserve)
changes=[]
for name in names:
    folder=OUT/name
    data=json.loads((OLD/name/'study.json').read_text(encoding='utf-8'))
    data['_review_status']='V2 named exclusions and handle load, setup review only. Optimisation not authorised.'
    data['_new_assumptions']='Light D40 x L100; cable D6 + 1mm radial clearance. Alternative light orientations are reserved together, not simultaneous equipment. Front pose exceeds depth limit; not approved.'
    if name=='child_core_frame':
        data['_preserve_changes']='Two cable-channel transitions opened in reserved material using inputs/preserve_with_cable_passages.scad; compare original before_cable_passages mesh.'
        data['regions']['grip_underside']={'type':'box','min':[-30,-101,145],'max':[30,-89,148.5]}
        data['cases'].append({'name':'L6 grip lift +200 N: equivalent handling test with vessel restrained; provisional 6kg x 3g rounded up',
            'supports':[{'region':'pocket_bot','fix':'xyz'},{'region':'pocket_top','fix':'xyz'}],
            'loads':[{'region':'grip_underside','force':[0,0,200]}]})
        data['required_cases'].append('L6')
    ds=trimesh.load(folder/'inputs/design_space.stl',force='mesh').bounds
    applied=[]; outside=[]
    for cat in categories:
        body=trimesh.load(SCENE/f'{cat}.stl',force='mesh')
        import numpy as np
        overlap=np.minimum(ds[1],body.bounds[1])-np.maximum(ds[0],body.bounds[0])
        if (overlap>1e-5).all():
            data['geometry']['obstacle'][cat]=f'../scene/{cat}.stl'; applied.append(cat)
        else: outside.append(cat)
    data['_scene_outside_design_space']=outside
    data['_scene_outside_note']='Full bodies are present in scene/exclusions.scad and review figures. No volume intersection with this design-space bbox, so excluded by design boundary itself.'
    study=folder/'study.json';study.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    changes.append({'part':name,'added_obstacles':applied,'outside_design_space':outside})
    print('SETUP',name,applied,flush=True)
    with (folder/'setup.log').open('w',encoding='utf-8') as log:
        res=subprocess.run([sys.executable,'-m','topopt','setup',str(study),'--out',str(folder/'setup'),'--iters','80'],stdout=log,stderr=log)
    print('SETUP EXIT',name,res.returncode,flush=True)
(OUT/'exclusion_application.json').write_text(json.dumps(changes,indent=2),encoding='utf-8')
print('DONE',flush=True)
