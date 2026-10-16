"""Sequential native validation after a detached optimisation/finishing job.

Stops on geometry or coarse stiffness/strength failures and leaves every verdict
intact. Never publishes an unchecked candidate or replaces native convergence.
"""
from pathlib import Path
import argparse
import json
import os
import subprocess
import sys
import time
from child_clamp_case import analysis_case

ROOT=Path(__file__).resolve().parents[1]
CASE=analysis_case(ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp')
STATUS=CASE/'validation_pipeline_status.json'

def save(data):
    STATUS.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')

def run(name, arguments, allowed=(0,)):
    save(dict(stage=name,status='running'))
    with (CASE/(name+'_validation.log')).open('w',encoding='utf-8') as log:
        code=subprocess.run([sys.executable,'-u',*arguments],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT).returncode
    result=dict(stage=name,exit_code=code,status='finished')
    (CASE/(name+'_validation_status.json')).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result),flush=True)
    if code not in allowed: raise RuntimeError(f'{name} exited {code}')

def main():
    os.environ['PYTHONIOENCODING']='utf-8'
    os.environ.setdefault('OMP_NUM_THREADS','4')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--wait-for-finish',action='store_true')
    parser.add_argument('--convergence-voxel',type=float,default=1.0)
    parser.add_argument('--screen-voxel',type=float,default=2.0)
    parser.add_argument('--screen-only',action='store_true')
    args=parser.parse_args()
    if args.wait_for_finish:
        save(dict(stage='waiting_for_native_optimisation',status='waiting'))
        deadline=time.monotonic()+8*3600
        while time.monotonic()<deadline:
            file=CASE/'pipeline_status.json'
            if file.exists():
                try: status=json.loads(file.read_text(encoding='utf-8'))
                except json.JSONDecodeError: time.sleep(5); continue
                if status.get('status')=='failed': raise RuntimeError('Upstream optimisation/finishing failed')
                if status.get('stage')=='finished_candidate' and status.get('status')=='complete': break
            time.sleep(15)
        else: raise RuntimeError('Upstream job did not complete within 8 hours')
    run('geometry',['tools/verify_child_clamp_cage.py','--require-no-closed-voids'])
    run('coarse_fea',['tools/clamp_bambu_material.py','fea',str(CASE/'study_final.json'),
                     '--out',str(CASE/'fea'),'--voxel',str(args.screen_voxel),'--no-png'],allowed=(0,1))
    fea=json.loads((CASE/'fea/finished_cage_fea.json').read_text(encoding='utf-8'))
    failures=[row['case'] for row in fea['cases'] if row['min_safety_factor']<1.5 or any(
        check['name'] in ['strength','stiffness'] and not check['pass'] for check in row['checks'])]
    if failures: raise RuntimeError('Revise candidate after coarse failure: '+', '.join(failures))
    run('slice',['tools/slice_child_clamp_cage.py','--support','tree'])
    if args.screen_only:
        save(dict(stage='geometry_fea_slice_screen_complete',status='complete',
                  note='Screen only; convergence, independent CCX and publication remain required.'))
        return
    run('convergence',['tools/run_child_clamp_convergence.py','--group-size','1','--voxel',str(args.convergence_voxel)],allowed=(0,1))
    grouped=json.loads((CASE/'grouped_convergence.json').read_text(encoding='utf-8'))
    if not grouped.get('all_original_cases_present'):
        raise RuntimeError('Fine native validation stopped before all required cases completed; inspect grouped_convergence.json')
    save(dict(stage='screening_complete',status='complete',
              note='Inspect native convergence and slice mass; independent CCX and publication still required.'))

if __name__=='__main__':
    try: main()
    except Exception as exc:
        save(dict(status='requires_review',error=str(exc)))
        raise
