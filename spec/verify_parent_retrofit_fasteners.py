"""Exact nut insertion sweeps and axial reaction probes for retrofit candidates.

This checks geometry, not strength, friction or a manufactured thread.
"""
from pathlib import Path
import json,sys,math
import FreeCAD as A,Part

def build(doc,parameters):
    root=Path(__file__).resolve().parents[1]
    sys.path.insert(0,str(root/'scad/lib'))
    import parent_gnss as G
    from parent_service_retrofit import fixed_sensor_columns,main_antenna_cradle,power_adapter,hex_tool,cyl,retrofit_fasteners,MAIN_LIFT,ANT_LIFT,PWR_LIFT,PWR_SOUTH,spacer_threads,ring_service
    data=json.loads((root/'assemblies/parent_hand_service/_work/analysis/retrofit_20261024/interfaces.json').read_text(encoding='utf-8'))
    mh=[[18+x,112-y] for x,y in data['PARENT_MAIN']['holes'].values()]
    ph=[[25.8+y,115+x] for x,y in data['PARENT_PWR']['holes'].values()]
    shapes=fixed_sensor_columns(G,parameters['pcb_holes']['TX_improved'])
    shapes['main_antenna_cradle']=main_antenna_cradle(mh,G)
    shapes.update(main_antenna_cradle(mh,G,True))
    shapes['power_adapter']=power_adapter(ph)
    from parent_corner_mounts import sony_shapes,sony_holes
    shapes['sony_mount_plate']=sony_shapes(sony_holes(G),G)['sony_mount_plate']
    floor=Part.read(str(root/'parts/parent/interior/printed/parent_hand_service/floor_plate.step'))
    case=Part.read(str(root/'parts/parent/exterior/cots/bcas212310g/bcas212310g.step'))
    ring=ring_service(Part.read(str(root/'parts/parent/interior/printed/ann_mb1_internal_rack/ann_mb1_coax_ring.step')))
    ring.translate(A.Vector(60,60,18.8))
    def overlap(a,b):
        if not a.BoundBox.intersect(b.BoundBox):return 0.
        c=a.common(b);return 0. if c.isNull() else c.Volume
    def hull(points):
        p=sorted(set(points))
        def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
        lo=[];hi=[]
        for v in p:
            while len(lo)>1 and cross(lo[-2],lo[-1],v)<=0:lo.pop()
            lo.append(v)
        for v in reversed(p):
            while len(hi)>1 and cross(hi[-2],hi[-1],v)<=0:hi.pop()
            hi.append(v)
        return lo[:-1]+hi[:-1]
    rows=[]
    def check(name,label,x,y,z,direction,entry,axis='x',af=5.5,height=2.4,pocket_height=2.6):
        s=shapes[name]
        # Insertion at the middle of the pocket, before the screw is inserted.
        iz=z+(pocket_height-height)/2
        r=af/math.sqrt(3)
        points=[(x+r*math.cos(math.pi/6+i*math.pi/3),y+r*math.sin(math.pi/6+i*math.pi/3)) for i in range(6)]
        moved=[(px+entry*12 if axis=='x' else px,py+entry*12 if axis=='y' else py) for px,py in points]
        pp=[A.Vector(px,py,iz) for px,py in hull(points+moved)]
        swept=Part.Face(Part.makePolygon(pp+[pp[0]])).extrude(A.Vector(0,0,height))
        if axis=='z':swept=hex_tool(x,y,iz-12,af,12+height)
        clamp_z=z+pocket_height-height if direction>0 else z
        nut=hex_tool(x,y,clamp_z,af,height).cut(cyl(x,y,clamp_z-.1,1.5,height+.2))
        pushed=nut.copy();pushed.translate(A.Vector(0,0,direction*.1))
        rotate_probes=[]
        for angle in [-30,30]:
            rotated=nut.copy();rotated.rotate(A.Vector(x,y,0),A.Vector(0,0,1),angle)
            rotate_probes.append(overlap(rotated,s))
        record=dict(label=label,part=name,xy_mm=[x,y],nut_bottom_mm=clamp_z,
                    force_direction='+Z' if direction>0 else '-Z',
                    insertion_sweep_overlap_mm3=overlap(swept,s),seated_overlap_mm3=overlap(nut,s),
                    stop_probe_0_1mm_overlap_mm3=overlap(pushed,s),
                    nut_case_overlap_mm3=overlap(nut,case),rotation_stop_probe_pm30deg_mm3=rotate_probes)
        record['geometry_pass']=record['insertion_sweep_overlap_mm3']<.001 and record['seated_overlap_mm3']<.001 and record['stop_probe_0_1mm_overlap_mm3']>.1 and record['nut_case_overlap_mm3']<.001 and min(rotate_probes)>.01
        rows.append(record);print('FASTENER='+json.dumps(record),flush=True)
    direct=[]
    for row in retrofit_fasteners(G,mh,ph):
        if not row['label'].startswith(('main_pcb_','pwr_pcb_')):continue
        is_main=row['label'].startswith('main_')
        host=shapes['main_service_frame' if is_main else 'power_adapter']
        x,y=row['xy'];seat=44.95 if is_main else 33.75
        bottom=37.1 if is_main else 28.25;tip=row['head_z']-row['length']
        # PCB ring is the clamped member: head -> PCB -> boss -> plastic thread.
        pcb=cyl(x,y,seat+.05,3.1,1.6).cut(cyl(x,y,seat,1.6,1.8))
        down=pcb.copy();down.translate(A.Vector(0,0,-.1))
        head=cyl(x,y,row['head_z'],2.75,3)
        hd=head.copy();hd.translate(A.Vector(0,0,-.1))
        pilot=cyl(x,y,bottom+.2,1.39,seat-bottom-.4)
        slices=[]
        for i in range(12):
            z=tip+.15+(seat-tip-.3)*(i+.5)/12
            shell=cyl(x,y,z,1.5,.05).cut(cyl(x,y,z-.01,1.3,.07))
            slices.append(overlap(shell,host))
        rec=dict(label=row['label'],pilot_d_mm=2.8,screw_length_mm=row['length'],
                 nominal_engagement_mm=seat-tip,tip_to_boss_bottom_mm=tip-bottom,
                 pilot_core_overlap_mm3=overlap(pilot,host),pcb_overlap_mm3=overlap(pcb,host),
                 pcb_down_reaction_mm3=overlap(down,host),head_down_pcb_reaction_mm3=overlap(hd,pcb),
                 thread_shell_slices_mm3=slices)
        rec['passes']=rec['pilot_core_overlap_mm3']<.001 and rec['pcb_overlap_mm3']<.001 and min(slices)>.001 and rec['pcb_down_reaction_mm3']>.1 and rec['head_down_pcb_reaction_mm3']>.1 and seat-tip>=4 and tip-bottom>=1
        direct.append(rec)
    for i,(x,y) in enumerate(G.GROUND_PLATE_HOLES_XY):
        check('antenna_service_shelf','steel_'+str(i),x,y-12,58.5+ANT_LIFT,1,-1,'z',pocket_height=2.7)
    for i,x in enumerate([26,94]):
        check('antenna_service_shelf','antenna_'+str(i),x,48,58.5+ANT_LIFT,1,-1,'z',af=7,height=3.2,pocket_height=3.4)
    # Lower screw heads and washers, including the floor reaction surface.
    bearing=[]
    for x,y in G.UNIVERSAL_FRAME_FOOT_XY+[p for i,p in enumerate(G.SONY_CARRIER_FOOT_XY) if i!=2]+G.RACK_FOOT_XY:
        washer=cyl(x,y,8.34,3.5,.5).cut(cyl(x,y,8.24,1.6,.7))
        head=cyl(x,y,5.34,2.75,3)
        pushed=washer.copy();pushed.translate(A.Vector(0,0,.1))
        bearing.append(dict(xy_mm=[x,y],washer_floor_probe_mm3=overlap(pushed,floor),washer_case_overlap_mm3=overlap(washer,case),head_case_overlap_mm3=overlap(head,case)))
    # Validate the full plastic thread engagement and the actual clamped parts.
    placement=json.loads((root/'assemblies/parent_hand_service/placement.json').read_text(encoding='utf-8'))
    def placed(label):
        row=next(r for r in placement['items'] if r['label']==label)
        folder=root/row['part'];p=Part.read(str(folder/(row.get('file',folder.name)+'.step')))
        for op in reversed(row.get('ops',[])):
            if 'rotate' in op:
                for axis,angle in zip([A.Vector(1,0,0),A.Vector(0,1,0),A.Vector(0,0,1)],op['rotate']):p.rotate(A.Vector(),axis,angle)
            if 'translate' in op:p.translate(A.Vector(*op['translate']))
        return p
    clamp_shapes=dict(plate=floor,coax_ring=ring,main_service_frame=shapes['main_service_frame'],antenna_service_shelf=shapes['antenna_service_shelf'],
                      gnss_universal_carrier=placed('gnss_universal_carrier'),sony_mount_plate=shapes['sony_mount_plate'])
    hardware={r['label']:r for r in retrofit_fasteners(G,mh,ph)}
    spacer_checks=[]
    for spec in spacer_threads(G):
        row=hardware[spec['label']];x,y=row['xy'];lo=spec['zlo'];hi=spec['zhi'];host=shapes[spec['host']]
        clear=cyl(x,y,lo+.15,1.39,hi-lo-.3)
        outside=[];engaged=[]
        for i in range(12):
            z=lo+.2+(hi-lo-.4)*(i+.5)/12
            shell=cyl(x,y,z,1.5,.05).cut(cyl(x,y,z-.01,1.3,.07))
            wall=cyl(x,y,z,2,.05).cut(cyl(x,y,z-.01,1.55,.07))
            engaged.append(overlap(shell,host));outside.append(wall.cut(host).Volume)
        seat=host.common(cyl(x,y,lo-2,6,hi-lo+4));seat.translate(A.Vector(0,0,-spec['direction']*.1))
        held=clamp_shapes[spec['clamped']]
        rec=dict(**spec,xy_mm=[x,y],nominal_engagement_mm=hi-lo,thread_contact_slices_mm3=engaged,
                 missing_wall_slices_mm3=outside,pilot_core_overlap_mm3=overlap(clear,host),
                 reaction_probe_mm3=overlap(seat,held),length_mm=row['length'])
        rec['passes']=hi-lo>=4 and min(engaged)>.001 and max(outside)<.001 and rec['pilot_core_overlap_mm3']<.001 and rec['reaction_probe_mm3']>.05
        spacer_checks.append(rec)
    opposed=[]
    for i in range(4):
        low=hardware['cradle_floor_'+str(i)];high=hardware['cradle_service_'+str(i)]
        gap=(high['head_z']-high['length'])-(low['head_z']+low['length'])
        opposed.append(dict(label='cradle_'+str(i),nominal_tip_gap_mm=gap,passes=gap>=.49))
    adapter_clamps=[]
    for i,(x,y) in enumerate(ph):
        host=shapes['power_adapter'];head=cyl(x,y,30.25,2.75,3)
        down=head.copy();down.translate(A.Vector(0,0,-.1))
        foot=host.common(cyl(x,y,28.25,4.3,2));foot.translate(A.Vector(0,0,-.1))
        row=dict(label='pwr_adapter_'+str(i),head_overlap_mm3=overlap(head,host),head_down_stop_mm3=overlap(down,host),foot_floor_stop_mm3=overlap(foot,floor),seat_thickness_mm=2,nominal_plastic_thread_engagement_mm=6)
        row['passes']=row['head_overlap_mm3']<.001 and row['head_down_stop_mm3']>.1 and row['foot_floor_stop_mm3']>.1
        adapter_clamps.append(row)
    threads=[]
    for row in retrofit_fasteners(G,mh,ph):
        if row['nut_z'] is None:continue
        h=2.4 if row['diameter']==3 else 3.2
        tip=row['head_z']+row['direction']*row['length']
        a,b=sorted([tip,row['head_z']]);lo=row['nut_z'];hi=lo+h
        overlap_length=max(0,min(b,hi)-max(a,lo))
        tip_margin=lo-tip if row['direction']<0 else tip-hi
        threads.append(dict(label=row['label'],length_mm=row['length'],nominal_engagement_mm=overlap_length,nut_height_mm=h,tip_beyond_nut_mm=tip_margin,
                            passes=overlap_length>=h-1e-6 and tip_margin>=.3 and row['length']<=50))
    report=dict(status='GEOMETRY_ONLY',nuts=rows,floor_bearings=bearing,thread_lengths=threads,spacer_threads=spacer_checks,opposed_screws=opposed,adapter_clamps=adapter_clamps,direct_pcb=direct,
                limitations=['No preload, strength, creep, print tolerance or physical assembly validation.',
                             'Insertion sweep checks the printed host; assembly is performed outside the case before electronics installation.',
                             'Nut is manually held until the screw engages; installed screw constrains lateral escape.',
                             'Threads and tool fit are nominal envelopes, not measured inventory.'])
    print('FASTENER_REPORT='+json.dumps(report),flush=True)
    o=doc.addObject('Part::Feature','verification_marker');o.Label='NUMERIC CHECK MARKER - NOT PRINTABLE'
    o.Shape=Part.makeBox(1,1,1);o.addProperty('App::PropertyString','Report');o.Report=json.dumps(report)
    return [o]
