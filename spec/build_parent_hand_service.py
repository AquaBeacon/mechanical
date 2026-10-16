"""FreeCAD Python: explicit closed/service poses, captive lift carrier and hand sweeps.
Sources are existing downloaded Sony STEP and KiCad PCB; never simplify their solids.
"""
import FreeCAD as A, Part, MeshPart, Import
from pathlib import Path
import json, re, math, copy, sys
R=Path(__file__).resolve().parents[1]
O=R/'assemblies/parent_hand_service'; O.mkdir(exist_ok=True)
P=R/'parts/parent/interior/printed/parent_hand_service'; P.mkdir(exist_ok=True)
sys.path.insert(0,str(R/'scad/lib'))
import parent_gnss as GNSS
from cad_edge_finish import sharp_edges
def v(*p): return A.Vector(*p)
class CSG:
 def __init__(self,s,t): self.s,self.t=s,t
 def fuse(self,b): return CSG(self.s.fuse(b.s),'union(){'+self.t+b.t+'}')
 def cut(self,b): return CSG(self.s.cut(b.s),'difference(){'+self.t+b.t+'}')
def box(x,y,z,w,d,h): return CSG(Part.makeBox(w,d,h,v(x,y,z)),f'translate([{x},{y},{z}]) cube([{w},{d},{h}]);')
def cyl(x,y,z,r,h): return CSG(Part.makeCylinder(r,h,v(x,y,z)),f'translate([{x},{y},{z}]) cylinder(r={r},h={h},$fn=64);')
round_bore_mode=True
def bore(x,y,z,d,h):
 if round_bore_mode:
  relief=.4
  shape=Part.makeCylinder(d/2,h,v(x,y,z)).fuse(Part.makeCone(d/2+relief,d/2,relief,v(x,y,z))).fuse(Part.makeCone(d/2,d/2+relief,relief,v(x,y,z+h-relief)))
  return CSG(shape,f'translate([{x},{y},{z}]) union(){{cylinder(r={d/2},h={h},$fn=96);cylinder(r1={d/2+relief},r2={d/2},h={relief},$fn=96);translate([0,0,{h-relief}]) cylinder(r1={d/2},r2={d/2+relief},h={relief},$fn=96);}}')
 r=d/2/math.cos(math.pi/12); ps=[v(x+r*math.cos(i*math.pi/6),y+r*math.sin(i*math.pi/6),z) for i in range(12)]
 return CSG(Part.Face(Part.makePolygon(ps+[ps[0]])).extrude(v(0,0,h)),f'translate([{x},{y},{z}]) cylinder(r={r},h={h},$fn=12);')
def save(name,c):
 s=c.s.removeSplitter()
 if not s.isValid() or len(s.Solids)!=1:
  (P/'_work/intermediate').mkdir(parents=True,exist_ok=True)
  s.exportStep(str(P/'_work/intermediate'/(name+'_failed.step')))
 assert s.isValid() and len(s.Solids)==1,(name,[(q.Volume,str(q.BoundBox)) for q in s.Solids])
 s.exportStep(str(P/(name+'.step')))
 mesh=MeshPart.meshFromShape(Shape=s,LinearDeflection=.1,AngularDeflection=.2,Relative=False)
 mesh.write(str(P/(name+'.stl')))
 if name=='floor_plate':
  # Exact final analytic shape avoids repeatedly booleaning hundreds of holes
  # against chamfer polyhedra in OpenSCAD. Parameters remain in this generator.
  points,faces=mesh.Topology
  c.t='polyhedron(points='+json.dumps([[p.x,p.y,p.z] for p in points])+',faces='+json.dumps([list(f) for f in faces])+',convexity=10);'
 (P/(name+'.scad')).write_text('// Generated from the same CSG operations as STEP. Rebuild with spec/build_parent_hand_service.py.\n'+c.t,encoding='utf-8')
 return s
