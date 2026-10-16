"""Plot actual STL center sections and projected left link for design review."""
from pathlib import Path
import json,sys
import numpy as np,trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from shapely.affinity import rotate,translate
from dji_verify import section
from geometry import layout,dead_angle

ROOT=Path(__file__).resolve().parents[2];P=ROOT/'parts/common/jigs/over_center_latch'
v=json.loads((P/'parameters.json').read_text(encoding='utf-8'))
fig,axes=plt.subplots(3,1,figsize=(12,9))
colors={'base':'#7d8e9a','keeper':'#38845b','lever':'#3d80b5','link_left':'#d99625','epdm':'#212121'}
for ax,(theta,lift,title) in zip(axes,[(v['closed_angle_deg'],0,'Closed / nominal 40 N'),(dead_angle(v),0,'Dead point'),(v['open_angle'],v['release_angle'],'Hood lifted / claw disengaged')]):
    for i in layout(v,theta,lift):
        name=i['label']
        if name not in colors:continue
        m=trimesh.load(P/(i['file']+'.stl'))
        poly=section(m,v['link_thickness']/2 if name=='link_left' else 0)
        poly=translate(rotate(poly,-i['ops'][1]['rotate'][1],origin=(0,0)),xoff=i['ops'][0]['translate'][0],yoff=i['ops'][0]['translate'][2])
        for q in ([poly] if poly.geom_type=='Polygon' else poly.geoms):
            ax.fill(*q.exterior.xy,color=colors[name],alpha=.95)
            for ring in q.interiors:ax.fill(*ring.xy,color='white')
    if theta==v['closed_angle_deg']:
        x=v['catch_distance']+v['toe_face_x'];seam=v['host_seam_x']
        ax.annotate('',xy=(x,-7),xytext=(seam,-7),arrowprops=dict(arrowstyle='<->',color='#b72b2b'))
        ax.text((x+seam)/2,-6.7,f'{x-seam:.1f} mm from seam',ha='center',color='#b72b2b',fontsize=9)
    ax.set_title(title);ax.set_aspect('equal');ax.set_xlim(-56,51);ax.set_ylim(-9,40)
    ax.set_ylabel('Z (mm)');ax.grid(alpha=.12)
axes[-1].set_xlabel('X (mm) / center section; left link projected; EPDM shown in closed outline')
fig.tight_layout();fig.savefig(ROOT/'assemblies/over_center_latch/_work/images/section_operation.png',dpi=160)
