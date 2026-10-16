"""Build and geometrically check the small trial interfaces (no load rating).

python tools/build_quick_release_prototypes.py [--no-step]
SCAD is authoritative; placement.json is authoritative for assembly layout.
"""
from pathlib import Path
import argparse
import json
import os
import subprocess
import sys
import re
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT / "parts/common/jigs/quick_release_prototypes"
ASM = ROOT / "assemblies/quick_release_trials"
SCAD = PART / "quick_release_prototypes.scad"
OSC = Path(r"C:\Program Files\OpenSCAD\openscad.exe")
FC = Path(r"C:\Users\ryupc\AppData\Local\Programs\FreeCAD 1.0\bin\freecadcmd.exe")
KINDS = ["slide_male", "slide_female", "slide_gib", "snap_male", "snap_female", "twist_male", "twist_female", "knob", "twist_knob"]


def hardware():
    """Read scalar hardware dimensions from the CAD source for matching test fixtures."""
    source = SCAD.read_text(encoding="utf-8")
    values = {}
    for key in ["turn_deg", "twist_cam_lift", "twist_pad_compression", "twist_pad_t", "twist_pad_depth", "twist_pad_side_clearance", "twist_pad_w", "twist_pad_l", "twist_pad_r", "ring_h", "slide_plate_t", "twist_plate_t", "slide_nut_x", "twist_nut_x", "bolt_nominal", "slide_bolt_length", "twist_bolt_length", "head_seat", "thread_pitch", "unlock_turns", "hex_af", "washer_t", "metal_nut_t", "slide_cheek_x", "slide_gib_x", "slide_opening", "twist_face_x", "twist_axis_z", "mount_pitch", "mount_d", "pad_t", "snap_entry", "snap_tab_l", "snap_end", "snap_floor", "snap_t"]:
        match = re.search(rf"(?m)^\s*{key}\s*=\s*(-?[0-9.]+)\s*;", source)
        if not match:
            raise ValueError(f"Missing scalar hardware parameter: {key}")
        values[key] = float(match.group(1))
    values["twist_lock_gap"] = values["twist_pad_t"]-values["twist_pad_depth"]-values["twist_pad_compression"]
    return values


