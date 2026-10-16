"""Run with FreeCAD bundled Python from workspace root. Exact Sony solids + provisional IMU envelope."""
import FreeCAD as App,Part,MeshPart,Import,json,math,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'assemblies/parent_service_review'
REF=ROOT/'parts/parent/interior/cots/spresense_logger/ref'
STACK=ROOT/'parts/parent/interior/cots/spresense_service_stack';STACK.mkdir(exist_ok=True)
PLATE=ROOT/'parts/parent/interior/printed/parent_plate_service'
def export(s,p):
 s.exportStep(str(p.with_suffix('.step')))
 MeshPart.meshFromShape(Shape=s,LinearDeflection=.12,AngularDeflection=.2,Relative=False).write(str(p.with_suffix('.stl')))
def moved(s,x,y,z):
 s=s.copy();s.translate(App.Vector(x,y,z));return s
ext=Part.read(str(REF/'CXD5602PWBEXT1.stp'))
main=Part.read(str(REF/'CXD5602PWBMAIN1.stp'))
# XY comes directly from matching mount holes (EXT 13.29/29.89, MAIN 2/18.6).
# Main upper PCB face +4.6 relative to EXT upper face: provisional mating placement.
# Normalize EXT underside from -1.6 to 0, preserving every vendor solid.
ext=moved(ext,0,0,1.6);main=moved(main,11.29,0,6.2)
imu=Part.makeBox(20.6,50,9.1,App.Vector(11.29,0,9.9))
# Additional 5mm of stack uncertainty reserved, not presented as actual board geometry.
uncertain=Part.makeBox(20.6,50,5,App.Vector(11.29,0,19.0))
stack=Part.makeCompound([ext,main,imu]);export(stack,STACK/'spresense_service_stack')
export(imu,STACK/'imu_nominal_envelope')
# A native solid equivalent of the SCAD plate (same polygon, boss positions and compensated bores).
holes=json.loads((OUT/'hole_sources.json').read_text())['holes_plate_mm']
pts=[[8,0],[175,0],[183,8],[183,195],[175,203],[8,203],[0,195],[0,8]]
wire=Part.makePolygon([App.Vector(x,y,0) for x,y in pts+[pts[0]]]);plate=Part.Face(wire).extrude(App.Vector(0,0,5))
for k,coords in holes.items():
 for x,y in coords: plate=plate.fuse(Part.makeCylinder(3.5,9.5 if k=='PWR' else 6,App.Vector(x,y,5)))
for x,y in [[51.5,11.5],[91.5,11.5]]:plate=plate.fuse(Part.makeCylinder(1.6,6.2,App.Vector(x,y,-6)))
# Polygon holes match the SCAD circumscribed 12-gon.
def bore(x,y,d,h):
 r=d/2/math.cos(math.pi/12)
 ps=[App.Vector(x+r*math.cos(i*math.pi/6),y+r*math.sin(i*math.pi/6),-.1) for i in range(12)]
 return Part.Face(Part.makePolygon(ps+[ps[0]])).extrude(App.Vector(0,0,h))
for k,coords in holes.items():
 for x,y in coords:plate=plate.cut(bore(x,y,2.6,14.7 if k=='PWR' else 11.2))
for x,y in [[11.5,11.5],[171.5,11.5]]:
 plate=plate.cut(bore(x,y,4.5,5.2)).cut(Part.makeCone(2.25,4.5,2.65,App.Vector(x,y,2.45)))
for x,y in [[116.5,70],[176,110],[176,160]]:plate=plate.cut(Part.makeBox(3,10,5.2,App.Vector(x-1.5,y-5,-.1)))
plate=plate.removeSplitter();assert plate.isValid() and len(plate.Solids)==1
plate.exportStep(str(PLATE/'parent_plate_service.step'))
asm=json.loads((OUT/'placement.json').read_text(encoding='utf-8'))
def transform(s,ops):
 for op in reversed(ops):
  if 'translate' in op:s.translate(App.Vector(*op['translate']))
  if 'rotate' in op:
   for axis,ang in zip([App.Vector(1,0,0),App.Vector(0,1,0),App.Vector(0,0,1)],op['rotate']):s.rotate(App.Vector(0,0,0),axis,ang)
 return s
