from pathlib import Path
import FreeCAD as A, Part
R=Path(__file__).resolve().parents[1]
case=Part.read(str(R/'parts/parent/exterior/cots/bcas212310g/bcas212310g.step'))
for xyz in [[145,143,43.4],[142.5,130,43.4],[142.5,128,43.4],[143,130,45]]:
 p=Part.makeBox(60,80,1.6,A.Vector(*xyz));c=p.common(case)
 print(xyz,c.Volume,c.BoundBox,flush=True)
for y in [209,210,211]:
 p=Part.makeBox(60,3.5,5,A.Vector(142.5,y,40.4));c=p.common(case);print('rear beam',y,c.Volume,c.BoundBox,flush=True)
