"""Derive topology inputs from the existing clamp CAD, without solving or adoption.

The topopt package owns all optimisation and FEA. This adapter only authors CAD
input volumes and records the user's confirmed manufacturing/interface choices.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import ast,hashlib,json,re,subprocess,sys
import trimesh

PART=Path(__file__).resolve().parents[1]
ROOT=PART.parents[4]
CASE=PART/'_work/analysis/topology_print'
if '--binary-cad' in sys.argv: CASE=CASE/'precision_cad'
WORK=PART/'_work/intermediate/topology_print'
LOGS=PART/'_work/logs'
OSC=Path('C:/Program Files/OpenSCAD/openscad.exe')

def save(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    for folder in [CASE,WORK,LOGS]: folder.mkdir(parents=True,exist_ok=True)
    source=PART/'child_wte4_petg_clamp.scad'
    interfaces=ROOT/'scad/lib/child_horizontal_plate_interfaces.scad'
    finish=ROOT/'scad/lib/edge_finished_profiles.scad'
    scad=WORK/'inputs.scad'
    scad.write_text(f'''// Generated analysis inputs only; never a printable part.
include <{interfaces.as_posix()}>
use <{finish.as_posix()}>
use <{source.as_posix()}>
edge_chamfer=hf_edge_chamfer;
edge_fillet_r=hf_edge_fillet;
link_root_chamfer=hf_clamp_link_root;
$fn=96;
half="upper";
kind="design_space";
pitch=max(hf_stations)-min(hf_stations);
length=pitch+hf_clamp_width;
contact_preserve_t=4; // Analysis input skin; exact mating geometry is retained.
mount_pad_halfwidth=7;
ear_preserve_halfwidth=14;
echo(["LINER_AUDIT",hf_liner_t_provisional,hf_liner_compression_provisional,
      2*hf_clamp_r,wte4_acrylic_od,hf_clamp_width,pitch,length,hf_clamp_mount_plane]);
module original_bands() {{
    for(z=[0,pitch]) translate([0,0,z]) clamp_half(half=="lower");
}}
module envelope() {{
    difference() {{
        ef_profile(length,edge_chamfer) clamp_outline();
        ef_cut(length,edge_chamfer) circle(r=hf_clamp_r);
    }}
}}
module hole_cuts() {{
    // Exact existing voids at both bands, plus open axial nut insertion routes.
    for(z0=[0,pitch]) translate([0,0,z0]) {{
        difference() {{
            ef_profile(hf_clamp_width,edge_chamfer) clamp_outline();
            clamp_half(half=="lower");
        }}
        for(x=hf_mount_x,dy=hf_mount_axial) {{
            z=hf_clamp_width/2+dy;
            mount_nut_channel(x,z,z<hf_clamp_width/2 ? -20 : hf_clamp_width+20);
        }}
    }}
}}
module preserved_interfaces() {{
    intersection() {{
        original_bands();
        union() {{
            // Entire rubber mating skin, including its original entry chamfers.
            linear_extrude(length) circle(r=hf_clamp_r+contact_preserve_t);
            // Full mounting pads retain faces, bores and axial nut channels.
            for(x=hf_mount_x) translate([x-mount_pad_halfwidth,0,0])
                cube([2*mount_pad_halfwidth,hf_clamp_mount_plane+1,length]);
            // Full ears retain screw seating and the lower ordinary-nut seats.
            for(s=[-1,1]) translate([s*hf_ear_x-ear_preserve_halfwidth,0,0])
                cube([2*ear_preserve_halfwidth,hf_ear_height+2,length]);
        }}
    }}
}}
if(kind=="design_space") difference() {{ envelope(); hole_cuts(); }}
else if(kind=="preserve") preserved_interfaces();
else if(kind=="cuts") hole_cuts();
else assert(false,"Unknown analysis input");
''',encoding='utf-8')
    tasks=[(half,kind) for half in ['upper','lower'] for kind in ['design_space','preserve','cuts']]
    def render(task):
        half,kind=task;path=CASE/f'{half}_{kind}.stl'
        result=subprocess.run([str(OSC),'--export-format','binstl' if '--binary-cad' in sys.argv else 'asciistl','-D',f'half="{half}"',
            '-D',f'kind="{kind}"','-o',str(path),str(scad)],capture_output=True,text=True,
            encoding='utf-8',errors='replace')
        log=result.stdout+result.stderr
        (LOGS/f'topology_print_{half}_{kind}.log').write_text(log,encoding='utf-8')
        if result.returncode or re.search(r'\b(?:ERROR|WARNING):',log):
            raise RuntimeError(f'Analysis input render failed: {half}/{kind}')
        line=next(x for x in log.splitlines() if x.startswith('ECHO: ["LINER_AUDIT"'))
        dimensions=ast.literal_eval(line[6:])[1:]
        mesh=trimesh.load(path,force='mesh')
        if not mesh.is_volume: raise RuntimeError(f'Input is not a valid volume: {path}')
        return dict(half=half,kind=kind,file=path.relative_to(ROOT).as_posix(),
            volume_mm3=float(mesh.volume),dimensions_mm=mesh.extents.tolist(),
            watertight=bool(mesh.is_watertight),connected_components=len(mesh.split()),
            sha256=hashlib.sha256(path.read_bytes()).hexdigest()),dimensions
    with ThreadPoolExecutor(max_workers=2) as pool:
        results=list(pool.map(render,tasks))
    rows=[r for r,_ in results];d=results[0][1]
    assert all(values==d for _,values in results)
    thickness,compression,diameter,vessel_d,width,pitch,length,mount=d
    assert thickness==1 and abs(diameter-(vessel_d+2*(thickness-compression)))<1e-6
    request_path=PART/'spec/print_topology_request.json'
    previous=json.loads(request_path.read_text(encoding='utf-8')) if request_path.exists() else {}
    request=dict(
        status='awaiting_load_inputs',scope='upper_and_lower_linked_clamps_only',
        confirmed=dict(rubber_thickness_mm=thickness,printer='X1C',material='Bambu PETG Basic',
                       print_priority='avoid long horizontal bridges and inaccessible supports'),
        provisional=dict(rubber_compression_mm_per_side=compression,required_safety_factor=3.0),
        interfaces=dict(vessel_diameter_mm=vessel_d,clamp_inner_diameter_mm=diameter,
            band_width_mm=width,station_pitch_mm=pitch,total_axial_length_mm=length,mount_plane_mm=mount),
        analysis_plan=dict(build_axis='Z',raster_axis='X',voxel_mm=2.0,filter_mm=6.0,
            overhang=True,finish='smooth the actual density field and restore local exact interfaces',
            acceptance=['one connected half','functional dimensions and access unchanged',
                'minimum thickness and drainability checked','finished shape re-analysis and convergence',
                'support quality and removal paths checked in real X1C slicing']),
        missing=['supported vessel plus contents mass','handling acceleration or maximum loads',
                 'bolt preload or a documented provisional preload sensitivity range'],
        note='Geometry preparation only. No optimisation, strength result or print adoption yet.')
    # Regenerating CAD must not erase the user's confirmed loads or study status.
    for key in ['confirmed','provisional']:
        request[key].update(previous.get(key,{}))
    for key in ['status','missing','note']:
        if key in previous: request[key]=previous[key]
    save(request_path,request)
    save(CASE/'input_manifest.json',dict(status='exploration_only',inputs=rows,
        sources_sha256={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
            for p in [Path(__file__),source,interfaces,finish]},
        note='Broad continuous half-shell envelope; current shoulder rails do not constrain the search.'))
    print(json.dumps(dict(result='TOPOLOGY_INPUTS_READY',rubber_mm=thickness,inner_diameter_mm=diameter,
                         input_volumes=len(rows)),ensure_ascii=False))

if __name__=='__main__': main()
