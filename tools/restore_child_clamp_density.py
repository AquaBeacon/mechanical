"""Restore direct native density smoothing, with original functional interfaces.

No optimisation/FEA/smoothing algorithm is implemented here. Reuses the recorded
native finish output and renders the canonical CAD interface operations only.
"""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp'
ASM=ROOT/'assemblies/child_clamp_suspension'
SOURCE=PART/'_work/analysis/lightweight_epdm_v020'
CASE=PART/'_work/analysis/direct_density_smoothed_20261005'


def save(path,data):
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if CASE.exists(): raise RuntimeError('Preserve the existing case; do not overwrite')
    CASE.mkdir(parents=True)
    snapshot=CASE/'before_direct_density'
    records=[]
    for base,label in [(PART,'part'),(ASM,'assembly')]:
        for src in base.iterdir():
            if src.name=='_work': continue
            dst=snapshot/label/src.name
            if src.is_dir(): shutil.copytree(src,dst)
            else:
                dst.parent.mkdir(parents=True,exist_ok=True)
                shutil.copy2(src,dst)
            records.append(str(src.relative_to(ROOT)))
    save(snapshot/'manifest.json',dict(source_paths=records,reason='User rejects primitive reconstruction; preserve prior prototype unchanged'))
    policy=dict(mode='direct_smoothed_density',user_confirmed='2026-10-05',
        forbidden='Replacement of organic optimisation members by hand-authored rings, columns or beams',
        allowed='Native density smoothing, mesh repair without topology redesign, exact functional interface restoration',
        required='Recheck connectivity, minimum thickness, fit and final-geometry strength after changes')
    save(PART/'spec/topology_postprocess_policy.json',policy)
    scad=PART/'child_wte4_suspension_clamp.scad'
    text=scad.read_text(encoding='utf-8')
    text=text.replace('(model=="cage" || model=="cage_lattice") ? 28.0 : 24','model=="cage_lattice" ? 28.0 : 24')
    text=text.replace('(model=="cage" || model=="cage_lattice") ? 71.95 : undef','model=="cage_lattice" ? 71.95 : undef')
    text=text.replace('else if(model=="cage_density") cage_smooth();\nelse if(model=="cage" || model=="cage_lattice") cage_lattice();',
        'else if(model=="cage" || model=="cage_density") cage_smooth();\n// Historical reconstruction only; user prohibits adoption.\nelse if(model=="cage_lattice") cage_lattice();')
    scad.write_text(text,encoding='utf-8')
    for name in ['cage_density_surface.stl','interface.json','study_cage.json']:
        shutil.copy2(SOURCE/name,CASE/name)
    shutil.copyfile(CASE/'cage_density_surface.stl',PART/'spec/cage_density_surface.stl')
    final=CASE/'finished_cage.stl'
    cmd=[r'C:\Program Files\OpenSCAD\openscad.com','-o',str(final),'-D','model="cage"',str(scad)]
    with (CASE/'render.log').open('w',encoding='utf-8') as log:
        subprocess.run(cmd,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True)
    from clean_stl_degenerates import clean
    clean(final,CASE/'degeneracy_cleanup.json')
    study=json.loads((SOURCE/'study_final.json').read_text(encoding='utf-8'))
    study['part']=str(final)
    study['_part_sha256']=digest(final)
    save(CASE/'study_final.json',study)
    native=json.loads((SOURCE/'final_provenance.json').read_text(encoding='utf-8'))
    save(CASE/'final_provenance.json',dict(
        source_native_run=str(SOURCE.relative_to(ROOT)),
        native_finish=str((SOURCE/'extract/study_cage_t40_finish.stl').relative_to(ROOT)),
        native_finish_sha256=native['source_sha256'],
        density_surface_sha256=digest(CASE/'cage_density_surface.stl'),
        finishing_scad_sha256=digest(scad),final_sha256=digest(final),
        identical_to_previously_verified_direct_mesh=digest(final)==digest(SOURCE/'finished_cage.stl'),
        original_finish_provenance=native,
        source='Native density-field smoothing; exact CAD interfaces only; no replacement ribs',
        status='exploration_only',note='Prior native stiffness failure remains; this is a shape-policy correction, not strength qualification.'))
    print(CASE)


if __name__=='__main__':main()
