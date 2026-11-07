// Canonical source, millimetres. Print flat, Z=0 on bed.
use <../../../../scad/lib/edge_finished_profiles.scad>
/* [Nut interface] */
nut_af = 10;
af_clearance = 0.05; // Total across-flats difference: 0.025 mm per flat.
socket_corner_r = 0.05;
// Provisional until the actual nut thickness and bolt diameter are measured.
socket_depth = 7;
lid_thickness = 3;
bolt_clearance_d = 7;
floor_chamfer = 0.01;
/* [Grip] */
grip_length = 72;
grip_width = 32;
finger_hole_d = 22;
finger_offset = 20;
edge_chamfer = 0.6;
entry_chamfer = 0.4;
/* [Hidden] */
body_height = socket_depth+lid_thickness;
$fn = 96;
assert(nut_af>0 && af_clearance>0);
assert(grip_length>=grip_width && grip_width>2*(nut_af+af_clearance)/sqrt(3)+4);
assert(body_height>2*max(edge_chamfer,entry_chamfer));
assert(socket_corner_r>0 && edge_chamfer>0 && entry_chamfer>0);
assert(af_clearance/2 > socket_corner_r*(1/cos(30)-1));
assert(floor_chamfer>0 && floor_chamfer<af_clearance/2-socket_corner_r*(1/cos(30)-1));
assert(lid_thickness>2*entry_chamfer && socket_depth>2*entry_chamfer);
assert(bolt_clearance_d+2*entry_chamfer<nut_af);
assert(finger_offset-finger_hole_d/2/cos(180/32)-(nut_af+af_clearance)/sqrt(3)>2);
module socket_profile() {
    // Round hex vertices locally; straight drive flats keep the specified AF.
    offset(r=socket_corner_r,$fn=24) offset(delta=-socket_corner_r)
        ef_hex(nut_af+af_clearance);
}
module nut_pocket() {
    // Floor-root bevel stays within the nut clearance, preserving a flat seat.
    hull() {
        translate([0,0,lid_thickness]) linear_extrude(0.01)
            offset(delta=-floor_chamfer) socket_profile();
        translate([0,0,lid_thickness+floor_chamfer]) linear_extrude(0.01) socket_profile();
    }
    translate([0,0,lid_thickness+floor_chamfer])
        linear_extrude(socket_depth+0.1) socket_profile();
    hull() {
        translate([0,0,body_height-entry_chamfer]) linear_extrude(0.01) socket_profile();
        translate([0,0,body_height]) linear_extrude(0.1)
            offset(delta=entry_chamfer) socket_profile();
    }
}
difference() {
    ef_convex_profile(body_height,edge_chamfer)
        rotate(90) ef_capsule(grip_width,grip_length);
    nut_pocket();
    // Only the bolt crosses the lid; the 10 mm nut cannot pass this opening.
    ef_poly_bore(bolt_clearance_d,lid_thickness,0.3,32);
    for(x=[-finger_offset,finger_offset]) translate([x,0,0])
        ef_poly_bore(finger_hole_d,body_height,edge_chamfer,32);
}
