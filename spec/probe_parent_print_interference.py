"""Diagnostic exact floor/case intersections, retained in assembly work logs."""
from parent_access_common import *
d,c=load();overlap=c['plate'].common(c['box_bcas212310g'])
for s in overlap.Solids:print(s.Volume,str(s.BoundBox),flush=True)
overlap.exportStep(str(O/'_work/intermediate/print_floor_case_overlap.step'))
