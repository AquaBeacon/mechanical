"""Measured holes, coplanar contact, clearances and scope of the fixture change."""
from parent_access_common import *
import hashlib, sys, Mesh
sys.path.insert(0,str(R/'scad/lib'))
import parent_gnss as G

d,c=load();rows=[]
frame=c['gnss_universal_carrier'];board=c['gnss_universal_pcb']
expected=[[G.UNIVERSAL_ORIGIN[0]+x,G.UNIVERSAL_ORIGIN[1]+y] for y in [2.5,77.5] for x in [2.5,57.5]]
assert expected==G.universal_mounting_xy()
for i,(x,y) in enumerate(expected):
    for name,shape,z,h,r in [('PCB M3 through hole',board,56.05,1.5,1.5),('printed M3 bore',frame,50.05,5.9,1.72)]:
        volume=common(shape,Part.makeCylinder(r,h,v(x,y,z)))
        rows.append(dict(name=f'{name} {i}',pass_=volume<.001,overlap_mm3=volume))
    bearing=frame.common(Part.makeCylinder(2.5,.2,v(x,y,55.8)))
    rows.append(dict(name=f'PCB support contact {i}',pass_=bearing.Volume>.1 and bearing.distToShape(board)[0]<.001))
rows.append(dict(name='Sensor and universal PCB bottoms both Z56',pass_=abs(c['magnetometer'].BoundBox.ZMin-board.BoundBox.ZMin)<.001 and abs(board.BoundBox.ZMin-56)<.001))
# The single printed body joins each sensor rail to the GNSS west/rear rails.
rows.append(dict(name='Connected support frame',pass_=frame.isValid() and len(frame.Solids)==1))
for x in sorted(set(x for x,y in G.magnetometer_mounting_xy())):
    contact=frame.common(Part.makeBox(2,.2,2,v(x-1,218.9,52)))
    rows.append(dict(name=f'Sensor longitudinal rail joins rear beam X{x}',pass_=contact.Volume>.1))
for y in sorted(set(y for x,y in G.magnetometer_mounting_xy())):
    contact=frame.common(Part.makeBox(.2,2,2,v(G.UNIVERSAL_ORIGIN[0]+.5,y-1,52)))
    rows.append(dict(name=f'Sensor transverse rail joins GNSS X rail Y{y}',pass_=contact.Volume>.1))
changed=['gnss_universal_carrier','gnss_universal_pcb','gnss_receiver','gnss_sma_plug','gnss_pin_headers','gnss_xh_keepout','gnss_coax_route','magnetometer']+[n for n in c if n.startswith(('gnss_pcb_', 'mag_bolt_', 'mag_nut_'))]
for n in changed:
    col=collisions(c[n],c,[n])
    rows.append(dict(name=n+' final occupied geometry',pass_=not col,collisions=col))
W=O/'_work/analysis/sensor_mounts_20261011';baseline=json.loads((W/'baseline.json').read_text(encoding='utf-8'))
prior=W/'intermediate/frame_before_switch_relief.step'
if prior.exists():
    oldframe=Part.read(str(prior))
    added=frame.cut(oldframe).Volume
    rows.append(dict(name='Switch relief only removes material from the assembly-path-verified frame',pass_=added<.01,added_material_mm3=added,prior_volume_mm3=oldframe.Volume,current_volume_mm3=frame.Volume))
unaffected=[]
for name,old in baseline.items():
    if name in changed or name.startswith(('gnss_edge_cap_','gnss_cap_screw_')):continue
    it=next(it for it in d['items'] if it['label']==name)
    p=R/it['part']/(it.get('file',Path(it['part']).name)+'.step')
    ok=it==old['item'] and hashlib.sha256(p.read_bytes()).hexdigest()==old['sha256']
    rows.append(dict(name=name+' unchanged placement and STEP hash',pass_=ok));unaffected.append(name)
mesh=Mesh.Mesh(str(R/'parts/parent/interior/printed/gnss_universal_carrier/gnss_universal_carrier.stl'))
bb=frame.optimalBoundingBox(False,False);mb=mesh.BoundBox
delta=max(abs(getattr(bb,k)-getattr(mb,k)) for k in ['XMin','XMax','YMin','YMax','ZMin','ZMax'])
diff=abs(frame.Volume-mesh_volume(mesh))/frame.Volume
rows.append(dict(name='Closed STL and analytic STEP agreement',pass_=mesh.isSolid() and delta<.05 and diff<.02,bbox_difference_mm=delta,relative_volume_difference=diff))
report=dict(status='PASS' if all(r['pass_'] for r in rows) else 'FAIL',checks=rows,holes_xy_mm=expected,pitch_XY_mm=[55,75],edge_offsets_mm=[2.5,2.5],unchanged_components=unaffected,frame_bounds_mm=[bb.XMin,bb.YMin,bb.ZMin,bb.XMax,bb.YMax,bb.ZMax],frame_volume_mm3=frame.Volume,gnss_nut_to_right_column_nominal_X_gap_mm=130.5-(expected[1][0]+5.5/3**.5),minimum_M3_rail_edge_ligament_mm=3.5-(3.45/2)/__import__('math').cos(__import__('math').pi/8),structural_validation='No load/FEA/creep/physical validation; connected geometry and four bearing contacts only',manufacturing_release=False)
path=O/'sensor_mount_checks.json';path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(report['status'],[r for r in rows if not r['pass_']],flush=True)
assert report['status']=='PASS'
