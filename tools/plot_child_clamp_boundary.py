"""Draw the actual clamp study's frame supports and axial load paths."""
from pathlib import Path
import json
import numpy as np
import trimesh
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/"parts/child/exterior/printed/child_wte4_suspension_clamp"
d=json.loads((PART/"_work/analysis/interface.json").read_text())
s=json.loads((PART/"_work/analysis/study_mount.json").read_text())
m=trimesh.load(PART/"child_wte4_suspension_clamp_half.stl",force="mesh")
fig=plt.figure(figsize=(11,7),facecolor="#f6f8f8")
ax=fig.add_subplot(projection="3d",facecolor="#f6f8f8",computed_zorder=False)
ax.add_collection3d(Poly3DCollection(m.triangles,facecolors="#8dc7b6",edgecolor="none",alpha=0.60,zorder=1))
fix=[]
for p in s["regions"]:
    if not p.startswith("frame_hole_"):continue
    r=s["regions"][p]
    fix.append([r["centre"][0],d["mount_y"],r["centre"][2]])
fix=np.array(fix)
ax.scatter(*fix.T,color="#c43842",s=110,edgecolors="white",label="FOUR M3 frame-hole supports (xyz fixed)",depthshade=False,zorder=5)
pts=[]
for i in range(6):
    c=np.array(s["regions"][f"rubber_contact_{i}"]["centre"][:2])
    c=c/np.linalg.norm(c)*d["inner_r"]
    pts.append([*c,16])
pts=np.array(pts)
ax.quiver(*pts.T,np.zeros(6),np.zeros(6),-np.ones(6)*20,color="#315aaf",arrow_length_ratio=.22,linewidth=2,label="Axial vessel force: total 78.45 N",zorder=4)
for i,p in enumerate(pts):
    f=np.array(s["cases"][3]["loads"][4+i]["force"])
    f[2]=0
    ax.quiver(*p,*(f/np.linalg.norm(f)*14),color="#df9739",arrow_length_ratio=.2,linewidth=1.3,zorder=3)
ax.set(xlim=(-105,105),ylim=(-100,8),zlim=(-8,45),xlabel="X (mm)",ylabel="Y (mm)",zlabel="Z / build axis (mm)")
ax.set_box_aspect([210,108,53]);ax.view_init(elev=29,azim=-115)
ax.legend(loc="upper right",fontsize=9)
fig.suptitle("WTE4 PETG clamp: force enters via rubber, reaction leaves via frame holes",fontsize=13,x=.52,y=.98)
fig.text(.035,.06,"4 kg total / 3 clamps / worst share 50% / 4g equivalent\nOrange: provisional radial contact pressure; M3 preload 150 N each\nRigid mating frame and bolt shafts; rubber friction and creep require physical testing.",fontsize=10,color="#34434b")
fig.subplots_adjust(top=.92,bottom=.16,left=.03,right=.99)
out=PART/"_work/images/boundary_conditions.png"
fig.savefig(out,dpi=180)
print(out)
