from pathlib import Path
import sys
import FreeCAD as A,Part
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'scad/lib'))
from cad_edge_finish import sharp_edges
s=Part.read(str(R/'parts/parent/interior/printed/parent_hand_service/_work/intermediate/floor_plate_unfinished.step'))
for i,e in enumerate(sharp_edges(s)):
 try:
  t=s.makeChamfer(.05,[e])
  if not t.isValid():print('INVALID',i,e.BoundBox,flush=True)
 except Part.OCCError:print('FAIL',i,e.BoundBox,flush=True)
