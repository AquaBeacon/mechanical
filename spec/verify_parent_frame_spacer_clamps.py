"""Read-only mating reaction, nut insertion and staged tool-path checks."""
from pathlib import Path
import json,sys
import FreeCAD as A,Part
R=Path(__file__).resolve().parents[1];W=R/'assemblies/parent_hand_service/_work/analysis/frame_spacers_20261024'
def main():
    rows=json.loads((R/'assemblies/parent_hand_service/placement.json').read_text(encoding='utf-8'))['items']
    wanted={'plate','coax_ring','main_service_frame','antenna_service_shelf','gnss_universal_carrier','sony_mount_plate'}
    scene={}
    for row in rows:
        name=row['label']
        if name not in wanted and not name.startswith(('gnss_fixed_','gnss_sony_shared_','sony_fixed_','cradle_floor_foot_')):continue
        folder=R/row['part'];s=Part.read(str(folder/(row.get('file',folder.name)+'.step')))
        for op in reversed(row.get('ops',[])):
            if 'translate' in op:s.translate(A.Vector(*op['translate']))
            elif 'rotate' in op:
                for axis,angle in zip([(1,0,0),(0,1,0),(0,0,1)],op['rotate']):s.rotate(A.Vector(),A.Vector(*axis),angle)
            else:raise ValueError(op)
        scene[name]=s
    sys.path.insert(0,str(R/'scad/lib'));import parent_gnss as G
    from parent_service_retrofit import hex_tool,cyl
    checks=[]
    def overlap(a,b):
        return a.common(b).Volume if a.BoundBox.intersect(b.BoundBox) else 0.
    def record(name,passed,**kw):
        checks.append(dict(name=name,passed=bool(passed),**kw))
    axes=[]
    for i,(x,y) in enumerate(G.RACK_FOOT_XY):axes.append(('cradle_floor_foot_'+str(i),x,y,21.8,33.4,'coax_ring','main_service_frame'))
    for i,(x,y) in enumerate(G.UNIVERSAL_FRAME_FOOT_XY):axes.append(('gnss_sony_shared_column' if i==3 else 'gnss_fixed_column_'+str(i),x,y,18.8,66,'plate','gnss_universal_carrier'))
    for i,(x,y) in enumerate(G.SONY_CARRIER_FOOT_XY):axes.append(('gnss_sony_shared_column' if i==2 else 'sony_fixed_column_'+str(i),x,y,18.8,60.5,'plate','sony_mount_plate'))
    for host,x,y,lo,hi,bottom,top in axes:
        for direction,z,target in [(-1,lo,bottom),(1,hi,top)]:
            patch=scene[host].common(Part.makeBox(10,10,3,A.Vector(x-5,y-5,z-1)))
            patch.translate(A.Vector(0,0,direction*.1));value=overlap(patch,scene[target])
            record(host+' '+str([x,y])+' '+('upper' if direction>0 else 'lower')+' bearing',value>.05,force_direction='+Z' if direction>0 else '-Z',probe_translation_mm=.1,overlap_mm3=value)
    hardware=json.loads((W/'publication.json').read_text(encoding='utf-8'))['hardware']
    for row in hardware:
        x,y=row['xy'];z=row['head_z']
        # Boards are installed after these bolts; floor is outside the case.
        driver=cyl(x,y,z+3.05,1.75,100-z)
        hits={name:overlap(driver,s) for name,s in scene.items() if driver.BoundBox.intersect(s.BoundBox)}
        record(row['label']+' vertical driver path',all(v<.001 for v in hits.values()),overlaps_mm3=hits,stage='PCBs not yet installed; printed fixtures assembled')
        if row['washer']:
            sweep=hex_tool(x,y,-10,5.5,18.34)
            value=overlap(sweep,scene['plate']);record(row['label']+' nut insertion from underside',value<.001,overlap_mm3=value,stage='floor removed from case')
            wrench=cyl(x,y,5.94,6,2)
            value=overlap(wrench,scene['plate']);record(row['label']+' thin wrench clearance',value<.001,overlap_mm3=value,envelope_diameter_mm=12,thickness_mm=2)
        else:
            nut=hex_tool(x,y,55.7,5.5,2.4)
            probes=[]
            for angle in [-30,30]:
                n=nut.copy();n.rotate(A.Vector(x,y,0),A.Vector(0,0,1),angle);probes.append(overlap(n,scene['gnss_sony_shared_column']))
            record(row['label']+' nut rotation stops',min(probes)>.01,rotation_deg=[-30,30],overlaps_mm3=probes)
    report=dict(passed=all(c['passed'] for c in checks),checks=checks,limitations=['Geometric nominal envelopes only; use a 2mm-thick 5.5mm wrench outside the case.','No strength, torque or physical assembly qualification.'])
    (W/'clamp_path_checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report),flush=True)
    assert report['passed'],[c for c in checks if not c['passed']]
main()
