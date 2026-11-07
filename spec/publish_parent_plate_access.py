"""Stage, verify and publish the existing parent's floor-access revision."""
from pathlib import Path
from datetime import datetime,timezone
import copy,hashlib,json,os,shutil,subprocess,sys
import trimesh

R=Path(__file__).resolve().parents[1]
ASM=R/'assemblies/parent_hand_service'
W=ASM/'_work/analysis/underside_nuts_20261029'
OSC='C:/Program Files/OpenSCAD/openscad.exe'
FC='C:/Users/ryupc/AppData/Local/Programs/FreeCAD 1.0/bin/freecadcmd.exe'

def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def archive(p):
    if not p.exists():return
    dst=W/'history'/p.relative_to(R)
    if not dst.exists():dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dst)

def run(command,purpose,env=None,timeout=240,cwd=None):
    records=read(W/'publication_processes.json') if (W/'publication_processes.json').exists() else []
    log=W/(purpose+'.log')
    with log.open('wb') as stream:
        p=subprocess.Popen(command,cwd=cwd or R,env=env,stdout=stream,stderr=subprocess.STDOUT,creationflags=0x08004000)
        rec=dict(pid=p.pid,start_utc=datetime.now(timezone.utc).isoformat(),command=command,
                 owner='parent_underside_nuts_20261029',purpose=purpose,cwd=str(cwd or R))
        if 'bambu-studio' in str(command[0]).lower():
            import ctypes
            affinity=ctypes.c_size_t();system=ctypes.c_size_t()
            api=ctypes.windll.kernel32
            api.GetProcessAffinityMask.argtypes=[ctypes.c_void_p,ctypes.POINTER(ctypes.c_size_t),ctypes.POINTER(ctypes.c_size_t)]
            api.SetProcessAffinityMask.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
            handle=ctypes.c_void_p(int(p._handle))
            if api.GetProcessAffinityMask(handle,ctypes.byref(affinity),ctypes.byref(system)):
                bits=[1<<i for i in range(affinity.value.bit_length()) if affinity.value&(1<<i)]
                mask=sum(bits[:2])
                if api.SetProcessAffinityMask(handle,ctypes.c_size_t(mask)):rec['cpu_affinity_mask']=mask
        records.append(rec);write(W/'publication_processes.json',records)
        try:code=p.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            p.terminate()
            try:p.wait(timeout=10)
            except subprocess.TimeoutExpired:p.kill();p.wait(timeout=10)
            raise
        finally:
            rec.update(exit_code=p.poll(),ended_utc=datetime.now(timezone.utc).isoformat())
            write(W/'publication_processes.json',records)
    assert code==0,(purpose,log.read_text(encoding='utf-8',errors='replace')[-2000:])
    return log

def folder(name):
    if name.startswith('wetlink_'):return R/'parts/common/exterior/cots/wetlink_penetrator_m10'
    if name.startswith('screw_'):return R/'parts/common/interior/cots/screw'
    if name.startswith('nylon_'):return R/'parts/parent/interior/cots/adafruit_lis3mdl'
    if name.startswith('coax_'):return R/'parts/parent/interior/cots/ann_mb1'
    if name.startswith('gnss_'):return R/'parts/parent/interior/printed/gnss_universal_carrier'
    if name in ['ann_mb1_coax_ring_service','antenna_service_shelf'] or name.startswith('cradle_floor_foot_'):return R/'parts/parent/interior/printed/ann_mb1_internal_rack'
    return R/'parts/parent/interior/printed/parent_hand_service'

def verify_fresh(result):
    assert result['status']=='passed'
    job=read(Path(result['run_dir'])/'job.json')
    for relative,rec in job['snapshots'].items():
        assert sha(R/relative)==rec['sha256'],('Stale candidate input',relative)
    return job

