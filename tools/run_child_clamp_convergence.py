"""Run native mesh convergence in small case groups to fit the 16 GB GPU.

Only CLI orchestration and reporting: every native load/support/material field
is preserved. No solver or convergence criterion is implemented here.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
from copy import deepcopy
from child_clamp_case import analysis_case

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp'
CASE=analysis_case(PART)


def save(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--voxel',type=float,default=1.3)
    parser.add_argument('--group-size',type=int,choices=[1,2],default=2)
    args=parser.parse_args()
    src=CASE/'study_final.json'
    original=json.loads(src.read_text(encoding='utf-8'))
    priority=['skew_y_-1_2g','skew_x_+1_2g']
    cases=sorted(original['cases'],key=lambda c:priority.index(c['name']) if c['name'] in priority else 2)
    summary=dict(schema='body-models/topopt-batch-validation/1',
        source_study_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),
        source_stl_sha256=hashlib.sha256(Path(original['part']).read_bytes()).hexdigest(),
        reason=f'Validate all {len(cases)} cases with {args.group_size} case(s) per native invocation to bound the 16GB GPU working set.',
        voxel_mm=[2*args.voxel,args.voxel,args.voxel/2],runs=[],native_fine_cases=[],native_case_convergence={})
    for i in range(0,len(cases),args.group_size):
        group=i//args.group_size+1
        study=deepcopy(original)
        study['cases']=cases[i:i+args.group_size]
        study['required_cases']=[c['name'] for c in study['cases']]
        study['_batch_source_sha256']=summary['source_study_sha256']
        path=CASE/'fea_group_studies'/f'group_{group:02d}.json'
        out=CASE/'fea_grouped'/f'group_{group:02d}'
        save(path,study)
        out.mkdir(parents=True,exist_ok=True)
        with (out/'run.log').open('w',encoding='utf-8') as log:
            code=subprocess.run([sys.executable,'-u',str(ROOT/'tools/clamp_bambu_material.py'),
                'fea',str(path),'--out',str(out),'--voxel',str(args.voxel),'--converge','--no-png'],
                stdout=log,stderr=subprocess.STDOUT,cwd=ROOT).returncode
        row=dict(group=group,cases=study['required_cases'],exit_code=code,
                 study=path.relative_to(ROOT).as_posix(),output=out.relative_to(ROOT).as_posix())
        conv_path=out/'finished_cage_fea_convergence.json'
        fine_path=out/'finished_cage_fea.json'
        if conv_path.exists() and fine_path.exists():
            conv=json.loads(conv_path.read_text(encoding='utf-8'))
            fine=json.loads(fine_path.read_text(encoding='utf-8'))
            row['native_convergence_pass']=conv['pass']
            summary['native_fine_cases'].extend(fine['cases'])
            summary['native_case_convergence'].update(conv['cases'])
        summary['runs'].append(row)
        save(CASE/'grouped_convergence.json',summary)
        print(json.dumps(row),flush=True)
        if not (conv_path.exists() and fine_path.exists()):
            raise RuntimeError('Native convergence did not finish; see group run.log')
        failures=[c['case'] for c in fine['cases'] if any(
            ch['name'] in ['strength','stiffness'] and not ch['pass'] for ch in c['checks'])]
        # Native voxel screening can mark a worst-element warning as inspect.
        # Record the skill's absolute floor separately; never alter its verdict.
        worst_failures=[c['case'] for c in fine['cases'] if c['min_safety_factor']<1.5]
        row['worst_element_sf_at_least_1p5']=not worst_failures
        if worst_failures:
            summary['stopped_for_absolute_safety_floor']=worst_failures
            save(CASE/'grouped_convergence.json',summary)
            raise RuntimeError('Worst-element safety factor below 1.5: '+', '.join(worst_failures))
        if failures:
            summary['stopped_for_fine_geometry_failure']=failures
            save(CASE/'grouped_convergence.json',summary)
            raise RuntimeError('Fine mesh requires geometry review: '+', '.join(failures))
    summary['all_original_cases_present']=set(summary['native_case_convergence'])==set(original['required_cases'])
    summary['all_native_mesh_verdicts_pass']=all(v['verdict']['pass'] for v in summary['native_case_convergence'].values())
    summary['all_native_fine_case_checks_pass']=all(c['pass'] for c in summary['native_fine_cases'])
    summary['pass']=summary['all_original_cases_present'] and summary['all_native_mesh_verdicts_pass'] and summary['all_native_fine_case_checks_pass']
    save(CASE/'grouped_convergence.json',summary)
    return 0 if summary['pass'] else 1


if __name__=='__main__': sys.exit(main())
