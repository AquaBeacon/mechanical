"""Deterministic placement and fastener BOM for the screw-fastened parent."""
from pathlib import Path
import math,json,sys,subprocess,os
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_parent_spar_bolted import ROOT,OUT,PRINT,OSC,FC,run

items=[]; fasteners=[]
def add(label,part,t=(0,0,0),rot=None,color='DarkOrange',group='exterior',file=None,mirror=None):
 ops=[{'translate':list(t)}]
 if rot: ops.append({'rotate':list(rot)})
 if mirror: ops.append({'mirror':mirror})
 item=dict(label=label,part=part,ops=ops,color=color,group=group)
 if file:item['file']=file
 items.append(item)
def printed(key,label=None,t=(0,0,0),rot=None,color='DarkOrange',mirror=None):
 add(label or key,'parts/parent/exterior/printed/parent_spar_'+key,t,rot,color,mirror=mirror)

printed('disk',t=(0,0,-300),color='Orange')
for a in range(0,360,90):
 c,s=math.cos(math.radians(a)),math.sin(math.radians(a))
 printed('fin',f'fin_{a}',(30*c+2*s,30*s-2*c,-295),(0,0,a),'Gold')
for z in [-295,-202]:printed('hub',f'hub_{z}',(0,0,z))
printed('beam_lower',t=(0,0,-295),color='DarkSlateGray')
printed('beam_upper',t=(0,0,-115),color='DarkSlateGray')
printed('coupler_half','coupler_front',(0,0,-147))
printed('coupler_half','coupler_back',(0,0,-147),mirror=[0,1,0])
printed('float_bottom',t=(0,0,-8))
for i,z in enumerate([0,186]):
 printed('float_body',f'float_body_{i}',(0,0,z),color='LightSkyBlue')
 printed('float_lid',f'float_lid_{i}',(0,0,z+180),color='SkyBlue')
printed('float_top',t=(0,0,372))
printed('ballast_body',t=(0,0,-300),rot=(180,0,0),color='SlateGray')
printed('ballast_lid',t=(0,0,-357),color='SlateGray')
printed('camera_bridge',t=(0,0,322))
printed('gps_bridge',t=(108,70,410))
add('deck','parts/parent/exterior/printed/parent_deck',(0,0,460))
add('camera_mount','parts/child/exterior/printed/dji_osmo_action6_mount',(0,190,330),color='SteelBlue')
# Keep the established box and existing P1 interior together; no invented IMU.
old=json.loads((ROOT/'assemblies/parent_assembly/placement.json').read_text(encoding='utf-8'))
for it in old['items']:
 if it['group']=='interior' or it['label']=='box_bcas212310g' or 'penetrator' in it['part']:
  clone=json.loads(json.dumps(it)); clone['ops']=[{'translate':[0,0,460]}]+clone.get('ops',[])
  items.append(clone)

REF=OUT/'reference';REF.mkdir(exist_ok=True)
def reference(name,source,color,t,rot=None):
 scad=REF/(name+'.scad'); scad.write_text(source,encoding='utf-8')
 run([OSC,'-o',REF/(name+'.stl'),scad],REF/(name+'.log'))
 csg=REF/(name+'.csg');step=REF/(name+'.step')
 run([OSC,'-o',csg,scad],REF/(name+'_csg.log'))
 env=os.environ.copy();env.update(OPENSCAD=OSC,CSG_IN=str(csg),STEP_OUT=str(step),STL_REF=str(REF/(name+'.stl')))
 run([FC,ROOT/'scad/lib/csg_to_step.py'],REF/(name+'_step.log'),env)
 add(name,str(REF.relative_to(ROOT)).replace('\\','/'),t,rot,color,'reference',name)
