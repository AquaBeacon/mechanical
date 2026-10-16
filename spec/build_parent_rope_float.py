"""Rope-only attachment of two existing fenders; preserve proven keel parts."""
from pathlib import Path
import sys,json,copy,os,math,subprocess,shutil,zipfile
import trimesh
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'spec'))
from build_parent_spar_bolted import run,OSC,FC
OUT=ROOT/'assemblies/parent_rope_float';OUT.mkdir(exist_ok=True)
PRINT=ROOT/'print_jobs/parent_rope_float';PRINT.mkdir(exist_ok=True)
old=ROOT/'assemblies/parent_spar_bolted'
source=json.loads((old/'placement.json').read_text(encoding='utf-8'))
fast={x['label']:x for x in json.loads((old/'fasteners.json').read_text(encoding='utf-8'))}
items=[];kept=[]
lower={'disk','hub_-295','hub_-202','beam_lower','beam_upper','coupler_front','coupler_back','ballast_body','ballast_lid','ballast_rings'}|{f'fin_{a}' for a in range(0,360,90)}
lower_notes={'fin -> hub','hub -> beam','coupler -> beam','coupler halves','hub -> disk -> ballast roof','ballast lid','metal ballast rings'}
for orig in source['items']:
 it=copy.deepcopy(orig); label=it['label']
 if label.startswith('float_'):continue
 if it['group']=='hardware':
  f=fast[label];note=f['note']
  if 'float' in note or 'top plate' in note or f['type'].startswith('coupling_'):continue
  delta=-60 if note in lower_notes else -460
  kept.append(copy.deepcopy(f))
 else:delta=-60 if label in lower else -460
 it['ops']=[{'translate':[0,0,delta]}]+it['ops'];items.append(it)

folder=ROOT/'parts/parent/exterior/printed/parent_rope_keel_adapter';name=folder.name
scad=folder/(name+'.scad');stl=folder/(name+'.stl');step=folder/(name+'.step');csg=folder/(name+'.csg')
run([OSC,'-o',stl,scad],folder/'render.log')
run([OSC,'-D','part="print"','-o',PRINT/(name+'.stl'),scad],folder/'print_render.log')
run([OSC,'-o',csg,scad],folder/'csg.log')
env=os.environ.copy();env.update(OPENSCAD=OSC,CSG_IN=str(csg),STEP_OUT=str(step),STL_REF=str(stl))
run([FC,ROOT/'scad/lib/csg_to_step.py'],folder/'step.log',env)
assert step.exists()
items.append(dict(label='keel_adapter',part=str(folder.relative_to(ROOT)).replace('\\','/'),color='DarkOrange',group='exterior',ops=[{'translate':[0,0,-68]}]))
# Reuse existing metal hardware envelopes. New plate bolts go into deck inserts.
def hw(kind,t,rot,note):
 label=f'new_{kind}_{len(kept)}';items.append(dict(label=label,part='assemblies/parent_spar_bolted/hardware',file=kind,color='Silver',group='hardware',ops=[{'translate':t},{'rotate':rot}]))
 kept.append(dict(label=label,type=kind,note=note))
for x in [-20,20]:
 for y in [-20,20]:
  hw('screw_m5x16',[x,y,-69],[0,0,0],'keel adapter -> deck M5 insert')
  hw('washer_m5x1',[x,y,-69],[0,0,0],'keel adapter -> deck M5 insert')
hw('screw_m6x60',[-25,0,-88],[0,90,0],'keel adapter -> beam')
hw('washer_m6x1',[-25,0,-88],[0,90,0],'keel adapter -> beam')
hw('washer_m6x1',[24,0,-88],[0,90,0],'keel adapter -> beam')
hw('nut_m6',[25,0,-88],[0,90,0],'keel adapter -> beam')
# Existing bought floats, dimensions remain explicitly provisional.
for side in [-1,1]:
 items.append(dict(label=f'rope_float_{side}',part='parts/parent/exterior/cots/parent_fender',color='LightSkyBlue',group='floats',ops=[{'translate':[side*178,0,0]}],note='Existing fender envelope, diameter100 x length300 provisional; free to move on rope.'))

