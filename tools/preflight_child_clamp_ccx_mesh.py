"""Run native topopt/Gmsh meshing and native quality checks before a costly solve.

No FEM, element-quality formula or acceptance threshold is implemented here.
The native verdict is retained verbatim; a separate STL/tet volume check is added.
"""
from pathlib import Path
import argparse
import hashlib
import json
import time
import trimesh
from topopt import ccx
from child_clamp_case import analysis_case

ROOT=Path(__file__).resolve().parents[1]
CASE=analysis_case(ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--surface',default='ccx_remesh_surface')
    parser.add_argument('--mesh-mm',type=float,default=8)
    parser.add_argument('--algorithm',type=int,choices=[1,10],default=10)
    parser.add_argument('--high-order-optimize',type=int,choices=[0,1,2],default=0)
    parser.add_argument('--minimum-mm',type=float)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--inspect-existing',action='store_true',help='Recover quality reporting from an already generated mesh; no meshing rerun')
    args=parser.parse_args()
    if args.minimum_mm is not None and not 0<args.minimum_mm<=args.mesh_mm:
        raise ValueError('Minimum size must be positive and no greater than the target')
    if args.out.exists() and not args.inspect_existing: raise RuntimeError('Preserve existing preflight output')
    if (args.out/'preflight.json').exists(): raise RuntimeError('Preserve existing preflight report')
    args.out.mkdir(parents=True,exist_ok=True)
    surface=CASE/(args.surface+'.stl')
    original=trimesh.load(surface,force='mesh')
    if not original.is_watertight or len(original.split())!=1:
        raise RuntimeError('Preflight requires one closed shell')
    result=dict(surface=str(surface),surface_sha256=hashlib.sha256(surface.read_bytes()).hexdigest(),
        mesh_target_mm=args.mesh_mm,algorithm=args.algorithm,
        high_order_optimize=args.high_order_optimize,second_order_linear=True,
        minimum_mm=args.minimum_mm,
        native_functions=['refine_stl','write_geo','run_gmsh','read_mesh','mesh_quality','mass_properties'])
    start=time.monotonic()
    try:
        shell=args.out/'refined_shell.stl'
        geo=args.out/'mesh.geo'; mesh=args.out/'mesh.inp'
        if not args.inspect_existing:
            result['refinement']=ccx.refine_stl(str(surface),str(shell),args.mesh_mm)
            ccx.write_geo(str(geo),str(shell),args.mesh_mm,algorithm=args.algorithm)
            with geo.open('a',encoding='utf-8') as stream:
                stream.write('\nMesh.SecondOrderLinear = 1;\n')
                if args.minimum_mm is not None:
                    stream.write(f'Mesh.MeshSizeMin = {args.minimum_mm};\n')
                if args.high_order_optimize:
                    stream.write(f'Mesh.HighOrderOptimize = {args.high_order_optimize};\n')
            ccx.run_gmsh(str(geo),str(mesh))
        result['inspection_only']=args.inspect_existing
        result['generated_geo_sha256']=hashlib.sha256(geo.read_bytes()).hexdigest()
        result['generated_mesh_sha256']=hashlib.sha256(mesh.read_bytes()).hexdigest()
        data=ccx.read_mesh(str(mesh))
        result['nodes']=len(data['ids'])
        result['native_quality']=ccx.mesh_quality(data['xyz'],data['elements'],ids=data['ids'])
        result['native_mass_properties']=ccx.mass_properties(data['xyz'],data['elements'],1250,ids=data['ids'])
        result['relative_stl_volume_error']=float(abs(result['native_mass_properties']['volume_mm3']-original.volume)/original.volume)
        result['volume_matches_stl']=bool(result['relative_stl_volume_error']<.001)
        result['pass_check']=bool(result['native_quality']['pass'] and result['volume_matches_stl'])
    except Exception as exc:
        result.update(pass_check=False,error=str(exc))
    result['elapsed_seconds']=time.monotonic()-start
    (args.out/'preflight.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2),flush=True)
    return 0 if result['pass_check'] else 1


if __name__=='__main__': raise SystemExit(main())
