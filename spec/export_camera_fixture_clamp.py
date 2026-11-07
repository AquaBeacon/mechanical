"""Bounded, serial STEP/assembly exports for the camera fixture revision."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, os, shutil, subprocess, sys, time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from compact_coplanar_mesh import compact
from prepare_child_horizontal_plate_frame import save
FC=Path(r'C:\Users\ryupc\AppData\Local\Programs\FreeCAD 1.0\bin\FreeCADCmd.exe')
WORK=ROOT/'assemblies/child_horizontal_plate_frame/_work/analysis/camera_hand_release_20261029'
PARTS=[('parts/child/exterior/printed/dji_osmo_action6_mount_m3','camera_mount_twist'),
 ('parts/child/exterior/printed/child_horizontal_twist_mount','child_horizontal_twist_mount_camera_receiver'),
 ('parts/parent/exterior/printed/parent_oneplate_camera_qr','parent_oneplate_camera_qr_female'),
 ('parts/child/exterior/printed/dji_osmo_action6_mount_m3','camera_hand_spacer'),
 ('parts/child/exterior/printed/dji_osmo_action6_mount_m3','camera_hand_knob'),
 ('parts/child/exterior/printed/dji_osmo_action6_mount_m3','camera_hand_knob_cap')]

def run(script,env,log,timeout=300):
    log.parent.mkdir(parents=True,exist_ok=True)
    record=dict(purpose=script,owner='camera_fixture_20261029',started_utc=datetime.now(timezone.utc).isoformat())
    with log.open('w',encoding='utf-8') as stream:
        p=subprocess.Popen([str(FC),str(ROOT/script)],cwd=ROOT,env=env,stdout=stream,stderr=subprocess.STDOUT)
        record['pid']=p.pid; save(log.with_suffix('.process.json'),record)
        try: record['exit_code']=p.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            # Popen handle identifies this task's exact process, avoiding PID reuse.
            p.terminate();p.wait(timeout=15);record['timed_out']=True
        finally:
            record['exited']=p.poll() is not None;save(log.with_suffix('.process.json'),record)
    text=log.read_text(encoding='utf-8',errors='replace')
    if record.get('timed_out') or record.get('exit_code') or 'Traceback' in text or 'Exception while processing file:' in text:
        raise RuntimeError(str(log))

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--assemblies-only',action='store_true');args=parser.parse_args()
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')
    env=os.environ.copy();env['PYTHONIOENCODING']='utf-8'
    if not args.assemblies_only:
        for i,(folder,stem) in enumerate(PARTS):
            part=ROOT/folder; work=WORK/'step'/stamp/str(i);work.mkdir(parents=True,exist_ok=False)
            src=part/(stem+'.stl')
            try: compact(src,work/'m.stl',work/'compact.json')
            except ValueError as exc:
                # Never accept a compacted mesh that fails fidelity; export raw.
                shutil.copy2(src,work/'m.stl')
                save(work/'compact.json',dict(fallback='unmodified STL',reason=str(exc)))
            save(work/'source.json',dict(path=str(src.relative_to(ROOT)),sha256=hashlib.sha256(src.read_bytes()).hexdigest()))
            env.update(STL_IN=str(work/'m.stl'),STEP_OUT=str(work/'m.step'))
            run('scad/lib/stl_to_step.py',env,work/'export.log')
            if not (work/'m.step').exists():raise RuntimeError('Missing STEP')
            shutil.copy2(work/'m.step',part/(stem+'.step'))
            print('STEP',stem,flush=True)
        job=WORK/'step'/stamp/'job.json'
        save(job,dict(parts=[folder+'/'+stem for folder,stem in PARTS]))
        env.update(ASM_ROOT=str(ROOT),CAMERA_STEP_JOB=str(job),CAMERA_STEP_REPORT=str(WORK/'step_checks.json'))
        run('spec/verify_camera_fixture_steps.py',env,WORK/'step'/stamp/'verify.log')
    for name in ['parent_exterior','child_horizontal_plate_frame']:
        a=ROOT/'assemblies'/name
        subprocess.run([sys.executable,str(ROOT/'scad/lib/asm_gen.py'),str(a/'placement.json'),str(a/(name+'_view.scad'))],check=True,timeout=60,capture_output=True)
        env.update(ASM_JSON=str(a/'placement.json'),ASM_ROOT=str(ROOT),STL_OUT=str(a/(name+'.stl')))
        run('scad/lib/asm_to_stl.py',env,a/'_work/logs/camera_hand_release_20261029_stl.log')
        if name=='parent_exterior':
            env['STEP_OUT']=str(a/(name+'.step'))
            run('scad/lib/asm_to_step.py',env,a/'_work/logs/camera_hand_release_20261029_step.log',600)
            env['STEP_IN']=env['STEP_OUT']
            run('scad/lib/verify_asm_step.py',env,a/'_work/logs/camera_hand_release_20261029_step_check.log',600)
        print('Assembly',name,flush=True)

if __name__=='__main__':main()
