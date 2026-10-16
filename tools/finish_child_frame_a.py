"""Exact stock/clearance booleans on native smoothed topology, using Manifold.

All dimensions and mask shapes come from the generated canonical SCAD. This
replaces costly CGAL evaluation of identical boolean operations, not the native
solver, density smoothing, or the preserved physical interface definitions.
"""
from pathlib import Path
import hashlib,json,subprocess
import numpy as np
import trimesh

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_exterior_structural_frame'
CASE=PART/'_work/analysis/frame_a_rim_thickness'
OSC=r'C:\Program Files\OpenSCAD\openscad.com'


def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def finish():
    source=PART/'child_exterior_structural_frame.scad'
    inputs=json.loads((CASE/'input_identity.json').read_text())
    if digest(source)!=inputs['source']: raise RuntimeError('Input CAD identity changed')
    for name in ['domain','preserve','cuts']:
        if digest(CASE/(name+'.stl'))!=inputs['geometry'][name]:
            raise RuntimeError(f'{name} input geometry changed after preparation')
    meshes={n:trimesh.load(CASE/(n+'.stl'),force='mesh') for n in ['domain','preserve','cuts']}
    for n,m in meshes.items():
        if not m.is_watertight or not m.is_winding_consistent: raise RuntimeError(f'{n} is invalid')
    native=PART/'spec/frame_a_density_surface.stl'
    surface=trimesh.load(native,force='mesh')
    combined=trimesh.boolean.union([surface,meshes['preserve']],engine='manifold')
    cut=trimesh.boolean.difference([combined,meshes['cuts']],engine='manifold')
    full=trimesh.boolean.intersection([cut,meshes['domain']],engine='manifold')
    outputs={'finished_surface':full}
    for n in ['lower_minus','lower_plus','upper_minus','upper_plus']:
        mask=CASE/(f'mask_{n}.stl')
        with (CASE/(f'mask_{n}_render.log')).open('w') as stream:
            subprocess.run([OSC,'-o',str(mask),'-D',f'model="mask_{n}"',str(source)],
                           stdout=stream,stderr=subprocess.STDOUT,check=True)
        outputs[n]=trimesh.boolean.intersection([full,trimesh.load(mask,force='mesh')],engine='manifold')
    rows={}
    for name,m in outputs.items():
        intermediate=CASE/(name+'_boolean.stl'); m.export(intermediate)
        from clean_stl_degenerates import clean,precision_weld
        precision=precision_weld(intermediate,CASE/(name+'_precision_weld.json'),allow_collinear=True)
        cleanup=clean(intermediate,CASE/(name+'_edge_flip.json'),binary=True)
        m=trimesh.load(intermediate,force='mesh')
        zero=int(np.count_nonzero(m.area_faces<1e-12))
        bodies=sum(s.volume>0 for s in m.split(only_watertight=False))
        if not m.is_watertight or not m.is_winding_consistent or zero or bodies!=1:
            raise RuntimeError(f'{name} rejected: watertight={m.is_watertight}, zero_area={zero}, bodies={bodies}')
        path=PART/f'spec/frame_a_{name}.stl'; m.export(path)
        rows[name]=dict(sha256=digest(path),triangles=len(m.faces),zero_area=zero,precision_weld=precision,edge_flip=cleanup,
                       bounds_mm=m.bounds.tolist(),volume_mm3=float(m.volume),positive_bodies=int(bodies))
    report=dict(method='Exact Manifold union(native smooth,preserve), difference(cuts), intersection(domain/tile masks)',
                input_hashes={n:digest(CASE/(n+'.stl')) for n in meshes},
                native_surface_sha256=digest(native),source_sha256=digest(source),outputs=rows)
    (CASE/'finished_cad_provenance.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    print(json.dumps(finish()))
