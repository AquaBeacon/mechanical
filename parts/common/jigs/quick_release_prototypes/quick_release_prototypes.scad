// Reusable trial interfaces, mm. Authoritative geometry; no rated load.
use <../../../../scad/lib/util.scad>
/* [Output] */
part = "slide_male"; // [slide_male,slide_female,slide_gib,snap_male,snap_female,twist_male,twist_male_mount,twist_female,knob,twist_knob]
/* [Common interface - provisional] */
pad = 40;
pad_t = 4;
mount_pitch = 32;
mount_d = 3.45;
gap = 0.30; // per-side fit allowance
edge_relief = 0.35;
touch_fillet = 0.8; // exposed upper edges; keep flat print/mounting faces
plate_corner_r = 3;
/* [Metal hardware - measure before printing] */
bolt_nominal = 3;
slide_bolt_length = 40;
twist_bolt_length = 40;
thread_pitch = 0.5;
unlock_turns = 3;
bolt_d = bolt_nominal + 0.45;
hex_af = 5.75; // M3 head/nut nominal AF5.5, +0.25
head_seat = 3.8; // knob bearing face to underside of bolt HEAD
slide_nut_x = -16.5;
twist_nut_x = -15.5;
nut_loading_clearance = 0.15;
washer_d = 7;
washer_id = 3.2;
washer_t = 0.5;
metal_af = 5.5;
metal_nut_t = 2.4;
metal_head_h = 2.12;
knob_d = 22;
knob_h = 10;
/* [Dovetail] */
slide_plate_t = 10; // thicker upper mounting plate clears the D22 knob
rail_l = 20;
rail_neck = 14;
rail_head = 22;
rail_h = 6;
slide_floor = 9; // raises the knob swept envelope above the mounting plane
slide_cheek_x = -14;
slide_gib_x = 18;
slide_preload_x = gap*(1+(rail_head-rail_neck)/(2*rail_h));
slide_opening = 1.0;
slide_slot_d = 4.0;
/* [Side release] */
arm_l = 36;
arm_t = 1.4;
arm_x = 9;
snap_t = 4;
snap_floor = 3;
snap_inner = 22.6;
snap_wall = 2.5;
snap_roof = 2.4;
hook_out = 15.3;
hook_back = 15.3;
hook_ramp = 19;
snap_entry = -12;
snap_end = 27;
snap_tab_l = 12;
snap_seat_y = -0.15;
/* [Bayonet] */
twist_plate_t = 6; // upper mounting plate, female base remains 4 mm
post_d = 14;
post_h = 8;
lug_r = 10.5;
lug_w = 6;
lug_t = 3;
ring_d = 28;
ring_h = 14;
turn_deg = 60;
entry_angle = 80;
twist_face_x = 20; // through bolt runs from the left cheek to the right knob
twist_axis_z = 14;
twist_knob_d = 16; // keep the entire side knob below the upper mounting plane
twist_cam_lift = 0.60; // axial draw over the 60-degree turn
twist_pad_t = 1.0; // user-confirmed rubber thickness; not a printed part
twist_pad_depth = 0.40; // shallow male-side pocket retains 40% of rubber thickness
twist_pad_side_clearance = 0.20; // each side of the 5 x 8 mm rubber cut
twist_pad_compression = 0.10; // provisional nominal squeeze
twist_lock_gap = twist_pad_t-twist_pad_depth-twist_pad_compression;
twist_pad_w = 5.0; // X/radial cut width
twist_pad_l = 8.0; // Y/tangential cut length
twist_pad_r = 10.5; // centres of two rectangular pads on male underside
/* [Hidden] */
$fn = 64;
eps = 0.02;
slide_z = slide_plate_t + slide_floor + rail_h + gap;
slide_axis_z = slide_floor + rail_h/2;
track_floor = pad_t + ring_h - post_h;
twist_z = pad_t + ring_h + twist_plate_t + twist_lock_gap;
snap_socket_h = snap_floor + snap_t + 2*gap + snap_roof;
assert(gap > 0 && gap < 0.8);
assert(rail_head > rail_neck && rail_head/2+gap < pad/2-2);
assert(hex_af > metal_af && knob_h-head_seat >= metal_head_h);
assert(slide_nut_x-nut_loading_clearance > -pad/2+2);
assert(twist_nut_x-nut_loading_clearance > -pad/2+2);
assert(slide_z-gap-slide_axis_z-knob_d/2 >= 1);
assert(thread_pitch*unlock_turns >= slide_opening);
assert(twist_axis_z+4 <= pad_t+ring_h);
assert(twist_axis_z+twist_knob_d/2 < twist_z);
assert(hook_out > snap_inner/2 && arm_x-arm_t/2 > 5);
assert(ring_d/2 > sqrt(pow(lug_r+gap,2)+pow(lug_w/2+gap,2))+2);
assert(twist_pad_depth > 0 && twist_pad_depth < twist_pad_t);
assert(twist_pad_compression > 0 && twist_pad_compression < twist_pad_t*0.15);
assert(twist_lock_gap > 0);
assert(twist_pad_r-twist_pad_w/2-twist_pad_side_clearance > post_d/2+0.5);
assert(sqrt(pow(twist_pad_r+twist_pad_w/2+twist_pad_side_clearance,2)+pow(twist_pad_l/2+twist_pad_side_clearance,2)) < ring_d/2-0.1);
function twist_cam_height(a) = track_floor+lug_t+twist_lock_gap+twist_cam_lift*(1-a/turn_deg);
function twist_draw_offset(angle) = twist_cam_lift*min(1,max(0,-angle/turn_deg));

