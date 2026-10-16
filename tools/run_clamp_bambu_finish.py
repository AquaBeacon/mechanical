"""Run native finishing and one independent mesh after the Bambu optimiser.

This command writes only the analysis trial. Canonical adoption is a separate,
reviewed operation after geometry checks; historical outputs are preserved.
"""
from pathlib import Path
import json
import os
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp'
CASE=PART/'_work/analysis/bambu_petg_basic_v3'


def run(args,log,allowed=(0,)):
    print('START',log,flush=True)
    with (CASE/log).open('w',encoding='utf-8') as stream:
        completed=subprocess.run(args,cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT)
    print('END',log,completed.returncode,flush=True)
    if completed.returncode not in allowed:
        raise RuntimeError(f'{log}: exit {completed.returncode}')
    return completed.returncode


def main():
    summary=CASE/'opt/study_stress_smooth.json'
    while not summary.exists():
        time.sleep(10)
    opt=json.loads(summary.read_text(encoding='utf-8'))
    if not opt.get('pass'):
        raise RuntimeError('Native optimisation checks failed; retain the run for review')
    run([sys.executable,'-u','tools/finish_child_clamp_smooth.py','--case',str(CASE),'--candidate-only'],
        'finish.log')
    final=CASE/'finished_candidate.stl'
    run([sys.executable,'tools/verify_child_clamp.py','--stl',str(final),'--out',str(CASE/'geometry_checks.json'),
        '--density-g-cm3','1.25'],'geometry.log')
    run([sys.executable,'tools/plot_child_clamp_topology.py','--smooth','--stl',str(final),
        '--density-g-cm3','1.25','--image-prefix','bambu_topology'],'plot.log')
    os.environ['TOPOPT_GMSH']=str(ROOT/'tools/gmsh_clamp_delaunay.cmd')
    os.environ['OMP_NUM_THREADS']='4'
    os.environ['CCX_NPROC_EQUATION_SOLVER']='4'
    run([sys.executable,'-u','tools/clamp_bambu_material.py','ccx',str(final),'--study',str(CASE/'study_final.json'),
        '--out',str(CASE/'ccx'),'--mesh-mm','5','--map','surface'],'ccx_driver.log',allowed=(0,1))
    run([sys.executable,'tools/report_clamp_bambu.py'],'report.log')
    print('FINISHED: trial only; read report and geometry before canonical adoption',flush=True)


if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        (CASE/'pipeline_failure.json').write_text(json.dumps(dict(error=str(exc)),indent=2)+'\n',encoding='utf-8')
        raise
