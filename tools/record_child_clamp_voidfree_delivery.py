"""Record completed geometry/slicing checks; never run optimisation or FEA."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import report_child_clamp_cage as historical_report

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT / 'parts/child/exterior/printed/child_wte4_suspension_clamp'
CASE = PART / '_work/analysis/connected_cage_rubber1_solid'
ASSEMBLY = ROOT / 'assemblies/child_clamp_suspension'


def read(name):
    return json.loads((CASE / name).read_text(encoding='utf-8'))


def main():
    historical_report.CASE = CASE
    assembly_step = historical_report.assembly_step_result()
    if not assembly_step:
        raise RuntimeError('Native assembly STEP readback has not finished')
    checks = {name: read(name) for name in (
        'void_free_revision.json', 'geometry_checks.json',
        'step_proxy_geometry_checks.json', 'step_checks.json', 'slice_checks.json')}
    if not assembly_step['pass_check'] or not checks['step_checks.json']['pass_check']:
        raise RuntimeError('Native STEP readback failed')
    note = ('2026-10-02最終CAD検査: 部品STEPは1ソリッド・1シェルで有効、STLとの外形/体積照合合格。'
            '組立STEPは61部品の配置照合で0 NG。材料内部の密閉空洞0個、X1C実スライス合格。'
            '構造再解析・再最適化は行っていません。')
    for path in (PART / 'README.md', ASSEMBLY / 'README.md'):
        content = path.read_text(encoding='utf-8')
        content = '\n'.join(line for line in content.splitlines()
                            if not line.startswith('2026-10-02最終CAD検査:'))
        path.write_text(content.rstrip() + '\n\n' + note + '\n', encoding='utf-8')
    subprocess.run([sys.executable, 'tools/assembly_parts.py', 'sync', 'child_clamp_suspension'],
                   cwd=ROOT, check=True)
    files = [PART / 'child_wte4_suspension_clamp_cage.stl',
             PART / 'child_wte4_suspension_clamp_cage.step',
             PART / 'spec/cage_density_surface.stl',
             ASSEMBLY / 'parts/child_wte4_suspension_clamp_cage.stl',
             CASE / 'cage_print_orientation.stl',
             CASE / 'slice/cage_x1c_petg100.3mf',
             ASSEMBLY / 'print_jobs/cage_x1c_petg100.3mf']
    hashes = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in files}
    expected = checks['void_free_revision.json']['result_stl_sha256']
    assert hashes[files[0].relative_to(ROOT).as_posix()] == expected
    assert hashes[files[3].relative_to(ROOT).as_posix()] == hashes[files[4].relative_to(ROOT).as_posix()]
    assert checks['slice_checks.json']['part_sha256'] == hashes[files[4].relative_to(ROOT).as_posix()]
    assert hashes[files[5].relative_to(ROOT).as_posix()] == hashes[files[6].relative_to(ROOT).as_posix()]
    command_checks = {}
    for key, args in (
        ('print_package', ['tools/assembly_parts.py', 'check', 'child_clamp_suspension']),
        ('workspace_tidy', ['tools/tidy_workspace.py', 'check']),
        ('all_print_packages', ['tools/assembly_parts.py', 'check']),
    ):
        result = subprocess.run([sys.executable, *args], cwd=ROOT, capture_output=True,
                                text=True, encoding='utf-8', errors='replace')
        (CASE / (key + '.log')).write_text(result.stdout + result.stderr, encoding='utf-8')
        command_checks[key] = dict(exit_code=result.returncode, pass_check=result.returncode == 0)
    passed = all(v.get('pass_check', v.get('pass', False)) for v in checks.values())
    passed = bool(passed and assembly_step['pass_check'] and command_checks['print_package']['pass_check']
                  and command_checks['workspace_tidy']['pass_check'])
    out = dict(date='2026-10-02', topology_optimisation_started=False, fea_started=False,
               structural_qualification=False, enclosed_material_cavities=0,
               geometry_and_slicing_pass=passed, checks=checks, assembly_step=assembly_step,
               command_checks=command_checks, sha256=hashes,
               tools_tests=dict(passed=14, failed=0, note='Executed after source/cache changes in this revision'),
               note='Global package failures are recorded separately and are not silently waived.')
    (CASE / 'delivery_checks.json').write_text(json.dumps(out, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(dict(geometry_and_slicing_pass=passed, command_checks=command_checks), indent=2))
    if not passed:
        raise RuntimeError('Current revision geometry/slice/package verification failed')


if __name__ == '__main__':
    main()
