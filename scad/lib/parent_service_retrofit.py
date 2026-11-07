"""Parametric retrofit candidates for existing parent generators. Units: mm.

Not topology-optimization reconstruction. Keep candidates out of production until
the complete assembly and fastening checks have passed.
"""
import math
import FreeCAD as A
import Part
import parent_gnss as D
from parent_service_datums import (MAIN_LIFT,ANT_SOUTH,ANT_LIFT,PWR_LIFT,PWR_SOUTH,
    SENSOR_LEG_LENGTH,SENSOR_BASE_Z,SENSOR_JOINT_Z,SONY_SERVICE_LIFT,GNSS_SERVICE_LIFT,
    FLOOR_WASHER_T,FLOOR_HEAD_Z,retrofit_fasteners)
from parent_corner_mounts import main_shapes,arm,column
from cad_edge_finish import sharp_edges

V=A.Vector
BASE_HEAD_Z=35.6 # M3x30 clears a full nut + washer below the reused floor.
EDGE=.2
PCB_PILOT_D=2.8 # Same nominal M3 plastic pilot as child_vtray_deck.
SPACER_CLEARANCE_D=3.5
MAIN_FRAME_BOTTOM_Z=33.4
MAIN_FRAME_TOP_Z=39.5

def box(x,y,z,w,d,h): return Part.makeBox(w,d,h,V(x,y,z))
def cyl(x,y,z,r,h): return Part.makeCylinder(r,h,V(x,y,z))
def bore(s,x,y,z,r,h):
    # Circumscribed octagon: specified diameter is the across-flat clearance.
    rr=r/math.cos(math.pi/8)
    p=[V(x+rr*math.cos(math.pi/8+i*math.pi/4),y+rr*math.sin(math.pi/8+i*math.pi/4),z) for i in range(8)]
    tool=Part.Face(Part.makePolygon(p+[p[0]])).extrude(V(0,0,h))
    tool=tool.fuse(Part.makeCone(r+.15,r,.15,V(x,y,z))).fuse(Part.makeCone(r,r+.15,.15,V(x,y,z+h-.15)))
    return s.cut(tool)
def finish(s,r=EDGE):
    s=s.removeSplitter()
    return s.makeChamfer(r,sharp_edges(s))

def hex_tool(x,y,z,af,h):
    r=af/math.sqrt(3)
    p=[V(x+r*math.cos(math.pi/6+i*math.pi/3),y+r*math.sin(math.pi/6+i*math.pi/3),z) for i in range(6)]
    return Part.Face(Part.makePolygon(p+[p[0]])).extrude(V(0,0,h))

def nut_slot(s,x,y,bottom,af=5.8,height=2.6,entry=1,reach=7,axis='x'):
    # Side entry; axial reaction is the roof above the nut, not a top-open hex.
    s=s.cut(hex_tool(x,y,bottom,af,height))
    ywidth=2*af/math.sqrt(3)
    if axis=='y':
        return s.cut(box(x-af/2,y if entry>0 else y-reach,bottom,af,reach,height))
    x0=x if entry>0 else x-reach
    return s.cut(box(x0,y-ywidth/2,bottom,reach,ywidth,height))

