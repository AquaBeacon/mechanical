"""Actual upper adapter + four columns, ideal bonded reference only.

This is a solver input, not a printable replacement or joint qualification.
"""
import FreeCAD as A, Part, MeshPart
from pathlib import Path
import json,sys,hashlib
R=Path(__file__).resolve().parents[1];out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
d=json.loads((R/'assemblies/parent_hand_service/placement.json').read_text(encoding='utf-8'))
shapes=[];sources={}
for it in d['items']:
 if it['label']!='sony_upper_carrier' and not it['label'].startswith('sony_column_'):continue
 p=R/it['part']/(it['file']+'.step');s=Part.read(str(p));sources[p.relative_to(R).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
 for op in reversed(it['ops']):
  if 'translate' in op:s.translate(A.Vector(*op['translate']))
  else:raise ValueError('Unexpected column rotation; update analysis transform')
 shapes.append(s)
assert len(shapes)==5
s=shapes[0].multiFuse(shapes[1:]).removeSplitter();assert s.isValid() and len(s.Solids)==1,(s.isValid(),len(s.Solids))
s.exportStep(str(out/'sony_carrier.step'))
MeshPart.meshFromShape(Shape=s,LinearDeflection=.025,AngularDeflection=.1,Relative=False).write(str(out/'sony_carrier.stl'))
(out/'stack_source_hashes.json').write_text(json.dumps(dict(sources=sources,assumption='Ideal bonded contact at actual seats. Steel bolts, preload, slip, printed creep and case/PCB flexibility excluded.'),indent=2),encoding='utf-8')
print('ideal stack',s.Volume,flush=True)
