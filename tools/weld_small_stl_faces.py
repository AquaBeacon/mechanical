"""Collapse only micrometre-sized numeric sliver faces, with strict CAD audit.

No global rounding, filling, decimation or smoothing. Large collinear facets
are handled separately by the established Edge Flip cleanup.
"""
from pathlib import Path
import hashlib,json
import numpy as np
import trimesh
from scipy.spatial import cKDTree

def weld(path,report=None):
    path=Path(path);raw=path.read_bytes();original=trimesh.load(path,force='mesh')
    result=original.copy();movement_limit=1e-5
    mapping=np.arange(len(result.vertices));collapsed=0
    for _ in range(3):
        lengths=np.linalg.norm(np.roll(result.triangles,-1,axis=1)-result.triangles,axis=2).max(axis=1)
        selected=(result.area_faces<1e-12)&(lengths<movement_limit)
        if not np.any(selected): break
        parent=np.arange(len(result.vertices))
        def find(index):
            while parent[index]!=index:
                parent[index]=parent[parent[index]];index=parent[index]
            return index
        for face in result.faces[selected]:
            roots=[find(int(x)) for x in face];anchor=min(roots)
            for vertex in roots: parent[vertex]=anchor
        parent=np.array([find(i) for i in range(len(parent))])
        result.faces=parent[result.faces];faces=result.faces
        result.update_faces((faces[:,0]!=faces[:,1])&(faces[:,1]!=faces[:,2])&(faces[:,0]!=faces[:,2]))
        result.update_faces(result.unique_faces());result.remove_unreferenced_vertices()
        collapsed+=int(selected.sum())
    data=result.export(file_type='stl')
    import io
    result=trimesh.load(io.BytesIO(data),file_type='stl',force='mesh')
    movement=float(cKDTree(result.vertices).query(original.vertices)[0].max())
    volume=abs(float(result.volume-original.volume));bounds=float(np.abs(result.bounds-original.bounds).max())
    if not result.is_volume or len(result.split())!=1 or result.euler_number!=original.euler_number or movement>1e-5 or volume>.001 or bounds>.001:
        raise RuntimeError(f'Local sliver weld rejected: {movement}, {volume}, {bounds}, euler {original.euler_number}/{result.euler_number}')
    info=dict(method='Merge vertices only on faces with area<1e-12 mm2 and all edges<1e-5 mm; remove collapsed/duplicate facets',
        sliver_faces_collapsed=collapsed,triangles_before=len(original.faces),triangles_after=len(result.faces),
        maximum_vertex_movement_mm=movement,volume_delta_mm3=volume,bounds_delta_mm=bounds,
        euler_number=int(result.euler_number),raw_sha256=hashlib.sha256(raw).hexdigest(),
        output_sha256=hashlib.sha256(data).hexdigest())
    if report:
        report=Path(report);report.parent.mkdir(parents=True,exist_ok=True)
        report.write_text(json.dumps(info,indent=2)+'\n',encoding='utf-8')
    path.write_bytes(data)
    return info
