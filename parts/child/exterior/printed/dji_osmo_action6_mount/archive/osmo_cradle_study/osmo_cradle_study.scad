// DESIGN STUDY: no field use or final fit claim. mm. +Y lens/front, +Z up.
// Contact locations and case envelope are provisional, tab dimensions measured.
part = "assembly"; // [assembly,base,receiver,pad]
show_case = true;
case_w = 95;
case_d = 45.9; // nominal, not measured
case_h = 75; // approximate sketch, not precision measurement
body_to_axis = 12.5;
tab_t = 3;
tab_gap = 3;
case_hole = 5;
fit = 0.3;
base_t = 6;
base_w = 104;
base_d = 54;
axis_z = 20;
pad_w = 12;
pad_d = 6;
shim = 0.3; // initial gap below ideal body; replace with measured hard shim
pad_xy = [[-30,19],[30,19],[0,-19]]; // provisional: avoid rear hinge
lug_r = 7;
lower_t = 6;
upper_t = 3;
nut_af = 8.2;
nut_depth = 4.2;
$fn = 48;
eps = 0.02;
middle_t = tab_gap-fit;
slot = tab_t+fit;
stack = lower_t+2*slot+middle_t+upper_t;
body_z = axis_z+body_to_axis;
pad_h = body_z-base_t-shim;
receiver_w = 30;
receiver_d = 30;
receiver_fix_y = 11;
receiver_fix_x = 11;
assert(middle_t>0 && shim>=0 && pad_h>0);
assert(nut_depth<lower_t-1);
assert(body_to_axis>lug_r);
for(p=pad_xy) {
    assert(abs(p[0])+pad_w/2<base_w/2);
    assert(abs(p[1])+pad_d/2<base_d/2);
    assert(abs(p[0])>receiver_w/2+pad_w/2 || abs(p[1])-pad_d/2>receiver_d/2,
           "Pad overlaps receiver footprint");
}
module hole(d,h) { cylinder(d=d/cos(180/32),h=h,$fn=32); }
module fixing_holes(h) {
    for(x=[-receiver_fix_x,receiver_fix_x],y=[-receiver_fix_y,receiver_fix_y])
        translate([x,y,-eps]) hole(3.4,h+2*eps);
}
module base() {
    difference() {
        translate([-base_w/2,-base_d/2,0]) cube([base_w,base_d,base_t]);
        fixing_holes(base_t);
        for(p=pad_xy) translate([p[0],p[1],-eps]) hole(3.4,base_t+2*eps);
        // Provisional bridge mounting, same nominal 22 x 32 pattern as existing mount.
        for(x=[-11,11],y=[-16,16]) translate([x,y,-eps]) hole(5.4,base_t+2*eps);
    }
}
module pad() {
    difference() {
        translate([-pad_w/2,-pad_d/2,0]) cube([pad_w,pad_d,pad_h]);
        // Blind pilot; fastening choice remains provisional. Not a modeled metal thread.
        translate([0,0,-eps]) hole(2.7,10);
    }
}
module receiver() {
    // Horizontal screw axis X. Set body tabs symmetrically around x=0.
    left = -(slot+middle_t/2+lower_t);
    starts = [left,-middle_t/2,middle_t/2+slot];
    thick = [lower_t,middle_t,upper_t];
    difference() {
        union() {
            translate([-receiver_w/2,-receiver_d/2,0]) cube([receiver_w,receiver_d,4]);
            for(i=[0:2]) {
                translate([starts[i],-lug_r,0]) cube([thick[i],2*lug_r,axis_z-base_t]);
                translate([starts[i],0,axis_z-base_t]) rotate([0,90,0]) cylinder(r=lug_r,h=thick[i]);
            }
        }
        translate([left-eps,0,axis_z-base_t]) rotate([0,90,0]) hole(case_hole+0.2,stack+2*eps);
        translate([left-eps,0,axis_z-base_t]) rotate([0,90,0])
            cylinder(d=nut_af/cos(30),h=nut_depth+eps,$fn=6);
        fixing_holes(4);
    }
}
if(part=="base") base();
else if(part=="receiver") receiver();
else if(part=="pad") pad();
else {
    color("SlateGray") base();
    color("Orange") translate([0,0,base_t]) receiver();
    for(p=pad_xy) color("SeaGreen") translate([p[0],p[1],base_t]) pad();
    if(show_case) color([0.5,0.75,1,0.22])
        translate([-case_w/2,-case_d/2,body_z]) cube([case_w,case_d,case_h]);
}