# A flexible line shown through each central bore, from front to rear deck eyes.
rope='''// Flexible rope ROUTE ENVELOPE, not a rigid member or printable part.
$fn=20; rope_d=4;
module segment(a,b){v=b-a;L=norm(v);translate(a)rotate(a=acos(v[2]/L),v=[-v[1],v[0],0])cylinder(d=rope_d,h=L);}
module route(p){for(i=[0:len(p)-2])segment(p[i],p[i+1]);for(q=p)translate(q)sphere(d=rope_d);}
'''
for s in [-1,1]:
 points=[[s*90,108,-35],[s*118,108,-35],[s*150,170,-20],[s*178,165,0],[s*178,150,0],[s*178,-150,0],[s*178,-165,0],[s*150,-170,-20],[s*118,-108,-35],[s*90,-108,-35]]
 rope+='route('+json.dumps(points)+');\n'
rp=OUT/'rope_routes.scad';rp.write_text(rope,encoding='utf-8')
run([OSC,'-o',OUT/'rope_routes.stl',rp],OUT/'rope_render.log')
run([OSC,'-o',OUT/'rope_routes.csg',rp],OUT/'rope_csg.log')
env.update(CSG_IN=str(OUT/'rope_routes.csg'),STEP_OUT=str(OUT/'rope_routes.step'),STL_REF=str(OUT/'rope_routes.stl'))
run([FC,ROOT/'scad/lib/csg_to_step.py'],OUT/'rope_step.log',env)
if not (OUT/'rope_routes.step').exists():
 env.update(STL_IN=str(OUT/'rope_routes.stl'))
 run([FC,ROOT/'scad/lib/stl_to_step.py'],OUT/'rope_step_fallback.log',env)
assert (OUT/'rope_routes.step').exists(), 'Rope STEP export missing'
items.append(dict(label='flexible_ropes',part='assemblies/parent_rope_float',file='rope_routes',color='BurlyWood',group='ropes',ops=[]))
asm=dict(name='parent_rope_float',note='Two adjacent bought fenders attached ONLY by ropes. No float yokes, collars, rigid links, or cylindrical printed float stack.',coordinate_system='Box bottom Z=0. Float placements and rope curves are a nominal illustration, not constrained rigid placements.',groups={'exterior':True,'interior':False,'vessel':True,'reference':True,'envelope':True,'hardware':True,'floats':True,'ropes':True},items=items)
OUT.joinpath('placement.json').write_text(json.dumps(asm,ensure_ascii=False,indent=2),encoding='utf-8')
OUT.joinpath('fasteners.json').write_text(json.dumps(kept,ensure_ascii=False,indent=2),encoding='utf-8')
run([sys.executable,ROOT/'scad/lib/asm_gen.py',OUT/'placement.json',OUT/'parent_rope_float_view.scad'],OUT/'view.log')
names=set()
for it in items:
 if it['group']=='exterior' and '/printed/' in it['part']:
  n=it.get('file',it['part'].split('/')[-1]);names.add(n)
  if n!=name:shutil.copy2(ROOT/'print_jobs/parent_spar_bolted'/(n+'.stl'),PRINT/(n+'.stl'))
checks={}
for n in sorted(names):
 m=trimesh.load(PRINT/(n+'.stl'),force='mesh');assert m.is_watertight and len(m.split())==1
 assert m.extents[0]+10<=236 and m.extents[1]+10<=250 and m.extents[2]<=250
 checks[n]=dict(size_mm=m.extents.tolist(),quantity=sum(it.get('file',it['part'].split('/')[-1])==n for it in items))
OUT.joinpath('print_checks.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
run([OSC,'--imgsize=1200,1200','--viewall','--autocenter','--camera=0,0,0,68,0,215,1400','-o',OUT/'preview.png',OUT/'parent_rope_float_view.scad'],OUT/'preview.log')
env.update(ASM_JSON=str(OUT/'placement.json'),ASM_ROOT=str(ROOT),STEP_OUT=str(OUT/'parent_rope_float.step'))
run([FC,ROOT/'scad/lib/asm_to_step.py'],OUT/'assembly_step.log',env)
print('Built',len(items),'items;',len(checks),'print types',flush=True)
