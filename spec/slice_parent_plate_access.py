"""Two bounded review plates; stream G-code and check nut access voids."""
from pathlib import Path
import json,math,re,shutil,sys,zipfile
import numpy as np
import trimesh
from shapely.geometry import Polygon,Point
from shapely.ops import unary_union
from publish_parent_plate_access import R,ASM,W,run,read,write,sha
from slice_parent_retrofit import attach_blocker

S=W/'slicing';J=ASM/'print_jobs/underside_nuts_20261029'


def intersects_box(start,end,lo,hi):
    """Continuous segment/box intersection, including short crossing moves."""
    near,far=0.,1.
    for a,b,l,h in zip(start,end,lo,hi):
        delta=b-a
        if abs(delta)<1e-12:
            if a<l or a>h:return False
        else:
            t0,t1=sorted(((l-a)/delta,(h-a)/delta))
            near=max(near,t0);far=min(far,t1)
            if near>far:return False
    return True


def paths(file):
    p=np.zeros(3);kind='';relative=True;old_e=0.;xyz_absolute=True
    with file.open(encoding='utf-8') as stream:
        for raw in stream:
            if raw.startswith('; FEATURE:'):kind=raw.split(':',1)[1].strip()
            line=raw.split(';',1)[0].strip()
            if line=='M83':relative=True
            if line=='M82':relative=False
            if line=='G90':xyz_absolute=True
            if line=='G91':xyz_absolute=False
            if line.startswith('G92 E'):old_e=float(re.search(r'E(-?\d*\.?\d+)',line)[1])
            if not re.match(r'^G[0123] ',line):continue
            args={k:float(n) for k,n in re.findall(r'([XYZEIJ])(-?\d*\.?\d+)',line)}
            old=p.copy()
            for i,k in enumerate('XYZ'):
                if k in args:p[i]=args[k] if xyz_absolute else p[i]+args[k]
            extrusion=args.get('E',0) if relative else args.get('E',old_e)-old_e
            if 'E' in args:old_e=old_e+args['E'] if relative else args['E']
            if extrusion<=0 or not any(k in args for k in 'XYIJ') or not kind:continue
            yield round(float(p[2]),3),kind,old.copy(),p.copy()


