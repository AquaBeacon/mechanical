"""STL-only four-piece polygon variant derived from the existing MAIN interface.

The round source remains the assembly reference. This requested print variant
uses its STEP datums, never a second copy of the height/bore dimensions.
"""
import hashlib
import json
import math
from pathlib import Path
import subprocess
import FreeCAD as A
import Part
import MeshPart
import Mesh

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'parts/parent/interior/printed/parent_hand_service'
OUT=ROOT/'assemblies/parent_hand_service'
WORK=OUT/'_work/analysis/main_polygon_4'
JOB=OUT/'print_jobs/main_polygon_4'
WORK.mkdir(parents=True,exist_ok=True);JOB.mkdir(parents=True,exist_ok=True)
v=A.Vector
OUTER_SIDES=6
BORE_SIDES=8
EDGE_CHAMFER=.10
MOUTH_CHAMFER=.15
PITCH=12.0

reference=Part.read(str(P/'main_corner_column.step'))
b=reference.optimalBoundingBox(False,False)
HEIGHT=b.ZLength
OUTER_RADIUS=b.XLength/2
radii=[f.Surface.Radius for f in reference.Faces if isinstance(f.Surface,Part.Cylinder)]
BORE_DIAMETER=2*min(radii)
assert abs(HEIGHT-14.3)<.001 and abs(BORE_DIAMETER-3.45)<.001

def wire(radius,sides,z,angle=0):
    points=[v(radius*math.cos(angle+2*math.pi*i/sides),radius*math.sin(angle+2*math.pi*i/sides),z) for i in range(sides)]
    return Part.makePolygon(points+[points[0]])

outer=Part.Face(wire(OUTER_RADIUS,OUTER_SIDES,0)).extrude(v(0,0,HEIGHT))
# Treat the six long outside corners as well as both end rims.
outer=outer.makeChamfer(EDGE_CHAMFER,outer.Edges)
assert outer.isValid() and len(outer.Solids)==1
hole_radius=(BORE_DIAMETER/2)/math.cos(math.pi/BORE_SIDES)
mouth_radius=(BORE_DIAMETER/2+MOUTH_CHAMFER)/math.cos(math.pi/BORE_SIDES)
angle=math.pi/BORE_SIDES
tool=Part.Face(wire(hole_radius,BORE_SIDES,-.1,angle)).extrude(v(0,0,HEIGHT+.2))
tool=tool.fuse(Part.makeLoft([wire(mouth_radius,BORE_SIDES,0,angle),wire(hole_radius,BORE_SIDES,MOUTH_CHAMFER,angle)],True,True))
tool=tool.fuse(Part.makeLoft([wire(hole_radius,BORE_SIDES,HEIGHT-MOUTH_CHAMFER,angle),wire(mouth_radius,BORE_SIDES,HEIGHT,angle)],True,True))
single=outer.cut(tool).removeSplitter()
assert single.isValid() and len(single.Solids)==1
assert single.common(Part.makeCylinder(BORE_DIAMETER/2,HEIGHT+.2,v(0,0,-.1))).Volume<1e-6

# Bearing/contact checks at the four original MAIN mounting positions.
placement=json.loads((OUT/'placement.json').read_text(encoding='utf-8'))
main=[i for i in placement['items'] if i['label'].startswith('main_column_')]
assert len(main)==4
floor=Part.read(str(P/'floor_plate.step'))
top=Part.read(str(P/'main_mount_plate.step'))
checks=[]
for item in main:
    xyz=next(op['translate'] for op in item['ops'] if 'translate' in op)
    placed=single.copy();placed.translate(v(*xyz))
    plane=Part.makePlane(20,20,v(xyz[0]-10,xyz[1]-10,xyz[2]))
    area=placed.common(plane).common(floor.common(plane)).Area
    collisions=floor.common(placed).Volume+top.common(placed).Volume
    gap=placed.distToShape(top)[0]
    assert area>.1 and collisions<.001 and gap<.001,(item['label'],area,collisions,gap)
    checks.append(dict(label=item['label'],floor_contact_area_mm2=area,overlap_mm3=collisions,upper_gap_mm=gap))