edge_finishing={}
def finished(c,name,requested):
 s=c.s.removeSplitter(); edges=sharp_edges(s)
 (P/'_work/intermediate').mkdir(parents=True,exist_ok=True)
 s.exportStep(str(P/'_work/intermediate'/(name+'_unfinished.step')))
 if name=='floor_plate':
  # Preserve the thin nut-capture roof and its open insertion lips. These are
  # existing mating/retention edges, not handling edges; rounding destroys fit.
  edges=[e for e in edges if not any(e.BoundBox.ZMin<14.0 and e.BoundBox.XMin>=x-4.1 and e.BoundBox.XMax<=x+4.1 and e.BoundBox.YMin>=y+dy-4.1 and e.BoundBox.YMax<=y+dy+4.2 for x,y in prop_centres for dy in [-9,9])]
  # Unchanged guide sockets and TX screw-seat interfaces must retain their
  # nominal footprints; their coincident mating edges are intentional.
  edges=[e for e in edges if not any(e.BoundBox.XMin>=x-5.1 and e.BoundBox.XMax<=x+5.1 and e.BoundBox.YMin>=y-13.1 and e.BoundBox.YMax<=y+13.1 for x,y in guides)]
  edges=[e for e in edges if not any(e.BoundBox.XMin>=x-3.6 and e.BoundBox.XMax<=x+3.6 and e.BoundBox.YMin>=y-3.6 and e.BoundBox.YMax<=y+3.6 for x,y in th)]
  edges=[e for e in edges if not any(e.BoundBox.XMin>=x-4.1 and e.BoundBox.XMax<=x+4.1 and e.BoundBox.YMin>=y-13.1 and e.BoundBox.YMax<=y+13.1 for x,y in prop_centres)]
  edges=[e for e in edges if max(e.BoundBox.XLength,e.BoundBox.YLength)>8 and abs(e.BoundBox.ZLength)<1e-6 and any(abs(e.BoundBox.ZMin-z)<1e-6 for z in [13.84,18.8])]
 print('FINISH START',name,len(edges),flush=True)
 if name=='floor_plate':
  # The base perimeter was chamfered before adding the functional fixtures;
  # all circular hole mouths use explicit conical relief in bore(). Preserve
  # existing guide/prop/nut interfaces rather than perturbing their fit.
  edge_finishing[name]=dict(chamfer_mm=.25,hole_mouth_relief_mm=.4,permitted_sharp_edges='Existing guide/prop seating, nut capture and boss attachment interfaces; retained to preserve their mating footprints')
  return c
 if name=='battery_base':
  # Only new handling edges at the open wire face; keep inherited seats/nuts.
  edges=[e for e in edges if abs(e.BoundBox.XMin+3.4)<1e-5 and abs(e.BoundBox.XMax+3.4)<1e-5 and e.BoundBox.YMin>=7.5-1e-5 and e.BoundBox.YMax<=47.5+1e-5 and e.BoundBox.ZMin>=3-1e-5]
  assert edges
  ss=s.makeChamfer(.2,edges)
  assert ss.isValid() and len(ss.Solids)==1
  mesh=MeshPart.meshFromShape(Shape=ss,LinearDeflection=.025,AngularDeflection=.1,Relative=False)
  points,faces=mesh.Topology
  edge_finishing[name]=dict(chamfer_mm=.2,new_wire_face_edges_treated=len(edges),hole_mouth_relief_mm=.4,permitted_sharp_edges='Inherited foam cavity, floor bearing and captured nut interfaces retain their mating dimensions')
  return CSG(ss,'polyhedron(points='+json.dumps([[p.x,p.y,p.z] for p in points])+',faces='+json.dumps([list(f) for f in faces])+',convexity=10);')
 if name=='lift_carrier':
  edges=[e for e in edges if e.BoundBox.XMin>=18.9 and e.BoundBox.XMax<=132.1 and e.BoundBox.YMin>=183.9 and e.BoundBox.YMax<=190.2 and e.BoundBox.ZMin>=54.4 and e.BoundBox.ZMax<=58.9]
 for amount in [requested,.1,.05,.025]:
  try:
   ss=s.makeChamfer(amount,edges)
   if not ss.isValid() or len(ss.Solids)!=1:continue
   mesh=MeshPart.meshFromShape(Shape=ss,LinearDeflection=.05,AngularDeflection=.15,Relative=False)
   points,faces=mesh.Topology
   edge_finishing[name]=dict(chamfer_mm=amount,sharp_edges_treated=len(edges),permitted_sharp_edges='Existing nut-capture roof and insertion lips preserve the documented M3 nut interface' if name=='floor_plate' else [])
   print('FINISHED',name,amount,len(edges),flush=True)
   return CSG(ss,'polyhedron(points='+json.dumps([[p.x,p.y,p.z] for p in points])+',faces='+json.dumps([list(f) for f in faces])+',convexity=10);')
  except Part.OCCError:pass
 if name=='lift_carrier':
  edge_finishing[name]=dict(hole_mouth_relief_mm=.4,permitted_sharp_edges='Existing slider tongues, board bearing pads and support interfaces',edge_finishing_status='Outer legacy geometry retained; new rear storage cut requires manual deburring before use')
  return c
 raise RuntimeError('Cannot finish '+name)
