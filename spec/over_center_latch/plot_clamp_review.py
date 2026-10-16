"""Plot conditional operating forces and measured CAD volumes."""
from pathlib import Path
import json
import numpy as np
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from clamp_loads import load_at
from geometry import closed_angle,dead_angle

root=Path(__file__).resolve().parents[2];p=root/'parts/common/jigs/over_center_latch'
v=json.loads((p/'parameters.json').read_text());angles=np.linspace(v['open_angle'],closed_angle(v),801)
rows=[load_at(v,a) for a in angles]
fig,ax=plt.subplots(1,2,figsize=(12,4.5),layout='constrained')
for field,label in [('gasket_N','Horizontal clamp'),('link_N','Two-link compression'),('hand_vertical_N','Hand force magnitude')]:
 ax[0].plot(angles,[abs(r[field]) for r in rows],label=label)
ax[0].axvline(dead_angle(v),color='gray',ls=':',label='Dead centre')
ax[0].set(xlabel='Link angle / deg',ylabel='Force / N',title='Target: 40 N closed clamping force')
ax[0].legend(fontsize=8);ax[0].grid(alpha=.25)
before=p/'_work/analysis/dji_groove40N_20261010/before/parts/common/jigs/over_center_latch'
names=['lever','bail'];old=[];new=[]
for n in names:
 old.append(trimesh.load(before/('over_center_latch_'+n+'.stl')).volume/1000)
 new.append(trimesh.load(p/('over_center_latch_'+n+'.stl')).volume/1000*(2 if n=='bail' else 1))
x=np.arange(2);ax[1].bar(x-.18,old,.36,label='Previous');ax[1].bar(x+.18,new,.36,label='Revised')
for i in range(2):ax[1].text(i,new[i]+1,f'{100*(1-new[i]/old[i]):.1f}% less volume',ha='center',fontsize=9)
ax[1].set(xticks=x,xticklabels=['Hood lever','Old hook / two short links'],ylabel='CAD volume / cm³',title='Canonical printed component volumes');ax[1].legend()
fig.suptitle('PETG Basic V3 + EPGR-01: conditional design calculation, not a measured rating',fontsize=11)
fig.savefig(root/'assemblies/over_center_latch/_work/images/clamp_40N_review.png',dpi=160)
