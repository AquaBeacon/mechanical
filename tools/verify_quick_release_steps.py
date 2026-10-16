"""FreeCAD CLI: validate each trial STEP against STL in the same coordinates."""
from pathlib import Path
import json
import Mesh
import Part

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT / "parts/common/jigs/quick_release_prototypes"
ASM = ROOT / "assemblies/quick_release_trials"
results = []
for stl in sorted(PART.glob("quick_release_prototypes_*.stl")):
    step = stl.with_suffix(".step")
    shape = Part.read(str(step))
    mesh = Mesh.Mesh(str(stl))
    a, b = shape.BoundBox, mesh.BoundBox
    delta = max(abs(getattr(a,k)-getattr(b,k)) for k in ["XMin","YMin","ZMin","XMax","YMax","ZMax"])
    volume_error = abs(shape.Volume-mesh.Volume)/mesh.Volume
    assert shape.isValid() and len(shape.Solids)==1 and shape.Volume>0, str(step)
    assert delta<0.06 and volume_error<0.002, str(step)
    results.append({"file":step.name,"valid":True,"solids":len(shape.Solids),
                    "bbox_max_difference_mm":delta,"relative_volume_difference":volume_error})
    print("PASS STEP",step.name,flush=True)
(ASM / "_work/analysis/step_verification.json").write_text(json.dumps(results,indent=2)+"\n",encoding="utf-8")
