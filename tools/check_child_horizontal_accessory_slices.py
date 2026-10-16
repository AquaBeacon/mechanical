"""Inspect real per-job settings and auto-support detection for new parts."""
from pathlib import Path
import hashlib,json,shutil,zipfile,re
import numpy as np
import trimesh
from topopt import external,slicer
from topopt.cli import slice as native
from prepare_child_horizontal_plate_frame import ROOT,OUT,save
from build_child_horizontal_accessories import PART
from build_child_horizontal_accessories import TAG

def support_paths(path):
    point=np.zeros(3);feature='';paths=[];wall=[]
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.startswith('; FEATURE:'):feature=line.split(':',1)[1].strip()
        if not re.match(r'^G[0123] ',line):continue
        args={k:float(v) for k,v in re.findall(r'([XYZ E])(-?\d*\.?\d+)',line) if k!=' '}
        previous=point.copy()
        for i,key in enumerate('XYZ'):
            if key in args:point[i]=args[key]
        if args.get('E',0)>0 and ('X' in args or 'Y' in args):
            if feature.startswith('Support'):paths.append(np.vstack([previous,point]))
            if feature=='Outer wall':wall.append(point.copy())
    if not paths:return [],None
    allwall=np.array(wall);allpaths=np.array(paths)
    # Parts were grounded to XY min=0 before slicing. Recover arrangement
    # translation from the symmetric outer-wall envelope, independent of bed.
    mesh=trimesh.load(OUT/'parts'/(path.parent.name+'.stl'),force='mesh')
    centre=(allwall[:,:2].min(axis=0)+allwall[:,:2].max(axis=0))/2
    offset=centre-(mesh.bounds[0,:2]+mesh.bounds[1,:2])/2
    allpaths[:,:,:2]-=offset
    bounds=np.array([allpaths.reshape(-1,3).min(axis=0),allpaths.reshape(-1,3).max(axis=0)])
    return allpaths,bounds.tolist()

