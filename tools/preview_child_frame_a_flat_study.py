"""Show the exact uniform-plate preparation and its standing load setup."""
from pathlib import Path
import json,shutil
import numpy as np
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.patches import Rectangle,Patch
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_exterior_structural_frame'
CASE=PART/'_work/analysis/frame_a_flat_thickness'
OUT=PART/'_work/images'

def main():
    read=lambda p:json.loads(p.read_text(encoding='utf-8'))
    check=read(CASE/'preparation_checks.json');t=check['plate_thickness_mm']
    d=read(PART/'spec/design_parameters.json')
    domain=trimesh.load(CASE/'domain.stl',force='mesh')
    preserve=trimesh.load(CASE/'preserve.stl',force='mesh')
    plt.rcParams.update({'font.family':'Yu Gothic','font.size':10})
    fig=plt.figure(figsize=(12.5,8),facecolor='#f7f9fc')
    front=fig.add_axes([.06,.19,.40,.68]);iso=fig.add_axes([.47,.19,.48,.68],projection='3d')
    for m,col in [(domain,'#c4ced7'),(preserve,'#40996c')]:
        tri=m.triangles[:,:,:2];a=tri[:,1]-tri[:,0];b=tri[:,2]-tri[:,0]
        area=np.abs(a[:,0]*b[:,1]-a[:,1]*b[:,0])
        front.add_collection(PolyCollection(tri[area>1e-7],facecolors=col,edgecolors='none'))
    front.set_aspect('equal');front.set_xlim(-188,188);front.set_ylim(-164,302)
    front.set_xlabel('機体Y / mm');front.set_ylabel('機体Z / mm')
    front.spines[['top','right']].set_visible(False)
    front.add_patch(Rectangle((-135,-82),270,100,fill=False,edgecolor='#248169',linestyle='--',linewidth=1.3))
    front.text(0,-37,'手の通路\n270 × 100 mm',ha='center',va='center',color='#1c7155',fontsize=12)
    front.text(0,230,'指入れ100 × 40',ha='center',va='center',fontsize=9)
    for points,col in [(d['clamp_holes_yz'],'#e08b2c'),(d['c_holes_yz'],'#8955b4')]:
        a=np.array(points);front.scatter(a[:,0],a[:,1],s=25,facecolors='none',edgecolors=col,zorder=5)
    for x in [-18,18]:
        front.annotate('',xy=(x,134),xytext=(x,157),arrowprops=dict(arrowstyle='-|>',color='#ba4b48',lw=1.6))
    front.text(0,110,'直立：49.03 N／片側\n偏り：98.07 N／片側\n＋フレーム自重',ha='center',color='#9d4142',fontsize=9,bbox=dict(facecolor='white',alpha=.8,edgecolor='none'))
    front.plot([-164,164],[-132,-132],color='#347cad',lw=3)
    front.scatter([-140,140],[-132,-132],s=16,color='#347cad')
    front.text(0,-155,'床：鉛直拘束＋剛体移動防止の最小拘束',ha='center',fontsize=8,color='#2d6e98')
    front.set_title('正面：保持領域と荷重位置',pad=12)
    for m,col,alpha in [(domain,'#b6c3cf',.24),(preserve,'#40996c',.98)]:
        tri=m.triangles[:,:,[0,2,1]]
        pc=Poly3DCollection(tri,facecolors=col,edgecolors='none',alpha=alpha,zsort='average')
        iso.add_collection3d(pc)
    iso.set_xlim(-180,180);iso.set_ylim(-38,45);iso.set_zlim(-150,290)
    iso.set_box_aspect([340,70,408]);iso.view_init(elev=18,azim=-62)
    iso.set_xlabel('機体Y',labelpad=5);iso.set_ylabel('板厚方向',labelpad=6);iso.set_zlabel('機体Z',labelpad=5)
    iso.set_yticks([0,t]);iso.set_yticklabels(['0',f'{t:g} mm'])
    iso.set_title(f'全体を厚み{t:g} mmの平板にした準備モデル',pad=14)
    section=fig.add_axes([.79,.61,.17,.19],facecolor='#f7f9fc')
    path=domain.section(plane_origin=[0,140,0],plane_normal=[0,1,0])
    for line in path.discrete:section.fill(line[:,0],line[:,2],color='#40996c')
    section.set_xlim(146,172);section.set_ylim(-2,12);section.set_aspect('equal')
    section.set_xticks([148,170]);section.set_yticks([0,t]);section.spines[['top','right']].set_visible(False)
    section.set_title('側面外枠の実断面',fontsize=9);section.tick_params(labelsize=8)
    fig.suptitle('フレームA：トポロジー最適化の準備',fontsize=17,y=.98)
    fig.text(.5,.922,f'外形340 × 408 mm · 厚み一定{t:g} mm（暫定）· 最適化・強度解析は未実行',ha='center',fontsize=11,color='#536577')
    fig.legend(handles=[Patch(color='#40996c',label='保持：外周・接地・持ち手・M3座'),Patch(color='#c4ced7',label='探索：内部の設計領域')],loc='lower center',bbox_to_anchor=(.5,.09),ncol=2,frameon=False)
    fig.text(.5,.045,'解析準備用モデル。印刷用ではありません。直立の転倒・滑りと分割接合は後段で確認します。',ha='center',fontsize=9,color='#536577')
    OUT.mkdir(parents=True,exist_ok=True);image=OUT/'frame_a_flat_preparation.png'
    fig.savefig(image,dpi=145)
    dst=ROOT/'assemblies/child_exterior_structure/_work/images'/image.name;shutil.copy2(image,dst)
    # Exact CSG partitions avoid overlapping coloured surfaces in OpenSCAD.
    (CASE/'frame_a_flat_view.scad').write_text('// Exploration-only; generated colour view.\ncolor([0.7,0.76,0.82,0.65]) difference() { import("domain.stl"); import("preserve.stl"); }\ncolor([0.18,0.65,0.40,1]) import("preserve.stl");\n',encoding='utf-8')
    print(dst)

if __name__=='__main__':main()
