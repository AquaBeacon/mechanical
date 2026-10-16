// =====================================================================
// child_lcd_cradle.scad — hinged NHD-C0216CiZ LCD door + rear clamps
//
// Print coordinates: X = LCD short side, Y = LCD long side, Z = depth.
// The visible bezel face is on the bed (Z=0), so both variants print without
// support. The left edge has two support-free hinge leaves; a single recessed
// M2.5 screw at the right releases the door for C-MAIN service.
// =====================================================================

include <../../../../../scad/lib/util.scad>;

/* [Output] */
part = 0;                        // [0:bezel,1:clamp]

/* [LCD — Newhaven NHD-C0216CiZ-FSW-FBW-3V3] */
lcd_w = 26.2;                   // short side
lcd_l = 56.8;                   // long side
lcd_body_h = 5.5;
view_w = 14.3;                  // visible area, short side
view_l = 45.7;                  // visible area, long side
fit = 0.6;                      // 0.3 mm per side
foam_t = 0.8;                   // thin closed-cell foam around the front rim

/* [Bezel] */
wall = 3.0;
front_t = 2.0;
pocket_h = lcd_body_h + foam_t + 0.5;
corner_r = 2.0;
hinge_x = -18.5;                // vertical hinge axis, kept inside tube envelope
hinge_pin_d = 3.4;              // M3 threaded rod captured by both LCD support arches (2026-08-28)
hinge_block_w = 6.4;
hinge_block_h = 10.5;
hinge_axis_z = 7.0;
hinge_segments = [[-20.5,-8.0],[8.0,20.5]];   // shortened 2026-08-28 so the rear clamp bars (|y| = clamp_y ± 2.5) clear the leaves

/* [One-screw latch] */
latch_x = 16.5;
latch_clear_d = 2.9;            // M2.5 clearance
latch_head_d = 5.2;             // low-profile head, recessed flush
latch_head_h = 2.2;
latch_boss_d = 5.8;

/* [Rear clamps] */
clamp_w = 5.0;
clamp_t = 2.5;
clamp_screw = 2.5;
clamp_clear_d = 2.9;
clamp_pilot_d = 2.0;
clamp_x = lcd_w/2 + fit/2 + wall/2;
clamp_y = lcd_l/2 - 5.0;        // 23.4: bars press the LCD ends, between the hinge leaves and the plate end
end_wall = wall;
rear_foam_c = 0.5;              // 0.8 closed-cell foam strip under each bar, compressed to 0.5
clamp_seat_h = front_t + foam_t + lcd_body_h + rear_foam_c;     // 8.8 from bezel front (= total_h)
// Bars must stay below the hinge pin (world Y 35.0..38.0): bar top = 43.5-8.8 = 34.7

/* [Fixed-frame knuckle clearance] */
// child_lcd_hinge_frame's centre knuckle (x hinge_x ± 3.2, y ±7.5, world Y 27..40)
// used to cut 1.1 mm into the door plate edge. Notch the plate around it.
knuckle_w = 6.4;
knuckle_y = 7.5;
knuckle_top_world_y = 40.0;     // frame origin 27 + hinge_block_h 13
door_front_world_y = 43.5;
knuckle_clear = 0.3;
notch_x1 = hinge_x + knuckle_w/2 + knuckle_clear;                 // -15.0
notch_z0 = door_front_world_y - knuckle_top_world_y - knuckle_clear;  // 3.2 (print z)

$fa = 4;
$fs = 0.3;

pocket_w = lcd_w + fit;
pocket_l = lcd_l + fit;
outer_w = pocket_w + 2*wall;
outer_l = pocket_l + 2*end_wall;
assert(clamp_y - clamp_w/2 >= hinge_segments[1][1], "clamp bar overlaps the hinge leaves");
assert(clamp_y + clamp_w/2 <= lcd_l/2 + 2, "clamp bar misses the LCD end");
total_h = front_t + pocket_h;

assert(view_w < lcd_w - 2, "LCD window exceeds module short side");
assert(view_l < lcd_l - 2, "LCD window exceeds module long side");
assert(notch_x1 <= -(pocket_w/2) - 1.5, "knuckle notch leaves < 1.5 mm wall beside the LCD pocket");
assert(notch_z0 > front_t, "knuckle notch would cut the front bezel plate");
assert(latch_x-latch_clear_d/2 > pocket_w/2+1.5,
       "Latch hole leaves too little wall beside the LCD pocket");

