"""Adopt native-density candidate parameters after verifying exact compiled CSG.

No new structural members or alternative topology are introduced. The candidate
must already have passed geometry, slice, and native fine stiffness/strength.
This operation does not convert pending independent qualification into a pass.
"""
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess
from child_clamp_case import analysis_case

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp'
CASE=analysis_case(PART)
SCAD=PART/'child_wte4_suspension_clamp.scad'
EXE=r'C:\Program Files\OpenSCAD\openscad.com'

def main():
    geometry=json.loads((CASE/'geometry_checks.json').read_text(encoding='utf-8'))
    sliced=json.loads((CASE/'slice_checks.json').read_text(encoding='utf-8'))
    proof=json.loads((CASE/'final_provenance.json').read_text(encoding='utf-8'))
    fine=json.loads((CASE/'grouped_convergence.json').read_text(encoding='utf-8'))
    if not geometry['pass'] or not sliced['pass_check']:
        raise RuntimeError('Geometry and slice must pass')
    if not fine.get('all_original_cases_present') or not fine.get('all_native_fine_case_checks_pass'):
        raise RuntimeError('All native fine stiffness/strength checks required')
    source=SCAD.read_bytes()
    source_hash=hashlib.sha256(source).hexdigest()
    if proof['finishing_scad_sha256']!=source_hash or proof['final_sha256']!=geometry['sha256']:
        raise RuntimeError('Candidate identity mismatch')
    if 'no replacement ribs' not in proof['source']:
        raise RuntimeError('Native direct smoothing provenance required')
    backup=CASE/'before_native_stiffness'
    if backup.exists(): raise RuntimeError('Existing adoption history; inspect before retrying')
    shutil.copytree(PART,backup/'part',ignore=shutil.ignore_patterns('_work','__pycache__'))
    shutil.copytree(ROOT/'assemblies/child_clamp_suspension',backup/'assembly',
                    ignore=shutil.ignore_patterns('_work','__pycache__'))
    params=json.loads((CASE/'design_parameters.json').read_text(encoding='utf-8'))
    args=[EXE,'-D','model="cage"','-D','cage_surface_file='+json.dumps((CASE/'cage_density_surface.stl').as_posix())]
    before=CASE/'canonical_before.csg'
    after=CASE/'canonical_after.csg'
    defines=[arg for k,v in params.items() for arg in ['-D',k+'='+json.dumps(v)]]
    subprocess.run(args+['-o',str(before),*defines,str(SCAD)],check=True,capture_output=True)
    text=source.decode('utf-8')
    for name,value in params.items():
        pattern=r'(?m)^'+re.escape(name)+r'\s*=\s*([^;]+);'
        match=re.search(pattern,text)
        if not match: raise RuntimeError('Missing parameter: '+name)
        # Keep unrelated single-band/historical variants at their old defaults.
        condition=' || '.join('model=='+json.dumps(mode) for mode in
                             ['cage','cage_density','cage_space','cage_preserve','cage_cuts'])
        replacement=name+' = ('+condition+') ? '+json.dumps(value)+' : ('+match.group(1)+');'
        text,n=re.subn(pattern,lambda _:replacement,text)
        if n!=1: raise RuntimeError('Expected one parameter: '+name)
    (CASE/'canonical_before_adoption.scad.txt').write_bytes(source)
    SCAD.write_text(text,encoding='utf-8')
    try:
        subprocess.run(args+['-o',str(after),str(SCAD)],check=True,capture_output=True)
        if before.read_bytes()!=after.read_bytes():
            raise RuntimeError('Compiled CSG changed; must rerender and reanalyse')
    except BaseException:
        SCAD.write_bytes(source)
        raise
    proof['finishing_scad_sha256_before_default_adoption']=source_hash
    proof['finishing_scad_sha256']=hashlib.sha256(SCAD.read_bytes()).hexdigest()
    proof['native_compiled_csg_identical_after_default_adoption']=True
    proof['csg_sha256']=hashlib.sha256(after.read_bytes()).hexdigest()
    (CASE/'final_provenance.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
    print('Direct-density defaults adopted; native CSG byte-identical. Qualification remains separate.')

if __name__=='__main__': main()
