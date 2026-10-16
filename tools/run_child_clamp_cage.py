"""Execute the native cage optimisation, extraction and exact CAD finishing.

Detached-friendly driver: every stage has a log, exit code and input identity.
Does not publish raw optimisation meshes into the assembly print package.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp'
from child_clamp_case import analysis_case
CASE = analysis_case(PART)
CLI = [sys.executable, '-u', str(ROOT/'tools/clamp_bambu_material.py')]


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def run(stage, cmd, allowed=(0,)):
    status = dict(stage=stage, status='running', started_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
    save(CASE/'pipeline_status.json', status)
    print('START', stage, flush=True)
    with (CASE/(stage+'_driver.log')).open('w', encoding='utf-8') as stream:
        result = subprocess.run(cmd, cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT)
    status.update(status='finished', exit_code=result.returncode)
    save(CASE/(stage+'_status.json'), status)
    print('END', stage, result.returncode, flush=True)
    if result.returncode not in allowed:
        raise RuntimeError(f'{stage}: exit {result.returncode}; see stage driver log')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reuse-opt', action='store_true')
    parser.add_argument('--iters', type=int, default=100)
    parser.add_argument('--setup-dir', default='setup')
    parser.add_argument('--opt-dir',type=Path,help='Reuse an existing native field without copying or modifying it')
    parser.add_argument('--levels',default='0.4,0.5,0.6')
    parser.add_argument('--skip-extract-fea','--reuse-threshold-fea',dest='skip_extract_fea',action='store_true',
                        help='Geometry-only postprocessing exploration; no threshold FEA pass is implied, finished FEA still required')
    parser.add_argument('--extract-only',action='store_true')
    parser.add_argument('--reuse-extract',action='store_true')
    parser.add_argument('--close-enclosed-density-voids',action='store_true',
                        help='Direct-mesh removal of small enclosed inward shells; exterior triangles must stay identical')
    args = parser.parse_args()
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['OMP_NUM_THREADS'] = '4'
    study = CASE/'study_cage.json'
    data = json.loads(study.read_text(encoding='utf-8'))
    opt_dir=args.opt_dir.resolve() if args.opt_dir else CASE/'opt'
    if args.opt_dir and not args.reuse_opt:
        raise RuntimeError('External optimisation directory is read-only; specify --reuse-opt')
    if not args.reuse_opt:
        setup = json.loads((CASE/args.setup_dir/'study_cage_setup.json').read_text(encoding='utf-8'))
        if not setup['ok']:
            raise RuntimeError('Inspect and correct setup before optimisation')
        run('opt', CLI+['opt', str(study), '--out', str(CASE/'opt'), '--voxel', str(data['voxel_mm']), '--iters', str(args.iters)], allowed=(0,1))
    optimisation = json.loads((opt_dir/'study_cage.json').read_text(encoding='utf-8'))
    save(CASE/'optimisation_verdict.json', dict(pass_check=optimisation.get('pass'),
        termination_reason=optimisation.get('termination_reason'), checks=optimisation.get('checks')))
    # Even a failed stress check is a useful geometry exploration, clearly marked.
    # Finishing never changes that into a structural pass.
    if not args.reuse_extract:
        run('extract', CLI+['extract', str(opt_dir), '--study', str(study), '--out', str(CASE/'extract'),
            '--levels', args.levels]+(['--no-fea'] if args.skip_extract_fea else []), allowed=(0,1))
    extraction = json.loads((CASE/'extract/study_cage_extract.json').read_text(encoding='utf-8'))
    level = extraction['chosen_level']
    source = CASE/f'extract/study_cage_t{round(level*100):02d}_finish.stl'
    if not source.exists():
        raise RuntimeError('Native smoothed density extraction missing')
    from finish_child_clamp_smooth import repair_surface
    surface = CASE/'cage_density_surface.stl'
    repair = repair_surface(source, surface, CASE/'surface_repair.json')
    void_cleanup=None
    if args.close_enclosed_density_voids:
        from finish_child_clamp_smooth import close_enclosed_density_voids
        void_cleanup=close_enclosed_density_voids(surface,CASE/'density_void_cleanup.json')
    if args.extract_only:
        save(CASE/'pipeline_status.json',dict(stage='density_surface_ready',status='complete',
             note='Postprocessing exploration only; exact CAD finishing and all final validation remain required.'))
        return
    final = CASE/'finished_cage.stl'
    parameter_file = CASE/'design_parameters.json'
    parameters = json.loads(parameter_file.read_text(encoding='utf-8')) if parameter_file.exists() else {}
    defines = [arg for key,value in parameters.items() for arg in ['-D',key+'='+json.dumps(value)]]
    run('exact_interface', [r'C:\Program Files\OpenSCAD\openscad.com', '-o', str(final),
        '-D', 'model="cage"', '-D', 'cage_surface_file='+json.dumps(surface.as_posix()),
        *defines, str(PART/'child_wte4_suspension_clamp.scad')])
    from clean_stl_degenerates import clean
    clean(final, CASE/'exact_interface_degeneracy_cleanup.json')
    final_study = dict(data)
    for key in ['geometry', 'design', 'finish', 'voxel_mm']:
        final_study.pop(key, None)
    final_study['part'] = str(final)
    final_study['resolution_mm'] = 2.0
    final_study['_part_sha256'] = hashlib.sha256(final.read_bytes()).hexdigest()
    save(CASE/'study_final.json', final_study)
    keys = ['material','build_axis','raster_axis','infill','walls','safety_factor','max_deflection_mm','regions','cases']
    save(CASE/'final_provenance.json', dict(same_condition_keys=keys,
        all_equal=all(final_study[k]==data[k] for k in keys), chosen_level=level,
        chosen_reason=extraction['chosen_reason'], surface_repair=repair,
        source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        finishing_scad_sha256=hashlib.sha256((PART/'child_wte4_suspension_clamp.scad').read_bytes()).hexdigest(),
        local_finishing='Canonical SCAD restores functional interfaces after density smoothing, adds 0.3mm M3 entrance relief and the washer-access clearance recorded in design_parameters; working bores and washer seating planes are retained. Final geometry is separately reanalysed.',
        final_sha256=final_study['_part_sha256'],
        design_parameters=parameters,
        native_optimisation_dir=str(opt_dir),
        extract_fea_skipped=args.skip_extract_fea,
        enclosed_density_void_cleanup=void_cleanup,
        source='Native density-field smoothing + canonical SCAD exact interfaces; no replacement ribs'))
    run('print', CLI+['print', str(final), '--printer', 'X1C', '--keep-flat', 'Y', '--load-axis', '0,0,1',
        '--json', str(CASE/'print_checks.json'), '--png', str(PART/'_work/images/cage_print_check.png')], allowed=(0,1))
    save(CASE/'pipeline_status.json', dict(stage='finished_candidate', status='complete',
        structural_qualification='pending final independent analysis and mesh convergence'))


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        save(CASE/'pipeline_status.json', dict(status='failed', error=str(exc)))
        raise
