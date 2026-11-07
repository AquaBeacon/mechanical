"""Local floor access features; called by the existing parent floor generator.

Dimensions are mm. This revision is a candidate until the penetrator positions
and the complete assembly have been verified. No optimized mesh is involved.
"""
import math
import FreeCAD as A
import Part
from cad_edge_finish import sharp_edges
from parent_service_datums import FLOOR_NUT_DEPTH

HEAD_CLEAR_D = 10.8  # User head diameter approximately 10; 0.4 radial allowance.
NUT_AF = 5.5
NUT_CLEAR_AF = 5.8
NUT_Z = 13.0
NUT_HEIGHT = 2.4
POCKET_HEIGHT = 2.6
EDGE = .1
PENETRATOR_X = [150., 175.]
PENETRATOR_HEIGHT_RANGE = [30., 35.]
THREAD_FRONT_Y = 208.0125  # 20.2875 from actual body wall Y228.3 (lid rim is230)
NUT_FRONT_Y = 216.0        # conservative axial nut envelope over the drafted wall
PENETRATOR_CLEARANCE = .8


def hex_prism(x, y, z, af, height):
    r = af / math.sqrt(3)
    p = [A.Vector(x+r*math.cos(math.pi/6+i*math.pi/3),
                  y+r*math.sin(math.pi/6+i*math.pi/3), z) for i in range(6)]
    return Part.Face(Part.makePolygon(p+[p[0]])).extrude(A.Vector(0, 0, height))


def overlap(a, b):
    if not a.BoundBox.intersect(b.BoundBox):
        return 0.
    aa,bb=a.BoundBox,b.BoundBox
    if any(min(getattr(aa,axis+'Max'),getattr(bb,axis+'Max'))-
           max(getattr(aa,axis+'Min'),getattr(bb,axis+'Min'))<1e-7 for axis in 'XYZ'):
        return 0.
    solids_a,solids_b=a.Solids,b.Solids
    if len(solids_a)>1 or len(solids_b)>1:
        return sum(overlap(first,second) for first in solids_a for second in solids_b
                   if first.BoundBox.intersect(second.BoundBox))
    try:return a.common(b).Volume
    except (ValueError,Part.OCCError):
        # Imported compounds can fail FreeCAD's element mapper on an empty
        # boolean. Repeat the geometric calculation by solid, never assume0.
        total=0.
        for first in a.Solids:
            for second in b.Solids:
                if not first.BoundBox.intersect(second.BoundBox):continue
                try:total+=second.common(first).Volume
                except (ValueError,Part.OCCError):
                    cut=first.cut(second)
                    assert cut.isValid()
                    delta=first.Volume-cut.Volume
                    assert -.001<=delta<=min(first.Volume,second.Volume)+.001
                    total+=max(0,delta)
        assert a.Solids and b.Solids
        return total


def finish_cut_rims(shape, cutters):
    edges=[]
    for edge in sharp_edges(shape):
        # Polygon facets approximate a round recess; their vertical seams
        # are not design corners. Keep flat screw reaction seats functional.
        if edge.Length < .8:
            continue
        horizontal=edge.BoundBox.ZLength<1e-6
        if horizontal and edge.BoundBox.ZMax<18.7:
            continue
        if not horizontal and edge.BoundBox.ZLength<1:
            continue
        p=Part.Vertex(edge.valueAt((edge.FirstParameter+edge.LastParameter)/2))
        relevant=cutters if horizontal else cutters[:2]
        if any(p.distToShape(c)[0]<1e-6 for c in relevant):
            edges.append(edge)
    if not edges:
        return shape, 0
    for size in [EDGE,.05,.025]:
        try:
            candidate=shape.makeChamfer(size,edges).removeSplitter()
            if candidate.isValid() and len(candidate.Solids)==1:
                return candidate,dict(edges=len(edges),chamfer_mm=size,
                                      functional_sharp='Flat screw reaction seats, polygon seams and sub0.8mm inherited bevel intersections')
        except Part.OCCError:
            pass
    raise ValueError('Access rim chamfer failed')


def socket_axes(g):
    rows = [('cradle_service_'+str(i), x, y) for i, (x, y) in enumerate(g.RACK_FOOT_XY)]
    rows += [('gnss_top_'+str(i), x, y) for i, (x, y) in enumerate(g.UNIVERSAL_FRAME_FOOT_XY)]
    rows += [('sony_top_'+str(i), x, y) for i, (x, y) in enumerate(g.SONY_CARRIER_FOOT_XY) if i != 2]
    return rows