def main_antenna_cradle(holes,G,return_parts=False):
    plate_z=37.1;seat=41.95+MAIN_LIFT
    s=main_shapes(holes,G,arm_z=plate_z,seat_z=seat,finish_access=False,include_offset=False)['main_mount_plate']
    # Solid PCB bosses for direct M3 fastening; no nut pockets.
    for x,y in holes:
        p=column(5,plate_z,seat-plate_z);p.translate(V(x,y,0));s=s.fuse(p)
    # Existing ring/floor attachment axes are kept. Right wall is offset to
    # clear the PCB edge and leave the base fasteners accessible from above.
    base_z=G.RACK_BASE_Z+G.RACK_RING_JOINT_LOCAL_Z
    top=G.GROUND_PLATE_Z+ANT_LIFT
    for x,y in G.RACK_FOOT_XY:
        s=s.fuse(finish(cyl(x,y,base_z,5,BASE_HEAD_Z-base_z)))
    wall_z=33.4 # above the cable winding and its outer wall
    s=s.fuse(finish(box(8.1,21,wall_z,7.8,78,top-wall_z)))
    s=s.fuse(finish(box(134.5,21,wall_z,6,78,top-wall_z)))
    for x,y in G.RACK_FOOT_XY:
        wall_x=12 if x<60 else 137.5
        s=s.fuse(arm([x,y],[wall_x,y],base_z,6,8)) if x!=wall_x else s
    for y in [35,75]:
        s=s.fuse(arm([12,y],[22,y],plate_z,2.4,8))
        s=s.fuse(arm([125,y],[137.5,y],plate_z,2.4,8))
    # New antenna platform avoids the expanded RTC entirely in XY.
    s=s.fuse(finish(box(16,30-ANT_SOUTH,top-5,88,60,5)))
    for y in [35,65]:
        s=s.fuse(arm([12,y],[22,y],top-5,5,8))
        s=s.fuse(arm([100,y],[137.5,y],top-5,5,8))
    # Existing steel plate holes, translated with the plate. Nuts enter from
    # the bottom; local captive roof prevents pull-through toward the steel.
    for gx,gy in G.GROUND_PLATE_HOLES_XY:
        y=gy-ANT_SOUTH
        s=bore(s,gx,y,top-5.1,1.725,5.2)
    for x in [26,94]:
        y=60-ANT_SOUTH
        s=bore(s,x,y,top-5.1,2.25,5.2)
    for x,y in holes:
        s=bore(s,x,y,plate_z-.1,PCB_PILOT_D/2,seat-plate_z+.2)
        s=s.cut(cyl(x,y,seat+.1,3.5,top-seat+2))
    for x,y in G.RACK_FOOT_XY:
        s=bore(s,x,y,base_z-.1,1.725,BASE_HEAD_Z-base_z+.2)
        # M3x8 service bolt; its head and hex key fit outside the PCB/steel.
        s=bore(s,x,y,BASE_HEAD_Z,3.2,top-BASE_HEAD_Z+5)
    # Remove thin wall crescents around the socket wells; retain a 3.44mm
    # deep connection below the nut seats and the continuous central walls.
    for y in [20,90]:
        s=s.cut(box(6,y,BASE_HEAD_Z,11,10,top-BASE_HEAD_Z+1))
        s=s.cut(box(129,y,BASE_HEAD_Z,13,10,top-BASE_HEAD_Z+1))
    # Required RTC reserve (+10 mm, plus a 1 mm XY border).
    s=s.cut(box(58,82.3,52.095+MAIN_LIFT,42,22,20))
    # Recesses for the unchanged LiPo tray and the moved PWR front component.
    s=s.cut(box(138.2,20,base_z-.1,5,6.5,10.6))
    s=s.cut(box(81.8,104,plate_z-.1,7.9,8,2.6))
    # Clear the original-orientation PWR front edge and fastening heads.
    # Rear MAIN corner posts remain whole; both side rails retain their load path.
    cutter=box(27.7,100,plate_z-.3,81.8,12,3.5)
    before=s;s=s.cut(cutter).removeSplitter()
    edges=[e for e in sharp_edges(s) if Part.Vertex(e.valueAt((e.FirstParameter+e.LastParameter)/2)).distToShape(cutter)[0]<1e-5 and not any(e.isSame(old) for old in before.Edges)]
    assert edges
    s=s.makeChamfer(.1,edges).removeSplitter()
    from parent_case_access import tool
    s=s.cut(tool(0))
    s=s.removeSplitter()
    assert s.isValid() and len(s.Solids)==1,('cradle',[(p.Volume,str(p.BoundBox)) for p in s.Solids])
    # Separate feet have clearance bores; one bolt clamps frame, foot and floor.
    bases={}
    for i,(x,y) in enumerate(G.RACK_FOOT_XY):
        p=s.common(box(x-7,y-7,21.7,14,14,11.7))
        z=p.BoundBox.ZMin
        p=p.fuse(cyl(x,y,z,1.9,33.4-z))
        # Clip to an octagonal envelope; preserve the existing contact datums.
        radius=5
        points=[V(x+radius*math.cos(math.pi/8+j*math.pi/4),y+radius*math.sin(math.pi/8+j*math.pi/4),z-.1) for j in range(8)]
        envelope=Part.Face(Part.makePolygon(points+[points[0]])).extrude(V(0,0,33.6-z))
        p=p.common(finish(envelope,.1))
        p=bore(p,x,y,z-.1,SPACER_CLEARANCE_D/2,33.4-z+.2)
        bases['cradle_floor_foot_'+str(i)]=p.removeSplitter()
    s=s.common(box(0,0,33.4,210,230,80))
    # Shelf is installed after MAIN, then stays attached during service.
    # This avoids sliding the populated board under a permanently closed roof.
    joints=[(12,35),(12,75),(137.5,35),(137.5,75)]
    for x,y in joints:
        s=bore(s,x,y,40.3,PCB_PILOT_D/2,top-40.3+.2)
    lower=s.common(box(0,0,33.4,210,230,16.6))
    # Extend the actual finished lower faces to the feet's print datum. Keep
    # the original PCB seat, rear PWR relief and lightening bays unchanged.
    for face in list(lower.Faces):
        if face.BoundBox.ZLength<1e-6 and abs(face.BoundBox.ZMin-plate_z)<1e-6 and face.normalAt(0,0).z<-.99:
            extension=face.extrude(V(0,0,-(plate_z-MAIN_FRAME_BOTTOM_Z+.05)))
            extension.translate(V(0,0,.05))
            # Keep functional bore rims/coplanar union seams exact. Finish the
            # long straight bed perimeter; tiny legacy mouth facets stay local.
            edges=[e for e in sharp_edges(extension) if e.BoundBox.ZLength<1e-6 and abs(e.BoundBox.ZMin-MAIN_FRAME_BOTTOM_Z)<1e-6 and e.Length>4 and isinstance(e.Curve,Part.Line)]
            if edges:extension=extension.makeChamfer(.05,edges)
            lower=lower.fuse(extension)
    lower=lower.cut(tool(0)).removeSplitter()
    # Top-down M3x30 bolts clamp MAIN, foot, ring and floor to underside nuts.
    # Preserve the original open head wells and their flat Z35.6 bearing seats.
    for x,y in G.RACK_FOOT_XY:
        lower=bore(lower,x,y,MAIN_FRAME_BOTTOM_Z-.1,SPACER_CLEARANCE_D/2,2.4)
    # Broad PWR-edge relief, with a sloping roof rather than a new floating
    # horizontal ledge. It clears the board's underside without pin pockets.
    profile=[V(x,99.8,z) for x,z in [(25.6,33.3),(110,33.3),(110,40.3),(28.7,40.3),(25.6,35.6)]]
    pwr_relief=Part.Face(Part.makePolygon(profile+[profile[0]])).extrude(V(0,12.8,0))
    before=lower;lower=lower.cut(pwr_relief).removeSplitter()
    # The curved intersection with a PCB boss is a functional bearing/root
    # transition. Bevel only free straight handling rims of the relief.
    new_edges=[e for e in sharp_edges(lower) if e.Length>2 and isinstance(e.Curve,Part.Line) and e.BoundBox.ZMax>35.6 and Part.Vertex(e.valueAt((e.FirstParameter+e.LastParameter)/2)).distToShape(pwr_relief)[0]<1e-5 and not any(e.isSame(old) for old in before.Edges)]
    for amount in [.1,.05,.025]:
        try:
            candidate=lower.makeChamfer(amount,new_edges).removeSplitter()
            if candidate.isValid() and len(candidate.Solids)==1:
                lower=candidate;break
        except Part.OCCError:pass
    else:raise RuntimeError('PWR relief edge finishing failed')
    upper=s.common(box(0,0,50,210,230,40))
    for x,y in joints:
        key=cyl(x,y,49.9,2.7,.9).cut(cyl(x,y,49.8,PCB_PILOT_D/2,1.1))
        lower=lower.fuse(key)
        lower=bore(lower,x,y,40.3,PCB_PILOT_D/2,11)
        upper=bore(upper,x,y,49.9,1.725,top-49.9+.2)
        upper=upper.cut(cyl(x,y,49.9,2.8,1.0))
    parts=dict(main_service_frame=lower.removeSplitter(),antenna_service_shelf=upper.removeSplitter(),**bases)
    for name,p in parts.items():
        assert p.isValid() and len(p.Solids)==1,(name,len(p.Solids))
    return parts if return_parts else Part.makeCompound([parts['main_service_frame'],parts['antenna_service_shelf']])

