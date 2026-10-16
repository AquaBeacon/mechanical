"""Inspect original TAKACHI DXF geometry without changing reference data."""
from pathlib import Path
import json, math
import ezdxf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

R=Path(__file__).resolve().parents[1]
P=R/'parts/parent/exterior/cots/bcas212310g'
O=P/'_work/analysis/cad_correction_20261010'
O.mkdir(parents=True,exist_ok=True)
I=P/'_work/images';I.mkdir(parents=True,exist_ok=True)
doc=ezdxf.readfile(P/'ref/BCAS212310G.dxf')
entities=[]
for e in doc.modelspace():
    if e.dxftype()=='LWPOLYLINE':
        entries=e.virtual_entities()
    else:entries=[e]
    for q in entries:
        k=q.dxftype()
        if k=='LINE':
            row=dict(kind=k,handle=e.dxf.handle,layer=e.dxf.layer,start=list(q.dxf.start)[:2],end=list(q.dxf.end)[:2])
        elif k in ['ARC','CIRCLE']:
            row=dict(kind=k,handle=e.dxf.handle,layer=e.dxf.layer,centre=list(q.dxf.center)[:2],radius=q.dxf.radius,start_angle=q.dxf.start_angle if k=='ARC' else 0,end_angle=q.dxf.end_angle if k=='ARC' else 360)
        else:continue
        entities.append(row)
(O/'dxf_entities.json').write_text(json.dumps(entities,indent=2),encoding='utf-8')
regions={'body_plan':(2130,2375,447,673),'body_corner':(2135,2175,630,668),'section_bb':(2130,2380,820,932),'section_aa':(2130,2380,190,302),'section_dd':(2520,2648,447,673),'section_ee':(1960,2010,190,302)}
for name,(xmin,xmax,ymin,ymax) in regions.items():
    fig,ax=plt.subplots(figsize=(14,8))
    selected=[]
    for row in entities:
        if row['kind']=='LINE':xx=[row['start'][0],row['end'][0]];yy=[row['start'][1],row['end'][1]]
        else:
            a=row['start_angle'];b=row['end_angle']
            if b<=a:b+=360
            ts=[math.radians(a+(b-a)*i/64) for i in range(65)]
            xx=[row['centre'][0]+row['radius']*math.cos(t) for t in ts]
            yy=[row['centre'][1]+row['radius']*math.sin(t) for t in ts]
        if min(xx)<xmin or max(xx)>xmax or min(yy)<ymin or max(yy)>ymax:continue
        if row['layer'] in ['AM_7','0']:continue
        selected.append(row)
        layer=row['layer'];color='#cf222e' if 'FF84' in layer else '#0969da' if 'FF8E' in layer else '#aaa'
        ax.plot(xx,yy,color=color,lw=.7)
        if name!='body_plan':ax.text(xx[len(xx)//2],yy[len(yy)//2],row['handle'],fontsize=4)
    ax.set(xlim=(xmin,xmax),ylim=(ymin,ymax),title=name);ax.set_aspect('equal');ax.grid(alpha=.2)
    fig.savefig(I/(name+'_dxf.png'),dpi=180);plt.close(fig)
    (O/(name+'_entities.json')).write_text(json.dumps(selected,indent=2),encoding='utf-8')
print(O)
