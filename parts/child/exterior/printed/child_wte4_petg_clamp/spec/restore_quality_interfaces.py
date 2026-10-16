"""Restore only nut entry routes and screw seats after surface remeshing."""
from pathlib import Path
import argparse, hashlib, json, subprocess
import numpy as np
import trimesh
from manifold3d import Manifold, Mesh64
from topopt.geom import shell_report

PART=Path(__file__).resolve().parents[1]
ROOT=PART.parents[4]

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source',type=Path,required=True)
    ap.add_argument('--half',choices=['upper','lower'],required=True)
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args()
    args.out.mkdir(parents=True,exist_ok=False)
    work=PART/'_work/intermediate/topology_print'
    scad=work/f'{args.half}_quality_interface_cuts.scad'
    scad.write_text(f'''// Functional voids only; never a replacement topology.
include <{(ROOT/'scad/lib/child_horizontal_plate_interfaces.scad').as_posix()}>
use <{(PART/'child_wte4_petg_clamp.scad').as_posix()}>
use <{(ROOT/'scad/lib/edge_finished_profiles.scad').as_posix()}>
$fn=96;
union() {{
 for(z0=[0,120]) translate([0,0,z0]) {{
  // Add 0.05 mm finishing clearance per side to the M3 nut entries.
  // Side flats remain parallel and retain the ordinary nut against rotation.
  for(x=hf_mount_x,dy=hf_mount_axial) {{
   z=hf_clamp_width/2+dy;
   a=dy<0 ? -20 : z-(hf_nut_af+0.1)/cos(30)/2;
   b=dy<0 ? z+(hf_nut_af+0.1)/cos(30)/2 : hf_clamp_width+20;
   translate([x-(hf_nut_af+0.1)/2,hf_mount_nut_radius-0.05,a])
    cube([hf_nut_af+0.1,hf_nut_t+0.1,b-a]);
  }}
  // A 0.05 mm local seat recess removes surface-processing bulges.
  {'for(row=hf_ear_rows) translate([row[0],hf_ear_height-0.05,hf_clamp_width/2+row[1]]) rotate([-90,0,0]) cylinder(r=3.6,h=5);' if args.half=='upper' else ''}
 }}
}}
''',encoding='utf-8')
    cut=args.out/'interface_cuts.stl'
    run=subprocess.run(['C:/Program Files/OpenSCAD/openscad.exe','--export-format','asciistl','-o',str(cut),str(scad)],capture_output=True,text=True)
    (args.out/'cad.log').write_text(run.stdout+run.stderr,encoding='utf-8')
    if run.returncode or 'WARNING:' in run.stderr or 'ERROR:' in run.stderr:
        raise RuntimeError('Functional CAD cuts failed')
    def solid(m):
        return Manifold(Mesh64(np.asarray(m.vertices,dtype=np.float64),np.asarray(m.faces,dtype=np.uint64)))
    original=trimesh.load(args.source,force='mesh')
    body=solid(original)-solid(trimesh.load(cut,force='mesh'))
    data=body.to_mesh64()
    result=trimesh.Trimesh(data.vert_properties[:,:3],data.tri_verts,process=False)
    target=args.out/'finished_interfaces.stl'
    target.write_text(trimesh.exchange.stl.export_stl_ascii(result),encoding='ascii')
    result=trimesh.load(target,force='mesh')
    # A submicron weld is permitted only if it preserves the closed topology.
    result.merge_vertices(digits_vertex=5)
    result.update_faces(result.nondegenerate_faces());result.update_faces(result.unique_faces())
    result.remove_unreferenced_vertices()
    target.write_text(trimesh.exchange.stl.export_stl_ascii(result),encoding='ascii')
    native=shell_report(result.triangles,intersections=False)
    r=dict(status='exploration_only',source=str(args.source),
        source_sha256=hashlib.sha256(args.source.read_bytes()).hexdigest(),
        output_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
        native_shell=native,euler=[int(original.euler_number),int(result.euler_number)],
        volume_removed_mm3=float(original.volume-result.volume),dimensions_mm=result.extents.tolist(),
        nut_entry_flats_mm=5.9,nut_entry_depth_mm=2.9,upper_washer_seat_recess_mm=.05,
        method='Local functional finishing: nut entry clearance +0.05 mm per side and upper washer seat recess 0.05 mm; no global body reconstruction')
    r['pass']=bool(result.is_volume and native['closed_shell'] and r['euler'][0]==r['euler'][1] and 0<=r['volume_removed_mm3']<200)
    (args.out/'interface_validation.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(r),flush=True)
    if not r['pass']: raise RuntimeError('Local interface restoration rejected')

if __name__=='__main__':main()
