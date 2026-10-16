"""Record reproducible strength screening; never turn a solver FAIL into PASS."""
from pathlib import Path
import argparse,json,subprocess,sys,time

ROOT=Path(__file__).resolve().parents[2]
P=ROOT/'parts/common/jigs/over_center_latch'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--case',required=True)
    ap.add_argument('--voxel',type=float,default=.4)
    ap.add_argument('--parts',nargs='+',default=['bail','lever','base','keeper'])
    ap.add_argument('--ccx',action='store_true');a=ap.parse_args()
    case=P/'_work/analysis'/a.case;studies=case/'studies'
    subprocess.run([sys.executable,Path(__file__).with_name('clamp_studies.py'),'--case',a.case],cwd=ROOT,check=True)
    status_path=case/('ccx_status.json' if a.ccx else 'fea_status.json')
    status=json.loads(status_path.read_text(encoding='utf-8')) if status_path.exists() else {};ok=True
    for name in a.parts:
        out=case/(name+('_ccx' if a.ccx else '_convergence'))
        if out.exists():raise FileExistsError(f'Preserve previous output: {out}')
        out.mkdir(parents=True)
        cmd=[sys.executable,Path(__file__).with_name('petg_basic_ccx.py' if a.ccx else 'petg_basic_fea.py')]
        if a.ccx:
            cmd += [studies/(name+'_closed.stl'),'--study',studies/(name+'_study.json'),'--mesh-mm',str(a.voxel),'--quiet']
        else:cmd += [studies/(name+'_study.json'),'--voxel',str(a.voxel),'--no-png']
        cmd += ['--out',out,'--converge'];cmd=[str(x) for x in cmd]
        start=time.monotonic();print('START',name,flush=True)
        with (out/'command.log').open('w',encoding='utf-8') as f:
            r=subprocess.run(cmd,cwd=ROOT,stdout=f,stderr=subprocess.STDOUT)
        status[name]=dict(returncode=r.returncode,seconds=round(time.monotonic()-start,1),command=cmd)
        status_path.write_text(json.dumps(status,indent=2)+'\n',encoding='utf-8')
        print('END',name,r.returncode,flush=True);ok &= r.returncode==0
    return 0 if ok else 1

if __name__=='__main__':sys.exit(main())
