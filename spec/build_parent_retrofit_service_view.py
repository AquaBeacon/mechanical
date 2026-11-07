"""Build the documented service pose using the existing assembly exporters."""
from pathlib import Path
import datetime,json,os,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];ASM=ROOT/'assemblies/parent_hand_service'
WORK=ASM/'_work/analysis/retrofit_20261024'
EXE=Path('C:/Users/ryupc/AppData/Local/Programs/FreeCAD 1.0/bin/freecadcmd.exe')
def main():
    env=os.environ.copy();env.update(ASM_JSON=str(ASM/'service_placement.json'),ASM_ROOT=str(ROOT),STL_OUT=str(ASM/'service.stl'),STEP_OUT=str(ASM/'service.step'),STEP_IN=str(ASM/'service.step'),PYTHONIOENCODING='utf-8')
    env.pop('ASM_GROUP',None)
    subprocess.run([sys.executable,str(ROOT/'scad/lib/asm_gen.py'),env['ASM_JSON'],str(ASM/'service_view.scad')],check=True,timeout=30)
    records=[]
    for script in ['asm_to_stl.py','asm_to_step.py','verify_asm_step.py']:
        log=ASM/'_work/logs'/('retrofit_service_'+script+'.log')
        with log.open('w',encoding='utf-8') as f:
            p=subprocess.Popen([str(EXE),str(ROOT/'scad/lib'/script)],env=env,stdout=f,stderr=subprocess.STDOUT,creationflags=0x08000000)
            row=dict(pid=p.pid,start_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),purpose='service pose '+script);records.append(row)
            (WORK/'service_build_processes.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
            try:p.wait(timeout=240)
            except subprocess.TimeoutExpired:p.terminate();p.wait(timeout=10);raise
            row.update(exit_code=p.returncode,ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat());assert p.returncode==0,log
        print(script+' PASS',flush=True)
    (WORK/'service_build_processes.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
    for suffix in ['step','stl']:shutil.copy2(ASM/('parent_hand_service.'+suffix),ASM/('closed.'+suffix))
if __name__=='__main__':main()
