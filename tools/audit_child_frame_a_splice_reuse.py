"""Audit unchanged splice geometry against the archived analysed revision."""
from pathlib import Path
import hashlib,json,shutil
import numpy as np
import trimesh
from topopt.voxel import voxelize_stl,largest_connected

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_exterior_structural_frame'
BASE=PART/'_work/analysis/frame_a_compact_grip'
CASE=PART/'_work/analysis/frame_a_rim_thickness'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    old=BASE/'input_history/before_rim_revision'/PART.relative_to(ROOT)/'child_exterior_structural_frame_splice.stl'
    new=PART/'child_exterior_structural_frame_splice.stl'
    a,b=[trimesh.load(p,force='mesh') for p in [old,new]]
    surface_delta=0.
    for source,target in [(a,b),(b,a)]:
        pts=np.concatenate([source.vertices,source.triangles_center])
        distance=trimesh.proximity.closest_point(target,pts)[1]
        surface_delta=max(surface_delta,float(distance.max()))
    difference=trimesh.boolean.union([trimesh.boolean.difference([a,b],engine='manifold'),trimesh.boolean.difference([b,a],engine='manifold')],engine='manifold')
    volume_delta=float(abs(difference.volume))
    grids=[]
    for h in [2,1,.5]:
        x,y=[largest_connected(voxelize_stl(str(p),h=h)) for p in [old,new]]
        layout=x.h==y.h and np.array_equal(x.origin,y.origin) and x.solid.shape==y.solid.shape
        changed=int(np.count_nonzero(x.solid!=y.solid)) if layout else None
        grids.append(dict(voxel_mm=h,origin_identical=layout,changed_material_voxels=changed,identical=layout and changed==0))
    current=CASE/'splice_reuse_provenance.json'
    history=CASE/'input_history/unreinforced_grip_root/splice_reuse_provenance.json'
    if current.exists() and not history.exists():shutil.copy2(current,history)
    solid_volume_delta=float(abs(a.volume-b.volume))
    same_surface_and_solid_volume=surface_delta<=.00001 and solid_volume_delta<=.0001 and np.array_equal(a.bounds,b.bounds)
    identical_grids=all(g['identical'] for g in grids)
    result=dict(old_sha256=sha(old),new_sha256=sha(new),symmetric_difference_mm3=volume_delta,
                bounds_delta_mm=float(np.abs(a.bounds-b.bounds).max()),volume_delta_mm3=float(abs(a.volume-b.volume)),
                surface_delta_mm=surface_delta,audited_all_vertices_and_triangle_centres=True,
                volume_tolerance_mm3=.0001,surface_tolerance_mm=.00001,native_grids=grids,
                boolean_symmetric_difference_within_tolerance=volume_delta<=.0001,
                same_surface_and_solid_volume=same_surface_and_solid_volume,
                all_native_grids_identical=identical_grids,
                native_voxel_analysis_reuse_permitted=same_surface_and_solid_volume and identical_grids,
                analysis_reused='splice_recessed_stock; unchanged 48x26x20/seat8/well10; load/support/material study retained',
                method_limit='Boolean symmetric difference is reported separately; exact native grid identity governs voxel FEA reuse. Does not establish a new CCX result.',
                qualification='Original unit analysis has failed mesh convergence; split joints remain unqualified.')
    current.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)
    if not result['native_voxel_analysis_reuse_permitted']:
        raise RuntimeError('Splice analysis cannot be reused for this export')

if __name__=='__main__':main()
