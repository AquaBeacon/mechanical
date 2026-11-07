"""Plot actual G-code extrusion, interpolating G2/G3 arcs for visual QA."""
from pathlib import Path
import re,math,json,sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
ROOT=Path(__file__).resolve().parents[1]
def read(path):
 point=np.zeros(3);feature='';rows=[];relative=True;e=0.
 for line in path.read_text(encoding='utf-8').splitlines():
  if line.startswith('M83'):relative=True
  if line.startswith('M82'):relative=False
  if line.startswith('; FEATURE:'):feature=line.split(':',1)[1].strip()
  if line.startswith('G92 E'):
   match=re.search(r'E(-?\d*\.?\d+)',line)
   if match:e=float(match.group(1))
  match=re.match(r'^(G[0123])\s',line)
  if not match:continue
  args={k:float(v) for k,v in re.findall(r'([XYZEIJ])(-?\d*\.?\d+)',line)};old=point.copy()
  for n,k in enumerate('XYZ'):
   if k in args:point[n]=args[k]
  extrusion=args.get('E',0) if relative else args.get('E',e)-e
  if 'E' in args:e=args['E'] if not relative else e+args['E']
  if extrusion<=0 or not ('X' in args or 'Y' in args) or not feature:continue
  q=np.array([old,point])
  if match.group(1) in ('G2','G3') and ('I' in args or 'J' in args):
   center=old[:2]+[args.get('I',0),args.get('J',0)]; r=np.linalg.norm(old[:2]-center)
   if r>0:
    a0=math.atan2(old[1]-center[1],old[0]-center[0]);a1=math.atan2(point[1]-center[1],point[0]-center[0])
    delta=(a1-a0)%(2*math.pi)
    if match.group(1)=='G2':delta=-((a0-a1)%(2*math.pi))
    n=max(2,int(math.ceil(abs(delta)*r/.08))+1); angles=np.linspace(a0,a0+delta,n)
    q=np.column_stack((center[0]+r*np.cos(angles),center[1]+r*np.sin(angles),np.linspace(old[2],point[2],n)))
    q[-1]=point
  rows.append((round(float(point[2]),3),feature,q))
 return rows
for stem in ['camera_hand_knob','camera_hand_knob_cap']:
 path=ROOT/'assemblies/parent_exterior/print_jobs/camera_hand_release_20261029'/stem/'plate_1.gcode';rows=read(path)
 fig,axes=plt.subplots(1,4,figsize=(16,4))
 for ax,z in zip(axes,[.2,.3,.4,.8]):
  for cat,col in [('wall','#247895'),('bridge','#d88714'),('support','#8a659f')]:
   lines=[p[:,:2] for zz,f,p in rows if zz==z and cat in f.lower()]
   if lines:ax.add_collection(LineCollection(lines,colors=col,linewidths=.65))
  ax.autoscale();ax.set_aspect('equal');ax.set_title(f'Z={z:g} mm')
 fig.suptitle(stem+' actual G-code, G2/G3 arcs interpolated; blue = wall');fig.tight_layout()
 out=ROOT/'assemblies/parent_exterior/_work/images'/(stem+'_camera_hand_release_20261029_arc_layers.png');fig.savefig(out,dpi=140);plt.close(fig);print(out)