def main():
    p=json.loads((OUT/'placement.json').read_text(encoding='utf-8'))
    labels={r['label'] for r in p['items'] if r.get('owner')==TAG and r['print']}
    manifest=json.loads((OUT/'parts/manifest.json').read_text(encoding='utf-8'));rows=[];views=[]
    exe=external.require('slicer','Verify accessory slicing')
    interface=json.loads((PART/'_work/analysis/geometry/interface.json').read_text())
    for entry in manifest['parts']:
        if not labels.intersection(entry['labels']):continue
        stem=Path(entry['file']).stem;job=OUT/'print_jobs/x1c_petg_basic'/stem
        evidence=json.loads((job/'source_manifest.json').read_text(encoding='utf-8'))
        if evidence['source_sha256']!=hashlib.sha256((OUT/'parts'/entry['file']).read_bytes()).hexdigest():
            raise RuntimeError('Stale production slice: '+stem)
        with zipfile.ZipFile(job/(stem+'.3mf')) as z:
            config=json.loads(z.read('Metadata/project_settings.config'))
        if abs(float(config['layer_height'])-evidence['layer_height_mm'])>1e-8:raise RuntimeError('Wrong layer: '+stem)
        work=OUT/'_work/analysis/side_twist_mount/slicer_support_detection'/stem;work.mkdir(parents=True,exist_ok=True)
        files={}
        for kind in ('machine','process','filament'):
            src=job/f'preset_{kind}.json';dest=work/src.name
            if kind=='process':
                data=json.loads(src.read_text(encoding='utf-8'));data.update(slicer.SUPPORT_MODES['auto']);data['support_on_build_plate_only']='1';save(dest,data)
            else:shutil.copyfile(src,dest)
            files[kind]=str(dest)
        code,output,seconds=native._run(exe,files,str(OUT/'parts'/entry['file']),str(work),stem+'.3mf','keep',240,bed_type='Textured PEI Plate')
        (work/'slicer.log').write_text(output,encoding='utf-8')
        if code:raise RuntimeError('Auto support slicing failed: '+stem)
        info,header,features=native._read_3mf(work/(stem+'.3mf'))
        with zipfile.ZipFile(work/(stem+'.3mf')) as z:
            auto_config=json.loads(z.read('Metadata/project_settings.config'))
        support=slicer.support_mm(features)
        paths,bounds=support_paths(work/'plate_1.gcode')
        production_paths,production_bounds=support_paths(job/'plate_1.gcode')
        protected=None
        if stem=='child_horizontal_twist_mount_light_twist':
            # Holder axis is V in the canonical integral male coordinates.
            centre=np.array([0,0,interface[10],1.])@np.array(entry['model_to_print']).T
            protected=dict(kind='light_bore',centre_xy_mm=centre[:2].tolist(),radius_mm=16.3,
                           z_min_mm=.4,z_max_mm=80.6)
        elif stem=='child_horizontal_twist_mount_frame_receiver':
            centre=np.array([interface[6],interface[7],interface[5],1.])@np.array(entry['model_to_print']).T
            protected=dict(kind='C_cam_and_socket',centre_xy_mm=centre[:2].tolist(),radius_mm=14.1,
                           z_min_mm=centre[2]+4.2,z_max_mm=centre[2]+17.8)
        bad=[]
        if protected is not None and len(production_paths):
            # G1 support strokes sampled at <=0.25 mm, including segments that
            # enter and exit the protected void between their endpoints.
            for line in production_paths:
                n=max(2,int(np.ceil(np.linalg.norm(line[1]-line[0])/.25))+1)
                samples=np.linspace(line[0],line[1],n)
                hit=(np.linalg.norm(samples[:,:2]-protected['centre_xy_mm'],axis=1)<protected['radius_mm']) & (samples[:,2]>protected['z_min_mm']) & (samples[:,2]<protected['z_max_mm'])
                if hit.any():bad.append(line.tolist())
        if bad:raise RuntimeError('Support enters protected bore/cam: '+stem+' '+str(bad[:2]))

        if bounds is not None:views.append((stem,paths))
        row=dict(file=entry['file'],quantity=entry['quantity'],layer_height_mm=float(config['layer_height']),
            production_support_filament_mm=evidence['support_filament_mm'],auto_enable_support=auto_config.get('enable_support'),
            auto_threshold_deg=auto_config.get('support_threshold_angle'),auto_support_filament_mm=support,
            auto_features_mm=features,auto_warnings=native._warnings(output),
            auto_support_bounds_in_print_coordinates_mm=bounds,
            production_support_bounds_in_print_coordinates_mm=production_bounds,protected_support_exclusion=protected,
            protected_region_support_strokes=len(bad),source_sha256=hashlib.sha256((OUT/'parts'/entry['file']).read_bytes()).hexdigest(),
            auto_3mf_sha256=hashlib.sha256((work/(stem+'.3mf')).read_bytes()).hexdigest(),
            production_3mf_sha256=hashlib.sha256((job/(stem+'.3mf')).read_bytes()).hexdigest())
        rows.append(row);print(stem,'auto support mm:',support,flush=True)
    if len(rows)!=len(labels):raise RuntimeError('Incomplete accessory print files')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection,Line3DCollection
    fig=plt.figure(figsize=(12,6),facecolor='#f4f3ef')
    for index,(stem,paths) in enumerate(views):
        ax=fig.add_subplot(1,len(views),index+1,projection='3d')
        mesh=trimesh.load(OUT/'parts'/(stem+'.stl'),force='mesh')
        ax.add_collection3d(Poly3DCollection(mesh.triangles,facecolor='#558c99',edgecolor='none',alpha=.15,rasterized=True))
        ax.add_collection3d(Line3DCollection(paths,colors='#c85d46',linewidths=.65))
        ax.set_xlim(*mesh.bounds[:,0]);ax.set_ylim(*mesh.bounds[:,1]);ax.set_zlim(*mesh.bounds[:,2]);ax.set_box_aspect(mesh.extents.copy());ax.view_init(26,35)
        ax.set_title(stem.replace('quick_release_prototypes_',''),fontsize=11)
    fig.suptitle('Auto-support toolpaths (red), actual print pose',fontsize=14)
    fig.tight_layout();fig.savefig(OUT/'_work/images/side_twist_support_detection.png',dpi=150);plt.close(fig)
    save(OUT/'_work/analysis/side_twist_mount/slicing.json',dict(result='PASS',parts=rows,
        additional_filament_g=sum(json.loads((OUT/'print_jobs/x1c_petg_basic'/Path(r['file']).stem/'source_manifest.json').read_text(encoding='utf-8'))['filament_g_per_part'] for r in rows),
        additional_print_time_s=sum(json.loads((OUT/'print_jobs/x1c_petg_basic'/Path(r['file']).stem/'source_manifest.json').read_text(encoding='utf-8'))['print_time_s_per_part'] for r in rows),
        limitations=['Slicer support detection and G-code do not prove successful printing; integral light male uses removable external build-plate supports',
                     'Inspect first-print C lug bridges, groove roofs, small bores and mating fit']))

if __name__=='__main__':main()