def power_adapter(old_holes,pwr_lift=PWR_LIFT,pwr_south=PWR_SOUTH):
    """Offset mount using existing floor bosses; original board orientation.

    The rectangular hole set is180-degree symmetric; mapping pairs is retained.
    """
    s=None
    old_seat=28.25;new_seat=old_seat+pwr_lift
    for x,y in old_holes:
        nx,ny=135.6-x,330-y-pwr_south
        # Match the mirrored hole to the nearest original boss on the same side.
        ox,oy=min(old_holes,key=lambda p:(p[0]-nx)**2+(p[1]-(ny+pwr_south))**2)
        piece=arm([ox,oy],[nx,ny],old_seat,3,6)
        piece=piece.fuse(finish(cyl(ox,oy,old_seat,4.2,3)))
        radius=3.8 if nx<50 and ny<150 else 4.5
        piece=piece.fuse(finish(cyl(nx,ny,old_seat,radius,new_seat-old_seat)))
        piece=bore(piece,ox,oy,old_seat-.1,1.725,3.2)
        piece=bore(piece,nx,ny,old_seat-.1,PCB_PILOT_D/2,new_seat-old_seat+.2)
        s=piece if s is None else s.fuse(piece)
    # Two longitudinal rails and a transverse rear link form one printable part.
    xs=sorted(set(x for x,y in old_holes));ys=sorted(set(y for x,y in old_holes))
    for x in xs:
        s=s.fuse(arm([x,ys[0]],[x,ys[-1]],old_seat,3,3))
    s=s.fuse(arm([xs[0],ys[-1]],[xs[-1],ys[-1]],old_seat,3,3))
    # Rails must not refill the previously cut screw and nut passages.
    for x,y in old_holes:
        nx,ny=135.6-x,330-y-pwr_south
        s=bore(s,x,y,old_seat-.1,1.725,3.2)
        # Recess M3 socket head1mm; retain2mm clamping seat underneath.
        s=bore(s,x,y,old_seat+2,2.9,1.2)
        s=bore(s,nx,ny,old_seat-.1,PCB_PILOT_D/2,new_seat-old_seat+.2)
    s=s.removeSplitter()
    assert s.isValid() and len(s.Solids)==1,('power adapter',len(s.Solids))
    return s

