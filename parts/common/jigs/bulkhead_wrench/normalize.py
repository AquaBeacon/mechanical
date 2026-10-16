import FreeCAD as A, Part, MeshPart
from pathlib import Path
p=Path('parts/common/jigs/bulkhead_wrench').resolve()
s=Part.read(str(p/'ref/original.step'))
m=A.Matrix(); m.A11=0;m.A12=1;m.A13=0;m.A21=0;m.A22=0;m.A23=-1;m.A31=-1;m.A32=0;m.A33=0;m.A34=76
s.transformShape(m)
MeshPart.meshFromShape(Shape=s,LinearDeflection=0.03,AngularDeflection=0.08,Relative=False).write(str(p/'ref/original_print_orientation.stl'))
s.exportBrep(str(p/'ref/original_print_orientation.brep'))
print(s.BoundBox)