def holes(board):
 text=(R.parent/'hardware/pcb'/board/(board+'.kicad_pcb')).read_text(encoding='utf-8'); out=[]
 starts=[m.start() for m in re.finditer(r'\(footprint ',text)]
 for a,b in zip(starts,starts[1:]+[len(text)]):
  t=text[a:b]
  if re.search(r'\(property "Reference" "H[1-4]"',t):
   at=re.search(r'\(at ([\d.-]+) ([\d.-]+)',t); out.append([float(at[1]),float(at[2])])
 assert len(out)==4;return out

def build_battery_base():
 global bc
 # Compact battery retainer variant; reuse six compliant pads and lid CAD unchanged.
 src=R/'parts/parent/interior/printed/parent_lipo_retainer'
 bc=json.loads((src/'dimensions.json').read_text()); cap=29
 base=finished(box(-4,5,0,111,45,29),'battery_outer_perimeter',.2)
 for x in [0,103]:base=base.fuse(finished(box(x-4,-4.5,0,8,63.5,12),'battery_mount_rail_'+str(x),.2))
 for x,y in bc['bolt_xy']:base=base.fuse(cyl(x,y,0,4,29))
 base=base.cut(box(-1.5,7.5,3,106,40,29))
 # Leads emerge from both edges of the west end: no lip, roof or end foam
 # may cross the full 40 mm insertion/wire opening above the 3 mm floor.
 base=base.cut(box(-4.2,7.5,3,2.8,40,27))
 for x,y in [[0,0],[103,0],[0,55.5],[103,55.5]]:base=base.cut(bore(x,y,-.1,3.45,3.2)).cut(cyl(x,y,3,3.1,30))
 for x,y in [bc['bolt_xy'][0]]:
  base=base.cut(bore(x,y,-.1,3.45,29.2))
  from parent_battery_slide import nut_socket,finish_nut_roof
  socket=nut_socket(x,y)
  before_socket=base.s
  base=base.cut(CSG(socket,''))
  base=CSG(finish_nut_roof(base.s,socket,before_socket),'')
 base=base.cut(box(-4.2,-5,-.1,.8,65,30))
 from parent_case_access import finish_cut,BATTERY_TOOL_D
 from parent_battery_slide import base_sockets
 base=finished(base,'battery_base',.2)
 base=CSG(base_sockets(base.s,bc['bolt_xy']),'')
 base=CSG(finish_cut(base.s,1,GNSS.BATTERY_ORIGIN,GNSS.BATTERY_ROTATION[2],diameter=BATTERY_TOOL_D),'')
 # The aperture also belongs in the generated SCAD, from the final analytic solid.
 mesh=MeshPart.meshFromShape(Shape=base.s,LinearDeflection=.025,AngularDeflection=.1,Relative=False)
 points,faces=mesh.Topology
 base.t='polyhedron(points='+json.dumps([[p.x,p.y,p.z] for p in points])+',faces='+json.dumps([list(f) for f in faces])+',convexity=10);'
 save('battery_base',base)
 from parent_battery_slide import nut_support_blocker
 blocker=nut_support_blocker(bc['bolt_xy'])
 blocker.exportStep(str(P/'battery_lid_nut_support_blocker.step'))
 MeshPart.meshFromShape(Shape=blocker,LinearDeflection=.025,AngularDeflection=.1,Relative=False).write(str(P/'battery_lid_nut_support_blocker.stl'))
 from parent_battery_slide import rail_support_blocker
 blocker=rail_support_blocker()
 blocker.exportStep(str(P/'battery_slide_rail_support_blocker.step'))
 MeshPart.meshFromShape(Shape=blocker,LinearDeflection=.025,AngularDeflection=.1,Relative=False).write(str(P/'battery_slide_rail_support_blocker.stl'))
 edge_finishing['battery_base'].update(case_access_hole_mm=BATTERY_TOOL_D,case_access_chamfer_mm=.2,nut_roof='Hex taper >=45 degrees; triangular side-entry roof50 degrees; external mouth chamfer0.1',permitted_sharp_edges='Inherited nut floor/hex capture and internal roof ridges retain nut fit and steep planar printing profile')
 # Variant of the inherited non-print foam: keep top, sides and far end.
 # The two west-end pieces obstruct the user's two lead exits.
 pads=Part.read(str(src/'parent_lipo_retainer_pads.step'))
 keep=[q for q in pads.Solids if q.BoundBox.XMax>1]
 assert len(keep)==4
 pads=Part.makeCompound(keep)
 pads.exportStep(str(P/'battery_pads_open_end.step'))
 MeshPart.meshFromShape(Shape=pads,LinearDeflection=.025,AngularDeflection=.1,Relative=False).write(str(P/'battery_pads_open_end.stl'))

