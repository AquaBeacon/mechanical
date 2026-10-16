"""Re-triangulate coplanar regions for manageable faceted STEP output.

The authoritative print STL is read only. Manifold simplifies at zero requested
tolerance; curved geometry is retained to its recorded numerical tolerance.
"""
from pathlib import Path
import argparse,hashlib,json
import manifold3d as mf
import numpy as np
import trimesh
from clean_stl_degenerates import precision_weld,clean


def compact(source,out,report):
    source,out,report=Path(source),Path(out),Path(report)
    original=trimesh.load(source,force='mesh')
    if not original.is_watertight or not original.is_winding_consistent:
        raise ValueError('STEP input must be a closed, consistently wound mesh')
    solid=mf.Manifold(mf.Mesh64(original.vertices,np.asarray(original.faces,dtype=np.uint64)))
    reduced=solid.simplify(0)
    if reduced.status()!=mf.Error.NoError or reduced.get_tolerance()>1e-7:
        raise ValueError('Coplanar simplification status/tolerance rejected')
    raw=reduced.to_mesh64()
    result=trimesh.Trimesh(raw.vert_properties[:,:3],raw.tri_verts,process=False)
    # Float32 STL can exceed the strict volume tolerance on a large plate even
    # when vertices move only micrometres. Keep solver doubles through cleanup.
    out.parent.mkdir(parents=True,exist_ok=True);result.export(out,file_type='stl_ascii')
    weld=precision_weld(out,allow_collinear=True,binary=False)
    flip=clean(out,binary=False)
    result=trimesh.load(out,force='mesh')
    volume=abs(result.volume-original.volume)
    bounds=float(np.max(np.abs(result.bounds-original.bounds)))
    # Audit a deterministic set of vertices and face centres in both directions.
    maximum=0.
    for src,dst in [(original,result),(result,original)]:
        samples=np.vstack([src.vertices[::max(1,len(src.vertices)//1500)],
                           src.triangles_center[::max(1,len(src.faces)//1500)]])
        for start in range(0,len(samples),500):
            maximum=max(maximum,float(trimesh.proximity.closest_point(dst,samples[start:start+500])[1].max()))
    if volume>.001 or bounds>.001 or maximum>.001 or not result.is_volume:
        raise ValueError(f'Coplanar fidelity failed: volume={volume}, bounds={bounds}, surface={maximum}')
    data=dict(method='Manifold Mesh64 simplify(0), numerical weld and Edge Flip only',
              native_tolerance_mm=reduced.get_tolerance(),export_format='asciistl',source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
              output_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),triangles_before=len(original.faces),
              triangles_after=len(result.faces),volume_delta_mm3=volume,bounds_delta_mm=bounds,
              sampled_bidirectional_surface_delta_mm=maximum,weld=weld,edge_flip=flip)
    report.parent.mkdir(parents=True,exist_ok=True);report.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    return data


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('source',type=Path);parser.add_argument('--out',type=Path,required=True);parser.add_argument('--report',type=Path,required=True)
    args=parser.parse_args();data=compact(args.source,args.out,args.report)
    print(json.dumps({k:data[k] for k in ['triangles_before','triangles_after','volume_delta_mm3','sampled_bidirectional_surface_delta_mm']}))