def add_floor_access(shape, g, protected_axes):
    """North clearance and plain through holes; no nut recess or internal roof."""
    s = shape
    report = dict(status='candidate_pending_assembly_verification', sockets=[], heads=[],
                  penetrators=dict(x_mm=PENETRATOR_X, height_range_mm=PENETRATOR_HEIGHT_RANGE,
                                   wall='north body Y228.3; lid rim Y230', thread_front_y_mm=THREAD_FRONT_Y,
                                   nut_front_y_mm=NUT_FRONT_Y, clearance_mm=PENETRATOR_CLEARANCE))
    # Open to the north edge: the floor may pass vertically beside the dry
    # threads AND the nuts. The nut relief is wider only where its axial body
    # exists, preserving the relocated shared-column seat further inboard.
    rim_cutters=[]
    for radius,front in [(5+PENETRATOR_CLEARANCE,THREAD_FRONT_Y-PENETRATOR_CLEARANCE),
                         (9+PENETRATOR_CLEARANCE,NUT_FRONT_Y-PENETRATOR_CLEARANCE)]:
        # The intervening rear grid bar has no remaining support if two
        # separate slots cut it at both ends. Remove that loose strip too.
        x0=min(PENETRATOR_X)-radius;x1=max(PENETRATOR_X)+radius
        tool=Part.makeBox(x1-x0,235-front,50,A.Vector(x0,front,0))
        s=s.cut(tool).removeSplitter()
        rim_cutters.append(tool)
    assert s.isValid() and len(s.Solids)==1,('Port relief disconnects floor',len(s.Solids))
    print('FLOOR_STAGE=port notches',flush=True)
    for i, (x, y) in enumerate(g.CASE_ANCHOR_XY):
        # Compensated 24-sided recess; original shank hole and seat height stay.
        r = HEAD_CLEAR_D/2/math.cos(math.pi/24)
        p = [A.Vector(x+r*math.cos(i*math.pi/12), y+r*math.sin(i*math.pi/12),
                      g.CASE_ANCHOR_SEAT_Z) for i in range(24)]
        tool = Part.Face(Part.makePolygon(p+[p[0]])).extrude(A.Vector(0, 0, 20))
        s = s.cut(tool).removeSplitter()
        rim_cutters.append(tool)
        report['heads'].append(dict(index=i, xy=[x, y], diameter_across_flats_mm=HEAD_CLEAR_D,
                                    seat_z_mm=g.CASE_ANCHOR_SEAT_Z, used=i < 3))
    s,report['notch_and_head_rim_chamfer_edges']=finish_cut_rims(s,rim_cutters)
    # Ordinary underside screw heads bear on the unpocketed floor. Preserve
    # the verified case boundary; do not grow pads into the molded side wall.
    for label,x,y in socket_axes(g):
        r=3.5/2/math.cos(math.pi/8)
        pts=[A.Vector(x+r*math.cos(math.pi/8+j*math.pi/4),y+r*math.sin(math.pi/8+j*math.pi/4),8.7) for j in range(8)]
        s=s.cut(Part.Face(Part.makePolygon(pts+[pts[0]])).extrude(A.Vector(0,0,10.3))).removeSplitter()
        # Open only to the underside: no printing pause and no side tunnel.
        # Flats face +/-X, keeping the two east-edge nuts inside the case.
        depth=FLOOR_NUT_DEPTH
        pocket=hex_prism(x,y,g.FLOOR_GRID_BOTTOM_Z-.1,NUT_CLEAR_AF,depth+.1)
        # Small lead-in; retain sharp hex flats and roof as functional faces.
        def wire(af,z):
            rr=af/math.sqrt(3)
            pts=[A.Vector(x+rr*math.cos(math.pi/6+j*math.pi/3),y+rr*math.sin(math.pi/6+j*math.pi/3),z) for j in range(6)]
            return Part.Wire(Part.makePolygon(pts+[pts[0]]).Edges)
        lead=Part.makeLoft([wire(NUT_CLEAR_AF+.3,g.FLOOR_GRID_BOTTOM_Z-.01),
                            wire(NUT_CLEAR_AF,g.FLOOR_GRID_BOTTOM_Z+.15)],True,False)
        s=s.cut(pocket.fuse(lead)).removeSplitter()
        report['sockets'].append(dict(label=label,xy=[x,y],type='underside_open_hex_nut',
            diameter_across_flats_mm=3.5,nut_across_flats_mm=5.5,pocket_across_flats_mm=NUT_CLEAR_AF,
            pocket_depth_mm=depth,seat_z_mm=g.FLOOR_GRID_BOTTOM_Z+depth,
            insertion_direction='+Z from below',print_pause_required=False,
            functional_sharp_edges='hex antirotation flats and axial bearing shoulder',
            load_path='top screw head -> upper plate/frame -> feet -> floor -> underside nut'))
    assert s.isValid() and len(s.Solids)==1
    report['embedded_nut_pockets']=0
    report['underside_open_nut_pockets']=len(report['sockets'])
    return s,report

