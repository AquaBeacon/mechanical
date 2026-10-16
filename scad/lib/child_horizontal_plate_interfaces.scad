// Canonical interfaces, mm. Independent design, not density postprocessing.
include <wte4_interface.scad>
include <wte4_endcap_key_profile.scad>
include <ballast_plate_b_interface.scad>
hf_width=244;
hf_length=230;
hf_height=230;
hf_side_t=12;
hf_bottom_t=8;
hf_top_t=10;
hf_inside_width=hf_width-2*hf_side_t;
hf_vessel_z=138;
hf_vessel_length=200;
hf_stations=[-60,60];
hf_joint_y=[-80,80]; // corner feet/brim remain clear of the X1C exclusion
hf_clamp_width=40;
// The two stations are joined within each removable half, along the vessel axis.
hf_clamp_link_width=12;
hf_clamp_link_t=5.2;
hf_clamp_link_root=1;
hf_clamp_link_angle=45;
hf_liner_t_provisional=1;
hf_liner_compression_provisional=0.2;
hf_clamp_r=wte4_acrylic_od/2+hf_liner_t_provisional-hf_liner_compression_provisional;
hf_clamp_wall=8; // keep an 8 mm driver corridor beside the clamping ears
hf_clamp_mount_plane=62.8; // preserve the official mounting face, no extension
hf_mount_x=[-20,20]; // official 40 mm mounting pitch
hf_mount_axial=[-10,10]; // official 20 mm axial mounting pitch
hf_ear_x=67.84812820819513; // official clamping axes
hf_split_gap=1.6;
hf_ear_height=14.8;
hf_top_z=hf_vessel_z+hf_clamp_mount_plane;
hf_lower_z=hf_vessel_z-hf_clamp_mount_plane;
hf_arm_t=17;
hf_cross_depth=34;
// Independent lower-clamp brackets, four identical parts.
hf_support_foot_t=8;
hf_support_foot_bottom=32;
hf_support_tip_x=12;
hf_support_gusset_x=85;
hf_support_joint_z=[42,66];
hf_support_joint_axial=[-10,10];
hf_support_screw_length=25; // exposed nut + two 0.5 mm washers
hf_new_hole_sides=8;
hf_open_nut_access_w=11; // open wrench relief, not a captive hex pocket
hf_open_nut_access_depth=8; // short bridge in the bracket's broad-face-down print
hf_m3_clearance=3.5;
hf_nut_af=5.8; // M3 AF5.5 +0.3 fit allowance
hf_nut_t=2.8; // M3 thickness2.4 +0.4 fit allowance
hf_edge_chamfer=0.6;
hf_edge_fillet=2;
hf_ballast_x=[-54,54];
hf_ballast_band_y=[-24,5]; // both on the measured 53 mm body
hf_ballast_d=48.5;
hf_ballast_length=76;
hf_ballast_pad_t_provisional=0.8;
hf_ballast_r=hf_ballast_d/2+hf_ballast_pad_t_provisional;
hf_ballast_z=hf_bottom_t+hf_ballast_r;
hf_ballast_cap_t=6;
hf_ballast_bolt_offset=32;
hf_ballast_band_width=12;
hf_ballast_ear_h=13; // washer seat clears the curved cap shoulder
hf_plate_y=[-96,-60,60,96]; // centre inner rows between the lower-clamp tool holes
hf_plate_hole_x=ballast_b_hole_x;
hf_plate_t=ballast_b_size[2];
hf_plate_bore_d=5.6;
hf_plate_nut_af=8.4;
hf_plate_nut_depth=4.4;
hf_plate_nut_base=0.4;
hf_plate_washer_t=1;
hf_plate_screw_length=12;
hf_mount_nut_radius=56.5;
hf_mount_upper_screw_length=18;
hf_mount_lower_screw_length=25;
hf_joint_nut_inset=12;
hf_lower_joint_z=20;
hf_ballast_nut_z=18.5;
hf_ballast_screw_length=30;
hf_clamp_screw_length=30;
hf_frame_screw_length=25;
hf_top_frame_screw_length=30;
hf_ear_rows=[[-hf_ear_x,-10],[-hf_ear_x,10],[hf_ear_x,0]];
// Side extensions; cable reservation 50 mm confirmed by user 2026-10-08.
hf_guard_t=8;
hf_guard_front_tip=174;
hf_guard_overlap=80;
hf_guard_z=[64,212];
hf_guard_joint_y=[-98,98];
hf_guard_joint_z=[100,176];
hf_guard_screw_length=25;
hf_guard_rail=20;
hf_flange_exposed_t=8;
hf_endcap_anchor_z=wte4_endcap_plug_t-hf_flange_exposed_t;
hf_endcap_outer_y=-hf_vessel_length/2-hf_flange_exposed_t-wte4_endcap_exposed_t;
hf_cable_keepout_length=50;
hf_cable_keepout_d=75;
hf_guard_end_margin=12;
hf_guard_rear_tip=hf_endcap_outer_y-hf_cable_keepout_length-hf_guard_end_margin;
hf_key_clearance=0.55;
hf_key_body_clearance=0.55;
hf_key_y=hf_endcap_outer_y+wte4_endcap_exposed_t/2;
hf_key_depth=wte4_endcap_exposed_t+2*hf_key_clearance;
hf_key_z=[114,149];
hf_key_lift=100;
// Separate tab receiver mounts directly to the side frame's inside face.
hf_key_mount_y=-98;
hf_key_mount_z=[122,142];
hf_key_mount_t=8;
hf_key_screw_length=25;
// Generic M3 accessory interface; 20 mm pitch along the continuous rails.
hf_accessory_y=[-60,-40,-20,0,20,40,60];
hf_accessory_z=[16,220];
hf_accessory_column_y=[-60,60];
hf_accessory_column_z=[100,120,140,160];
// Numeric export: placement generator reads this; it never copies hole pitches.
echo(["INTERFACES",["stations",hf_stations],["joint_y",hf_joint_y],
 ["band_width",hf_clamp_width],["link_width",hf_clamp_link_width],
 ["link_t",hf_clamp_link_t],["link_root",hf_clamp_link_root],
 ["link_angle",hf_clamp_link_angle],["mount_x",hf_mount_x],["mount_axial",hf_mount_axial],
 ["ear_rows",hf_ear_rows],["ear_height",hf_ear_height],["nut_t",hf_nut_t],
 ["mount_nut_r",hf_mount_nut_radius],["upper_screw_l",hf_mount_upper_screw_length],
 ["lower_screw_l",hf_mount_lower_screw_length],["arm_t",hf_arm_t],
 ["support_foot_t",hf_support_foot_t],["support_bottom",hf_support_foot_bottom],
 ["support_joint_z",hf_support_joint_z],["support_joint_axial",hf_support_joint_axial],
 ["support_screw_l",hf_support_screw_length],["cross_depth",hf_cross_depth],
 ["joint_inset",hf_joint_nut_inset],["lower_joint_z",hf_lower_joint_z],
 ["ballast_x",hf_ballast_x],["ballast_y",hf_ballast_band_y],
 ["ballast_length",hf_ballast_length],["ballast_band_width",hf_ballast_band_width],
 ["ballast_bolt_offset",hf_ballast_bolt_offset],["ballast_ear_h",hf_ballast_ear_h],
 ["split_gap",hf_split_gap],["ballast_nut_z",hf_ballast_nut_z],
 ["plate_y",hf_plate_y],["plate_hole_x",hf_plate_hole_x],["plate_t",hf_plate_t],
 ["plate_nut_base",hf_plate_nut_base],["plate_nut_depth",hf_plate_nut_depth],
 ["plate_screw_l",hf_plate_screw_length],["plate_washer_t",hf_plate_washer_t],
 ["ballast_screw_l",hf_ballast_screw_length],["clamp_screw_l",hf_clamp_screw_length],
 ["frame_screw_l",hf_frame_screw_length],
 ["top_frame_screw_l",hf_top_frame_screw_length],
 ["new_hole_sides",hf_new_hole_sides],["open_nut_access_w",hf_open_nut_access_w],
 ["open_nut_access_depth",hf_open_nut_access_depth],
 ["guard_t",hf_guard_t],["guard_front_tip",hf_guard_front_tip],
 ["guard_rear_tip",hf_guard_rear_tip],["guard_overlap",hf_guard_overlap],
 ["guard_z",hf_guard_z],["guard_joint_y",hf_guard_joint_y],["guard_joint_z",hf_guard_joint_z],
 ["guard_screw_l",hf_guard_screw_length],["endcap_anchor_z",hf_endcap_anchor_z],
 ["endcap_outer_y",hf_endcap_outer_y],["key_y",hf_key_y],
 ["key_clearance",hf_key_clearance],["key_depth",hf_key_depth],
 ["key_mount_y",hf_key_mount_y],["key_mount_z",hf_key_mount_z],
 ["key_mount_t",hf_key_mount_t],["key_screw_l",hf_key_screw_length],
 ["accessory_y",hf_accessory_y],["accessory_z",hf_accessory_z],
 ["accessory_column_y",hf_accessory_column_y],["accessory_column_z",hf_accessory_column_z],
 ["cable_length",hf_cable_keepout_length],["cable_d",hf_cable_keepout_d],
 ["guard_margin",hf_guard_end_margin]]);
assert(hf_top_z+hf_top_t<hf_height);
assert(hf_clamp_mount_plane>hf_clamp_r);
assert(hf_length+10<=256 && hf_height+10<=256);