def main():
    S.mkdir(parents=True,exist_ok=True);J.mkdir(parents=True,exist_ok=True)
    # Open-bottom hex seats: keep support out of the removable nut space.
    sys.path.insert(0,str(R/'scad/lib'))
    import parent_gnss as G
    from parent_service_datums import FLOOR_NUT_DEPTH
    source=R/'parts/parent/interior/printed/parent_hand_service'
    stem='floor_underside_nut_support_blocker'
    blockers=[]
    points=G.RACK_FOOT_XY+G.UNIVERSAL_FRAME_FOOT_XY+[p for i,p in enumerate(G.SONY_CARRIER_FOOT_XY) if i!=2]
    for x,y in points:
        h=FLOOR_NUT_DEPTH+.4
        block=trimesh.creation.box(extents=[7,7,h])
        block.apply_translation([x,y,G.FLOOR_GRID_BOTTOM_Z-.2+h/2]);blockers.append(block)
    trimesh.util.concatenate(blockers).export(source/(stem+'.stl'),file_type='stl_ascii')
    meta=read(source/'manufacturing.json')
    meta['non_print_files']=sorted(set(meta.get('non_print_files',[])+[stem]))
    meta.setdefault('modifier_generators',{})[stem]='spec/slice_parent_plate_access.py'
    write(source/'manufacturing.json',meta)
    cfg=read(ASM/'print_config.json')
    cfg['modifiers']=[m for m in cfg['modifiers'] if m['host']!='floor_plate' and not m['source'].endswith('/main_floor_pilot_support_blocker.stl')]
    cfg['modifiers'].append(dict(host='floor_plate',source=(source/(stem+'.stl')).relative_to(R).as_posix()))
    write(ASM/'print_config.json',cfg)
    run([sys.executable,str(R/'tools/assembly_parts.py'),'sync','parent_hand_service'],'sync_nut_modifiers')
    previous=ASM/'_work/analysis/retrofit_20261024/slicing'
    for name in ['machine','process','filament']:
        profile=read(previous/(name+'.json'))
        if name=='process':profile.update(print_settings_id='Parent north wall floor access',enable_support='1',support_threshold_angle='45',dont_support_bridges='0',enable_arc_fitting='0')
        write(S/(name+'.json'),profile)
    manifest=read(ASM/'parts/manifest.json');entries={e['stem']:e for e in manifest['parts']}
    modifiers=manifest['modifiers'];records=[]
    plates=[[('floor_plate',30,21,0)],
            [('main_service_frame',25,32,0),('gnss_support_frame',25,150,0),('sony_support_frame',180,32,0)]]
    offset=np.array([float(n) for n in read(S/'machine.json')['extruder_offset'][0].split('x')]+[0])
    for index,members in enumerate(plates,1):
        work=S/('plate_'+str(index));work.mkdir(exist_ok=True)
        meshes=[];blocks=[];placed=[];voids=[]
        for name,x,y,angle in members:
            e=entries[name];source=ASM/'parts'/e['file'];assert sha(source)==e['sha256']
            mesh=trimesh.load_mesh(source);rotation=trimesh.transformations.euler_matrix(0,0,np.radians(angle));mesh.apply_transform(rotation);shift=np.array([x,y,0])-mesh.bounds[0];mesh.apply_translation(shift)
            assert mesh.bounds[1,:2].max()<253
            meshes.append(mesh)
            placed.append(dict(name=name,sha256=sha(source),bounds=mesh.bounds.tolist(),shift=shift.tolist(),bed_rotation_z_deg=angle))
            for m in modifiers:
                if m['host']!=name:continue
                b=trimesh.load_mesh(ASM/'parts'/m['file']);b.apply_transform(rotation);b.apply_translation(shift);blocks.append(b)
            matrix=rotation@np.array(e['model_to_print'])
            def xyz(point):return (matrix@np.array([*point,1]))[:3]+shift
            def void(label,x,y,z0,z1,r=1.35):
                corners=trimesh.bounds.corners([[x-r,y-r,z0],[x+r,y+r,z1]])
                q=np.array([xyz(p) for p in corners]);voids.append(dict(label=label,lo=q.min(0),hi=q.max(0)))
            import importlib.util
            spec=importlib.util.spec_from_file_location('dims',R/'scad/lib/parent_gnss.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
            if name=='floor_plate':
                for row in read(W/'candidate_checks.json')['sockets']:
                    xx,yy=row['xy'];void(row['label'],xx,yy,8.9,18.6)
                    void(row['label']+'_nut',xx,yy,8.85,11.43,r=3.35)
            elif name in ['sony_support_frame','gnss_support_frame']:
                points=g.SONY_CARRIER_FOOT_XY if name.startswith('sony') else g.UNIVERSAL_FRAME_FOOT_XY
                for i,(xx,yy) in enumerate(points):
                    if name.startswith('gnss') or i!=2:void(name+'_bottom_'+str(i),xx,yy,18.9,29.6,r=1.25)
                    void(name+'_top_'+str(i),xx,yy,59,69.5,r=1.25)
            elif name=='main_service_frame':
                for i,(xx,yy) in enumerate(g.RACK_FOOT_XY):void('MAIN_through_'+str(i),xx,yy,33.5,35.5,r=1.25)
            elif name=='battery_base':
                # Existing lid axis in battery-local coordinates.
                xx,yy=read(R/'parts/parent/interior/printed/parent_lipo_retainer/dimensions.json')['bolt_xy'][0]
                void('battery_lid_pilot',xx,yy,18.2,28.9,r=1.25)
        base=trimesh.util.concatenate(meshes);block=trimesh.util.concatenate(blocks) if blocks else None
        base.export(work/'placed.stl',file_type='stl_ascii')
        check=trimesh.load_mesh(work/'placed.stl');assert check.is_watertight and check.is_winding_consistent
        common=['C:/Program Files/Bambu Studio/bambu-studio.exe','--debug','2','--datadir',str(work/'studio_data'),
                '--load-settings',str(S/'machine.json')+';'+str(S/'process.json'),'--load-filaments',str(S/'filament.json'),
                '--arrange','0','--orient','0']
        run(common+['--slice','0','--export-3mf','seed.3mf','--outputdir',str(work),str(work/'placed.stl')],'slice_'+str(index)+'_seed',timeout=240,cwd=work)
        if block is not None:attach_blocker(work/'seed.3mf',work/'blocked.3mf',base,block)
        else:shutil.copyfile(work/'seed.3mf',work/'blocked.3mf')
        name='parent_underside_nuts_'+str(index)+'.3mf'
        run(common+['--slice','0','--export-3mf',name,'--outputdir',str(work),str(work/'blocked.3mf')],'slice_'+str(index)+'_blocked',timeout=240,cwd=work)
        assert read(work/'result.json')['return_code']==0
        with zipfile.ZipFile(work/name) as archive:
            assert archive.testzip() is None
            with archive.open('Metadata/plate_1.gcode') as src,(work/'plate_1.gcode').open('wb') as dst:shutil.copyfileobj(src,dst)
            for image in [n for n in archive.namelist() if n.startswith('Metadata/') and n.endswith('.png')]:
                if 'plate_1' in image:(ASM/'_work/images'/('underside_nuts_slice_'+str(index)+'_'+Path(image).name)).write_bytes(archive.read(image))
        first={p['name']:None for p in placed};last=first.copy();support_in_void=[];bridges=[]
        for z,kind,start,end in paths(work/'plate_1.gcode'):
            start+=offset;end+=offset;mid=(start+end)/2
            for item in placed:
                lo,hi=np.array(item['bounds'])
                if kind=='Outer wall' and np.all(mid[:2]>=lo[:2]-.05) and np.all(mid[:2]<=hi[:2]+.05):
                    first[item['name']]=z if first[item['name']] is None else min(first[item['name']],z)
                    last[item['name']]=z if last[item['name']] is None else max(last[item['name']],z)
            if kind.lower().startswith('support'):
                for v in voids:
                    if intersects_box(start,end,v['lo'],v['hi']):support_in_void.append(dict(label=v['label'],z=z,mid=mid.tolist()))
            if index==1 and 'bridge' in kind.lower() and 2.5<=z<=3.2:
                if any(np.all(mid[:2]>=v['lo'][:2]) and np.all(mid[:2]<=v['hi'][:2]) for v in voids):
                    bridges.append(dict(start=start.tolist(),end=end.tolist(),length_mm=float(np.linalg.norm(end-start))))
        assert not support_in_void,support_in_void[:10]
        for item in placed:
            assert first[item['name']] is not None and first[item['name']]<=.21 and last[item['name']]>item['bounds'][1][2]-.4,item
        record=dict(plate=index,passed=True,members=placed,first_model_layers_mm=first,last_model_layers_mm=last,
                    support_extrusions_in_nut_access_voids=len(support_in_void),nut_roof_bridges=bridges,
                    printed_embedded_nut_pockets=0,maximum_nut_roof_span_mm=6.7,
                    support_free_printability_verified=False,physical_print_test=False,
                    sha256=sha(work/name),profiles='X1C/0.4, PETG,0.2mm,wall4,100%, auto supports45deg, bridges included, local blockers',
                    limitations=['Underside-open hex pockets have roofs spanning at most6.7mm; no print pause. Actual bridge quality, thread pullout and fit require physical testing. Arcs disabled for continuous segment/void checks.'])
        write(work/'review.json',record);records.append(record);shutil.copyfile(work/name,J/name)
        print('SLICE_REVIEW',index,'functional void support0','bridge segments',len(bridges),'nut pocket roof span <=6.7mm',flush=True)
        del base,block,meshes,blocks,check
    for n in ['machine','process','filament']:shutil.copyfile(S/(n+'.json'),J/(n+'.json'))
    write(J/'manifest.json',dict(passed=True,plates=records,material='PETG',actual_print_test=False))


if __name__=='__main__':main()
