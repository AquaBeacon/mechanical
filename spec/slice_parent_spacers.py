"""Offline X1C/PETG plate with all twelve individually delivered parent spacers."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import re
import math
import zipfile
import numpy as np
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from configure_parent_spacer_delivery import SPACERS


def paths(path):
    """Actual extruding paths, interpolating circular G2/G3 moves for review."""
    point=np.zeros(3);feature='';rows=[];relative=True;previous_e=0.
    for raw in path.read_text(encoding='utf-8').splitlines():
        if raw.startswith('; FEATURE:'):feature=raw.split(':',1)[1].strip()
        line=raw.split(';',1)[0].strip()
        if line=='M83':relative=True
        if line=='M82':relative=False
        if line.startswith('G92 E'):previous_e=float(re.search(r'E(-?\d*\.?\d+)',line).group(1))
        if not re.match(r'^G[0123] ',line):continue
        args={k:float(n) for k,n in re.findall(r'([XYZEIJ])(-?\d*\.?\d+)',line)}
        old=point.copy()
        for i,key in enumerate('XYZ'):
            if key in args:point[i]=args[key]
        extrusion=args.get('E',0) if relative else args.get('E',previous_e)-previous_e
        if 'E' in args:previous_e=args['E'] if not relative else previous_e+args['E']
        if extrusion<=0 or not any(k in args for k in 'XYIJ') or not feature:continue
        points=np.array([old,point.copy()])
        if line.startswith(('G2 ','G3 ')) and any(k in args for k in 'IJ'):
            center=old[:2]+np.array([args.get('I',0),args.get('J',0)])
            a=math.atan2(*(old[:2]-center)[::-1]);b=math.atan2(*(point[:2]-center)[::-1])
            delta=(b-a)%(2*math.pi) if line.startswith('G3 ') else -((a-b)%(2*math.pi))
            if abs(delta)<1e-8:delta=2*math.pi if line.startswith('G3 ') else -2*math.pi
            angles=np.linspace(a,a+delta,max(3,int(abs(delta)*30)))
            xy=center+np.linalg.norm(old[:2]-center)*np.column_stack([np.cos(angles),np.sin(angles)])
            points=np.column_stack([xy,np.linspace(old[2],point[2],len(xy))])
        rows.append((round(float(point[2]),3),feature,points))
    return rows

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'assemblies/parent_hand_service'
WORK = OUT/'_work/analysis/spacer_delivery_20261022'
JOB = OUT/'print_jobs/spacers_20261022'
PROFILES = Path('C:/Program Files/Bambu Studio/resources/profiles/BBL')


def write(path, data):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def main():
    WORK.mkdir(parents=True,exist_ok=True);JOB.mkdir(parents=True,exist_ok=True)
    manifest = json.loads((OUT/'parts/manifest.json').read_text(encoding='utf-8'))
    entries = [e for e in manifest['parts'] if e['stem'] in SPACERS]
    assert {e['stem']:e['quantity'] for e in entries} == SPACERS
    meshes=[];members=[];names=[]
    # Rows: MAIN, Sony, GNSS. Same ordering as the installation table.
    for stem in SPACERS:
        entry=next(e for e in entries if e['stem']==stem)
        source=OUT/'parts'/entry['file']
        assert hashlib.sha256(source.read_bytes()).hexdigest()==entry['sha256']
        for label in entry['labels']:
            i=len(meshes);cx=70+38*(i%4);cy=75+40*(i//4)
            mesh=trimesh.load(source,force='mesh');assert mesh.is_volume
            mesh.apply_translation([cx-mesh.bounds[:,0].mean(),cy-mesh.bounds[:,1].mean(),-mesh.bounds[0,2]])
            members.append(dict(label=label,file=entry['file'],source_sha256=entry['sha256'],
                                center_xy_mm=[cx,cy],bounds_mm=mesh.bounds.tolist()))
            meshes.append(mesh);names.append(stem.replace('_column','')+' / '+label.rsplit('_',1)[-1])
    combined=trimesh.util.concatenate(meshes)
    assert len(combined.split())==12 and combined.is_volume
    staged=WORK/'spacers_placed.stl';combined.export(staged)

    index={p.stem:p for p in PROFILES.rglob('*.json')}
    def resolve(name):
        d=json.loads(index[name].read_text(encoding='utf-8'));result={}
        if d.get('inherits'):result.update(resolve(d['inherits']))
        for included in d.get('include',[]):result.update(resolve(included))
        result.update(d)
        for key in ('inherits','include'):result.pop(key,None)
        return result
    machine=resolve('Bambu Lab X1 Carbon 0.4 nozzle');machine['curr_bed_type']='Textured PEI Plate'
    process=resolve('0.20mm Standard @BBL X1C')
    process.update(print_settings_id='Parent twelve slip spacers PETG 0.20 wall4 solid',
                   layer_height='0.2',initial_layer_print_height='0.2',wall_loops='4',
                   top_shell_layers='5',bottom_shell_layers='5',sparse_infill_density='100%',
                   sparse_infill_pattern='zig-zag',brim_type='outer_only',brim_width='3',
                   enable_support='1',support_type='normal(auto)',support_on_build_plate_only='0',
                   support_threshold_angle='45',dont_support_bridges='0',
                   support_top_z_distance='0.2',support_bottom_z_distance='0.2',
                   support_object_xy_distance='0.35',support_interface_top_layers='2',
                   enable_prime_tower='0',skirt_loops='0')
    filament=resolve('Generic PETG')
    for name,data in [('machine',machine),('process',process),('filament',filament)]:write(WORK/(name+'.json'),data)
    project=JOB/'parent_spacers.3mf'
    cmd=['C:/Program Files/Bambu Studio/bambu-studio.exe','--debug','2','--datadir',str(WORK/'studio_data'),
         '--load-settings',str(WORK/'machine.json')+';'+str(WORK/'process.json'),
         '--load-filaments',str(WORK/'filament.json'),'--arrange','0','--orient','0','--slice','0',
         '--export-3mf',project.name,'--outputdir',str(JOB),str(staged)]
    if '--review-only' in sys.argv:
        previous=json.loads((JOB/'manifest.json').read_text(encoding='utf-8'))
        assert hashlib.sha256(staged.read_bytes()).hexdigest()==previous['staged_stl_sha256']
        assert hashlib.sha256(project.read_bytes()).hexdigest()==previous['three_mf_sha256']
        exit_code=0
    else:
        run=subprocess.run(cmd,capture_output=True,text=True,errors='replace',cwd=JOB,creationflags=0x08000000)
        (OUT/'_work/logs/spacer_delivery_slice.log').write_text(run.stdout+run.stderr,encoding='utf-8')
        exit_code=run.returncode
    result=json.loads((JOB/'result.json').read_text(encoding='utf-8'))
    assert exit_code==0 and result['return_code']==0,result
    with zipfile.ZipFile(project) as z:
        assert z.testzip() is None
        settings=json.loads(z.read('Metadata/project_settings.config'))
        (WORK/'plate_1.gcode').write_bytes(z.read('Metadata/plate_1.gcode'))
    assert str(settings['wall_loops'])=='4' and settings['sparse_infill_density']=='100%'
    assert str(settings['enable_support'])=='1' and abs(float(settings['layer_height'])-.2)<1e-8
    segments=paths(WORK/'plate_1.gcode')
    real=[p[:,:2] for z,f,p in segments if f!='Custom']
    bounds=np.concatenate(real);lo=bounds.min(axis=0);hi=bounds.max(axis=0)
    support_moves=sum(1 for z,f,p in segments if f.lower().startswith('support'))
    # Per member: verify first-layer outer wall and wall extrusion immediately
    # below its top. Brims alone must never count as a present spacer.
    for member,mesh in zip(members,meshes):
        bb=mesh.bounds;layers=[]
        for z,f,p in segments:
            midpoint=p[:,:2].mean(axis=0)
            if f=='Outer wall' and np.all(midpoint>=bb[0,:2]-.05) and np.all(midpoint<=bb[1,:2]+.05):
                layers.append(z)
        member['first_outer_wall_z_mm']=min(layers) if layers else None
        member['last_outer_wall_z_mm']=max(layers) if layers else None
        member['passed']=bool(layers and abs(min(layers)-.2)<.001 and max(layers)>=bb[1,2]-.4)
    plate=result['sliced_plates'][0]
    record=dict(passed=all(m['passed'] for m in members) and bool(np.all(lo>.25) and np.all(hi<255.75)) and support_moves==0,
                geometry='12 separate spacer solids, no runner',members=members,
                quantities=dict(Counter(m['file'] for m in members)),material='Generic PETG',
                printer='Bambu Lab X1 Carbon',nozzle_mm=.4,layer_mm=.2,walls=4,infill_percent=100,
                brim_mm=3,support_detection='normal(auto), 45 degrees, all surfaces, bridge exemption disabled',
                support_extrusion_moves=support_moves,extrusion_bounds_xy_mm=[lo.tolist(),hi.tolist()],
                filament_g=sum(f['total_used_g'] for f in plate['filaments']),
                prediction_seconds=plate['total_predication'],warnings=plate.get('warning_message',''),
                source='assemblies/parent_hand_service/parts/manifest.json',
                three_mf_sha256=hashlib.sha256(project.read_bytes()).hexdigest(),
                staged_stl_sha256=hashlib.sha256(staged.read_bytes()).hexdigest(),
                limits=['Physical print, fit and tightening remain unverified.',
                        'G2/G3 paths interpolated for layer review; actual machine accuracy is unmeasured.'])
    write(JOB/'manifest.json',record)
    # Actual toolpaths at the bed and at both locator transitions / top layers.
    targets=[.2,14.2,31.2,31.8,41.8,42.4]
    actual=sorted({z for z,f,p in segments if f=='Outer wall'})
    fig,axes=plt.subplots(3,2,figsize=(12,10))
    for ax,target in zip(axes.flat,targets):
        height=min(actual,key=lambda x:abs(x-target))
        pp=[p[:,:2] for z,f,p in segments if z==height and f!='Custom']
        ax.add_collection(LineCollection(pp,colors='#137c8b',linewidths=.6))
        ax.set(xlim=(60,194),ylim=(65,165),aspect='equal',title=f'Actual G-code / Z={height:g} mm',xlabel='bed X [mm]',ylabel='bed Y [mm]')
    fig.tight_layout();fig.savefig(OUT/'_work/images/spacer_delivery_layers.png',dpi=150);plt.close(fig)
    fig=plt.figure(figsize=(13,7));ax=fig.add_subplot(111,projection='3d')
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    for member,mesh in zip(members,meshes):
        color='#da8a27' if member['label'].startswith('main') else ('#218891' if member['label'].startswith('sony') else '#4777bb')
        ax.add_collection3d(Poly3DCollection(mesh.triangles,facecolor=color,edgecolor='none'))
        x,y=member['center_xy_mm'];ax.text(x,y,mesh.bounds[1,2]+3,member['label'],fontsize=8,ha='center')
    ax.set(xlim=(58,196),ylim=(64,168),zlim=(0,52),xlabel='bed X [mm]',ylabel='bed Y [mm]',zlabel='height [mm]')
    ax.set_box_aspect((138,104,52));ax.view_init(elev=36,azim=-62)
    fig.suptitle('Parent spacers: MAIN x4 / Sony x4 / GNSS x4\nPETG | 0.4 mm nozzle | 0.2 mm layers | 4 walls | 100% infill')
    fig.tight_layout();fig.savefig(OUT/'_work/images/spacer_delivery_plate.png',dpi=160);plt.close(fig)
    print(json.dumps({k:record[k] for k in ('passed','filament_g','prediction_seconds','support_extrusion_moves','warnings')},ensure_ascii=False))
    assert record['passed'],record


if __name__=='__main__':main()
