"""Extract/smooth with installed topopt; restore exact CAD interfaces via SCAD.

Run only after opt writes its summary. No geometry simplification or stress code.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import argparse
import numpy as np
import trimesh
import pymeshfix

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp'
CASE=PART/'_work/analysis/stress_smooth_r85_v065'


def repair_surface(source, destination, report_path=None):
    """Repair only nonclosed shells; preserve signed cavity orientations."""
    original=trimesh.load(source,force='mesh')
    components=original.split(only_watertight=False)
    repaired=[]
    changes=[]
    for shell in components:
        if shell.is_watertight:
            repaired.append(shell)
            continue
        fix=pymeshfix.MeshFix(shell.vertices,shell.faces)
        fix.repair(joincomp=False,remove_smallest_components=False)
        result=trimesh.Trimesh(fix.points,fix.faces)
        if result.volume*shell.volume<0:
            result.invert()
        delta_volume=abs(result.volume-shell.volume)
        delta_bounds=float(np.max(np.abs(result.bounds-shell.bounds)))
        points=np.vstack([result.vertices,result.triangles_center])
        surface_delta=0.0
        for offset in range(0,len(points),2000):
            surface_delta=max(surface_delta,float(trimesh.proximity.closest_point(shell,points[offset:offset+2000])[1].max()))
        if not result.is_watertight or delta_volume>0.001 or delta_bounds>0.001 or surface_delta>0.001:
            raise RuntimeError('Repair changed the native topology envelope; do not adopt')
        changes.append(dict(faces_before=len(shell.faces),faces_after=len(result.faces),
                            signed_volume_before_mm3=float(shell.volume),
                            signed_volume_after_mm3=float(result.volume),
                            bounds_max_delta_mm=delta_bounds,surface_max_delta_mm=surface_delta))
        repaired.append(result)
    result=trimesh.util.concatenate(repaired)
    if not result.is_watertight or not result.is_winding_consistent:
        raise RuntimeError('Native smoothed surface is still invalid')
    data=result.export(file_type='stl')
    if not destination.exists() or destination.read_bytes()!=data:
        destination.write_bytes(data)
    info=dict(method='MeshFix only on nonclosed shell; no component removal or join; cavity orientations retained',
              shells=changes,volume_delta_mm3=float(result.volume-original.volume),
              raw_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
              repaired_sha256=hashlib.sha256(destination.read_bytes()).hexdigest())
    (report_path or CASE/'surface_repair.json').write_text(json.dumps(info,indent=2)+'\n',encoding='utf-8')
    return info


def close_enclosed_density_voids(surface, report_path, max_fraction=.005):
    """Remove only small inward closed boundary shells from a smoothed mesh.

    This is direct mesh cleanup, not a CAD plug or a replacement member. Every
    exterior triangle must survive byte-identically at STL float32 precision.
    Positive disconnected pieces are rejected, never joined or dropped.
    """
    from verify_child_clamp_cage import native_solid, contains
    mesh=trimesh.load(surface,force='mesh')
    if not mesh.is_watertight or not mesh.is_winding_consistent:
        raise RuntimeError('Closed consistently oriented density surface required')
    shells=mesh.split(only_watertight=False)
    outer=[s for s in shells if s.volume>0]
    inner=[s for s in shells if s.volume<0]
    if len(outer)!=1 or len(outer)+len(inner)!=len(shells):
        raise RuntimeError('Do not join or delete disconnected positive topology')
    volume=-sum(s.volume for s in inner)
    if volume/mesh.volume>max_fraction:
        raise RuntimeError('Enclosed voids exceed the small-cleanup volume budget')
    body=native_solid(outer[0])
    if not all(contains(body,s.vertices).all() for s in inner):
        raise RuntimeError('Inward boundary is not completely enclosed by the exterior')
    before=surface.read_bytes()
    backup=surface.with_name(surface.stem+'_before_void_cleanup.stl')
    if backup.exists(): raise RuntimeError('Preserve prior cleanup history')
    backup.write_bytes(before)
    data=outer[0].export(file_type='stl')
    surface.write_bytes(data)
    checked=trimesh.load(surface,force='mesh',process=False)
    equal=np.array_equal(outer[0].triangles.astype(np.float32),checked.triangles.astype(np.float32))
    if not equal:
        surface.write_bytes(before)
        raise RuntimeError('Exterior triangles changed; cleanup rejected')
    record=dict(method='Remove enclosed inward boundary shells from the directly smoothed density mesh',
        source_sha256=hashlib.sha256(before).hexdigest(),result_sha256=hashlib.sha256(data).hexdigest(),
        inward_shells_removed=len(inner),filled_volume_mm3=float(volume),
        relative_volume_added=float(volume/mesh.volume),maximum_allowed_fraction=max_fraction,
        exterior_triangles_bit_identical=True,exterior_triangle_count=len(outer[0].faces),
        functional_through_holes_unchanged=True,replacement_members_added=False,
        cavities=[dict(volume_mm3=float(-s.volume),bounds_mm=s.bounds.tolist()) for s in inner],
        qualification='Requires exact CAD finishing and fresh structural validation; no strength pass inferred')
    report_path.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    return record


def main():
    global CASE
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case',type=Path,help='analysis directory (default retains the historical run)')
    parser.add_argument('--candidate-only',action='store_true',help='write a finished trial inside the analysis case without replacing the canonical part')
    parser.add_argument('--reuse-extract',action='store_true',help='reuse completed native extraction')
    parser.add_argument('--reuse-render',action='store_true',help='reuse an already rendered identical surface (hash checked)')
    args=parser.parse_args()
    if args.case:
        CASE=args.case.resolve()
    study=CASE/'study_stress_smooth.json'
    out=CASE/'extract'
    out.mkdir(exist_ok=True)
    # Sample the native smoothed field at the optimisation resolution.
    # This is surface tessellation, not rib reconstruction or mesh decimation.
    finish_study=json.loads(study.read_text(encoding='utf-8'))
    finish_study['finish']['voxel_mm']=1.0
    finishing=CASE/'study_finish.json'
    finishing.write_text(json.dumps(finish_study,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if not args.reuse_extract:
        with (out/'run.log').open('w',encoding='utf-8') as stream:
            native_cli=[sys.executable,'-u',str(ROOT/'tools/clamp_bambu_material.py')] if finish_study['material']=='BAMBU-PETG-BASIC' else [sys.executable,'-u','-m','topopt']
            run=subprocess.run(native_cli+['extract',str(CASE/'opt'),
                                '--study',str(finishing),'--out',str(out),'--levels','0.4,0.5,0.6'],
                               stdout=stream,stderr=subprocess.STDOUT)
        if run.returncode not in (0,1):
            raise RuntimeError('Extraction failed; see extract/run.log')
    extraction=json.loads((out/'study_stress_smooth_extract.json').read_text(encoding='utf-8'))
    chosen_level=extraction['chosen_level']
    surface=out/f'study_stress_smooth_t{round(chosen_level*100):02d}_finish.stl'
    if not surface.exists():
        raise RuntimeError('Native finished/smoothed surface missing')
    destination=CASE/'smoothed_density_surface.stl' if args.candidate_only else PART/'spec/smoothed_density_surface.stl'
    destination.parent.mkdir(exist_ok=True)
    existing_hash=hashlib.sha256(destination.read_bytes()).hexdigest() if destination.exists() else None
    repair=repair_surface(surface,destination)
    final=CASE/'finished_candidate.stl' if args.candidate_only else PART/'child_wte4_suspension_clamp_smooth.stl'
    if args.reuse_render:
        if existing_hash!=repair['repaired_sha256'] or not final.exists():
            raise RuntimeError('Existing render does not match the repaired surface')
        print('Reused unchanged surface render after SHA-256 equality check')
    else:
        with (CASE/'exact_interface_render.log').open('w',encoding='utf-8') as stream:
            subprocess.run([r'C:\Program Files\OpenSCAD\openscad.com','-o',str(final),'-D','model="smooth"',
                            '-D','smooth_surface_file='+json.dumps(destination.as_posix()),
                            str(PART/'child_wte4_suspension_clamp.scad')],stdout=stream,stderr=subprocess.STDOUT,check=True)
    from clean_stl_degenerates import clean
    clean(final,CASE/'exact_interface_degeneracy_cleanup.json')
    final_study=json.loads(study.read_text(encoding='utf-8'))
    for key in ['geometry','design','finish','voxel_mm']:
        final_study.pop(key,None)
    final_study['part']=str(final)
    final_study['resolution_mm']=1.0
    final_study['_part_sha256']=hashlib.sha256(final.read_bytes()).hexdigest()
    final_study['_not_a_part']='Directly smoothed topology with exact source-CAD interfaces. Final geometry needs independent verification; no simplified rib reconstruction.'
    keys=['material','build_axis','raster_axis','infill','walls','safety_factor','max_deflection_mm','regions','cases']
    if '_material_card' in final_study:
        keys.append('_material_card')
    original=json.loads(study.read_text(encoding='utf-8'))
    assert all(final_study[key]==original[key] for key in keys),'Optimiser and verifier conditions diverged'
    (CASE/'study_final.json').write_text(json.dumps(final_study,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    identity=dict(same_condition_keys=keys,all_equal=True,topology=str(study),final=str(CASE/'study_final.json'),
                  native_smoothed_sha256=hashlib.sha256(surface.read_bytes()).hexdigest(),
                  final_part_sha256=final_study['_part_sha256'],
                  chosen_level=chosen_level,chosen_reason=extraction['chosen_reason'],
                  finishing_study=str(finishing),surface_sampling_mm=1.0,smooth_mm=0.75,
                  surface_repair=repair,
                  source='Native topopt extraction + source SCAD exact interfaces; no replacement ribs')
    (CASE/'final_provenance.json').write_text(json.dumps(identity,indent=2)+'\n',encoding='utf-8')
    print(final)


if __name__=='__main__':
    main()
