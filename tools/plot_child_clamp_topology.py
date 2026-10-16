"""Draw measured CAD sections and mass comparison, using existing STL geometry."""
from pathlib import Path
import numpy as np
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import argparse

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp'
plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':11})


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--smooth',action='store_true',help='show the directly smoothed canonical variant')
    parser.add_argument('--stl',type=Path,help='explicit finished trial mesh')
    parser.add_argument('--density-g-cm3',type=float,default=1.27)
    parser.add_argument('--image-prefix',default='smooth_topology')
    args=parser.parse_args()
    baseline=trimesh.load(PART/'child_wte4_suspension_clamp_half.stl',force='mesh')
    source=PART/'child_wte4_suspension_clamp_smooth.stl' if args.smooth else PART/'_work/analysis/topology_petg/candidate.stl'
    source=args.stl or source
    candidate=trimesh.load(source,force='mesh')
    label='Directly smoothed topology' if args.smooth else 'Topology-guided CAD candidate'
    fig, axes=plt.subplots(1,2,figsize=(12,5),facecolor='#f7f7f3')
    for ax, mesh, name, color in zip(axes,[baseline,candidate],['Initial solid design',label],['#9aa6ad','#2c746a']):
        section=mesh.section(plane_origin=[0,0,16],plane_normal=[0,0,1])
        loops=sorted(section.discrete,key=lambda p:abs(np.sum(p[:-1,0]*p[1:,1]-p[1:,0]*p[:-1,1])),reverse=True)
        for i,p in enumerate(loops):
            ax.fill(p[:,0],p[:,1],facecolor=color if i==0 else '#f7f7f3',edgecolor='#29403e',lw=0.7)
        a=np.linspace(np.pi,2*np.pi,300)
        ax.plot(57.15*np.cos(a),57.15*np.sin(a),color='#be914e',lw=1.3,ls='--')
        ax.set(title=f'{name}\n{mesh.volume*args.density_g_cm3/1000:.1f} g per half (PETG solid)',xlabel='X (mm)',ylabel='Y (mm)')
        ax.set_aspect('equal'); ax.set_xlim(-102,102); ax.set_ylim(-98,10)
        ax.set_facecolor('#f7f7f3'); ax.spines[['top','right']].set_visible(False)
    axes[1].annotate('Rubber seat: 1.2 mm radial space',xy=(0,-58.35),xytext=(-72,-95),arrowprops={'arrowstyle':'->','color':'#29403e'},fontsize=9)
    axes[1].annotate('M3 mounting: 2 x 2 holes\nunchanged 36 x 16 mm pitch',xy=(0,-82),xytext=(17,-93),arrowprops={'arrowstyle':'->','color':'#29403e'},fontsize=9)
    saving=100*(1-candidate.volume/baseline.volume)
    fig.suptitle(f'WTE4 / M3 / PETG   |   {saving:.1f}% mass reduction\nCandidate requires strength and mesh-convergence acceptance',fontsize=14,color='#183d38')
    fig.tight_layout(rect=[0,0,1,0.86])
    filename=args.image_prefix+'_comparison.png' if args.smooth else 'topology_candidate_comparison.png'
    fig.savefig(PART/'_work/images'/filename,dpi=180)
    if args.smooth:
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection
        outer=next(s for s in candidate.split() if s.volume>0)
        fig=plt.figure(figsize=(11,6),facecolor='#f7f7f3')
        ax=fig.add_subplot(111,projection='3d')
        light=np.array([-.3,-.5,1.]); light/=np.linalg.norm(light)
        shade=np.clip(0.52+0.44*(outer.face_normals@light),0.15,1.)
        colors=np.column_stack([shade*.22,shade*.64,shade*.58,np.ones(len(shade))])
        ax.add_collection3d(Poly3DCollection(outer.triangles,facecolors=colors,edgecolors='none',linewidths=0))
        ax.set_xlim(-98,98); ax.set_ylim(-87,2); ax.set_zlim(0,32)
        ax.set_box_aspect([196,89,32]); ax.view_init(elev=47,azim=-68)
        ax.set_axis_off(); ax.set_facecolor('#f7f7f3')
        fig.suptitle(f'Directly smoothed topology / exact M3 interfaces\nPETG {candidate.volume*args.density_g_cm3/1000:.1f} g per half | suspension strength not qualified',color='#183d38',fontsize=14)
        fig.tight_layout()
        fig.savefig(PART/'_work/images'/(args.image_prefix+'_3d.png'),dpi=180)


if __name__=='__main__':
    main()