if '--battery-only' in sys.argv:
 build_battery_base()
 current=json.loads((O/'edge_finishing.json').read_text())
 current.update(edge_finishing)
 (O/'edge_finishing.json').write_text(json.dumps(current,indent=2),encoding='utf-8')
 raise SystemExit(0)
if '--case-access-only' in sys.argv:
 # Rebuild only upper parts; do not execute the floor generator.
 build_battery_base()
 from parent_corner_mounts import main_shapes
 mh=[[GNSS.MAIN_ORIGIN[0]+x,GNSS.MAIN_ORIGIN[1]-y] for x,y in holes('PARENT_MAIN')]
 s=main_shapes(mh,GNSS)['main_mount_plate']
 mesh=MeshPart.meshFromShape(Shape=s,LinearDeflection=.025,AngularDeflection=.1,Relative=False)
 points,faces=mesh.Topology
 save('main_mount_plate',CSG(s,'polyhedron(points='+json.dumps([[p.x,p.y,p.z] for p in points])+',faces='+json.dumps([list(f) for f in faces])+',convexity=10);'))
 current=json.loads((O/'edge_finishing.json').read_text());current.update(edge_finishing)
 current['main_mount_plate'].update(case_access_hole_mm=4.2,case_access_chamfer_mm=.15)
 (O/'edge_finishing.json').write_text(json.dumps(current,indent=2),encoding='utf-8')
 raise SystemExit(0)
body=(R/'spec/parent_switch_tx_body.py').read_text(encoding='utf-8')
if any(flag in sys.argv for flag in ['--corner-only','--main-only','--sony-only']):
 exec(compile(body.split('guides=[];prop_centres=[]')[0],str(R/'spec/parent_switch_tx_body.py'),'exec'))
 exec(compile('# MAIN rotated'+body.split('# MAIN rotated',1)[1].split("old=json.loads((R/'assemblies/parent_service_review/placement.json').read_text(encoding='utf-8'))",1)[0],str(R/'spec/parent_switch_tx_body.py'),'exec'))
 current=json.loads((O/'edge_finishing.json').read_text());current.update(edge_finishing)
 (O/'edge_finishing.json').write_text(json.dumps(current,indent=2),encoding='utf-8')
 raise SystemExit(0)
if '--floor-only' in sys.argv:
 exec(compile(body.split('# Battery source')[0],str(R/'spec/parent_switch_tx_body.py'),'exec'))
 current=json.loads((O/'edge_finishing.json').read_text()) if (O/'edge_finishing.json').exists() else {}
 current.update(edge_finishing)
 (O/'edge_finishing.json').write_text(json.dumps(current,indent=2),encoding='utf-8')
 raise SystemExit(0)
if '--assemblies-only' in sys.argv:
 # Only for independently rebuilt CAD; never used as a substitute for a build.
 head,tail=body.split("old=json.loads((R/'assemblies/parent_service_review/placement.json').read_text(encoding='utf-8'))",1)
 exec(compile(head.split('guides=[];prop_centres=[]')[0],str(R/'spec/parent_switch_tx_body.py'),'exec'))
 bc=json.loads((R/'parts/parent/interior/printed/parent_lipo_retainer/dimensions.json').read_text())
 edge_finishing=json.loads((O/'edge_finishing.json').read_text())
 exec(compile("old=json.loads((R/'assemblies/parent_service_review/placement.json').read_text(encoding='utf-8'))"+tail,str(R/'spec/parent_switch_tx_body.py'),'exec'))
else:
 exec(compile(body,str(R/'spec/parent_switch_tx_body.py'),'exec'))
