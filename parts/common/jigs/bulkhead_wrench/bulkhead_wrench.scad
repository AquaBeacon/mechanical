/* [Reinforcement mm] */
outer_radius = 14;
overlap_radius = 10.20;
side_opening = 16.4;
/* [Handle mm] */
handle_span = 100;
handle_width = 24;
handle_thickness = 16;
edge_bevel = 1;
/* [Hidden] */
$fn = 128;
original_length = 60;
eps = 0.02;
assert(outer_radius > 10.25 && overlap_radius < 10.25);
assert(overlap_radius >= 10.15, "Do not change the original working cavity");
assert(side_opening >= 16.3 && side_opening < 2*overlap_radius);
assert(handle_span >= 2*outer_radius+20 && handle_width >= 20);
assert(handle_thickness > 2*edge_bevel && edge_bevel > 0);
// Capsule handle with 45-degree bevels. All dimensions in mm.
module capsule(w,span) {
    hull() for (y=[-(span-handle_width)/2,(span-handle_width)/2])
        translate([0,y]) circle(d=w);
}
module grip() {
    hull() {
        linear_extrude(eps) capsule(handle_width-2*edge_bevel,handle_span);
        translate([0,0,edge_bevel]) linear_extrude(eps) capsule(handle_width,handle_span);
    }
    translate([0,0,edge_bevel])
        linear_extrude(handle_thickness-2*edge_bevel) capsule(handle_width,handle_span);
    hull() {
        translate([0,0,handle_thickness-edge_bevel-eps]) linear_extrude(eps) capsule(handle_width,handle_span);
        translate([0,0,handle_thickness-eps]) linear_extrude(eps) capsule(handle_width-2*edge_bevel,handle_span);
    }
}
union() {
    // Exact working geometry tessellated from the supplied STEP, not scaled.
    translate([0,0,handle_thickness-16]) import("ref/original_print_orientation.stl");
    // External C sleeve: keeps nut cavity and lateral cable entry open.
    difference() {
        translate([0,0,handle_thickness-eps]) cylinder(r=outer_radius,h=original_length+eps);
        translate([0,0,handle_thickness-2*eps]) cylinder(r=overlap_radius,h=original_length+4*eps);
        translate([0,-side_opening/2,handle_thickness-2*eps])
            cube([outer_radius+eps,side_opening,original_length+4*eps]);
    }
    grip();
    // Solid rear hub spreads the handle load into the cylindrical body.
    cylinder(r=outer_radius,h=handle_thickness);
}
