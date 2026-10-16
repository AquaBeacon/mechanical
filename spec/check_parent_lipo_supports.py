import FreeCAD as A,Part,json
from pathlib import Path
R=Path('mechanical');P=R/'parts/parent/interior/printed/parent_lipo_retainer'
base=Part.read(str(P/'parent_lipo_retainer_base.step'));lid=Part.read(str(P/'parent_lipo_retainer_lid.step'))
nut=Part.read(str(R/'parts/common/interior/cots/screw/screw_nut_m3.step'))
sp=Part.read(str(R/'parts/common/interior/cots/hex_spacer/hex_spacer_m3_mf25.step'))
result=[]
for x,y in [(12,5),(91,5),(12,50),(91,50)]:
 n=nut.copy();n.translate(A.Vector(x,y,21.6));v=base.common(n).Volume;d=base.distToShape(n)[0]
 assert v<.01 and d<.001,(x,y,v,d)
 result.append({'support':'nut_roof','xy':[x,y],'intersection_mm3':v,'distance_mm':d})
for x,y in [(0,0),(103,0),(0,75.5),(103,75.5)]:
 n=sp.copy();n.translate(A.Vector(x,y,-25));d=base.distToShape(n)[0]
 assert d<.001,(x,y,d)
 result.append({'support':'MAIN_spacer','xy':[x,y],'distance_mm':d})
(P/'support_checks.json').write_text(json.dumps(result,indent=2));print('PASS 4 nut roofs and 4 MAIN spacers')
