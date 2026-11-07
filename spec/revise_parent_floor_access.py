"""Bounded candidate build, source snapshots, process ownership and inspection."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import subprocess
import sys
import shutil

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT/'assemblies/parent_hand_service/_work/analysis/underside_nuts_20261029'


def write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    holes = {}
    sources = {}
    for board in ['PARENT_MAIN', 'PARENT_PWR', 'TX_improved']:
        path = ROOT.parent/'hardware/pcb'/board/(board+'.kicad_pcb')
        text = path.read_text(encoding='utf-8')
        starts = [m.start() for m in re.finditer(r'\(footprint ', text)]
        rows = []
        for a, b in zip(starts, starts[1:]+[len(text)]):
            section = text[a:b]
            if re.search(r'\(property "Reference" "H[1-4]"', section):
                at = re.search(r'\(at ([\d.-]+) ([\d.-]+)', section)
                rows.append([float(at[1]), float(at[2])])
        assert len(rows) == 4, board
        holes[board] = rows
        sources[board] = dict(path=str(path), sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    write(WORK/'pcb_interfaces.json', dict(holes=holes, sources=sources))
    sys.path.insert(0, str(ROOT/'tools/cad_foundation'))
    from service import CadService
    import cli
    original_run = subprocess.run

    def tracked_run(command, **kwargs):
        if 'freecadcmd' not in str(command[0]).lower():
            return original_run(command, **kwargs)
        timeout = kwargs.pop('timeout')
        kwargs['creationflags']=kwargs.get('creationflags',0)|0x08004000
        started = datetime.now(timezone.utc).isoformat()
        process = subprocess.Popen(command, **kwargs)
        receipt = dict(pid=process.pid, start_utc=started, command=command,
                       owner='parent_underside_nuts_20261029', purpose=Path(generator).stem)
        history=json.loads((WORK/'process_history.json').read_text(encoding='utf-8')) if (WORK/'process_history.json').exists() else []
        if (WORK/'process.json').exists():
            previous=json.loads((WORK/'process.json').read_text(encoding='utf-8'))
            if not any(r['pid']==previous['pid'] and r['start_utc']==previous['start_utc'] for r in history):history.append(previous)
        write(WORK/'process_history.json',history)
        write(WORK/'process.json', receipt)
        try:
            code = process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill(); process.wait(timeout=10)
            raise
        finally:
            receipt.update(exit_code=process.poll(), ended_utc=datetime.now(timezone.utc).isoformat())
            write(WORK/'process.json', receipt)
        return subprocess.CompletedProcess(command, code)

    cli.subprocess.run = tracked_run
    dependencies = ['scad/lib/parent_service_datums.py', 'spec/build_parent_hand_service.py', 'spec/parent_switch_tx_body.py',
                    'scad/lib/parent_gnss.py', 'scad/lib/cad_edge_finish.py', 'scad/lib/parent_floor_access.py',
                    'parts/parent/exterior/cots/bcas212310g/dimensions.json',
                    'parts/parent/exterior/cots/bcas212310g/interior_corner_clearance.step']
    generator='spec/build_parent_floor_access.py'
    if '--survey' in sys.argv:
        generator='spec/survey_parent_penetrator_access.py'
        rows=json.loads((ROOT/'assemblies/parent_hand_service/placement.json').read_text(encoding='utf-8'))['items']
        dependencies+=['assemblies/parent_hand_service/placement.json']
        dependencies+=[(Path(r['part'])/(r.get('file',Path(r['part']).name)+'.step')).as_posix() for r in rows
                       if r['label'] in ['plate','tx_improved','sony_mount_plate','gnss_sony_shared_column','gnss_universal_carrier']]
        dependencies += [str(p.relative_to(ROOT)).replace('\\','/') for p in
                         (ROOT/'parts/common/exterior/cots/wetlink_penetrator_m10/ref').glob('*/*.STEP')]
    if '--related' in sys.argv:
        generator='spec/build_parent_access_related.py'
        dependencies += ['scad/lib/parent_service_datums.py','scad/lib/parent_service_retrofit.py','scad/lib/parent_corner_mounts.py',
                         'scad/lib/parent_case_access.py','scad/lib/parent_penetrator_access.py',
                         'parts/parent/interior/printed/ann_mb1_internal_rack/ann_mb1_coax_ring.step',
                         'parts/common/exterior/cots/wetlink_penetrator_m10/wetlink_penetrator_m10_ref_body_only.step',
                         'spec/build_parent_gnss.py','scad/lib/parent_battery_slide.py',
                         'parts/parent/interior/printed/parent_lipo_retainer/dimensions.json',
                         'parts/parent/interior/printed/parent_lipo_retainer/parent_lipo_retainer_pads.step',
                         'parts/child/interior/printed/child_vtray_batt_floor/child_vtray_batt_floor.scad',
                         'parts/parent/interior/cots/adafruit_lis3mdl/ref/Adafruit LIS3MDL.brd',
                         'assemblies/parent_hand_service/_work/analysis/underside_nuts_20261029/candidate_checks.json']
        dependencies += [str(p.relative_to(ROOT)).replace('\\','/') for p in
                         (ROOT/'parts/common/exterior/cots/wetlink_penetrator_m10/ref').glob('*/*.STEP')]
    if '--verify' in sys.argv:
        generator='spec/verify_parent_plate_access.py'
        files=json.loads((WORK/'candidate_files.json').read_text(encoding='utf-8'))['candidates']
        layout=ROOT/'assemblies/parent_hand_service/_work/intermediate/us_layout.json'
        baseline=ROOT/'assemblies/parent_hand_service/_work/intermediate/us_baseline.json'
        shutil.copyfile(WORK/'candidate_placement.json',layout)
        shutil.copyfile(WORK/'history/assemblies/parent_hand_service/placement.json',baseline)
        rows=json.loads(layout.read_text(encoding='utf-8'))['items']
        dependencies+=list(files.values())+['scad/lib/parent_penetrator_access.py','scad/lib/parent_service_datums.py',
                       'parts/parent/interior/cots/adafruit_lis3mdl/ref/Adafruit LIS3MDL.brd',
                       layout.relative_to(ROOT).as_posix(),
                       'assemblies/parent_hand_service/_work/analysis/underside_nuts_20261029/candidate_checks.json']
        aliases={'plate':'floor_plate','lipo_tray':'battery_base','coax_ring':'ann_mb1_coax_ring_service'}
        dependencies+=[(Path(r['part'])/(r.get('file',Path(r['part']).name)+'.step')).as_posix() for r in rows
                       if not r['part'].endswith('/screw') and not r['label'].startswith('pen_')
                       and aliases.get(r['label'],r.get('file',r['label'])) not in files]
        old_shapes={}
        for i,row in enumerate(rows):
            rel=Path(row['part'])/(row.get('file',Path(row['part']).name)+'.step')
            history=WORK/'history'/rel
            if history.exists():
                target=ROOT/'assemblies/parent_hand_service/_work/intermediate'/('pa_hist_'+str(i)+'.step')
                shutil.copyfile(history,target);old_shapes[row['label']]=target.relative_to(ROOT).as_posix()
        dependencies+=list(old_shapes.values())
        dependencies.append(baseline.relative_to(ROOT).as_posix())
    if '--normalize' in sys.argv:
        generator='spec/normalize_parent_floor_access.py'
        dependencies=['assemblies/parent_hand_service/_work/intermediate/pa_floor_source.FCStd',
                      'assemblies/parent_hand_service/_work/intermediate/pa_floor_source.step']
    # Same foundation worker/snapshots. Full legacy floor booleans need a
    # bounded ten-minute batch, beyond the interactive MCP's four-minute cap.
    service=CadService(root=ROOT)
    body=(ROOT/'spec/parent_switch_tx_body.py').read_text(encoding='utf-8').split('from parent_floor_access import add_floor_access')[0]
    seed=body.encode()+json.dumps(holes,sort_keys=True).encode()
    for path in ['spec/build_parent_hand_service.py','scad/lib/parent_gnss.py','scad/lib/cad_edge_finish.py',
                 'parts/parent/exterior/cots/bcas212310g/dimensions.json',
                 'parts/parent/exterior/cots/bcas212310g/interior_corner_clearance.step']:
        seed+=(ROOT/path).read_bytes()
    fingerprint=hashlib.sha256(seed).hexdigest()
    cache=ROOT/'assemblies/parent_hand_service/_work/intermediate'/('floor_base_'+fingerprint[:12]+'.brep')
    legacy=WORK/'base_cache'/fingerprint/'floor_base.brep'
    if legacy.exists() and not cache.exists():
        cache.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(legacy,cache)
    params=dict(pcb_holes=holes,base_fingerprint=fingerprint)
    if '--verify' in sys.argv:params.update(candidates=files,old_shapes=old_shapes,layout=layout.relative_to(ROOT).as_posix(),baseline_layout=baseline.relative_to(ROOT).as_posix())
    if cache.exists():
        dependencies.append(cache.relative_to(ROOT).as_posix())
        params['base_cache']=cache.relative_to(ROOT).as_posix()
    if '--survey' in sys.argv or '--related' in sys.argv or '--normalize' in sys.argv:
        sys.path.insert(0,str(ROOT/'scad/lib'));import parent_gnss as dimensions
        result=service.build_native(generator,parameters=dict(pcb_holes=holes,switch_centres=dimensions.power_switch_centres(),only_underside_nuts='--related' in sys.argv and '--all-related' not in sys.argv),dependencies=dependencies,timeout=240)
    else:
        plan=dict(schema_version=1,kind='native',name='build_parent_floor_access',units='mm',
                  generator=generator,parameters=params,input_files=[generator]+dependencies)
        try:
            with service._lock():
                result=cli.run_job(ROOT,plan,timeout=600)
        finally:
            process=json.loads((WORK/'process.json').read_text(encoding='utf-8'))
            run=Path(process['command'][2]).parents[1]
            candidate=run/'intermediate/floor_base.brep'
            if candidate.exists() and not cache.exists():
                cache.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(candidate,cache)
                write(cache.with_suffix('.json'),dict(base_fingerprint=fingerprint,sha256=hashlib.sha256(cache.read_bytes()).hexdigest(),run=str(run)))
    write(WORK/('related_run.json' if '--related' in sys.argv else 'survey_run.json' if '--survey' in sys.argv else 'verification_run.json' if '--verify' in sys.argv else 'floor_run.json'),result)
    write(WORK/'build_run.json', result)
    log = Path(result['run_dir'])/'logs/freecad.log'
    prefix='PENETRATOR_SURVEY=' if '--survey' in sys.argv else 'PLATE_ASSEMBLY_REPORT=' if '--verify' in sys.argv else 'FLOOR_ACCESS_REPORT='
    records = [line.split(prefix, 1)[1] for line in log.read_text(encoding='utf-8').splitlines()
               if prefix in line]
    if records:
        write(WORK/('penetrator_survey.json' if '--survey' in sys.argv else 'assembly_checks.json' if '--verify' in sys.argv else 'candidate_checks.json'), json.loads(records[-1]))
    if '--normalize' in sys.argv:
        record=[line.split('FLOOR_NORMALIZATION=',1)[1] for line in log.read_text(encoding='utf-8').splitlines() if 'FLOOR_NORMALIZATION=' in line]
        write(WORK/'exchange_check.json',json.loads(record[-1]))
    print(json.dumps(dict(status=result['status'],run_dir=result['run_dir'],report=result['report'],
                          exports=list(result.get('exports',{}))),ensure_ascii=False),flush=True)


if __name__ == '__main__':
    main()