def prepare():
    candidates={}
    exports={}
    for filename in ['floor_run.json','related_run.json']:
        result=read(W/filename);verify_fresh(result)
        exports.update(result['exports'])
    for i,(name,row) in enumerate(exports.items()):
        p=ASM/'_work/intermediate'/('pa_'+str(i)+'.step')
        shutil.copyfile(row['step'],p)
        assert sha(p)==row['step_sha256']
        candidates[name]=p.relative_to(R).as_posix()
    write(W/'candidate_files.json',dict(candidates=candidates,exports=exports,current_placement_sha256=sha(ASM/'placement.json')))
    write(W/'candidate_placement.json',candidate_layout())
    print('Staged',len(candidates),'candidate files')

def candidate_layout():
    d=read(ASM/'placement.json')
    sys.path.insert(0,str(R/'scad/lib'))
    import parent_gnss as G
    import parent_service_datums as S
    d['items']=[r for r in d['items'] if not r['label'].startswith('retrofit_')]
    def item(label,part,file,xyz,rotate=None,printed=False):
        row=dict(label=label,part=part,file=file,group='interior',ops=[{'translate':xyz}])
        if rotate:row['ops'].append({'rotate':rotate})
        if printed:row.update(print=True,color='Orange')
        d['items'].append(row)
    interfaces=read(W/'pcb_interfaces.json')['holes']
    mh=[[18+x,112-y] for x,y in interfaces['PARENT_MAIN']]
    ph=[[25.8+y,115+x] for x,y in interfaces['PARENT_PWR']]
    part='parts/common/interior/cots/screw'
    for row in S.retrofit_fasteners(G,mh,ph):
        name=row['label'];x,y=row['xy'];diameter=row['diameter'];length=int(row['length'])
        file='screw_m'+str(diameter)+'x'+str(length)+('_socket' if diameter==4 else '')
        item('retrofit_'+name+'_bolt',part,file,[x,y,row['head_z']],[180,0,0] if row['direction']>0 else None)
        nut=row['nut_z']
        if nut is not None:item('retrofit_'+name+'_nut',part,'screw_nut_m'+str(diameter),[x,y,nut],[0,0,30])
        if row['washer']:
            z=(nut+(3.2 if diameter==4 else 2.4)) if nut is not None else G.FLOOR_GRID_BOTTOM_Z-S.FLOOR_WASHER_T
            item('retrofit_'+name+'_washer',part,'screw_washer_m'+str(diameter)+('_08' if diameter==4 else '_05'),[x,y,z])
    d['build_order']=[r['label'] for r in d['items']]
    d['moving_labels']=[r['label'] for r in d['items'] if r.get('group')=='interior' and r['label']!='lid_keepout']
    d['service_translation_mm']=[240,0,0];d['lift_mm']=120;d['service_only']=[]
    d['note']='2026-10-29 underside-open nut seats; unified50mm frames. See unified_support_report.md.'
    d['retrofit']=dict(sensor_supports='Two one-piece four-legged frames',leg_length_mm=50,leg_datums_mm=[S.SENSOR_BASE_Z,S.SENSOR_JOINT_Z],floor_fixing='Top through bolts into eleven underside-open hex nut seats',sony_floor_fixings=3,gnss_floor_fixings=4,main_floor_fixings=4,top_fixing='M3x65 through bolts; Sony rear-left M3x10 pilot')
    d['plate_access_revision'].update(roofed_floor_nuts=0,floor_nut_z_mm=S.FLOOR_NUT_BOTTOM_Z,printed_nut_pockets=11,underside_open_nut_pockets=11,nut_pocket_depth_mm=S.FLOOR_NUT_DEPTH,print_pause_required=False)
    return d


