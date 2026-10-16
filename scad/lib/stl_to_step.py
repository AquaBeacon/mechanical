"""Convert a verified STL mesh to a faceted STEP fallback.

Used when FreeCAD's OpenSCAD CSG importer cannot rebuild a 2D hull because its
optional DXF Python module is unavailable. Environment: STL_IN, STEP_OUT.
"""

import os

import FreeCAD as App
import Mesh
import Part


src = os.environ["STL_IN"]
dst = os.environ["STEP_OUT"]

mesh = Mesh.Mesh(src)
shape = Part.Shape()
shape.makeShapeFromMesh(mesh.Topology, float(os.environ.get('STL_MESH_TOLERANCE', '0.05')))

# Make the outer shell and inward-facing cavity shells one solid. Making each
# shell a separate solid would turn a topology-optimised internal void into
# positive material in STEP (Part.makeSolid normalises individual orientations).
try:
    candidate = Part.makeSolid(shape)
except Exception:
    candidate = None
if candidate is not None and candidate.isValid():
    result = candidate
else:
    # Disconnected physical parts remain a compound, as in the original path.
    solids = []
    for shell in shape.Shells:
        try:
            solids.append(Part.makeSolid(shell))
        except Exception:
            pass
    result = Part.makeCompound(solids) if solids else shape

expected_volume = abs(mesh.Volume)
volume_error = abs(abs(result.Volume) - expected_volume) / max(expected_volume, 1e-12)
if not result.isValid() or volume_error > 0.0025:
    raise RuntimeError(f"Faceted STEP changes STL volume or is invalid: relative error={volume_error:g}")
doc = App.newDocument("STL_to_STEP")
obj = doc.addObject("Part::Feature", "Body")
obj.Shape = result
doc.recompute()
Part.export([obj], dst)
print(f"[stl2step] wrote {dst} solids={len(result.Solids)} shells={len(result.Shells)} faces={len(result.Faces)} volume_error={volume_error:g}")