members=[]
for x,y in [(0,0),(PITCH,0),(0,PITCH),(PITCH,PITCH)]:
    piece=single.copy();piece.translate(v(x,y,0));members.append(piece)
batch=Part.makeCompound(members)
bb=batch.optimalBoundingBox(False,False)
batch.translate(v(-bb.XMin,-bb.YMin,-bb.ZMin))

outputs={}
for stem,shape in [('main_corner_column_polygon',single),('main_corner_column_polygon_4',batch)]:
    shape.exportStep(str(P/(stem+'.step')))
    mesh=MeshPart.meshFromShape(Shape=shape,LinearDeflection=.01,AngularDeflection=.1,Relative=False)
    assert mesh.isSolid()
    mesh.write(str(P/(stem+'.stl')))
    points,faces=mesh.Topology
    (P/(stem+'.scad')).write_text('// Generated variant: spec/build_parent_main_polygon.py.\npolyhedron(points='+json.dumps([[q.x,q.y,q.z] for q in points])+',faces='+json.dumps([list(reversed(f)) for f in faces])+',convexity=10);\n',encoding='utf-8')
    rendered=WORK/(stem+'_scad.stl')
    run=subprocess.run(['C:/Program Files/OpenSCAD/openscad.exe','-o',str(rendered),str(P/(stem+'.scad'))],capture_output=True,text=True,creationflags=0x08000000)
    (WORK/(stem+'_render.log')).write_text(run.stdout+run.stderr,encoding='utf-8')
    assert run.returncode==0 and 'WARNING:' not in run.stderr and 'ERROR:' not in run.stderr
    independent=Mesh.Mesh(str(rendered));assert independent.isSolid()
    expected=shape.optimalBoundingBox(False,False)
    delta=max(abs(getattr(expected,k)-getattr(independent.BoundBox,k)) for k in ['XMin','XMax','YMin','YMax','ZMin','ZMax'])
    assert delta<.01
    outputs[stem]=dict(valid_step=shape.isValid(),solids=len(shape.Solids),closed_stl=True,
                       independent_scad_bbox_difference_mm=delta,
                       size_mm=[expected.XLength,expected.YLength,expected.ZLength])

# The requested standalone job contains precisely four disconnected spacers.
target=JOB/'MAIN_spacers_polygon_4.stl'
target.write_bytes((P/'main_corner_column_polygon_4.stl').read_bytes())
record=dict(status='PASS',height_mm=HEIGHT,outer_sides=OUTER_SIDES,
            outer_envelope_diameter_mm=2*OUTER_RADIUS,bore_sides=BORE_SIDES,
            bore_inscribed_diameter_mm=BORE_DIAMETER,outer_chamfer_mm=EDGE_CHAMFER,
            mouth_chamfer_mm=MOUTH_CHAMFER,quantity=4,spacing_mm=PITCH,
            source='spec/build_parent_main_polygon.py',reference='parts/parent/interior/printed/parent_hand_service/main_corner_column.step',
            reference_sha256=hashlib.sha256((P/'main_corner_column.step').read_bytes()).hexdigest(),
            stl=target.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
            outputs=outputs,mounting_checks=checks,
            print_pose='All flat bottom faces on Z0, bore axes vertical; four separate pieces, no runner.',
            permitted_sharp_edges='The eight longitudinal bore corners retain the requested functional octagonal profile.',
            limitations=['Physical fit/torque/creep not verified.','Existing full twelve-spacer 3MF is the previous circular MAIN variant.'])
(JOB/'manifest.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(WORK/'checks.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('PASS MAIN polygon spacers: four pieces, H',HEIGHT,'hex outside / octagonal bore AF',BORE_DIAMETER,flush=True)
