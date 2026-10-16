"""Minimal PCB corner supports for the existing parent generator, mm.

Uniform lightened fixing plates and raised screw seats; no pin-shaped pockets. Preserve the existing floor, column,
board and screw datums; offset arms clear the coax and TX reservation.
"""
import math
import FreeCAD as A,Part
v=A.Vector
MAIN_SEAT_Z=41.95
MAIN_ARM_Z=33.1
MAIN_ARM_H=2.4
SONY_ARM_Z=60.5
SONY_ARM_H=2.0
SONY_SEAT_Z=65.55
EDGE=.15

def cylinder(x,y,z,r,h):return Part.makeCylinder(r,h,v(x,y,z))
def bore(s,x,y,z,r,h):
    tool=cylinder(x,y,z,r,h)
    tool=tool.fuse(Part.makeCone(r+EDGE,r,EDGE,v(x,y,z))).fuse(Part.makeCone(r,r+EDGE,EDGE,v(x,y,z+h-EDGE)))
    return s.cut(tool)

def arm(start,end,z,h,width=6):
    x,y=start;dx,dy=end[0]-x,end[1]-y;length=math.hypot(dx,dy)
    # Rectangular strip with bevelled handling perimeter, never component pockets.
    s=Part.makeBox(length,width,h,v(0,-width/2,z))
    s=s.makeChamfer(EDGE,s.Edges)
    s.rotate(v(0,0,0),v(0,0,1),math.degrees(math.atan2(dy,dx)));s.translate(v(x,y,0))
    return s

def column(r,z,h):
    s=Part.makeCone(r-EDGE,r,EDGE,v(0,0,z))
    return s.fuse(cylinder(0,0,z+EDGE,r,h-2*EDGE)).fuse(Part.makeCone(r,r-EDGE,EDGE,v(0,0,z+h-EDGE)))

def lightened_plate(x,y,z,width,depth,height,nx,ny,rib=6):
    """Uniform rectangular bays; unrelated to pin/component positions."""
    s=Part.makeBox(width,depth,height,v(x,y,z))
    cell_w=(width-(nx+1)*rib)/nx;cell_d=(depth-(ny+1)*rib)/ny
    for i in range(nx):
        for j in range(ny):
            cut=Part.makeBox(cell_w,cell_d,height+.2,v(x+rib+i*(cell_w+rib),y+rib+j*(cell_d+rib),z-.1))
            s=s.cut(cut)
    s=s.makeChamfer(EDGE,s.Edges)
    assert s.isValid() and len(s.Solids)==1,('Lightened plate',len(s.Solids),s.Volume)
    return s

def main_shapes(holes,G):
    h=MAIN_ARM_Z-G.FLOOR_GRID_TOP_Z
    direct=bore(column(3.5,0,h),0,0,-.1,1.725,h+.2).removeSplitter()
    x0=min(q[0] for q in holes)-3.5;y0=min(q[1] for q in holes)-3.5
    width=max(q[0] for q in holes)+3.5-x0;depth=max(q[1] for q in holes)+3.5-y0
    s=lightened_plate(x0,y0,MAIN_ARM_Z,width,depth,MAIN_ARM_H,3,2)
    foot=G.MAIN_CARRIER_FOOT_XY[0]
    s=s.fuse(arm(foot,holes[1],MAIN_ARM_Z,MAIN_ARM_H))
    pad=column(3.5,MAIN_ARM_Z,36.8-MAIN_ARM_Z);pad.translate(v(*foot,0));s=s.fuse(pad)
    for i,(x,y) in enumerate(holes):
        pad=column(3.5,MAIN_ARM_Z,MAIN_SEAT_Z-MAIN_ARM_Z);pad.translate(v(x,y,0));s=s.fuse(pad)
        s=bore(s,x,y,MAIN_ARM_Z-.1,1.3 if i==1 else 1.725,MAIN_SEAT_Z-MAIN_ARM_Z+.2)
    s=bore(s,*foot,MAIN_ARM_Z-.1,1.725,36.8-MAIN_ARM_Z+.2)
    from parent_case_access import finish_cut
    s=finish_cut(s,0)
    return {'main_corner_column':direct,'main_mount_plate':s.removeSplitter()}

def sony_shapes(holes,G):
    z=G.SONY_COLUMN_JOINT_Z;thickness=1.6
    pts=G.SONY_CARRIER_FOOT_XY
    x0=min(q[0] for q in pts);y0=min(q[1] for q in pts)
    width=max(q[0] for q in pts)-x0;depth=max(q[1] for q in pts)-y0
    s=lightened_plate(x0,y0,z,width,depth,thickness,2,2)
    for x,y in pts:
        pad=column(3.5,z,thickness);pad.translate(v(x,y,0));s=s.fuse(pad)
        key=G.SONY_COLUMN_VARIANTS['sony_column_right' if x>200 else 'sony_column_left'][1]
        s=s.cut(cylinder(x,y,z-.1,(key+G.SONY_COLUMN_KEY_CLEARANCE)/2,G.SONY_COLUMN_KEY_HEIGHT+.2))
        s=bore(s,x,y,z-.1,1.725,thickness+.2)
    for x,y in holes:
        pad=column(3,z,SONY_SEAT_Z-z);pad.translate(v(x,y,0));s=s.fuse(pad)
        s=bore(s,x,y,z-.1,1.05,SONY_SEAT_Z-z+.2)
    return {'sony_mount_plate':s.removeSplitter()}