module hinge_leaf(y0,y1) {
    // A 45-degree ramp grows the leaf outwards without a support island.
    union() {
        hull() {
            translate([hinge_x-1.8,y0,0]) cube([3.2,y1-y0,0.01]);
            translate([hinge_x-hinge_block_w/2,y0,5.0])
                cube([hinge_block_w,y1-y0,0.01]);
        }
        translate([hinge_x-hinge_block_w/2,y0,5.0])
            cube([hinge_block_w,y1-y0,hinge_block_h-5.0]);
    }
}

module rounded_plate(w, l, h, r=2) {
    translate([-w/2, -l/2, 0]) rrect_prism(w, l, h, r);
}

module bezel() {
    difference() {
        union() {
            rounded_plate(outer_w, outer_l, total_h, corner_r);
            for (seg=hinge_segments) hinge_leaf(seg[0],seg[1]);
            translate([latch_x,0,0]) cylinder(d=latch_boss_d,h=total_h,$fn=32);
            // Four pilots for the removable rear clamp bars, confined to the plate
            // outline so they cannot reach the hinge rod (x < -16.4).
            intersection() {
                union() for (sx=[-1,1], sy=[-1,1])
                    translate([sx*clamp_x, sy*clamp_y, front_t])
                        cylinder(d=wall+clamp_pilot_d+1.6, h=clamp_seat_h-front_t, $fn=32);
                translate([-outer_w/2, -outer_l/2, -1]) cube([outer_w, outer_l, total_h+2]);   // plain cube keeps the STEP clean
            }
        }

        // LCD pocket opens from the rear, leaving the visible front bezel.
        translate([-pocket_w/2, -pocket_l/2, front_t])
            cube([pocket_w, pocket_l, pocket_h+0.2]);
        translate([-view_w/2, -view_l/2, -0.1])
            cube([view_w, view_l, front_t+0.2]);

        // Clamp screws enter from the rear; blind pilots retain material at face.
        for (sx=[-1,1], sy=[-1,1])
            translate([sx*clamp_x, sy*clamp_y, front_t+1.0])
                hole(clamp_pilot_d, pocket_h, fn=8, through=false);

        // Notch for the fixed frame's centre knuckle (between the two door leaves).
        translate([-outer_w/2-1, -knuckle_y-knuckle_clear, notch_z0])
            cube([notch_x1-(-outer_w/2-1), 2*(knuckle_y+knuckle_clear), total_h]);

        // M3 hinge pin. The pointed top faces +Z in the flat print orientation.
        for (seg=hinge_segments)
            translate([hinge_x,seg[0]-0.1,hinge_axis_z])
                rotate([0,0,90]) teardrop_bore(hinge_pin_d,seg[1]-seg[0]+0.2);

        // One recessed M2.5 screw releases the complete LCD door. Fit a small
        // O-ring on the rear of its shank after assembly to make it captive.
        translate([latch_x,0,-0.1]) hole(latch_clear_d,total_h+0.2,fn=8);
        translate([latch_x,0,-0.1]) hole(latch_head_d,latch_head_h+0.1,fn=12);
    }
}

module clamp_bar(sy) {
    difference() {
        translate([-outer_w/2-2, sy*(clamp_y-clamp_w/2), 0])
            cube([outer_w+4, clamp_w, clamp_t]);
        for (sx=[-1,1])
            translate([sx*clamp_x, sy*clamp_y, -0.1])
                hole(clamp_clear_d, clamp_t+0.2, fn=8);
    }
}

// One bar centred on its own axis (for assembly placement at y = ±clamp_y).
module clamp_bar_single() {
    difference() {
        translate([-outer_w/2-2, -clamp_w/2, 0]) cube([outer_w+4, clamp_w, clamp_t]);
        for (sx=[-1,1])
            translate([sx*clamp_x, 0, -0.1]) hole(clamp_clear_d, clamp_t+0.2, fn=8);
    }
}

echo(str("child_lcd_cradle: clamp bar seat z=", clamp_seat_h, " clamp_y=±", clamp_y,
         " clamp_x=±", clamp_x, " notch x<=", notch_x1, " z>=", notch_z0));

if (part == 0) bezel();
else if (part == 2) clamp_bar_single();
else if (part == 1) {
    // One STL intentionally contains both identical bars; print one build plate.
    translate([0, -8, 0]) clamp_bar(1);
    translate([0,  8, 0]) clamp_bar(-1);
}
