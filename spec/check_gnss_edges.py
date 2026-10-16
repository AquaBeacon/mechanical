import FreeCAD as A, Part
from pathlib import Path
R=Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0,str(R/'scad/lib'))
from cad_edge_finish import sharp_edges
s=Part.read(str(R/'parts/parent/interior/printed/ann_mb1_internal_rack/_work/intermediate/rack_unfinished.step'))
for i,e in enumerate(s.Edges):
 if not any(e.isSame(ee) for ee in sharp_edges(s)):continue
 try:
  t=s.makeChamfer(.1,[e])
 except Exception:print('FAIL',i,e.BoundBox,flush=True)
