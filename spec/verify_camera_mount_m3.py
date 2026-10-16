"""Independent STEP checks for the one-piece direct rear M3 revision."""
import FreeCAD as A,Part,os,json
from pathlib import Path
ROOT=Path(os.environ['CAMERA_M3_ROOT']);OUT=ROOT/'parts/child/exterior/printed/dji_osmo_action6_mount_m3'
mount=Part.read(str(OUT/'camera_mount.step'))
assert mount.isValid() and len(mount.Solids)==1,'Invalid STEP'
result={'revision':'direct_rear_M3_15pct','valid':True,'solids':1,'volume_mm3':mount.Volume}
mount.translate(A.Vector(0,113.45,60))
frame=Part.read(str(ROOT/'parts/child/exterior/printed/child_simple_front/child_simple_front.step'))
result['mount_frame_intersection_mm3']=mount.common(frame).Volume
assert result['mount_frame_intersection_mm3']<0.01,result
checks=[]
for x in [-20,20]:
 for z in [80,120]:
  bore=Part.makeCylinder(3.45/2,16,A.Vector(x,74,z),A.Vector(0,1,0))
  assert bore.common(mount).Volume<0.01 and bore.common(frame).Volume<0.01,('M3',x,z,bore.common(mount).Volume,bore.common(frame).Volume)
  head=Part.makeCylinder(5.5/2,3,A.Vector(x,86.4,z),A.Vector(0,1,0))
  assert head.common(mount).Volume<0.01,('head',x,z)
  tool=Part.makeCylinder(1.5,100,A.Vector(x,89.4,z),A.Vector(0,1,0))
  assert tool.common(mount).Volume<0.01,('front tool',x,z,tool.common(mount).Volume)
  nut_tool=Part.makeCylinder(5,10,A.Vector(x,64,z),A.Vector(0,1,0))
  assert nut_tool.common(frame).Volume<0.01 and nut_tool.common(mount).Volume<0.01,('nut tool',x,z)
  checks.append([x,82,z])
result['M3_hole_centers']=checks
result['hardware']='M3 socket heads D5.5 x 3 recessed 0.6 mm; straight D3 driver shaft; D10 rear tool clearance. Install before camera.'
result['strength']='Not analysed; infill 15 percent is a print setting, not a strength certification.'
mount.exportStep(str(OUT/'assembly.step'))
(OUT/'cad_checks.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
