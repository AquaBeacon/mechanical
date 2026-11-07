"""Before/after print-pose meshes, without opening a CAD application."""
from pathlib import Path
import numpy as np,trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
R=Path(__file__).resolve().parents[1];A=R/'assemblies/parent_hand_service'
def main():
    plt.rcParams['font.family']='Yu Gothic'
    fig,axes=plt.subplots(2,1,figsize=(14,5))
    for i,(title,file) in enumerate([
        ('変更前：格子の下面がベッドから3.7 mm浮く',A/'_work/analysis/frame_spacers_20261024/history/main_service_frame.stl'),
        ('変更後：格子の下面を脚と同じ印刷面へ',R/'parts/parent/interior/printed/parent_hand_service/main_service_frame.stl')]):
        m=trimesh.load_mesh(file);m.apply_translation([0,0,-33.4])
        ax=axes[i]
        shade=.55+.45*np.maximum(0,m.face_normals@np.array([-.25,-.4,.8]))
        colors=np.column_stack([shade*.91,shade*.65,shade*.28,np.ones(len(shade))])
        order=np.argsort(-m.triangles_center[:,1])
        ax.add_collection(PolyCollection(m.triangles[order][:,:,[0,2]],facecolors=colors[order],linewidths=0))
        ax.axhline(0,color='#59738a',linewidth=1)
        ax.set(xlim=(2,145),ylim=(-.5,19),ylabel='ベッドからの高さ [mm]',aspect='equal',title=title)
        ax.set_xticks([20,60,100,140]);ax.set_yticks([0,3.7,10,17.4]);ax.grid(alpha=.15)
    fig.tight_layout();out=A/'_work/images/frame_spacers_comparison.png';fig.savefig(out,dpi=160);plt.close(fig);print(out)
if __name__=='__main__':main()
