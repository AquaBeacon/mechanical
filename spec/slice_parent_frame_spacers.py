"""Two bounded X1C/PETG review plates, using canonical oriented print copies."""
from pathlib import Path
import json,hashlib,zipfile,sys
import numpy as np,trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from slice_parent_retrofit import run,attach_blocker,paths
R=Path(__file__).resolve().parents[1];A=R/'assemblies/parent_hand_service'
W=A/'_work/analysis/frame_spacers_20261024/slicing';J=A/'print_jobs/frame_spacers_20261024'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def model_paths(file):
    # Bambu G-code subtracts the configured nozzle offset. Convert back to
    # model/bed coordinates before comparing paths with source geometry.
    offset=read(W/'machine.json')['extruder_offset'];assert len(offset)==1
    xy=np.array([float(v) for v in offset[0].split('x')]);assert len(xy)==2
    return [(z,t,p+np.array([xy[0],xy[1],0])) for z,t,p in paths(file)]
def main():
    W.mkdir(parents=True,exist_ok=True);J.mkdir(parents=True,exist_ok=True)
    previous=A/'_work/analysis/retrofit_20261024/slicing'
    for n in ['machine','process','filament']:
        d=read(previous/(n+'.json'))
        if n=='process':d.update(print_settings_id='Parent flat frame and clearance spacers',enable_support='1',support_threshold_angle='45',dont_support_bridges='0')
        write(W/(n+'.json'),d)
    manifest=read(A/'parts/manifest.json');entries={e['stem']:e for e in manifest['parts']};mods={e['host']:e for e in manifest['modifiers']}
    plates=[[('main_service_frame',25,32),('antenna_service_shelf',25,142),('power_adapter',165,32)],
            [('ann_mb1_coax_ring_service',25,32),('gnss_fixed_column_0',180,32),('gnss_fixed_column_1',200,32),('gnss_fixed_column_2',220,32),('gnss_sony_shared_column',232,32),('sony_fixed_column_0',180,60),('sony_fixed_column_1',200,60),('sony_fixed_column_3',220,60),('sony_mount_plate',180,150)]+[('cradle_floor_foot_'+str(i),180+20*i,90) for i in range(4)]]
    records=[]
    for number,members in enumerate(plates,1):
        f=W/('plate_'+str(number));f.mkdir(exist_ok=True);meshes=[];blockers=[];placed=[]
        if '--plate2-only' in sys.argv and number==1:
            previous=read(f/'review.json')
            for member in previous['members']:assert sha(A/'parts'/entries[member['name']]['file'])==member['sha256']
            records.append(previous);continue
        for n,x,y in members:
            e=entries[n];source=A/'parts'/e['file'];assert sha(source)==e['sha256']
            mesh=trimesh.load_mesh(source);shift=np.array([x,y,0])-mesh.bounds[0];mesh.apply_translation(shift);meshes.append(mesh)
            placed.append(dict(name=n,sha256=sha(source),bounds=mesh.bounds.tolist()))
            if n in mods:
                b=trimesh.load_mesh(A/'parts'/mods[n]['file']);b.apply_translation(shift);blockers.append(b)
        base=trimesh.util.concatenate(meshes);blocked=trimesh.util.concatenate(blockers);base.export(f/'placed.stl')
        common=['C:/Program Files/Bambu Studio/bambu-studio.exe','--debug','2','--datadir',str(f/'studio_data'),'--load-settings',str(W/'machine.json')+';'+str(W/'process.json'),'--load-filaments',str(W/'filament.json'),'--arrange','0','--orient','0']
        name='parent_frame_spacers_plate_'+str(number)+'.3mf'
        if '--review-only' in sys.argv:
            previous=read(f/'review.json');assert sha(f/name)==previous['sha256']
            assert [(e['name'],e['sha256']) for e in placed]==[(e['name'],e['sha256']) for e in previous['members']]
        else:
            run(common+['--slice','0','--export-3mf','seed.3mf','--outputdir',str(f),str(f/'placed.stl')],f,'seed')
            attach_blocker(f/'seed.3mf',f/'blocked.3mf',base,blocked)
            run(common+['--slice','0','--export-3mf',name,'--outputdir',str(f),str(f/'blocked.3mf')],f,'slice')
        assert read(f/'result.json')['return_code']==0
        with zipfile.ZipFile(f/name) as z:
            assert z.testzip() is None;(f/'plate_1.gcode').write_bytes(z.read('Metadata/plate_1.gcode'))
        segments=model_paths(f/'plate_1.gcode');layers=sorted({z for z,t,p in segments if t!='Custom'})
        for e in placed:
            lo,hi=np.array(e['bounds']);walls=[z for z,t,p in segments if t=='Outer wall' and np.all(p[:,:2].mean(axis=0)>=lo[:2]-.05) and np.all(p[:,:2].mean(axis=0)<=hi[:2]+.05)]
            e['first_model_layer_mm']=min(walls) if walls else None;e['last_model_layer_mm']=max(walls) if walls else None
            assert walls and min(walls)<=.21 and max(walls)>hi[2]-.4,e
        fig,axs=plt.subplots(2,3,figsize=(13,9))
        for ax,target in zip(axs.flat,[.2,.8,2.2,3.8,10,max(layers)-.2]):
            z=min(layers,key=lambda v:abs(v-target))
            for support,color in [(False,'#236a88'),(True,'#d18431')]:
                lines=[p[:,:2] for zz,t,p in segments if abs(zz-z)<.001 and t!='Custom' and t.lower().startswith('support')==support]
                if lines:ax.add_collection(LineCollection(lines,colors=color,linewidths=.35))
            ax.set(xlim=(0,256),ylim=(0,256),aspect='equal',title=f'Z {z:.2f} mm')
        fig.suptitle(f'Parent plate {number}: actual G-code (blue=model, orange=support)');fig.tight_layout()
        fig.savefig(A/f'_work/images/frame_spacers_plate_{number}_toolpaths.png',dpi=140);plt.close(fig)
        rec=dict(plate=number,passed=True,members=placed,support_paths=sum(t.lower().startswith('support') for _,t,_ in segments),sha256=sha(f/name),profiles='X1C / 0.4 / Generic PETG / 0.2mm / 4 walls / 100% / supports auto45deg / bridges included / local bore and nut blockers')
        records.append(rec);write(f/'review.json',rec);(J/name).write_bytes((f/name).read_bytes())
        print('SLICE_PASS '+str(number),flush=True)
        del segments,base,blocked,meshes,blockers
    write(J/'manifest.json',dict(passed=True,plates=records,limitations=['Review actual bridge anchoring in toolpath images; physical printing remains unverified.']))
if __name__=='__main__':main()
