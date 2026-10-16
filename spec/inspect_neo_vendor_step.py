from pathlib import Path
import FreeCAD, Part
p=Path(__file__).resolve().parents[1]/'parts/parent/interior/cots/sparkfun_neo_f9p/ref/NEO-F9P.STEP'
s=Part.read(str(p));print('NEO-F9P',s.BoundBox,'solids',len(s.Solids),flush=True)
s=Part.read(str(p.parents[3]/'printed/ann_mb1_internal_rack/_work/intermediate/rack_unfinished.step'))
print('Unfinished frame',s.isValid(),len(s.Solids),[x.BoundBox for x in s.Solids],flush=True)
