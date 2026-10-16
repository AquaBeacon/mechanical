from pathlib import Path
import Part,FreeCAD,json
O=Path('C:/Users/ryupc/WorkSpace/Mitou26/AquaBeacon-OSS/mechanical/assemblies/child_petg100_design')
c=Part.Shape();c.read(str(O/'cad/child_core_frame.step'));g=Part.Shape();g.read(str(O/'cad/child_jaw_gate.step'))
v=Part.makeCylinder(57.15,216,FreeCAD.Vector(0,0,-8)).fuse(Part.makeCylinder(60.15,5.8,FreeCAD.Vector(0,0,-13.8))).fuse(Part.makeCylinder(60.15,6.5,FreeCAD.Vector(0,0,208)))
out=[]
for a in range(91):
 s=g.copy();s.rotate(FreeCAD.Vector(-72,10,0),FreeCAD.Vector(0,0,1),a)
 rec=dict(angle_deg=a,core_overlap_mm3=s.common(c).Volume,vessel_overlap_mm3=s.common(v).Volume)
 out.append(rec);print(rec,flush=True)
(O/'gate_opening_exact.json').write_text(json.dumps(out,indent=2))
