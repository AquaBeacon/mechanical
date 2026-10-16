"""Generate a smaller STEP tessellation while restoring all source CAD interfaces.

The print STL and all FEA inputs are immutable. MeshLab simplifies only the
derived density surface; the same canonical SCAD restores bores/seats/envelope.
The proxy is retained only under _work, never in the printing package.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import numpy as np
import pymeshlab
import trimesh

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp'
from child_clamp_case import analysis_case
CASE = analysis_case(PART)


def main():
    original = CASE/'cage_density_surface.stl'
    simplified = CASE/'step_density_surface.stl'
    attempts = []
    for count in [40000,80000,120000]:
        meshes = pymeshlab.MeshSet()
        meshes.load_new_mesh(str(original))
        source_faces = meshes.current_mesh().face_number()
        meshes.apply_filter('meshing_decimation_quadric_edge_collapse',targetfacenum=count,
            qualitythr=.3,preserveboundary=True,preservenormal=True,preservetopology=True,
            optimalplacement=True,planarquadric=True,autoclean=True)
        meshes.save_current_mesh(str(simplified))
        check = pymeshlab.MeshSet()
        check.load_new_mesh(str(original))
        check.load_new_mesh(str(simplified))
        distances = []
        for source,target in [(0,1),(1,0)]:
            result = check.apply_filter('get_hausdorff_distance',sampledmesh=source,targetmesh=target,
                samplevert=True,sampleedge=True,sampleface=True,samplenum=300000,savesample=False)
            distances.append({key:float(val) for key,val in result.items()})
        attempts.append(dict(target_faces=count,source_faces=source_faces,distances=distances))
        print(json.dumps(attempts[-1]),flush=True)
        if max(row['max'] for row in distances)<=.10:
            break
    else:
        raise RuntimeError('STEP density proxy exceeds 0.10mm sampled bidirectional deviation')
    proxy = CASE/'step_interface_proxy.stl'
    parameter_file=CASE/'design_parameters.json'
    parameters=json.loads(parameter_file.read_text(encoding='utf-8')) if parameter_file.exists() else {}
    defines=[arg for key,value in parameters.items() for arg in ['-D',key+'='+json.dumps(value)]]
    with (CASE/'step_proxy_cad.log').open('w',encoding='utf-8') as stream:
        result = subprocess.run([r'C:\Program Files\OpenSCAD\openscad.com','-o',str(proxy),
            '-D','model="cage"','-D','cage_surface_file='+json.dumps(simplified.as_posix()),
            *defines,str(PART/'child_wte4_suspension_clamp.scad')],stdout=stream,stderr=subprocess.STDOUT,cwd=ROOT)
    if result.returncode:
        raise RuntimeError('Exact STEP interface restoration failed')
    from clean_stl_degenerates import clean
    clean(proxy,CASE/'step_proxy_cleanup.json')
    ref = trimesh.load(CASE/'finished_cage.stl',force='mesh')
    mesh = trimesh.load(proxy,force='mesh')
    volume_error = float(abs(mesh.volume-ref.volume)/ref.volume)
    bounds_error = float(np.max(np.abs(mesh.bounds-ref.bounds)))
    if not mesh.is_watertight or not mesh.is_winding_consistent or volume_error>.005 or bounds_error>.10:
        raise RuntimeError(f'STEP proxy geometry mismatch: volume={volume_error}, bbox={bounds_error}')
    data = dict(source_print_stl_sha256=hashlib.sha256((CASE/'finished_cage.stl').read_bytes()).hexdigest(),
        print_geometry_unchanged=True,step_proxy=str(proxy),step_proxy_sha256=hashlib.sha256(proxy.read_bytes()).hexdigest(),
        proxy_faces=len(mesh.faces),reference_faces=len(ref.faces),relative_volume_error=volume_error,
        max_bounds_error_mm=bounds_error,simplification_attempts=attempts,
        interfaces='Restored by the identical canonical cage SCAD, preserve/cuts/envelope; no alternate dimensions',
        pass_check=True,approximation_note='Organic density surface only: bidirectional MeshLab samples <=0.10mm. This is a sampled error metric, not a proof of a global Hausdorff bound. No FEA or print files changed.')
    (CASE/'step_representation.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(data,indent=2),flush=True)


if __name__=='__main__':
    main()
