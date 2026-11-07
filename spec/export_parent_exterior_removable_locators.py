"""Export Rev.7 through the existing STL/STEP/assembly CLI contracts."""
from pathlib import Path
from datetime import datetime,timezone
import os,shutil
from export_camera_twist import fc
from compact_coplanar_mesh import compact

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'assemblies/parent_exterior'
JOB='removable_locators_20261022'

def main():
    run=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')
    parts=[('parent_oneplate_frame','parent_oneplate_frame')]+[
        ('parent_oneplate_box_locator','parent_oneplate_box_locator_'+v)
        for v in ('side_left','side_right','end_fixed','end_push')]
    for i,(folder,stem) in enumerate(parts):
        part=ROOT/'parts/parent/exterior/printed'/folder
        work=part/'_work/analysis'/JOB/run/str(i);work.mkdir(parents=True,exist_ok=False)
        source=part/(stem+'.stl')
        if i:
            candidate=work/'mesh.stl';compact(source,candidate,work/'compact.json')
        else:candidate=source
        env=os.environ.copy();env.update(STL_IN=str(candidate),STEP_OUT=str(work/'model.step'),PYTHONIOENCODING='utf-8')
        fc('scad/lib/stl_to_step.py',env,work/'export.log')
        assert (work/'model.step').exists()
        shutil.copy2(work/'model.step',part/(stem+'.step'))
        print('STEP',stem,flush=True)
    env=os.environ.copy();env.update(ASM_JSON=str(A/'placement.json'),ASM_ROOT=str(ROOT),
                                    STL_OUT=str(A/'parent_exterior.stl'),STEP_OUT=str(A/'parent_exterior.step'),PYTHONIOENCODING='utf-8')
    fc('scad/lib/asm_to_stl.py',env,A/'_work/logs'/f'{JOB}_assembly_stl.log')
    fc('scad/lib/asm_to_step.py',env,A/'_work/logs'/f'{JOB}_assembly_step.log')
    env['STEP_IN']=env['STEP_OUT']
    fc('scad/lib/verify_asm_step.py',env,A/'_work/logs'/f'{JOB}_assembly_check.log')
    env['PARENT_REVISION']=JOB
    fc('spec/verify_parent_exterior_qr_steps.py',env,A/'_work/logs'/f'{JOB}_part_step_check.log')
    print('STEP / assembly verification completed',flush=True)

if __name__=='__main__':main()
