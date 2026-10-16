"""Locate exact floor/case BRep overlap; diagnostic files stay with the assembly."""
import FreeCAD as A, Part
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];O=R/'assemblies/parent_hand_service/_work/analysis/access_revision_20261008'
a=Part.read(str(R/'parts/parent/interior/printed/parent_hand_service/floor_plate.step'))
b=Part.read(str(R/'parts/parent/exterior/cots/bcas212310g/bcas212310g.step'))
c=a.common(b);c.exportStep(str(O/'floor_case_overlap.step'))
rows=[]
for s in c.Solids:
    t=s.BoundBox;rows.append(dict(volume=s.Volume,bbox=[t.XMin,t.YMin,t.ZMin,t.XMax,t.YMax,t.ZMax]))
print(json.dumps(rows,indent=2))
