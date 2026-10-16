import FreeCAD as A,Part,json
from pathlib import Path
r=Path('mechanical');s=Part.read(str(r/'parts/parent/interior/pcb/parent_main/parent_main.step'));s.translate(A.Vector(18,168,64))
under=[a for a in s.Solids if a.BoundBox.ZMin<63.9]
print('UNDERSIDE',len(under))
for tag,args in [('left_edge',(18,84,58,2,84,5.7)),('right_edge',(128,84,58,2,84,5.7)),('front_rib',(20,92,58,108,2,5.7))]+[(f'pad{x}',(x-2,82.5,58,4,4,5.95)) for x in [34,43,50,55,65,70,78]]:
 b=Part.makeBox(*args[3:],A.Vector(*args[:3]));near=[q for q in under if q.BoundBox.intersect(b.BoundBox)];v=sum(q.common(b).Volume for q in near)
 print(tag,round(v,3),[(round(q.BoundBox.XMin,2),round(q.BoundBox.YMin,2),round(q.BoundBox.ZMin,2),round(q.BoundBox.XMax,2),round(q.BoundBox.YMax,2)) for q in near])