module mounting_holes(y0=0, y_pitch=mount_pitch, thickness=pad_t) {
    for(x=[-mount_pitch/2,mount_pitch/2],y=[y0-y_pitch/2,y0+y_pitch/2])
        translate([x,y,-eps]) hole(mount_d,thickness+2*eps,fn=12);
}
module pad_blank(y0=0, thickness=pad_t) {
    translate([-pad/2,y0-pad/2,0]) touch_box(pad,pad,thickness,plate_corner_r);
}
// Quarter-circle top fillet, using convex loft segments instead of a costly
// global Minkowski operation that would alter holes and mating surfaces.
module touch_box(w,d,h,r=1,fillet=touch_fillet) {
    f=min(fillet,h/3,r);
    translate([0,0,f]) rrect_prism(w,d,h-2*f,r);
    // Lower fillet is trimmed at 45 degrees into a bed chamfer. This keeps
    // layer growth <= layer height instead of the steep start of a full fillet.
    hull() {
        inset=max(edge_relief,f*(2-sqrt(2)));
        translate([inset,inset,0]) rrect_prism(w-2*inset,d-2*inset,eps,max(0.1,r-inset));
        inset2=f*(1-cos(45));
        translate([inset2,inset2,f*(1-sin(45))])
            rrect_prism(w-2*inset2,d-2*inset2,eps,max(0.1,r-inset2));
    }
    for(a=[0:15:30]) hull() for(t=[a,a+15]) {
        inset=f*(1-cos(t));
        translate([inset,inset,f*(1-sin(t))])
            rrect_prism(w-2*inset,d-2*inset,eps,max(0.1,r-inset));
    }
    for(a=[0:15:75]) hull() for(t=[a,a+15]) {
        inset=f*(1-cos(t));
        translate([inset,inset,h-f+f*sin(t)-eps])
            rrect_prism(w-2*inset,d-2*inset,eps,max(0.1,r-inset));
    }
}
module hex_cut(depth) {
    rotate([0,0,30]) cylinder(r=hex_af/sqrt(3),h=depth,$fn=6);
}
// Horizontal screw bore: round part + upward 45-degree roof relief.
module x_bore(length) {
    roof_tip = (bolt_d/2)/cos(180/16)*sqrt(2);
    rotate([0,90,0]) hole(bolt_d,length,fn=16);
    translate([0,-roof_tip,0]) rotate([0,90,0])
        linear_extrude(length) polygon([[0,0],[-roof_tip,roof_tip],[0,2*roof_tip]]);
}
// Recessed nut receiver: no external clip; continuous body within the pad footprint.
// Upward loading channel has no roof and therefore needs no internal support.
module fixed_nut_blank(z_axis) {
    translate([-pad/2,-5,pad_t-eps]) touch_box(pad/2-12,10,z_axis+4-pad_t+eps,1);
}
module fixed_nut_cuts(nut_x,z_axis) {
    translate([nut_x-nut_loading_clearance,0,z_axis]) rotate([0,90,0])
        hex_cut(metal_nut_t+nut_loading_clearance);
    translate([nut_x-nut_loading_clearance,-hex_af/sqrt(3),z_axis])
        cube([metal_nut_t+nut_loading_clearance,2*hex_af/sqrt(3),4+eps]);
}
module hand_knob(diameter=knob_d) {
    difference() {
        union() {
            rounded_knob_cylinder(diameter-3);
            for(a=[0:60:300]) rotate([0,0,a]) translate([(diameter-5)/2,0,0]) rounded_knob_cylinder(5);
        }
        translate([0,0,-eps]) hole(bolt_d,knob_h+2*eps,fn=16);
        // Bolt head bears on a 3.8 mm floor. Hex shape transmits torque.
        // A small adhesive spot keeps the head with the knob when removed.
        translate([0,0,head_seat]) hex_cut(knob_h-head_seat+eps);
    }
}
module rounded_knob_cylinder(d) {
    cylinder(d=d,h=knob_h-touch_fillet);
    for(a=[0:15:75]) hull() for(t=[a,a+15])
        translate([0,0,knob_h-touch_fillet+touch_fillet*sin(t)-eps])
            cylinder(d=d-2*touch_fillet*(1-cos(t)),h=eps);
}

