from pathlib import Path
import Part,FreeCAD,MeshPart
O=Path('C:/Users/ryupc/WorkSpace/Mitou26/AquaBeacon-OSS/mechanical/assemblies/child_petg100_design')
p=O/'cad/child_jaw_gate.step';s=Part.Shape();s.read(str(p))
for a in range(0,91,5):
 for r,z,h in [(57.65,-8,216),(60.65,-13.8,5.8),(60.65,208,6.5)]:
  v=Part.makeCylinder(r,h,FreeCAD.Vector(0,0,z));v.rotate(FreeCAD.Vector(-72,10,0),FreeCAD.Vector(0,0,1),-a);s=s.cut(v)
s=s.removeSplitter();assert s.isValid() and len(s.Solids)==1
s.exportStep(str(p));MeshPart.meshFromShape(Shape=s,LinearDeflection=.12,AngularDeflection=.15,Relative=False).write(str(O/'cad/child_jaw_gate_print.stl'))
print('sweep corrected',s.Volume)
