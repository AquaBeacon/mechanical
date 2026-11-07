"""Refresh existing closed/service assembly artifacts with bounded processes."""
import os,shutil,sys
from publish_parent_frame_spacers import R,ASM,FC,run
def main():
    if '--service-only' not in sys.argv:
        run(['powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-File',str(R/'build.ps1'),'-Assemblies','-NoPreview','-Paths',str(ASM)],'assembly_build',timeout=240)
    env=os.environ.copy();env.update(ASM_JSON=str(ASM/'service_placement.json'),ASM_ROOT=str(R),STL_OUT=str(ASM/'service.stl'),STEP_OUT=str(ASM/'service.step'),STEP_IN=str(ASM/'service.step'),PYTHONIOENCODING='utf-8')
    env.pop('ASM_GROUP',None)
    run([sys.executable,str(R/'scad/lib/asm_gen.py'),env['ASM_JSON'],str(ASM/'service_view.scad')],'service_view',env)
    for script in ['asm_to_stl.py','asm_to_step.py','verify_asm_step.py']:run([FC,str(R/'scad/lib'/script)],'service_'+script,env,timeout=240)
    for suffix in ['step','stl']:shutil.copyfile(ASM/('parent_hand_service.'+suffix),ASM/('closed.'+suffix))
    print('Closed/service assembly exports verified',flush=True)
if __name__=='__main__':main()
