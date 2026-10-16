"""FreeCAD CLI: merge coplanar triangles for analysis, preserve print geometry."""
from pathlib import Path
import json
import os
import Part
import Mesh

part = Path(os.environ["ASM_ROOT"]) / "parts/child/exterior/printed/child_wte4_suspension_clamp"
work = Path(os.environ.get("CLAMP_ANALYSIS_WORK", str(part / "_work/analysis/surface_remesh")))
if os.environ.get("CLAMP_ANALYSIS_STL"):
    mesh = Mesh.Mesh(os.environ["CLAMP_ANALYSIS_STL"])
    shell = Part.Shape()
    shell.makeShapeFromMesh(mesh.Topology, 0.0001)
    src = Part.makeSolid(Part.Shell(shell.Faces))
else:
    src = Part.read(str(part / "child_wte4_suspension_clamp_half.step"))
shape = src.removeSplitter()
result = dict(valid=shape.isValid(), solids=len(shape.Solids),
              input_faces=len(src.Faces), output_faces=len(shape.Faces),
              volume_relative_error=abs(shape.Volume/src.Volume-1))
assert result["valid"] and result["solids"] == 1 and result["volume_relative_error"] < 1e-6
shape.exportStep(str(work / "refined.step"))
(work / "step_refinement.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
print(json.dumps(result))
