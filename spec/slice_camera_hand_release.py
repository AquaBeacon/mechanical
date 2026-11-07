"""Offline X1C/PETG slicing and saved 3MF/G-code audit for the new fixtures."""
from pathlib import Path
import hashlib, json, os, subprocess, sys, zipfile
import numpy as np
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
ROOT=Path(__file__).resolve().parents[1]
from review_parent_exterior_slices import paths
sys.path.insert(0,str(ROOT/'tools'))
from prepare_child_horizontal_plate_frame import save
PRE=ROOT/'print_jobs/child_simple/slice_validation'
CLI=r'C:\Program Files\Bambu Studio\bambu-studio.exe'

def main(job_name='camera_twist_20261021', camera_only=False, extra_jobs=None):
    os.chdir(ROOT)
    jobs=[('parent_exterior','camera_mount_twist',
           ROOT/'parts/child/exterior/printed/dji_osmo_action6_mount_m3/camera_mount_twist.stl',True),
          ('child_horizontal_plate_frame','child_horizontal_twist_mount_camera_receiver',
           ROOT/'parts/child/exterior/printed/child_horizontal_twist_mount/child_horizontal_twist_mount_camera_receiver.stl',True)]
    if camera_only: jobs=jobs[:1]
    if extra_jobs is not None: jobs=extra_jobs
    for assembly,stem,source,supports in jobs:
        base=ROOT/'assemblies'/assembly
        dest=base/'print_jobs'/job_name/stem;dest.mkdir(parents=True,exist_ok=True)
        process=json.loads((PRE/'process.json').read_text(encoding='utf-8'))
        process.update(print_settings_id='C camera fit prototype PETG 0.10 6 walls 15 percent',
            layer_height='0.1',initial_layer_print_height='0.2',wall_loops='6',top_shell_layers='8',bottom_shell_layers='8',
            sparse_infill_density='15%',sparse_infill_pattern='gyroid',enable_support='1' if supports else '0',support_type='normal(auto)',
            support_on_build_plate_only='1',support_top_z_distance='0.2',support_bottom_z_distance='0.2',
            support_threshold_angle='45',brim_width='5')
        save(dest/'process.json',process)
        m=trimesh.load(source,force='mesh');assert m.is_volume
        m.apply_translation([128-m.bounds[:,0].mean(),128-m.bounds[:,1].mean(),-m.bounds[0,2]])
        m.export(dest/'placed.stl')
        cmd=[CLI,'--debug','2','--datadir',str(dest/'studio_data'),'--load-settings',str(PRE/'machine.json')+';'+str(dest/'process.json'),
             '--load-filaments',str(PRE/'filament.json'),'--arrange','0','--orient','0','--slice','0',
             '--export-3mf',stem+'.3mf','--outputdir',str(dest),str(dest/'placed.stl')]
        print('Slicing',stem,flush=True)
        proc=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,errors='replace',cwd=dest)
        from datetime import datetime, timezone
        record=dict(pid=proc.pid,started_utc=datetime.now(timezone.utc).isoformat(),purpose='camera hand fixture slicer',owner='camera_hand_release_20261029')
        save(dest/'process_record.json',record)
        try: output,_=proc.communicate(timeout=360)
        except subprocess.TimeoutExpired:
            proc.terminate()
            try: output,_=proc.communicate(timeout=15)
            except subprocess.TimeoutExpired:proc.kill();output,_=proc.communicate()
            record.update(timed_out=True,exited=proc.poll() is not None);save(dest/'process_record.json',record);raise
        record.update(exit_code=proc.returncode,exited=proc.poll() is not None);save(dest/'process_record.json',record)
        r=subprocess.CompletedProcess(cmd,proc.returncode,output,'')
        (dest/'slice.log').write_text(r.stdout+r.stderr,encoding='utf-8')
        result=json.loads((dest/'result.json').read_text(encoding='utf-8'))
        assert r.returncode==0 and result['return_code']==0,result
        with zipfile.ZipFile(dest/(stem+'.3mf')) as z:
            assert z.testzip() is None
            gc=z.read('Metadata/plate_1.gcode');settings=json.loads(z.read('Metadata/project_settings.config'))
            (dest/'plate_1.gcode').write_bytes(gc)
        segments=paths(dest/'plate_1.gcode')
        extrusion=np.array([p[:,:2] for zz,f,p in segments if f!='Custom'])
        lo=extrusion.min(axis=(0,1));hi=extrusion.max(axis=(0,1))
        warnings=result['sliced_plates'][0].get('warning_message','')
        plate=result['sliced_plates'][0]
        report=dict(passed=bool(np.all(lo>=28.25) and np.all(hi<=255.75) and not warnings),
            source=source.relative_to(ROOT).as_posix(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
            three_mf_sha256=hashlib.sha256((dest/(stem+'.3mf')).read_bytes()).hexdigest(),
            layer_mm=float(settings['layer_height']),enable_support=settings['enable_support'],
            support_on_build_plate_only=settings['support_on_build_plate_only'],support_threshold_angle=settings['support_threshold_angle'],
            support_feature_sections=gc.decode().count('; FEATURE: Support'),
            extrusion_bounds_xy_mm=[lo.tolist(),hi.tolist()],warning_message=warnings,
            seconds=plate['total_predication'],grams=sum(f['total_used_g'] for f in plate['filaments']),
            material='Generic PETG',walls=6,infill='15% gyroid',
            limits=['Physical print and C fit unverified; G2/G3 plotted as chords.',
                    'Snap-cap nubs, finger fit and physical gripping require inspection on a real print.'])
        save(dest/'validation.json',report)
        layers=sorted({zz for zz,f,p in segments if f=='Outer wall'})
        candidates=[(zz,sum(1 for z,f,p in segments if z==zz and ('bridge' in f.lower() or 'support' in f.lower()))) for zz in layers]
        selected=[layers[0]]+[min(layers,key=lambda z:abs(z-target)) for target in (10,20,40)]
        selected.append(max(candidates,key=lambda x:x[1])[0])
        fig,axes=plt.subplots(1,len(selected),figsize=(4*len(selected),4))
        for ax,zz in zip(axes,selected):
            for category,color in [('wall','#247895'),('bridge','#d88714'),('support','#8a659f')]:
                lines=[p[:,:2] for z,f,p in segments if z==zz and (category in f.lower())]
                if lines:ax.add_collection(LineCollection(lines,colors=color,linewidths=.55))
            ax.autoscale();ax.set_aspect('equal');ax.set_title(f'Z={zz:g} mm')
        fig.suptitle(stem+' | walls blue, bridges amber, supports violet');fig.tight_layout()
        images=base/'_work/images';images.mkdir(parents=True,exist_ok=True)
        fig.savefig(images/(stem+'_'+job_name+'_layers.png'),dpi=140);plt.close(fig)
        print(json.dumps(report),flush=True)
        assert report['passed'],report

if __name__=='__main__':
    jobs=[
     ('parent_exterior','camera_mount_twist',ROOT/'parts/child/exterior/printed/dji_osmo_action6_mount_m3/camera_mount_twist.stl',True),
     ('parent_exterior','parent_oneplate_camera_qr_female',ROOT/'parts/parent/exterior/printed/parent_oneplate_camera_qr/parent_oneplate_camera_qr_female.stl',True),
     ('child_horizontal_plate_frame','child_horizontal_twist_mount_camera_receiver',ROOT/'parts/child/exterior/printed/child_horizontal_twist_mount/child_horizontal_twist_mount_camera_receiver.stl',True),
     ('parent_exterior','camera_hand_spacer',ROOT/'parts/child/exterior/printed/dji_osmo_action6_mount_m3/camera_hand_spacer.stl',True),
     ('parent_exterior','camera_hand_knob',ROOT/'parts/child/exterior/printed/dji_osmo_action6_mount_m3/camera_hand_knob.stl',True),
     ('parent_exterior','camera_hand_knob_cap',ROOT/'parts/child/exterior/printed/dji_osmo_action6_mount_m3/camera_hand_knob_cap.stl',False)]
    main('camera_hand_release_20261029',extra_jobs=jobs)
