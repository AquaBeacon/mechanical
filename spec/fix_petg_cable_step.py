from pathlib import Path
import Part,FreeCAD,MeshPart
O=Path('C:/Users/ryupc/WorkSpace/Mitou26/AquaBeacon-OSS/mechanical/assemblies/child_petg100_design')
pts=[[-18,-92,202],[0,-85,210],[0,-85,224]]
p=O/'cad/child_core_frame.step';s=Part.Shape();s.read(str(p))
for a,b in zip(pts,pts[1:]):
 a=FreeCAD.Vector(*a);b=FreeCAD.Vector(*b);v=b-a
 for cut in [Part.makeCylinder(4.15,v.Length,a,v),Part.makeSphere(4.15,a),Part.makeSphere(4.15,b)]:s=s.cut(cut)
s=s.removeSplitter();assert s.isValid() and len(s.Solids)==1
s.exportStep(str(p));MeshPart.meshFromShape(Shape=s,LinearDeflection=.12,AngularDeflection=.15,Relative=False).write(str(O/'cad/child_core_frame_print.stl'))
print('cable corrected',s.Volume)
