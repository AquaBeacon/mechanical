// Four main frames and four ballast caps. Independent parametric design.
include <../../../../../scad/lib/child_horizontal_plate_interfaces.scad>
use <../../../../../scad/lib/edge_finished_profiles.scad>
part="side"; // [side,bottom,top,ballast_cap,guard_front,guard_rear,guard_front_inner,guard_rear_inner,rotation_key,clamp_support]
edge_chamfer=hf_edge_chamfer;
edge_fillet_r=hf_edge_fillet;
// Clamp service from above. Existing assembly uses an 8 mm driver envelope.
top_access_driver_d=8;
top_access_radial_clearance=1;
top_access_d=top_access_driver_d+2*top_access_radial_clearance;
top_access_chamfer=0.4;
top_access_radial_land=4.5;
top_access_sides=12;
top_access_driver_length=70;
$fn=64;
echo(["LAYOUT",hf_width,hf_length,hf_height,hf_side_t,hf_bottom_t,hf_top_t,
      hf_vessel_z,hf_vessel_length,hf_top_z,hf_lower_z,hf_ballast_z]);
echo(["TOP_CLAMP_ACCESS",top_access_d,top_access_chamfer,top_access_radial_land,
      top_access_sides,top_access_driver_d,top_access_driver_length]);
module octagon(w,h,cut=30) {
    offset(r=edge_fillet_r) offset(delta=-edge_fillet_r)
        polygon([[-w/2,-h/2+cut],[-w/2+cut,-h/2],[w/2-cut,-h/2],
                 [w/2,-h/2+cut],[w/2,h/2-cut],[w/2-cut,h/2],
                 [-w/2+cut,h/2],[-w/2,h/2-cut]]);
}
module captive_vertical_slot(x,y,z,width,entry_sign=1) {
    translate([x,y,z]) linear_extrude(hf_nut_t) ef_hex(hf_nut_af);
    translate([x,y+entry_sign*(width/2+1)/2,z])
        linear_extrude(hf_nut_t) ef_round_rect(hf_nut_af,width/2+1,0.25);
}
module joint_block(z,depth) {
    for(s=[-1,1],y=hf_joint_y) translate([s*(hf_inside_width/2-hf_joint_nut_inset/2),y,z])
        ef_box(hf_joint_nut_inset,depth,32,edge_fillet_r,edge_chamfer);
}
module joint_holes(z,depth,entry_z=32,open_nut=false) {
    for(s=[-1,1],y=hf_joint_y) {
        bore_depth=open_nut ? hf_joint_nut_inset+hf_open_nut_access_depth+10 : hf_joint_nut_inset+1.5;
        translate([s*hf_inside_width/2,y,z]) rotate([0,s*90,0])
            translate([0,0,-bore_depth])
                if(open_nut) ef_poly_bore(hf_m3_clearance,bore_depth,sides=hf_new_hole_sides);
                else ef_bore(hf_m3_clearance,hf_joint_nut_inset+1.5);
        if(open_nut) {
            // Open through the top/bottom. Flat pad at X=+/-98, no hex trap.
            translate([s*(hf_inside_width/2-hf_joint_nut_inset-hf_open_nut_access_depth/2),y,z])
                translate([0,0,-20]) ef_box(hf_open_nut_access_depth,hf_open_nut_access_w,40,0.5,0.3);
        } else translate([s*(hf_inside_width/2-hf_joint_nut_inset),y,z]) rotate([0,s*90,0])
            ef_cut(hf_nut_t,0.25) hull() {
                ef_hex(hf_nut_af);
                translate([-s*(entry_z-z+4),0]) ef_hex(hf_nut_af);
            }
    }
}
module arm_profile() {
    // Independent bracket in the left-side world X/Z section. Preserve the
    // original clamp mounting plane and the inward arm/gusset profile.
    inside=-hf_inside_width/2;
    original_root_z=hf_support_foot_bottom+
        hf_side_t*(hf_lower_z-hf_arm_t-hf_support_foot_bottom)/
        (hf_width/2-hf_support_gusset_x);
    ef_plan_finish(edge_fillet_r) union() {
        translate([inside,hf_support_foot_bottom])
            square([hf_support_foot_t,hf_lower_z-hf_support_foot_bottom]);
        polygon([[inside,original_root_z],[-hf_support_gusset_x,hf_lower_z-hf_arm_t],
                 [-hf_support_tip_x,hf_lower_z-hf_arm_t],[-hf_support_tip_x,hf_lower_z],
                 [inside,hf_lower_z]]);
    }
}
module clamp_support_world() {
    difference() {
        translate([0,hf_cross_depth/2,0]) rotate([90,0,0])
            ef_profile(hf_cross_depth,edge_chamfer) arm_profile();
        for(dy=hf_mount_axial)
            translate([hf_mount_x[0],dy,hf_lower_z-hf_arm_t])
                ef_poly_bore(hf_m3_clearance,hf_arm_t,sides=hf_new_hole_sides);
        for(dy=hf_support_joint_axial,z=hf_support_joint_z) {
            translate([-hf_inside_width/2,dy,z]) rotate([0,90,0])
                ef_poly_bore(hf_m3_clearance,hf_inside_width/2-hf_support_tip_x,sides=hf_new_hole_sides);
            // Nut/washer bear on the unrecessed 8 mm foot. This opening goes
            // to the axial edge for a spanner; the shaft continues through.
            translate([-hf_inside_width/2+hf_support_foot_t+hf_open_nut_access_depth/2,
                       sign(dy)*(abs(dy)+hf_cross_depth/2)/2,z-hf_open_nut_access_w/2])
                ef_box(hf_open_nut_access_depth,hf_cross_depth/2-abs(dy)+hf_open_nut_access_w,
                       hf_open_nut_access_w,0.5,0.3);
        }
    }
}
module clamp_support_print() {
    // Broad X/Z gusset face on the bed: proper rotation, not a reflection.
    multmatrix([[1,0,0,hf_inside_width/2],[0,0,-1,hf_lower_z],
                [0,1,0,hf_cross_depth/2],[0,0,0,1]]) clamp_support_world();
}
module left_side_world() {
    difference() {
        union() {
            translate([-hf_width/2,0,hf_height/2]) rotate([90,0,90])
                ef_profile(hf_side_t,edge_chamfer) ef_plan_finish(edge_fillet_r) union() {
                    difference() {
                        octagon(hf_length,hf_height);
                        for(row=[[-90,27],[0,82],[90,27]]) translate([row[0],102-hf_height/2])
                            ef_round_rect(row[1],112,7);
                        translate([0,189-hf_height/2]) ef_round_rect(90,34,7);
                    }
                    for(y=hf_guard_joint_y,z=hf_guard_joint_z)
                        translate([y,z-hf_height/2]) ef_round_rect(24,22,2);
                    // Both ends carry identical seats so one side STL still
                    // serves left/right by a proper 180 degree rotation.
                    for(y=hf_guard_joint_y)
                        translate([y,(hf_key_z[0]+hf_key_z[1])/2-hf_height/2])
                            ef_round_rect(24,hf_key_z[1]-hf_key_z[0],2);
                }
        }
        for(y=hf_guard_joint_y,z=hf_guard_joint_z) {
            translate([-hf_width/2,y,z]) rotate([0,90,0]) ef_bore(hf_m3_clearance,hf_side_t);
            translate([-hf_inside_width/2,y,z]) rotate([0,-90,0]) ef_cut(hf_nut_t,0.25) ef_hex(hf_nut_af);
        }
        for(y=hf_joint_y,z=[hf_lower_joint_z,hf_top_z+hf_top_t/2])
            translate([-hf_width/2,y,z]) rotate([0,90,0]) ef_bore(hf_m3_clearance,hf_side_t);
        for(y=hf_guard_joint_y,z=hf_key_mount_z)
            translate([-hf_width/2,y,z]) rotate([0,90,0]) ef_bore(hf_m3_clearance,hf_side_t);
        for(y=hf_accessory_y,z=hf_accessory_z) accessory_hole(y,z);
        for(y=hf_accessory_column_y,z=hf_accessory_column_z) accessory_hole(y,z);
        for(y=hf_stations,dy=hf_support_joint_axial,z=hf_support_joint_z)
            translate([-hf_width/2,y+dy,z]) rotate([0,90,0])
                ef_bore(hf_m3_clearance,hf_side_t);
    }
}
module accessory_hole(y,z) {
    translate([-hf_width/2,y,z]) rotate([0,90,0]) ef_bore(hf_m3_clearance,hf_side_t);
    translate([-hf_inside_width/2,y,z]) rotate([0,-90,0])
        ef_cut(hf_nut_t,0.25) ef_hex(hf_nut_af);
}
module side_print() {
    // Plain side plate, outside face on bed. 230 x 230 x 12.
    multmatrix([[0,1,0,0],[0,0,1,-hf_height/2],[1,0,0,hf_width/2],[0,0,0,1]])
        left_side_world();
}
module cradle_positive() {
    translate([0,hf_ballast_band_width/2,0]) rotate([90,0,0])
        ef_convex_profile(hf_ballast_band_width,edge_chamfer)
            translate([0,(hf_bottom_t+hf_ballast_z-0.8)/2])
                ef_round_rect(2*(hf_ballast_r+hf_ballast_cap_t),
                              hf_ballast_z-0.8-hf_bottom_t+2,edge_fillet_r);
}
module cradle_cut() {
    translate([0,hf_ballast_band_width/2,hf_ballast_z]) rotate([90,0,0])
        ef_cut(hf_ballast_band_width,edge_chamfer) circle(r=hf_ballast_r);
}
module bottom_frame() {
    difference() {
        union() {
            ef_convex_profile(hf_bottom_t,edge_chamfer) octagon(hf_inside_width,hf_length);
            joint_block(0,28);
            for(x=hf_ballast_x,y=hf_ballast_band_y) {
                translate([x,y,0]) cradle_positive();
                for(s=[-1,1]) translate([x+s*hf_ballast_bolt_offset,y,hf_bottom_t-1])
                    ef_box(14,18,hf_ballast_z-hf_split_gap/2-hf_bottom_t+1,2,edge_chamfer);
            }
            for(x=hf_ballast_x,s=[-1,1]) translate([x,s*(hf_ballast_length/2+2.1),hf_bottom_t-1])
                ef_box(48,3,20,1,edge_chamfer);
            for(y=hf_plate_y,s=[-1,1]) translate([s*85,y,hf_bottom_t-1])
                ef_box(3,22,8,1,edge_chamfer);
            intersection() {
                translate([-hf_inside_width/2,-hf_length/2,0]) cube([hf_inside_width,hf_length,60]);
                union() {
                    for(s=[-1,1],y=hf_joint_y) translate([s*(hf_inside_width/2-6),y,hf_bottom_t]) ef_root(12,28);
                    for(x=hf_ballast_x,y=hf_ballast_band_y) {
                        translate([x,y,hf_bottom_t]) ef_root(2*(hf_ballast_r+hf_ballast_cap_t),hf_ballast_band_width);
                        for(s=[-1,1]) translate([x+s*hf_ballast_bolt_offset,y,hf_bottom_t]) ef_root(14,18);
                    }
                    for(x=hf_ballast_x,s=[-1,1]) translate([x,s*(hf_ballast_length/2+2.1),hf_bottom_t]) ef_root(48,3,1,1);
                    for(y=hf_plate_y,s=[-1,1]) translate([s*85,y,hf_bottom_t]) ef_root(3,22,1,1);
                }
            }
        }
        joint_holes(hf_lower_joint_z,28);
        for(x=hf_ballast_x,y=hf_ballast_band_y) {
            translate([x,y,0]) cradle_cut();
            for(s=[-1,1]) {
                translate([x+s*hf_ballast_bolt_offset,y,13.5])
                    ef_bore(hf_m3_clearance,hf_ballast_z-hf_split_gap/2-13.5);
                captive_vertical_slot(x+s*hf_ballast_bolt_offset,y,hf_ballast_nut_z,18);
            }
        }
        // All four existing B holes are used. Nuts enter from the underside.
        for(y=hf_plate_y,x=hf_plate_hole_x) {
            translate([x,y,0]) ef_bore(hf_plate_bore_d,hf_bottom_t);
            translate([x,y,hf_plate_nut_depth]) rotate([180,0,0])
                ef_cut(hf_plate_nut_depth,0.15) ef_hex(hf_plate_nut_af);
        }
        for(y=[-42,38]) translate([0,y,0])
            ef_cut(hf_bottom_t,edge_chamfer) ef_round_rect(16,6,2);
        // Lower-clamp screwdriver access. Remove B plates for service.
        for(y=hf_stations,x=hf_mount_x,dy=hf_mount_axial)
            translate([x,y+dy,0]) ef_bore(9,hf_bottom_t,0.4);
    }
}
module top_frame() {
    difference() {
        union() {
            ef_profile(hf_top_t,edge_chamfer)
                ef_plan_finish(edge_fillet_r) union() {
                    ef_round_rect(28,220,3);
                    for(y=hf_stations) translate([0,y]) ef_round_rect(hf_inside_width,hf_cross_depth,4);
                    for(y=hf_joint_y) translate([0,y]) ef_round_rect(hf_inside_width,28,4);
                    // Local lands prevent the inner pair of service bores from
                    // leaving a thin edge in the existing 34 mm cross members.
                    for(y=hf_stations,ear=hf_ear_rows)
                        translate([ear[0],y+ear[1]])
                            circle(d=top_access_d+2*top_access_radial_land);
                }
            for(s=[-1,1],y=hf_joint_y) translate([s*(hf_inside_width/2-6),y,0])
                ef_box(12,28,12,edge_fillet_r,edge_chamfer);
            intersection() {
                translate([-hf_inside_width/2,-hf_length/2,0]) cube([hf_inside_width,hf_length,20]);
                for(s=[-1,1],y=hf_joint_y) translate([s*(hf_inside_width/2-6),y,hf_top_t]) ef_root(12,28);
            }
        }
        translate([0,0,-hf_top_z]) joint_holes(hf_top_z+hf_top_t/2,28,hf_top_z+12,true);
        for(y=hf_stations,x=hf_mount_x,dy=hf_mount_axial)
            translate([x,y+dy,0]) ef_poly_bore(hf_m3_clearance,hf_top_t,sides=hf_new_hole_sides);
        // Align to the actual tightening axes, not the eight clamp mount holes.
        for(y=hf_stations,ear=hf_ear_rows) translate([ear[0],y+ear[1],0])
            ef_poly_bore(top_access_d,hf_top_t,top_access_chamfer,sides=top_access_sides);
        for(y=[-27,27]) translate([0,y,0])
            ef_cut(hf_top_t,edge_chamfer) ef_capsule(10,25);
    }
}
module ballast_cap() {
    // +print Z is the assembly band axis; cap x4.
    difference() {
        ef_profile(hf_ballast_band_width,edge_chamfer)
            ef_plan_finish(edge_fillet_r) union() {
                intersection() {
                    circle(r=hf_ballast_r+hf_ballast_cap_t);
                    translate([-42,hf_split_gap/2]) square([84,44]);
                }
                for(s=[-1,1]) translate([s*hf_ballast_bolt_offset,
                         hf_split_gap/2+hf_ballast_ear_h/2]) ef_round_rect(18,hf_ballast_ear_h,2);
            }
        ef_cut(hf_ballast_band_width,edge_chamfer) circle(r=hf_ballast_r);
        for(s=[-1,1]) translate([s*hf_ballast_bolt_offset,hf_split_gap/2,hf_ballast_band_width/2])
            rotate([-90,0,0]) ef_poly_bore(hf_m3_clearance,hf_ballast_ear_h,sides=hf_new_hole_sides);
    }
}
module guard_outline(front) {
    a=front ? hf_guard_overlap : hf_guard_rear_tip;
    b=front ? hf_guard_front_tip : -hf_guard_overlap;
    middle=(a+b)/2;
    translate([middle,(hf_guard_z[0]+hf_guard_z[1])/2])
        octagon(b-a,hf_guard_z[1]-hf_guard_z[0],10);
}
module guard_window(front) {
    // A continuous 36 mm root rail joins both bolt seats to the end rails.
    a=front ? hf_guard_overlap+36 : hf_guard_rear_tip+hf_guard_rail;
    b=front ? hf_guard_front_tip-hf_guard_rail : -hf_guard_overlap-36;
    translate([(a+b)/2,(hf_guard_z[0]+hf_guard_z[1])/2])
        ef_round_rect(b-a,hf_guard_z[1]-hf_guard_z[0]-2*hf_guard_rail,6);
}
module cap_lift_profile(keyed=true) {
    // The two tab recesses open upward so the vessel can be lowered in.
    r=keyed ? wte4_key_half_width+hf_key_clearance : wte4_key_base_r+hf_key_body_clearance;
    union() {
        if(keyed) offset(delta=hf_key_clearance) wte4_key_profile();
        else circle(r=r,$fn=128);
        translate([-r,0]) square([2*r,hf_key_lift]);
    }
}
module rear_key_support() {
    foot_inner_x=-hf_inside_width/2+hf_key_mount_t;
    arm_top_z=hf_key_z[0]+12;
    key_root_chamfer=2;
    difference() {
        union() {
            translate([0,0,hf_key_z[0]]) ef_profile(12,edge_chamfer) ef_plan_finish(2) union() {
                hull() {
                    translate([-hf_inside_width/2+hf_key_mount_t/2,hf_key_mount_y])
                        ef_round_rect(hf_key_mount_t,24,2);
                    translate([-76,hf_key_y]) ef_round_rect(16,16,2);
                }
                translate([-60,hf_key_y]) ef_round_rect(20,16,2);
            }
            translate([-58.5,hf_key_y,hf_key_z[0]]) ef_box(15,19,hf_key_z[1]-hf_key_z[0],2,edge_chamfer);
            translate([-58.5,hf_key_y,hf_key_z[0]+12]) ef_root(15,19,1,2);
            translate([-hf_inside_width/2,0,0]) rotate([90,0,90])
                ef_convex_profile(hf_key_mount_t,edge_chamfer)
                    translate([hf_key_mount_y,(hf_key_z[0]+hf_key_z[1])/2])
                        ef_round_rect(24,hf_key_z[1]-hf_key_z[0],2);
            // Local 2 mm relief at the mounting-foot / receiver-arm root.
            translate([0,hf_key_mount_y+11,0]) rotate([90,0,0])
                ef_profile(22,0.3) offset(r=0.25) offset(delta=-0.25)
                    polygon([[foot_inner_x-0.5,arm_top_z-0.5],
                             [foot_inner_x+key_root_chamfer,arm_top_z-0.5],
                             [foot_inner_x-0.5,arm_top_z+key_root_chamfer+0.5]]);
        }
        translate([0,hf_key_y+11,hf_vessel_z]) rotate([90,0,0])
            ef_cut(22,0.3) cap_lift_profile(false);
        translate([0,hf_key_y+hf_key_depth/2,hf_vessel_z]) rotate([90,0,0])
            ef_cut(hf_key_depth,0.3) cap_lift_profile(true);
        for(z=hf_key_mount_z) {
            translate([-hf_inside_width/2,hf_key_mount_y,z]) rotate([0,90,0])
                ef_poly_bore(hf_m3_clearance,36,sides=hf_new_hole_sides);
            translate([-hf_inside_width/2+hf_key_mount_t+hf_open_nut_access_depth/2,
                       hf_key_mount_y+6,z-hf_open_nut_access_w/2])
                ef_box(hf_open_nut_access_depth,12+hf_open_nut_access_w,
                       hf_open_nut_access_w,0.5,0.3);
        }
    }
}
module inner_guard_clearance(front) {
    // Open edge reliefs preserve the original bolt stations. One millimetre
    // allowance also covers the finished notch corners around the R2 seats.
    y=front ? hf_joint_y[1] : hf_joint_y[0];
    translate([y,hf_top_z+6]) ef_round_rect(30,14,2);
    // The key's sloping arm projects behind the mounting foot. Connect this
    // opening to the guard window instead of leaving a thin 2 mm ligament.
    if(!front) translate([(hf_key_mount_y-21-hf_guard_overlap+1)/2,
                             (hf_key_z[0]+hf_key_z[1])/2])
        ef_round_rect(-hf_guard_overlap+1-(hf_key_mount_y-21),
                      hf_key_z[1]-hf_key_z[0]+2,2);
}
module guard_world(front,inner=false) {
    difference() {
        union() {
            translate([-hf_width/2-hf_guard_t,0,0]) rotate([90,0,90])
                if(inner) ef_profile(hf_guard_t,edge_chamfer)
                    ef_plan_finish(edge_fillet_r) difference() {
                        guard_outline(front);
                        guard_window(front);
                        inner_guard_clearance(front);
                    }
                else difference() {
                    ef_convex_profile(hf_guard_t,edge_chamfer) guard_outline(front);
                    ef_cut(hf_guard_t,edge_chamfer) guard_window(front);
                }
        }
        for(z=hf_guard_joint_z)
            translate([-hf_width/2-hf_guard_t,front ? hf_guard_joint_y[1] : hf_guard_joint_y[0],z])
                rotate([0,90,0]) ef_poly_bore(hf_m3_clearance,hf_guard_t,sides=hf_new_hole_sides);
        // Keep the original top-frame washer and screwdriver route accessible.
        translate([-hf_width/2-hf_guard_t,front ? hf_joint_y[1] : hf_joint_y[0],hf_top_z+hf_top_t/2])
            rotate([0,90,0]) ef_bore(10,hf_guard_t);
        // Recess around the direct-to-side key screws and their driver route.
        for(z=hf_key_mount_z)
            translate([-hf_width/2-hf_guard_t,front ? hf_guard_joint_y[1] : hf_guard_joint_y[0],z])
                rotate([0,90,0]) ef_bore(10,hf_guard_t);
    }
}
module guard_print(front,inner=false) {
    multmatrix([[0,1,0,0],[0,0,1,-hf_vessel_z],[1,0,0,hf_width/2+hf_guard_t],[0,0,0,1]]) guard_world(front,inner);
}
if(part=="side") side_print();
else if(part=="bottom") bottom_frame();
else if(part=="top") top_frame();
else if(part=="ballast_cap") ballast_cap();
else if(part=="guard_front") guard_print(true);
else if(part=="guard_rear") guard_print(false);
else if(part=="guard_front_inner") guard_print(true,true);
else if(part=="guard_rear_inner") guard_print(false,true);
else if(part=="clamp_support") clamp_support_print();
else if(part=="rotation_key")
    multmatrix([[0,1,0,0],[0,0,1,-hf_vessel_z],[1,0,0,hf_inside_width/2],[0,0,0,1]])
        rear_key_support();
else assert(false,"Unknown part");
