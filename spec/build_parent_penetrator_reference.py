"""Import vendor COTS models with one shared local datum; no printable parts."""
from pathlib import Path
import sys


def build(doc,parameters):
    root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'scad/lib'))
    from parent_penetrator_access import vendor_shapes
    result=[]
    for name,shape in vendor_shapes(root).items():
        assert shape.isValid() and len(shape.Solids)>0,name
        obj=doc.addObject('Part::Feature',name);obj.Shape=shape;result.append(obj)
    return result
