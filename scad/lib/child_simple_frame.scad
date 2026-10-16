// Simple vertical WTE4 enclosure. mm; +Y front; tube bottom z=0.
// Shared geometry: all interfaces are defined here, never in the wrappers.
// 2026-09-16 r2: shoulder-supported guard, exposed M3 nuts; no captive inserts.

/* [Vessel] */
tube_od = 114.3;
tube_length = 200;
eva_thickness = 2;
eva_compression = 0.8;
cap_od = 120.3;
cap_bottom = -13.8;
cap_top = -8;
flange_exposed = 8;
// Provisional: clearance accommodates both historic 114.3 and 120.3 rings.
dome_ring_clearance_od = 120.3;
dome_ring_height = 6.5;
dome_neck_radius = 49;
radial_clearance = 0.75;
axial_clearance = 0.5;
lip_thickness = 4;

/* [Frame] */
outer_radius = 70;
side_strip_x = 54;
center_spine_width = 20;
middle_z = 100;
middle_band_height = 16;
bottom_band_top = 14;
top_band_start_offset = -4;
ear_x = 77;
ear_width = 18;
ear_depth = 10;
join_z = [20,180];
join_ear_height = 24;
lift_hole_d = 10;
lift_z = 208;
lift_ear_depth = 20;

/* [M3 attachment interface] */
// Interface specification: docs/child_simple_mount_interface.md
// CHILD-SIMPLE-M3-40x40 Rev.1; update specification with any interface change.
m3_clearance_d = 3.45;
mount_pitch = 40;
mount_width = 60;
mount_height = 60;
mount_thickness = 8;
mount_inner_y = 74;
mount_rib_inner_x = 26;
mount_rib_thickness = 8;
mount_rib_start_y = 44;
front_mount_z = 100;
rear_mount_z = 190;
rear_light_mount_z = 100; // r3: user-confirmed M3 40x40 future light bracket
hardware_seat_radius = 3.5;

/* [Lower cable guard] */
guard_bottom = -85;
guard_rail = 20;
guard_half_depth = 84;
guard_post_inner_x = 90;
guard_post_width = 20;
guard_tab_inner_x = 54;
guard_tab_inner_y = 17;
guard_tab_depth = 16;
guard_tongue_depth = 12;
guard_tab_bottom = -19;
guard_tab_top = 12;
guard_bolt_z = [-7,5];
tie_slot_width = 5;
tie_slot_height = 3;
tie_slot_z = [-52,-42];

/* [Hidden] */
$fn = 96;
eps = 0.02;
inner_radius = tube_od/2 + eva_thickness - eva_compression;
bottom_pocket_z0 = cap_bottom-axial_clearance;
bottom_pocket_z1 = cap_top+axial_clearance;
top_pocket_z0 = tube_length+flange_exposed-axial_clearance;
top_pocket_z1 = tube_length+flange_exposed+dome_ring_height+axial_clearance;
frame_bottom = bottom_pocket_z0-lip_thickness;
frame_top = top_pocket_z1+lip_thickness;
frame_height = frame_top-frame_bottom;
side_outer_x = ear_x+ear_width/2;
guard_half_width = guard_post_inner_x+guard_post_width;
guard_interface_y = guard_tab_inner_y+guard_tab_depth;
guard_post_outer_y = guard_interface_y+guard_tongue_depth;
guard_bolt_x = guard_post_inner_x+guard_post_width/2;
guard_post_y = (guard_tab_inner_y+guard_post_outer_y)/2;
guard_holes = [for(z=guard_bolt_z) [guard_bolt_x,z,hardware_seat_radius]];
mount_holes = [for(x=[-mount_pitch/2,mount_pitch/2],z=[-mount_pitch/2,mount_pitch/2]) [x,z,hardware_seat_radius]];

assert(inner_radius < cap_od/2-1, "Bottom lip needs radial overlap");
assert(dome_neck_radius > 47.25+1, "Dome reference requires clearance");
assert(dome_neck_radius < 114.3/2-4, "Top lip must catch smaller dome ring");
assert(outer_radius > cap_od/2+radial_clearance+6, "Pocket wall too thin");
assert(frame_height < 250 && 2*guard_half_width < 250 && 2*guard_half_depth < 250, "X1C envelope");
assert(mount_inner_y-outer_radius >= hardware_seat_radius, "Rear nut clearance");
assert(mount_rib_inner_x > mount_pitch/2+hardware_seat_radius+1, "Mount hole/tool intersects rib");
assert(mount_rib_inner_x+mount_rib_thickness < mount_width/2+5, "Rib must overlap pad");
assert(guard_bolt_x-hardware_seat_radius > side_outer_x+5, "Guard nut/tool must be outside the frame side rails");
assert(guard_post_outer_y+5 < guard_half_depth-guard_rail, "Post clear of front/back bottom rail");
assert(guard_tab_bottom < frame_bottom+1 && guard_tab_bottom > guard_bottom+guard_rail+20, "Guard shoulder height");
for(h=guard_holes) {
    assert(h[0]-5 > guard_post_inner_x && h[0]+5 < guard_half_width, "Guard tool edge clearance");
    assert(h[1]-h[2] > guard_tab_bottom+3 && h[1]+h[2] < guard_tab_top-3, "Guard bolt edge clearance");
}
for(i=[0:len(guard_holes)-1],j=[0:len(guard_holes)-1])
    if(j>i) assert(abs(guard_holes[i][1]-guard_holes[j][1]) >= 12, "Guard tools overlap");