def update_placements():
    d=read(W/'candidate_placement.json')
    for file in ['placement.json','service_placement.json']:archive(ASM/file)
    write(ASM/'placement.json',d)
    service=copy.deepcopy(d)
    for row in service['items']:
        if row['label'] in d['moving_labels']:row['ops']=[{'translate':[240,0,0]}]+row.get('ops',[])
    service['items']=[r for r in service['items'] if r['label']!='lid_keepout']
    service['build_order']=[r['label'] for r in service['items']]
    service['note']='Interior moved aside after vertical extraction with both M10 penetrators retained.'
    write(ASM/'service_placement.json',service)

def publish():
    assert read(W/'assembly_checks.json')['passed']
    staged=read(W/'candidate_files.json');exports=staged['exports']
    assert sha(ASM/'placement.json')==staged['current_placement_sha256'],'Assembly changed after staging; restage and verify without overwriting concurrent work'
    job=verify_fresh(read(W/'verification_run.json'))
    assert job['parameters']['candidates']==staged['candidates'],'Verified candidate selection changed'
    assert read(R/job['parameters']['layout'])==read(W/'candidate_placement.json'),'Verified placement changed'
    for phase in ['floor_run.json','related_run.json']:verify_fresh(read(W/phase))
    publication={}
    for name,row in exports.items():
        src=Path(row['stl']);assert sha(src)==row['stl_sha256']
        mesh=trimesh.load_mesh(src)
        assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume>0,name
        dst=folder(name);dst.mkdir(parents=True,exist_ok=True)
        for ext in ['step','stl','scad']:archive(dst/(name+'.'+ext))
        if not name.startswith('screw_'):
            text='// Generated by the canonical parent Python sources and validated exchange pipeline.\n'
            text+='polyhedron(points='+json.dumps(mesh.vertices.tolist())+',faces='+json.dumps(mesh.faces[:,::-1].tolist())+',convexity=10);\n'
            (dst/(name+'.scad')).write_text(text,encoding='utf-8')
        publication[name]=dict(folder=dst.relative_to(R).as_posix(),sha256=row['stl_sha256'],
                               volume_mm3=float(mesh.volume),bounds_mm=mesh.bounds.tolist())
        if '/printed/' in dst.as_posix() and not name.endswith('_support_blocker'):
            independent=W/(name+'_render.stl')
            log=run([OSC,'-o',str(independent),str(dst/(name+'.scad'))],'render_'+name,timeout=180)
            text=log.read_text(encoding='utf-8',errors='replace')
            assert 'WARNING:' not in text and 'ERROR:' not in text,text
            rendered=trimesh.load_mesh(independent)
            assert rendered.is_watertight and rendered.is_winding_consistent and abs(rendered.volume-mesh.volume)/mesh.volume<.001,name
    # All generated CAD sources must exist before their corresponding freshly
    # generated meshes are copied. The print pack checks folder-wide CAD age.
    for name,row in exports.items():
        for ext in ['step','stl']:shutil.copyfile(row[ext],folder(name)/(name+'.'+ext))
    for dst in {folder(n) for n in exports if '/printed/' in folder(n).as_posix()}:
        meta_path=dst/'manufacturing.json';archive(meta_path);meta=read(meta_path)
        deps=['spec/build_parent_access_related.py','scad/lib/parent_service_datums.py']
        if dst.name=='parent_hand_service':deps+=['scad/lib/parent_floor_access.py','spec/build_parent_floor_access.py']
        for dep in deps:
            rel=os.path.relpath(R/dep,dst).replace('\\','/')
            if rel not in meta.setdefault('source_dependencies',[]):meta['source_dependencies'].append(rel)
        for name in exports:
            if folder(name)==dst and name.endswith('_support_blocker'):
                meta['non_print_files']=sorted(set(meta.get('non_print_files',[])+[name]))
        # Preserve floating-point precision when placing detailed generated CAD
        # on the bed. Copies are still verified after reload by assembly_parts.
        meta['portable_stl_export_format']='stl_ascii'
        if dst.name=='parent_hand_service':meta.setdefault('print_rotations_deg',{})['floor_plate']=[0,0,0]
        write(meta_path,meta)
    update_placements()
    from collections import Counter
    rows=read(ASM/'placement.json')['items']
    path=ASM/'manufacturing_parts.json';archive(path);m=read(path)
    m.update(revision='2026-10-29 underside-open nuts with unified50mm supports',
             printed_parts=[r.get('file',Path(r['part']).name) for r in rows if r.get('print') is True],
             additional_printed_parts=[],print_sets=[],
             note='Complete portable set15 parts. Reprint4 changed parts; see unified_support_report.md.',
             purchased_fasteners_by_file=dict(Counter(r.get('file',Path(r['part']).name) for r in rows if r['part'].endswith('/screw'))))
    m['metal_fasteners']=m['purchased_fasteners_by_file'].copy()
    m['spacer_delivery']=dict(revision=m['revision'],mode='two_unified_frames',sensor_leg_length_mm=50,floor_nuts=11,floor_washers=0,embedded_nut_pockets=0)
    write(path,m)
    for variant_path,line in [
        (R/'parts/common/exterior/cots/wetlink_penetrator_m10/variants.txt','body_only wall_t=3.1 show_nut=false'),
        (R/'parts/common/interior/cots/screw/variants.txt','m4x12_head10_h5_envelope d=4 l=12 head_d=10 head_h=5'),
        (R/'parts/common/interior/cots/screw/variants.txt','m4x18_socket d=4 l=18 head_d=7 head_h=4')]:
        text=variant_path.read_text(encoding='utf-8-sig')
        if line not in text:
            archive(variant_path)
            with variant_path.open('w',encoding='utf-8-sig',newline='') as stream:
                stream.write((text.rstrip()+'\n'+line+'\n').replace('\r\n','\n').replace('\n','\r\n'))
    cfg_path=ASM/'print_config.json';archive(cfg_path);cfg=read(cfg_path)
    cfg['note']='2026-10-29：床下面のM3六角ナット座11か所。上からの貫通ねじで固定。50mm一体支持枠を維持。手順は ../unified_support_report.md。電池本体・蓋の同時交換は ../battery_top_lid_report.md を参照。'
    cfg['notes']=list(dict.fromkeys(['assemblies/parent_hand_service/unified_support_report.md']+cfg.get('notes',[])))
    active={r.get('file',Path(r['part']).name) for r in rows if r.get('print') is True}
    cfg['modifiers']=[q for q in cfg['modifiers'] if q['host'] in active and q['host']!='floor_plate']
    for name in ['sony_support_frame','gnss_support_frame']:
        cfg['modifiers']=[q for q in cfg['modifiers'] if q['host']!=name]
        cfg['modifiers'].append(dict(host=name,source=(folder(name)/(name+'_support_blocker.stl')).relative_to(R).as_posix()))
    write(cfg_path,cfg)
    write(W/'publication.json',dict(status='fit_check_prototype',exports=publication,
                                   structural_and_physical_validation=False))
    run([sys.executable,str(R/'tools/assembly_parts.py'),'sync','parent_hand_service'],'sync_parts')
    print('Published verified geometric prototype; physical fit and strength remain unverified.')

