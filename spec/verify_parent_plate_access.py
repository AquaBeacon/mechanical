"""Continuous clearance and clamps for underside-open nuts and50mm frames."""
from pathlib import Path
import json,sys,math
import FreeCAD as A
import Part


def build(doc,parameters):
    root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'scad/lib'))
    import parent_gnss as G
    import parent_service_datums as D
    from parent_floor_access import overlap,hex_prism
    from parent_penetrator_access import dry_projection_sweep,wrench_height_envelope
    rows=json.loads((root/parameters['layout']).read_text(encoding='utf-8'))['items']
    oldrows={r['label']:r for r in json.loads((root/parameters['baseline_layout']).read_text(encoding='utf-8'))['items']}
    candidates={name:Part.read(str(root/file)) for name,file in parameters['candidates'].items()}
    aliases={'plate':'floor_plate','lipo_tray':'battery_base','coax_ring':'ann_mb1_coax_ring_service'}
    checks=[];scene={};oldscene={};access_preconditions=[]
    def check(name,passed,**detail):
        rec=dict(name=name,passed=bool(passed),**detail);checks.append(rec)
        print('ACCESS_CHECK='+json.dumps(rec),flush=True)
    def transform(shape,ops):
        s=shape.copy()
        for op in reversed(ops):
            if 'translate' in op:s.translate(A.Vector(*op['translate']))
            elif 'rotate' in op:
                for axis,angle in zip([(1,0,0),(0,1,0),(0,0,1)],op['rotate']):s.rotate(A.Vector(),A.Vector(*axis),angle)
            else:raise ValueError(op)
        return s
    for row in rows:
        label=row['label'];part=row['part']
        if part.endswith('/screw') or label.startswith('pen_'):continue
        stem=row.get('file',Path(part).name);key=aliases.get(label,stem)
        local=candidates.get(key)
        if local is None:local=Part.read(str(root/part/(stem+'.step')))
        scene[label]=transform(local,row.get('ops',[]))
        previous=oldrows.get(label)
        if previous:
            history=parameters.get('old_shapes',{}).get(label)
            path=root/history if history else root/previous['part']/(previous.get('file',Path(previous['part']).name)+'.step')
            if path.exists():oldscene[label]=(path,previous.get('ops',[]))
    def baseline(label):
        value=oldscene[label]
        if isinstance(value,tuple):
            value=transform(Part.read(str(value[0])),value[1]);oldscene[label]=value
        return value
    floor=scene['plate'];case=scene['box_bcas212310g']
    check('floor valid single solid',floor.isValid() and len(floor.Solids)==1)
    for name,points in [('sony_support_frame',G.SONY_CARRIER_FOOT_XY),('gnss_support_frame',G.UNIVERSAL_FRAME_FOOT_XY)]:
        shape=scene[name]
        check(name+' joins four feet in one printable solid',shape.isValid() and len(shape.Solids)==1,solids=len(shape.Solids))
        for i,(x,y) in enumerate(points):
            column=shape.common(Part.makeBox(4,4,D.SENSOR_LEG_LENGTH,A.Vector(x-2,y-2,D.SENSOR_BASE_Z)))
            length=column.BoundBox.ZLength
            check(name+' leg'+str(i)+'50mm shoulder length',abs(length-50)<1e-5,length_mm=length,datums_mm=[D.SENSOR_BASE_Z,D.SENSOR_JOINT_Z],key_height_excluded_mm=.8)
        check(name+' base ribs below low electronics',shape.BoundBox.ZMin>=18.8-1e-6,build_direction='+Z',base_rib_height_mm=4)
    def contact(upper,lower,name,region=None):
        probe=scene[upper].copy();probe.translate(A.Vector(0,0,-.05))
        if region:probe=probe.common(region)
        volume=overlap(probe,scene[lower]);check(name,volume>.05,volume_mm3=volume,compression_direction='-Z',probe_mm=.05)
    for frame,plate,points in [('sony_support_frame','sony_mount_plate',G.SONY_CARRIER_FOOT_XY),('gnss_support_frame','gnss_universal_carrier',G.UNIVERSAL_FRAME_FOOT_XY)]:
        for i,(x,y) in enumerate(points):
            region=Part.makeBox(12,12,60,A.Vector(x-6,y-6,18.7))
            contact(plate,frame,frame+' top plate bears on leg'+str(i),region)
            contact(frame,'plate',frame+' leg'+str(i)+' bears on floor',region)
    for i in range(4):
        foot='cradle_floor_foot_'+str(i)
        contact('main_service_frame',foot,'MAIN to foot'+str(i))
        contact(foot,'coax_ring','MAIN foot'+str(i)+' to coax ring')
    contact('coax_ring','plate','coax ring to floor')
    # Changed and raised geometry versus every actual component, including lid.
    changed=['plate','main_service_frame','antenna_service_shelf','lipo_tray','gnss_universal_carrier','sony_mount_plate','sony_support_frame','gnss_support_frame']
    checked_pairs=set()
    for label in changed:
        s=scene[label]
        for other,t in scene.items():
            if other==label or not s.BoundBox.intersect(t.BoundBox):continue
            pair=tuple(sorted((label,other)))
            if pair in checked_pairs:continue
            checked_pairs.add(pair)
            print('COLLISION_PAIR='+label+'|'+other,flush=True)
            volume=overlap(s,t)
            previous=overlap(baseline(label),baseline(other)) if volume>.02 and label in oldscene and other in oldscene else 0
            check(label+' vs '+other,volume<=previous+.02,overlap_mm3=volume,inherited_overlap_mm3=previous)
    for x in [150,175]:
        envelope=dry_projection_sweep(x)
        for label,s in scene.items():
            if label in ['box_bcas212310g','lid_keepout'] or not envelope.BoundBox.intersect(s.BoundBox):continue
            volume=overlap(s,envelope)
            check('continuous extraction '+label+' vs M10_'+str(x),volume<.001,volume_mm3=volume,lift_mm=120,height_range_mm=[30,35])
        tool=wrench_height_envelope(x,advance=10)
        volume=overlap(tool,case)
        check('M10_'+str(x)+' wrench insertion and360deg',volume<.001,volume_mm3=volume,working_state='whole interior removed, both penetrators retained')
    # Old hex pocket volumes must now contain material, rather than a roofed void.
    from parent_floor_access import socket_axes
    for label,x,y in socket_axes(G):
        filled=overlap(hex_prism(x,y,13.2,5.5,2.4),floor)
        check(label+' old buried nut cavity removed',filled>15,restored_material_mm3=filled)
    filled=overlap(hex_prism(*G.SONY_CARRIER_FOOT_XY[2],55.5,5.5,2.4),scene['sony_support_frame'])
    check('shared Sony buried nut removed',filled>20,restored_material_mm3=filled)
    # Entire clamp paths: head/washer -> floor -> foot/frame -> plastic thread.
    interfaces=parameters['pcb_holes']
    mh=[[18+x,112-y] for x,y in interfaces['PARENT_MAIN']];ph=[[25.8+y,115+x] for x,y in interfaces['PARENT_PWR']]
    for row in D.retrofit_fasteners(G,mh,ph):
        label=row['label'];x,y=row['xy'];head=row['head_z'];length=row['length']
        if label.startswith(('cradle_service_','gnss_floor_','sony_floor_')):
            host='main_service_frame' if label.startswith('cradle') else 'gnss_support_frame' if label.startswith('gnss') else 'sony_support_frame'
            plate=host if host=='main_service_frame' else 'gnss_universal_carrier' if host.startswith('gnss') else 'sony_mount_plate'
            nz=row['nut_z'];nt=nz+D.FLOOR_NUT_HEIGHT;tip=head-length
            nut=hex_prism(x,y,nz,5.5,D.FLOOR_NUT_HEIGHT).cut(Part.makeCylinder(1.5,3,A.Vector(x,y,nz-.1)))
            check(label+' underside nut fits',overlap(nut,floor)<.001,overlap_mm3=overlap(nut,floor))
            insertion=hex_prism(x,y,G.FLOOR_GRID_BOTTOM_Z-4,5.5,nt-(G.FLOOR_GRID_BOTTOM_Z-4))
            check(label+' continuous bottom insertion',overlap(insertion,floor)<.001,volume_mm3=overlap(insertion,floor),assembly_state='outside case',direction='+Z')
            pressed=nut.copy();pressed.translate(A.Vector(0,0,.05));area=overlap(pressed,floor)/.05
            check(label+' nut axial shoulder reacts through floor',area>12,bearing_area_mm2=area,roof_thickness_mm=G.FLOOR_GRID_TOP_Z-nt,direction='+Z')
            pull=hex_prism(x,y,nz,5.5,D.FLOOR_NUT_HEIGHT+.5)
            check(label+' upward extraction blocked by shoulder',overlap(pull,floor)>5,barrier_volume_mm3=overlap(pull,floor),travel_mm=.5)
            for angle in [-10,10]:
                turned=nut.copy();turned.rotate(A.Vector(x,y,0),A.Vector(0,0,1),angle)
                check(label+' antirotation '+str(angle),overlap(turned,floor)>.1,barrier_volume_mm3=overlap(turned,floor),rotation_deg=angle)
            check(label+' nut and tip clear case',overlap(nut,case)<.001 and overlap(Part.makeCylinder(1.5,head-tip,A.Vector(x,y,tip)),case)<.001,nut_case_mm3=overlap(nut,case),tip_z_mm=tip)
            check(label+' nut fully threaded',tip<nz-.25,engaged_mm=D.FLOOR_NUT_HEIGHT,protrusion_mm=nz-tip)
            shank=Part.makeCylinder(1.5,head-tip,A.Vector(x,y,tip))
            for name in [host,'plate',plate]+(['coax_ring','cradle_floor_foot_'+label.rsplit('_',1)[1]] if host=='main_service_frame' else []):
                check(label+' shank clearance '+name,overlap(shank,scene[name])<.001,overlap_mm3=overlap(shank,scene[name]))
            seat=Part.makeCylinder(2.75,.05,A.Vector(x,y,head-.05))
            area=overlap(seat,scene[plate])/.05
            check(label+' top head reaction',area>10,bearing_area_mm2=area,head_seat_z_mm=head)
            headshape=Part.makeCylinder(2.75,3,A.Vector(x,y,head))
            tool=Part.makeCylinder(1.5,50,A.Vector(x,y,head+1))
            for name,body in scene.items():
                if name in ['box_bcas212310g','lid_keepout']:continue
                if headshape.BoundBox.intersect(body.BoundBox):
                    check(label+' head clears '+name,overlap(headshape,body)<.001,overlap_mm3=overlap(headshape,body))
                if tool.BoundBox.intersect(body.BoundBox):
                    volume=overlap(tool,body)
                    if label=='sony_floor_3' and name=='spresense':
                        access_preconditions.append(dict(fastener=label,remove_before_tool_use=name,
                            installed_obstruction_mm3=volume,reason='Install support bolts before SPRESENSE; remove board before disassembly'))
                        print('ACCESS_PREREQUISITE='+json.dumps(access_preconditions[-1]),flush=True)
                    else:
                        check(label+' driver approach '+name,volume<.001,overlap_mm3=volume)

        elif label.startswith(('gnss_plate_','sony_plate_')):
            host='gnss_support_frame' if label.startswith('gnss') else 'sony_support_frame';tip=head-length
            thread=Part.makeCylinder(1.5,D.SENSOR_JOINT_Z-tip,A.Vector(x,y,tip))
            volume=overlap(thread,scene[host])
            check(label+' top plate clamped to solid leg',tip>D.SENSOR_JOINT_Z-10+.5 and volume>1,nominal_thread_engagement_mm=D.SENSOR_JOINT_Z-tip,bottoming_clearance_mm=tip-(D.SENSOR_JOINT_Z-10),thread_material_mm3=volume)
        elif row['nut_z'] is not None:
            d=row['diameter'];nz=row['nut_z'];height=3.2 if d==4 else 2.4;thickness=.8 if d==4 else .5
            nut=hex_prism(x,y,nz,7 if d==4 else 5.5,height)
            volume=overlap(nut,scene['antenna_service_shelf'])
            check(label+' exposed nut outside printed shelf',volume<.001,overlap_mm3=volume,tip_protrusion_mm=nz-(head-length))
            washer=Part.makeCylinder(4.5 if d==4 else 3.5,thickness,A.Vector(x,y,nz+height))
            washer=washer.cut(Part.makeCylinder(2.15 if d==4 else 1.6,thickness+.2,A.Vector(x,y,nz+height-.1)))
            washer.translate(A.Vector(0,0,.05))
            check(label+' external washer and shelf reaction',overlap(washer,scene['antenna_service_shelf'])>.2,contact_mm3=overlap(washer,scene['antenna_service_shelf']))
            check(label+' full nut thread coverage',head-length<nz-.25,tip_z_mm=head-length,nut_z_mm=[nz,nz+height])
    # Preserve the concurrently revised battery; use its current placement,
    # not the retired slide-lid screw axis. Battery geometry is not republished.
    boltrow=next(r for r in rows if r['label']=='lipo_ret_bolt_0')
    point=transform(Part.Vertex(A.Vector()),boltrow.get('ops',[])).Vertexes[0].Point
    thread=Part.makeCylinder(1.5,9,A.Vector(point.x,point.y,point.z-12))
    check('current battery lid pilot engagement',overlap(thread,scene['lipo_tray'])>1,
          engagement_mm=9,axis_mm=[point.x,point.y],source='current placement.json')
    for i,(x,y) in enumerate(G.magnetometer_mounting_xy()):
        nut=scene['mag_nut_'+str(i)];washer=scene['mag_washer_'+str(i)]
        volume=overlap(nut,scene['gnss_universal_carrier'])
        check('mag M2 nut'+str(i)+' fully external',volume<.001,overlap_mm3=volume)
        pressed=washer.copy();pressed.translate(A.Vector(0,0,.05))
        check('mag M2 washer'+str(i)+' flat carrier reaction',overlap(pressed,scene['gnss_universal_carrier'])>.1,contact_mm3=overlap(pressed,scene['gnss_universal_carrier']))
    for label in ['spresense','gnss_receiver','gnss_sma_plug']:
        overlap_lid=overlap(scene[label],scene['lid_keepout'])
        check(label+' below actual lid solid',overlap_lid<.001,overlap_mm3=overlap_lid,highest_z_mm=scene[label].BoundBox.ZMax)
    for i,(x,y) in enumerate(G.CASE_ANCHOR_XY[:3]):
        head=Part.makeCylinder(5,5,A.Vector(x,y,16.8))
        for label in ['plate','lipo_tray','coax_ring','main_service_frame','sony_support_frame','gnss_support_frame']:
            volume=overlap(head,scene[label]);check('M4 head'+str(i)+' vs '+label,volume<.001,volume_mm3=volume)
        seat=Part.makeCylinder(5,.05,A.Vector(x,y,16.75))
        check('M4 seat'+str(i)+' retained',overlap(seat,floor)/.05>40,bearing_area_mm2=overlap(seat,floor)/.05)
    result=dict(passed=all(c['passed'] for c in checks),checks=checks,access_preconditions=access_preconditions,leg_length_mm=50,printed_embedded_nut_pockets=0,
                limitations=['Printed thread pullout, torque/creep, physical print and fit, cable loops and actual drive tools remain unverified.'])
    print('PLATE_ASSEMBLY_REPORT='+json.dumps(result),flush=True)
    assert result['passed'],[c for c in checks if not c['passed']]
    obj=doc.addObject('Part::Feature','VerifiedFloor');obj.Shape=floor
    obj.addProperty('App::PropertyString','Checks');obj.Checks=json.dumps(result)
    return [obj]