def fixed_column(x,y,width,depth,joint_z,key=None,entry=None):
    """Polygonal column, clearance bore, through bolt with an underside nut."""
    s=finish(box(x-width/2,y-depth/2,18.8,width,depth,joint_z-18.8),.15)
    if key:
        kind,a,b=key
        k=cyl(x,y,joint_z-.1,a/2,.9) if kind=='round' else box(x-a/2,y-b/2,joint_z-.1,a,b,.9)
        s=s.fuse(k)
    s=bore(s,x,y,18.7,SPACER_CLEARANCE_D/2,joint_z-18.7+1)
    return s.removeSplitter()

def fixed_sensor_columns(G,tx_holes):
    """Two one-piece support frames, four50mm legs each, no captive nuts."""
    result={}
    for name,points in [('gnss_support_frame',G.UNIVERSAL_FRAME_FOOT_XY),
                        ('sony_support_frame',G.SONY_CARRIER_FOOT_XY)]:
        pieces=[]
        for i,(x,y) in enumerate(points):
            if name.startswith('gnss'):
                w,d=G.UNIVERSAL_COLUMN_SIZE_REAR if y>200 else G.UNIVERSAL_COLUMN_SIZE_FRONT
            else:w,d=G.SONY_COLUMN_VARIANTS['sony_column_right' if x>200 else 'sony_column_left'][0],9
            piece=box(x-w/2,y-d/2,SENSOR_BASE_Z,w,d,SENSOR_LEG_LENGTH)
            if name.startswith('gnss'):
                key=box(x-(w-2)/2,y-(d-2)/2,SENSOR_JOINT_Z-.1,w-2,d-2,.9)
            else:
                key_d=G.SONY_COLUMN_VARIANTS['sony_column_right' if x>200 else 'sony_column_left'][1]
                key=cyl(x,y,SENSOR_JOINT_Z-.1,key_d/2,.9)
            pieces.append(piece.fuse(key))
        if name.startswith('gnss'):
            routes=[(points[a],points[b]) for a,b in [(0,1),(1,3),(3,2)]]
            # Go west of the NW M4 head, then east of the case corner post.
            routes += [(points[0],[13,200]),([13,200],[16,211]),([16,211],points[2])]
        else:
            # U frame opens north. The front link lies south of the low TX
            # pins (Y>=135.53) and north of the battery tray (Y<=129.1).
            front_y=131.4  # 0.3mm north of the battery envelope at Y129.1.
            routes=[([points[0][0],front_y],points[2]),
                    ([points[1][0],front_y],points[3]),
                    ([points[0][0],front_y],[points[1][0],front_y])]
        pieces.extend(arm(a,b,SENSOR_BASE_Z,4,4,finish_edges=False) for a,b in routes)
        shape=pieces[0]
        for piece in pieces[1:]:shape=shape.fuse(piece)
        shape=shape.removeSplitter()
        if name.startswith('sony'):
            # Actual KiCad mounting axes, transformed with the TX placement.
            # Radius3.5 floor bosses +0.3 clearance leave a2.3mm front web.
            for hx,hy in tx_holes:
                x,y=G.TX_ORIGIN[0]+hy,G.TX_ORIGIN[1]+hx
                shape=shape.cut(cyl(x,y,SENSOR_BASE_Z-.1,3.8,6.2))
            shape=shape.removeSplitter()
        # Finish the complete union once, including its concave beam roots.
        # Bevelled primitives fused first can leave frozen micro-edges in OCC.
        shape=finish(shape,.1)
        for i,(x,y) in enumerate(points):
            if name.startswith('sony') and i==2:
                shape=bore(shape,x,y,SENSOR_JOINT_Z-10,PCB_PILOT_D/2,11)
            else:
                shape=bore(shape,x,y,SENSOR_BASE_Z-.1,SPACER_CLEARANCE_D/2,SENSOR_LEG_LENGTH+1.1)
        assert shape.isValid() and len(shape.Solids)==1,(name,len(shape.Solids))
        result[name]=shape.removeSplitter()
    return result

