# csg_to_step.py - convert an OpenSCAD .csg into a STEP solid via FreeCAD.
# Paths are passed via environment variables to avoid freecadcmd treating them
# as documents to open:
#   CSG_IN   = input .csg
#   STEP_OUT = output .step
#   OPENSCAD = path to openscad.exe (so FreeCAD can resolve hull/offset nodes)
#   STL_REF  = (optional) the STL OpenSCAD wrote from the same .scad. The STEP is
#              compared against it (bbox + volume) and NOT written if they differ,
#              so build.ps1 falls back to the faceted STL->STEP path instead of
#              silently keeping a wrong solid. hull()/teardrop parts came out as
#              garbage (child_lcd_support: 103 mm^3 vs 1653) before this check.
# Run: OPENSCAD=... CSG_IN=... STEP_OUT=... freecadcmd csg_to_step.py
import os, sys
import FreeCAD, Part

def log(*a):
    print("[csg2step]", *a); sys.stdout.flush()

src = os.environ["CSG_IN"]
dst = os.environ["STEP_OUT"]
oscad = os.environ.get("OPENSCAD")
ref = os.environ.get("STL_REF")

# tell FreeCAD's OpenSCAD importer where openscad.exe is
if oscad:
    p = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/OpenSCAD")
    p.SetString("openscadexecutable", oscad)

import importCSG
importCSG.open(src)
doc = FreeCAD.ActiveDocument
log("doc objects:", len(doc.Objects))

referenced = set()
for o in doc.Objects:
    for child in getattr(o, "OutList", []):
        referenced.add(child.Name)

def solid(o):
    s = getattr(o, "Shape", None)
    return s is not None and not s.isNull() and s.Volume > 1e-6

tops = [o for o in doc.Objects if solid(o) and o.Name not in referenced]
if not tops:
    tops = [o for o in doc.Objects if solid(o)]
log("tops:", [(o.Name, round(o.Shape.Volume, 1)) for o in tops])

if not tops:
    log("ERROR: no solids")
    sys.exit(1)

shape = tops[0].Shape
for o in tops[1:]:
    shape = shape.fuse(o.Shape)
shape = shape.removeSplitter()

if ref and os.path.exists(ref):
    import Mesh
    m = Mesh.Mesh(ref)
    bs, bm = shape.BoundBox, m.BoundBox
    dbox = max(abs(a - b) for a, b in ((bs.XMin, bm.XMin), (bs.YMin, bm.YMin), (bs.ZMin, bm.ZMin),
                                       (bs.XMax, bm.XMax), (bs.YMax, bm.YMax), (bs.ZMax, bm.ZMax)))
    dvol = abs(shape.Volume - m.Volume) / max(m.Volume, 1e-9)
    log("check vs STL: bbox maxdiff=%.2f mm  volume step=%.1f stl=%.1f (%.1f%%)"
        % (dbox, shape.Volume, m.Volume, dvol * 100))
    if dbox > 0.5 or dvol > 0.02:
        log("ERROR: CSG->STEP result does not match the STL (hull/offset/teardrop node lost?). "
            "Not writing STEP; build.ps1 will fall back to STL->STEP.")
        sys.exit(1)

obj = doc.addObject("Part::Feature", "Result")
obj.Shape = shape
doc.recompute()
Part.export([obj], dst)
log("wrote", dst, "volume=", round(shape.Volume, 1),
    "solids=", len(shape.Solids), "faces=", len(shape.Faces))
