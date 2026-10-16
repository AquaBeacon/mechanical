"""FreeCAD command-line exporter; run with CABLE_ROOT set to Body_Models."""
import os,json
from pathlib import Path
import FreeCAD as App
import Part,MeshPart

root=Path(os.environ['CABLE_ROOT'])
folder=root/'parts/common/cabling/parent_td04a_cable'
data=json.loads((folder/'route.json').read_text(encoding='utf-8'))
def v(x):return App.Vector(*x)
edges=[]
for s in data['segments']:
    edges.append(Part.makeLine(v(s['start']),v(s['end'])) if s['kind']=='line'
                 else Part.Arc(v(s['start']),v(s['middle']),v(s['end'])).toShape())
path=Part.Wire(edges)
start=v(data['segments'][0]['start']); tangent=v(data['segments'][0]['end'])-start
for name,radius in [('parent_td04a_cable',data['diameter_mm']/2),
                    ('parent_td04a_cable_clearance',data['diameter_mm']/2+data['margin_mm'])]:
    profile=Part.Wire([Part.makeCircle(radius,start,tangent)])
    solid=path.makePipeShell([profile],True,False)
    assert solid.isValid() and len(solid.Solids)==1,name
    solid.exportStep(str(folder/(name+'.step')))
    mesh=MeshPart.meshFromShape(Shape=solid,LinearDeflection=0.10,AngularDeflection=0.15,Relative=False)
    mesh.write(str(folder/(name+'.stl')))
    print(name,'valid',solid.Volume,flush=True)
