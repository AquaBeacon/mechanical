"""Case-anchor tool envelopes for the current parent; floor datums unchanged."""
import math
import FreeCAD as A, Part
import parent_gnss as G
from cad_edge_finish import sharp_edges

TOOL_CLEAR_D = 3.5  # 2.5 mm AF key: corner diameter 2.887 plus clearance
GUIDE_ID = 4.2
GUIDE_OD = 11.4  # >= 0.9 mm wall at upper mouth, clears adjacent MAIN column
BATTERY_TOOL_D = 8.0  # effective across flats, upper tray only; floor unchanged
EDGE = .2
TILT_DEG = 10.0

def direction(index):
    t=math.radians(TILT_DEG)
    return A.Vector(-math.sin(t)/math.sqrt(2),-math.sin(t)/math.sqrt(2),math.cos(t)) if index==0 else A.Vector(-math.sin(t),0,math.cos(t)) if index==2 else A.Vector(0,0,1)

def tool(index,diameter=GUIDE_ID):
    x,y=G.CASE_ANCHOR_XY[index]
    z=G.CASE_ANCHOR_SEAT_Z+G.CASE_ANCHOR_HEAD_DH[1]
    axis=direction(index)
    return Part.makeCylinder(diameter/2,125,A.Vector(x,y,z)-axis*3,axis)

def in_local(s,offset=(0,0,0),rotation_z=0):
    s=s.copy(); s.translate(A.Vector(*[-x for x in offset]))
    if rotation_z:s.rotate(A.Vector(),A.Vector(0,0,1),-rotation_z)
    return s

def finish_cut(shape,index,offset=(0,0,0),rotation_z=0,diameter=None):
    """Chamfer only newly introduced handling edges of the tool aperture."""
    if diameter is None:
        cutter=in_local(tool(index),offset,rotation_z)
    else:
        assert index==1, 'Enlarged polygon is the vertical battery tool opening'
        x,y=G.CASE_ANCHOR_XY[index];r=diameter/2/math.cos(math.pi/12)
        points=[A.Vector(x+r*math.cos(i*math.pi/6),y+r*math.sin(i*math.pi/6),-10) for i in range(12)]
        cutter=in_local(Part.Face(Part.makePolygon(points+[points[0]])).extrude(A.Vector(0,0,150)),offset,rotation_z)
    result=shape.cut(cutter).removeSplitter()
    edges=[e for e in sharp_edges(result) if Part.Vertex(e.valueAt((e.FirstParameter+e.LastParameter)/2)).distToShape(cutter)[0]<1e-5 and not any(e.isSame(old) for old in shape.Edges)]
    assert edges, ('No new access edges',index)
    for amount in [EDGE,.15,.1,.05]:
        try:
            candidate=result.makeChamfer(amount,edges).removeSplitter()
            if candidate.isValid() and len(candidate.Solids)==1:
                result=candidate
                print('ACCESS CHAMFER',index,amount,len(edges),flush=True)
                break
        except Part.OCCError:pass
    else:raise RuntimeError(('Could not finish access aperture',index,len(edges)))
    assert result.isValid() and len(result.Solids)==1,('Access hole disconnected part',index)
    return result

def ring_access(ring):
    offset=G.ANTENNA_CENTRE+[G.RACK_BASE_Z]
    # Closed guide wall keeps the installed coil out of the tool bore. Top is
    # horizontal in print pose, and all new mouths receive a local chamfer.
    x,y=G.CASE_ANCHOR_XY[0]
    guard=in_local(Part.makeCylinder(GUIDE_OD/2,30,A.Vector(x,y,G.RACK_BASE_Z)),offset)
    bottom=3.3  # preserve the existing M4 head relief below the ring
    clip=Part.makeBox(210,230,G.COIL_BOTTOM_LOCAL+G.COIL_HEIGHT+.5-bottom,A.Vector(-60,-60,bottom))
    guard=guard.common(clip)
    guard=guard.makeChamfer(EDGE,sharp_edges(guard))
    old=ring
    ring=ring.fuse(guard).removeSplitter()
    old_wire=Part.makeCompound(old.Edges);guard_wire=Part.makeCompound(guard.Edges)
    roots=[]
    for e in sharp_edges(ring):
        point=Part.Vertex(e.valueAt((e.FirstParameter+e.LastParameter)/2))
        # Bevel intersections at the already finished top/bottom rims retain
        # their bevel; blend the new long vertical cylinder-to-wall roots.
        if e.BoundBox.ZLength>.5 and max(e.BoundBox.XLength,e.BoundBox.YLength)<.5 and point.distToShape(guard)[0]<1e-5 and point.distToShape(old)[0]<1e-5 and point.distToShape(old_wire)[0]>1e-5 and point.distToShape(guard_wire)[0]>1e-5:roots.append(e)
    if roots:
        for method,size in [('makeFillet',.2),('makeFillet',.1),('makeChamfer',.1),('makeChamfer',.05),('makeChamfer',.025)]:
            try:
                candidate=getattr(ring,method)(size,roots).removeSplitter()
                if candidate.isValid() and len(candidate.Solids)==1:
                    ring=candidate;print('ACCESS ROOT',method,size,len(roots),flush=True);break
            except Part.OCCError:pass
        else:raise RuntimeError(('Could not finish guide root',len(roots)))
    return finish_cut(ring,0,offset)

def coil_access(reserve):
    # The OD100/ID75/H10 outer bounds remain. The installed winding must leave
    # the guard occupied region vacant; actual 5 m capacity remains unverified.
    x,y=G.CASE_ANCHOR_XY[0]
    guard=Part.makeCylinder((GUIDE_OD+.4)/2,30,A.Vector(x,y,G.RACK_BASE_Z))
    return reserve.cut(in_local(guard,G.ANTENNA_CENTRE+[G.RACK_BASE_Z])).removeSplitter()
