"""Regenerate the existing cage with filled enclosed cavities, without optimisation.

Uses the completed density surface, canonical SCAD and existing native tools.
Does not call opt, extract, setup, FEA or CalculiX. Original analyses are retained.
"""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys

from fill_child_clamp_closed_voids import fill

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp'
ORIGINAL = PART/'_work/analysis/connected_cage_rubber1_v065'
CASE = PART/'_work/analysis/connected_cage_rubber1_solid'
ASSEMBLY = ROOT/'assemblies/child_clamp_suspension'


def main():
    CASE.mkdir(parents=True,exist_ok=True)
    snapshot = ORIGINAL/'before_closed_void_fill'
    snapshot.mkdir(exist_ok=True)
    for base, names, label in [(PART,['README.md','CAGE_TOPOLOGY.md','manufacturing.json',
        'child_wte4_suspension_clamp.scad','child_wte4_suspension_clamp_cage.stl',
        'child_wte4_suspension_clamp_cage.step'],'part'),
        (ASSEMBLY,['README.md','placement.json','print_config.json','child_clamp_suspension.step'],'assembly')]:
        folder = snapshot/label
        folder.mkdir(exist_ok=True)
        for name in names:
            if (base/name).exists() and not (folder/name).exists():
                shutil.copy2(base/name,folder/name)
    for name in ['interface.json','study_cage.json']:
        shutil.copy2(ORIGINAL/name,CASE/name)
    info = fill(ORIGINAL/'cage_density_surface.stl',CASE/'cage_density_surface.stl',CASE/'density_closed_void_fill.json')
    output = CASE/'finished_cage.stl'
    with (CASE/'exact_interface_driver.log').open('w',encoding='utf-8') as stream:
        result = subprocess.run([r'C:\Program Files\OpenSCAD\openscad.com','-o',str(output),
            '-D','model="cage"','-D','cage_surface_file='+json.dumps((CASE/'cage_density_surface.stl').as_posix()),
            str(PART/'child_wte4_suspension_clamp.scad')],cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError('Canonical void-free cage render failed')
    from clean_stl_degenerates import clean
    clean(output,CASE/'exact_interface_degeneracy_cleanup.json')
    import trimesh
    import numpy as np
    from verify_child_clamp_cage import native_solid
    old = trimesh.load(ORIGINAL/'finished_cage.stl',force='mesh')
    new = trimesh.load(output,force='mesh')
    outer = [s for s in old.split() if s.volume>0][0]
    a,b = native_solid(outer),native_solid(new)
    symmetric_difference = float(abs((a-b).volume())+abs((b-a).volume()))
    if len(new.split())!=1 or not new.is_watertight or symmetric_difference>.01:
        raise RuntimeError('Void-free cage changes its external shape or still has an internal shell')
    proxy = CASE/'step_interface_proxy.stl'
    fill(ORIGINAL/'step_interface_proxy.stl',proxy,CASE/'step_closed_void_fill.json')
    representation = json.loads((ORIGINAL/'step_representation.json').read_text(encoding='utf-8'))
    representation.update(source_print_stl_sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
        step_proxy=str(proxy),step_proxy_sha256=hashlib.sha256(proxy.read_bytes()).hexdigest(),
        proxy_faces=len(trimesh.load(proxy,force='mesh').faces),reference_faces=len(new.faces),
        relative_volume_error=float(abs(trimesh.load(proxy,force='mesh').volume-new.volume)/new.volume),
        previous_representation_record=str(ORIGINAL/'step_representation.json'),
        void_fill_note='Only enclosed inward shells removed from original verified density and STEP representation; no new decimation or optimisation.')
    (CASE/'step_representation.json').write_text(json.dumps(representation,indent=2)+'\n',encoding='utf-8')
    revision = dict(date='2026-10-02',topology_optimisation_started=False,fea_started=False,
        original_case=str(ORIGINAL),original_study_sha256=hashlib.sha256((ORIGINAL/'study_cage.json').read_bytes()).hexdigest(),
        source_scad_sha256=hashlib.sha256((PART/'child_wte4_suspension_clamp.scad').read_bytes()).hexdigest(),
        source_stl_sha256=hashlib.sha256((ORIGINAL/'finished_cage.stl').read_bytes()).hexdigest(),
        result_stl_sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
        old_volume_mm3=float(old.volume),new_volume_mm3=float(new.volume),added_volume_mm3=float(new.volume-old.volume),
        bounds_difference_mm=float(np.max(np.abs(new.bounds-old.bounds))),
        outer_symmetric_difference_mm3=symmetric_difference,enclosed_cavities_after=0,
        density_processing=info,pass_check=True,
        structural_note='Original stiffness failure and failed independent meshing are historical. No structural reanalysis of this filled revision has run; lifting remains unqualified.')
    (CASE/'void_free_revision.json').write_text(json.dumps(revision,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(revision,indent=2),flush=True)


if __name__=='__main__':
    main()
