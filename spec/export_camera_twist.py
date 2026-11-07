"""Use the existing verified STL->STEP and placement export CLI contracts."""
from pathlib import Path
from datetime import datetime, timezone
import json, os, shutil, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from compact_coplanar_mesh import compact
from prepare_child_horizontal_plate_frame import call, save
FC=r'C:\Users\ryupc\AppData\Local\Programs\FreeCAD 1.0\bin\FreeCADCmd.exe'
PARTS=[('parts/child/exterior/printed/dji_osmo_action6_mount_m3','camera_mount'),
       ('parts/child/exterior/printed/dji_osmo_action6_mount_m3','camera_mount_twist'),
       ('parts/child/exterior/printed/child_horizontal_twist_mount','child_horizontal_twist_mount_camera_receiver')]

def fc(script,env,log):
    result=subprocess.run([FC,str(ROOT/script)],cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace')
    log.parent.mkdir(parents=True,exist_ok=True);log.write_text(result.stdout+result.stderr,encoding='utf-8')
    output=result.stdout+result.stderr
    if result.returncode or 'Traceback' in output or 'Exception while processing file:' in output:
        raise RuntimeError('FreeCAD failed: '+str(log))

def main():
    os.chdir(ROOT)
    run_id=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    for index,(folder,stem) in enumerate(PARTS):
        # FreeCAD's Windows mesh reader has a legacy path-length limit. Keep
        # the isolated run paths short even when the canonical stem is long.
        part=ROOT/folder;work=part/'_work/analysis/camera_twist_step'/run_id/str(index);work.mkdir(parents=True,exist_ok=False)
        save(work/'source.json',dict(part=folder,stem=stem))
        candidate=work/'mesh.stl'
        compact(part/(stem+'.stl'),candidate,work/'coplanar_report.json')
        env=os.environ.copy();env.update(STL_IN=str(candidate),STEP_OUT=str(work/'model.step'),PYTHONIOENCODING='utf-8')
        fc('scad/lib/stl_to_step.py',env,work/'export.log')
        assert (work/'model.step').is_file()
        shutil.copy2(work/'model.step',part/(stem+'.step'))
        print('STEP exported',stem,flush=True)
    for name in ['parent_exterior','child_horizontal_plate_frame']:
        folder=ROOT/'assemblies'/name
        env=os.environ.copy();env.update(ASM_JSON=str(folder/'placement.json'),ASM_ROOT=str(ROOT),STL_OUT=str(folder/(name+'.stl')),PYTHONIOENCODING='utf-8')
        fc('scad/lib/asm_to_stl.py',env,folder/'_work/logs/camera_twist_assembly_stl.log')
        if name=='parent_exterior':
            env['STEP_OUT']=str(folder/(name+'.step'))
            fc('scad/lib/asm_to_step.py',env,folder/'_work/logs/camera_twist_assembly_step.log')
            env['STEP_IN']=env['STEP_OUT']
            fc('scad/lib/verify_asm_step.py',env,folder/'_work/logs/camera_twist_assembly_step_check.log')
    env=os.environ.copy();env.update(PARENT_REVISION='support_reduction',PYTHONIOENCODING='utf-8')
    fc('spec/verify_parent_exterior_qr_steps.py',env,ROOT/'assemblies/parent_exterior/_work/logs/camera_twist_part_step_check.log')
    print('Current assembly STL exports and parent STEP placement/parts verified.',flush=True)

if __name__=='__main__':main()
