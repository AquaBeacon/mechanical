"""Re-tessellate unchanged STEP siblings after folder-wide source invalidation."""
from pathlib import Path
import Part
R=Path(__file__).resolve().parents[1]
def build(doc,parameters):
    out=[]
    for name,path in parameters.items():
        obj=doc.addObject('Part::Feature',name)
        obj.Shape=Part.read(str(R/path)).cleaned();out.append(obj)
    return out
