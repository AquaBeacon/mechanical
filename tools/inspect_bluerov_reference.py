"""Read official BlueROV CAD in FreeCAD CLI; write a coarse reference mesh.

Uses BODY_MODELS_REF_INPUT and BODY_MODELS_REF_OUTPUT for CLI file paths.
The downloaded manufacturer's originals stay in the assembly ref/ folder.
"""
import os
import json
from pathlib import Path
import Part
import MeshPart

source = Path(os.environ['BODY_MODELS_REF_INPUT'])
out = Path(os.environ['BODY_MODELS_REF_OUTPUT'])
shape = Part.Shape()
shape.read(str(source))
box = shape.BoundBox
report = dict(source=source.name, solids=len(shape.Solids), faces=len(shape.Faces),
              bounds_mm=[[box.XMin,box.YMin,box.ZMin],[box.XMax,box.YMax,box.ZMax]],
              dimensions_mm=[box.XLength,box.YLength,box.ZLength],
              note='Manufacturer assembly read for layout reference; no product geometry copied into child design.')
out.mkdir(parents=True,exist_ok=True)
(out/'bluerov_cad_summary.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
mesh = MeshPart.meshFromShape(Shape=shape, LinearDeflection=2.0, AngularDeflection=0.6, Relative=False)
mesh.write(str(out/'bluerov_reference.stl'))
print('BLUEROV_CAD_REVIEW',json.dumps(report))
