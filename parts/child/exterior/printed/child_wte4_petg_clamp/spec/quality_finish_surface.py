"""Improve triangulation of a density-derived finished surface using MeshLab.

This is surface processing, not reconstruction of the topology. MeshFix only
removes local self intersections; topology, volume and surface movement are
audited. Geometry/interface, assembly, CCX and slicer checks remain separate.
"""
from pathlib import Path
import argparse, hashlib, json
import numpy as np
import pymeshlab
import trimesh
from topopt.ccx import repair_stl, shell_check, refine_stl


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decimate(mesh, count):
    ms = pymeshlab.MeshSet()
    ms.add_mesh(pymeshlab.Mesh(mesh.vertices, mesh.faces))
    ms.meshing_decimation_quadric_edge_collapse(targetfacenum=count,
        preservetopology=True, preserveboundary=True, preservenormal=True,
        planarquadric=True, qualitythr=.8 if count == 40000 else .5,
        autoclean=True)
    return trimesh.Trimesh(ms.current_mesh().vertex_matrix(),
                           ms.current_mesh().face_matrix())


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    if args.out.exists():
        raise RuntimeError('Use a fresh output directory')
    args.out.mkdir(parents=True)
    source = trimesh.load(args.source, force='mesh')
    if not source.is_volume:
        raise RuntimeError('Input must be a closed volume')
    decimate(source, 60000).export(args.out/'decimated.stl')
    repairs = [repair_stl(str(args.out/'decimated.stl'),
                          str(args.out/'decimated_repaired.stl'))]
    a = trimesh.load(args.out/'decimated_repaired.stl', force='mesh')
    ms = pymeshlab.MeshSet()
    ms.add_mesh(pymeshlab.Mesh(a.vertices, a.faces))
    ms.meshing_isotropic_explicit_remeshing(iterations=5,
        targetlen=pymeshlab.PureValue(1.0), featuredeg=30,
        checksurfdist=True, maxsurfdist=pymeshlab.PureValue(.02))
    trimesh.Trimesh(ms.current_mesh().vertex_matrix(),
                   ms.current_mesh().face_matrix()).export(args.out/'isotropic.stl')
    repairs.append(repair_stl(str(args.out/'isotropic.stl'),
                              str(args.out/'isotropic_repaired.stl')))
    result = decimate(trimesh.load(args.out/'isotropic_repaired.stl',
                                  force='mesh'), 40000)
    target = args.out/'finished_quality.stl'
    result.export(target)
    result = trimesh.load(target, force='mesh')
    shell = shell_check(str(target))
    # Sample both directions, including face interiors. This is explicitly a
    # sampled error, never a certificate of exact interface dimensions.
    distances = []
    for src, dst in [(source, result), (result, source)]:
        points = np.vstack([src.vertices[::max(1, len(src.vertices)//6000)],
            src.triangles_center[::max(1, len(src.faces)//6000)]])
        maximum = 0.
        for i in range(0, len(points), 500):
            maximum = max(maximum, float(trimesh.proximity.closest_point(
                dst, points[i:i+500])[1].max()))
        distances.append(maximum)
    volume_error = abs(float(result.volume/source.volume-1))
    bounds_error = float(np.abs(result.bounds-source.bounds).max())
    failures = []
    if not shell['closed_shell'] or shell.get('self_intersections') != 0:
        failures.append('closed shell and self intersections')
    if result.euler_number != source.euler_number:
        failures.append('topology changed')
    if volume_error > .001 or bounds_error > .02 or max(distances) > .25:
        failures.append('surface processing error bound')
    fine = args.out/'refined_1.5mm.stl'
    refinement = refine_stl(str(target), str(fine), 1.5)
    refinement['shell'] = shell_check(str(fine))
    if not refinement['shell']['closed_shell']:
        failures.append('finest analysis shell')
    report = dict(status='exploration_only', result='FAIL' if failures else 'PASS',
        method='MeshLab quadric decimation 60000, MeshFix, 1 mm isotropic remesh (5 iterations, 0.02 mm projection bound), MeshFix, quality-preserving decimation 40000',
        source=str(args.source.resolve()), source_sha256=sha(args.source),
        output=str(target.resolve()), output_sha256=sha(target),
        script_sha256=sha(Path(__file__)), shell=shell,
        euler=[int(source.euler_number), int(result.euler_number)],
        volume_mm3=float(result.volume), volume_relative_error=volume_error,
        dimensions_mm=result.extents.tolist(), bounds_error_mm=bounds_error,
        bidirectional_sampled_surface_error_mm=distances, repairs=repairs,
        finest_shell=refinement, failures=failures,
        remaining='Exact functional clearance, assembly, strength convergence and slicer support checks required before adoption')
    (args.out/'quality_validation.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, indent=2), flush=True)
    if failures:
        raise RuntimeError('Quality surface rejected')


if __name__ == '__main__':
    main()
