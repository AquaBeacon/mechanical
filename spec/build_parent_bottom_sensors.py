"""Revision of rope-float parent: integral fins and bottom downward sensors."""
from pathlib import Path
import os,sys,json,copy,shutil,collections,hashlib
import numpy as np
import trimesh
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'spec'))
from build_parent_spar_bolted import run,OSC,FC
OUT=ROOT/'assemblies/parent_bottom_sensors';OUT.mkdir(exist_ok=True)
PRINT=ROOT/'print_jobs/parent_bottom_sensors';PRINT.mkdir(parents=True,exist_ok=True)
old=ROOT/'assemblies/parent_rope_float'
source=json.loads((old/'placement.json').read_text(encoding='utf-8'))
fast={f['label']:f for f in json.loads((old/'fasteners.json').read_text(encoding='utf-8'))}
items=[];fasteners=[];joints=[]
remove={'disk','hub_-295','hub_-202','camera_bridge','camera_mount','camera_case_envelope'}|{f'fin_{a}' for a in range(0,360,90)}
remove_notes={'fin -> hub','hub -> beam','hub -> disk -> ballast roof','camera bridge -> deck insert','camera mount -> bridge','camera case fingers; verify against OEM screw','camera mount captive nut'}
for orig in source['items']:
 if orig['label'] in remove:continue
 if orig['group']=='hardware':
  if fast[orig['label']]['note'] in remove_notes:continue
  fasteners.append(copy.deepcopy(fast[orig['label']]))
 items.append(copy.deepcopy(orig))

def add(label,part,t=(0,0,0),rot=(0,0,0),color='DarkOrange',group='exterior',file=None):
 it=dict(label=label,part=part,color=color,group=group,ops=[{'translate':list(t)},{'rotate':list(rot)}])
 if file:it['file']=file
 items.append(it);return it

def build(folder,name,src,print_src=None):
 folder.mkdir(parents=True,exist_ok=True)
 scad=folder/(name+'.scad')
 stl=folder/(name+'.stl');step=folder/(name+'.step');csg=folder/(name+'.csg')
 shared=ROOT/'scad/lib/parent_bottom_sensors.scad'
 if scad.exists() and scad.read_text(encoding='utf-8')==src and stl.exists() and step.exists() and min(stl.stat().st_mtime,step.stat().st_mtime)>shared.stat().st_mtime and (not print_src or (PRINT/(name+'.stl')).exists()):return
 scad.write_text(src,encoding='utf-8')
 run([OSC,'-o',stl,scad],folder/(name+'_render.log'))
 run([OSC,'-o',csg,scad],folder/(name+'_csg.log'))
 env=os.environ.copy();env.update(OPENSCAD=OSC,CSG_IN=str(csg),STEP_OUT=str(step),STL_REF=str(stl))
 r=run([FC,ROOT/'scad/lib/csg_to_step.py'],folder/(name+'_step.log'),env)
 assert step.exists() and '[csg2step] wrote' in r.stdout,(name,r.stdout[-1000:])
 if print_src:
  run([OSC,'-D','part="print"','-o',PRINT/(name+'.stl'),scad],folder/(name+'_print.log'))
 print('Built',name,flush=True)

parts={
 'parent_fin_cartridge':('cartridge();','cartridge();',[0,0,-360]),
 'parent_sensor_carrier':('carrier();','translate([0,0,75])rotate([90,0,0])carrier();',[0,0,-360]),
 'parent_td04a_clamp_body':('td_clamp(false);','rotate([90,0,0])td_clamp(false);',[65,-67,-460]),
 'parent_td04a_clamp_cap':('td_clamp(true);','translate([0,0,46.5])rotate([-90,0,0])td_clamp(true);',[65,-67,-460]),
}
for name,(body,orient,t) in parts.items():
 folder=ROOT/'parts/parent/exterior/printed'/name
 src='// mm. Assembly coordinates and explicit bed orientation.\npart="assembly"; // [assembly,print]\nuse <../../../../../scad/lib/parent_bottom_sensors.scad>\nif(part=="print"){'+orient+'}else{'+body+'}\n'
 build(folder,name,src,orient)
 add(name,str(folder.relative_to(ROOT)).replace('\\','/'),t,color='Gold' if 'fin_' in name else 'DarkOrange')
 folder.joinpath(name+'.md').write_text('# '+name+'\n\n2026-09-10 下向きカメラ・TD04A版。数量1。寸法・印刷姿勢は assemblies/parent_bottom_sensors/print_checks.json。\n\n共通パラメータ: scad/lib/parent_bottom_sensors.scad。要確認: TD04A胴径 td_d=26、胴長 td_len=55、締付隙間 clamp_gap=0.5 は実測未確定。既存カメラケース包絡も実測未確定。試作形状であり実荷重・防水性は未評価。\n',encoding='utf-8')

