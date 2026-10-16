"""Flip only numerical T-vertex degeneracies; never decimate or fill holes."""
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np
import trimesh


def precision_weld(path, report=None, allow_collinear=False, binary=True):
    """Remove only facets collapsed at the native solver's 1e-5 mm weld.

    No new faces, hole filling or decimation. The maximum vertex displacement,
    signed volume and envelope must stay within explicit micrometre bounds.
    """
    path=Path(path)
    original=trimesh.load(path,force='mesh')
    result=original.copy()
    result.merge_vertices(digits_vertex=5)
    # Rounding bins can separate vertices only a micrometre apart at a bin
    # boundary. Also merge connected edges shorter than the same tolerance.
    edges=result.edges_unique
    short=edges[np.linalg.norm(result.vertices[edges[:,0]]-result.vertices[edges[:,1]],axis=1)<1e-5]
    parent=np.arange(len(result.vertices))
    def find(index):
        while parent[index]!=index:
            parent[index]=parent[parent[index]]
            index=parent[index]
        return index
    for u,v in short:
        u=find(u);v=find(v);parent[max(u,v)]=min(u,v)
    for index in np.unique(short):
        parent[index]=find(index)
    result.faces=parent[result.faces]
    # A collinear triangle with three distinct vertices is still required for
    # closure until Edge Flip repairs it. Remove repeated IDs only.
    faces=result.faces
    result.update_faces((faces[:,0]!=faces[:,1]) & (faces[:,1]!=faces[:,2]) & (faces[:,2]!=faces[:,0]))
    result.update_faces(result.unique_faces())
    result.remove_unreferenced_vertices()
    data=(result.export(file_type='stl') if binary
          else result.export(file_type='stl_ascii').encode('ascii'))
    import io
    result=trimesh.load(io.BytesIO(data),file_type='stl',force='mesh')
    from scipy.spatial import cKDTree
    movement=float(cKDTree(result.vertices).query(original.vertices)[0].max())
    volume=abs(result.volume-original.volume)
    bounds=float(np.max(np.abs(result.bounds-original.bounds)))
    from topopt.geom import shell_report
    native=shell_report(result.triangles,intersections=False)
    if (not result.is_watertight or not result.is_winding_consistent or
        (not allow_collinear and np.any(result.area_faces<1e-12)) or not native['closed_shell'] or native['degenerate'] or
        movement>2e-5 or volume>.001 or bounds>.001):
        raise RuntimeError(f'Precision weld rejected: movement={movement}, volume={volume}, bounds={bounds}, native={native}')
    info=dict(method='Merge coordinate bins and connected edges below 1e-5 mm, remove collapsed/duplicate triangles only; no filling or new faces',
              export_format='binstl' if binary else 'asciistl',
              triangles_before=len(original.faces),triangles_after=len(result.faces),
              collinear_faces_pending_edge_flip=int(np.count_nonzero(result.area_faces<1e-12)),
              maximum_vertex_movement_mm=movement,volume_delta_mm3=volume,bounds_delta_mm=bounds,
              native_shell=native,raw_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
              cleaned_sha256=hashlib.sha256(data).hexdigest())
    if report:
        Path(report).parent.mkdir(parents=True,exist_ok=True)
        Path(report).write_text(json.dumps(info,indent=2)+'\n',encoding='utf-8')
    path.write_bytes(data)
    return info


