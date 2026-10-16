"""Read-only OCC edge-finishing diagnosis for the sensor-frame revision."""
import FreeCAD as A,Part,sys,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'scad/lib'))
from cad_edge_finish import sharp_edges
s=Part.read(str(R/'parts/parent/interior/printed/ann_mb1_internal_rack/_work/intermediate/rack_unfinished.step'))
edges=sharp_edges(s);fails=[]
for i,e in enumerate(edges):
    try:
        t=s.makeChamfer(.025,[e]);ok=t.isValid() and len(t.Solids)==1
    except Part.OCCError:ok=False
    if not ok:fails.append(dict(index=i,length=e.Length,bounds=str(e.BoundBox)))
print(json.dumps(fails,indent=2),flush=True)
(R/'assemblies/parent_hand_service/_work/analysis/lis3mdl_revision_20261009/edge_failures.json').write_text(json.dumps(fails,indent=2))
for key in ['XMin','XMax','YMin','YMax','ZMin','ZMax']:
 print(key,getattr(s.BoundBox,key))
