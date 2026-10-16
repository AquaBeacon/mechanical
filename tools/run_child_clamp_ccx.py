"""Run native independent CCX on the checked faceted surface; record even tool failure."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
import time
from child_clamp_case import analysis_case

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp'
CASE=analysis_case(PART)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mesh-mm',type=float,default=8)
    parser.add_argument('--voxel-fea',type=Path,default=CASE/'voxel_comparison.json',
        help='Existing native comparison output; final fine comparison is collected separately.')
    parser.add_argument('--surface-stem',default='ccx_manifold_surface')
    parser.add_argument('--geometry-checks',type=Path,default=CASE/'ccx_surface_geometry_checks.json')
    parser.add_argument('--study',type=Path)
    parser.add_argument('--out-name',default='ccx')
    parser.add_argument('--algorithm',type=int,choices=[1,10],default=1)
    parser.add_argument('--minimum-mm',type=float)
    parser.add_argument('--screen-only',action='store_true',help='One mesh only; never a convergence qualification')
    args=parser.parse_args()
    if Path(args.out_name).name!=args.out_name or Path(args.surface_stem).name!=args.surface_stem:
        raise RuntimeError('Use case-local output/stem names')
    checked=json.loads(args.geometry_checks.read_text(encoding='utf-8'))
    surface=CASE/(args.surface_stem+'.stl')
    study=args.study or CASE/('study_'+args.surface_stem+'.json')
    comparison=args.voxel_fea
    if not checked['pass'] or checked['sha256']!=hashlib.sha256(surface.read_bytes()).hexdigest():
        raise RuntimeError('The analysis surface must pass its own interface verification')
    if (CASE/args.out_name).exists(): raise RuntimeError('Preserve the existing CCX run')
    command=[sys.executable,'-u',str(ROOT/'tools/clamp_bambu_material.py'),'ccx',str(surface),
        '--study',str(study),'--out',str(CASE/args.out_name),'--mesh-mm',str(args.mesh_mm),
        *([] if args.screen_only else ['--converge']),
        '--map','volume','--gmsh-algorithm',str(args.algorithm),'--gmsh-straight-second-order',
        '--voxel-fea',str(comparison)]
    if args.minimum_mm is not None:
        command += ['--gmsh-min-mm',str(args.minimum_mm)]
    record=dict(command=command,mesh_targets_mm=([args.mesh_mm] if args.screen_only else [2*args.mesh_mm,args.mesh_mm,args.mesh_mm/2]),
        screen_only=args.screen_only,
        case_names=json.loads(study.read_text(encoding='utf-8'))['required_cases'],
        note='C3D10 retained; midside nodes interpolate straight faceted STL edges (Mesh.SecondOrderLinear=1). Native surface refinement remains enabled. All cases in the supplied study are retained; a screen is not a full-study or convergence qualification.',
        reference='https://gmsh.info/doc/texinfo/',
        input_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [surface,study,comparison]})
    started=time.monotonic()
    with (CASE/(args.out_name+'_run.log')).open('w',encoding='utf-8') as log:
        code=subprocess.run(command,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT).returncode
    record.update(exit_code=code,elapsed_seconds=time.monotonic()-started,
                  native_summary_present=(CASE/args.out_name/'ccx_summary.json').exists())
    (CASE/(args.out_name+'_execution.json')).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(record,indent=2))
    return code


if __name__=='__main__':sys.exit(main())
