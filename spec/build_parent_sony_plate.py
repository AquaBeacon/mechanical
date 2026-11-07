"""Build only the existing Sony plate, using its shared canonical generator."""
from pathlib import Path
import sys

def build(doc, parameters):
    root=Path(__file__).resolve().parents[1]
    sys.path.insert(0,str(root/'scad/lib'))
    import parent_gnss as G
    from parent_corner_mounts import sony_holes,sony_shapes
    holes=sony_holes(G)
    obj=doc.addObject('Part::Feature','sony_mount_plate')
    obj.Shape=sony_shapes(holes,G)['sony_mount_plate']
    return [obj]
