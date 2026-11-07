"""Rev.4 actual meshes: bolt lengths, clear passages, tool paths and contact seats."""
from pathlib import Path
import itertools, json
import numpy as np
import trimesh
from verify_parent_exterior_qr import intersection, probe

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assemblies/parent_exterior/_work/analysis/bolt_on_plate'


def check_fixtures(rows,meshes,integrated=False):
    bores=[];tools=[];contacts=[];hardware_collisions=[];lengths=[]
    side_x=() if integrated else (-110,110)
    end_s=() if integrated else (-1,1)
    from topopt.geom import shell_report
    native=[]
    for name,row in rows.items():
        if 'printed' not in row['part'] and 'jigs' not in row['part']:continue
        report=shell_report(meshes[name].triangles,intersections=False)
        native.append(dict(label=name,**report,passed=bool(report['closed_shell'] and not report['degenerate'])))
    def bore(host,a,b,d):
        v=intersection(meshes[host],probe(a,b,d))
        bores.append(dict(host=host,axis_mm=[a,b],diameter_mm=d,obstruction_mm3=v,passed=v<0.02))
    def tool(name,a,b,d,omit=()):
        hits=[];p=probe(a,b,d)
        for n,m in meshes.items():
            if rows[n]['group'] in ['hardware','pads'] or n in omit:continue
            v=intersection(p,m)
            if v>0.04:hits.append(dict(part=n,mm3=v))
        tools.append(dict(name=name,axis_mm=[a,b],diameter_mm=d,collisions=hits,passed=not hits))
    def contact(host,xyz):
        distance=float(trimesh.proximity.closest_point(meshes[host],[xyz])[1][0])
        contacts.append(dict(host=host,point_mm=xyz,distance_mm=distance,passed=distance<0.02))
    # Full-sized shanks, excluding chamfer allowances, must traverse both parts.
    for x in (65,85):
        for host in ('open_frame','sensor_carrier'):bore(host,[x,-55,-28.1],[x,-55,0],5.4)
        contact('open_frame',[x,-48,-20]);contact('sensor_carrier',[x,-48,-20])
        tool(f'TD_lower_socket_{x}',[x,-55,-90],[x,-55,-33],11)
        tool(f'TD_upper_driver_{x}',[x,-55,-0.79],[x,-55,60],4,('box_bcas212310g',))
    for x in side_x:
        for y in (-8,8):
            for host in ('open_frame','bolt_on_side_left' if x<0 else 'bolt_on_side_right'):
                bore(host,[x,y,-20],[x,y,1.3],4.4)
            tool(f'side_driver_{x}_{y}',[x,y,1.31],[x,y,35],3.5)
            for host,point in [('open_frame',[x+3,y,-12.3]),(f'bolt_on_side_nut_{x}_{y}',[x+3,y,-12.3]),
                               ('bolt_on_side_left' if x<0 else 'bolt_on_side_right',[x+3,y,1.3]),(f'bolt_on_side_bolt_{x}_{y}',[x+3,y,1.3])]:contact(host,point)
    for s in end_s:
        for y in (52,62):
            for host in ('open_frame','bolt_on_end_push' if s<0 else 'bolt_on_end_fixed'):
                bore(host,[s*94,s*y,-22.3],[s*94,s*y,-0.8],4.4)
            tool(f'end_driver_{s}_{y}',[s*94,s*y,-90],[s*94,s*y,-22.31],3.5)
            for host,point in [('open_frame',[s*94+3,s*y,-7.3]),(f'bolt_on_end_nut_{s}_{y}',[s*94+3,s*y,-7.3]),
                               ('bolt_on_end_push' if s<0 else 'bolt_on_end_fixed',[s*94+3,s*y,-22.3]),(f'bolt_on_end_bolt_{s}_{y}',[s*94+3,s*y,-22.3])]:contact(host,point)
    for x in (-60,-20):
        for y in (-20,20):
            contact('open_frame',[x+5,y,-20]);contact('camera_qr_female',[x+5,y,-20])
            for host,point in [('open_frame',[x+2.3,y,-6.5]),(f'qr_female_nut_{x}_{y}',[x+2.3,y,-6.5]),
                               ('camera_qr_female',[x+2.3,y,-27.4]),(f'qr_female_bolt_{x}_{y}',[x+2.3,y,-27.4])]:contact(host,point)
    contact('sensor_carrier',[43,1,-35]);contact('sensor_carrier',[55,1,-27])
    # The straight M4 driver is blocked by the perpendicular bridge hardware
    # while installed. Service the removable stop off the camera mount.
    for x in (() if 'locating_camera_stop' not in meshes else (-20,20)):
        p=probe([-40+x,-40,-109.95],[-40+x,-15.51,-109.95],3.2)
        v=intersection(p,meshes['locating_camera_stop'])
        tools.append(dict(name=f'detached_camera_adjuster_{x}',diameter_mm=3.2,
                          state='Stop removed from camera; bridge attachment screws removed',
                          collisions=[] if v<0.04 else [dict(part='locating_camera_stop',mm3=v)],passed=v<0.04))
    locator_seats=[] if integrated else [('bolt_on_side_right',[108,-20,-0.8]),('bolt_on_side_left',[-110,-20,-0.8]),
                     ('bolt_on_end_fixed',[94,57,-20]),('bolt_on_end_push',[-94,-57,-20])]
    for host,xyz in locator_seats:
        contact(host,xyz);contact('open_frame',xyz)
    # Check all metal pairs too; the general assembly checker filters hardware-only pairs.
    hardware=[n for n in meshes if rows[n]['group']=='hardware']
    for a,b in itertools.combinations(hardware,2):
        v=intersection(meshes[a],meshes[b])
        if v>0.04:hardware_collisions.append(dict(a=a,b=b,mm3=v))
    # Use the transformed mesh bounds for engagement and vessel/ground clearance.
    def length(bolt,nut,pitch,direction):
        bounds=meshes[bolt].bounds;nb=meshes[nut].bounds
        tip=float(bounds[1 if direction>0 else 0,2])
        protrusion=float(tip-nb[1,2] if direction>0 else nb[0,2]-tip)
        engagement=float(nb[1,2]-nb[0,2])
        lengths.append(dict(bolt=bolt,nut=nut,tip_z_mm=tip,nut_thickness_mm=engagement,
                            protrusion_mm=protrusion,pitch_mm=pitch,minimum_protrusion_mm=2*pitch,
                            vessel_bottom_gap_mm=-tip if direction>0 else None,
                            ground_gap_mm=tip+72 if direction<0 else None,
                            passed=protrusion>=2*pitch-0.02 and (tip<-0.8 if direction>0 else tip>-72)))
    for x in (-60,-20):
        for y in (-20,20):length(f'qr_female_bolt_{x}_{y}',f'qr_female_nut_{x}_{y}',0.5,1)
    for x in (65,85):length(f'carrier_screw_{x}',f'carrier_nut_{x}',0.8,-1)
    for x in side_x:
        for y in (-8,8):length(f'bolt_on_side_bolt_{x}_{y}',f'bolt_on_side_nut_{x}_{y}',0.7,-1)
    for s in end_s:
        for y in (52,62):length(f'bolt_on_end_bolt_{s}_{y}',f'bolt_on_end_nut_{s}_{y}',0.7,1)
    return dict(passed=all(x['passed'] for x in bores+tools+contacts+lengths+native) and not hardware_collisions,
                bores=bores,tools=tools,contacts=contacts,fastener_lengths=lengths,hardware_collisions=hardware_collisions,
                native_shells=native,
                assembly_order=('Integral locators need no bolts; fit optional spare nuts and camera nuts with vessel removed, then attach TD/C female and install vessel/skids.' if integrated else 'Fit all recessed nuts and tighten side locators before skids; attach TD and camera female with vessel/camera removed; then install skids, vessel and moving camera unit.'),
                cable_access='Existing camera release sweep and +Y bolt withdrawal retained; actual cables are not represented.')


if __name__=='__main__':
    import verify_parent_exterior_qr as base
    raise SystemExit(base.main(OUT,bolt_on=True))
