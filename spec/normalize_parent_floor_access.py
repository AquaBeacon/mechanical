"""Verify the source-to-STEP round trip before remeshing the exchange solid."""
from pathlib import Path
import json
import FreeCAD as A
import Part


def build(doc,parameters):
    root=Path(__file__).resolve().parents[1]
    folder=root/'assemblies/parent_hand_service/_work/intermediate'
    source=A.openDocument(str(folder/'pa_floor_source.FCStd'))
    original=source.getObject('floor_plate').Shape.copy()
    access=json.loads(source.getObject('floor_plate').AccessReport)
    exchanged=Part.read(str(folder/'pa_floor_source.step'))
    def metrics(s):
        b=s.optimalBoundingBox(False,False)
        return dict(volume=s.Volume,area=s.Area,bounds=[b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax],solids=len(s.Solids),valid=s.isValid())
    before=metrics(original);after=metrics(exchanged)
    errors=[]
    for a,b in [(original,exchanged),(exchanged,original)]:
        vertices=a.Vertexes
        stride=max(1,len(vertices)//500)
        errors.append(max(Part.Vertex(v.Point).distToShape(b)[0] for v in vertices[::stride]))
    volume_delta=abs(before['volume']-after['volume'])/before['volume']
    bounds_delta=max(abs(a-b) for a,b in zip(before['bounds'],after['bounds']))
    report=dict(source=before,step=after,relative_volume_delta=volume_delta,
                bounding_box_delta_mm=bounds_delta,sampled_boundary_distance_mm=errors,
                reason='Normalize exchange tolerances after independently checking the generated analytic solid.',
                limitations='Sampled boundary check, not an exact global Hausdorff bound.')
    print('FLOOR_NORMALIZATION='+json.dumps(report),flush=True)
    assert after['valid'] and after['solids']==1 and volume_delta<1e-5 and bounds_delta<1e-5 and max(errors)<.001,report
    A.closeDocument(source.Name)
    obj=doc.addObject('Part::Feature','floor_plate');obj.Shape=exchanged
    obj.addProperty('App::PropertyString','AccessReport');obj.AccessReport=json.dumps(access)
    obj.addProperty('App::PropertyString','ExchangeCheck');obj.ExchangeCheck=json.dumps(report)
    print('FLOOR_ACCESS_REPORT='+json.dumps(access),flush=True)
    return [obj]
