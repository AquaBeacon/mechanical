"""Check delivered clamp CAD geometry and real bolt/tool passage on its STL."""
import json
from pathlib import Path
import numpy as np
import trimesh
import argparse

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/"parts/child/exterior/printed/child_wte4_suspension_clamp"


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stl',type=Path)
    parser.add_argument('--out',type=Path)
    parser.add_argument('--density-g-cm3',type=float,default=1.27,help='documented filament density; default preserves historical generic PETG')
    args=parser.parse_args()
    d=json.loads((PART/"_work/analysis/interface.json").read_text())
    source=args.stl or PART/"child_wte4_suspension_clamp_half.stl"
    mesh=trimesh.load(source,force="mesh")
    checks={}
    checks['zero_area_triangles']=int(np.count_nonzero(mesh.area_faces<1e-12))
    checks['no_zero_area_triangles']=checks['zero_area_triangles']==0
    shells=mesh.split(only_watertight=False)
    outer=[shell for shell in shells if shell.volume>0]
    cavities=[shell for shell in shells if shell.volume<0]
    cavities_inside=bool(len(outer)==1 and all(outer[0].contains(shell.vertices[::max(1,len(shell.vertices)//24)]).all()
                                             for shell in cavities))
    checks["closed_boundary_shells"]=len(shells)
    checks["internal_cavity_volume_mm3"]=float(-sum(shell.volume for shell in cavities))
    checks["watertight_one_body"]=bool(mesh.is_watertight and mesh.is_winding_consistent and
                                       len(outer)==1 and cavities_inside)
    pts=mesh.vertices
    checks["tube_plastic_radial_clearance_mm"]=float(np.sqrt(pts[:,0]**2+pts[:,1]**2).min()-d["tube_od"]/2)
    checks["tube_does_not_hit_plastic"]=checks["tube_plastic_radial_clearance_mm"]>=1.19
    def passage(x,z,y0,y1,radius):
        # A full cylinder envelope verifies the actual M3 shank/tool, not just centreline.
        angles=np.linspace(0,2*np.pi,24,endpoint=False)
        ys=np.linspace(y0,y1,28)
        p=np.array([[x+radius*np.cos(a),y,z+radius*np.sin(a)] for y in ys for a in angles])
        return not mesh.contains(p).any()
    frames=[]
    access=[]
    for x in [-d["frame_pitch_x"]/2,d["frame_pitch_x"]/2]:
        for z in d["bolt_zs"]:
            frames.append(passage(x,z,d["mount_y"]-0.2,d["shoulder_y"]+0.2,1.5))
            access.append(passage(x,z,d["shoulder_y"]+0.2,0,4.0))
    checks["all_four_frame_M3_shanks_clear"]=all(frames)
    checks["all_four_inside_OD8_tool_paths_clear"]=all(access)
    checks["all_four_inside_OD9_washers_fit"]=all(passage(x,z,d["shoulder_y"]+0.1,d["shoulder_y"]+1.1,4.5)
          for x in [-d["frame_pitch_x"]/2,d["frame_pitch_x"]/2] for z in d["bolt_zs"])
    # Cast from the tool pocket upwards at the washer seat. Organic exterior
    # vertices near the top plane are not the tool-pocket ceiling.
    origins=np.array([[x,d['shoulder_y']+offset,d['bolt_zs'][-1]]
                      for x in [-d['frame_pitch_x']/2,d['frame_pitch_x']/2]
                      for offset in [0.2,0.8]])
    locations,ray_ids,_=mesh.ray.intersects_location(origins,np.tile([0,0,1],(len(origins),1)))
    roofs=[]
    for i in range(len(origins)):
        heights=np.unique(np.round(locations[ray_ids==i,2],6))
        roofs.append(float(heights[1]-heights[0]) if len(heights)>=2 else 0.0)
    checks["round_tool_pocket_roof_mm"]=min(roofs)
    checks["roof_measurement_scope"]="Tool pocket above upper washer seat; first ceiling-to-exit material segment. Organic tunnel farther inward may open."
    checks["round_tool_pocket_roof_at_least_3mm"]=checks["round_tool_pocket_roof_mm"]>=3
    checks["all_four_clamp_M3_shanks_clear"]=all(passage(x,z,-40,0,1.5) for x in [-d["bolt_x"],d["bolt_x"]] for z in d["bolt_zs"])
    liner=trimesh.load(PART/"child_wte4_suspension_clamp_liner.stl",force="mesh")
    # Interior penetration samples, excluding touching contact surfaces.
    centres=liner.triangles_center
    interior=centres-liner.face_normals*0.02
    checks["rubber_does_not_penetrate_PETG"]=not mesh.contains(interior).any()
    checks["other_half_separation_mm"]=float(-2*mesh.bounds[1,1])
    checks["three_rings_have_axial_clearance_mm"]=float(60-d["band_width"])
    checks["fits_250mm_bed_flat"]=bool(np.max(mesh.extents[:2])<250)
    checks["volume_mm3"]=float(mesh.volume)
    checks["extents_mm"]=mesh.extents.tolist()
    checks['density_g_cm3']=args.density_g_cm3
    checks["PETG_solid_mass_g_per_half"]=float(mesh.volume*args.density_g_cm3/1000)
    checks["PETG_solid_mass_g_six_halves"]=float(mesh.volume*args.density_g_cm3/1000*6)
    checks["pass"]=all(v for k,v in checks.items() if isinstance(v,bool))
    target=args.out or PART/"_work/analysis/geometry_checks.json"
    checks["source"]=str(source.resolve())
    target.write_text(json.dumps(checks,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(checks,indent=2))
    raise SystemExit(0 if checks["pass"] else 1)


if __name__=="__main__":
    main()
