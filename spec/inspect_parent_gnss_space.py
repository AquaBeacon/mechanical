import FreeCAD as A, Part
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
a=json.loads((R/'assemblies/parent_hand_service/placement.json').read_text(encoding='utf-8'))
for it in a['items']:
 if it['label'] not in ['p_pwr','tx_improved','p_main','lift_carrier','plate','spresense']:continue
 s=Part.read(str(R/it['part']/(it.get('file',Path(it['part']).name)+'.step')))
 for op in reversed(it['ops']):
  if 'rotate' in op:
   for axis,ang in zip([A.Vector(1,0,0),A.Vector(0,1,0),A.Vector(0,0,1)],op['rotate']):s.rotate(A.Vector(),axis,ang)
  if 'translate' in op:s.translate(A.Vector(*op['translate']))
 print(it['label'],s.BoundBox,flush=True)
