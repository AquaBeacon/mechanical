import FreeCAD as A,Part,Import,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'assemblies/parent_service_review'
doc=A.newDocument('battery_check');Import.insert(str(O/'parent_service_review.step'),doc.Name)
labels={i['label'] for i in json.loads((O/'placement.json').read_text(encoding='utf-8'))['items']}
s={o.Label:o.Shape for o in doc.Objects if o.Label in labels and hasattr(o,'Shape') and not o.Shape.isNull()}
rows=[]
# Added rigid parts must not intersect the pack, boards, vessel, cover or retaining foam.
for name in ['lipo_tray','lipo_ret_lid']:
 for b in ['p_main','p_pwr','tx_improved','spresense','lipo','box_bcas212310g','pen_tether','pen_td04a','lipo_ret_pads']:
  v=s[name].common(s[b]).Volume if s[name].BoundBox.intersect(s[b].BoundBox) else 0
  rows.append({'part':name,'other':b,'intersection_mm3':round(v,5)})
assert max(r['intersection_mm3'] for r in rows)<.01,rows
# Tool access from the open enclosure. Driver OD8 assumed; screw heads end at Z85.4.
tools=[]
for x,y in [(32,53.5),(111,53.5),(32,98.5),(111,98.5)]:
 v=Part.makeCylinder(4,35,A.Vector(x,y,85.4));bad=[]
 for n,shape in s.items():
  if n.startswith('lipo_ret_bolt_'):continue
  if v.BoundBox.intersect(shape.BoundBox) and v.common(shape).Volume>.01:bad.append(n)
 tools.append({'xy':[x,y],'collisions':bad})
assert all(not t['collisions'] for t in tools),tools
# Swept volume for straight upward removal: lid + top pad first; pack next.
lid=s['lipo_ret_lid'];b=lid.BoundBox
lv=Part.makeBox(b.XLength,b.YLength,b.ZLength+30,A.Vector(b.XMin,b.YMin,b.ZMin))
p=s['lipo'].BoundBox
pv=Part.makeBox(p.XLength,p.YLength,p.ZLength+35,A.Vector(p.XMin,p.YMin,p.ZMin))
removed=['lipo','lipo_ret_lid','lipo_ret_pads']+[n for n in s if n.startswith('lipo_ret_bolt_')]
release=[]
for name,v in [('lid_lift_30mm',lv),('pack_lift_35mm',pv)]:
 bad=[]
 for n,shape in s.items():
  if n in removed:continue
  if v.BoundBox.intersect(shape.BoundBox) and v.common(shape).Volume>.01:bad.append(n)
 # Side/end foam stays on housing during removal; top foam is attached to the removed lid.
 if name.startswith('pack'):
  for i,pad in enumerate(s['lipo_ret_pads'].Solids):
   if pad.BoundBox.ZMin>77:continue
   assert v.common(pad).Volume<.01,('fixed_foam',i)
 release.append({'path':name,'collisions':bad})
assert all(not x['collisions'] for x in release),release
r={'rigid_parts_vs_assembly':rows,'driver_access_d8mm':tools,'upward_removal_paths':release,'thread_intersection_excluded':True,'nominal_pack_only':True}
(O/'battery_retention_checks.json').write_text(json.dumps(r,indent=2));print('PASS: 18 rigid clearance pairs, 4 driver approaches, lid and pack lift paths',flush=True)

