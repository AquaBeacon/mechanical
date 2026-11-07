"""Case-anchor tool envelopes for the current parent; floor datums unchanged."""
import math
import FreeCAD as A, Part
import parent_gnss as G
from cad_edge_finish import sharp_edges

TOOL_CLEAR_D = 3.5  # 2.5 mm AF key: corner diameter 2.887 plus clearance
GUIDE_ID = 4.2
GUIDE_OD = 11.4  # >= 0.9 mm wall at upper mouth, clears adjacent MAIN column
BATTERY_TOOL_D = 10.8  # 2026-10-27: also passes the approximately10mm M4 head
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
        if diameter>=10:
            # Open the thin sliver beside the lead end instead of leaving a
            # fragile strip between the enlarged head passage and that end.
            b=cutter.BoundBox;cx=(b.XMin+b.XMax)/2
            cutter=cutter.fuse(Part.makeBox(cx-shape.BoundBox.XMin+1,b.YLength,150,
                                           A.Vector(shape.BoundBox.XMin-1,b.YMin,-10))).removeSplitter()
            # Construct external lip bevels as planar loft cutters. A global
            # OCC chamfer on the inherited rail/cavity intersections is not
            # stable here. Flat battery/rail bearing rims at Z3/12 are exact
            # functional interfaces, retained without a post-boolean chamfer.
            cy=(b.YMin+b.YMax)/2;front=shape.BoundBox.XMin
            def profile(z,extra):
                rr=r+extra
                pp=[A.Vector(cx+rr*math.cos(i*math.pi/6),cy+rr*math.sin(i*math.pi/6),z) for i in range(12)]
                disk=Part.Face(Part.makePolygon(pp+[pp[0]]))
                q=[A.Vector(xx,yy,z) for xx,yy in [(front-1,cy-rr),(cx,cy-rr),(cx,cy+rr),(front-1,cy+rr)]]
                face=disk.fuse(Part.Face(Part.makePolygon(q+[q[0]]))).removeSplitter()
                assert len(face.Faces)==1
                return face.Faces[0].OuterWire
            bottom=shape.BoundBox.ZMin;top=shape.BoundBox.ZMax
            for z0,e0,z1,e1 in [(bottom-.01,EDGE,bottom+EDGE,0),(top-EDGE,0,top+.01,EDGE)]:
                cutter=cutter.fuse(Part.makeLoft([profile(z0,e0),profile(z1,e1)],True,True))
            for sign in [-1,1]:
                yy=cy+sign*r
                q=[A.Vector(front-EDGE,yy, -10),A.Vector(front-EDGE,yy+sign*EDGE,-10),A.Vector(front+EDGE,yy,-10)]
                cutter=cutter.fuse(Part.Face(Part.makePolygon(q+[q[0]])).extrude(A.Vector(0,0,150)))
            result=shape.cut(cutter).removeSplitter()
            assert result.isValid() and len(result.Solids)==1,('Battery head passage disconnected part',len(result.Solids))
            print('BATTERY_HEAD_OPENING D10.8, open lead end; external lip bevel0.2; flat bearing rims preserved',flush=True)
            return result
    result=shape.cut(cutter).removeSplitter()
    edges=[e for e in sharp_edges(result) if Part.Vertex(e.valueAt((e.FirstParameter+e.LastParameter)/2)).distToShape(cutter)[0]<1e-5 and not any(e.isSame(old) for old in shape.Edges)]
    if diameter is not None and diameter>=10:
        # Round-profile polygon seams are not physical handling corners.
        edges=[e for e in edges if e.Length>.5 and
               (e.BoundBox.ZLength<1e-6 or abs(e.BoundBox.XMin-shape.BoundBox.XMin)<1e-6)]
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
