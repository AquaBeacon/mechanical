"""Render named CAD exclusion solids in assembly coordinates, no solver."""
from pathlib import Path
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch, FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import trimesh

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT/'assemblies/child_frame2_assembly/topopt_review_20260910_v2'
SINGLE=OUT.name=='child_single_camera_topopt'
plt.rcParams.update({'font.family':'Yu Gothic','font.size':11,'axes.unicode_minus':False})
entries=[('pressure_vessel','#3c91d4',.19,'1 耐圧容器（中も埋めた除外体積）'),
 ('cameras','#ef8227',.65,'2 カメラ＋防水ケース ×2'),
 ('light_forward','#e2b32b',.36,'3 前向きライト Ø40×100【仮・奥行超過】'),
 ('light_vertical','#b9890d',.25,'4 縦向きライト候補＋取付座【仮】'),
 ('td04a','#a448bb',.8,'5 TD04A Ø26.4×55【仮】'),
 ('td04a_socket','#9465af',.17,'   TD04Aソケット占有空間'),
 ('cables','#e43c4a',.9,'6 配線経路 Ø6＋周囲1 mm【仮】'),
 ('hand_clearance','#18b5c5',.26,'7 指の空間＋背面からの進入空間')]
if SINGLE:
    entries=[e for e in entries if e[0]!='light_forward']
    entries=[(n,c,a,('2 中央カメラ＋防水ケース ×1' if n=='cameras' else '4 縦向きライト ×1＋取付座【仮寸法】' if n=='light_vertical' else l)) for n,c,a,l in entries]
meshes={name:trimesh.load(OUT/'scene'/f'{name}.stl',force='mesh') for name,_,_,_ in entries}
preserved={name:trimesh.load(OUT/name/'inputs/preserve.stl',force='mesh') for name in ['child_core_frame','child_jaw_gate','child_cam_bridge']}
def plotmesh(ax,mesh,color,alpha):
    ax.add_collection3d(Poly3DCollection(mesh.triangles,facecolors=color,edgecolor='none',alpha=alpha,rasterized=True))
def scene(ax):
    for name,mesh in preserved.items():plotmesh(ax,mesh,'#4c9869',.4)
    for name,color,alpha,label in entries:plotmesh(ax,meshes[name],color,alpha)
    ax.set(xlim=(-145,145),ylim=(-155,190),zlim=(-65,300),xlabel='X 左右 [mm]',ylabel='Y 前方 [mm]',zlabel='Z 上方 [mm]')
    ax.set_box_aspect((290,345,365));ax.tick_params(labelsize=9)
    labels=[([0,0,185],'1 容器','#2466a2'),([0 if SINGLE else 90,129 if SINGLE else 120,165],'2 カメラ','#ac4d00'),([101,-75,150],'4 縦向きライト','#805d00'),([0,-85,285],'5 TD04A','#783087'),([34,-79,100],'6 配線','#c32030'),([0,-140,130],'7 手の進入口','#00899a')]
    if not SINGLE:labels.append(([0,178,15],'3 前向き候補','#9c7100'))
    for xyz,label,color in labels:
        ax.text(*xyz,label,color=color,fontsize=10,bbox={'facecolor':'white','edgecolor':'none','alpha':.8,'pad':1},zorder=100)
