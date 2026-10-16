from pathlib import Path
import json,hashlib,itertools
import numpy as np,trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from topopt.voxel import voxelize_stl
R=Path(__file__).resolve().parents[1];O=R/'assemblies/child_petg100_design';C=O/'cad'
plt.rcParams['font.family']='Yu Gothic'
names=['child_core_frame','child_jaw_gate','child_cam_bridge','vertical_light_saddle','vertical_light_cap','td04a_socket']
colors=['#5486b0','#47b095','#d69d4a','#ddbf52','#ccaa33','#aa75bb']
meshes={n:trimesh.load(C/(n+'_print.stl')) for n in names}
manifest=[]
for n,m in meshes.items():
 manifest.append(dict(name=n,stl=n+'_print.stl',step=n+'.step',watertight=bool(m.is_watertight),single_solid=len(m.split())==1,volume_cm3=float(m.volume/1000),mass_kg=float(m.volume*1.27e-6),bounds_mm=m.bounds.tolist(),sha256=hashlib.sha256((C/(n+'_print.stl')).read_bytes()).hexdigest()))
(C/'manifest.json').write_text(json.dumps(manifest,indent=2))
# Shared-grid geometric screening; sub-voxel details are not certified by this check.
grid={n:voxelize_stl(m.triangles,h=1,origin=[-120,-150,-50],shape=[260,310,350]).solid for n,m in meshes.items()}
checks=[]
for a,b in itertools.combinations(names,2):
 count=int((grid[a]&grid[b]).sum());checks.append(dict(a=a,b=b,overlap_mm3=count))
for p in (O/'scene').glob('*.stl'):
 if p.stem=='td04a_socket':continue
 mask=voxelize_stl(p,h=1,origin=[-120,-150,-50],shape=[260,310,350]).solid
 for n in names:
  # light/cap/socket use mating hardware spaces deliberately; only actual COTS body is checked.
  checks.append(dict(a=n,b='reserved_'+p.stem,overlap_mm3=int((grid[n]&mask).sum())))
(O/'assembly_overlap_1mm.json').write_text(json.dumps(checks,indent=2))
print('Overlaps', [x for x in checks if x['overlap_mm3']],flush=True)
def scene(ax,items,az=60):
 ts=[];cs=[]
 for m,c in items:
  ts.extend(m.triangles);cs.extend([to_rgba(c)]*len(m.faces))
 ax.add_collection3d(Poly3DCollection(ts,facecolors=cs,edgecolors='none'))
 ax.set(xlim=(-120,120),ylim=(-130,145),zlim=(-35,290),xlabel='X',ylabel='Y',zlabel='Z')
 ax.set_box_aspect((240,275,325));ax.view_init(23,az)
items=list(zip(meshes.values(),colors))
fig=plt.figure(figsize=(15,8));
for i,az in enumerate([60,-120]):
 ax=fig.add_subplot(1,2,i+1,projection='3d');scene(ax,items,az);ax.set_title('前方' if i==0 else '後方・持ち手')
fig.suptitle('PETG 100%・実際のSTEPから生成した設計CAD');fig.savefig(O/'design.png',dpi=130);plt.close(fig)
reserve=[(trimesh.load(O/'scene'/f'{n}.stl'),c) for n,c in [('pressure_vessel','#9bc4dc'),('cameras','#dcac52'),('light_vertical','#d8d341'),('td04a','#a980bd'),('hand_clearance','#e48795'),('cables','#505050')]]
fig=plt.figure(figsize=(9,9));scene(fig.add_subplot(111,projection='3d'),reserve,60);fig.suptitle('除外領域：耐圧容器・カメラ1台・縦ライト・TD04A・手・配線');fig.savefig(O/'reservations.png',dpi=120);plt.close(fig)
# One panel per actual analysis case, every regional force represented.
links=[]
for n in names:
 study=(O/'verification/studies'/f'{n}.json') if n in names[:3] else (O/'fixture_checks'/f'{n}.json')
 d=json.loads(study.read_text(encoding='utf-8'))
 extra=O/'verification/studies'/f'{n}_transport500.json'
 if extra.exists():d['cases']+=json.loads(extra.read_text(encoding='utf-8'))['cases']
 for j,case in enumerate(d['cases']):
  fig=plt.figure(figsize=(11,8));ax=fig.add_subplot(111,projection='3d');scene(ax,[(meshes[n],'#becbd2')],60 if n!='child_core_frame' else -120)
  labels=[]
  for k,l in enumerate(case.get('loads',[])):
   r=d['regions'][l['region']]
   if 'min' in r:p=(np.array(r['min'])+r['max'])/2
   else:p=np.array(r.get('centre',[0,0,0]),float);p['XYZ'.index(r.get('axis','Z'))]=np.mean(r.get('range',[0,0]))
   f=np.array(l['force'],float);norm=np.linalg.norm(f)
   if norm:ax.quiver(*p,*(f/norm*35),color='#d63031',arrow_length_ratio=.25)
   ax.text(*p,str(k+1),color='red');labels.append(f'{k+1}: {l["region"]} F={np.round(f,2).tolist()} N')
  g=case.get('gravity')
  if g:
   labels.append('分布自重 gravity='+str(g)+'（実体全体に適用）')
   v=np.array(g if isinstance(g,list) else g.get('direction',[0,0,-1]),float);v=v/(np.linalg.norm(v) or 1)
   ax.quiver(-100,0,230,*(v*50),color='purple',arrow_length_ratio=.2)
  fig.suptitle(case['name'],fontsize=10);fig.text(.02,.02,'\n'.join(labels),fontsize=8)
  fn=f'forces_{n}_{j+1}.png';fig.savefig(O/fn,dpi=110);plt.close(fig);links.append((case['name'],fn))
html='<!doctype html><meta charset="utf-8"><title>PETG100設計</title><style>body{font-family:sans-serif;max-width:1100px;margin:30px auto;background:#f4f6f8}img{max-width:100%}p{line-height:1.7}</style><h1>PETG 100% 子機外装</h1><p>設計CAD。解析・干渉検査の制限は README.md を参照。荷重の矢印は方向を示し、長さは力に比例しません。</p><img src="design.png"><h2>除外領域</h2><img src="reservations.png"><h2>考慮した全荷重ケース</h2>'
for title,fn in links:html+=f'<h3>{title}</h3><img src="{fn}">'
(O/'review.html').write_text(html,encoding='utf-8')
print('review generated',flush=True)