reference('gps_ann_mb1','use <../../../scad/lib/parent_spar_bolted.scad>\ngps_reference();','Black',(65,70,593))
reference('camera_case_envelope','// Provisional case envelope; no print.\ntranslate([-47.5,-22.95,0]) cube([95,45.9,75]);','DimGray',(0,190,366.5))
reference('box_lid_envelope','// Purchased lid envelope, not print.\ncube([210,230,4]);','LightSteelBlue',(-105,-115,556.3))
for it in items:
 if it['label'] in ['camera_case_envelope','box_lid_envelope']:it['group']='envelope'
reference('ballast_rings','// Purchased steel ring stack: OD50/ID9, 10 x 3 mm. Not printable.\n$fn=64;difference(){cylinder(d=50,h=30);translate([0,0,-1])cylinder(d=9,h=32);}','Gray',(0,0,-336))

HARD=OUT/'hardware';HARD.mkdir(exist_ok=True)
types={}
def hw(kind,d,length,t,rot=(0,0,0),note=''):
 name=f'{kind}_m{d}'+(f'x{length:g}' if length else '')
 types[name]=(kind,d,length)
 label=f'{name}_{len(fasteners):03d}'
 add(label,str(HARD.relative_to(ROOT)).replace('\\','/'),t,rot,'Silver','hardware',name)
 fasteners.append(dict(label=label,type=name,note=note))
def along(t,rot,dist):
 import trimesh,numpy as np
 r=trimesh.transformations.euler_matrix(*np.radians(rot),axes='sxyz')
 return (np.array(t)+r[:3,2]*dist).tolist()
def joint(d,length,t,rot,grip,note,nut=True):
 # t = first mating face. Washer occupies -1..0; screw shoulder -1.
 hw('screw',d,length,along(t,rot,-1),rot,note)
 hw('washer',d,1,along(t,rot,-1),rot,note)
 if nut:
  hw('washer',d,1,along(t,rot,grip),rot,note)
  hw('nut',d,0,along(t,rot,grip+1),rot,note)

for a in range(0,360,90):
 c,s=math.cos(math.radians(a)),math.sin(math.radians(a))
 for z in [-285,-192]:joint(5,40,(37*c+16*s,37*s-16*c,z),(-90,0,a),32,'fin -> hub')
for z in [-271,-178]:joint(6,100,(-44,10,z),(0,90,0),88,'hub -> beam')
for z in [-135,-95]:joint(6,70,(-27,0,z),(0,90,0),54,'coupler -> beam')
for x in [-22,22]:
 for z in [-123,-107]:joint(5,65,(x,-27,z),(-90,0,0),54,'coupler halves')
joint(6,60,(-23,0,-28),(0,90,0),46,'float bottom -> beam')
# Shared disk / lower hub / ballast roof bolts, inserted from above.
for x in [-23,23]:
 for y in [-23,23]:joint(5,55,(x,y,-263),(180,0,0),43,'hub -> disk -> ballast roof')
for a in range(0,360,90):
 c,s=math.cos(math.radians(a)),math.sin(math.radians(a))
 joint(5,20,(52*c,52*s,-357),(0,0,0),12,'ballast lid')
joint(8,50,(0,0,-300),(180,0,0),36,'metal ballast rings')
for z in [0,186]:
 for a in [22.5+45*i for i in range(8)]:
  x,y=105.5*math.cos(math.radians(a)),105.5*math.sin(math.radians(a))
  joint(4,20,(x,y,z+186),(180,0,0),12,'float lid and seal')
for a in [45,135,225,315]:
 x,y=105.5*math.cos(math.radians(a)),105.5*math.sin(math.radians(a))
 hw('rod',6,205,(x,y,-18),note='float stack lower tie rod')
 hw('rod',6,205,(x,y,188),note='float stack upper tie rod')
 hw('coupling',6,18,(x,y,178),note='M6 coupling nut; 9 / 8 mm engagement, 1 mm tip gap')
 for z in [-9,380]:hw('washer',6,1,(x,y,z),note='float stack')
 for z in [-14,381]:hw('nut',6,0,(x,y,z),note='float stack')
