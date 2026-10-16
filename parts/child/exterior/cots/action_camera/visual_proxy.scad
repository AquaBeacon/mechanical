// DJI Osmo Action 6 + waterproof case: appearance / envelope proxy only.
// Dimensions and measured mounting-tab data are transcribed from action_camera.md.
// The actual manufacturer geometry is unavailable; this is not a fit-certified model.

$fn = 64;
$fa = 4;
$fs = 0.35;

/* [Envelope (mm)] */
case_w = 94.7;             // nominal X: baseline / lateral direction
case_d = 45.9;             // nominal Y: lens-to-rear direction
case_h = 84.1;             // nominal overall Z envelope, interpreted as tab-inclusive
case_corner_r = 6;         // provisional appearance radius; not measured
body_h = 75;               // provisional shell height used by existing mount proxy
body_bottom_z = case_h - body_h;

/* [Lens (mm)] */
lens_axis_z = 52;           // provisional value already used by child_osmo_holder
lens_r = 16;                // appearance proxy from visual_proxy.json
lens_rim_r = 19;            // provisional cosmetic bezel
lens_rim_depth = 1.2;       // provisional cosmetic bezel
body_d = case_d - lens_rim_depth;
body_center_y = -lens_rim_depth/2;

/* [Measured bottom interface (mm)] */
tab_t = 3;                  // measured thickness along X
tab_gap = 3;                // measured clear gap between inner faces
tab_hole_d = 5;             // measured hole diameter
tab_hole_z = 12.5;          // interpreted from lowest overall Z plane
tab_span_y = 18;            // provisional tab width along Y; measure on the case
tab_overlap = 0.5;          // overlap into shell to make a fused proxy

/* [Display] */
show_case = true;

eps = 0.02;
tab_pitch_x = tab_t + tab_gap;

assert(case_corner_r > 0 && case_corner_r < min(case_w, case_d)/2);
assert(body_h > 2*case_corner_r && body_bottom_z >= 0);
assert(tab_hole_d < tab_span_y && tab_hole_z > tab_hole_d/2);
assert(abs(body_bottom_z + body_h - case_h) < 0.001);

// Rounded envelope with exact outside dimensions.
module rounded_body(w, d, h, r) {
    minkowski() {
        translate([-(w-2*r)/2, -(d-2*r)/2, r])
            cube([w-2*r, d-2*r, h-2*r]);
        sphere(r=r);
    }
}

module bottom_tabs() {
    for (sx = [-1, 1]) {
        translate([sx*tab_pitch_x/2-tab_t/2, -tab_span_y/2, 0])
            cube([tab_t, tab_span_y,
                  tab_hole_z+tab_hole_d/2+tab_overlap]);
    }
}

module lens_bezel() {
    // Camera faces +Y. The bezel and glass reach, but do not exceed, the envelope.
    translate([0, case_d/2-lens_rim_depth-eps, lens_axis_z])
        rotate([-90, 0, 0])
            cylinder(r=lens_rim_r, h=lens_rim_depth+eps);
    translate([0, case_d/2-0.8-eps, lens_axis_z])
        rotate([-90, 0, 0])
            cylinder(r=lens_r, h=0.8+eps);
}

module case_proxy() {
    difference() {
        union() {
            translate([0, body_center_y, body_bottom_z])
                rounded_body(case_w, body_d, body_h, case_corner_r);
            bottom_tabs();
            lens_bezel();
        }
        // Coaxial screw holes through both 3 mm tabs; use measured nominal Ø5.
        translate([-tab_pitch_x-tab_t, 0, tab_hole_z])
            rotate([0, 90, 0])
                cylinder(d=tab_hole_d, h=2*(tab_pitch_x+tab_t), center=false);
    }
}

if (show_case) color("SteelBlue") case_proxy();
