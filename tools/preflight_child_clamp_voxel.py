"""Check native voxel boundary-region mapping without solving or changing BCs."""
from pathlib import Path
import json
from topopt.loadcase import load_case_from_json, build_bcs
from topopt.materials import get_material
from topopt.voxel import voxelize_stl, largest_connected

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / 'parts/child/exterior/printed/child_wte4_suspension_clamp/_work/analysis'

def main():
    study = load_case_from_json(str(WORK / 'study_mount.json'))
    checks = []
    for h in (2.0, 1.0):
        grid = largest_connected(voxelize_stl(study.part_path, h=h))
        cases = []
        for case in study.cases:
            try:
                fixed, force = build_bcs(grid, case, study.regions, get_material(study.material),
                                         infill=study.infill, walls=study.walls)
                cases.append(dict(case=case.name, valid=True, fixed_dofs=int(fixed.sum())))
            except ValueError as error:
                cases.append(dict(case=case.name, valid=False, error=str(error)))
        checks.append(dict(voxel_mm=h, solid_voxels=grid.n_solid, cases=cases))
    report = dict(source=str(WORK / 'study_mount.json'), solver_run=False, checks=checks,
                  note='Native mapping only. No region inflation or change of support/load premises.')
    (WORK / 'voxel_preflight.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()
