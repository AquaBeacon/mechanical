// DJI genuine Action 6 waterproof case: FIT COUPON ONLY, not a load-bearing mount.
// User measured 2026-09-09: tabs 3, gap 3, bore 5, body bottom to axis 12.5 mm.
/* [Measured case] */
tab_t = 3;
tab_gap = 3;
case_bore = 5;
body_to_axis = 12.5;
/* [Print fit] */
gap_allowance = 0.3;
center_allowance = 0.3;
bore_allowance = 0.2;
/* [Receiver] */
lower_t = 6;
upper_t = 3;
lug_r = 7;
axis_x = 10;
back_t = 4;
// Assumed ordinary M5 nut; verify actual thread pitch and nut before use.
nut_af = 8.2;
nut_depth = 4.2;
/* [Hidden] */
$fn = 64;
eps = 0.02;
middle_t = tab_gap-center_allowance;
slot = tab_t+gap_allowance;
middle_z = lower_t+slot;
upper_z = middle_z+middle_t+slot;
height = upper_z+upper_t;
hole_d = case_bore+bore_allowance;
assert(middle_t > 0 && nut_depth < lower_t-1);
assert(body_to_axis > lug_r);
echo(total_stack=height, nut_entry_from_head=height-nut_depth,
     nominal_body_plane_x=axis_x+body_to_axis);
module lug(z,t) {
    translate([0,0,z]) linear_extrude(t) hull() {
        translate([-back_t,-lug_r]) square([back_t,2*lug_r]);
        translate([axis_x,0]) circle(r=lug_r);
    }
}
difference() {
    union() {
        translate([-back_t,-lug_r,0]) cube([back_t,2*lug_r,height]);
        lug(0,lower_t);
        lug(middle_z,middle_t);
        lug(upper_z,upper_t);
    }
    translate([axis_x,0,-eps])
        cylinder(d=hole_d/cos(180/32),h=height+2*eps,$fn=32);
    translate([axis_x,0,-eps])
        cylinder(d=nut_af/cos(30),h=nut_depth+eps,$fn=6);
}
