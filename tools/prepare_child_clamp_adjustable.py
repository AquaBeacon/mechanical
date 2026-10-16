"""Prepare native FEA/topopt inputs for the EPDM clamp preload envelope.

This only transforms recorded load inputs; native topopt performs all analysis.
The preload endpoints are sensitivity assumptions, not tightening instructions.
"""
from copy import deepcopy
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT / 'parts/child/exterior/printed/child_wte4_suspension_clamp'
CASE = PART / '_work/analysis/epdm_adjustable_20261005'
PREVIOUS = PART / '_work/analysis/connected_cage_rubber1_v065'


def save(name, data):
    (CASE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def sensitivity(original):
    study = deepcopy(original)
    preload = {item['region']: item['force'] for item in original['cases'][0]['loads']}
    study['cases'] = []
    for endpoint in (75, 300):
        for previous in original['cases']:
            case = deepcopy(previous)
            case['name'] = f"{previous['name']}_preload{endpoint}N"
            for load in case['loads']:
                load['force'] = [value + (endpoint / 150 - 1) * base
                                 for value, base in zip(load['force'], preload[load['region']])]
            study['cases'].append(case)
    study['required_cases'] = [case['name'] for case in study['cases']]
    study['_why'] = ('User specifies 1mm EPDM, unknown hardness, adjustable stronger tightening; '
                     '4kg total assumed. 75/300N per bolt are sensitivity endpoints around the '
                     'previous provisional 150N, NOT validated torque/preload limits.')
    study['_limits'] += ' EPDM stiffness, friction, acrylic contact stress and actual tightening torque remain unmodelled.'
    study['_rope'] = 'Existing 10.5mm hole retained provisionally; rope diameter not supplied.'
    return study


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--study',type=Path,help='Use an already-authored finished-part study, preserving its CAD/regions')
    parser.add_argument('--out',type=Path,help='New sensitivity study JSON, outside the FEA output directory')
    args=parser.parse_args()
    if bool(args.study)!=bool(args.out):
        parser.error('--study and --out must be used together')
    if args.study:
        if args.out.exists():
            raise RuntimeError('Preserve existing study; choose a new output path')
        original=json.loads(args.study.read_text(encoding='utf-8'))
        study=sensitivity(original)
        study['_sensitivity_source_sha256']=hashlib.sha256(args.study.read_bytes()).hexdigest()
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(json.dumps(study,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(args.out)
        return
    CASE.mkdir(parents=True, exist_ok=True)
    original = json.loads((PREVIOUS / 'study_cage.json').read_text(encoding='utf-8'))
    study=sensitivity(original)
    study['design']['volfrac'] = .8
    save('study_cage.json', study)
    for name, mesh in [('current', PART / 'child_wte4_suspension_clamp_cage.stl'),
                       ('full_space', Path(study['geometry']['design_space']))]:
        fea = deepcopy(study)
        for key in ('geometry', 'design', 'finish', 'voxel_mm'):
            fea.pop(key, None)
        fea['part'] = str(mesh)
        fea['resolution_mm'] = 2.0
        fea['_part_sha256'] = hashlib.sha256(mesh.read_bytes()).hexdigest()
        save(f'study_{name}.json', fea)
    save('input_record.json', dict(rubber='EPDM', free_thickness_mm=1,
         hardness='unknown (user confirmed)', total_mass_kg_assumed=4,
         bolt_preload_sensitivity_N=[75, 300], allowed_torque_Nm=None,
         source_study=str(PREVIOUS / 'study_cage.json'),
         source_study_sha256=hashlib.sha256((PREVIOUS / 'study_cage.json').read_bytes()).hexdigest(),
         status='analysis preparation; no new design released'))
    print(CASE)


if __name__ == '__main__':
    main()
