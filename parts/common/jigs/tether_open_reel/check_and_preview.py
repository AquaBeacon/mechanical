"""Inspect exported parts; derive assembly placements from the SCAD source."""
from pathlib import Path
import re,json,subprocess,math
import trimesh
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent
ROOT=P.parents[3]
name=P.name
s=(P/f'{name}.scad').read_text()
vals={k:float(v) for k,v in re.findall(r'^([a-z_]+)\s*=\s*([\d.]+)\s*;',s,re.M)}
v=vals
w=v['winding_width']+2*v['flange_t'];r=v['flange_d']/2
sr=r+v['shell_clear']+v['shell_wall'];f=v['stand_floor']
parts={'base':1,'lid':1,'stand':1,'cover_half':2,'clip':4,'coupon_socket':1,'coupon_spring':1}
report={}
for part,count in parts.items():
 m=trimesh.load_mesh(P/f'{name}_{part}.stl')
 report[part]=dict(count=count,size_mm=m.extents.round(3).tolist(),watertight=bool(m.is_watertight),
                  consistent=bool(m.is_winding_consistent),components=len(m.split(only_watertight=False)))
 assert m.is_watertight and m.is_winding_consistent and report[part]['components']==1,report[part]
 assert max(m.extents[:2])<237 and m.extents[2]<250
cap=v['packing_factor']*((v['flange_d']-2*v['rim_reserve'])**2-v['core_d']**2)*v['winding_width']/v['cable_d']**2/1000
report['capacity_estimate_m']=cap
report['snap_beam_strain_estimate']=1.5*v['spring_t']*v['hook_depth']/v['spring_l']**2
report['clip_strain_estimate']=1.5*v['clip_t']*(v['tab_half_w']-(v['clip_gap']/2-v['clip_hook']))/(v['clip_l']-v['clip_t'])**2
(P/'mesh_check.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
rel='parts/common/jigs/tether_open_reel'
def comp(p,label,ops,col='SlateGray'):
 return dict(part=rel,file=f'{name}_{p}',label=label,ops=ops,color=col,group='reel')
for closed in [False,True]:
 aname='tether_open_reel_closed' if closed else 'tether_open_reel'
 ap=ROOT/'assemblies'/aname;ap.mkdir(exist_ok=True)
 outer=[{'translate':[0,w/2,f+(sr if closed else r)]},{'rotate':[90,0,0]}]
 cs=[comp('stand','Upright cradle',[], 'DarkSlateGray'),comp('base','Single winding chamber',outer),
     comp('lid','Side plate with two release latches',outer+[{'translate':[0,0,w]},{'rotate':[180,0,0]}],'Orange')]
 if closed:
  for a in [0,180]:cs.append(comp('cover_half',f'Transport half {a}',outer+[{'rotate':[0,0,a]},{'translate':[0,0,-v['cover_lip']-v['fit_clear']]}],'LightSteelBlue'))
  for side in [0,180]:
   for z in [30,w-30]:cs.append(comp('clip',f'Removable clip {side}/{z}',outer+[{'rotate':[0,0,side]},
      {'translate':[sr-v['clip_l']+v['clip_t'],0,z-v['tab_axial_w']/2]}],'Tomato'))
 # Same schema as other Body_Models assemblies.
 (ap/'placement.json').write_text(json.dumps({'name':aname,'parts':cs},indent=2),encoding='utf-8')
 cmd=['python',str(ROOT/'scad/lib/asm_gen.py'),str(ap/'placement.json'),str(ap/f'{aname}_view.scad')]
 subprocess.run(cmd,check=True,capture_output=True)
osc=r'C:/Program Files/OpenSCAD/openscad.com'
for part in ['assembly','closed','latch_detail']:
 subprocess.run([osc,'-o',str(P/f'{name}_{part}_preview.png'),'--imgsize=1000,900',
  '--camera=0,0,120,75,0,35,800','--viewall','--autocenter','--projection=o','--render',
  '-D',f'part="{part}"',str(P/f'{name}.scad')],check=True,capture_output=True)
fontpath='C:/Windows/Fonts/meiryo.ttc'
font=ImageFont.truetype(fontpath,28)
canvas=Image.new('RGB',(2000,1020),'#f4f6f8');d=ImageDraw.Draw(canvas)
for i,label in enumerate(['使用時：両側に開口・収納部は一つ','移動時：カバー＋印刷クリップ']):
 canvas.paste(Image.open(P/f'{name}_{["assembly","closed"][i]}_preview.png').convert('RGB'),(i*1000,60))
 d.text((i*1000+55,16),label,font=font,fill='#243c46')
d.text((55,969),'30 m / 標準径7.6 mm　　X1 Carbon：最大部品236×118×186.8 mm　　PETG試作',font=font,fill='#243c46')
canvas.save(P/f'{name}_preview.png')
print('Mesh checks PASS; capacity estimate',round(cap,2),'m; assembly placements and previews saved')
