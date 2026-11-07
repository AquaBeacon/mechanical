"""Render actual candidate meshes, without opening a CAD GUI."""
from pathlib import Path
import sys
import numpy as np
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def main():
    run=Path(sys.argv[1]);root=Path(__file__).resolve().parents[1]
    out=root/'assemblies/parent_hand_service/_work/images/retrofit_parts_candidate.png'
    names=['main_service_frame','antenna_service_shelf','power_adapter','gnss_fixed_column_0','gnss_fixed_column_1','gnss_fixed_column_2','gnss_sony_shared_column','sony_fixed_column_0','sony_fixed_column_1','sony_fixed_column_3']+['cradle_floor_foot_'+str(i) for i in range(4)]
    meshes={n:trimesh.load_mesh(run/(n+'.stl')) for n in names}
    plt.rcParams['font.family']='Yu Gothic'
    fig=plt.figure(figsize=(15,7));fig.patch.set_facecolor('#f4f6f8')
    for i,angles in enumerate([(25,-55),(65,-105)]):
        ax=fig.add_subplot(1,2,i+1,projection='3d',proj_type='ortho')
        for name,m in meshes.items():
            color='#dca64b' if name in {'main_service_frame','antenna_service_shelf'} else '#49a18a' if name=='power_adapter' else '#8484b9'
            pc=Poly3DCollection(m.triangles,facecolor=color,edgecolor='#38404a',linewidth=.035,alpha=1)
            ax.add_collection3d(pc)
        ax.set(xlim=(0,210),ylim=(0,230),zlim=(0,100),xlabel='X [mm]',ylabel='Y [mm]',zlabel='Z [mm]')
        ax.set_box_aspect((210,230,100));ax.view_init(*angles)
        ax.set_title('一体枠・電源アダプタ・固定柱の実形状' if i==0 else '上方からの確認',fontsize=12)
    fig.suptitle('親機内装：改良部品の実形状（実物嵌合確認前）',fontsize=17)
    fig.text(.08,.035,'黄：MAIN＋アンテナ枠　緑：電源基板アダプタ　紫：固定柱・床側受け\n基板・床板・容器を非表示。検証の範囲は retrofit_report.md を参照。',fontsize=11)
    fig.subplots_adjust(top=.92,bottom=.13,left=.02,right=.98,wspace=.04)
    fig.savefig(out,dpi=150);plt.close(fig)
    print(out)
if __name__=='__main__':main()