def spacer_threads(G):
    """Intentional thread volumes only; no general collision exclusions."""
    out=[]
    def add(label,host,lo,hi,clamped,direction):
        out.append(dict(label=label,host=host,zlo=lo,zhi=hi,clamped=clamped,direction=direction))
    for i in range(4):
        add('shelf_joint_'+str(i),'main_service_frame',42.4,50.8,'antenna_service_shelf',-1)
    return out

def collect_shapes(G,main_holes,pwr_holes,tx_holes):
    out=main_antenna_cradle(main_holes,G,True)
    out['power_adapter']=power_adapter(pwr_holes)
    from parent_corner_mounts import sony_shapes,sony_holes
    out['sony_mount_plate']=sony_shapes(sony_holes(G),G)['sony_mount_plate']
    out.update(fixed_sensor_columns(G,tx_holes))
    ring=Part.read(str(G.ROOT/'parts/parent/interior/printed/ann_mb1_internal_rack/ann_mb1_coax_ring.step'))
    out['ann_mb1_coax_ring_service']=ring_service(ring)
    out.update(cable_routes(G))
    return out

def variant_folder(name):
    if name.startswith('coax_'):return 'parts/parent/interior/cots/ann_mb1'
    if name in ['antenna_service_shelf','ann_mb1_coax_ring_service','cradle_nut_keeper'] or name.startswith('cradle_floor_foot_'):
        return 'parts/parent/interior/printed/ann_mb1_internal_rack'
    if name.startswith('gnss_'):
        return 'parts/parent/interior/printed/gnss_universal_carrier'
    return 'parts/parent/interior/printed/parent_hand_service'

def cradle_nut_keeper():
    # The head and shank share Y=-0.4: one flat bed face after X90 rotation.
    return finish(box(-2,-.4,0,4,1.0,.8).fuse(box(-1.5,-.4,.7,3,.8,10.0)),.05)

