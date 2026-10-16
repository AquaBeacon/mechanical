"""Record this cage's delivery checks without upgrading its lifting verdict.

Requires completed native STEP verification. Shape/print preparation and
structural qualification have separate verdicts; native failures are retained.
"""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp'
ASSEMBLY = ROOT/'assemblies/child_clamp_suspension'
CASE = PART/'_work/analysis/connected_cage_rubber1_v065'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(name, arguments):
    log = CASE/(name+'_final.log')
    with log.open('w',encoding='utf-8') as stream:
        result = subprocess.run([sys.executable,*arguments],cwd=ROOT,
            env=dict(os.environ,PYTHONIOENCODING='utf-8'),
            stdout=stream,stderr=subprocess.STDOUT)
    print(f'{name}: exit {result.returncode}; {log.relative_to(ROOT)}',flush=True)
    return dict(exit_code=result.returncode,log=log.relative_to(ROOT).as_posix())


def main():
    report = run('report',['tools/report_child_clamp_cage.py'])
    if report['exit_code']:
        raise RuntimeError('Documentation generation failed')
    assembly_step = read(CASE/'assembly_step_checks.json')
    if not assembly_step['pass_check']:
        raise RuntimeError('Native assembly STEP placement verification incomplete/failed')
    commands = {}
    commands['sync'] = run('sync',['tools/assembly_parts.py','sync','child_clamp_suspension'])
    if commands['sync']['exit_code']:
        raise RuntimeError('Print package sync failed')
    commands['assembly_print_package'] = run('target_package',['tools/assembly_parts.py','check','child_clamp_suspension'])
    commands['global_print_packages'] = run('global_packages',['tools/assembly_parts.py','check'])
    commands['workspace_tidy'] = run('tidy',['tools/tidy_workspace.py','check'])
    commands['tool_tests'] = run('tests',['-m','unittest','discover','-s','tools/tests'])
    native_files = [CASE/name for name in ['opt/study_cage.json','extract/study_cage_extract.json',
        'fea/finished_cage_fea.json','print_checks.json','slice_checks.json']]
    commands['native_output_schemas'] = run('schemas',['tools/clamp_bambu_material.py','validate',
        *[str(path) for path in native_files]])
    geometry = read(CASE/'geometry_checks.json')
    slicing = read(CASE/'slice_checks.json')
    fea = read(CASE/'fea/finished_cage_fea.json')
    fea_manifest = read(CASE/'fea/manifest.json')
    final_study = read(CASE/'study_final.json')
    independent = read(CASE/'independent_analysis_status.json')
    step = read(CASE/'step_checks.json')
    proxy = read(CASE/'step_proxy_geometry_checks.json')
    manifest = read(ASSEMBLY/'parts/manifest.json')
    job = read(ASSEMBLY/'print_jobs/cage_x1c_petg100.json')
    print_part = manifest['parts'][0]
    source_hash = digest(PART/'child_wte4_suspension_clamp_cage.stl')
    print_hash = digest(ASSEMBLY/'parts'/print_part['file'])
    identities = dict(
        design_stl=source_hash==geometry['sha256']==final_study['_part_sha256']==independent['part_sha256'],
        native_fea_study=digest(CASE/'study_final.json')==fea_manifest['inputs'][0]['sha256'],
        print_stl=print_hash==slicing['part_sha256']==job['sliced_print_stl_sha256']==print_part['sha256'],
        sliced_project=digest(ASSEMBLY/'print_jobs'/job['project'])==job['project_sha256']==digest(Path(slicing['project_3mf'])),
        quantity=print_part['quantity']==2 and len(manifest['parts'])==1,
        source_cad=digest(PART/'child_wte4_suspension_clamp.scad')==read(CASE/'final_provenance.json')['finishing_scad_sha256'])
    shape_print_pass = bool(all(identities.values()) and geometry['pass'] and slicing['pass_check']
        and step['pass_check'] and proxy['pass'] and assembly_step['pass_check']
        and all(value['exit_code']==0 for key,value in commands.items() if key!='global_print_packages'))
    structural_pass = bool(fea['pass'] and independent.get('pass_check',False))
    if manifest['release_status']!='exploration_only' and not structural_pass:
        raise RuntimeError('A failed structural check must not be promoted to a production part')
    result = dict(schema='body-models/cage-validation/1',release_status=manifest['release_status'],
        shape_print_preparation_pass=shape_print_pass,lifting_qualification_pass=structural_pass,
        input_identity_checks=identities,source_stl_sha256=source_hash,print_stl_sha256=print_hash,
        checks=commands,native_finished_fea_pass=fea['pass'],independent_analysis_completed=independent['completed'],
        assembly_step=assembly_step,
        global_check_note='Global check may report another assembly being edited; consult global_packages_final.log. The target package has its own check.',
        note='Digital geometry and slicing checks only. Native stiffness failure and incomplete independent convergence remain; no physical print/lifting certification.')
    (CASE/'delivery_checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2),flush=True)
    return 0 if shape_print_pass else 1


if __name__=='__main__':
    sys.exit(main())
