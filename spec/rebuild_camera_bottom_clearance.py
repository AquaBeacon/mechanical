"""Bounded exports for the 2026-10-24 shared camera revision."""
from pathlib import Path
from datetime import datetime, timezone
import json
import os
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from compact_coplanar_mesh import compact
PART=ROOT/'parts/child/exterior/printed/dji_osmo_action6_mount_m3'
OUT=PART/'_work/analysis/rear_clearance_20261024'
FC=r'C:\Users\ryupc\AppData\Local\Programs\FreeCAD 1.0\bin\FreeCADCmd.exe'

def call(script, env, work, name):
    log=work/(name+'.log')
    with log.open('w',encoding='utf-8') as stream:
        process=subprocess.Popen([FC,str(ROOT/script)],cwd=ROOT,env=env,stdout=stream,stderr=subprocess.STDOUT)
        record=dict(pid=process.pid,start_utc=datetime.now(timezone.utc).isoformat(),purpose=name,owner='camera_bottom_clearance',command=[FC,str(script)])
        record_path=work/(name+'_process.json')
        record_path.write_text(json.dumps(record,indent=2),encoding='utf-8')
        try:
            code=process.wait(timeout=240)
        except subprocess.TimeoutExpired:
            process.terminate();process.wait(timeout=15)
            raise
        finally:
            record['exit_code']=process.poll()
            record_path.write_text(json.dumps(record,indent=2),encoding='utf-8')
    text=log.read_text(encoding='utf-8',errors='replace')
    assert code==0 and 'Traceback' not in text and 'Exception while processing file:' not in text, str(log)

def main():
    work=OUT/datetime.now(timezone.utc).strftime('export_%H%M%S')
    work.mkdir(parents=True,exist_ok=False)
    for index,stem in enumerate(['camera_mount','camera_mount_twist']):
        compact(PART/(stem+'.stl'),work/f'{index}.stl',work/f'{index}_compact.json')
        env=os.environ.copy();env.update(STL_IN=str(work/f'{index}.stl'),STEP_OUT=str(work/f'{index}.step'),PYTHONIOENCODING='utf-8')
        call('scad/lib/stl_to_step.py',env,work,f'part_{index}')
        shutil.copy2(work/f'{index}.step',PART/(stem+'.step'))
        print('STEP:',stem,flush=True)
    for name in ['parent_exterior','child_horizontal_plate_frame']:
        assembly=ROOT/'assemblies'/name
        # Use a short output filename for FreeCAD's legacy Windows STL writer.
        staged=work/'assembly.stl'
        env=os.environ.copy();env.update(ASM_JSON=str(assembly/'placement.json'),ASM_ROOT=str(ROOT),STL_OUT=str(staged),PYTHONIOENCODING='utf-8')
        call('scad/lib/asm_to_stl.py',env,work,name+'_stl')
        shutil.copy2(staged,assembly/(name+'.stl'))
        if name=='parent_exterior':
            env['STEP_OUT']=str(assembly/(name+'.step'))
            call('scad/lib/asm_to_step.py',env,work,name+'_step')
            env['STEP_IN']=env['STEP_OUT']
            call('scad/lib/verify_asm_step.py',env,work,name+'_verify')
            p=json.loads((assembly/'placement.json').read_text(encoding='utf-8'))
            p['items']=[r for r in p['items'] if r['group']!='hardware']
            filtered=work/'structure.json';filtered.write_text(json.dumps(p),encoding='utf-8')
            env.update(ASM_JSON=str(filtered),STEP_OUT=str(assembly/'parent_oneplate_structure.step'))
            call('scad/lib/asm_to_step.py',env,work,'structure_step')
        print('Assembly:',name,flush=True)

if __name__=='__main__':main()
