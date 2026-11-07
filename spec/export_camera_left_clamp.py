"""Existing FreeCAD CLI exports, isolated logs and short Windows filenames."""
from pathlib import Path
from datetime import datetime,timezone
import os,json,shutil,sys
from rebuild_camera_bottom_clearance import call,compact,ROOT,PART,FC

def main():
    work=PART/'_work/analysis/clamp_clearance_20261026'/datetime.now(timezone.utc).strftime('export_%H%M%S')
    work.mkdir(parents=True,exist_ok=False)
    for i,stem in enumerate(['camera_mount','camera_mount_twist','camera_front_clamp','camera_case_41mm']):
        compact(PART/(stem+'.stl'),work/f'{i}.stl',work/f'{i}_compact.json')
        env=os.environ.copy();env.update(STL_IN=str(work/f'{i}.stl'),STEP_OUT=str(work/f'{i}.step'),PYTHONIOENCODING='utf-8')
        call('scad/lib/stl_to_step.py',env,work,f'part_{i}')
        shutil.copy2(work/f'{i}.step',PART/(stem+'.step'))
        print('STEP',stem,flush=True)
    for name in ['parent_exterior','child_horizontal_plate_frame']:
        a=ROOT/'assemblies'/name;env=os.environ.copy()
        env.update(ASM_JSON=str(a/'placement.json'),ASM_ROOT=str(ROOT),STL_OUT=str(work/'assembly.stl'),PYTHONIOENCODING='utf-8')
        call('scad/lib/asm_to_stl.py',env,work,name+'_stl');shutil.copy2(work/'assembly.stl',a/(name+'.stl'))
        if name=='parent_exterior':
            env['STEP_OUT']=str(work/'assembly.step')
            call('scad/lib/asm_to_step.py',env,work,'parent_step');shutil.copy2(work/'assembly.step',a/(name+'.step'))
            env['STEP_IN']=str(a/(name+'.step'))
            call('scad/lib/verify_asm_step.py',env,work,'parent_placement_check')
            p=json.loads((a/'placement.json').read_text(encoding='utf-8'));p['items']=[r for r in p['items'] if r['group'] not in ['hardware','fasteners']]
            (work/'structure.json').write_text(json.dumps(p),encoding='utf-8')
            env.update(ASM_JSON=str(work/'structure.json'),STEP_OUT=str(a/'parent_oneplate_structure.step'))
            call('scad/lib/asm_to_step.py',env,work,'parent_structure')
        print('Assembly',name,flush=True)
    call('spec/verify_camera_left_clamp_steps.py',os.environ.copy(),work,'step_checks')

if __name__=='__main__':main()
