"""Adopt checked lattice defaults only when native compiled CSG is identical.

The candidate STL was already rendered from this exact CSG. This changes the
default variant, not geometry, and then uses the existing prototype packager.
Strength qualification remains separate and explicit.
"""
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import sys
from child_clamp_case import analysis_case

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp'
CASE=analysis_case(PART)
SCAD=PART/'child_wte4_suspension_clamp.scad'
EXE=r'C:\Program Files\OpenSCAD\openscad.com'


def main():
    policy=PART/'spec/topology_postprocess_policy.json'
    if policy.exists() and json.loads(policy.read_text(encoding='utf-8')).get('mode')=='direct_smoothed_density':
        raise RuntimeError('User requires directly smoothed topology; lattice reconstruction cannot be adopted.')
    study=json.loads((CASE/'study_final.json').read_text(encoding='utf-8'))
    geometry=json.loads((CASE/'geometry_checks.json').read_text(encoding='utf-8'))
    sliced=json.loads((CASE/'slice_checks.json').read_text(encoding='utf-8'))
    source=SCAD.read_bytes()
    source_hash=hashlib.sha256(source).hexdigest()
    if source_hash!=study['_source_scad_sha256']:
        raise RuntimeError('Canonical source changed since candidate generation')
    if not geometry['pass'] or not sliced['pass_check']:
        raise RuntimeError('Geometry and actual slice must pass before prototype adoption')
    parameters=json.loads((CASE/'cad_parameters.json').read_text(encoding='utf-8'))
    before=CASE/'canonical_before.csg'
    after=CASE/'canonical_after.csg'
    cmd=[EXE,'-o',str(before),'-D','model="cage_lattice"']
    for k,v in parameters.items(): cmd+=['-D',f'{k}={v}']
    subprocess.run(cmd+[str(SCAD)],check=True,capture_output=True)
    text=source.decode('utf-8')
    for name,value in parameters.items():
        expr=str(value)
        if name=='clamp_bolt_x':
            expr=f'(model=="cage" || model=="cage_lattice") ? {value} : undef'
        if name=='ear_t':
            expr=f'(model=="cage" || model=="cage_lattice") ? {value} : 24'
        text,n=re.subn(r'(?m)^'+re.escape(name)+r'\s*=\s*[^;]+;',name+' = '+expr+';',text)
        if n!=1: raise RuntimeError('Expected one parameter definition: '+name)
    text=text.replace('model = "half"; // [cage,half,liner,assembled]',
                      'model = "cage"; // [cage,half,liner,assembled,cage_density]')
    # OpenSCAD evaluates this conditional using definitions in scope before it.
    # The historical ear_t declaration predates model, so move it just after.
    ear_line=re.search(r'(?m)^ear_t\s*=\s*[^;]+;',text).group(0)
    text=text.replace(ear_line,'// Ear thickness is selected after model below.',1)
    model_line='model = "cage"; // [cage,half,liner,assembled,cage_density]'
    text=text.replace(model_line,model_line+'\n'+ear_line,1)
    text=text.replace('else if(model=="cage") cage_smooth();',
                      'else if(model=="cage_density") cage_smooth();')
    # Preserve branch depth as well as geometry so native CSG stays byte-equal.
    text=text.replace('else if(model=="cage_lattice") cage_lattice();',
                      'else if(model=="cage" || model=="cage_lattice") cage_lattice();')
    SCAD.write_text(text,encoding='utf-8')
    try:
        subprocess.run([EXE,'-o',str(after),'-D','model="cage"',str(SCAD)],check=True,capture_output=True)
        if before.read_bytes()!=after.read_bytes():
            raise RuntimeError('Compiled CSG differs; do not publish a changed shape without rerender/reanalysis')
    except BaseException:
        SCAD.write_bytes(source)
        raise
    record=dict(candidate_stl_sha256=geometry['sha256'],source_before_sha256=source_hash,
        source_after_sha256=hashlib.sha256(SCAD.read_bytes()).hexdigest(),parameters=parameters,
        native_compiled_csg_identical=True,csg_sha256=hashlib.sha256(after.read_bytes()).hexdigest(),
        status='exploration_only',note='Default cage now compiles to the exact candidate CSG; historic single-half/density variants retain original bolt coordinates.')
    (CASE/'canonical_adoption.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    subprocess.run([sys.executable,str(ROOT/'tools/package_child_clamp_cage.py'),'--parametric'],
        cwd=ROOT,env=os.environ,check=True)
    print(json.dumps(record,indent=2))


if __name__=='__main__':main()
