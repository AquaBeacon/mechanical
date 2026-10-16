from pathlib import Path
import json,trimesh,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
p=Path(__file__).resolve().parent
m=trimesh.load(p/'bulkhead_wrench.stl')
r=json.loads((p/'step_validation.json').read_text())
r.update(stl_watertight=bool(m.is_watertight),stl_winding_consistent=bool(m.is_winding_consistent),stl_components=len(m.split()),stl_volume_mm3=float(m.volume),stl_bounds_mm=m.extents.tolist())
r['relative_volume_difference']=abs(m.volume-r['step_volume_mm3'])/r['step_volume_mm3']
assert r['stl_watertight'] and r['stl_winding_consistent'] and r['stl_components']==1
assert r['relative_volume_difference']<0.002
assert np.max(np.abs(m.extents-np.array(r['bounds_mm'])))<0.05
(p/'validation.json').write_text(json.dumps(r,indent=2))
fig=plt.figure(figsize=(13,7),facecolor='#f4f6f8')
for n,(elev,azim,title) in enumerate([(28,35,'Reinforced wrench + integrated T handle'),(90,0,'Working end / cable entry')]):
 ax=fig.add_subplot(1,2,n+1,projection='3d')
 col=Poly3DCollection(m.triangles,linewidths=0,shade=True,facecolors='#e8a13b')
 ax.add_collection3d(col)
 ax.set_xlim(-52,52);ax.set_ylim(-52,52);ax.set_zlim(0,80);ax.set_box_aspect((104,104,80));ax.view_init(elev,azim);ax.set_axis_off();ax.set_title(title,fontsize=13)
fig.suptitle('M10 BULKHEAD WRENCH  |  100 x 28 x 76 mm',fontsize=18)
fig.text(.5,.05,'Original mating geometry retained  /  OD 28 mm reinforced sleeve  /  16 mm thick handle',ha='center',fontsize=11)
fig.tight_layout();fig.savefig(p/'bulkhead_wrench_preview.png',dpi=170)
print(json.dumps(r,indent=2))
