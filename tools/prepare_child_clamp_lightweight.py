"""Reuse the recorded CAD interfaces and loads for a lower material budget."""
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp'
BASE = PART/'_work/analysis/connected_cage_rubber1_v065'
CASE = PART/'_work/analysis/lightweight_epdm_v020'


def main():
    CASE.mkdir(parents=True, exist_ok=True)
    destination = CASE/'study_cage.json'
    if destination.exists():
        raise RuntimeError('Study already exists; preserve its results and provenance')
    study = json.loads((BASE/'study_cage.json').read_text(encoding='utf-8'))
    study['design']['volfrac'] = .20
    study['_why'] = ('2026-10-05 user requests less filament. Retain the original 150N/bolt '
        'provisional preload and all eleven 4kg/2g/skew cases; do not weaken loads to pass. '
        'Reduce free-cell volume budget from 0.65 to 0.20. EPDM 1mm, unknown hardness. '
        '300N was a sensitivity assumption, not a user-specified working preload.')
    study['_mass_target'] = ('Exploration target: below 1kg for TWO halves including supports; '
        'CAD target about 0.8kg total. Actual mass and slice usage must be measured.')
    study['_source_study_sha256'] = hashlib.sha256((BASE/'study_cage.json').read_bytes()).hexdigest()
    destination.write_text(json.dumps(study,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    shutil.copy2(BASE/'interface.json',CASE/'interface.json')
    record = {str(path.relative_to(ROOT)):hashlib.sha256(path.read_bytes()).hexdigest()
              for path in [BASE/'design_space.stl',BASE/'preserve.stl',BASE/'cuts.stl',
                           PART/'child_wte4_suspension_clamp.scad']}
    (CASE/'input_hashes.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print(destination)


if __name__ == '__main__':
    main()
