"""Build analytic STEP with the SCAD defaults; verify against rendered STL separately."""
from pathlib import Path
import json
import FreeCAD as A
import Part

p = Path(__file__).resolve().parent
V = A.Vector
original = Part.Shape()
original.read(str(p / 'ref/original_print_orientation.brep'))

def capsule_wire(r, z):
    a = 38.0
    return Part.Wire([
        Part.makeLine(V(r,-a,z),V(r,a,z)),
        Part.Arc(V(r,a,z),V(0,a+r,z),V(-r,a,z)).toShape(),
        Part.makeLine(V(-r,a,z),V(-r,-a,z)),
        Part.Arc(V(-r,-a,z),V(0,-a-r,z),V(r,-a,z)).toShape(),
    ])

grip = Part.makeLoft([capsule_wire(11,0),capsule_wire(12,1)],True,True)
grip = grip.fuse(Part.Face(capsule_wire(12,1)).extrude(V(0,0,14)))
grip = grip.fuse(Part.makeLoft([capsule_wire(12,15),capsule_wire(11,16)],True,True))
sleeve = Part.makeCylinder(14,60.02,V(0,0,15.98))
sleeve = sleeve.cut(Part.makeCylinder(10.2,60.08,V(0,0,15.96)))
sleeve = sleeve.cut(Part.makeBox(14.02,16.4,60.08,V(0,-8.2,15.96)))
added = sleeve.fuse(grip).fuse(Part.makeCylinder(14,16)).removeSplitter()
result = original.fuse(added).removeSplitter()
assert result.isValid() and len(result.Solids)==1
result.exportStep(str(p/'bulkhead_wrench.step'))
# Check the added sleeve never intrudes inside the original radial envelope.
# The 0.05-mm overlap is intentionally restricted to the outside surface.
interior = Part.makeCylinder(10.15,59.9,V(0,0,16.05)).cut(original)
intrusion = added.common(interior).Volume
assert intrusion < 1e-5, intrusion
report={'step_valid':result.isValid(),'solids':len(result.Solids),
        'step_volume_mm3':result.Volume,
        'bounds_mm':[result.BoundBox.XLength,result.BoundBox.YLength,result.BoundBox.ZLength],
        'working_cavity_added_material_mm3':intrusion,
        'original_step_volume_mm3':original.Volume,
        'note':'Geometry validation only. No material test or torque rating.'}
(p/'step_validation.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
