"""Finish actual optimized connections, then join immutable existing bands once.

The native density-smoothed connecting surface is cropped with 4 mm overlap
inside each existing band. Functional CAD clipping touches that surface only.
No whole-part remeshing or reconstruction of optimized material is performed.
"""
from pathlib import Path
import argparse,hashlib,json
import numpy as np
import trimesh
from manifold3d import Manifold,Mesh64
from topopt.ccx import shell_check,refine_stl
from finish_print_topology import numeric_cleanup,solver_grid_cleanup

PART=Path(__file__).resolve().parents[1]
BASE=PART/'_work/analysis/topology_print'

def solid(m):
    return Manifold(Mesh64(np.asarray(m.vertices,dtype=np.float64),np.asarray(m.faces,dtype=np.uint64)))

def mesh(s):
    d=s.to_mesh64();return trimesh.Trimesh(d.vert_properties[:,:3],d.tri_verts,process=False)

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--half',choices=['upper','lower'],required=True)
    ap.add_argument('--native-finish',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=False)
    request=json.loads((PART/'spec/print_topology_request.json').read_text())
    width=request['interfaces']['band_width_mm'];pitch=request['interfaces']['station_pitch_mm']
    original_path=PART/f'child_wte4_petg_clamp_{args.half}.stl'
    original=trimesh.load(original_path,force='mesh')
    band,numeric=numeric_cleanup(original);band,grid=solver_grid_cleanup(band)
    second=band.copy();second.apply_translation([0,0,pitch])
    preserved=trimesh.util.concatenate([band,second]);bands=solid(preserved)
    smoothed=trimesh.load(args.native_finish,force='mesh')
    # Box only crops the native density result; it never supplies material.
    a,b=width-4,pitch+4
    crop=trimesh.creation.box(extents=[200,200,b-a],
        transform=trimesh.transformations.translation_matrix([0,50,(a+b)/2]))
    design_path=BASE/f'{args.half}_design_space.stl'
    design=solid(trimesh.load(design_path,force='mesh'))
    links=(solid(smoothed)^solid(crop))^design
    extras=[]
    if args.half=='lower':
        extra=BASE/'lower_access_tool_obstacles.stl';extras.append(extra)
        links=links-solid(trimesh.load(extra,force='mesh'))
    result=mesh((bands+links).set_tolerance(1e-5).simplify(.0001))
    path=args.out/f'{args.half}_finished_connections.stl'
    path.write_text(trimesh.exchange.stl.export_stl_ascii(result),encoding='ascii')
    result=trimesh.load(path,force='mesh')
    result,cleanup=numeric_cleanup(result);result,final_grid=solver_grid_cleanup(result)
    path.write_text(trimesh.exchange.stl.export_stl_ascii(result),encoding='ascii')
    final=solid(result);cuts_path=BASE/f'{args.half}_cuts.stl'
    missing=max(0.,float((bands-final).volume()))
    outside=max(0.,float((final-design).volume()))
    void=max(0.,float((final^solid(trimesh.load(cuts_path,force='mesh'))).volume()))
    source=PART/f'child_wte4_petg_clamp_{args.half}_linked.stl'
    baseline=trimesh.load(source,force='mesh')
    sections=[]
    for z in [width-2,width+.1,(width+pitch)/2,pitch-.1,pitch+2]:
        section=result.section(plane_origin=[0,0,z],plane_normal=[0,0,1])
        sections.append(dict(z_mm=z,loops=0 if section is None else len(section.discrete)))
    shell=shell_check(str(path));failures=[]
    if not shell['closed_shell'] or shell.get('components')!=1 or shell.get('self_intersections') not in [0,None]:failures.append('native closed single shell')
    if max(missing,outside,void)>.1:failures.append('functional geometry')
    if not result.is_volume or len(result.split())!=1 or any(r['loops']==0 for r in sections):failures.append('connected overlaps')
    if float(result.volume)>float(baseline.volume):failures.append('CAD material budget')
    report=dict(status='exploration_only',geometry_result='FAIL' if failures else 'PASS',
        method='Native actual density-smoothed links, crop with 4 mm hidden overlap, clip link material only, union unchanged CAD bands once; numerical cleanup below 0.0001 mm; no global remesh',
        source_sha256={str(p):sha(p) for p in [Path(__file__),original_path,args.native_finish,design_path,cuts_path,source,*extras]},
        output=str(path),output_sha256=sha(path),shell=shell,
        volume_mm3=float(result.volume),baseline_volume_mm3=float(baseline.volume),dimensions_mm=result.extents.tolist(),
        preserved_band_missing_mm3=missing,outside_envelope_mm3=outside,functional_void_overlap_mm3=void,
        root_and_midspan_sections=sections,band_cleanup=dict(numeric=numeric,grid=grid),
        union_cleanup=dict(numeric=cleanup,grid=final_grid),failures=failures)
    (args.out/'geometry_validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2),flush=True)
    if failures:raise RuntimeError('Finished connections rejected')

if __name__=='__main__':main()