def run(args, log, env=None, allow_empty=False):
    result = subprocess.run(list(map(str, args)), cwd=ROOT, capture_output=True,
                            encoding="utf-8", errors="replace", env=env,
                            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text(result.stdout + result.stderr, encoding="utf-8")
    output = result.stdout + result.stderr
    if any(marker in output for marker in ["ERROR:", "WARNING:", "Traceback (most recent call last)", "Exception while processing file:"]):
        raise RuntimeError(f"CAD error/warning: {log}")
    if result.returncode and not (allow_empty and "Current top level object is empty" in output):
        raise RuntimeError(f"exit {result.returncode}: {log}")
    return output


def check_mesh(path, expected=None):
    mesh = trimesh.load(path, force="mesh")
    if not mesh.is_watertight or not mesh.is_winding_consistent or mesh.volume <= 0:
        raise RuntimeError(f"Invalid solid: {path}")
    if len(mesh.split()) != 1:
        raise RuntimeError(f"Disconnected printable part: {path}")
    if expected is not None and not np.allclose(mesh.extents, expected, atol=0.06):
        raise RuntimeError(f"Wrong dimensions {mesh.extents}: {path}")
    return {"bounds_mm": mesh.bounds.round(4).tolist(), "volume_mm3": round(float(mesh.volume), 3),
            "watertight": True, "single_body": True, "faces": len(mesh.faces)}


def collision_checks(reuse=False, prefix=None):
    """Sample insertion envelopes; spring shear approximates clearance only."""
    work = ASM / "_work/analysis/fit"
    work.mkdir(parents=True, exist_ok=True)
    cases = []
    for t in [0, 2, 5, 10, 15, 20, 25, 30]:
        cases.append((f"slide_{t}", f'seated_male("slide",travel={t})', 'union() {receiver("slide"); slide_gib(opening=1); metal_stack("slide",loosen=1); placed_knob("slide",loosen=1);}'))
    cases.append(("slide_gib_open", 'slide_gib(opening=1)', 'receiver("slide")'))
    cases.append(("snap_seated", 'seated_male("snap")', 'receiver("snap")'))
    for t in [0, 2, 5, 10, 15, 20, 25, 30, 40]:
        cases.append((f"snap_squeezed_{t}", f'seated_male("snap",travel={t},squeeze=6)', 'receiver("snap")'))
    turn=int(hardware()["turn_deg"])
    for a in range(-turn, 1, 5):
        cases.append((f"twist_turn_{a}", f'seated_male("twist",angle={a})', 'receiver("twist")'))
    for t in [0, 1, 3, 5, 8, 12, 16, 24]:
        cases.append((f"twist_entry_{t}", f'seated_male("twist",travel={t},angle={-turn})', 'receiver("twist")'))
    for kind in ["slide", "twist"]:
        for t in [0,2,5,8]:
            cases.append((f"{kind}_nut_loading_{t}", f'translate([0,0,{t}]) fixed_nut("{kind}",bearing_margin=0.01)', f'receiver("{kind}")'))
        metal = f'metal_stack("{kind}",bearing_margin=0.01)'
        gib = 'slide_gib();' if kind=="slide" else ''
        plastic = f'union() {{ receiver("{kind}"); seated_male("{kind}",clamped=true); {gib} placed_knob("{kind}"); }}'
        cases.append((f"{kind}_shaft_fit", metal, plastic))
        cases.append((f"{kind}_knob_clearance", f'placed_knob("{kind}")', f'seated_male("{kind}",clamped=true)'))
    # Side pin must be removed before turning; verify its extraction and insertion path.
    for t in [0,2,5,10,20,30,40,55]:
        cases.append((f"twist_bolt_withdraw_{t}", f'translate([{t},0,0]) through_bolt("twist",bearing_margin=0.01,include_washer=false)',
                      'union() { receiver("twist"); seated_male("twist"); }'))
    cases.append(("twist_compressed_pad_fit", 'twist_pad_reference(compressed=true,bearing_margin=0.01)',
                  'union() { receiver("twist"); seated_male("twist"); metal_stack("twist"); }'))
    cases.append(("twist_pad_entry_clearance", f'twist_pad_reference(compressed=false,bearing_margin=0.01,angle={-turn})', 'receiver("twist")'))
    for a in range(-turn,-10,5):
        cases.append((f"twist_pad_rotate_{a}", f'twist_pad_reference(compressed=false,bearing_margin=0.01,angle={a})', 'receiver("twist")'))
    if prefix is not None:
        cases=[case for case in cases if case[0].startswith(prefix)]
    def check_case(case):
        name, male, female = case
        # Use the just-rendered, closed native receiver mesh. This avoids
        # rebuilding the many swept groove hulls for every sampled position.
        for kind in ["slide", "snap", "twist"]:
            expression = f'import("{(PART / ("quick_release_prototypes_"+kind+"_female.stl")).as_posix()}")'
            male = male.replace(f'receiver("{kind}")',expression)
            female = female.replace(f'receiver("{kind}")',expression)
        source = work / (name + ".scad")
        out = work / (name + ".stl")
        code = f"use <{SCAD.as_posix()}>\nintersection() {{ {male}; {female}; }}\n"
        log = work / (name + ".log")
        if reuse:
            stamp = max(SCAD.stat().st_mtime_ns, (ROOT / "scad/lib/util.scad").stat().st_mtime_ns,
                        *( (PART / ("quick_release_prototypes_"+kind+"_female.stl")).stat().st_mtime_ns for kind in ["slide","snap","twist"]))
            if not source.exists() or source.read_text(encoding="utf-8") != code or not log.exists() or log.stat().st_mtime_ns < stamp:
                raise RuntimeError(f"Missing/stale fit check: {name}; rerun without --finish-existing")
            result = log.read_text(encoding="utf-8")
            if "Current top level object is empty" not in result or "WARNING:" in result or "ERROR:" in result:
                raise RuntimeError(f"Fit check not clean: {name}")
            return
        source.write_text(code, encoding="utf-8")
        # Remove only this script's prior intersection output, not design meshes.
        if out.exists():
            out.unlink()
        result = run([OSC, "-o", out, source], work / (name + ".log"), allow_empty=True)
        if "Current top level object is empty" not in result:
            # Nominal seating faces can touch, but may not overlap in volume.
            contact = trimesh.load(out, force="mesh")
            if abs(float(contact.volume)) > 1e-5:
                raise RuntimeError(f"Unintended interference: {name}; see {work}")
    with ThreadPoolExecutor(max_workers=3) as pool:
        list(pool.map(check_case, cases))
    return [name for name, _, _ in cases]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--no-step", action="store_true")
    ap.add_argument("--steps-only", action="store_true", help="Convert already verified source STL to STEP")
    ap.add_argument("--finish-existing", action="store_true", help="Finish a partial build using only current STL and clean matching fit logs")
    args = ap.parse_args()
    logs = PART / "_work/logs"
    intermediate = PART / "_work/intermediate"
    intermediate.mkdir(parents=True, exist_ok=True)
    metrics = {}
    expected = {"slide_male": [40, 40, 16], "slide_female": [40, 40, 16.2], "slide_gib": [11.5,20,8.4],
                "snap_male": [40, 48, 4], "snap_female": [40, 39, 10],
                "twist_male": [40, 40, 14], "twist_female": [40, 40, 18], "knob": [22, 19.7224, 10], "twist_knob": [16,14.5263,10]}
    if args.steps_only:
        for kind in KINDS:
            stem = "quick_release_prototypes_"+kind
            stl = PART / (stem+".stl")
            check_mesh(stl, expected[kind])
            env = os.environ.copy()
            env.update(STL_IN=str(stl), STEP_OUT=str(stl.with_suffix(".step")))
            run([FC, ROOT / "scad/lib/stl_to_step.py"], logs / (stem+"_faceted.log"), env)
        run([FC, ROOT / "tools/verify_quick_release_steps.py"], ASM / "_work/logs/step_verify.log")
        export_assembly_step()
        return
    for kind in KINDS:
        stem = "quick_release_prototypes_" + kind
        stl = PART / (stem + ".stl")
        if args.finish_existing:
            if not stl.exists() or stl.stat().st_mtime_ns < SCAD.stat().st_mtime_ns:
                raise RuntimeError(f"Stale STL: {stl}")
        else:
            # The finely triangulated sloping C groove requires binary precision.
            # Keep other exports in the established ASCII format for STEP sewing.
            fmt = "binstl" if kind=="twist_female" else "asciistl"
            run([OSC, "--export-format", fmt, "-D", f'part="{kind}"', "-o", stl, SCAD], logs / (stem + ".log"))
        metrics[kind] = check_mesh(stl, expected[kind])
        print(f"PASS solid {kind}", flush=True)
        if not args.no_step:
            csg = intermediate / (stem + ".csg")
            step = PART / (stem + ".step")
            run([OSC, "-D", f'part="{kind}"', "-o", csg, SCAD], logs / (stem + "_csg.log"))
            env = os.environ.copy()
            env.update(OPENSCAD=str(OSC), CSG_IN=str(csg), STEP_OUT=str(step), STL_REF=str(stl))
            stamp = csg.stat().st_mtime_ns
            try:
                run([FC, ROOT / "scad/lib/csg_to_step.py"], logs / (stem + "_step.log"), env)
            except RuntimeError:
                print(f"CSG import fallback for {kind}", flush=True)
            if not step.exists() or step.stat().st_mtime_ns < stamp:
                env.update(STL_IN=str(stl))
                run([FC, ROOT / "scad/lib/stl_to_step.py"], logs / (stem + "_faceted.log"), env)
            if not step.exists() or step.stat().st_mtime_ns < stamp:
                raise RuntimeError(f"STEP not updated: {step}")
    cases = collision_checks(reuse=args.finish_existing)
    check_locking()
    clamped = check_clamped_assembly()
    check_mounting_holes()
    check_pad_bond_surfaces()
    if not args.no_step:
        run([FC, ROOT / "tools/verify_quick_release_steps.py"], ASM / "_work/logs/step_verify.log")
    run([sys.executable, ROOT / "scad/lib/asm_gen.py", ASM / "placement.json", ASM / "quick_release_trials_view.scad"], ASM / "_work/logs/view.log")
    env = os.environ.copy()
    env.update(ASM_JSON=str(ASM / "placement.json"), ASM_ROOT=str(ROOT), STL_OUT=str(ASM / "quick_release_trials.stl"))
    run([FC, ROOT / "scad/lib/asm_to_stl.py"], ASM / "_work/logs/assembly_stl.log", env)
    if not args.no_step:
        export_assembly_step()
    report = {"status": "geometry_checked_physical_trial_pending", "parts": metrics, "hardware": hardware(),
              "collision_free_samples": cases, "clamped_pair_checks":clamped,
              "clamped_pair_volume_tolerance_mm3":0.001,
              "hardware_fit_bearing_margin_mm":0.01,
              "limits": "Discrete geometry samples; 0.01 mm at intended metal/rubber bearing faces excluded from fit checks; no elasticity, strength, fatigue, actual printer-fit certification."}
    (ASM / "_work/analysis/verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    run([sys.executable, ROOT / "tools/assembly_parts.py", "sync", "quick_release_trials"], ASM / "_work/logs/sync.log")
    print(f"PASS {len(cases)} collision samples; print set synced", flush=True)


def check_locking():
    """Confirm flank/floor seating and geometric hooks; no friction/load certification."""
    work = ASM / "_work/analysis/locking"
    work.mkdir(parents=True, exist_ok=True)
    cases = [
        ("slide_left_preload", 'translate([-0.1,0,0.01]) seated_male("slide",clamped=true)', 'receiver("slide")'),
        ("slide_floor_preload", 'translate([0,0,-0.1]) seated_male("slide",clamped=true)', 'receiver("slide")'),
        ("slide_gib_preload", 'translate([-0.1,0,0.01]) slide_gib()', 'seated_male("slide",clamped=true)'),
        ("snap_blocked", 'seated_male("snap",travel=4)', 'receiver("snap")'),
        ("twist_axial_retained", 'seated_male("twist",travel=1)', 'receiver("twist")'),
        ("twist_side_pin_rotation", 'seated_male("twist",angle=-10)', 'through_bolt("twist")'),
        ("twist_side_pin_axial", 'seated_male("twist",travel=0.5)', 'through_bolt("twist")')]
    cases.append(("twist_cam_bearing", 'translate([0,0,0.2]) seated_male("twist")', 'receiver("twist")'))
    cases.append(("twist_pad_precompression", 'twist_pad_reference(compressed=false)', 'receiver("twist")'))
    for kind in ["slide", "twist"]:
        cases.extend([
            (f"{kind}_fixed_nut_bearing", f'translate([0.1,0,0]) fixed_nut("{kind}")', f'receiver("{kind}")'),
            (f"{kind}_knob_head_bearing", f'translate([-0.1,0,0]) through_bolt("{kind}",include_washer=false)', f'placed_knob("{kind}")')])
    # Exact native meshes and authoritative placement avoid re-evaluating the
    # many fillet lofts for each independent contact probe.
    placed = json.loads((ASM / "placement.json").read_text(encoding="utf-8"))["items"]
    def local_mesh(label):
        item = next(x for x in placed if x["label"]==label)
        female = next(x for x in placed if x["label"][0]==label[0] and "female" in x["label"])
        origin = female["ops"][0]["translate"] if female["ops"] else [0,0,0]
        ops = " ".join(f'{k}({json.dumps(v)})' for op in item["ops"] for k,v in op.items())
        path = (ROOT / item["part"] / (item["file"]+".stl")).as_posix()
        return f'translate({json.dumps([-v for v in origin])}) {ops} import("{path}")'
    aliases = {
        'seated_male("slide",clamped=true)': local_mesh("A slide male"),
        'seated_male("snap",travel=4)': 'translate([0,-4,0]) '+local_mesh("B snap male"),
        'seated_male("twist",travel=1)': 'translate([0,0,1]) '+local_mesh("C twist male"),
        'seated_male("twist",angle=-10)': 'rotate([0,0,-10]) '+local_mesh("C twist male"),
        'seated_male("twist",travel=0.5)': 'translate([0,0,0.5]) '+local_mesh("C twist male"),
        'placed_knob("slide")': local_mesh("A knob"),
        'placed_knob("twist")': local_mesh("C knob"),
        'seated_male("twist")': local_mesh("C twist male"),
    }
    for kind in ["slide","snap","twist"]:
        aliases[f'receiver("{kind}")'] = f'import("{(PART / ("quick_release_prototypes_"+kind+"_female.stl")).as_posix()}")'
    report = []
    for name, first, second in cases:
        for old, new in aliases.items():
            first = first.replace(old,new)
            second = second.replace(old,new)
        scad = work / (name+".scad")
        stl = work / (name+".stl")
        scad.write_text(f"use <{SCAD.as_posix()}>\nintersection() {{ {first}; {second}; }}\n", encoding="utf-8")
        run([OSC,"-o",stl,scad],work / (name+".log"))
        volume = abs(float(trimesh.load(stl,force="mesh").volume))
        if volume < 0.01:
            raise RuntimeError(f"Lock does not block motion: {name}")
        report.append({"case":name,"contact_detected":True,"interference_volume_mm3":volume})
    h = hardware()
    # Measure actual roof take-up rather than treating a tiny initial contact
    # as absent because of the coarser positive-volume retention threshold.
    male = trimesh.load(PART / "quick_release_prototypes_twist_male.stl",force="mesh")
    male.apply_transform(trimesh.transformations.rotation_matrix(np.pi,[1,0,0]))
    male.apply_translation([0,0,h["pad_t"]+h["ring_h"]+h["twist_plate_t"]+h["twist_lock_gap"]])
    female = trimesh.load(PART / "quick_release_prototypes_twist_female.stl",force="mesh")
    nominal = h["twist_pad_t"]-h["twist_pad_depth"]-h["twist_lock_gap"]
    takeup = None
    for lift in np.arange(0,nominal+0.0001,0.005):
        probe=male.copy(); probe.apply_translation([0,0,float(lift)])
        contact=trimesh.boolean.intersection([probe,female],engine="manifold")
        if abs(float(contact.volume))>0.000001:
            takeup=float(lift); break
    if takeup is None or takeup >= nominal:
        raise RuntimeError("Cam roof cannot retain positive rubber precompression")
    report.append({"case":"twist_cam_take_up","first_contact_lift_upper_bound_mm":takeup,
                   "remaining_pad_compression_lower_bound_mm":nominal-takeup,
                   "limits":"Geometry only; no bearing stress or rubber-force certification."})
    tip = h["slide_gib_x"]+h["washer_t"]+h["head_seat"]-h["slide_bolt_length"]
    nut_end = h["slide_nut_x"]+h["metal_nut_t"]
    engaged = min(h["metal_nut_t"], nut_end-tip-h["thread_pitch"]*h["unlock_turns"])
    if engaged < 1.5:
        raise RuntimeError("A nut disengages during the specified release stroke")
    report.append({"case":"slide_release_thread_engagement", "engagement_mm":engaged,
                   "turns":h["unlock_turns"], "limits":"Nominal geometry, not thread strength."})
    (ASM / "_work/analysis/locking_verification.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    cam=[]
    for angle in range(-int(h["turn_deg"]),1,5):
        lift=h["twist_cam_lift"]*(-angle/h["turn_deg"])
        separation=h["twist_lock_gap"]+lift
        compression=max(0,h["twist_pad_t"]-h["twist_pad_depth"]-separation)
        cam.append(dict(angle_deg=angle, axial_lift_mm=lift, pad_compression_mm=compression))
    assert all(cam[i]["axial_lift_mm"]>cam[i+1]["axial_lift_mm"] for i in range(len(cam)-1))
    assert 0<cam[-1]["pad_compression_mm"]<h["twist_pad_t"]*0.15
    (ASM / "_work/analysis/cam_verification.json").write_text(json.dumps({
        "pad_thickness_mm":h["twist_pad_t"], "bond_side":"male_plate_underside", "pocket_depth_mm":h["twist_pad_depth"],
        "pad_cut_size_mm":[h["twist_pad_w"],h["twist_pad_l"],h["twist_pad_t"]],
        "pocket_size_mm":[h["twist_pad_w"]+2*h["twist_pad_side_clearance"],h["twist_pad_l"]+2*h["twist_pad_side_clearance"],h["twist_pad_depth"]],
        "pad_count":2,"total_bond_area_mm2":2*h["twist_pad_w"]*h["twist_pad_l"],"turn_samples":cam,
        "limits":"Nominal kinematics and overlap only; rubber hardness, torque and actual preload unverified."},indent=2)+"\n",encoding="utf-8")


def check_pad_bond_surfaces():
    """Both pockets have open mouths, solid floors and full female bearing lands."""
    h=hardware()
    male=trimesh.load(PART / "quick_release_prototypes_twist_male.stl",force="mesh")
    female=trimesh.load(PART / "quick_release_prototypes_twist_female.stl",force="mesh")
    report=[]
    for side in [-1,1]:
        pocket_floor=h["twist_plate_t"]-h["twist_pad_depth"]
        cavity=trimesh.creation.box(extents=[h["twist_pad_w"],h["twist_pad_l"],h["twist_pad_depth"]])
        cavity.apply_translation([side*h["twist_pad_r"],0,pocket_floor+h["twist_pad_depth"]/2])
        remaining=trimesh.boolean.intersection([male,cavity],engine="manifold")
        if abs(float(remaining.volume))>0.001:
            raise RuntimeError(f"Rubber pocket blocked: {side}")
        report.append(dict(side=side,land="male_pocket_open",depth_mm=h["twist_pad_depth"],
                           size_mm=[h["twist_pad_w"]+2*h["twist_pad_side_clearance"],h["twist_pad_l"]+2*h["twist_pad_side_clearance"]]))
        for kind,mesh,z in [("male_pocket_floor",male,pocket_floor-0.5),
                            ("female_bearing",female,h["pad_t"]+h["ring_h"]-0.5)]:
            probe=trimesh.creation.box(extents=[h["twist_pad_w"],h["twist_pad_l"],1.0])
            probe.apply_translation([side*h["twist_pad_r"],0,z])
            common=trimesh.boolean.intersection([mesh,probe],engine="manifold")
            expected=float(probe.volume)
            if abs(float(common.volume)-expected)>0.001:
                raise RuntimeError(f"Rubber {kind} land is not continuous: {side}")
            report.append(dict(side=side,land=kind,solid_depth_checked_mm=1.0,area_mm2=h["twist_pad_w"]*h["twist_pad_l"]))
    (ASM / "_work/analysis/pad_bond_verification.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")


def export_assembly_step():
    env = os.environ.copy()
    step = ASM / "quick_release_trials.step"
    env.update(ASM_JSON=str(ASM / "placement.json"),ASM_ROOT=str(ROOT),STEP_OUT=str(step),STEP_IN=str(step))
    run([FC,ROOT / "scad/lib/asm_to_step.py"],ASM / "_work/logs/assembly_step.log",env)
    run([FC,ROOT / "scad/lib/verify_asm_step.py"],ASM / "_work/logs/assembly_step_verify.log",env)


def check_clamped_assembly():
    """Check every pair in each locked group using closed source meshes and placement."""
    items = json.loads((ASM / "placement.json").read_text(encoding="utf-8"))["items"]
    meshes = []
    for item in items:
        mesh = trimesh.load(ROOT / item["part"] / (item["file"]+".stl"), force="mesh")
        matrix = np.eye(4)
        for op in item.get("ops", []):
            for kind, value in op.items():
                if kind == "translate": transform = trimesh.transformations.translation_matrix(value)
                elif kind == "rotate": transform = trimesh.transformations.euler_matrix(*np.radians(value))
                else: raise ValueError(f"Unsupported trial transform: {kind}")
                matrix = matrix @ transform
        mesh.apply_transform(matrix)
        meshes.append((item["label"],mesh))
    c = dict(meshes)
    clearances = []
    for prefix,name in [("A","slide"),("C","twist")]:
        upper = float(c[f"{prefix} {name} male"].bounds[1,2])
        lower = float(c[f"{prefix} {name} female"].bounds[0,2])
        top = float(c[f"{prefix} knob"].bounds[1,2])
        bottom = float(c[f"{prefix} knob"].bounds[0,2])
        if min(upper-top,bottom-lower) < 0.25:
            raise RuntimeError(f"{prefix} knob obstructs a mounting plane")
        clearances.append(dict(part=prefix, upper_plane_mm=upper, lower_plane_mm=lower,
                               knob_top_mm=top, knob_bottom_mm=bottom,
                               upper_clearance_mm=upper-top, lower_clearance_mm=bottom-lower))
    (ASM / "_work/analysis/top_mount_clearance.json").write_text(
        json.dumps(clearances,indent=2)+"\n",encoding="utf-8")
    report = []
    for i,(first,a) in enumerate(meshes):
        for second,b in meshes[i+1:]:
            if first[0] != second[0]: continue
            common = trimesh.boolean.intersection([a,b],engine="manifold")
            with np.errstate(divide="ignore",invalid="ignore"):
                volume = abs(float(common.volume)) if len(common.faces) else 0.0
            if volume > 0.001: raise RuntimeError(f"Clamped assembly interference: {first}, {second}, {volume} mm3")
            report.append({"first":first,"second":second,"overlap_mm3":volume})
    return report


def check_mounting_holes():
    """Pass actual M3 shaft envelopes through all retained mounting holes."""
    h = hardware()
    pitch = h["mount_pitch"]/2
    report = []
    for kind in ["slide_male","slide_female","snap_male","snap_female","twist_male","twist_female"]:
        ys = [pitch] if kind=="slide_male" else [-pitch,pitch]
        thickness = h["slide_plate_t"] if kind=="slide_male" else h["twist_plate_t"] if kind=="twist_male" else h["pad_t"]
        if kind=="snap_male": ys=[h["snap_entry"]-h["snap_tab_l"]/2]; thickness=h["snap_t"]
        if kind=="snap_female": ys=[h["snap_entry"]+4,h["snap_end"]-4]; thickness=h["snap_floor"]
        mesh = trimesh.load(PART / ("quick_release_prototypes_"+kind+".stl"),force="mesh")
        for x in [-pitch,pitch]:
            for y in ys:
                shaft = trimesh.creation.cylinder(radius=h["bolt_nominal"]/2,height=thickness+2,sections=48)
                shaft.apply_translation([x,y,thickness/2])
                common = trimesh.boolean.intersection([mesh,shaft],engine="manifold")
                with np.errstate(divide="ignore",invalid="ignore"):
                    volume = abs(float(common.volume)) if len(common.faces) else 0.0
                if volume > 0.001: raise RuntimeError(f"M3 mounting hole blocked: {kind} at {x},{y}")
                report.append({"part":kind,"center_xy_mm":[x,y],"nominal_shaft_mm":h["bolt_nominal"],"overlap_mm3":volume})
    (ASM / "_work/analysis/mounting_verification.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    return report


if __name__ == "__main__":
    main()
