"""Full-length side-groove lid; existing parent datums and child fit clearance."""
from pathlib import Path
import math,re
import FreeCAD as A, Part
from cad_edge_finish import sharp_edges
v=A.Vector
ROOT=Path(__file__).resolve().parents[2]
CHILD_SOURCE=ROOT/'parts/child/interior/printed/child_vtray_batt_floor/child_vtray_batt_floor.scad'
text=CHILD_SOURCE.read_text(encoding='utf-8')
def child(name):
    m=re.search(r'^'+name+r'\s*=\s*([0-9.]+)\s*;',text,re.M)
    assert m,('Child hook datum missing',name)
    return float(m[1])
CLEAR=child('side_clear');END_CLEAR=child('end_clear')
SCREW_INDEX=0
CAP_Z=29.0;LID_T=3.0;EDGE=.15
CAV_END=104.5;BASE_END=107.0;PLATE_END=CAV_END-END_CLEAR
NUT_AF=5.8;NUT_BOTTOM=21.5;NUT_TOP=24.0
NUT_ROOF_H=2.4;NUT_ROOF_TOP_AF=2.8;NUT_ENTRY_ANGLE_DEG=50.0
RAIL_FRONT=-3.4;RAIL_END=PLATE_END
TRAVEL=RAIL_END-RAIL_FRONT+2*CLEAR
GROOVE_BOTTOM=25.7;GROOVE_BACK_Y=6.3;GROOVE_BACK_TOP=26.9
RAIL_EDGE=0.1
MODULE_LIFT=90.0
assert RAIL_END-TRAVEL<RAIL_FRONT
def box(x,y,z,w,d,h):return Part.makeBox(w,d,h,v(x,y,z))

def nut_support_blocker(bolts):
    x,y=bolts[SCREW_INDEX];r=NUT_AF/math.sqrt(3)+1
    return box(x-r,y-7,-.1,2*r,11,CAP_Z+.2)

def rail_support_blocker():
    return Part.makeCompound([box(RAIL_FRONT-.1,6.0,25.4,CAV_END-RAIL_FRONT+.2,2.1,3.2),box(RAIL_FRONT-.1,46.9,25.4,CAV_END-RAIL_FRONT+.2,2.1,3.2)])

def nut_socket(x,y):
    """Side-loaded M3 nut with a 45-degree-or-steeper roof in upright print pose."""
    def wire(af,z):
        r=af/math.sqrt(3)
        ps=[v(x+r*math.cos(i*math.pi/3),y+r*math.sin(i*math.pi/3),z) for i in range(6)]
        return Part.makePolygon(ps+[ps[0]])
    pocket=Part.Face(wire(NUT_AF,NUT_BOTTOM)).extrude(v(0,0,NUT_TOP-NUT_BOTTOM))
    roof=Part.makeLoft([wire(NUT_AF,NUT_TOP),wire(NUT_ROOF_TOP_AF,NUT_TOP+NUT_ROOF_H)],True,False)
    r=NUT_AF/math.sqrt(3);mouth_y=y-4.5
    peak=NUT_TOP+r*math.tan(math.radians(NUT_ENTRY_ANGLE_DEG))
    ps=[v(x-r,mouth_y,NUT_BOTTOM),v(x+r,mouth_y,NUT_BOTTOM),v(x+r,mouth_y,NUT_TOP),v(x,mouth_y,peak),v(x-r,mouth_y,NUT_TOP)]
    entry=Part.Face(Part.makePolygon(ps+[ps[0]])).extrude(v(0,4.5,0))
    return pocket.fuse(roof).fuse(entry).removeSplitter()

def finish_nut_roof(shape,cutter,original):
    exterior=Part.makeCompound(original.Faces)
    # Finish the exposed entry mouth. Internal hex corners and planar roof
    # ridges preserve nut capture and the >=45 degree printing profile.
    edges=[]
    for e in sharp_edges(shape):
        p=Part.Vertex(e.valueAt((e.FirstParameter+e.LastParameter)/2))
        if e.BoundBox.ZMax>NUT_TOP+1e-5 and e.BoundBox.YMax<4.0 and p.distToShape(cutter)[0]<1e-5 and p.distToShape(exterior)[0]<1e-5:edges.append(e)
    assert edges
    for amount in [.1,.05,.025]:
        try:
            out=shape.makeChamfer(amount,edges).removeSplitter()
            if out.isValid() and len(out.Solids)==1:
                print('NUT ROOF CHAMFER',amount,len(edges),flush=True);return out
        except Part.OCCError:pass
    raise RuntimeError('Cannot finish nut entry mouth')
