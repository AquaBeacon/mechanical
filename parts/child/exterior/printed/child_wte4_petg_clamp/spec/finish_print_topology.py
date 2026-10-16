"""Exact local interface restoration of the native density-smoothed surface.

No beam/ring reconstruction: all non-interface material comes from native
topopt extract. CAD Boolean operations restore preserved faces and clip the
original permissible envelope and functional voids. The resulting shape still
requires independent structural and printing checks before adoption.
"""
from pathlib import Path
import argparse, hashlib, json, sys
import numpy as np
import trimesh
from manifold3d import Manifold, Mesh64

PART=Path(__file__).resolve().parents[1]
INPUT=PART/'_work/analysis/topology_print'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def solid(mesh):
    result=Manifold(Mesh64(np.asarray(mesh.vertices,dtype=np.float64),
                           np.asarray(mesh.faces,dtype=np.uint64)))
    if str(result.status())!='Error.NoError': raise RuntimeError(f'CAD Boolean input: {result.status()}')
    return result

def surface(body):
    data=body.to_mesh64()
    return trimesh.Trimesh(vertices=data.vert_properties[:,:3],faces=data.tri_verts,process=False)

def numeric_cleanup(original):
    """Edge flip, then collapse only residual all-short degenerate faces."""
    import pymeshlab
    from scipy.spatial import cKDTree
    ms=pymeshlab.MeshSet()
    ms.add_mesh(pymeshlab.Mesh(original.vertices,original.faces))
    ms.meshing_remove_t_vertices(method='Edge Flip',threshold=1e9,repeat=True)
    result=trimesh.Trimesh(ms.current_mesh().vertex_matrix(),ms.current_mesh().face_matrix())
    collapsed=0
    for _ in range(3):
        lengths=np.linalg.norm(np.roll(result.triangles,-1,axis=1)-result.triangles,axis=2).max(axis=1)
        selected=(result.area_faces<1e-12)&(lengths<1e-5)
        if not np.any(selected): break
        parent=np.arange(len(result.vertices))
        def find(i):
            while parent[i]!=i:
                parent[i]=parent[parent[i]];i=parent[i]
            return i
        for face in result.faces[selected]:
            roots=[find(int(i)) for i in face];anchor=min(roots)
            for i in roots: parent[i]=anchor
        parent=np.array([find(i) for i in range(len(parent))])
        result.faces=parent[result.faces]
        faces=result.faces
        result.update_faces((faces[:,0]!=faces[:,1])&(faces[:,1]!=faces[:,2])&(faces[:,0]!=faces[:,2]))
        result.update_faces(result.unique_faces());result.remove_unreferenced_vertices()
        collapsed+=int(selected.sum())
    movement=float(cKDTree(result.vertices).query(original.vertices)[0].max())
    # Check all vertices and centroids of every changed triangle in both directions.
    _,ids=np.unique(np.vstack([original.vertices,result.vertices]),axis=0,return_inverse=True)
    keys=[]
    for mesh,v in [(original,ids[:len(original.vertices)]),(result,ids[len(original.vertices):])]:
        faces=np.ascontiguousarray(np.sort(v[mesh.faces],axis=1))
        keys.append(faces.view(np.dtype((np.void,faces.dtype.itemsize*3))).ravel())
    changed=[~np.isin(keys[0],keys[1]),~np.isin(keys[1],keys[0])]
    maximum=0.
    for src,dst,mask in [(original,result,changed[0]),(result,original,changed[1])]:
        samples=np.vstack([src.triangles[mask].reshape(-1,3),src.triangles_center[mask]])
        for start in range(0,len(samples),1000):
            maximum=max(maximum,float(trimesh.proximity.closest_point(dst,samples[start:start+1000])[1].max()))
    volume=abs(float(result.volume-original.volume))
    bounds=float(np.abs(result.bounds-original.bounds).max())
    zeros=int(np.sum(result.area_faces<1e-12))
    if not result.is_volume or zeros or len(result.split())!=1 or result.euler_number!=original.euler_number or movement>1e-5 or maximum>2e-5 or volume>.001 or bounds>.001:
        raise RuntimeError(f'Numerical cleanup rejected: {movement=}, {maximum=}, {volume=}, {bounds=}, {zeros=}, euler={original.euler_number}/{result.euler_number}')
    return result,dict(method='MeshLab edge flip then collapse only zero-area faces whose every edge is below 0.00001 mm; ASCII double precision',
        collapsed_sliver_faces=collapsed,maximum_vertex_movement_mm=movement,
        changed_triangles_sampled=[int(mask.sum()) for mask in changed],bidirectional_surface_delta_mm=maximum,
        volume_delta_mm3=volume,bounds_delta_mm=bounds,euler_number=int(result.euler_number))

