"""Rebuild the cage's smaller CAD STEP and verify it against the print STL."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp'
from child_clamp_case import analysis_case
CASE = analysis_case(PART)
FREECAD = r'C:\Users\ryupc\AppData\Local\Programs\FreeCAD 1.0\bin\freecadcmd.exe'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reuse-prepared',action='store_true',
        help='Use the existing bounded proxy after checking source and proxy hashes.')
    args=parser.parse_args()
    if (CASE/'cad_parameters.json').exists():
        # Parametric rings have a modest mesh: export the exact checked mesh,
        # rather than trying to reconstruct it from a historic density field.
        proxy = CASE/'finished_cage.stl'
        representation = dict(source_print_stl_sha256=hashlib.sha256(proxy.read_bytes()).hexdigest(),
            step_proxy=str(proxy),print_geometry_unchanged=True,pass_check=True,
            approximation_note='Exact print tessellation; faceted STEP without mesh simplification.')
        (CASE/'step_representation.json').write_text(json.dumps(representation,indent=2)+'\n',encoding='utf-8')
    else:
        if not args.reuse_prepared:
            subprocess.run([sys.executable,str(ROOT/'tools/prepare_child_clamp_cage_step.py')],cwd=ROOT,check=True)
        representation = json.loads((CASE/'step_representation.json').read_text(encoding='utf-8'))
        if not representation['pass_check'] or hashlib.sha256(Path(representation['step_proxy']).read_bytes()).hexdigest()!=representation['step_proxy_sha256']:
            raise RuntimeError('Prepared STEP proxy identity or bounds check failed')
    if hashlib.sha256((PART/'child_wte4_suspension_clamp_cage.stl').read_bytes()).hexdigest()!=representation['source_print_stl_sha256']:
        raise RuntimeError('Rebuild/reanalyse the case: its checked print STL is not the canonical print STL')
    env = dict(os.environ,STL_IN=representation['step_proxy'],
        STEP_OUT=str(PART/'child_wte4_suspension_clamp_cage.step'))
    with (CASE/'step_export_proxy.log').open('w',encoding='utf-8') as stream:
        subprocess.run([FREECAD,str(ROOT/'scad/lib/stl_to_step.py')],cwd=ROOT,env=env,
            stdout=stream,stderr=subprocess.STDOUT,check=True)
    env.update(ASM_ROOT=str(ROOT),CLAMP_STEP_NAMES='["child_wte4_suspension_clamp_cage"]',
        CLAMP_STEP_CHECKS=str(CASE/'step_checks.json'))
    checker=ROOT/'tools/verify_child_clamp_steps.py'
    policy=PART/'spec/topology_postprocess_policy.json'
    if policy.exists() and json.loads(policy.read_text(encoding='utf-8')).get('mode')=='direct_smoothed_density':
        # Read the already valid faceted STEP without automatic shape rewriting;
        # the same native validity, solid count, volume and bounds gates remain.
        env.update(CLAMP_DIRECT_CASE=str(CASE),CLAMP_DIRECT_STEP_MODE='part-check')
        checker=ROOT/'tools/read_child_clamp_step_direct.py'
    with (CASE/'step_verify.log').open('w',encoding='utf-8') as stream:
        subprocess.run([FREECAD,str(checker)],cwd=ROOT,env=env,
            stdout=stream,stderr=subprocess.STDOUT,check=True)
    print((CASE/'step_checks.json').read_text(encoding='utf-8'))


if __name__=='__main__':
    main()