// Male is printed pad down. Closed assembly flips it over the female.
module rail_profile(extra=0) {
    polygon([[-rail_neck/2-extra,slide_plate_t], [rail_neck/2+extra,slide_plate_t],
             [rail_head/2+extra,slide_plate_t+rail_h],[-rail_head/2-extra,slide_plate_t+rail_h]]);
}
module slide_male() {
    difference() {
        union() {
            pad_blank(thickness=slide_plate_t);
            // rotate maps the profile XY to XZ, extrusion along -Y
            translate([0,rail_l/2,0]) rotate([90,0,0]) linear_extrude(rail_l) rail_profile();
        }
        mounting_holes(thickness=slide_plate_t);
        // Open plate notches clear the gib and left head cradle during withdrawal.
        translate([rail_neck/2-gap,-pad/2-eps,-eps]) cube([pad,pad/2+11.3+eps,slide_plate_t+2*eps]);
        translate([-pad+slide_cheek_x+2+slide_preload_x+gap+0.1,-pad/2-eps,-eps]) cube([pad,pad/2+11.3+eps,slide_plate_t+2*eps]);
        // Longitudinal open slot: the through bolt can stay in place when sliding out.
        hull() for(y=[0,-rail_l/2-slide_slot_d])
            translate([-rail_head,y,slide_plate_t+rail_h/2]) rotate([0,90,0])
                hole(slide_slot_d,2*rail_head,fn=24);
    }
}
module slide_female() {
    difference() {
        union() {
            pad_blank();
            translate([-rail_head/2-3,-rail_l/2,pad_t-eps]) touch_box(rail_head+6,rail_l,slide_floor-pad_t+rail_h+eps,1);
            translate([-rail_head/2-3,rail_l/2+gap,pad_t-eps]) touch_box(rail_head+6,3,slide_floor-pad_t+rail_h+eps,1);
            translate([slide_cheek_x,-5,pad_t]) touch_box(2,10,12.2,0.6);
            // Broad recessed fixed-nut receiver, integral with base and left cheek.
            fixed_nut_blank(slide_axis_z);
        }
        mounting_holes();
        // Channel widens downward; the lips provide positive Z retention.
        translate([0,rail_l/2,0]) rotate([90,0,0]) linear_extrude(rail_l+1)
            polygon([[-rail_head/2-gap-gap*(rail_head-rail_neck)/(2*rail_h),slide_floor],
                     [rail_head/2+gap+gap*(rail_head-rail_neck)/(2*rail_h),slide_floor],
                     [rail_neck/2+gap,slide_floor+rail_h+gap],[-rail_neck/2-gap,slide_floor+rail_h+gap]]);
        // Separate moving right flank and its chamfered foot.
        translate([5.8,-rail_l/2-eps,slide_floor]) cube([pad,rail_l+2*eps,rail_h+3]);
        translate([rail_head/2-slide_preload_x-gap,-rail_l/2-eps,pad_t])
            cube([pad,rail_l+2*eps,slide_floor-pad_t]);
        // Clear the lower swept rim of the nut knob; keep all four mounting holes.
        translate([slide_gib_x+washer_t-gap,-knob_d/2-gap,-eps])
            cube([pad,knob_d+2*gap,pad_t+2*eps]);
        translate([-pad,0,slide_axis_z]) x_bore(2*pad);
        fixed_nut_cuts(slide_nut_x,slide_axis_z);
    }
}

