"""Prepare clamp studies and closed-form checks from OpenSCAD's interface echo.

FEA itself is delegated to the installed topopt CLI, never reimplemented here.
Run after build.ps1. Provisional assembly placement is kept in placement.json.
"""
from pathlib import Path
import ast
import hashlib
import json
import math
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT / "parts/child/exterior/printed/child_wte4_suspension_clamp"
ASSEMBLY = ROOT / "assemblies/child_clamp_suspension"


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    mass,g,share,shock,mu,retention=4,9.80665,0.5,4,0.15,0.5
    demand=mass*g*share*shock
    work = PART / "_work"
    csg = work / "intermediate/interface.csg"
    csg.parent.mkdir(parents=True, exist_ok=True)
    run = subprocess.run([r"C:\Program Files\OpenSCAD\openscad.com", "-o", str(csg),
                          str(PART / "child_wte4_suspension_clamp.scad")],
                         capture_output=True, text=True, check=True)
    echo = next(x.removeprefix("ECHO: ") for x in (run.stdout+run.stderr).splitlines()
                if x.startswith('ECHO: ["CLAMP_INTERFACE"'))
    values = ast.literal_eval(echo)
    d = dict(zip(values[1::2], values[2::2]))
    save(work / "analysis/interface.json", d)
    r = d["inner_r"]
    regions, mounts, ears, pressure, axial = {}, [], [], [], []
    for ix, x in enumerate([-d["frame_pitch_x"]/2, d["frame_pitch_x"]/2]):
        for iz, z in enumerate(d["bolt_zs"]):
            name = f"frame_hole_{ix}_{iz}"
            regions[name] = dict(type="cylinder", axis="Y", centre=[x,0,z], r=2.1,
                                 range=[d["mount_y"]-0.1,d["shoulder_y"]+0.1])
            mounts.append(dict(region=name,fix="xyz"))
    # Only fastener bore skins are fixed, no whole mounting pad or ground face.
    # Surface mapping must be selected on the ccx command line.
    scad_text = (PART / "child_wte4_suspension_clamp.scad").read_text(encoding="utf-8")
    import re
    def scalar(name):
        return float(re.search(rf"^\s*{name}\s*=\s*([\d.]+)\s*;",scad_text,re.M)[1])
    ear_y = -scalar("ear_t")-scalar("split_gap")/2
    preload = 150.0  # N per screw, torque is only an approximate starting point
    for ix, x in enumerate([-d["bolt_x"],d["bolt_x"]]):
        for iz,z in enumerate(d["bolt_zs"]):
            name=f"clamp_washer_{ix}_{iz}"
            regions[name]=dict(type="cylinder",axis="Y",centre=[x,0,z],r=scalar("clamp_washer_d")/2,
                               range=[ear_y-0.05,ear_y+0.12])
            ears.append(dict(region=name,force=[0,preload,0]))
    angles=[math.radians(-15-30*i) for i in range(6)]
    radial_force = 4*preload / -sum(math.sin(a) for a in angles)
    for i,a in enumerate(angles):
        name=f"rubber_contact_{i}"
        regions[name]=dict(type="cylinder",axis="Z",centre=[(r-10)*math.cos(a),(r-10)*math.sin(a),0],
                           r=15.5,range=[2,d["band_width"]-2])
        pressure.append(dict(region=name,force=[radial_force*math.cos(a),radial_force*math.sin(a),0]))
        axial.append(dict(region=name,force=[0,0,-demand/6]))
    def case(name,load,abnormal=False):
        return dict(name=name,load_class="abnormal" if abnormal else "normal",
                    supports=mounts,loads=load)
    equivalent_moment_arm=40.0 # adds centre-of-vessel eccentricity missing on rear half
    def with_pressure(axial_factor=0,lateral_factor=0,include_preload=True):
        # Merge components per region: duplicate CLOAD node/dof records may
        # overwrite rather than add in CalculiX. Keep contact away from supports.
        result=[]
        axial_moment=demand*equivalent_moment_arm*axial_factor
        lateral_moment=demand*equivalent_moment_arm*lateral_factor
        for i,e in enumerate(ears):
            xsign=-1 if i<2 else 1
            zsign=-1 if i%2==0 else 1
            fy=(preload if include_preload else 0)+zsign*axial_moment/(2*(d["bolt_zs"][1]-d["bolt_zs"][0]))-xsign*lateral_moment/(4*d["bolt_x"])
            result.append(dict(region=e["region"],force=[0,fy,0]))
        return result+[{"region":p["region"],"force":[(p["force"][0] if include_preload else 0)-a["force"][2]*lateral_factor,
                          p["force"][1] if include_preload else 0,a["force"][2]*axial_factor]}
                      for p,a in zip(pressure,axial)]
    cases=[case("static_1g_50percent",with_pressure(axial_factor=0.25,include_preload=False)),
           case("axial_4g_50percent",with_pressure(axial_factor=1,include_preload=False),True),
           case("preload_plus_static_1g",with_pressure(axial_factor=0.25)),
           case("preload_plus_axial_4g",with_pressure(axial_factor=1),True),
           case("preload_plus_lateral_4g",with_pressure(lateral_factor=1),True)]
    stl=PART / "child_wte4_suspension_clamp_half.stl"
    study=dict(units="mm_N_MPa",part=str(stl),material="PETG",build_axis="Z",raster_axis="X",
               infill=1.0,walls=8,printer="X1C",safety_factor=5.0,max_deflection_mm=1.0,
               resolution_mm=4,regions=regions,cases=cases,
               _what="One printed half conservatively carries the entire one-clamp vessel load",
               _why="3 clamps, 4 kg in air, worst clamp share 50%, handling acceleration 4g",
               _boundary="Rigid mating frame and M3 shafts fixed at FOUR frame hole skins; --map surface. No floor support.",
               _limits="Generic dry PETG card, no rubber contact solver, no bolt elasticity, no creep or wet knockdown. 6 contact patches replace uniform radial pressure. Preload is assumed, not predicted from interference or torque.",
               _part_sha256=hashlib.sha256(stl.read_bytes()).hexdigest())
    study["_moment"]="Rear-half force patches alone underestimate vessel eccentricity. A pure couple F*40 mm at clamp washer rows adds the missing vessel-centre moment. Combined effective CG is slightly forward of tube centre (about +3 mm Y). Nominal frame-to-tube-centre distance 85.35 mm."
    save(work / "analysis/study_mount.json",study)
    # Cap load path: same part, attached only by the four clamping bolts.
    cap=json.loads(json.dumps(study))
    cap_supports=[]
    for ix,x in enumerate([-d["bolt_x"],d["bolt_x"]]):
        for iz,z in enumerate(d["bolt_zs"]):
            name=f"cap_bolt_{ix}_{iz}"
            cap["regions"][name]=dict(type="cylinder",axis="Y",centre=[x,0,z],r=2.1,range=[ear_y-0.1,-scalar("split_gap")/2+0.1])
            cap_supports.append(dict(region=name,fix="xyz"))
    cap["cases"]=[dict(name="cap_axial_4g_to_clamp_bolts",load_class="abnormal",supports=cap_supports,loads=axial),
                  dict(name="cap_pressure_plus_static_1g",load_class="normal",supports=cap_supports,
                       loads=[dict(region=p["region"],force=[p["force"][0],p["force"][1],a["force"][2]*.25]) for p,a in zip(pressure,axial)]),
                  dict(name="cap_pressure_plus_axial_4g",load_class="abnormal",supports=cap_supports,
                       loads=[dict(region=p["region"],force=[p["force"][0],p["force"][1],a["force"][2]]) for p,a in zip(pressure,axial)])]
    cap["_boundary"]="Cap friction force to four clamp bolts, then mounting half and its four frame bolts. Rigid shaft skin supports."
    save(work / "analysis/study_cap.json",cap)
    # Same geometry: run the cap case on the same three meshes to avoid remeshing.
    study["regions"].update({k:v for k,v in cap["regions"].items() if k.startswith("cap_bolt_")})
    study["cases"].extend(cap["cases"])
    study["_cap_case"]="Last THREE cases use clamp bolt bores; first FIVE cases use only FOUR frame bores."
    save(work / "analysis/study_mount.json",study)
    normal=math.pi*4*preload
    p=2*preload/(d["band_width"]*r)
    washer_area=math.pi*(scalar("clamp_washer_d")**2-3.5**2)/4
    # Conservative local ear cantilever, two bolts across axial width.
    # Root reference inner radius deliberately uses longer lever than real junction.
    lever=d["bolt_x"]-r
    ear_stress=6*(2*preload)*lever/(d["band_width"]*scalar("ear_t")**2)
    hand=dict(mass_kg=mass,gravity_m_s2=g,number_of_clamps=3,worst_clamp_load_share=share,
              nominal_equal_force_N=mass*g/3,worst_static_force_N=mass*g*share,
              handling_force_per_clamp_N=demand,handling_g=shock,
              clamp_screws_per_ring=4,preload_N_per_screw=preload,
              assumed_nut_factor_K=0.2,approx_torque_Nm=0.2*preload*0.003,
              ideal_normal_force_per_clamp_N=normal,assumed_retained_preload_fraction=retention,
              assumed_wet_friction_coefficient=mu,friction_capacity_N=normal*retention*mu,
              friction_safety_factor_4g=normal*retention*mu/demand,
              minimum_mu_at_retention_half=demand/(normal*retention),
              minimum_retained_fraction_at_mu_015=demand/(normal*mu),
              nominal_rubber_pressure_MPa=p,
              ear_nominal_bending_MPa=ear_stress,ear_assumed_Kt=2.0,
              ear_local_bending_MPa=ear_stress*2,washer_preload_bearing_MPa=preload/washer_area,
              frame_holes_per_clamp=4,frame_bolt_force_with_50percent_two_bolt_sharing_N=demand/2,
              frame_hole_bearing_MPa=(demand/2)/(3*scalar("washer_shoulder_depth")),
              frame_eccentricity_to_vessel_centre_mm=-d["mount_y"],
              frame_moment_at_4g_Nmm=demand*(-d["mount_y"]),
              frame_upper_bolt_tension_from_moment_N=demand*(-d["mount_y"])/(2*(d["bolt_zs"][1]-d["bolt_zs"][0])),
              frame_assumed_preload_N_per_screw=preload,
              frame_washer_OD_mm=9,
              frame_washer_combined_bearing_4g_MPa=(preload+demand*(-d["mount_y"])/(2*(d["bolt_zs"][1]-d["bolt_zs"][0])))/(math.pi*(9**2-scalar("m3_clearance")**2)/4),
              added_axial_moment_Nmm=demand*equivalent_moment_arm,
              max_clamp_bolt_force_4g_N=preload+demand*equivalent_moment_arm/(2*(d["bolt_zs"][1]-d["bolt_zs"][0])),
              m3_assumed_tensile_stress_area_mm2=5.03,
              clamp_screw_tension_MPa=preload/5.03,
              frame_bolt_simple_shear_MPa=(demand/2)/(math.pi*3**2/4),
              material="topopt PETG orthotropic card; E=2100/1750/1150 MPa, tensile=42/33/25 MPa, interlayer shear=14 MPa",
              limits="Closed-form provisional checks; creep/wet adhesion/actual preload need testing. Stress concentration Kt=2 is assumed. Friction model N=pi*sum bolt preload assumes a flexible, conforming, uniformly pressed ring; rigid printed-ring contact and ovality can LOWER N. Use axial pull test to verify measured capacity.")
    save(work / "analysis/hand_checks.json",hand)
    ASSEMBLY.mkdir(exist_ok=True)
    source=json.loads((ROOT / "assemblies/child_vertical_assembly/placement.json").read_text(encoding="utf-8"))
    vessel=[i for i in source["items"] if i.get("group")=="vessel"]
    items=[]
    for i,zc in enumerate([40,100,160]):
        for front,ang in [(False,0),(True,180)]:
            ops=[dict(translate=[0,0,zc-d["band_width"]/2]),dict(rotate=[0,0,ang])]
            items.append(dict(label=f"clamp_{i+1}_{'front' if front else 'rear'}",part=PART.relative_to(ROOT).as_posix(),
                              file="child_wte4_suspension_clamp_half",group="clamps",color="SteelBlue" if front else "SeaGreen",ops=ops))
            items.append(dict(label=f"rubber_{i+1}_{'front' if front else 'rear'}",part=PART.relative_to(ROOT).as_posix(),
                              file="child_wte4_suspension_clamp_liner",group="rubber",color="DimGray",ops=ops,
                              note="Compressed visualization only; buy/cut rubber sheet. Not a printed part."))
        screw_part="parts/common/interior/cots/screw"
        def hardware(label,file,x,y,z,rotation):
            items.append(dict(label=label,part=screw_part,file=file,group="hardware",color="Silver",
                              ops=[dict(translate=[x,y,z]),dict(rotate=rotation)]))
        for ix,x in enumerate([-d["bolt_x"],d["bolt_x"]]):
            for iz,z in enumerate(d["bolt_zs"]):
                tag=f"clamp_{i+1}_{ix}_{iz}"
                zz=zc-d["band_width"]/2+z
                hardware(tag+"_bolt","screw_m3x60",x,ear_y-1,zz,[90,0,0])
                hardware(tag+"_washer_head","screw_washer_m3_12x1",x,ear_y,zz,[90,0,0])
                hardware(tag+"_washer_nut","screw_washer_m3_12x1",x,-ear_y,zz,[-90,0,0])
                hardware(tag+"_nut","screw_nut_m3",x,-ear_y+1,zz,[-90,0,0])
    placement=dict(name=ASSEMBLY.name,status="prototype_pending_pull_and_creep_test",coordinate_system="Tube axis Z; lower tube end z=0; rear mounting faces -Y.",
                   note="New external clamp subassembly, existing WTE4 200 mm. Provisional z centres 40/100/160, frame pattern 36 x 16 mm. Frame not yet designed. Old shells are not included.",
                   groups=dict(clamps=True,rubber=True,hardware=True,vessel=True),items=items+vessel)
    save(ASSEMBLY / "placement.json",placement)
    print(json.dumps(hand,ensure_ascii=False,indent=2))


if __name__=="__main__":
    main()
