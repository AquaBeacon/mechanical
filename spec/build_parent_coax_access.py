"""Rebuild only the service ring from its canonical generator."""
from pathlib import Path
import sys,json

def build(doc,parameters):
    root=Path(__file__).resolve().parents[1]
    sys.path.insert(0,str(root/'scad/lib'))
    import Part
    from parent_service_retrofit import ring_service
    from parent_case_access import tool,in_local
    folder=root/'parts/parent/interior/printed/ann_mb1_internal_rack'
    old=Part.read(str(folder/'ann_mb1_coax_ring.step'))
    s=ring_service(old)
    # Use tighter exchange precision for the inherited small chamfer surfaces.
    import FreeCAD as A
    A.ParamGet('User parameter:BaseApp/Preferences/Mod/Part').SetInt('WritePrecisionMode',1)
    A.ParamGet('User parameter:BaseApp/Preferences/Mod/Part').SetFloat('WritePrecisionVal',1e-8)
    clearance=s.common(in_local(tool(0,8),(60,60,18.8))).Volume
    assert s.isValid() and len(s.Solids)==1 and clearance<1e-6
    guide_relief=Part.makeCylinder(7,20,A.Vector(-35,-35,3))
    assert s.common(guide_relief).Volume<1e-6
    import FreeCAD as A
    import parent_gnss as G
    for x,y in G.RACK_FOOT_XY:
        seat=Part.makeCylinder(5,3,A.Vector(x-60,y-60,0))
        assert old.common(seat).cut(s).Volume<1e-6
    print('RING_REPORT='+json.dumps(dict(valid=True,solids=1,tool_diameter_mm=8,tool_intersection_mm3=clearance,wall_opening_deg=110,volume_mm3=s.Volume,bottom_seats_unchanged=True)),flush=True)
    # Normalize inherited STEP tolerances through a checked exchange roundtrip.
    import os
    path=Path(os.environ['CAD_FOUNDATION_JOB']).parent/'intermediate/ring_normalized.step'
    s.exportStep(str(path));normalized=Part.read(str(path))
    delta=abs(normalized.Volume-s.Volume)/s.Volume
    print('RING_STEP_RELATIVE_VOLUME_DELTA='+str(delta),flush=True)
    assert normalized.isValid() and len(normalized.Solids)==1 and delta<1e-5
    assert normalized.common(in_local(tool(0,8),(60,60,18.8))).Volume<1e-5
    obj=doc.addObject('Part::Feature','ann_mb1_coax_ring_service');obj.Shape=normalized
    return [obj]
