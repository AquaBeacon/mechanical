"""Plot CalculiX stress with installed topopt's parser and von Mises function.

Display only: the printed PETG strength judge remains anisotropic. Surface
triangle colors average its three corner values; no new FEA is implemented.
"""
from pathlib import Path
import argparse
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from topopt import ccx
from topopt.cli.ccx import mesh_context
from topopt.hex8 import von_mises

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/"parts/child/exterior/printed/child_wte4_suspension_clamp"
parser=argparse.ArgumentParser()
parser.add_argument("mesh_mm",type=float,nargs="?",default=4.0)
parser.add_argument("--solver-suffix",default="")
parser.add_argument("--directory",default="mount_ccx")
args=parser.parse_args()
work=PART/"_work/analysis"/args.directory
h=args.mesh_mm
tag=f"child_wte4_suspension_clamp_half_h{h:.2f}"
solver_tag=tag+"_"+args.solver_suffix if args.solver_suffix else tag
m=mesh_context(str(work/(tag+"_mesh.inp")))
r=ccx.parse_frd(str(work/(solver_tag+".frd")))
tri=np.array([[m["xyz"][m["index"][int(n)]] for n in f] for f in m["faces"]])
fig=plt.figure(figsize=(12,6))
cases=[(2,"Preload + static 1g"),(3,"Preload + axial handling 4g")]
norm=Normalize(0,12)
for j,(step,title) in enumerate(cases):
    stress=r["steps"][step]["stress"]
    ids=list(stress)
    vm=dict(zip(ids,von_mises(np.array([stress[n] for n in ids]))))
    colors=np.array([np.mean([vm[int(n)] for n in f]) for f in m["faces"]])
    ax=fig.add_subplot(1,2,j+1,projection="3d")
    ax.add_collection3d(Poly3DCollection(tri,facecolors=plt.cm.turbo(norm(colors)),edgecolor="none"))
    ax.set(xlim=(-100,100),ylim=(-90,0),zlim=(0,32),xlabel="X (mm)",ylabel="Y (mm)",zlabel="Z (mm)")
    ax.set_box_aspect((200,90,45))
    ax.view_init(elev=40,azim=-62)
    ax.set_title(title)
fig.suptitle(f"PETG clamp / {h:g} mm mesh / provisional elastic analysis\nSupported through four frame M3 holes; bolt preload 150 N each")
fig.subplots_adjust(left=0.02,right=0.86,bottom=0.16,top=0.80,wspace=0.05)
cax=fig.add_axes([0.90,0.25,0.018,0.46])
fig.colorbar(plt.cm.ScalarMappable(norm=norm,cmap="turbo"),cax=cax,label="von Mises stress (MPa), color display only")
fig.text(0.04,0.035,"No rubber contact / creep simulation. See STRENGTH.md for mesh convergence and anisotropic safety factors.",fontsize=10)
out=PART/"_work/images/stress_preview.png"
fig.savefig(out,dpi=160,bbox_inches="tight")
(PART/"_work/analysis/stress_plot_source.json").write_text(json.dumps(dict(mesh_mm=h,frd=str(work/(solver_tag+".frd")),
        steps=[3,4],display="Average of nodal von Mises stress at triangle corners. Strength uses anisotropic maximum-stress rule."),indent=2)+"\n",encoding="utf-8")
print(out)
