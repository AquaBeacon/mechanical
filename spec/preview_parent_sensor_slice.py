"""Plot actual positive-extrusion paths at the fixture's support transitions."""
from pathlib import Path
import zipfile, re, math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
R=Path(__file__).resolve().parents[1]
O=R/'assemblies/parent_hand_service'
project=O/'_work/analysis/sensor_mounts_20261011/slicing/after/gnss_universal_carrier/gnss_universal_carrier.3mf'
with zipfile.ZipFile(project) as z:
    code=z.read(next(n for n in z.namelist() if n.endswith('.gcode'))).decode('utf-8')
layers=[.2,1.8,5.8,6.0];segments={z:[] for z in layers};colors={z:[] for z in layers}
pos=[0.,0.,0.];last_e=0.;relative=False;feature=''
for line in code.splitlines():
    if line.startswith('; FEATURE: '):feature=line[11:]
    if line.startswith('M83'):relative=True
    if line.startswith('M82'):relative=False
    values={a:float(n) for a,n in re.findall(r'\b([XYZEIJ])(-?[0-9.]+)',line.split(';')[0])}
    if line.startswith('G92 '):last_e=values.get('E',last_e);continue
    if not line.startswith(('G0 ','G1 ','G2 ','G3 ')):continue
    target=[values.get(a,pos[i]) for i,a in enumerate('XYZ')]
    extrusion=values.get('E',0.) if relative else values.get('E',last_e)-last_e
    if 'E' in values and not relative:last_e=values['E']
    layer=round(target[2],3)
    path=[pos,target]
    if line.startswith(('G2 ','G3 ')):
        cx=pos[0]+values.get('I',0);cy=pos[1]+values.get('J',0)
        radius=math.hypot(pos[0]-cx,pos[1]-cy);start=math.atan2(pos[1]-cy,pos[0]-cx);end=math.atan2(target[1]-cy,target[0]-cx)
        angle=(end-start)%(2*math.pi) if line.startswith('G3 ') else -((start-end)%(2*math.pi))
        if abs(angle)<1e-9:angle=2*math.pi if line.startswith('G3 ') else -2*math.pi
        n=max(1,math.ceil(abs(angle)*radius/.1))
        path=[[cx+radius*math.cos(start+angle*i/n),cy+radius*math.sin(start+angle*i/n),target[2]] for i in range(n+1)]
    if layer in segments and extrusion>0 and any(a in values for a in 'XYIJ'):
        for a,b in zip(path,path[1:]):
            segments[layer].append([a[:2],b[:2]])
            colors[layer].append('#ba4ab8' if feature.lower().startswith('support') else '#176c9e')
    pos=target
fig,axes=plt.subplots(2,2,figsize=(12,8))
for ax,z in zip(axes.flat,layers):
    assert segments[z],z
    ax.add_collection(LineCollection(segments[z],colors=colors[z],linewidths=.4))
    ax.autoscale();ax.set_aspect('equal');ax.set_title(f'Actual toolpaths: Z{z:.1f} mm');ax.set_xlabel('X mm');ax.set_ylabel('Y mm')
fig.suptitle('PETG / X1 Carbon 0.4 / 0.2 mm | blue: part, purple: support')
fig.tight_layout()
fig.savefig(O/'_work/images/sensor_slice_layers.png',dpi=140)
print({z:len(segments[z]) for z in layers})
