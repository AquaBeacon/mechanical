"""Serial orchestration of existing geometry checks and native CCX screening.

Waits for the separate geometry/voxel/slice screen before the memory-heavy
independent solve. A successful single case is never a convergence certificate.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import time
from child_clamp_case import analysis_case

ROOT=Path(__file__).resolve().parents[1]
CASE=analysis_case(ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp')


def save(name, data):
    (CASE/name).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')


def wait_status(filename, stage):
    deadline=time.monotonic()+4*3600
    while time.monotonic()<deadline:
        path=CASE/filename
        if path.exists():
            try: value=json.loads(path.read_text(encoding='utf-8'))
            except json.JSONDecodeError:
                time.sleep(5)
                continue
            if value.get('status') in ['failed','requires_review']:
                raise RuntimeError(f'{filename}: {value}')
            if value.get('stage')==stage and value.get('status')=='complete':
                return
        time.sleep(10)
    raise RuntimeError('Timed out waiting for '+filename)


def run(stage, args, allowed=(0,)):
    save('independent_screen_status.json',dict(stage=stage,status='running'))
    with (CASE/(stage+'_orchestration.log')).open('w',encoding='utf-8') as log:
        result=subprocess.run([sys.executable,'-u',*args],cwd=ROOT,
                              stdout=log,stderr=subprocess.STDOUT)
    print(stage,result.returncode,flush=True)
    if result.returncode not in allowed:
        raise RuntimeError(f'{stage} failed: {result.returncode}')


def main():
    wait_status('pipeline_status.json','finished_candidate')
    run('analysis_remesh',['tools/prepare_child_clamp_analysis_mesh.py','--method','remesh',
        '--remesh-mm','1.5','--remesh-surface-error-mm','.005',
        '--remesh-feature-deg','75','--remesh-iterations','10','--uniform-remesh'])
    run('analysis_decimate',['tools/prepare_child_clamp_analysis_mesh.py','--method','decimate',
        '--input-surface',str(CASE/'ccx_remesh_surface.stl'),
        '--faces','220000','260000','300000','--keep-vertices'])
    run('analysis_geometry',['tools/verify_child_clamp_cage.py',
        '--stl',str(CASE/'ccx_surface_proxy.stl'),
        '--out',str(CASE/'ccx_vertex_preserved_geometry_checks.json'),
        '--print-stl',str(CASE/'ccx_vertex_preserved_print.stl'),'--require-no-closed-voids'])
    run('analysis_preflight',['tools/preflight_child_clamp_ccx_mesh.py',
        '--surface','ccx_surface_proxy','--mesh-mm','8','--algorithm','1','--minimum-mm','.2',
        '--out',str(CASE/'ccx_vertex_preserved_preflight_h8')])
    save('independent_screen_status.json',dict(stage='waiting_for_voxel_and_slice',status='waiting'))
    wait_status('validation_pipeline_status.json','geometry_fea_slice_screen_complete')
    run('candidate_hardware',['tools/verify_child_clamp_hardware.py','--candidate'])
    source=CASE/'study_ccx_surface_proxy.json'
    study=json.loads(source.read_text(encoding='utf-8'))
    name='skew_y_-1_2g'
    study['cases']=[c for c in study['cases'] if c['name']==name]
    if len(study['cases'])!=1: raise RuntimeError('Expected original skew condition')
    study['required_cases']=[name]
    study['_screen_provenance']=dict(full_study=str(source),
        sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        note='Exact original one-case subset. Not full-study or convergence qualification.')
    save('study_ccx_screen_regular.json',study)
    run('independent_solve',['tools/run_child_clamp_ccx.py','--mesh-mm','8',
        '--surface-stem','ccx_surface_proxy',
        '--geometry-checks',str(CASE/'ccx_vertex_preserved_geometry_checks.json'),
        '--study',str(CASE/'study_ccx_screen_regular.json'),
        '--out-name','ccx_vertex_screen','--algorithm','1','--minimum-mm','.2',
        '--screen-only','--voxel-fea',str(CASE/'fea/finished_cage_fea.json')],allowed=(0,1))
    summary=json.loads((CASE/'ccx_vertex_screen/ccx_summary.json').read_text(encoding='utf-8'))
    row=summary['runs'][-1]['cases'][0]
    result=dict(stage='independent_screen_complete',status='complete',
        native_strength_equilibrium_pass=row['pass'],
        max_displacement_mm=row['max_disp_mm'],
        stiffness_limit_mm=study['max_deflection_mm'],
        stiffness_pass=row['max_disp_mm']<=study['max_deflection_mm'],
        full_study_convergence_qualification=False)
    save('independent_screen_status.json',result)
    print(json.dumps(result),flush=True)


if __name__=='__main__':
    try: main()
    except Exception as exc:
        save('independent_screen_status.json',dict(status='requires_review',error=str(exc)))
        raise
