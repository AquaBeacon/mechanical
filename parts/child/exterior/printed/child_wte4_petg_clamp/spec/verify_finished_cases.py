"""Run unchanged native topopt CCX one case per process to bound FRD memory.

All solving, meshing, judgement and convergence use the installed topopt CLI.
The only cache is an identical native Gmsh mesh keyed by shell content/options.
No FEA or convergence criterion is implemented here.
"""
from pathlib import Path
import argparse, gc, hashlib, json, re, shutil, subprocess, sys

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source',type=Path,required=True)
    ap.add_argument('--study',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--mesh-mm',type=float,default=6)
    ap.add_argument('--max-nodes',type=int,default=400000)
    ap.add_argument('--only',nargs='*')
    ap.add_argument('--worker',action='store_true')
    args=ap.parse_args()
    if args.worker:
        from topopt import ccx
        from topopt.cli import ccx as native
        original=ccx.run_gmsh
        cache=args.out.parent/'mesh_cache';cache.mkdir(exist_ok=True)
        def mesher(geo,out,**kw):
            txt=Path(geo).read_text()
            shell=Path(re.search(r'Merge "([^"]+)"',txt)[1])
            normalized=re.sub(r'Merge "[^"]+";', 'Merge "SHELL";',txt)
            key=hashlib.sha256((sha(shell)+normalized).encode()).hexdigest()
            cached=cache/(key+'.inp')
            if cached.exists():
                shutil.copyfile(cached,out)
            else:
                original(geo,out,**kw)
                shutil.copyfile(out,cached)
            # Count the native mesh nodes before native parser/factorization.
            count=0;nodes=False
            with Path(out).open() as f:
                for line in f:
                    if line.startswith('*'):
                        nodes=line.upper().startswith('*NODE')
                    elif nodes and line.strip(): count+=1
            print(f'Native mesh budget: {count} / {args.max_nodes} nodes',flush=True)
            if count>args.max_nodes:
                raise RuntimeError('Native mesh exceeded the explicit memory budget; strength UNKNOWN')
            return out
        ccx.run_gmsh=mesher
        raise SystemExit(native.main([str(args.source),'--study',str(args.study),
            '--out',str(args.out),'--mesh-mm',str(args.mesh_mm),'--converge']))
    args.out.mkdir(parents=True,exist_ok=False)
    study=json.loads(args.study.read_text(encoding='utf-8'))
    cases=study['cases']
    if args.only: cases=[c for c in cases if c['name'] in args.only]
    order=['one_station_transfer_X_2g','assumed_preload_150N_per_bolt']
    cases.sort(key=lambda c:order.index(c['name']) if c['name'] in order else 2)
    summary=dict(status='exploration_only',source=str(args.source.resolve()),
        source_sha256=sha(args.source),study=str(args.study.resolve()),study_sha256=sha(args.study),
        method='Native CCX CLI, sequential single-case processes, native boundary refinement and native three-mesh convergence; identical native mesh cache only',
        required_cases=study['required_cases'],selected_cases=[c['name'] for c in cases],cases=[])
    for case in cases:
        folder=args.out/case['name'];folder.mkdir()
        one=dict(study);one['cases']=[case];one['required_cases']=[case['name']]
        path=args.out/(case['name']+'.study.json');path.write_text(json.dumps(one,indent=2)+'\n',encoding='utf-8')
        command=[sys.executable,'-u',str(Path(__file__).resolve()),'--worker',
            '--source',str(args.source),'--study',str(path),'--out',str(folder),
            '--mesh-mm',str(args.mesh_mm),'--max-nodes',str(args.max_nodes)]
        print('Starting native CCX:',case['name'],flush=True)
        with (folder/'native.log').open('w',encoding='utf-8') as log:
            run=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT)
        result=folder/'ccx_summary.json'
        row=dict(case=case['name'],exit_code=run.returncode,native_summary=str(result))
        if result.exists():
            native_result=json.loads(result.read_text());row['pass']=run.returncode==0
            row['mesh_convergence']=native_result.get('mesh_convergence')
            row['runs']=[dict(target_mm=r['mesh_target_mm'],nodes=r['nodes'],pass_=r.get('pass'),
                cases=r.get('cases'),mesh_quality=r.get('mesh_quality')) for r in native_result['runs']]
        else:
            row['pass']=None;row['status']='UNKNOWN';row['log_tail']=(folder/'native.log').read_text()[-2500:]
        summary['cases'].append(row)
        summary['pass']=len(summary['cases'])==len(summary['required_cases']) and all(r.get('pass') is True for r in summary['cases'])
        (args.out/'verification_summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({k:row.get(k) for k in ['case','exit_code','pass','status','log_tail']}),flush=True)
        if row['pass'] is None: break
    raise SystemExit(0 if summary.get('pass') else 1)

if __name__=='__main__':main()
