"""Build and geometrically verify clearance spacers and bed-flat MAIN frame."""
from pathlib import Path
import json,sys
import FreeCAD as A,Part

def build(doc,parameters):
    root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'scad/lib'))
    import parent_gnss as G
    from parent_service_retrofit import main_antenna_cradle,fixed_sensor_columns,retrofit_fasteners,hex_tool,cyl,variant_folder,power_adapter,ring_service
    data=json.loads((root/'assemblies/parent_hand_service/_work/analysis/retrofit_20261024/interfaces.json').read_text(encoding='utf-8'))
    mh=[[18+x,112-y] for x,y in data['PARENT_MAIN']['holes'].values()]
    ph=[[25.8+y,115+x] for x,y in data['PARENT_PWR']['holes'].values()]
    shapes=main_antenna_cradle(mh,G,True)
    shapes.update(fixed_sensor_columns(G,parameters['pcb_holes']['TX_improved']))
    shapes['power_adapter']=power_adapter(ph)
    from parent_corner_mounts import sony_shapes,sony_holes
    shapes['sony_mount_plate']=sony_shapes(sony_holes(G),G)['sony_mount_plate']
    ring=Part.read(str(root/'parts/parent/interior/printed/ann_mb1_internal_rack/ann_mb1_coax_ring.step'))
    shapes['ann_mb1_coax_ring_service']=ring_service(ring)
    rows=json.loads((root/'assemblies/parent_hand_service/placement.json').read_text(encoding='utf-8'))['items']
    scene={};rowmap={}
    for row in rows:
        label=row['label'];rowmap[label]=row
        if parameters.get('diagnostic') and label not in ['p_pwr','power_adapter']:continue
        if label.startswith('retrofit_') and any(label.startswith('retrofit_'+p) for p in ['cradle_floor_','cradle_service_','gnss_floor_','gnss_top_','sony_floor_','sony_top_']):continue
        if label in shapes:scene[label]=shapes[label];continue
        folder=root/row['part'];s=Part.read(str(folder/(row.get('file',folder.name)+'.step')))
        for op in reversed(row.get('ops',[])):
            if 'translate' in op:s.translate(A.Vector(*op['translate']))
            elif 'rotate' in op:
                for axis,angle in zip([(1,0,0),(0,1,0),(0,0,1)],op['rotate']):s.rotate(A.Vector(),A.Vector(*axis),angle)
            else:raise ValueError(op)
        scene[label]=s
    def overlap(a,b):
        if not a.BoundBox.intersect(b.BoundBox):return 0.
        return a.common(b).Volume
    checks=[]
    def check(name,passed,**details):
        rec=dict(name=name,passed=bool(passed),**details);checks.append(rec)
        print('PRINTABILITY_CHECK='+json.dumps(rec),flush=True)
    frame=shapes['main_service_frame']
    old=Part.read(str(root/variant_folder('main_service_frame')/'main_service_frame.step'))
    added=frame.cut(old)
    for label,target in scene.items():
        if label=='main_service_frame' or rowmap[label]['part'].endswith('/screw'):continue
        vol=overlap(added,target)
        if added.BoundBox.intersect(target.BoundBox):check('frame added material vs '+label,vol<.001,volume_mm3=vol,overlap_bounds=str(added.common(target).BoundBox))
    if parameters.get('diagnostic'):
        obj=doc.addObject('Part::Feature','main_service_frame');obj.Shape=frame
        return [obj]
    # First-layer footprint must contain the former Z37.1 horizontal grid faces.
    raised=[]
    for f in frame.Faces:
        if f.BoundBox.ZLength<1e-6 and f.normalAt(0,0).z<-.99 and f.Area>5 and f.BoundBox.ZMin>33.401:
            raised.append(dict(z=f.BoundBox.ZMin,area=f.Area))
    check('frame horizontal underside at print datum',not raised,raised_faces=raised)
    paths=[]
    for i,(x,y) in enumerate(G.RACK_FOOT_XY):paths.append(('cradle_floor_foot_'+str(i),x,y,21.8,33.4))
    for i,(x,y) in enumerate(G.UNIVERSAL_FRAME_FOOT_XY):paths.append(('gnss_sony_shared_column' if i==3 else 'gnss_fixed_column_'+str(i),x,y,18.8,66.8))
    for i,(x,y) in enumerate(G.SONY_CARRIER_FOOT_XY):paths.append(('gnss_sony_shared_column' if i==2 else 'sony_fixed_column_'+str(i),x,y,18.8,61.3))
    for name,x,y,lo,hi in paths:
        vol=overlap(cyl(x,y,lo-.1,1.75,hi-lo+.2),shapes[name])
        check(name+' M3 clearance '+str([x,y]),vol<.001,diameter_mm=3.5,volume_mm3=vol)
    hardware=[r for r in retrofit_fasteners(G,mh,ph) if r['label'].startswith(('cradle_service_','gnss_top_','sony_top_'))]
    for row in hardware:
        x,y=row['xy'];headz=row['head_z'];tip=headz-row['length'];nz=row['nut_z']
        nut=hex_tool(x,y,nz,5.5,2.4).cut(cyl(x,y,nz-.1,1.5,2.6))
        head=cyl(x,y,headz,2.75,3);shaft=cyl(x,y,tip,1.5,row['length'])
        washer=cyl(x,y,8.34,3.5,.5).cut(cyl(x,y,8.24,1.6,.7)) if row['washer'] else Part.Shape()
        metal=Part.makeCompound([head,shaft,nut]+([washer] if row['washer'] else []))
        for label,target in scene.items():
            if rowmap[label]['part'].endswith('/screw'):continue
            if not metal.BoundBox.intersect(target.BoundBox):continue
            vol=overlap(metal,target);check(row['label']+' vs '+label,vol<.001,volume_mm3=vol)
        # Full nut engagement, lower nut reaction into floor through washer,
        # and upper head reaction into the clamped frame/plate.
        check(row['label']+' full nut engagement',tip<=nz-.3,tip_z=tip,nut_bottom_z=nz,tip_projection_mm=nz-tip)
        host='main_service_frame' if row['label'].startswith('cradle') else 'gnss_universal_carrier' if row['label'].startswith('gnss') else 'sony_mount_plate'
        probe=head.copy();probe.translate(A.Vector(0,0,-.1))
        reaction=overlap(probe,scene[host]);check(row['label']+' head reaction',reaction>.05,volume_mm3=reaction)
        if row['washer']:
            probe=washer.copy();probe.translate(A.Vector(0,0,.1));reaction=overlap(probe,scene['plate'])
            check(row['label']+' floor reaction',reaction>.05,volume_mm3=reaction)
            # Nut->washer must stop +Z movement; washer->floor stops lift-off.
            probe=nut.copy();probe.translate(A.Vector(0,0,.1));reaction=overlap(probe,washer)
            check(row['label']+' nut axial stop',reaction>.05,volume_mm3=reaction)
        else:
            # Side insertion sweep for the Sony axis above a case boss.
            sweep=hex_tool(x,y,55.6,5.5,2.4).fuse(Part.makeBox(5.5,8,2.4,A.Vector(x-2.75,y,55.6)))
            check(row['label']+' nut insertion',overlap(sweep,shapes['gnss_sony_shared_column'])<.001,volume_mm3=overlap(sweep,shapes['gnss_sony_shared_column']))
            probe=nut.copy();probe.translate(A.Vector(0,0,.3));reaction=overlap(probe,shapes['gnss_sony_shared_column'])
            check(row['label']+' captured roof reaction',reaction>.05,volume_mm3=reaction)
    report=dict(passed=all(c['passed'] for c in checks),checks=checks,fasteners=hardware,parts=list(shapes),
                limitations=['Geometry only; physical torque, creep and printed fits unverified.'])
    print('FRAME_SPACER_REPORT='+json.dumps(report),flush=True)
    assert report['passed'],[c for c in checks if not c['passed']]
    out=[]
    for name,s in shapes.items():
        assert s.isValid() and len(s.Solids)==1,(name,len(s.Solids))
        obj=doc.addObject('Part::Feature',name);obj.Shape=s;out.append(obj)
    return out
