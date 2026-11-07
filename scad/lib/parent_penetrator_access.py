"""Vendor WetLink references and north-wall maintenance envelopes, mm."""
import FreeCAD as A
import Part

V=A.Vector
WALL_T=3.6  # conservative north inner-face contact over the nut's vertical span
OUTER_WALL_Y=228.3  # actual body wall; the lid flange reaches Y230
HEIGHTS=[30.,32.5,35.]
PORT_X=[150.,175.]


def vendor_shapes(root):
    ref=root/'parts/common/exterior/cots/wetlink_penetrator_m10/ref'
    # The downloaded body STEP contains three open shells; it is preserved in
    # ref/ and is not repaired into a claimed manufacturer solid. Reuse the
    # established SCAD body-only variant for its conservative reference volume.
    body=Part.read(str(ref.parent/'wetlink_penetrator_m10_ref_body_only.step'))
    assert body.isValid() and len(body.Solids)==1
    # STEP and vendor STL have different origins. Use STEP exclusively and
    # remesh after these rigid transforms; never pair it with the shifted STL.
    nut=Part.read(str(ref/'WL-M10-NUT-R1/WL-M10-NUT-PUBLIC.STEP'))
    b=nut.optimalBoundingBox(False,False)
    axial_offset=WALL_T-b.XMin
    print('VENDOR_NUT_AXIS_BOUNDS',b.XMin,b.XMax,'wall datum',WALL_T,flush=True)
    nut.rotate(V(),V(0,1,0),-90);nut.translate(V(0,0,axial_offset))
    tool=Part.read(str(ref/'WL-M10-BULKHEAD-WRENCH-R1/WL-M10-BULKHEAD-WRENCH-R1-PUBLIC.STEP'))
    tool.rotate(V(),V(0,1,0),-90);tool.translate(V(0,0,WALL_T+.5))
    # Keep imported occurrence transforms nested in a compound. Assigning an
    # imported occurrence directly to a new root feature loses its STEP frame
    # on export in this FreeCAD version; the compound preserves that frame.
    return dict(wetlink_m10_bcas_reference=Part.makeCompound([body,nut]),
                wetlink_m10_bulkhead_wrench=Part.makeCompound([tool]))


def at_north(shape,x,z):
    out=shape.copy();out.rotate(V(),V(1,0,0),90);out.translate(V(x,OUTER_WALL_Y,z))
    return out


def dry_projection_sweep(x,lift=120):
    # Bounding solids contain ALL heights in30..35 and all nut rotations.
    # Translating this stationary envelope downward covers the complete
    # upward extraction of the interior, rather than sampled mesh poses.
    shapes=[]
    for radius,front,depth in [(5.05,208.0125,20.2875),(9,216.0,9.2)]:
        low=30-radius-lift;high=35+radius
        shapes.append(Part.makeBox(2*radius,depth,high-low,V(x-radius,front,low)))
    return Part.makeCompound(shapes)


def wrench_rotation_envelope(x,z,advance=0):
    # 20.5mm outside diameter and60mm axial length from the vendor wrench.
    # A circular envelope covers its entire360-degree rotation, with0.3mm gap.
    mouth=OUTER_WALL_Y-WALL_T-.5
    return Part.makeCylinder(10.55,60+advance,V(x,mouth-60-advance,z),V(0,1,0))


def wrench_height_envelope(x,advance=10):
    mouth=OUTER_WALL_Y-WALL_T-.5
    return wrench_rotation_envelope(x,30,advance).fuse(wrench_rotation_envelope(x,35,advance)).fuse(
        Part.makeBox(21.1,60+advance,5,V(x-10.55,mouth-60-advance,30))).removeSplitter()
