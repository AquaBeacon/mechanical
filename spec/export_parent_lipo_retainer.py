import FreeCAD as A,Part,Mesh,MeshPart,json,math,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];P=R/'parts/parent/interior/printed/parent_lipo_retainer'
c=json.loads((P/'dimensions.json').read_text()); cap=c['floor']+c['h']+c['top_gap'];bl=c['l']+2*c['end_gap']+2*c['wall'];bw=c['w']+2*c['side_gap']+2*c['wall']
def box(x,y,z,w,d,h):return Part.makeBox(w,d,h,A.Vector(x,y,z))
def cyl(x,y,z,r,h):return Part.makeCylinder(r,h,A.Vector(x,y,z))
def poly(x,y,z,r,n,h):
 ps=[A.Vector(x+r*math.cos(2*math.pi*i/n),y+r*math.sin(2*math.pi*i/n),z) for i in range(n)]
 return Part.Face(Part.makePolygon(ps+[ps[0]])).extrude(A.Vector(0,0,h))
def bore(x,y,z,d,h):return poly(x,y,z,d/2/math.cos(math.pi/12),12,h)
if '--slide-lid-only' in sys.argv:
 sys.path.insert(0,str(R/'scad/lib'))
 from parent_battery_slide import lid
 s=lid(c['bolt_xy']);stem='parent_lipo_retainer_lid_slide'
 s.exportStep(str(P/(stem+'.step')))
 mesh=MeshPart.meshFromShape(Shape=s,LinearDeflection=.025,AngularDeflection=.1,Relative=False)
 assert mesh.isSolid();mesh.write(str(P/(stem+'.stl')))
 points,faces=mesh.Topology
 (P/(stem+'.scad')).write_text('// Generated variant by spec/export_parent_lipo_retainer.py --slide-lid-only.\npolyhedron(points='+json.dumps([[p.x,p.y,p.z] for p in points])+',faces='+json.dumps([list(reversed(f)) for f in faces])+',convexity=10);',encoding='utf-8')
 print('Built slide lid; legacy retainer outputs unchanged',flush=True)
 raise SystemExit(0)
mounts=[[0,0],[103,0],[0,75.5],[103,75.5]];bolts=c['bolt_xy']
base=box(-4,5,0,bl,bw,cap)
for x in [0,103]:base=base.fuse(box(x-4,-4.5,0,8,84.5,12))
for x,y in bolts:base=base.fuse(cyl(x,y,0,4,cap))
base=base.cut(box(-1.5,7.5,3,c['l']+4,c['w']+6,cap))
base=base.cut(box(-4.1,19.5,5,2.7,16,cap-7))
for x,y in mounts:base=base.cut(bore(x,y,-.1,3.45,3.2)).cut(cyl(x,y,3,3.1,cap+1))
for x,y in bolts:
 base=base.cut(bore(x,y,-.1,3.45,cap+.2))
 base=base.cut(poly(x,y,21.5,5.8/math.cos(math.pi/6)/2,6,2.5))
 base=base.cut(box(x-5.8/math.cos(math.pi/6)/2,y-4.5 if y==5 else y,21.5,5.8/math.cos(math.pi/6),4.5,2.5))
base=base.removeSplitter();lid=box(-4,1,0,bl,53,3)
for x,y in bolts:lid=lid.cut(bore(x,y,-.1,3.45,3.2))
pads=[box(1,11,26,101,33,3),box(20,7.5,3.5,63,3,22),box(20,44.5,3.5,63,3,22),box(102.5,11,3.5,2,33,22),box(-1.5,11,3.5,2,8,22),box(-1.5,36,3.5,2,8,22)]
checks=[]
for suffix,s in [('base',base),('lid',lid),('pads',Part.makeCompound(pads)),('lid_narrow',lid.cut(box(-4.1,-1,-.1,.7,60,3.2)))]:
 assert s.isValid() and (suffix=='pads' or len(s.Solids)==1)
 stem='parent_lipo_retainer_'+suffix;s.exportStep(str(P/(stem+'.step')))
 if suffix=='lid_narrow':
  subprocess.run(['C:/Program Files/OpenSCAD/openscad.exe','-o',str(P/(stem+'.stl')),'-D','part="lid"','-D','west_trim=0.6',str(P/'parent_lipo_retainer.scad')],check=True,capture_output=True,creationflags=0x08000000)
 mesh=Mesh.Mesh(str(P/(stem+'.stl')))
 diff=max(abs(getattr(s.BoundBox,k)-getattr(mesh.BoundBox,k)) for k in ['XMin','YMin','ZMin','XMax','YMax','ZMax'])
 delta=abs(s.Volume-mesh.Volume)/s.Volume
 checks.append(dict(part=stem,valid_step=s.isValid(),closed_stl=mesh.isSolid(),bbox_difference_mm=diff,relative_volume_difference=delta))
 assert mesh.isSolid() and diff<.05 and delta<.02,checks[-1]
 print(checks[-1],flush=True)
# Verify constraint chain, at nominal pack size. Faces constrain all six translation directions.
pack=box(.5,10.5,3,102,34,23)
contacts={'-Z_floor':pack.distToShape(base)[0],'+Z_top_pad':pack.distToShape(pads[0])[0],'-Y_side_pad':pack.distToShape(pads[1])[0],'+Y_side_pad':pack.distToShape(pads[2])[0],'+X_end_pad':pack.distToShape(pads[3])[0],'-X_end_pads':max(pack.distToShape(pads[i])[0] for i in [4,5])}
assert max(contacts.values())<1e-5,contacts
assert pack.common(base).Volume<.01
assert pack.common(Part.makeCompound(pads)).Volume<.01
for pad in pads:assert pad.common(base).Volume<.01
assert base.distToShape(lid.translated(A.Vector(0,0,cap)))[0]<1e-5
assert pads[0].distToShape(lid.translated(A.Vector(0,0,cap)))[0]<1e-5
# Direct metal fastener placement is checked separately against assembly; nut/screw threading is intentional.
report={'reference':c['reference'],'six_direction_contact_distance_mm':contacts,'rigid_lid_stop_z_local_mm':cap,'installed_foam_top_mm':3,'retainer_max_z_box_mm':51.4+cap+3+2,'enclosure_lid_z_mm':90.9,'part_checks':checks,'condition':'Nominal pack 102x34x23; choose foam/shims from actual measurements, no direct rigid clamping.'}
(P/'verification.json').write_text(json.dumps(report,indent=2));print('PASS 6 directions',contacts,flush=True)