def assemblies():
    env=os.environ.copy();env.update(ASM_ROOT=str(R),PYTHONIOENCODING='utf-8')
    for name,placement in [('parent_hand_service','placement.json'),('service','service_placement.json')]:
        env.update(ASM_JSON=str(ASM/placement),STL_OUT=str(ASM/(name+'.stl')),
                   STEP_OUT=str(ASM/(name+'.step')),STEP_IN=str(ASM/(name+'.step')))
        env.pop('ASM_GROUP',None)
        run([sys.executable,str(R/'scad/lib/asm_gen.py'),env['ASM_JSON'],str(ASM/(name+'_view.scad'))],name+'_view',env)
        for script in ['asm_to_stl.py','asm_to_step.py','verify_asm_step.py']:
            run([FC,str(R/'scad/lib'/script)],name+'_'+script,env,timeout=300)
    for ext in ['step','stl']:shutil.copyfile(ASM/('parent_hand_service.'+ext),ASM/('closed.'+ext))
    shutil.copyfile(ASM/'parent_hand_service_view.scad',ASM/'closed_view.scad')

def previews():
    images=ASM/'_work/images';images.mkdir(parents=True,exist_ok=True)
    p=R/'parts/parent/interior/printed/parent_hand_service'
    for name,camera in [('floor_top','0,0,0,0,0,0,500'),('floor_iso','0,0,0,55,0,35,500')]:
        run([OSC,'--render','--projection=ortho','--colorscheme=Tomorrow','--imgsize=1400,1100',
             '--viewall','--autocenter','--camera='+camera,'-o',str(images/('plate_access_'+name+'.png')),
             str(p/'floor_plate.scad')],'preview_'+name)
    inter=ASM/'_work/intermediate'
    def imp(path):return 'import('+json.dumps(str(path).replace('\\','/'))+');'
    for name in ['sony_support_frame','gnss_support_frame']:
        run([OSC,'--render','--projection=ortho','--colorscheme=Tomorrow','--imgsize=1400,1100',
             '--viewall','--autocenter','--camera=0,0,0,65,0,35,250',
             '-o',str(images/(name+'.png')),str(folder(name)/(name+'.scad'))],'preview_'+name)
    # The floor is clamped by an external underside head and washer, with
    # engagement in the leg. Never show the retired embedded-nut section.
    section=''
    clip='translate([9,144.9,4])cube([8,0.2,70]);'
    for path in [p/'floor_plate.stl',folder('gnss_support_frame')/'gnss_support_frame.stl']:
        section+='color([.72,.79,.84])intersection(){'+imp(path)+clip+'}\n'
    section+='color([.45,.48,.5])intersection(){translate([13,145,8.34])difference(){cylinder(r=3.5,h=.5,$fn=48);translate([0,0,-.1])cylinder(r=1.6,h=.7,$fn=48);}'+clip+'}\n'
    from_path=R/'parts/common/interior/cots/screw/screw_m3x16.stl'
    section+='color([.9,.65,.2])intersection(){translate([13,145,8.34])rotate([180,0,0])'+imp(from_path)+clip+'}\n'
    source=inter/'unified_support_section.scad';source.write_text(section,encoding='utf-8')
    run([OSC,'--render','--projection=ortho','--colorscheme=Tomorrow','--imgsize=1000,1400','--viewall','--autocenter',
         '--camera=0,0,0,90,0,0,90','-o',str(images/'unified_support_section.png'),str(source)],'preview_support_section')
    pen=R/'parts/common/exterior/cots/wetlink_penetrator_m10'
    text=''
    for x in [150,175]:text+='color([.5,.52,.55])translate(['+str(x)+',228.3,32.5])rotate([90,0,0])'+imp(pen/'wetlink_m10_bcas_reference.stl')+'\n'
    text+='color([.1,.65,.7])translate([150,228.3,32.5])rotate([90,0,0])'+imp(pen/'wetlink_m10_bulkhead_wrench.stl')+'\n'
    text+='color([.7,.76,.83,.22])'+imp(R/'parts/parent/exterior/cots/bcas212310g/bcas212310g.stl')
    source=inter/'pa_wrench_access.scad';source.write_text(text,encoding='utf-8')
    run([OSC,'--projection=ortho','--colorscheme=Tomorrow','--imgsize=1400,1100','--viewall','--autocenter',
         '--camera=0,0,0,40,0,210,400','-o',str(images/'plate_access_wrench_access.png'),str(source)],'preview_wrench_access')

if __name__=='__main__':
    if '--prepare' in sys.argv:prepare()
    elif '--assemblies' in sys.argv:assemblies()
    elif '--previews' in sys.argv:previews()
    else:publish()
