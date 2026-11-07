"""Offline installed X1C/PETG profile check. No printer connection."""
import hashlib
import json
import math
import re
from pathlib import Path
from topopt import slicer
from topopt.cli import slice as native
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'assemblies/child_interior/parts/child_spacer_set_set.stl'
JOB=ROOT/'assemblies/child_interior/print_jobs/child_spacer_set'
JOB.mkdir(parents=True,exist_ok=True)
original=native._write_presets


def presets(*args,**kwargs):
    files=original(*args,**kwargs)
    path=Path(files['process']);data=json.loads(path.read_text(encoding='utf-8'))
    data.update(layer_height='0.2',initial_layer_print_height='0.2',wall_loops='4',
        sparse_infill_density='100%',sparse_infill_pattern='alignedrectilinear',brim_type='no_brim',skirt_loops='0',
        enable_support='1',support_type='normal(auto)',support_on_build_plate_only='0',
        support_threshold_angle='45',enable_prime_tower='0')
    path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    return files


native._write_presets=presets
code=native.main([str(SOURCE),'--out',str(JOB),'--printer','X1C','--material','PETG',
    '--layer-mm','0.2','--supports','auto','--orient','keep','--bed-type','Textured PEI Plate',
    '--timeout','240','--quiet'])
report=json.loads((JOB/'slice.json').read_text(encoding='utf-8'))
record=dict(source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),material='PETG',
    nozzle_mm=.4,layer_height_mm=.2,walls=4,infill_percent=100,
    support_detection='normal(auto), 45 degrees, all surfaces',slice_exit=code,
    support_mm=slicer.support_mm(report.get('filament_by_feature_mm',{})),slice=report)
(JOB/'source_manifest.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
if code or not report.get('pass'):
    print(json.dumps(record,indent=2))
    raise SystemExit(1)

# Inspect the actual extrusion paths, including Bambu's G2/G3 arcs.
layers={.2:[],.4:[]};z=None;pos=np.zeros(2);relative=True;last_e=0
for raw in Path(report['plate_gcode']).read_text(encoding='utf-8').splitlines():
    if raw.startswith('; Z_HEIGHT:'):z=round(float(raw.split(':')[1]),4)
    line=raw.split(';')[0].strip()
    if line=='M83':relative=True
    if line=='M82':relative=False
    if not re.match(r'G[123] ',line):continue
    vals={k:float(v) for k,v in re.findall(r'([XYEIJ])(-?\d*\.?\d+)',line)}
    target=np.array([vals.get('X',pos[0]),vals.get('Y',pos[1])])
    e=vals.get('E',0) if relative else vals.get('E',last_e)-last_e
    if 'E' in vals:last_e=vals['E']
    if z in layers and e>0 and np.linalg.norm(target-pos)>.0001:
        points=np.array([pos.copy(),target.copy()])
        if line.startswith(('G2 ','G3 ')) and ('I' in vals or 'J' in vals):
            center=pos+np.array([vals.get('I',0),vals.get('J',0)])
            a=math.atan2(*(pos-center)[::-1]);b=math.atan2(*(target-center)[::-1])
            delta=(b-a)%(2*math.pi) if line.startswith('G3') else -((a-b)%(2*math.pi))
            theta=np.linspace(a,a+delta,max(2,int(abs(delta)*30)))
            points=center+np.linalg.norm(pos-center)*np.column_stack([np.cos(theta),np.sin(theta)])
        layers[z].append(points)
    pos=target

fig,axes=plt.subplots(2,1,figsize=(12,6))
connections={}
for ax,(height,paths) in zip(axes,layers.items()):
    for points in paths:ax.plot(points[:,0],points[:,1],color='#137c8b',lw=1)
    # Four separated pairs of long vertical extrusion segments are the necks.
    candidates=[]
    for pts in paths:
        if len(pts)==2 and abs(pts[1,0]-pts[0,0])<.001 and abs(pts[1,1]-pts[0,1])>1:
            candidates.append(float(pts[:,0].mean()))
    groups=[]
    for x in sorted(candidates):
        if not groups or x-groups[-1][-1]>1:groups.append([x])
        else:groups[-1].append(x)
    # Circle sides are arcs; long straight runs come from the four thin necks
    # and the two runner ends. Keep pairs at the 10 mm spacer pitch.
    centers=[float(np.mean(g)) for g in groups if len(g)>=2]
    connected=len(centers)==4 and np.allclose(np.diff(centers),10,atol=.05)
    connections[str(height)]=dict(neck_centers_x_mm=centers,all_four_necks_extruded=bool(connected))
    ax.set(title=f'PETG / X1C / layer Z={height:.1f} mm',xlabel='X [mm]',ylabel='Y [mm]',aspect='equal')
    if not connected:raise RuntimeError(f'Missing neck toolpaths at Z={height}: {centers}')
fig.tight_layout()
image_path=ROOT/'parts/child/interior/printed/child_spacer_set/_work/images/first_two_layers.png'
fig.savefig(image_path,dpi=150);plt.close(fig)
record['toolpaths']=connections
(JOB/'source_manifest.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(pass_=True,support_mm=record['support_mm'],toolpaths=connections),indent=2))
