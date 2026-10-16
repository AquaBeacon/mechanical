"""Render measured CAD projections of frame A; does not change mesh geometry."""
from pathlib import Path
import json
import numpy as np
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.patches import Rectangle

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_exterior_structural_frame'
OUT=ROOT/'assemblies/child_exterior_structure/_work/images'


def draw(ax, name, color, zorder=1, translate=(0,0), angle=0):
    mesh=trimesh.load(PART/f'child_exterior_structural_frame_{name}.stl',force='mesh')
    tri=mesh.triangles[:,:,:2]
    # All actual triangles, no simplified or invented outline. Edge-on faces
    # have zero projected area; filtering these only accelerates the preview.
    a=tri[:,1]-tri[:,0]; b=tri[:,2]-tri[:,0]
    area=np.abs(a[:,0]*b[:,1]-a[:,1]*b[:,0])
    theta=np.deg2rad(angle)
    tri=tri@np.array([[np.cos(theta),np.sin(theta)],[-np.sin(theta),np.cos(theta)]])+np.array(translate)
    ax.add_collection(PolyCollection(tri[area>1e-7],facecolors=color,edgecolors='none',zorder=zorder))


def main():
    d=json.loads((PART/'spec/design_parameters.json').read_text(encoding='utf-8'))
    plt.rcParams['font.family']='Yu Gothic'
    plt.rcParams['font.size']=10
    fig,axes=plt.subplots(1,2,figsize=(12,8),facecolor='#f7f9fc')
    draw(axes[0],'full','#3d87b9')
    for n,c in [('lower_minus','#3d87b9'),('lower_plus','#4b9ead'),
                ('upper_minus','#6b92c6'),('upper_plus','#609b91')]: draw(axes[1],n,c)
    for ax in axes:
        ax.set_aspect('equal'); ax.set_xlim(-189,189); ax.set_ylim(-150,294)
        ax.set_facecolor('white'); ax.set_xlabel('機体 Y / mm'); ax.set_ylabel('機体 Z / mm')
        ax.spines[['top','right']].set_visible(False)
        ax.add_patch(Rectangle((-135,-82),270,100,fill=False,edgecolor='#188562',linestyle='--',linewidth=1.4,zorder=5))
        ax.text(0,-33,'手の通路\n270 × 100 mm',ha='center',va='center',color='#116c50',fontsize=13,zorder=6)
        ax.text(0,230,'指入れ\n100 × 40',ha='center',va='center',fontsize=9,color='#2b5368',zorder=6)
    for kind,color,label in [('clamp_holes_yz','#db761e','クランプ M3'),('c_holes_yz','#9851b0','C接続 M3')]:
        pts=np.array(d[kind]); axes[0].scatter(pts[:,0],pts[:,1],s=28,facecolors='none',edgecolors=color,linewidths=1.1,label=label,zorder=7)
    axes[0].legend(loc='lower center',bbox_to_anchor=(.5,-.17),ncol=2,frameon=False)
    axes[0].set_title('仕上げた一体A：外周・下部開口を保持',pad=14)
    axes[1].set_title('印刷用4分割と外側M3接合板',pad=14)
    axes[1].axvline(0,color='#536374',linestyle=':',lw=.8,zorder=4)
    axes[1].axhline(80,color='#536374',linestyle=':',lw=.8,zorder=4)
    for x,y,angle in [(0,y,0) for y in d['splice_centres_y']]+[(x,d['split_y'],90) for x in [-158,158]]:
        draw(axes[1],'splice','#929fa9',zorder=8,translate=(x,y),angle=angle)
    for x,y in d['joint_holes_yz']:
        axes[1].scatter([x],[y],s=9,facecolors='#e7ecf0',edgecolors='#455361',linewidths=.4,zorder=9)
    fig.suptitle('フレームA / 340 × 408 mm · 最大奥行き45 mm',fontsize=17,y=.985)
    fig.text(.5,.017,'CADの正面投影  ·  PETG試作  ·  分割接合・完成機の強度は未認定',ha='center',fontsize=10,color='#526273')
    fig.subplots_adjust(top=.9,bottom=.15,wspace=.24)
    OUT.mkdir(parents=True,exist_ok=True)
    fig.savefig(OUT/'frame_a_design.png',dpi=150)
    print(OUT/'frame_a_design.png')


if __name__=='__main__': main()