def ring_service(s,world=False):
    """8 mm tool passage and 110 degree north wall opening; retain floor seats."""
    from parent_case_access import tool,in_local
    offset=0 if world else 60
    z=26.9 if world else 26.9-18.8
    s=s.cut(box(17-offset,88-offset,z,9.5,24,9)).removeSplitter()
    tool_d=8.0
    cutter=tool(0,tool_d)
    if not world:cutter=in_local(cutter,(60,60,18.8))
    # Remove the whole raised guide around the southwest tool access. Enlarging
    # the tilted bore alone leaves feather-thin remnants at the outer wall.
    guide_relief_radius=7.0
    guide_relief_z=21.8 if world else 3.0
    cutter=cutter.fuse(cyl(25-offset,25-offset,guide_relief_z,guide_relief_radius,20))
    # North (+Y) faces the power board. Remove only the raised outer wall.
    cx=60-offset;cy=60-offset;floor_top=22.3 if world else 3.5
    points=[V(cx,cy,floor_top)]+[V(cx+80*math.cos(math.radians(a)),cy+80*math.sin(math.radians(a)),floor_top) for a in range(35,146,5)]
    sector=Part.Face(Part.makePolygon(points+[points[0]])).extrude(V(0,0,20))
    sector=sector.cut(cyl(cx,cy,floor_top-1,50,22))
    cutter=cutter.fuse(sector)
    # Same approximately10mm M4 head envelope as the revised floor; preserve
    # the higher guide-wall relief but enlarge its former8.2mm lower opening.
    cutter=cutter.fuse(cyl(25-offset,25-offset,16.7 if world else -2.1,5.4,5.7))
    result=s.cut(cutter).removeSplitter()
    # Chamfer the two long, accessible cut ends; preserve inherited bevel joins.
    edges=[e for e in sharp_edges(result) if e.BoundBox.ZLength>5 and e.BoundBox.XLength<1e-5 and e.BoundBox.YLength<1e-5 and e.CenterOfMass.y>0]
    if edges:
        result=result.makeChamfer(.2,edges).removeSplitter()
    assert result.isValid() and len(result.Solids)==1
    return result


def cable_routes(G):
    """Nominal RG174 leads; 20mm circular bends and a free antenna-side loop.

    The winding itself retains the existing annular reservation. These two
    reference tubes are purchased cable, never printable parts.
    """
    r=20.;z=68.4+ANT_LIFT;end_z=G.BOARD_ORIGIN[2]+GNSS_SERVICE_LIFT+3.8
    def tube(edges,start,tangent):
        wire=Part.Wire(edges)
        profile=Part.Wire([Part.makeCircle(1.4,V(*start),V(*tangent))])
        s=wire.makePipeShell([profile],True,False)
        assert s.isValid() and len(s.Solids)==1
        return s,wire.Length
    edges=[]
    def arc(fn,angle):
        edges.append(Part.Arc(fn(0),fn(angle/2),fn(angle)).toShape());return fn(angle)
    def line(a,b):edges.append(Part.makeLine(a,b));return b
    p=arc(lambda a:V(60-r*(1-math.cos(a)),78+r*math.sin(a),z),math.pi/2)
    p=arc(lambda a:V(40-r*math.sin(a),118-r*math.cos(a),z),math.pi/2)
    p=line(p,V(20,148,z))
    p=arc(lambda a:V(20,148+r*math.sin(a),z-r*(1-math.cos(a))),math.pi/2)
    p=line(p,V(20,168,49.5))
    p=arc(lambda a:V(20,148+r*math.cos(a),49.5-r*math.sin(a)),math.pi/2)
    p=line(p,V(20,85,29.5))
    angle=math.atan2(25,60)
    p=arc(lambda a:V(r*math.cos(a),85-r*math.sin(a),29.5),angle)
    antenna,length=tube(edges,(60,78,z),(0,1,0))
    print('CABLE_LOOP_LENGTH_MM='+str(length),flush=True)
    edges=[];p=V(23.5,85,29.5);p=line(p,V(23.5,108,29.5))
    p=arc(lambda a:V(23.5,108+r*math.sin(a),29.5+r*(1-math.cos(a))),math.pi/2)
    p=line(p,V(23.5,128,end_z-r))
    p=arc(lambda a:V(23.5,148-r*math.cos(a),end_z-r+r*math.sin(a)),math.pi/2)
    p=line(p,V(23.5,159.6,end_z))
    p=arc(lambda a:V(43.5-r*math.cos(a),159.6+r*math.sin(a),end_z),math.pi/2)
    p=line(p,V(G.BOARD_ORIGIN[0]-64.256,179.6,end_z))
    receiver,_=tube(edges,(23.5,85,29.5),(0,1,0))
    return dict(coax_service_loop=antenna,coax_receiver_service=receiver)
