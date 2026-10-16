from pathlib import Path
import json,zipfile
root=Path('mechanical');out=root/'assemblies/parent_service_review'
r=json.loads((out/'verification.json').read_text(encoding='utf-8'))
assert all(not p['collisions'] for p in r['ports'])
assert all(p['intersection_mm3']<.1 for p in r['mechanical_pairs'])
assert all(p['intersection_mm3']<.1 for p in json.loads((out/'electronics_pairs.json').read_text()))
plate=root/'parts/parent/interior/printed/parent_plate_service/parent_plate_service.scad'
s=plate.read_text(encoding='utf-8')
for a,b in [('(',')'),('[',']'),('{','}')]:assert s.count(a)==s.count(b)
# Publish CAD + preview + evidence together; vendor originals remain distinguishable.
files=[f for f in out.iterdir() if f.suffix in ['.step','.png','.json','.md']]
files += list((root/'parts/parent/interior/printed/parent_plate_service').iterdir())
files += list((root/'parts/parent/interior/printed/parent_lipo_retainer').iterdir())
files += [f for f in (root/'parts/parent/interior/cots/spresense_service_stack').iterdir() if f.suffix in ['.json','.md']]
ref=root/'parts/parent/interior/cots/spresense_logger/ref'
files += [f for f in ref.iterdir() if f.suffix in ['.stp','.html']]
with zipfile.ZipFile(out/'parent_service_review.zip','w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for f in files:
  if f.is_file():z.write(f,str(f.relative_to(root)))
print('PASS 5 service paths; 21 electronics/enclosure pairs; 6 critical pairs; balanced SCAD')
print('ZIP bytes',(out/'parent_service_review.zip').stat().st_size)

