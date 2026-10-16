// Removable two-point camera angle stop for parent_oneplate.
// Coordinates are camera_mount local coordinates; case contact is provisional.
use <../../../../../scad/lib/edge_finished_profiles.scad>
$fn=48;
wall_center_y=27; wall_front_y=31; wall_back_y=23;
wall_top_z=32.2; tool_hole_pitch=40; tool_hole_z=20;
bolt_d=4.5; // M4 clearance through the existing nominal 5 mm tool holes
mount_plate_t=4; arm_w=3.6; arm_h=4.3;
case_stop_y=16; case_stop_z=36.5; // initial contact setting only; case is provisional
case_stop_depth=8; case_stop_width=10; adjuster_d=4.5; adjuster_nut_af=7.2;
adjuster_nut_h=3.2; edge_c=0.45; corner_r=1.5;
assert(wall_center_y==27 && wall_top_z>tool_hole_z);
module efbox_at(x,y,z,w,d,h,r=corner_r) translate([x,y,z])
 translate([w/2,d/2,0]) ef_box(w,d,h,r,edge_c);
module roof_hole_y(d,len) {
 r=d/2/cos(180/32);
 rotate([90,0,0]) linear_extrude(len) union() {
  circle(r=r,$fn=32);
  polygon([[-r/sqrt(2),r/sqrt(2)],[0,sqrt(2)*r],[r/sqrt(2),r/sqrt(2)]]);
 }
}
module adjuster_hole() cylinder(d=adjuster_d/cos(180/32),h=arm_h+0.04,$fn=32);
module one_stop() {
 difference() {
  union() {
   // Backing strip sits on the existing wall's outer face (y=31..35).
   // 52 mm strip gives the x=±20 holes 6 mm of edge distance.
   efbox_at(-26,wall_front_y,15,52,mount_plate_t,18.2,2);
   // Paired narrow risers clear the existing ±30 mm front pads.
   for(s=[-1,1]) {
    translate([s*tool_hole_pitch/2-arm_w/2,case_stop_y+case_stop_depth-1,
               wall_top_z])
     rbox([arm_w,wall_front_y-(case_stop_y+case_stop_depth)+2,
           case_stop_z-wall_top_z+1.3],1.2,"y");
    // Contact feet end at z=36.5; vertical M4 screws set the case angle independently.
    efbox_at(s*tool_hole_pitch/2-case_stop_width/2,case_stop_y,case_stop_z-arm_h,
             case_stop_width,case_stop_depth,arm_h,1.2);
   }
  }
  // Through-bolts align with the existing front-wall tool bores at x=±20,z=20.
  for(x=[-tool_hole_pitch/2,tool_hole_pitch/2])
   translate([x,wall_front_y+mount_plate_t+0.02,tool_hole_z])
    roof_hole_y(bolt_d,mount_plate_t+0.04);
  // Captive M4 nuts at each contact foot; screws rise from below and adjust independently.
  for(x=[-tool_hole_pitch/2,tool_hole_pitch/2]) {
   translate([x,case_stop_y+case_stop_depth/2,case_stop_z-arm_h-0.02])
    linear_extrude(adjuster_nut_h+0.02) rotate(-30) ef_hex(adjuster_nut_af);
   translate([x,case_stop_y+case_stop_depth/2,case_stop_z-arm_h-0.02]) adjuster_hole();
  }
 }
}
module rbox(s,r=2,axis="z") {
 if(axis=="z") translate([s[0]/2,s[1]/2,0]) ef_box(s[0],s[1],s[2],r,edge_c);
 if(axis=="y") translate([0,s[1],0]) rotate([90,0,0])
  translate([s[0]/2,s[2]/2,0]) ef_box(s[0],s[2],s[1],r,edge_c);
}
one_stop();
