"""Assembly preview; source is saved meshes and placement, not an invented shape."""
from pathlib import Path
import sys,json,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from prepare_child_horizontal_plate_frame import matrix,load_world
p=json.loads((ROOT/'assemblies/parent_exterior/placement.json').read_text(encoding='utf-8'))
for r in p['items']:r.setdefault('file',Path(r['part']).name)
w=load_world(p);rows={r['label']:r for r,m in w};meshes={r['label']:m for r,m in w};inv=np.linalg.inv(matrix(rows['camera_qr_female']['ops']))
fig=plt.figure(figsize=(10,8));ax=fig.add_subplot(111,projection='3d')
for label,col,alpha in [('camera_qr_female','#d88d38',.8),('camera_mount','#718496',.25),('camera_qr_axial_0_spacer','#c64a32',.95),('camera_qr_axial_1_spacer','#c64a32',.95),('camera_qr_axial_0_knob','#12856e',1),('camera_qr_axial_1_knob','#12856e',1),('camera_qr_axial_0_knob_cap','#a9d8cc',1),('camera_qr_axial_1_knob_cap','#a9d8cc',1)]:
 m=meshes[label].copy();m.apply_transform(inv)
 poly=Poly3DCollection(m.triangles,facecolor=col,edgecolor='none',alpha=alpha);ax.add_collection3d(poly)
ax.set(xlim=(-50,80),ylim=(-75,75),zlim=(-12,95),xlabel='Joint X (mm)',ylabel='Joint Y (mm)',zlabel='Joint Z (mm)')
ax.set_box_aspect((130,150,107));ax.view_init(elev=24,azim=-58);ax.set_title('Camera hand-release fixture: seated geometry')
fig.tight_layout();out=ROOT/'assemblies/parent_exterior/_work/images/camera_clamp_right5_20261029_assembly.png';fig.savefig(out,dpi=130);plt.close(fig);print(out)