// Print with outer X face down: vertical bolt bore and no enclosed roof.
module slide_gib(opening=0) {
    translate([opening,0,0]) difference() {
        translate([0,rail_l/2,0]) rotate([90,0,0]) linear_extrude(rail_l)
            polygon([[rail_head/2-slide_preload_x+0.8,slide_floor-1.2],
                     [slide_gib_x,slide_floor-1.2],[slide_gib_x,slide_floor+rail_h+1.2],
                     [rail_neck/2-slide_preload_x,slide_floor+rail_h+1.2],
                     [rail_neck/2-slide_preload_x,slide_floor+rail_h],
                     [rail_head/2-slide_preload_x,slide_floor]]);
        translate([0,0,slide_axis_z]) x_bore(pad);
    }
}

// Planar cantilevers: squeeze both hooks inward to release.
module snap_male(squeeze=0) {
    difference() {
        union() {
            translate([-pad/2,snap_entry-snap_tab_l,0]) touch_box(pad,snap_tab_l,snap_t,plate_corner_r);
            translate([-3,snap_entry-eps,0]) cube([6,24+eps,snap_t]);
            for(s=[-1,1]) scale([s,1,1]) {
                // Shear is a kinematic envelope, NOT an elastic FEA solution.
                multmatrix([[1,-squeeze/arm_l,0,squeeze*snap_entry/arm_l],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
                    union() {
                        translate([arm_x-arm_t/2,snap_entry-eps,0]) cube([arm_t,arm_l+eps,snap_t]);
                        linear_extrude(snap_t) polygon([[arm_x-arm_t/2,hook_back], [hook_out,hook_back],
                            [hook_out,hook_ramp],[arm_x+arm_t/2,snap_entry+arm_l], [arm_x-arm_t/2,snap_entry+arm_l]]);
                    }
                translate([arm_x,snap_entry+0.5,0]) cylinder(r=arm_t,h=snap_t);
            }
        }
        for(x=[-mount_pitch/2,mount_pitch/2]) translate([x,snap_entry-snap_tab_l/2,-eps]) hole(mount_d,snap_t+2*eps,fn=12);
    }
}
module snap_female() {
    difference() {
        union() {
            // Rear edge aligned with socket rear: mouth-up printing has a flat foot.
            translate([-pad/2,snap_entry,0]) touch_box(pad,snap_end-snap_entry,snap_floor,plate_corner_r);
            translate([-snap_inner/2-snap_wall,snap_entry,0])
                touch_box(snap_inner+2*snap_wall,snap_end-snap_entry,snap_socket_h,1);
        }
        translate([-snap_inner/2,snap_entry-eps,snap_floor]) cube([snap_inner,snap_end-snap_entry-2+eps,snap_t+2*gap]);
        for(s=[-1,1]) scale([s,1,1]) translate([snap_inner/2-eps,hook_back-gap,snap_floor-gap])
            cube([snap_wall+2*eps,snap_end-2-(hook_back-gap),snap_t+4*gap]);
        for(x=[-mount_pitch/2,mount_pitch/2],y=[snap_entry+4,snap_end-4]) {
            translate([x,y,-eps]) hole(mount_d,snap_floor+2*eps,fn=12);
            // Access for M3 heads at the edge of the socket side wall.
            translate([x,y,snap_floor]) hole(6.3,snap_socket_h,fn=24);
        }
    }
}

module twist_lugs(extra=0,phase=0) {
    for(a=[phase,phase+180]) rotate([0,0,a]) translate([post_d/2-1,-lug_w/2-extra,0])
        union() {
            cube([lug_r-post_d/2+1+extra,lug_w+2*extra,lug_t+2*extra]);
            translate([0,lug_w+2*extra,0]) rotate([90,0,0]) linear_extrude(lug_w+2*extra)
                polygon([[0,0],[2.5+extra,0],[1,-1.5]]);
        }
}
module twist_track_profile(extra=gap) {
    for(a=[entry_angle,entry_angle+180]) rotate(a)
        translate([post_d/2-1,-lug_w/2-extra])
            square([lug_r-post_d/2+1+extra,lug_w+2*extra]);
}
module twist_male() {
    difference() {
        union() {
            pad_blank(thickness=twist_plate_t);
            translate([0,0,twist_plate_t-eps]) cylinder(d=post_d,h=post_h+eps);
            translate([0,0,twist_plate_t+post_h-lug_t]) twist_lugs(phase=-entry_angle-turn_deg);
        }
        mounting_holes(thickness=twist_plate_t);
        // Upward-open shallow seats retain the rectangular rubber on the lid.
        // Square inside corners fit hand-cut pads; no enclosed support surfaces.
        for(s=[-1,1])
            translate([s*twist_pad_r-twist_pad_w/2-twist_pad_side_clearance,
                       -twist_pad_l/2-twist_pad_side_clearance,
                       twist_plate_t-twist_pad_depth])
                cube([twist_pad_w+2*twist_pad_side_clearance,
                      twist_pad_l+2*twist_pad_side_clearance,
                      twist_pad_depth+eps]);
        // Native X flip preserves the horizontal axis when the plates align.
        translate([-post_d,0,twist_z-twist_axis_z]) x_bore(2*post_d);
    }
}
// Mounted C male: recess M3 90-degree flat heads within the 6 mm plate.
// Preserve the original cam, lugs, pad pockets and mating surfaces. Standard
// male remains unchanged. A D5.5 head seats 0.425 mm inside the mating face.
module twist_male_mount() {
    difference() {
        twist_male();
        for(x=[-mount_pitch/2,mount_pitch/2],y=[-mount_pitch/2,mount_pitch/2])
            translate([x,y,twist_plate_t-1.45])
                cylinder(d1=mount_d,d2=mount_d+2*(1.45+eps),h=1.45+eps,$fn=48);
    }
}
module twist_female() {
    difference() {
        union() {
            pad_blank();
            translate([0,0,pad_t-eps]) cylinder(d=ring_d,h=ring_h+eps);
            for(s=[-1,1]) scale([s,1,1])
                translate([ring_d/2-2,-5,pad_t-eps])
                    touch_box(twist_face_x-ring_d/2+2,10,twist_axis_z+3.8-pad_t+eps,1);
            fixed_nut_blank(twist_axis_z);
        }
        mounting_holes();
        translate([0,0,pad_t]) hole(post_d+2*gap,ring_h+eps,fn=64);
        // Entry slots continue down to the circular retaining tracks.
        for(a=[entry_angle,entry_angle+180]) rotate([0,0,a]) translate([0,-lug_w/2-gap,track_floor])
            cube([lug_r+gap,lug_w+2*gap,pad_t+ring_h-track_floor+eps]);
        // Descending cam bearing roof draws the plate towards the four pads.
        // 45-degree gusset clearance remains above the bearing land.
        for(a=[0:3:turn_deg-3],phase=[entry_angle,entry_angle+180]) hull() {
            for(ang=[a+phase,a+3+phase]) rotate([0,0,ang]) {
                ceiling=twist_cam_height(ang-phase);
                translate([0,lug_w/2+gap,0]) rotate([90,0,0])
                    linear_extrude(lug_w+2*gap) polygon([
                        [post_d/2-1,ceiling-lug_t-2*gap],
                        [lug_r+gap,ceiling-lug_t-2*gap],
                        [lug_r+gap,ceiling],
                        [post_d/2+1.5+gap,ceiling],
                        [post_d/2+gap,ceiling+1.5],
                        [post_d/2-1,ceiling+1.5]]);
            }
        }
        // The upper rim stays flat; the pockets are in the male lid.
        translate([-pad,0,twist_axis_z]) x_bore(2*pad);
        fixed_nut_cuts(twist_nut_x,twist_axis_z);
    }
}

// Assembly coordinate transforms; same numbers are recorded in placement.json.
module seated_male(kind="slide",travel=0,angle=0,squeeze=0,clamped=false) {
    if(kind=="slide") translate([clamped ? -slide_preload_x : 0,-travel,slide_z-(clamped ? gap : 0)]) rotate([180,0,0]) slide_male();
    if(kind=="snap") translate([0,snap_seat_y-travel,snap_floor+gap]) snap_male(squeeze);
    if(kind=="twist") translate([0,0,twist_z+twist_draw_offset(angle)+travel]) rotate([0,0,angle]) rotate([180,0,0]) twist_male();
}
// Non-print preview envelopes: the exposed rubber moves with its male-side pocket.
module twist_pad_reference(compressed=true,bearing_margin=0,angle=0,travel=0) {
    h=compressed ? twist_lock_gap : twist_pad_t-twist_pad_depth;
    plate_bottom=pad_t+ring_h+twist_lock_gap+twist_draw_offset(angle)+travel;
    translate([0,0,plate_bottom-h]) rotate([0,0,angle])
        for(s=[-1,1]) translate([s*twist_pad_r-twist_pad_w/2+bearing_margin,-twist_pad_l/2+bearing_margin,bearing_margin])
            cube([twist_pad_w-2*bearing_margin,twist_pad_l-2*bearing_margin,h-2*bearing_margin]);
}

module placed_knob(kind="slide",loosen=0,clamped=true) {
    if(kind=="slide") translate([slide_gib_x+washer_t+loosen,0,slide_axis_z]) rotate([0,90,0]) hand_knob();
    if(kind=="twist") translate([twist_face_x+washer_t+loosen,0,twist_axis_z]) rotate([0,90,0]) hand_knob(twist_knob_d);
}
// Ideal smooth metal envelopes, for fit checks/preview only. Not print outputs.
module metal_washer(bearing_margin=0) {
    difference() { translate([0,0,bearing_margin]) cylinder(d=washer_d,h=washer_t-2*bearing_margin);
        translate([0,0,-eps]) cylinder(d=washer_id,h=washer_t+2*eps); }
}
module nut_reference(bearing_margin=0) {
    difference() { translate([0,0,bearing_margin]) rotate(30) cylinder(r=metal_af/sqrt(3),h=metal_nut_t-bearing_margin,$fn=6);
        translate([0,0,-eps]) cylinder(d=bolt_nominal,h=metal_nut_t+2*eps); }
}
module through_bolt(kind="slide",bearing_margin=0,include_washer=true,loosen=0) {
    face = kind=="slide" ? slide_gib_x : twist_face_x;
    axis = kind=="slide" ? slide_axis_z : twist_axis_z;
    length = kind=="slide" ? slide_bolt_length : twist_bolt_length;
    translate([face+washer_t+head_seat+loosen,0,axis]) {
        rotate([0,-90,0]) cylinder(d=bolt_nominal,h=length);
        rotate([0,90,0]) translate([0,0,bearing_margin]) rotate(30)
            cylinder(r=metal_af/sqrt(3),h=metal_head_h-bearing_margin,$fn=6);
    }
    if(include_washer) translate([face+loosen,0,axis]) rotate([0,90,0]) metal_washer(bearing_margin);
}
module fixed_nut(kind="slide",bearing_margin=0) {
    nut_x = kind=="slide" ? slide_nut_x : twist_nut_x;
    axis = kind=="slide" ? slide_axis_z : twist_axis_z;
    translate([nut_x,0,axis]) rotate([0,90,0]) difference() {
        rotate(30) cylinder(r=metal_af/sqrt(3),h=metal_nut_t-bearing_margin,$fn=6);
        translate([0,0,-eps]) cylinder(d=bolt_nominal+0.02,h=metal_nut_t+2*eps);
    }
}
module metal_stack(kind="slide",loosen=0,clamped=true,bearing_margin=0) {
    through_bolt(kind,bearing_margin,loosen=loosen);
    fixed_nut(kind,bearing_margin);
}
module receiver(kind="slide") {
    if(kind=="slide") slide_female();
    if(kind=="snap") snap_female();
    if(kind=="twist") twist_female();
}

if(part=="slide_male") slide_male();
else if(part=="slide_female") slide_female();
else if(part=="slide_gib") slide_gib();
else if(part=="snap_male") snap_male();
else if(part=="snap_female") snap_female();
else if(part=="twist_male") twist_male();
else if(part=="twist_male_mount") twist_male_mount();
else if(part=="twist_female") twist_female();
else if(part=="knob") hand_knob();
else if(part=="twist_knob") hand_knob(twist_knob_d);
else assert(false,"Unknown part selector");
