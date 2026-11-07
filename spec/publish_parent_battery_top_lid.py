"""Publish verified battery shapes, refresh metadata, and record bounded processes."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,shutil,subprocess,sys
import trimesh
from revise_parent_battery_top_lid import R,W,write
ASM=R/'assemblies/parent_hand_service'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def run(command,purpose,timeout=240,env=None,cwd=None):
    records=read(W/'publication_processes.json') if (W/'publication_processes.json').exists() else []
    log=W/(purpose+'.log')
    with log.open('wb') as out:
        p=subprocess.Popen(command,cwd=cwd or R,env=env,stdout=out,stderr=subprocess.STDOUT,creationflags=0x08000000)
        if 'bambu-studio' in command[0].lower():
            import ctypes
            api=ctypes.windll.kernel32
            api.SetProcessAffinityMask.argtypes=[ctypes.c_void_p,ctypes.c_size_t]
            api.SetProcessAffinityMask(ctypes.c_void_p(int(p._handle)),ctypes.c_size_t(3))
        row=dict(pid=p.pid,start_utc=datetime.now(timezone.utc).isoformat(),command=command,owner='battery_top_lid_20261029',purpose=purpose)
        records.append(row);write(W/'publication_processes.json',records)
        try:code=p.wait(timeout)
        except subprocess.TimeoutExpired:
            p.terminate()
            try:p.wait(10)
            except subprocess.TimeoutExpired:p.kill();p.wait(10)
            raise
        finally:
            row.update(exit_code=p.poll(),ended_utc=datetime.now(timezone.utc).isoformat());write(W/'publication_processes.json',records)
    if code:raise RuntimeError(str(log)+'\n'+log.read_text(encoding='utf-8',errors='replace')[-1500:])
    return log
def publish():
    result=read(W/'build_run.json');assert result['status']=='passed'
    verify=read(W/'verify_run.json')
    assert verify['status']=='passed'
    lines=(Path(verify['run_dir'])/'logs/freecad.log').read_text(encoding='utf-8').splitlines()
    report=json.loads(next(x.split('BATTERY_TOP_REPORT=',1)[1] for x in lines if 'BATTERY_TOP_REPORT=' in x))
    write(W/'checks.json',report);assert report['status']=='PASS',report
    geometry=[]
    for name,row in result['exports'].items():
        folder=R/'parts/parent/interior/printed'/('parent_hand_service' if name=='battery_base' else 'parent_lipo_retainer')
        m=trimesh.load(row['stl'],force='mesh');assert m.is_watertight and m.volume>0
        for suffix in ['step','stl']:shutil.copyfile(row[suffix],folder/(name+'.'+suffix))
        scad='// Generated from canonical Python sources by spec/revise_parent_battery_top_lid.py.\npolyhedron(points='+json.dumps(m.vertices.tolist())+',faces='+json.dumps(m.faces[:,::-1].tolist())+',convexity=10);\n'
        (folder/(name+'.scad')).write_text(scad,encoding='utf-8')
        test=W/(name+'_render.stl')
        run(['C:/Program Files/OpenSCAD/openscad.exe','-o',str(test),str(folder/(name+'.scad'))],name+'_openscad')
        rm=trimesh.load(test,force='mesh')
        assert rm.is_watertight and abs(abs(rm.volume)-m.volume)/m.volume<.001
        geometry.append(dict(part=name,watertight=True,bounds=m.bounds.tolist(),volume_mm3=m.volume,openscad_volume_mm3=rm.volume))
    write(W/'mesh_checks.json',geometry)
    for filename in ['placement.json','service_placement.json']:
        p=ASM/filename;d=read(p)
        for item in d['items']:
            if item['label']=='lipo_ret_bolt_0':
                # Locate from the lid placement, including a service translation.
                lid=next(i for i in d['items'] if i['label']=='lipo_ret_lid')
                shifts=[op['translate'] for op in lid['ops'] if 'translate' in op]
                xyz=[sum(a[j] for a in shifts) for j in range(3)]
                item['ops']=[{'translate':[xyz[0]-5,xyz[1]+50,xyz[2]+3]}]
                item['note']='M3x12, 9mm engagement in2.8mm plastic pilot; no nut.'
            if item['label'] in ['lipo_tray','lipo_ret_lid']:item['note']='2026-10-29 vertical-removal lid revision; reprint base and lid together.'
        d['battery_lid_design']=dict(type='vertical_lift_one_central_screw',screw='M3x12 into2.8mm plastic pilot; no nut',screw_xy_local_mm=[50,5],engagement_mm=9,bottom_clearance_mm=2,release_translation_box_mm=[0,0,120],operation='Open vessel lid, remove one M3x12, lift battery lid straight up; keep tray and four tray screws installed',locator_clearance_per_side_mm=.3,verification='battery_top_lid_report.md')
        write(p,d)
    p=R/'parts/parent/interior/printed/parent_lipo_retainer/manufacturing.json';d=read(p)
    d['print_rotations_deg']['parent_lipo_retainer_lid_slide']=[0,0,0]
    d['source_dependencies'].append('../../../../../spec/build_parent_battery_top_lid.py') if '../../../../../spec/build_parent_battery_top_lid.py' not in d['source_dependencies'] else None
    write(p,d)
    p=ASM/'print_config.json';d=read(p)
    d['modifiers']=[m for m in d['modifiers'] if m['host']!='battery_base']
    d['modifiers'].append(dict(host='battery_base',source='parts/parent/interior/printed/parent_hand_service/battery_lid_pilot_support_blocker.stl'))
    d['notes'].insert(0,'assemblies/parent_hand_service/battery_top_lid_report.md')
    d['note']='Battery base and lid: vertical removal with one M3x12. Reprint both; see battery_top_lid_report.md. Other component instructions retained.'
    write(p,d)
    for p in [ASM/'README.md',R/'parts/parent/interior/printed/parent_hand_service/README.md',R/'parts/parent/interior/printed/parent_lipo_retainer/README.md']:
        if p.exists():
            old=p.read_text(encoding='utf-8-sig')
            if '2026-10-29 電池蓋を上方取り外しへ変更' not in old:
                link='battery_top_lid_report.md' if p.parent==ASM else '../../../../../assemblies/parent_hand_service/battery_top_lid_report.md'
                p.write_text('## 2026-10-29 電池蓋を上方取り外しへ変更\n\n電池蓋はM3×12ねじ1本を外し、真上に持ち上げる方式へ変更。本体の固定ねじ4本は外さない。本体と蓋を各1個再印刷する。旧スライド手順は履歴。詳しくは [電池蓋の改訂報告]('+link+')。\n\n'+old,encoding='utf-8')
    p=R/'docs/部品一覧.md';old=p.read_text(encoding='utf-8-sig')
    if '2026-10-29 電池蓋：' not in old:p.write_text('2026-10-29 電池蓋：親機のbattery_baseとparent_lipo_retainer_lid_slideは上方取り外し・M3×12ねじ1本へ改訂。双方を各1個再印刷。[詳細](../assemblies/parent_hand_service/battery_top_lid_report.md)。\n\n'+old,encoding='utf-8')
    p=ASM/'manufacturing_parts.json';d=read(p);d['battery_lid_revision']=dict(date='2026-10-29',reprint=['battery_base','parent_lipo_retainer_lid_slide'],fastener='one M3x12, no nut',report='battery_top_lid_report.md');write(p,d)
    run([sys.executable,'-X','utf8','spec/revise_parent_battery_top_lid.py','--refresh'],'refresh_siblings',timeout=600)
    finish()
    print('Published verified battery base and lid',flush=True)
def finish():
    blocker=trimesh.creation.box(extents=[4,4,12]);blocker.apply_translation([50,5,23.5])
    blocker.export(R/'parts/parent/interior/printed/parent_hand_service/battery_lid_pilot_support_blocker.stl',file_type='stl_ascii')
    p=ASM/'print_config.json';d=read(p)
    d['modifiers']=[m for m in d['modifiers'] if m['host']!='battery_base']
    d['modifiers'].append(dict(host='battery_base',source='parts/parent/interior/printed/parent_hand_service/battery_lid_pilot_support_blocker.stl'))
    write(p,d)
    p=R/'parts/parent/interior/printed/parent_hand_service/manufacturing.json';d=read(p)
    d['modifier_generators']['battery_lid_pilot_support_blocker']='spec/review_parent_battery_top_lid.py'
    write(p,d)
    p=ASM/'validation_current.json';d=read(p)
    d['battery_top_lid_revision']=dict(date='2026-10-29',cad_status='PASS',evidence='_work/analysis/battery_top_lid_20261029/checks.json',slicing='_work/analysis/battery_top_lid_20261029/slice_checks.json',physical_strength='unverified')
    write(p,d)
    run([sys.executable,'tools/assembly_parts.py','sync','parent_hand_service'],'sync')
def assemblies():
    run(['powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-File',str(R/'build.ps1'),'-Assemblies','-NoPreview','-Paths',str(ASM)],'assembly_build')
    fc='C:/Users/ryupc/AppData/Local/Programs/FreeCAD 1.0/bin/freecadcmd.exe'
    env=os.environ.copy();env.update(ASM_JSON=str(ASM/'service_placement.json'),ASM_ROOT=str(R),STL_OUT=str(ASM/'service.stl'),STEP_OUT=str(ASM/'service.step'),STEP_IN=str(ASM/'service.step'),PYTHONIOENCODING='utf-8')
    env.pop('ASM_GROUP',None)
    run([sys.executable,str(R/'scad/lib/asm_gen.py'),env['ASM_JSON'],str(ASM/'service_view.scad')],'service_view',env=env)
    for script in ['asm_to_stl.py','asm_to_step.py','verify_asm_step.py']:run([fc,str(R/'scad/lib'/script)],'service_'+script,env=env)
    for suffix in ['step','stl']:shutil.copyfile(ASM/('parent_hand_service.'+suffix),ASM/('closed.'+suffix))
    shutil.copyfile(ASM/'parent_hand_service_view.scad',ASM/'closed_view.scad')
if __name__=='__main__':
    if '--assemblies' in sys.argv:assemblies()
    elif '--finish' in sys.argv:finish()
    else:publish()
