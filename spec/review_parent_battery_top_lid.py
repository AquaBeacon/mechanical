"""Render actual meshes and slice the battery parts using the existing PETG profile."""
import json,shutil,sys,zipfile,hashlib
import numpy as np
import trimesh
from publish_parent_battery_top_lid import R,W,ASM,read,write,run
def render():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    result=read(W/'build_run.json')
    meshes={n:trimesh.load(row['stl'],force='mesh') for n,row in result['exports'].items()}
    fig=plt.figure(figsize=(13,6))
    for i,elev in enumerate([24,80],1):
        ax=fig.add_subplot(1,2,i,projection='3d')
        for n,m in meshes.items():
            m=m.copy()
            if n!='battery_base':m.apply_translation([0,0,45])
            color=np.array([.93,.65,.30] if n=='battery_base' else [.44,.74,.78])
            light=np.array([-.3,-.4,1.]);light/=np.linalg.norm(light)
            colors=color[None,:]*(.55+.45*np.clip(m.face_normals@light,0,1))[:,None]
            ax.add_collection3d(Poly3DCollection(m.triangles,facecolors=colors,edgecolor='none',alpha=1))
        ax.set(xlim=(-6,110),ylim=(-6,60),zlim=(0,58),xlabel='X (mm)',ylabel='Y (mm)',zlabel='Z (mm)')
        ax.set_box_aspect([116,66,58]);ax.view_init(elev=elev,azim=-65)
        ax.set_title('Straight-up removable lid / one M3 screw' if i==1 else 'Four locating pins / flat underside')
    fig.tight_layout();out=ASM/'_work/images/battery_top_lid.png';fig.savefig(out,dpi=150);plt.close(fig)
    print(out)
def slice_parts():
    S=W/'slicing';S.mkdir(exist_ok=True)
    old=ASM/'_work/analysis/retrofit_20261024/slicing'
    for n in ['machine','process','filament']:
        d=read(old/(n+'.json'))
        if n=='process':d.update(print_settings_id='Parent battery vertical lid',enable_support='1',support_threshold_angle='45',dont_support_bridges='0',enable_arc_fitting='0')
        write(S/(n+'.json'),d)
    records=[]
    for name in ['battery_base','parent_lipo_retainer_lid_slide']:
        folder=S/name;folder.mkdir(exist_ok=True)
        source=R/'parts/parent/interior/printed'/('parent_hand_service' if name=='battery_base' else 'parent_lipo_retainer')/(name+'.stl');m=trimesh.load(source,force='mesh');m.apply_translation(np.array([60,60,0])-m.bounds[0]);m.export(folder/'placed.stl')
        cmd=['C:/Program Files/Bambu Studio/bambu-studio.exe','--debug','2','--datadir',str(folder/'studio_data'),'--load-settings',str(S/'machine.json')+';'+str(S/'process.json'),'--load-filaments',str(S/'filament.json'),'--arrange','0','--orient','0','--slice','0','--export-3mf','review.3mf','--outputdir',str(folder),str(folder/'placed.stl')]
        run(cmd,'slice_'+name,timeout=240,cwd=folder)
        if name=='battery_base':
            # The inherited45deg lower pilot relief gets a tiny spurious support
            # interface; keep this accessible vertical screw bore empty.
            from slice_parent_retrofit import attach_blocker
            blocker=trimesh.creation.box(extents=[4,4,12]);blocker.apply_translation([50,5,23.5])
            target=source.parent/'battery_lid_pilot_support_blocker.stl'
            blocker.export(target,file_type='stl_ascii')
            blocker.apply_translation(np.array([60,60,0])-trimesh.load(source,force='mesh').bounds[0])
            attach_blocker(folder/'review.3mf',folder/'blocked.3mf',m,blocker)
            cmd[-1]=str(folder/'blocked.3mf')
            run(cmd,'slice_'+name+'_pilot_blocked',timeout=240,cwd=folder)
        result=read(folder/'result.json');assert result['return_code']==0
        with zipfile.ZipFile(folder/'review.3mf') as z:
            for p in z.namelist():
                if p.endswith('.gcode'):
                    with z.open(p) as src,(folder/'plate.gcode').open('wb') as dst:shutil.copyfileobj(src,dst)
                if p.endswith('.png') and 'plate_1' in p:(ASM/'_work/images'/('battery_top_'+name+'_'+p.split('/')[-1])).write_bytes(z.read(p))
        records.append(dict(part=name,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),result=result,profile='X1C PETG existing profile; support detection enabled45deg; bridges supported'))
    write(W/'slice_checks.json',records)
if __name__=='__main__':slice_parts() if '--slice' in sys.argv else render()
