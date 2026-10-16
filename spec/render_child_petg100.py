"""Render the actual CAD STL candidates, not an imagined result."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import trimesh
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assemblies/child_petg100_design'
plt.rcParams.update({'font.family':'Yu Gothic','axes.unicode_minus':False})
parts=[('child_core_frame','コア','#527a98'),('child_jaw_gate','ゲート','#42a995'),('child_cam_bridge','カメラ取付部','#de9a4b')]
def draw(ax,m,color,alpha=1):
    ax.add_collection3d(Poly3DCollection(m.triangles,facecolor=color,edgecolor='none',alpha=alpha,rasterized=True))
for scene in ['assembly','parts']:
    fig=plt.figure(figsize=(15,9),facecolor='#f5f7fa')
    if scene=='assembly':
        for i,az in enumerate([-60,125]):
            ax=fig.add_subplot(1,2,i+1,projection='3d')
            for n,label,c in parts:draw(ax,trimesh.load(OUT/n/'manufactured.stl'),c)
            for n,c in [('pressure_vessel','#9abfe2'),('cameras','#edcc77'),('light_vertical','#b8a536'),('td04a','#9d64b9')]:
                draw(ax,trimesh.load(OUT/'scene'/f'{n}.stl'),c,.25)
            ax.set(xlim=(-140,140),ylim=(-140,160),zlim=(-40,300),xlabel='X mm',ylabel='Y mm',zlabel='Z mm')
            ax.set_box_aspect((280,300,340));ax.view_init(22,az)
            ax.set_title('前方から' if i==0 else '後方から')
    else:
        for i,(n,label,c) in enumerate(parts):
            ax=fig.add_subplot(1,3,i+1,projection='3d');m=trimesh.load(OUT/n/'manufactured.stl');draw(ax,m,c)
            mid=m.bounds.mean(axis=0);radius=max(m.extents)/2+10
            ax.set(xlim=(mid[0]-radius,mid[0]+radius),ylim=(mid[1]-radius,mid[1]+radius),zlim=(mid[2]-radius,mid[2]+radius))
            ax.set_box_aspect((1,1,1));ax.view_init(20,-60)
            ax.set_title(f'{label}\nPETG100% 換算 {m.volume*1.27e-6:.2f} kg')
    fig.suptitle('PETG 100%：補強した実形状の検証用CAD（合格未確認）',fontsize=19)
    fig.text(.04,.04,'CADから出力したSTLを表示。半透明は搭載機器の予約空間。ねじ・EVA・周辺ガードはこの図では省略。',fontsize=11)
    fig.savefig(OUT/f'{scene}_candidate.png',dpi=130);plt.close(fig)
print('Rendered actual CAD candidates.')
