"""Verify the thick Sony plate against the current canonical assembly, mm."""
from pathlib import Path
import sys,json
import FreeCAD as A,Part

def build(doc,parameters):
    root=Path(__file__).resolve().parents[1]
    sys.path.insert(0,str(root/'scad/lib'))
    import parent_gnss as G
    from parent_corner_mounts import sony_holes,sony_shapes,SONY_ARM_H,SONY_BOARD_LIFT,SONY_SEAT_Z
    data=json.loads((root/'assemblies/parent_hand_service/placement.json').read_text(encoding='utf-8'))
    holes=sony_holes(G)
    plate=sony_shapes(holes,G)['sony_mount_plate']
    scene={};rows={}
    for row in data['items']:
        n=row['label'];rows[n]=row
        if n=='sony_mount_plate':scene[n]=plate;continue
        folder=root/row['part'];p=folder/(row.get('file',folder.name)+'.step')
        s=Part.read(str(p))
        for op in reversed(row.get('ops',[])):
            if 'translate' in op:s.translate(A.Vector(*op['translate']))
            elif 'rotate' in op:
                for axis,angle in zip([(1,0,0),(0,1,0),(0,0,1)],op['rotate']):s.rotate(A.Vector(),A.Vector(*axis),angle)
            else:raise ValueError(op)
        # Candidate deltas only; canonical placement is changed after verification.
        if n=='spresense' or n.startswith('sony_mount_') or (n.startswith('retrofit_sony_top_') and n.endswith('_bolt')):
            s.translate(A.Vector(0,0,parameters.get('candidate_lift',SONY_BOARD_LIFT)))
        scene[n]=s
    def overlap(a,b):
        if not a.BoundBox.intersect(b.BoundBox):return 0.
        c=a.common(b);return 0. if c.isNull() else c.Volume
    checks=[]
    def check(name,value,passed):
        checks.append(dict(name=name,value=value,passed=bool(passed)))
        print('SONY_CHECK='+json.dumps(checks[-1]),flush=True)
    ignore={'sony_mount_plate','spresense'}
    for target in ['sony_mount_plate','spresense']:
        for n,s in scene.items():
            if n in ignore or n.startswith('sony_mount_'):continue
            if rows[n]['part'].endswith('/screw'):continue
            value=overlap(scene[target],s)
            check(target+' vs '+n,value,value<.001)
    c=overlap(plate,scene['spresense']);check('plate vs PCB/components',c,c<.001)
    fast=[]
    for i,(x,y) in enumerate(G.SONY_CARRIER_FOOT_XY):
        name='retrofit_sony_top_'+str(i)+'_bolt'
        head=G.SONY_COLUMN_JOINT_Z+SONY_ARM_H;tip=head-10
        host='gnss_sony_shared_column' if i==2 else 'sony_fixed_column_'+str(i)
        column=scene[host]
        # Bearing probe follows the full screw-head footprint; axial hole is excluded.
        ring=Part.makeCylinder(2.75,.1,A.Vector(x,y,head-.1)).cut(Part.makeCylinder(1.725,.2,A.Vector(x,y,head-.15)))
        bearing=overlap(plate,ring)
        contact=overlap(plate,Part.makeCylinder(2.6,.1,A.Vector(x,y,60.5)))
        thread=60.5-tip
        nut_name='retrofit_sony_top_'+str(i)+'_nut'
        nut_stop=None
        if nut_name in scene:
            nut=scene[nut_name];pushed=nut.copy();pushed.translate(A.Vector(0,0,1.0))
            nut_stop=overlap(pushed,column)
            check(nut_name+' axial retention +Z 1mm',nut_stop,nut_stop>.1)
            check(nut_name+' assembled fit',overlap(nut,column),overlap(nut,column)<.001)
        check(name+' head bearing mm3',bearing,bearing>.5)
        check(name+' column engagement mm',thread,thread>=6)
        # An assembled screw must pass through the unchanged clearance bore.
        shaft=Part.makeCylinder(1.5,3.2,A.Vector(x,y,60.5))
        check(name+' shaft clearance',overlap(shaft,plate),overlap(shaft,plate)<.001)
        fast.append(dict(label=name,head_z=head,tip_z=tip,engagement_mm=thread,bearing_probe_mm3=bearing,nut_stop_mm3=nut_stop))
    for i,(x,y) in enumerate(holes):
        head=67.2+SONY_BOARD_LIFT;tip=head-6
        check('PCB screw '+str(i)+' engagement mm',SONY_SEAT_Z-tip,SONY_SEAT_Z-tip>4)
        check('PCB screw '+str(i)+' floor clearance mm',tip-60.5,tip>60.5)
    check('TX reserved clearance mm',60.5-60.195,60.5>60.195)
    report=dict(thickness_mm=SONY_ARM_H,board_lift_mm=SONY_BOARD_LIFT,checks=checks,fasteners=fast,
                passed=all(x['passed'] for x in checks),limitations=['No physical torque, thread life or strength test.'])
    print('SONY_REPORT='+json.dumps(report),flush=True)
    assert report['passed'],[x for x in checks if not x['passed']]
    obj=doc.addObject('Part::Feature','sony_mount_plate');obj.Shape=plate
    return [obj]