add('camera_mount','parts/child/exterior/printed/dji_osmo_action6_mount',[-45,-67,-470],[-90,0,0],'SteelBlue')
add('camera_case_envelope','assemblies/parent_spar_bolted/reference',[-45,-30.5,-470],[-90,0,0],'DimGray','envelope','camera_case_envelope')
# Reference camera file has bottom Z=0; translate its native +36.5 Z along global +Y.
rf=OUT/'reference'
build(rf,'td04a_envelope','// Purchased TD04A PROVISIONAL d26, length55; face at Z=0, cable exits Z=55.\n$fn=64;cylinder(d=26,h=55);')
add('td04a_envelope',str(rf.relative_to(ROOT)).replace('\\','/'),[65,-40,-493],color='Black',group='envelope',file='td04a_envelope')
# Original display model omitted the external mounting bores and represented the
# corner pillars as solid. E-E of the existing manufacturer PDF gives D4.2 and
# the 6 mm bottom seat. Upper access-well D9.4 is a display assumption, not a
# manufacturer-certified dimension or an instruction to drill the bought box.
build(rf,'bcas_mounting_reference','''// Purchased box display correction, not a printable or machining part.
// Drawing E-E: external bore D4.2, seat height6. Access well D9.4 is provisional.
$fn=64;
difference(){
 union(){include <../../../parts/parent/exterior/cots/bcas212310g/bcas212310g.scad>}
 for(x=[9,201])for(y=[9,221]){
  translate([x,y,-1])cylinder(d=4.2,h=8);
  translate([x,y,6])cylinder(d=9.4,h=76);
 }
}
''')
for it in items:
 if it['label']=='box_bcas212310g':
  it['part']=str(rf.relative_to(ROOT)).replace('\\','/');it['file']='bcas_mounting_reference'
  it['note']+='; E-E mounting bores restored in display model; upper well D9.4 provisional.'

hardware=OUT/'hardware';types={}
def along(t,rot,d):
 r=trimesh.transformations.euler_matrix(*np.radians(rot),axes='sxyz')
 return (np.array(t)+r[:3,2]*d).tolist()
def hw(kind,d,length,t,rot,note):
 name=f'{kind}_m{d}'+(f'x{length:g}' if length else '')
 label=f'bottom_{name}_{len(fasteners):03d}'
 oldhw=ROOT/'assemblies/parent_spar_bolted/hardware'
 folder=oldhw if (oldhw/(name+'.step')).exists() else hardware
 if folder==hardware:types[name]=(kind,d,length)
 add(label,str(folder.relative_to(ROOT)).replace('\\','/'),t,rot,'Silver','hardware',name)
 fasteners.append(dict(label=label,type=name,note=note));return label
def joint(d,length,t,rot,grip,note):
 labels=[hw('screw',d,length,along(t,rot,-1),rot,note),hw('washer',d,1,along(t,rot,-1),rot,note),hw('washer',d,1,along(t,rot,grip),rot,note),hw('nut',d,0,along(t,rot,grip+1),rot,note)]
 nh={4:3.2,5:4,6:5}[d]
 assert length>=grip+2+nh and length<=grip+2+nh+8,(note,length,grip)
 joints.append(dict(note=note,labels=labels,first_face=t,axis_rotation=rot,grip_mm=grip,tail_mm=length-grip-2-nh))

for z in [-331,-238]:joint(6,60,[-23,10,z],[0,90,0],46,'cartridge -> beam: two removable cross bolts')
for x in [-23,23]:
 for y in [-23,23]:joint(5,35,[x,y,-343],[180,0,0],23,'cartridge boss -> ballast roof')