shapes={}
doc=App.newDocument('parent_service_review')
for it in asm['items']:
 name=it.get('file',Path(it['part']).name);s=Part.read(str(ROOT/it['part']/(name+'.step')))
 s=transform(s,it['ops']);shapes[it['label']]=s
 ob=doc.addObject('PartDesign::Feature',it['label']);ob.Label=it['label'];ob.Shape=s
Import.export(doc.Objects,str(OUT/'parent_service_review.step'))
# Service swept volumes include plug body + cable turn-up allowance, card extraction + fingers.
# USB mouth coordinate of PICO1 derives from footprint offset and actual KiCad Pico STEP end (26.8).
pico_mouth=128.5-84.6+24.13-26.8
ports=[
 dict(name='P_MAIN_USB',x=36.61,y=pico_mouth,z=29.4,direction=-1,w=14,l=30,h=8),
 dict(name='P_MAIN_SD',x=59.5,y=128.5-79-6.7,z=27.3,direction=-1,w=20,l=25,h=1),
 dict(name='SONY_MAIN_USB',x=134.5+11.29+9,y=41-1.6,z=27.9,direction=-1,w=14,l=30,h=8),
 dict(name='SONY_EXT_USB',x=134.5+44.6,y=41+.94,z=23.3,direction=-1,w=14,l=30,h=8),
 dict(name='SONY_SD',x=134.5+37.18,y=41+73.28,z=27.2,direction=1,w=22,l=25,h=1)
]
results=[];sv=[]
for p in ports:
 is_usb='USB' in p['name']
 setback=3 if is_usb else .2
 y=p['y']+setback if p['direction']==1 else p['y']-p['l']
 v=Part.makeBox(p['w'] if is_usb else 12,p['l']-setback,p['h'],App.Vector(p['x']-(p['w'] if is_usb else 12)/2,y,p['z']-p['h']/2))
 # USB mating tip is intentionally inside the receptacle; moulded body starts 3mm outside.
 # Fingers approach vertically outside the PCB, above the socket; card itself travels at slot height.
 fy=p['y']+3 if p['direction']==1 else p['y']-13
 fz=p['z']+(p['h']/2 if is_usb else 1.5)
 finger=Part.makeBox(p['w'],10,91-fz,App.Vector(p['x']-p['w']/2,fy,fz))
 v=v.fuse(finger);sv.append(v)
 collisions=[]
 for label,s in shapes.items():
  if label in ['plate','main_spacer_0','main_spacer_1','main_spacer_2','main_spacer_3']:continue
  if s.BoundBox.intersect(v.BoundBox):
   vol=s.common(v).Volume
   if vol>.1:collisions.append({'part':label,'volume_mm3':round(vol,3)})
 results.append(dict(port=p['name'],mouth_mm=[p['x'],p['y'],p['z']],reserved_width_mm=p['w'],reserved_length_mm=p['l'],collisions=collisions))
 print(p['name'],collisions,flush=True)
export(Part.makeCompound(sv),OUT/'service_volumes')
# B-Rep checks between moved electronics and enclosure: exact booleans, excluding intended connector mating.
pairs=[('spresense','box_bcas212310g'),('spresense','plate'),('p_pwr','box_bcas212310g'),('tx_improved','box_bcas212310g'),('lipo_tray','pen_tether'),('lipo_tray','pen_td04a')]
mechanical=[]
for a,b in pairs:
 vol=shapes[a].common(shapes[b]).Volume
 mechanical.append({'a':a,'b':b,'intersection_mm3':round(vol,4)})
 print(a,b,vol,flush=True)
report={'status':'REVIEW_PENDING_IMU_STACK_AND_CABLE_CONFIRMATION','ports':results,'mechanical_pairs':mechanical,'imu_source':'Sony product specification 50 x 20.6 x 9.1mm; detailed CAD not published in retrieved official design repository','stack_main_upper_face_mm':6.2,'stack_uncertainty_extra_mm':5,'lid_open_required':True}
(OUT/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
manifest=[]
for f in REF.iterdir():
 if f.suffix in ['.stp','.png','.html']:manifest.append({'file':f.name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
(STACK/'sources.json').write_text(json.dumps({'retrieved':'2026-09-26','urls':['https://github.com/sonydevworld/spresense-hw-design-files','https://developer.spresense.sony-semicon.com/ja/buy-spresense/spresense-imu-add-on-board/'],'files':manifest,'main_xy_translation':[11.29,0],'main_z_provisional':6.2,'imu_is_envelope':True},indent=2),encoding='utf-8')
print('DONE',flush=True)

