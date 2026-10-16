import FreeCAD as App,Import,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assemblies/parent_service_review'
doc=App.newDocument('verify_service_pairs');Import.insert(str(OUT/'parent_service_review.step'),doc.Name)
s={o.Label:o.Shape for o in doc.Objects if hasattr(o,'Shape') and not o.Shape.isNull()}
names=['p_main','p_pwr','tx_improved','spresense','lipo_tray','lipo','box_bcas212310g']
rows=[]
for i,a in enumerate(names):
 for b in names[i+1:]:
  vol=s[a].common(s[b]).Volume if s[a].BoundBox.intersect(s[b].BoundBox) else 0
  rows.append({'a':a,'b':b,'intersection_mm3':round(vol,4)})
  print(a,b,round(vol,4),flush=True)
(OUT/'electronics_pairs.json').write_text(json.dumps(rows,indent=2))
assert all(r['intersection_mm3']<.1 for r in rows), 'Electronic enclosure intersection'
print('PASS',flush=True)
