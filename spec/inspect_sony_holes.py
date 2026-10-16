import FreeCAD,Part
from pathlib import Path
p=Path('mechanical/parts/parent/interior/cots/spresense_logger/ref')
for n in ['CXD5602PWBEXT1','CXD5602PWBMAIN1']:
 s=Part.read(str(p/(n+'.stp'))); pcb=max(s.Solids,key=lambda x:x.Volume)
 print(n)
 for f in pcb.Faces:
  if isinstance(f.Surface,Part.Cylinder): print('cyl',f.Surface.Center,f.Surface.Radius)