def solver_grid_cleanup(original):
    """Match native shell weld; contract only microscopic boundary artefacts."""
    from scipy.spatial import cKDTree
    from topopt.geom import shell_report
    result=original.copy();result.vertices=np.round(result.vertices,5)
    result.merge_vertices(digits_vertex=5)
    result.update_faces(result.nondegenerate_faces());result.update_faces(result.unique_faces())
    result.remove_unreferenced_vertices()
    counts=np.bincount(result.edges_unique_inverse)
    if np.any(counts>2): raise RuntimeError('Native grid has non-manifold physical edges')
    edges=result.edges_unique[counts==1];mapping=np.arange(len(result.vertices));diameters=[]
    if len(edges):
        for component in trimesh.graph.connected_components(edges,nodes=np.unique(edges)):
            points=result.vertices[component]
            diameter=float(np.linalg.norm(points[:,None]-points[None,:],axis=2).max())
            if diameter>1e-4: raise RuntimeError(f'Boundary exceeds numerical repair limit: {diameter} mm')
            mapping[component]=min(component);diameters.append(diameter)
        result.faces=mapping[result.faces]
        result.update_faces(result.nondegenerate_faces());result.update_faces(result.unique_faces())
        result.remove_unreferenced_vertices()
    movement=float(cKDTree(result.vertices).query(original.vertices)[0].max())
    volume=abs(float(result.volume-original.volume))
    native=shell_report(result.triangles,intersections=False)
    if not result.is_volume or not native['closed_shell'] or movement>1e-4 or volume>.1 or result.euler_number!=original.euler_number:
        raise RuntimeError(f'Native grid cleanup rejected: {movement=}, {volume=}, {native=}')
    return result,dict(method='Round to native 0.00001 mm weld grid; remove collapsed/duplicate facets; contract boundary components only below 0.0001 mm diameter; no hole filling or MeshFix',
        contracted_boundary_diameters_mm=diameters,maximum_vertex_movement_mm=movement,volume_delta_mm3=volume,
        euler_before=int(original.euler_number),euler_after=int(result.euler_number),native_shell=native)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--half',choices=['upper','lower'],required=True)
    parser.add_argument('--native-finish',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--cad-dir',type=Path,default=INPUT)
    parser.add_argument('--extra-cut',type=Path,action='append',default=[])
    parser.add_argument('--simplify-mm',type=float,default=.0001)
    args=parser.parse_args()
    if args.out.exists(): raise RuntimeError('Use a fresh finished output directory')
    args.out.mkdir(parents=True)
    paths={kind:args.cad_dir/f'{args.half}_{kind}.stl' for kind in ['preserve','design_space','cuts']}
    shapes={k:trimesh.load(p,force='mesh') for k,p in paths.items()}
    smooth=trimesh.load(args.native_finish,force='mesh')
    if not smooth.is_volume: raise RuntimeError('Native smooth finish is not a volume')
    # Preserve double precision throughout coincident CAD cuts. The trimesh
    # float32 adapter can collapse triangulation edges on exact mating faces.
    bodies={k:solid(mesh) for k,mesh in shapes.items()}
    native=solid(smooth)
    # design_space already contains the exact functional-void subtraction.
    # Subtracting the same coincident surfaces twice creates zero-width sheets.
    exact_body=(native+bodies['preserve'])^bodies['design_space']
    for cut in args.extra_cut:
        exact_body=exact_body-solid(trimesh.load(cut,force='mesh'))
    # Remove numerical edges below 0.1 micrometre in model units. This is a
    # bounded simplification of the Boolean surface, not reconstruction.
    result=surface(exact_body.set_tolerance(min(args.simplify_mm,1e-5)).simplify(args.simplify_mm))
    target=args.out/f'{args.half}_finished_exact.stl'
    target.write_text(trimesh.exchange.stl.export_stl_ascii(result),encoding='ascii')
    result=trimesh.load(target,force='mesh')
    # Coincident CAD boundaries may emit disconnected, double-sided sheets.
    # They have no physical thickness; reject any loss of real solid material.
    components=result.split(only_watertight=False)
    physical=[mesh for mesh in components if abs(float(mesh.volume))>1e-6]
    debris=[mesh for mesh in components if abs(float(mesh.volume))<=1e-6]
    debris_volume=sum(abs(float(mesh.volume)) for mesh in debris)
    if len(physical)!=1 or debris_volume>1e-6:
        raise RuntimeError('CAD restoration produced disconnected physical material')
    cleanup=dict(zero_volume_sheets=len(debris),discarded_absolute_volume_mm3=debris_volume,
        discarded_double_sided_area_mm2=sum(float(mesh.area) for mesh in debris))
    result=physical[0]
    target.write_text(trimesh.exchange.stl.export_stl_ascii(result),encoding='ascii')
    result,cleanup['edge_flip_and_short_faces']=numeric_cleanup(result)
    result,cleanup['solver_grid']=solver_grid_cleanup(result)
    target.write_text(trimesh.exchange.stl.export_stl_ascii(result),encoding='ascii')
    result=trimesh.load(target,force='mesh')
    exact=solid(result)
    missing=surface(bodies['preserve']-exact)
    outside=surface(exact-bodies['design_space'])
    void=surface(exact^bodies['cuts'])
    def volume(mesh): return 0. if mesh is None or mesh.is_empty else max(0.,float(mesh.volume))
    failures=[]
    geometry=dict(watertight=bool(result.is_watertight),winding_consistent=bool(result.is_winding_consistent),
        components=len(result.split()),zero_area_triangles=int(np.sum(result.area_faces<1e-12)),
        volume_mm3=float(result.volume),dimensions_mm=result.extents.tolist(),bounds_mm=result.bounds.tolist(),
        preserve_missing_mm3=volume(missing),outside_envelope_mm3=volume(outside),functional_void_overlap_mm3=volume(void),
        native_smooth_volume_mm3=float(smooth.volume),numerical_cleanup=cleanup)
    geometry['surface_simplification_tolerance_mm']=args.simplify_mm
    from topopt.geom import shell_report
    geometry['native_shell_1e5_mm_weld']=shell_report(result.triangles,intersections=False)
    if not result.is_volume or geometry['components']!=1 or geometry['zero_area_triangles']:
        failures.append('Mesh must be one closed consistently wound volume without zero faces')
    if not geometry['native_shell_1e5_mm_weld']['closed_shell']:
        failures.append('Native 0.00001 mm weld shell check')
    for key in ['preserve_missing_mm3','outside_envelope_mm3','functional_void_overlap_mm3']:
        if geometry[key]>.1: failures.append(key)
    if abs(result.extents[2]-160)>.001: failures.append('axial_length')
    report=dict(status='exploration_only',geometry_result='FAIL' if failures else 'PASS',
        structural_result='NOT_CHECKED',printing_result='NOT_CHECKED',geometry=geometry,failures=failures,
        method='Native extract density smoothing, exact preserve union, original CAD envelope intersection containing functional voids; Boolean surface simplification tolerance 0.0001 mm',
        inputs_sha256={str(p):sha(p) for p in [Path(__file__),args.native_finish,*paths.values(),*args.extra_cut]},
        output_sha256=sha(target),output=str(target))
    (args.out/'geometry_validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))
    if failures: raise RuntimeError('Finished geometry failed; do not adopt')

if __name__=='__main__': main()
