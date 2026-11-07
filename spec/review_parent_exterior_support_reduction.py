"""Review enabled support detection, critical toolpaths and final print poses."""
from pathlib import Path
import json,subprocess,sys
import numpy as np
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from review_parent_exterior_slices import main as audit_saved,paths

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'assemblies/parent_exterior'
W=A/'_work/analysis/support_reduction'
PRIMARY={'parent_oneplate_frame':39.2,'parent_oneplate_td_support':15.8,'parent_oneplate_camera_stop':24.2}

def render_poses(poses):
    fig=plt.figure(figsize=(15,5))
    poses=sorted(poses,key=lambda p:list(PRIMARY).index(p[0]))
    for i,(stem,m) in enumerate(poses):
        ax=fig.add_subplot(1,3,i+1,projection='3d')
        shade=.55+.4*np.clip(m.face_normals@np.array([.3,-.5,.8]),0,1)
        colors=np.column_stack([shade*.15,shade*.62,shade*.75,np.ones(len(shade))])
        ax.add_collection3d(Poly3DCollection(m.triangles,facecolors=colors,linewidths=0))
        e=m.extents.copy()
        ax.set(xlim=(0,e[0]),ylim=(0,e[1]),zlim=(0,e[2]),xlabel='X / mm',ylabel='Y / mm',zlabel='build Z / mm')
        # Matplotlib normalises its input array in place.
        ax.set_box_aspect(e.copy());ax.view_init(elev=25,azim=-60)
        ax.set_title(stem.replace('parent_oneplate_','')+f'\n{e[0]:g} x {e[1]:g} x {e[2]:g} mm')
    fig.suptitle('Final print poses: Z=0 is the bed face');fig.tight_layout()
    fig.savefig(A/'_work/images/support_reduction_print_poses.png',dpi=140);plt.close(fig)

def main(resume=False):
    if not resume:
        code=audit_saved('support_reduction','support_reduction','support_reduction_all_layers')
        assert code==0,'Stored 3MF/hash/bed audit failed'
    audit=json.loads((W/'slice_audit.json').read_text());plots=[];poses=[]
    assert audit['passed'],'Cannot resume a failed base audit'
    detection={r['file']:r for r in json.loads((W/'support_detection/validation.json').read_text())}
    for record in audit['parts']:
        stem=Path(record['file']).stem
        segments=paths(A/'print_jobs/support_reduction'/stem/'plate_1.gcode')
        support=[p for z,f,p in segments if f.startswith('Support')]
        record['actual_support_extrusion_moves']=len(support)
        detected=detection[record['file']]
        record['automatic_detection_support_filament_mm']=detected['support_filament_mm']
        record['automatic_detection_source_matches']=detected['source_sha256']==next(r['source_sha256'] for r in json.loads((A/'print_jobs/support_reduction/validation.json').read_text()) if r['file']==record['file'])
        assert record['automatic_detection_source_matches']
        if stem not in PRIMARY:continue
        record['primary_support_free']=len(support)==0
        mesh=trimesh.load(A/'parts'/record['file'],force='mesh');poses.append((stem,mesh))
        report=W/(stem+'_overhang.json')
        run=subprocess.run(['python','-m','topopt','overhang',str(A/'parts'/record['file']),'--angle','45','--json',str(report)],capture_output=True)
        (A/'_work/logs'/(stem+'_support_reduction_overhang.log')).write_bytes(run.stdout+run.stderr)
        assert run.returncode==0
        layers=sorted({z for z,f,p in segments if f=='Outer wall'})
        for z in [layers[0],min(layers,key=lambda z:abs(z-PRIMARY[stem]))]:
            plots.append((stem,z,[(f,p) for zz,f,p in segments if zz==z]))
    fig,axes=plt.subplots(2,3,figsize=(15,9))
    for i,(stem,z,segments) in enumerate(plots):
        ax=axes[i%2,i//2]
        for kind,color in [('part','#247895'),('bridge','#d88714'),('support','#b33d59')]:
            selected=[p[:,:2] for f,p in segments if f!='Custom' and ('support' if f.startswith('Support') else 'bridge' if 'bridge' in f.lower() else 'part')==kind]
            if selected:ax.add_collection(LineCollection(selected,colors=color,linewidths=.5))
        ax.autoscale();ax.set_aspect('equal');ax.set_title(stem.replace('parent_oneplate_','')+f' / Z={z:g} mm')
        ax.set_xlabel('bed X / mm');ax.set_ylabel('bed Y / mm')
    fig.suptitle('Actual extrusion: first layer and hole-roof layer\nBlue: part; amber: bridge; red: generated support')
    fig.tight_layout(rect=[0,0,1,.94]);fig.savefig(A/'_work/images/support_reduction_detail_layers.png',dpi=140);plt.close(fig)
    render_poses(poses)
    audit['primary_support_free']=all(p.get('primary_support_free',True) for p in audit['parts'])
    audit['all_production_support_free']=all(p['actual_support_extrusion_moves']==0 for p in audit['parts'])
    audit['all_detector_support_free']=all(p['automatic_detection_support_filament_mm']==0 for p in audit['parts'])
    audit['limits'].append('Enabled detector still flags existing camera/clamp/cam details. Production omits these after reviewing unchanged short spans (<=4.2 mm) and overhangs; physical printing is unverified.')
    audit['passed']=bool(audit['passed'] and audit['primary_support_free'] and audit['all_production_support_free'])
    (W/'slice_audit.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
    print('Primary automatic support-free:',audit['primary_support_free'])
    print('Support extrusion moves:',{p['file']:p['actual_support_extrusion_moves'] for p in audit['parts']})
    return 0 if audit['passed'] else 1

if __name__=='__main__':
    if '--poses-only' in sys.argv:
        render_poses([(stem,trimesh.load(A/'parts'/(stem+'.stl'),force='mesh')) for stem in PRIMARY])
    else:raise SystemExit(main('--resume' in sys.argv))
