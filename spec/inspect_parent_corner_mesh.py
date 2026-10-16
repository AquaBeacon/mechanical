"""Diagnostic only: compare analytic and independent signed-volume meshes."""
import FreeCAD as A,Part,Mesh,MeshPart
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'parts/parent/interior/printed/parent_hand_service'
s=Part.read(str(p/'sony_corner_2.step'))
for f in [p/'sony_corner_2.stl',p.parents[4]/'assemblies/parent_hand_service/_work/intermediate/scad_check/sony_corner_2.stl']:
 m=Mesh.Mesh(str(f));print(f,s.Volume,m.Volume,m.isSolid(),flush=True)
for delta in [.025,.01,.005]:
 m=MeshPart.meshFromShape(Shape=s,LinearDeflection=delta,AngularDeflection=.05,Relative=False);m.write(str(p/'_work/intermediate'/('sony_corner_2_'+str(delta)+'.stl')));print(delta,s.Volume,m.Volume,flush=True)