def base_sockets(base,bolts):
    cutters=[];out=base
    for side in [0,1]:
        # The top rises45 degrees toward the cavity: no horizontal groove roof.
        yz=[(GROOVE_BACK_Y,GROOVE_BOTTOM),(7.8,GROOVE_BOTTOM),(7.8,GROOVE_BACK_TOP+1.5),(GROOVE_BACK_Y,GROOVE_BACK_TOP)]
        if side:yz=[(55-y,z) for y,z in reversed(yz)]
        ps=[v(RAIL_FRONT-.1,y,z) for y,z in yz]
        cutter=Part.Face(Part.makePolygon(ps+[ps[0]])).extrude(v(CAV_END-RAIL_FRONT+.2,0,0))
        cutters.append(cutter);out=out.cut(cutter)
    out=out.removeSplitter()
    edges=[e for e in sharp_edges(out) if any(Part.Vertex(e.valueAt((e.FirstParameter+e.LastParameter)/2)).distToShape(c)[0]<1e-5 for c in cutters)]
    # Preserve long dovetail faces; bevel the handling rims/entry mouth locally.
    edges=[e for e in edges if e.BoundBox.XLength<1e-5 or e.Length>20]
    for amount in [RAIL_EDGE,.05,.025]:
        try:
            s=out.makeChamfer(amount,edges).removeSplitter()
            if s.isValid() and len(s.Solids)==1:
                print('SIDE GROOVE CHAMFER',amount,len(edges),flush=True);return s
        except Part.OCCError:pass
    raise RuntimeError('Cannot finish slide grooves')

def rail(side,travel=0):
    yz=[(6.6,-3),(8.9,-3),(8.9,.1),(7.8,.1),(7.8,-.9),(6.6,-2.1)]
    if side:yz=[(55-y,z) for y,z in reversed(yz)]
    ps=[v(RAIL_FRONT-travel,y,z) for y,z in yz]
    return Part.Face(Part.makePolygon(ps+[ps[0]])).extrude(v(RAIL_END-RAIL_FRONT+travel,0,0))
def lid_blank():
    body=box(RAIL_FRONT,5.1,0,RAIL_END-RAIL_FRONT,44.8,LID_T)
    ear=box(8,1,0,8,7.3,LID_T)
    return body.fuse(ear).removeSplitter()
def lid(bolts):
    s=lid_blank()
    for side in [0,1]:s=s.fuse(rail(side))
    s=s.removeSplitter();edges=sharp_edges(s)
    for amount in [EDGE,.1,.05]:
        try:
            candidate=s.makeChamfer(amount,edges).removeSplitter()
            if candidate.isValid() and len(candidate.Solids)==1:
                s=candidate;print('FULL SLIDE LID CHAMFER',amount,flush=True);break
        except Part.OCCError:pass
    else:raise RuntimeError('Cannot finish child-derived lid')
    x,y=bolts[SCREW_INDEX];r=3.45/2/math.cos(math.pi/8)
    ps=[v(x+r*math.cos(math.pi/8+i*math.pi/4),y+r*math.sin(math.pi/8+i*math.pi/4),-.1) for i in range(8)]
    cutter=Part.Face(Part.makePolygon(ps+[ps[0]])).extrude(v(0,0,LID_T+.2))
    s=s.cut(cutter).removeSplitter()
    edges=[e for e in sharp_edges(s) if Part.Vertex(e.valueAt((e.FirstParameter+e.LastParameter)/2)).distToShape(cutter)[0]<1e-5]
    s=s.makeChamfer(EDGE,edges).removeSplitter()
    assert s.isValid() and len(s.Solids)==1
    return s
def lid_boxes(bolts):
    parts=[lid_blank(),rail(0),rail(1)]
    for side in [0,1]:
        y=7.8 if side==0 else 46.1
        parts.append(box(RAIL_FRONT,y-EDGE,-EDGE,RAIL_END-RAIL_FRONT,1.1+2*EDGE,2*EDGE+.1))
        y=7.8 if side==0 else 47.2
        parts.append(box(RAIL_FRONT,y-EDGE,-.9-EDGE,RAIL_END-RAIL_FRONT,2*EDGE,2*EDGE))
    for x in [8,16]:parts.append(box(x-EDGE,5.1-EDGE,0,2*EDGE,2*EDGE,LID_T))
    return parts