for view,azim,jp in [('front',55,'前方から'),('rear',-115,'背面から')]:
    fig=plt.figure(figsize=(14,10),facecolor='#f6f8fb')
    ax=fig.add_axes([.01,.10,.70,.81],projection='3d');scene(ax);ax.view_init(elev=24,azim=azim)
    fig.text(.04,.95,f'子機外装：機器と動作の除外領域  /  {jp}',fontsize=21,weight='bold')
    legend=[Patch(facecolor='#4c9869',label='緑：保持する機能部（最適化前）')]+[Patch(facecolor=c,label=l) for n,c,a,l in entries]
    fig.legend(handles=legend,loc='center left',bbox_to_anchor=(.70,.61),frameon=False,fontsize=10,labelspacing=1.6)
    note='中央カメラ1台＋右側縦向きライト1灯。\nカメラを前へ9mm移動して柱を回避。\n前端137／背面−110：奥行247mm。\n上限250mm以内。\n\nライトØ40×100、配線Ø6＋余裕1mm。\n機器寸法は引き続き仮値です。' if SINGLE else 'ライトは向きの候補を併記。\n全てを同時搭載する意味ではありません。\n\n前向き100mmでは機体奥行288mm。\n上限250mmに対して38mm超過。\n位置・向きの見直しが必要です。'
    fig.text(.72,.30,note,va='top',fontsize=10,color='#8d4716',linespacing=1.7)
    fig.text(.04,.055,'これらの内部へフレーム材を置かない設定。設計空間の外にある機器も、配置確認のため全体を表示。',fontsize=11)
    fig.savefig(OUT/f'exclusions_{view}.png',dpi=150);plt.close(fig)

class Arrow3D(FancyArrowPatch):
    def __init__(self,a,b,**kw):super().__init__((0,0),(0,0),**kw);self.xyz=np.array([a,b])
    def draw(self,renderer):
        x,y,z=proj3d.proj_transform(*self.xyz.T,self.axes.get_proj());self.set_positions((x[0],y[0]),(x[1],y[1]));super().draw(renderer)
    def do_3d_projection(self,renderer=None):return -1e9

fig=plt.figure(figsize=(14,9),facecolor='#f6f8fb')
ax=fig.add_axes([.03,.12,.62,.77],projection='3d',computed_zorder=False)
core=preserved['child_core_frame']
# Clip all context meshes to a common local window for a readable handle detail.
def cropped(mesh):
    out=mesh.copy()
    for origin,normal in [([-55,0,0],[1,0,0]),([55,0,0],[-1,0,0]),([0,-152,0],[0,1,0]),([0,-62,0],[0,-1,0]),([0,0,85],[0,0,1]),([0,0,212],[0,0,-1])]:
        vertices,faces,_=trimesh.intersections.slice_faces_plane(out.vertices,out.faces,normal,origin)
        out=trimesh.Trimesh(vertices=vertices,faces=faces,process=False)
    return out
plotmesh(ax,cropped(core),'#4c9869',.65)
plotmesh(ax,cropped(meshes['hand_clearance']),'#18b5c5',.22)
plotmesh(ax,cropped(meshes['cables']),'#e43c4a',.8)
ax.set(xlim=(-60,60),ylim=(-155,-60),zlim=(85,220),xlabel='X [mm]',ylabel='Y [mm]',zlabel='Z [mm]');ax.set_box_aspect((120,95,135));ax.view_init(elev=22,azim=-115)
ax.add_artist(Arrow3D([0,-95,146],[0,-95,198],arrowstyle='-|>',mutation_scale=24,lw=3,color='#d62b38',zorder=100))
ax.text(0,-95,204,'+200 N / +Z',color='#b31c25',weight='bold',zorder=110,bbox={'facecolor':'white','edgecolor':'none','alpha':.9})
fig.text(.04,.95,'持ち手：保持する握り部・指空間・持上げ荷重',fontsize=21,weight='bold')
fig.text(.68,.80,'緑：持ち手を残す領域\n水色：指＋手の進入空間\n赤い管：配線の予約経路\n赤い矢印：上向き200 N',va='top',fontsize=14,linespacing=1.9)
fig.text(.68,.48,'追加ケース L6（仮条件）\n6 kg × 3g 相当を切上げて200 N。\n握り下面に合計荷重を分布適用。\n耐圧容器の上下保持面を固定した\n等価的な持上げ評価です。\n\n指の入口：幅52 × 高さ30 mm。\n配線は左右へ逃がす候補経路。\n曲げ半径・手袋での操作性は未確定。',va='top',fontsize=11,linespacing=1.8)
fig.text(.04,.055,'最適化前のsetup。配線用の通路を保持部に追加したため、最終形状の強度評価はこれからです。',fontsize=11)
fig.savefig(OUT/'handle_detail.png',dpi=150);plt.close(fig)
print('Rendered named exclusion scene and handle detail.',flush=True)
