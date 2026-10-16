from pathlib import Path
import Part,FreeCAD,MeshPart
O=Path('C:/Users/ryupc/WorkSpace/Mitou26/AquaBeacon-OSS/mechanical/assemblies/child_petg100_design')
p=O/'cad/child_core_frame.step';s=Part.Shape();s.read(str(p))
box=Part.makeBox(22,12,240,FreeCAD.Vector(-83,10,-18))
pin=Part.makeCylinder(9,242,FreeCAD.Vector(-72,10,-19))
s=s.cut(box.cut(pin)).removeSplitter();assert s.isValid() and len(s.Solids)==1
s.exportStep(str(p));MeshPart.meshFromShape(Shape=s,LinearDeflection=.12,AngularDeflection=.15,Relative=False).write(str(O/'cad/child_core_frame_print.stl'))
print('hinge corrected',s.Volume)