for x in [-75,75]:
 for y in [-50,-25]:joint(5,25,[x,y,-355],[180,0,0],13,'disk -> sensor carrier flange')
for x in [-56,-34]:
 for z in [-486,-454]:joint(5,25,[x,-59,z],[90,0,0],16,'camera base -> carrier')
for x in [40,90]:
 for z in [-483,-437]:joint(5,25,[x,-59,z],[90,0,0],16,'TD clamp base -> carrier')
for x in [43,87]:joint(4,65,[x,-20.5,-460],[90,0,0],54.5,'TD split clamp -> body -> carrier (0.5 mm clamp gap)')
# Camera's OEM-style hinge axis is X after downward rotation as well.
hw('screw',5,20,[-37.35,-43,-470],[0,-90,0],'camera case fingers; verify against OEM screw')
items[-1]['ops'].insert(1,{'rotate':[-90,0,0]})
hw('nut',5,0,[-55.65,-43,-470],[0,90,0],'camera mount captive nut')
items[-1]['ops'].insert(1,{'rotate':[-90,0,0]})
for name,(kind,d,length) in types.items():
 if kind=='screw':src=f'union(){{cylinder(d={d},h={length});translate([0,0,-{d}])cylinder(d={1.7*d},h={d});}}'
 else:raise ValueError(name)
 build(hardware,name,'// Purchased hardware envelope. Not printable.\n$fn=32;'+src)

asm=copy.deepcopy(source);asm.update(name='parent_bottom_sensors',items=items,note='Current revision: two rope-only floats; one-piece fin cartridge; camera and TD04A downward at bottom.',coordinate_system='Box bottom Z=0; camera optical axis and TD04A acoustic axis -Z. TD04A d26 x55 is provisional.')
(OUT/'placement.json').write_text(json.dumps(asm,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'fasteners.json').write_text(json.dumps(fasteners,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'joints.json').write_text(json.dumps(joints,ensure_ascii=False,indent=2),encoding='utf-8')
run([sys.executable,ROOT/'scad/lib/asm_gen.py',OUT/'placement.json',OUT/'parent_bottom_sensors_view.scad'],OUT/'view.log')
checks={}
previous_checks=json.loads((OUT/'print_checks.json').read_text()) if (OUT/'print_checks.json').exists() else {}
for it in items:
 if it['group']!='exterior' or '/printed/' not in it['part']:continue
 n=it.get('file',it['part'].split('/')[-1])
 if n not in parts:shutil.copy2(ROOT/'print_jobs/parent_rope_float'/(n+'.stl'),PRINT/(n+'.stl'))
 if n in checks:checks[n]['quantity']+=1;continue
 m=trimesh.load(PRINT/(n+'.stl'),force='mesh')
 assert m.is_watertight and len(m.split())==1,n
 assert m.extents[0]+10<=236 and m.extents[1]+10<=250 and m.extents[2]<=250,(n,m.extents)
 assert abs(m.bounds[0,2])<.05,(n,m.bounds)
 checks[n]=dict(size_mm=m.extents.tolist(),quantity=1,watertight=True,bodies=1)
 if previous_checks.get(n,{}).get('sha256')==hashlib.sha256((PRINT/(n+'.stl')).read_bytes()).hexdigest():
  checks[n].update({k:v for k,v in previous_checks[n].items() if k not in ['quantity','size_mm']})
(OUT/'print_checks.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
run([OSC,'--imgsize=1400,1400','--viewall','--autocenter','--camera=0,0,0,68,0,215,1500','-o',OUT/'preview.png',OUT/'parent_bottom_sensors_view.scad'],OUT/'preview.log')
env=os.environ.copy();env.update(ASM_JSON=str(OUT/'placement.json'),ASM_ROOT=str(ROOT),STEP_OUT=str(OUT/'parent_bottom_sensors.step'))
run([FC,ROOT/'scad/lib/asm_to_step.py'],OUT/'assembly_step.log',env)
print('Assembly',len(items),'items;',len(checks),'print types',flush=True)
