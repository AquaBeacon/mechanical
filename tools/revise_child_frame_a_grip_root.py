"""Retain the native grip blend while removing old thin-rim boundary foil."""
from pathlib import Path
import json,os,shutil,subprocess,sys

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_exterior_structural_frame'
CASE=PART/'_work/analysis/frame_a_rim_thickness'

def main():
    os.environ.update(OMP_NUM_THREADS='4',OPENBLAS_NUM_THREADS='4',MKL_NUM_THREADS='4',PYTHONIOENCODING='utf-8')
    history=CASE/'input_history/unreinforced_grip_root'
    if not history.exists():
        history.mkdir(parents=True)
        for p in list(PART.glob('*.stl'))+[PART/'child_exterior_structural_frame.scad',PART/'spec/design_parameters.json',CASE/'study_final.json',CASE/'fine_mesh_thresholds.json']:
            shutil.copy2(p,history/p.name)
        for name in ['final_fea','final_fea_groups']:
            shutil.copytree(CASE/name,history/name)
    subprocess.run([sys.executable,'-u',str(ROOT/'tools/finish_child_frame_a_rim_boundary.py')],check=True)
    study=json.loads((CASE/'study_frame_a.json').read_text())
    for key in ['geometry','design','finish','voxel_mm']:study.pop(key,None)
    study['part']=str(PART/'child_exterior_structural_frame_full.stl')
    study['cases']=[study['cases'][2]]
    study['required_cases']=[c['name'] for c in study['cases']]
    folder=CASE/'grip_root_screen';folder.mkdir(exist_ok=True)
    (folder/'study.json').write_text(json.dumps(study,indent=2)+'\n')
    with (folder/'native.log').open('w') as log:
        r=subprocess.run([sys.executable,'-u',str(ROOT/'tools/clamp_bambu_material.py'),'fea',str(folder/'study.json'),'--out',str(folder/'results'),'--voxel','1'],stdout=log,stderr=subprocess.STDOUT)
    if r.returncode not in [0,1]:raise RuntimeError('Native grip screening failed to run')
    result=json.loads((folder/'results/child_exterior_structural_frame_full_fea.json').read_text())['cases'][0]
    print('Current grip: SF',result['min_safety_factor'],'displacement',result['max_displacement_mm'],flush=True)
    if not result['converged'] or result['min_safety_factor']<3 or result['max_displacement_mm']>2:
        raise RuntimeError('Retained grip-root blend fails fine-grid requirements')
    subprocess.run([sys.executable,'-u',str(ROOT/'tools/verify_child_frame_a_rim_groups.py')],check=True)

if __name__=='__main__':main()