def clean(path, report=None, binary=False):
    path=Path(path)
    original=trimesh.load(path,force='mesh')
    count=int(np.count_nonzero(original.area_faces<1e-12))
    if count==0:
        return {'changed':False,'zero_area_before':0,'zero_area_after':0}
    import pymeshlab
    ms=pymeshlab.MeshSet()
    ms.add_mesh(pymeshlab.Mesh(original.vertices,original.faces))
    # Only practically collinear triangles qualify at this aspect-ratio limit.
    # Edge Flip retains the vertices and triangle count, unlike Edge Collapse.
    ms.meshing_remove_t_vertices(method='Edge Flip',threshold=1e9,repeat=True)
    result=trimesh.Trimesh(ms.current_mesh().vertex_matrix(),ms.current_mesh().face_matrix())
    data=result.export(file_type='stl') if binary else result.export(file_type='stl_ascii').encode('ascii')
    import io
    result=trimesh.load(io.BytesIO(data),file_type='stl',force='mesh')
    area_after=int(np.count_nonzero(result.area_faces<1e-12))
    if area_after:
        raise RuntimeError(f'Edge flip left {area_after} degenerate triangles; no output written')
    # Identical triangles have identically zero surface error. Only changed
    # triangles need the expensive nearest-surface sampling, in both directions.
    _,ids=np.unique(np.vstack([original.vertices,result.vertices]),axis=0,return_inverse=True)
    keys=[]
    for mesh,vertex_ids in [(original,ids[:len(original.vertices)]),(result,ids[len(original.vertices):])]:
        faces=np.ascontiguousarray(np.sort(vertex_ids[mesh.faces],axis=1))
        keys.append(faces.view(np.dtype((np.void,faces.dtype.itemsize*3))).ravel())
    changed=[~np.isin(keys[0],keys[1]),~np.isin(keys[1],keys[0])]
    maximum=0.0
    for src,dst,mask in [(original,result,changed[0]),(result,original,changed[1])]:
        samples=np.vstack([src.triangles[mask].reshape(-1,3),src.triangles_center[mask]])
        for start in range(0,len(samples),1000):
            maximum=max(maximum,float(trimesh.proximity.closest_point(dst,samples[start:start+1000])[1].max()))
    delta=abs(result.volume-original.volume)
    bounds=float(np.max(np.abs(result.bounds-original.bounds)))
    before_shells=sorted(float(s.volume) for s in original.split())
    after_shells=sorted(float(s.volume) for s in result.split())
    if (area_after or not result.is_watertight or not result.is_winding_consistent or
        len(result.faces)!=len(original.faces) or len(before_shells)!=len(after_shells) or
        not np.allclose(before_shells,after_shells,rtol=0,atol=0.001) or
        delta>0.001 or bounds>0.001 or maximum>0.001):
        raise RuntimeError(f'Degeneracy cleanup rejected: zero_area={area_after}, watertight={result.is_watertight}, winding={result.is_winding_consistent}, faces={len(original.faces)}->{len(result.faces)}, shells={len(before_shells)}->{len(after_shells)}, volume_delta={delta}, bounds_delta={bounds}, surface_delta={maximum}')
    info=dict(changed=True,method='MeshLab T-vertex Edge Flip only; threshold 1e9; no collapse, decimation or hole filling',
              export_format='binstl' if binary else 'asciistl',zero_area_before=count,zero_area_after=area_after,triangles_before=len(original.faces),
              triangles_after=len(result.faces),volume_delta_mm3=delta,bounds_delta_mm=bounds,
              changed_triangles_sampled=[int(mask.sum()) for mask in changed],
              bidirectional_sampled_surface_delta_mm=maximum,
              raw_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
              cleaned_sha256=hashlib.sha256(data).hexdigest(),signed_shell_volumes_mm3=after_shells)
    if report:
        report=Path(report)
        report.parent.mkdir(parents=True,exist_ok=True)
        report.write_text(json.dumps(info,indent=2)+'\n',encoding='utf-8')
    path.write_bytes(data)
    return info


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('stl',type=Path)
    p.add_argument('--report',type=Path)
    p.add_argument('--configured',action='store_true',help='only act on manufacturing.json opt-in variants')
    a=p.parse_args()
    if a.configured:
        config=a.stl.parent/'manufacturing.json'
        options=json.loads(config.read_text(encoding='utf-8')) if config.exists() else {}
        if a.stl.stem in options.get('degenerate_local_sliver_weld_files',[]):
            from weld_small_stl_faces import weld as local_weld
            result=dict(local_sliver_weld=local_weld(a.stl),edge_flip=clean(a.stl,binary=True))
            if a.report:
                a.report.parent.mkdir(parents=True,exist_ok=True)
                a.report.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
            print(json.dumps(result))
            raise SystemExit(0)
        if a.stl.stem in options.get('degenerate_precision_weld_files',[]):
            # Some CSG unions contain both tiny collapsed edges and collinear
            # facets. Both opt-ins request the same validated sequence used by
            # compact_coplanar_mesh, without simplifying the print mesh.
            flip=a.stl.stem in options.get('degenerate_edge_flip_files',[])
            weld=precision_weld(a.stl,None if flip else a.report,allow_collinear=flip)
            if flip:
                result=dict(weld=weld,edge_flip=clean(a.stl,binary=True))
                if a.report:
                    a.report.parent.mkdir(parents=True,exist_ok=True)
                    a.report.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
            else:
                result=weld
            print(json.dumps(result))
            raise SystemExit(0)
        if a.stl.stem not in options.get('degenerate_edge_flip_files',[]):
            raise SystemExit(0)
        binary=options.get('stl_export_format')=='binstl'
    else:
        binary=False
    print(json.dumps(clean(a.stl,a.report,binary=binary)))
