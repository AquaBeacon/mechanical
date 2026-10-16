"""Compare measured STL side-rail sections before and after the rim revision."""
from pathlib import Path
import json
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_exterior_structural_frame'
BASE=PART/'_work/analysis/frame_a_compact_grip'
CASE=PART/'_work/analysis/frame_a_rim_thickness'
OUT=ROOT/'assemblies/child_exterior_structure/_work/images'


def main():
    archive=BASE/'input_history/before_rim_revision'/PART.relative_to(ROOT)
    dims=json.loads((PART/'spec/design_parameters.json').read_text())
    old=json.loads((BASE/'final_geometry_checks.json').read_text())['parts']
    new=json.loads((CASE/'final_geometry_checks.json').read_text())['parts']
    def mass(rows):return sum(rows[n]['mass_g_provisional'] for n in ['lower_minus','lower_plus','upper_minus','upper_plus'])+6*rows['splice']['mass_g_provisional']
    previous,current=mass(old),mass(new)
    plt.rcParams['font.family']='Yu Gothic'
    fig,axes=plt.subplots(1,2,figsize=(11,6),facecolor='#f7f9fc')
    for ax,p,title,color in [(axes[0],archive/'child_exterior_structural_frame_full.stl','変更前：底板12 mm・縦壁4 mm','#7f96aa'),
                              (axes[1],PART/'child_exterior_structural_frame_full.stl',f"変更後：底板{dims['rim_base_thickness']:g} mm・縦壁{dims['rail_wall']:g} mm",'#3d87b9')]:
        m=trimesh.load(p,force='mesh')
        section=m.section(plane_origin=[0,140,0],plane_normal=[0,1,0])
        assert section is not None
        for line in section.discrete:
            ax.fill(line[:,0],line[:,2],color=color,edgecolor=color,linewidth=.7)
        ax.set_aspect('equal');ax.set_xlim(146,172);ax.set_ylim(-2,48)
        ax.set_title(title,pad=15);ax.set_xlabel('外周の幅方向 / mm');ax.set_ylabel('A内面からの奥行き / mm')
        ax.set_xticks([148,152,158,166,170]);ax.set_yticks([0,4,6,8,12,24,36,45])
        ax.grid(alpha=.2);ax.set_axisbelow(True)
        ax.spines[['top','right']].set_visible(False)
    fig.suptitle('フレームA：側面外枠の実STL断面（機体Z=140 mm）',fontsize=15,y=.98)
    fig.text(.5,.09,f'片側A＋接合板6個：{previous/1000:.2f} → {current/1000:.2f} kg  /  {(1-current/previous)*100:.1f}%軽量化',ha='center',fontsize=13,color='#226b50')
    fig.text(.5,.035,'外形・接地範囲・持ち手上辺・ねじ座を保持  ·  CAD理論質量  ·  強度は試作評価',ha='center',fontsize=10,color='#526273')
    fig.subplots_adjust(top=.86,bottom=.23,wspace=.45)
    OUT.mkdir(parents=True,exist_ok=True);fig.savefig(OUT/'frame_a_rim_revision.png',dpi=160)
    print(OUT/'frame_a_rim_revision.png')


if __name__=='__main__':main()
