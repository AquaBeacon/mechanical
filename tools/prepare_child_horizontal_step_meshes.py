"""Numerical STEP intermediates with micrometre-scale surface/topology checks.

Authoritative printable STL remains read only. Only a 0.0001 mm simplification
is allowed for the faceted CAD conversion; physical openings are preserved.
"""
from pathlib import Path
import hashlib,json
import manifold3d as mf
import numpy as np
import trimesh

ROOT=Path(__file__).resolve().parents[1]
folders=[(ROOT/'parts/child/exterior/printed/child_horizontal_plate_frame',['side','bottom','top','ballast_cap']),
         (ROOT/'parts/child/exterior/printed/child_wte4_petg_clamp',['upper','lower'])]
for folder,variants in folders:
    for variant in variants:
        stem=folder.name+'_'+variant;source=folder/(stem+'.stl')
        target=folder/'_work/intermediate'/(stem+'_step_simplified.stl')
        original=trimesh.load(source,force='mesh')
        model=mf.Manifold(mf.Mesh64(original.vertices,np.array(original.faces,dtype=np.uint64)))
        simplified=model.simplify(0.0001)
        if simplified.status()!=mf.Error.NoError: raise RuntimeError('Numerical STEP simplification failed')
        data=simplified.to_mesh64()
        mesh=trimesh.Trimesh(data.vert_properties[:,:3],data.tri_verts,process=False)
        target.parent.mkdir(parents=True,exist_ok=True);mesh.export(target)
        result=trimesh.load(target,force='mesh')
        delta=abs(result.volume-original.volume);box=float(np.abs(original.bounds-result.bounds).max())
        if not result.is_volume or len(result.split())!=1 or result.euler_number!=original.euler_number:
            raise RuntimeError(f'STEP topology changed: {stem}')
        maximum=0
        for start,end in [(original,result),(result,original)]:
            points=np.vstack([start.vertices[::max(1,len(start.vertices)//2000)],
                              start.triangles_center[::max(1,len(start.faces)//2000)]])
            for i in range(0,len(points),500):
                maximum=max(maximum,float(trimesh.proximity.closest_point(end,points[i:i+500])[1].max()))
        if box>.001 or maximum>.001 or delta>max(.01,original.volume*1e-6):
            raise RuntimeError(f'STEP numerical fidelity failed: {stem}, {box}, {maximum}, {delta}')
        report=dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
            intermediate_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
            method='Manifold Mesh64 simplify(0.0001 mm), print STL read only',
            triangles_before=len(original.faces),triangles_after=len(result.faces),
            topology_preserved=True,euler_number=int(result.euler_number),
            bounds_delta_mm=box,sampled_bidirectional_surface_delta_mm=maximum,volume_delta_mm3=float(delta))
        audit=folder/'_work/analysis'/(stem+'_step_simplified.json');audit.parent.mkdir(parents=True,exist_ok=True)
        audit.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
        print(stem,json.dumps(report),flush=True)
