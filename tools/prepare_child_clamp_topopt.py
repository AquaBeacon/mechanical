"""Prepare a reproducible topology study without altering the current assembly.

Only the installed topopt CLI solves FEA/SIMP. Raw output stays exploration-only.
Dimensions and boundary definitions come from the existing clamp study/source.
"""
from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT / 'parts/child/exterior/printed/child_wte4_suspension_clamp'
CASE = PART / '_work/analysis/topology_petg'


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    CASE.mkdir(parents=True, exist_ok=True)
    preserve = CASE / 'preserve.stl'
    command = [r'C:\Program Files\OpenSCAD\openscad.com', '-o', str(preserve),
               '-D', 'model="topopt_preserve"', str(PART / 'child_wte4_suspension_clamp.scad')]
    run = subprocess.run(command, capture_output=True, text=True)
    (CASE / 'preserve_render.log').write_text(run.stdout + run.stderr, encoding='utf-8')
    run.check_returncode()
    candidate = CASE / 'candidate.stl'
    command[2] = str(candidate)
    command[4] = 'model="topology_candidate"'
    run = subprocess.run(command, capture_output=True, text=True)
    (CASE / 'candidate_render.log').write_text(run.stdout + run.stderr, encoding='utf-8')
    run.check_returncode()
    study = json.loads((PART / '_work/analysis/study_mount.json').read_text(encoding='utf-8'))
    baseline = PART / 'child_wte4_suspension_clamp_half.stl'
    study['geometry'] = {'design_space': str(baseline),
                         'preserve': {'functional_interfaces': str(preserve)},
                         'clearance_mm': 0}
    study.pop('part', None)
    study.pop('resolution_mm', None)
    study['voxel_mm'] = 2.0
    study['safety_factor'] = 3.0
    study['design'] = {'volfrac': 0.35, 'filter_mm': 6.0,
                       'overhang': False, 'symmetry': []}
    # The measured shaft/washer faces remain exact in the final CAD/CCX study.
    # Coarse topology voxels use finite pads instead of sub-voxel hole skins.
    for name, region in study['regions'].items():
        if name.startswith(('frame_hole_', 'cap_bolt_')):
            region['r'] = 4.5
        if name.startswith('clamp_washer_'):
            region['range'][1] += 2.5
        if name.startswith('rubber_contact_'):
            region['r'] = 12.0  # topology forces remain on the preserved inner skin
    cases = []
    for case in study['cases']:
        # 4g handling from the old study -> 2g, with preload kept at 150N/bolt.
        old_name = case['name']
        if '4g' in old_name:
            case['name'] = old_name.replace('4g', '2g')
            for load in case['loads']:
                force = load['force']
                if load['region'].startswith('clamp_washer_'):
                    force[1] = (150 if 'preload' in old_name else 0) + (force[1] - (150 if 'preload' in old_name else 0))/2
                else:
                    # Pressure components are unchanged; only body weight changes.
                    if 'lateral' in old_name:
                        index = int(load['region'].rsplit('_', 1)[1])
                        ref = next(c for c in study['cases'] if c['name'] == 'preload_plus_static_1g')
                        pressure_x = next(l['force'][0] for l in ref['loads'] if l['region'] == load['region'])
                        force[0] = pressure_x + (force[0]-pressure_x)/2
                    force[2] /= 2
        cases.append(case)
    selected = ['preload_plus_static_1g', 'preload_plus_axial_2g',
                'preload_plus_lateral_2g', 'cap_pressure_plus_axial_2g']
    study['cases'] = [c for c in cases if c['name'] in selected]
    study['required_cases'] = selected
    study['_why'] = '4kg total, 3 clamps, worst clamp carries 50%: 19.6133N static, 39.2266N at 2g. Lower support credit = zero.'
    study['_boundary'] = 'Topology only: finite r4.5mm pads around four frame/clamp holes. Final CAD verification must restore exact shaft-skin surface mapping.'
    study['_limits'] += ' Topology grid 2mm cannot resolve M3 bores. No strength acceptance from this grid alone.'
    study['_not_a_part'] = 'exploration_only; rebuild as parametric CAD and verify exact holes, CCX convergence and wet/creep tests before printing.'
    study['_baseline_sha256'] = hashlib.sha256(baseline.read_bytes()).hexdigest()
    save(CASE / 'study_topology.json', study)
    # Exact-region final candidate verification, separately reproducible.
    exact = json.loads((PART / '_work/analysis/study_mount.json').read_text(encoding='utf-8'))
    exact['cases'] = cases
    exact['part'] = str(candidate)
    exact['_part_sha256'] = hashlib.sha256(candidate.read_bytes()).hexdigest()
    exact['safety_factor'] = 3.0
    exact['_why'] = study['_why']
    exact['_not_a_part'] = 'Candidate must pass independent converged verification.'
    exact['_moment'] = 'Added F*40mm couple at clamping ears retains vessel-centre eccentricity; handling 2g, not the historic 4g.'
    save(CASE / 'study_candidate.json', exact)
    print(CASE / 'study_topology.json')


if __name__ == '__main__':
    main()
