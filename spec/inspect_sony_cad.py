import FreeCAD,Part,MeshPart,json
from pathlib import Path
p=Path('mechanical/parts/parent/interior/cots/spresense_logger/ref')
for n in ['CXD5602PWBEXT1','CXD5602PWBMAIN1']:
 s=Part.read(str(p/(n+'.stp')))
 MeshPart.meshFromShape(Shape=s,LinearDeflection=.15,AngularDeflection=.3,Relative=False).write(str(p/(n+'.stl')))
 print(n)
 for sol in s.Solids:
  b=sol.BoundBox
  if sol.Volume>35: print(round(sol.Volume,1),[round(v,2) for v in [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]])
