"""Read official STEP in FreeCAD CLI and record thin-panel layout candidates.

Uses existing BODY_MODELS_REF_INPUT/BODY_MODELS_REF_OUTPUT environment variables.
The derived reference mesh is a study artifact, never a child manufacturing part.
"""
from pathlib import Path
import json
import os
import Part
import MeshPart

source = Path(os.environ['BODY_MODELS_REF_INPUT'])
out = Path(os.environ['BODY_MODELS_REF_OUTPUT'])
out.mkdir(parents=True, exist_ok=True)
shape = Part.Shape()
shape.read(str(source))
box = shape.BoundBox
panels = []
records = []
for number, solid in enumerate(shape.Solids):
    bound = solid.BoundBox
    dimensions = [bound.XLength,bound.YLength,bound.ZLength]
    smallest, middle, largest = sorted(dimensions)
    if 4 <= smallest <= 20 and middle >= 100 and largest >= 200:
        panels.append(solid)
        records.append({'solid_index':number,'dimensions_mm':dimensions,
                        'center_mm':[bound.Center.x,bound.Center.y,bound.Center.z],
                        'volume_mm3':solid.Volume})
report = {'source':source.name,'solids':len(shape.Solids),
          'assembly_dimensions_mm':[box.XLength,box.YLength,box.ZLength],
          'thin_panel_candidates':records,
          'note':'Candidates selected by bounding dimensions, not semantic CAD names. Official geometry unchanged. Frame and mounts in child design are independent.'}
(out/'cad_review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
if panels:
    reference = Part.makeCompound(panels)
    mesh = MeshPart.meshFromShape(Shape=reference,LinearDeflection=1.0,AngularDeflection=0.4,Relative=False)
    mesh.write(str(out/'official_thin_panels.stl'))
print('OFFICIAL_REFERENCE_REVIEW_COMPLETE',json.dumps(report))
