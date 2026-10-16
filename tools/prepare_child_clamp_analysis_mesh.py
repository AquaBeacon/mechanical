"""Make and bound a CAD analysis tessellation; native topopt remains the solver.

This never edits the printing mesh. Tiny CAD triangles can prevent HXT from
meshing an otherwise closed solid. MeshLab simplifies the derived surface,
with measured bidirectional deviation and unchanged native load definitions.
"""
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np
import pymeshlab
import trimesh
from child_clamp_case import analysis_case

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp'
CASE=analysis_case(PART)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--faces',type=int,nargs='+',default=[20000,40000,60000,80000])
    parser.add_argument('--method',choices=['decimate','remesh','repair','manifold'],default='decimate')
    parser.add_argument('--remesh-mm',type=float,default=.8)
    parser.add_argument('--remesh-surface-error-mm',type=float,default=.02)
    parser.add_argument('--remesh-feature-deg',type=float,default=30)
    parser.add_argument('--remesh-iterations',type=int,default=5)
    parser.add_argument('--uniform-remesh',action='store_true')
    parser.add_argument('--input-surface',type=Path,
        help='Optional derived input; all error checks remain against the original print STL')
    parser.add_argument('--keep-vertices',action='store_true',help='Collapse onto existing vertices instead of moving functional surfaces')
    args=parser.parse_args()
    if args.input_surface is not None and args.method not in ['decimate','remesh']:
        raise ValueError('Derived input is supported for MeshLab decimation/remeshing only')
    source=CASE/'finished_cage.stl'
    simplification_input=args.input_surface or source
    stem={'decimate':'ccx_surface_proxy','remesh':'ccx_remesh_surface','repair':'ccx_repaired_surface','manifold':'ccx_manifold_surface'}[args.method]
    target=CASE/(stem+'.stl')
    original=trimesh.load(source,force='mesh')
    previous=CASE/(stem+'_attempts.json')
    attempts=json.loads(previous.read_text(encoding='utf-8')) if previous.exists() else []
    for count in (args.faces if args.method=='decimate' else [-1]):
        ms=pymeshlab.MeshSet()
        ms.load_new_mesh(str(simplification_input))
        repair_record=None
        if args.method=='manifold':
            import manifold3d as mf
            solid=mf.Manifold(mf.Mesh64(original.vertices,np.asarray(original.faces,dtype=np.uint64)))
            reduced=solid.simplify(.005)
            if reduced.status()!=mf.Error.NoError: raise RuntimeError('Manifold simplification failed')
            raw=reduced.to_mesh64()
            trimesh.Trimesh(raw.vert_properties[:,:3],raw.tri_verts,process=False).export(target)
            repair_record={'method':'Manifold simplify','requested_tolerance_mm':.005,'native_tolerance_mm':reduced.get_tolerance()}
        elif args.method=='repair':
            from topopt.ccx import repair_stl
            repair_record=repair_stl(str(source),str(target))
        elif args.method=='decimate':
            ms.apply_filter('meshing_decimation_quadric_edge_collapse',targetfacenum=count,
                qualitythr=.5,preserveboundary=True,preservenormal=True,preservetopology=True,
                optimalplacement=not args.keep_vertices,planarquadric=True,autoclean=True)
        else:
            ms.apply_filter('meshing_isotropic_explicit_remeshing',iterations=args.remesh_iterations,adaptive=not args.uniform_remesh,
                targetlen=pymeshlab.PureValue(args.remesh_mm),featuredeg=args.remesh_feature_deg,checksurfdist=True,
                maxsurfdist=pymeshlab.PureValue(args.remesh_surface_error_mm),splitflag=True,collapseflag=True,
                swapflag=True,smoothflag=False,reprojectflag=True)
        if args.method not in ['repair','manifold']: ms.save_current_mesh(str(target))
        # Simplification can expose collinear facets at native STL precision.
        # The existing bounded edge-flip cleanup keeps the surface and topology;
        # measure the exported, cleaned mesh below, not its pre-cleanup input.
        from clean_stl_degenerates import clean
        cleanup=clean(target,CASE/(stem+'_degenerate_cleanup.json'))
        comparison=pymeshlab.MeshSet()
        comparison.load_new_mesh(str(source))
        comparison.load_new_mesh(str(target))
        distances=[]
        for a,b in [(0,1),(1,0)]:
            distances.append({k:float(v) for k,v in comparison.apply_filter(
                'get_hausdorff_distance',sampledmesh=a,targetmesh=b,samplevert=True,
                sampleedge=True,sampleface=True,samplenum=300000,savesample=False).items()})
        proxy=trimesh.load(target,force='mesh')
        error=abs(proxy.volume-original.volume)/original.volume
        bounds=float(np.max(np.abs(proxy.bounds-original.bounds)))
        passed=bool(proxy.is_watertight and proxy.is_winding_consistent and len(proxy.split())==1
            and error<.001 and bounds<.05 and max(d['max'] for d in distances)<.05)
        attempts.append(dict(target_faces=count,actual_faces=len(proxy.faces),distances=distances,repair=repair_record,cleanup=cleanup,arguments={k:(str(v) if isinstance(v,Path) else v) for k,v in vars(args).items()},
            relative_volume_error=float(error),max_bounds_error_mm=bounds,pass_check=passed))
        print(json.dumps(attempts[-1]),flush=True)
        previous.write_text(json.dumps(attempts,indent=2)+'\n',encoding='utf-8')
        if passed: break
    else:
        raise RuntimeError('No analysis surface met the documented approximation bounds')
    record=dict(source_print_stl_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        derivation_input=str(simplification_input),derivation_input_sha256=hashlib.sha256(simplification_input.read_bytes()).hexdigest(),
        analysis_proxy_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
        source_faces=len(original.faces),attempts=attempts,pass_check=True,
        note='Derived analysis tessellation only. Printing mesh unchanged. Sampled bidirectional distance is not a proof of a global Hausdorff bound. Interface checks required separately.')
    (CASE/(stem+'.json')).write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    study=json.loads((CASE/'study_final.json').read_text(encoding='utf-8'))
    study['part']=str(target)
    study['_part_sha256']=record['analysis_proxy_sha256']
    study['_reference_print_stl_sha256']=record['source_print_stl_sha256']
    study['_analysis_surface']=record
    (CASE/('study_'+stem+'.json')).write_text(json.dumps(study,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(record,indent=2))


if __name__=='__main__': main()