for(h=mount_holes) {
    assert(abs(h[0])+h[2]+4 <= mount_width/2, "Mount X edge margin");
    assert(abs(h[1])+h[2]+4 <= mount_height/2, "Mount Z edge margin");
}
for(i=[0:len(mount_holes)-1],j=[0:len(mount_holes)-1])
    if(j>i) assert(norm([mount_holes[i][0]-mount_holes[j][0],mount_holes[i][1]-mount_holes[j][1]]) > mount_holes[i][2]+mount_holes[j][2]+2, "Hardware collision");

// Circumscribed functional hole; true flats >= requested clearance.
module hole(d,h) { cylinder(r=d/2/cos(180/24),h=h,$fn=24); }
module y_hole(x,y,z,d,h) { translate([x,y,z]) rotate([-90,0,0]) hole(d,h); }
module x_hole(x,y,z,d,h) { translate([x,y,z]) rotate([0,90,0]) hole(d,h); }
module block(x0,x1,y0,y1,z0,z1) { translate([x0,y0,z0]) cube([x1-x0,y1-y0,z1-z0]); }

module vessel_void() {
    translate([0,0,frame_bottom-1]) cylinder(r=inner_radius,h=top_pocket_z1-frame_bottom+1);
    translate([0,0,bottom_pocket_z0]) cylinder(r=cap_od/2+radial_clearance,h=bottom_pocket_z1-bottom_pocket_z0);
    translate([0,0,top_pocket_z0]) cylinder(r=dome_ring_clearance_od/2+radial_clearance,h=top_pocket_z1-top_pocket_z0);
    translate([0,0,top_pocket_z1-eps]) cylinder(r=dome_neck_radius,h=lip_thickness+2);
}
module positive_half_band(z0,z1) {
    intersection() {
        translate([0,0,z0]) cylinder(r=outer_radius,h=z1-z0);
        block(-outer_radius,outer_radius,0,outer_radius,z0-eps,z1+eps);
    }
}

module half_positive(mount_z, extra_mounts=[]) {
    difference() {
        union() {
            positive_half_band(frame_bottom,bottom_band_top);
            positive_half_band(middle_z-middle_band_height/2,middle_z+middle_band_height/2);
            positive_half_band(tube_length+top_band_start_offset,frame_top);
            // Two continuous side rails connect the three retaining bands.
            intersection() {
                positive_half_band(frame_bottom,frame_top);
                union() {
                    for(s=[-1,1]) scale([s,1,1]) block(side_strip_x,outer_radius,0,outer_radius,frame_bottom,frame_top);
                    block(-center_spine_width/2,center_spine_width/2,0,outer_radius,frame_bottom,frame_top);
                }
            }
            for(s=[-1,1]) scale([s,1,1]) {
                for(z=join_z) block(side_strip_x,side_outer_x,0,ear_depth,z-join_ear_height/2,z+join_ear_height/2);
                block(side_strip_x,side_outer_x,0,lift_ear_depth,lift_z-12,frame_top);
                block(guard_tab_inner_x,guard_half_width,guard_tab_inner_y,guard_interface_y,guard_tab_bottom,guard_tab_top);
                for(mz=concat([mount_z],extra_mounts))
                    block(mount_rib_inner_x,mount_rib_inner_x+mount_rib_thickness,mount_rib_start_y,mount_inner_y+mount_thickness,mz-mount_height/2,mz+mount_height/2);
            }
            for(mz=concat([mount_z],extra_mounts))
                block(-mount_width/2,mount_width/2,mount_inner_y,mount_inner_y+mount_thickness,mz-mount_height/2,mz+mount_height/2);
        }
        vessel_void();
        for(s=[-1,1]) {
            for(z=join_z) y_hole(s*ear_x,-eps,z,m3_clearance_d,ear_depth+2*eps);
            y_hole(s*ear_x,-eps,lift_z,lift_hole_d,lift_ear_depth+2*eps);
        }
        for(mz=concat([mount_z],extra_mounts),h=mount_holes)
            y_hole(h[0],mount_inner_y-eps,mz+h[1],m3_clearance_d,mount_thickness+2*eps);
        // Exposed through bolts: insert/remove nuts with the vessel installed.
        for(s=[-1,1],z=guard_bolt_z)
            y_hole(s*guard_bolt_x,guard_tab_inner_y-eps,z,m3_clearance_d,guard_tab_depth+2*eps);
    }
}
module child_simple_front() { half_positive(front_mount_z); }
module child_simple_rear() { mirror([0,1,0]) half_positive(rear_mount_z,[rear_light_mount_z]); }

module child_simple_guard() {
    difference() {
        union() {
            difference() {
                block(-guard_half_width,guard_half_width,-guard_half_depth,guard_half_depth,guard_bottom,guard_bottom+guard_rail);
                block(-guard_post_inner_x,guard_post_inner_x,-guard_half_depth+guard_rail,guard_half_depth-guard_rail,guard_bottom-1,guard_bottom+guard_rail+1);
            }
            for(s=[-1,1],t=[-1,1]) scale([s,t,1]) {
                // Full post supports the frame's underside at z=-19.
                block(guard_post_inner_x,guard_half_width,guard_tab_inner_y,guard_post_outer_y,guard_bottom,guard_tab_bottom);
                // Upper tongue overlaps the outside of the frame tab.
                block(guard_post_inner_x,guard_half_width,guard_interface_y,guard_post_outer_y,guard_bottom,guard_tab_top);
            }
        }
        for(s=[-1,1],t=[-1,1],z=guard_bolt_z)
            scale([1,t,1]) y_hole(s*guard_bolt_x,guard_interface_y-eps,z,m3_clearance_d,guard_tongue_depth+2*eps);
        for(y=[-guard_post_y,guard_post_y],z=tie_slot_z)
            block(-guard_half_width-1,guard_half_width+1,y-tie_slot_width/2,y+tie_slot_width/2,z-tie_slot_height/2,z+tie_slot_height/2);
    }
}
