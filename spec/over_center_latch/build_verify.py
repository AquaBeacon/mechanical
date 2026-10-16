"""Regenerate, build, validate and package the current latch. No legacy checks."""
from pathlib import Path
import subprocess,os,argparse
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'parts/common/jigs/over_center_latch';ASM=ROOT/'assemblies/over_center_latch'
FC=r'C:\Users\ryupc\AppData\Local\Programs\FreeCAD 1.0\bin\freecadcmd.exe'
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--existing-stl',action='store_true',help='Only for already regenerated and checked current source meshes');args=parser.parse_args()
    logs=P/'_work/logs';logs.mkdir(parents=True,exist_ok=True)
    def run(cmd,name,env=None):
        with (logs/(name+'.log')).open('w',encoding='utf-8') as f:
            r=subprocess.run([str(x) for x in cmd],cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT)
        if r.returncode:raise RuntimeError(f'{name}: exit {r.returncode}; see {logs/(name+".log")}')
        print('PASS',name,flush=True)
    run(['python',ROOT/'spec/over_center_latch/generate.py'],'generate')
    if not args.existing_stl:
        run(['powershell','-NoProfile','-ExecutionPolicy','Bypass','-File',ROOT/'build.ps1','-Paths',P,'-NoPreview'],'production_build')
    run(['python',ROOT/'spec/over_center_latch/dji_verify.py'],'verify_motion_interfaces')
    run(['python',ROOT/'spec/over_center_latch/clamp_loads.py'],'clamp_loads')
    run(['powershell','-NoProfile','-ExecutionPolicy','Bypass','-File',ROOT/'build.ps1','-Assemblies','-Paths',ASM],'assembly_build')
    env=os.environ.copy();env.update(ASM_ROOT=str(ROOT),ASM_JSON=str(ASM/'placement.json'),STEP_OUT=str(ASM/'over_center_latch.step'))
    run([FC,ROOT/'spec/over_center_latch/verify_step.py'],'verify_step',env)
    log=(logs/'verify_step.log').read_text(encoding='utf-8',errors='replace')
    if 'PASS: current STEP' not in log:raise RuntimeError('FreeCAD did not finish STEP validation')
    run(['python',ROOT/'tools/tidy_workspace.py','apply'],'tidy')
    run(['python',ROOT/'tools/assembly_parts.py','sync','over_center_latch'],'sync')
    print('BUILD AND CAD VERIFICATION COMPLETE',flush=True)
if __name__=='__main__':main()
