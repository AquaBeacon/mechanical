"""Native convergence analyses grouped by support set to limit GPU residency.

Every original case is solved by topopt. This only authors subgroup studies
and assembles their native JSON reports; no FEM computation is implemented.
"""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_exterior_structural_frame'
CASE=PART/'_work/analysis/frame_a_rim_thickness'
CLI=[sys.executable,'-u',str(ROOT/'tools/clamp_bambu_material.py')]
STEM='child_exterior_structural_frame_full'


def save(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')


def main():
    os.environ['OMP_NUM_THREADS']='4';os.environ['OPENBLAS_NUM_THREADS']='4'
    os.environ['MKL_NUM_THREADS']='4';os.environ['PYTHONIOENCODING']='utf-8'
    study=json.loads((CASE/'study_frame_a.json').read_text())
    for k in ['geometry','design','finish','voxel_mm']:study.pop(k,None)
    part=PART/(STEM+'.stl');study.update(part=str(part),_part_sha256=hashlib.sha256(part.read_bytes()).hexdigest())
    prior=CASE/'final_fea'
    history=CASE/'input_history/crop_boundary_foil/final_fea'
    if prior.exists() and not history.exists():shutil.copytree(prior,history)
    save(CASE/'study_final.json',study)
    results=[];convergences=[];statuses=[];plots={}
    groups=[('handle',study['cases'][:1]+study['cases'][2:4]),('standing',study['cases'][1:2]),('clamps',study['cases'][4:])]
    for name,cases in groups:
        folder=CASE/'final_fea_groups'/name;folder.mkdir(parents=True,exist_ok=True)
        sub=dict(study,cases=cases,required_cases=[c['name'] for c in cases],_full_model_case_names=[c['name'] for c in study['cases']])
        save(folder/'study.json',sub)
        with (folder/'native.log').open('w') as log:
            result=subprocess.run(CLI+['fea',str(folder/'study.json'),'--out',str(folder/'results'),'--voxel','2','--converge'],stdout=log,stderr=subprocess.STDOUT)
        statuses.append(dict(group=name,exit_code=result.returncode));print(name,result.returncode,flush=True)
        if result.returncode not in [0,1]:raise RuntimeError(f'Native subgroup {name} did not produce a valid analysis')
        results.append(json.loads((folder/'results'/(STEM+'_fea.json')).read_text()))
        convergences.append(json.loads((folder/'results'/(STEM+'_fea_convergence.json')).read_text()))
        for index,c in enumerate(cases,1):plots[c['name']]=folder/'results'/f'{STEM}_fea_{index}.png'
    by_case={c['case']:c for r in results for c in r['cases']}
    assert set(by_case)==set(c['name'] for c in study['cases'])
    merged=dict(results[0],cases=[by_case[c['name']] for c in study['cases']])
    merged['pass']=all(r['pass'] for r in results)
    conv=dict(convergences[0],cases={k:v for c in convergences for k,v in c['cases'].items()})
    conv['pass']=all(c['pass'] for c in convergences)
    conv['note']='All seven original cases, native 4/2/1mm studies run separately by support group. No case omitted.'
    conv['governing_case']=min(by_case,key=lambda k:by_case[k]['min_safety_factor'])
    save(prior/(STEM+'_fea.json'),merged);save(prior/(STEM+'_fea_convergence.json'),conv)
    for index,c in enumerate(study['cases'],1):
        shutil.copy2(plots[c['name']],prior/f'{STEM}_fea_{index}.png')
    save(prior/'manifest.json',dict(schema='local-native-fea-aggregation/1',
         method='Unmodified native reports in three support groups; seven cases assembled in original order.',
         part_sha256=study['_part_sha256'],study_sha256=hashlib.sha256((CASE/'study_final.json').read_bytes()).hexdigest(),
         native_manifests=[str(CASE/'final_fea_groups'/n/'results/manifest.json') for n,_ in groups],
         groups=statuses,case_names=[c['name'] for c in study['cases']]))
    strict=all(c['min_safety_factor']>=3 and c['max_displacement_mm']<=2 for c in merged['cases'])
    save(CASE/'fine_mesh_thresholds.json',dict(pass_fine_thresholds=strict,convergence_pass=conv['pass'],part_sha256=study['_part_sha256'],native_groups=statuses,note='Passing fine-grid thresholds does not qualify convergence, material calibration or split joints.'))
    if not strict:raise RuntimeError('Current finished rim failed fine-grid thresholds')


if __name__=='__main__':main()
