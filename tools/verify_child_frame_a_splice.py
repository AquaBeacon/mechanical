"""Native single-splice surrogate analyses; does not certify bolted joints."""
from pathlib import Path
import argparse,json,os,subprocess,sys
import psutil

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_exterior_structural_frame'
CASE=PART/'_work/analysis/splice_recessed_stock'
CLI=[sys.executable,'-u',str(ROOT/'tools/clamp_bambu_material.py')]


def run(name,command,timeout=600):
    with (CASE/(name+'.log')).open('w',encoding='utf-8') as log:
        child=subprocess.Popen(command,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT)
        print(name,'owned PID',child.pid,flush=True)
        try:
            code=child.wait(timeout=timeout)
            result=dict(status='finished',exit_code=code)
        except subprocess.TimeoutExpired:
            for p in reversed(psutil.Process(child.pid).children(recursive=True)):
                try: p.kill()
                except psutil.NoSuchProcess: pass
            child.kill();child.wait()
            result=dict(status='timeout',seconds=timeout)
    (CASE/(name+'_status.json')).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(name,result,flush=True)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--reuse-fea',action='store_true');args=parser.parse_args()
    os.environ['PYTHONIOENCODING']='utf-8'
    os.environ['TOPOPT_FREECAD']=r'C:\Users\ryupc\AppData\Local\Programs\FreeCAD 1.0\bin\freecadcmd.exe'
    if not args.reuse_fea:
        run('fea',CLI+['fea',str(CASE/'study.json'),'--out',str(CASE/'fea'),'--voxel','1','--converge'])
    run('ccx',CLI+['ccx',str(PART/'child_exterior_structural_frame_splice.stl'),
                 '--study',str(CASE/'study.json'),'--out',str(CASE/'ccx'),
                 '--mesh-mm','2','--converge','--map','volume'])


if __name__=='__main__':main()