for x in [-20,20]:
 for y in [-20,20]:
  joint(5,20,(x,y,389),(0,0,0),11,'top plate -> deck insert, 2 washers',False)
  hw('washer',5,1,(x,y,389),note='second top plate washer')
 for y in [50,90]:joint(5,16,(x,y,392),(0,0,0),8,'camera bridge -> deck insert',False)
for x in [-11,11]:
 for y in [174,206]:joint(5,25,(x,y,338),(180,0,0),16,'camera mount -> bridge')
for y in [50,90]:
 for z in [415,455]:joint(5,20,(118,y,z),(0,-90,0),10,'GPS bridge -> deck side insert',False)
for y in [36,104]:joint(4,25,(65,y,599),(180,0,0),14,'antenna ears -> GPS shelf')
for x in [-96,96]:
 for y in [-106,106]:joint(4,16,(x,y,466),(180,0,0),6,'box external feet -> deck M4 insert',False)
hw('screw',5,20,(7.65,190,354),(0,-90,0),'camera case fingers; verify against OEM screw')
hw('nut',5,0,(-10.65,190,354),(0,90,0),'camera mount captive nut')

for name,(kind,d,length) in types.items():
 af={4:7,5:8,6:10,8:13}[d]; nh={4:3.2,5:4,6:5,8:6.5}[d]
 if kind=='screw': src=f'union(){{cylinder(d={d},h={length});translate([0,0,-{d}])cylinder(d={1.7*d},h={d});}}'
 elif kind=='rod':src=f'cylinder(d={d},h={length});'
 elif kind in ['nut','coupling']:
  nh=length if kind=='coupling' else nh
  src=f'difference(){{cylinder(d={af}/cos(30),h={nh},$fn=6);translate([0,0,-1])cylinder(d={d},h={nh+2});}}'
 else:src=f'difference(){{cylinder(d={ {4:9,5:10,6:12,8:16}[d]},h=1);translate([0,0,-1])cylinder(d={d+0.5},h=3);}}'
 scad=HARD/(name+'.scad')
 fullsrc='// Purchased hardware envelope; no modeled threads, not print.\n$fn=32;\n'+src
 if scad.exists() and scad.read_text(encoding='utf-8')==fullsrc and (HARD/(name+'.stl')).exists() and (HARD/(name+'.step')).exists():continue
 scad.write_text(fullsrc,encoding='utf-8')
 run([OSC,'-o',HARD/(name+'.stl'),scad],HARD/(name+'.log'))
 # Hardware STEP via CSG also, for complete named assembly output.
 csg=HARD/(name+'.csg');step=HARD/(name+'.step')
 run([OSC,'-o',csg,scad],HARD/(name+'_csg.log'))
 env=os.environ.copy();env.update(OPENSCAD=OSC,CSG_IN=str(csg),STEP_OUT=str(step),STL_REF=str(HARD/(name+'.stl')))
 run([FC,ROOT/'scad/lib/csg_to_step.py'],HARD/(name+'_step.log'),env)

assembly={'name':'parent_spar_bolted','note':'2026-09-10 screw-fastened modular parent. Reference case/lid envelopes are not manufacturing models.','coordinate_system':'mm; float lower face Z=0; box bottom Z=460; +Y camera direction.','groups':{'exterior':True,'interior':False,'vessel':True,'reference':True,'envelope':True,'hardware':True},'items':items}
OUT.joinpath('placement.json').write_text(json.dumps(assembly,ensure_ascii=False,indent=2),encoding='utf-8')
OUT.joinpath('fasteners.json').write_text(json.dumps(fasteners,ensure_ascii=False,indent=2),encoding='utf-8')
run([sys.executable,ROOT/'scad/lib/asm_gen.py',OUT/'placement.json',OUT/'parent_spar_bolted_view.scad'],OUT/'view.log')
print('Assembly placements:',len(items),'hardware instances:',len(fasteners),flush=True)
