"""OpenSCAD source strings for parent_oneplate's locally fitted sensor interfaces.

These sources are consumed by the parent_oneplate preparation workflow.  They
remain separate from shared camera-mount geometry and make provisional sensor
fits explicit at the source.
"""


def td_support_source() -> str:
    """Return the bolt-on TD support with retained bracket datums."""
    return r'''// Parent oneplate TD04A support with flat frame seat and bracket datums.
// Units mm. TD bracket width and end position are provisional values from the
// current visual proxy; verify against the metal bracket before final use.
use <../../../../../scad/lib/edge_finished_profiles.scad>
include <../../../../../scad/lib/parent_oneplate_interfaces.scad>
$fn=48;
wall=8; x0=25; width=80; rear_y=-67; top_z=-po_deck_t; bottom_z=-54;
td_x=55; td_z=-35; pitch=36;
td_bracket_width=24; // provisional; COTS visual proxy says 24 mm
td_bracket_left=td_x-td_bracket_width/2; // x=43 datum
td_bracket_gap=0.4; // provisional assembly allowance; shim after measuring
td_bracket_top=-27; // provisional end stop datum, matching bracket jaw datum
td_bracket_thickness=2; // provisional visual-proxy plate thickness
datum_t=4; datum_y=td_bracket_thickness+0.2; datum_r=0.8; edge_c=0.45;
assert(width==80 && td_bracket_width>20 && td_bracket_width<30);
assert(td_bracket_left> x0+10 && td_bracket_left+td_bracket_width+td_bracket_gap < x0+width-10);
module rbox(s,r=2,axis="z") {
 if(axis=="z") translate([s[0]/2,s[1]/2,0]) ef_box(s[0],s[1],s[2],r,edge_c);
 if(axis=="y") translate([0,s[1],0]) rotate([90,0,0])
  translate([s[0]/2,s[2]/2,0]) ef_box(s[0],s[2],s[1],r,edge_c);
 if(axis=="x") translate([0,s[1]/2,s[2]/2]) rotate([0,90,0])
  ef_box(s[2],s[1],s[0],r,edge_c);
}
module fit_hole(d,h,c=0.3) {
 dd=d/cos(180/32);
 union() {
  cylinder(d=dd,h=h,$fn=32);
  cylinder(d1=dd+2*c,d2=dd,h=c,$fn=32);
  translate([0,0,h-c]) cylinder(d1=dd,d2=dd+2*c,h=c,$fn=32);
 }
}
module roof(d,h,angle=0) {
 r=d/2/cos(180/32);
 rotate([0,0,angle]) ef_cut(h,0.3) union() {
  circle(r=r,$fn=32);
  polygon([[r/sqrt(2),-r/sqrt(2)],[r/sqrt(2)*(1+tan(55)),0],[r/sqrt(2),r/sqrt(2)]]);
 }
}
module main_support() {
 difference() {
  union() {
   // Flat plate underside seat; retain the TD bracket and clamp coordinates.
   // Extrude along X: the complete L end face becomes the bed face at X=25.
   translate([x0,rear_y,top_z-wall]) rbox([width,-rear_y,wall],2,"x");
   translate([x0,-wall,bottom_z]) rbox([width,wall,top_z-bottom_z],2,"x");
   // Left bracket datum (contact at x=43) and top-end insertion stop (z=-27).
   translate([0,0,td_bracket_top-16])ef_profile(18,edge_c)
    offset(r=0.2)offset(delta=-0.2)polygon([
     [td_bracket_left-datum_t-datum_y-1,-0.2],[td_bracket_left,-0.2],
     [td_bracket_left,datum_y-0.2],[td_bracket_left-datum_t,datum_y-0.2]]);
   // Continuous top stop grows from the left datum; the redundant right cheek
   // is omitted. Left X=43 and top Z=-27 still locate the clamped bracket.
   translate([td_bracket_left-datum_t,-0.2,td_bracket_top])
    rbox([td_bracket_width+datum_t-2,datum_y,2],0.3,"x");
  }
  // Original M5 carrier attachment: x=65/85, y=-55, vertical axis.
 for(x=po_carrier_x) translate([x,po_carrier_y,top_z-wall-0.02]) {
  roof(5.5,wall+0.04,0);
  translate([0,0,-0.01]) cylinder(d1=6.1,d2=5.5,h=0.31,$fn=32);
  translate([0,0,wall-0.30]) cylinder(d1=5.5,d2=6.1,h=0.31,$fn=32);
 }
  // Original M4 TD clamp holes: x=37/73, z=-35, axis Y.
  for(x=[td_x-pitch/2,td_x+pitch/2])
   // In the Y=-90 degree print pose, local +X is upward.
   translate([x,-wall-0.02,td_z]) rotate([-90,0,0]) roof(4.5,wall+datum_y+0.04,0);
 }
}
main_support();
'''


def camera_stop_source() -> str:
    """Return one removable camera angle stop keyed to existing front-wall holes.

    Case contact height/y are explicitly initial settings for the still-provisional
    camera case.  The stop installs after the mount is secured and can be removed
    for M3 tool access.
    """
    return r'''// Removable two-point camera angle stop for parent_oneplate.
// Coordinates are camera_mount local coordinates; case contact is provisional.
use <../../../../../scad/lib/edge_finished_profiles.scad>
$fn=48;
wall_center_y=27; wall_front_y=31; wall_back_y=23;
wall_top_z=32.2; tool_hole_pitch=40; tool_hole_z=20;
bolt_d=4.5; // M4 clearance through the existing nominal 5 mm tool holes
mount_plate_t=4; arm_w=10; arm_h=4.3;
case_stop_y=8.5; case_stop_z=36.5; // initial contact setting only; case is provisional
case_stop_depth=13.5; adjuster_y=18; // retain the existing screw axes
case_stop_width=10; adjuster_d=4.5; adjuster_nut_af=7.2;
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
// Print backing face Y=35 down (X=-90). Local -Y is the upward roof.
module upward_roof(d){
 r=d/2/cos(180/32);
 union(){circle(r=r,$fn=32);polygon([[-r/sqrt(2),-r/sqrt(2)],[0,-r/sqrt(2)*(1+tan(55))],[r/sqrt(2),-r/sqrt(2)]]);}
}
module adjuster_hole() ef_cut(arm_h+0.04,0.2)upward_roof(adjuster_d);
module nut_profile(){
 r=adjuster_nut_af/2/cos(30);
 union(){rotate(-30)ef_hex(adjuster_nut_af);
  polygon([[-adjuster_nut_af/2,-r/2],[0,-r/2-adjuster_nut_af/2*tan(55)],[adjuster_nut_af/2,-r/2]]);}
}
module one_stop() {
 difference() {
  union() {
   // Backing strip sits on the existing wall's outer face (y=31..35).
   // 52 mm strip gives the x=±20 holes 6 mm of edge distance.
   translate([-26,wall_front_y,15])rbox([52,mount_plate_t,case_stop_z-15],2,"y");
   // Constant-width risers grow directly from the bed-facing backing strip.
   for(s=[-1,1]) {
    translate([s*tool_hole_pitch/2-arm_w/2,case_stop_y+case_stop_depth-1,
               wall_top_z])
     rbox([arm_w,wall_front_y-(case_stop_y+case_stop_depth)+2,
           case_stop_z-wall_top_z],1.2,"y");
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
   translate([x,adjuster_y,case_stop_z-arm_h-0.02])
    linear_extrude(adjuster_nut_h+0.02)nut_profile();
   translate([x,adjuster_y,case_stop_z-arm_h-0.02]) adjuster_hole();
  }
 }
}
module rbox(s,r=2,axis="z") {
 if(axis=="z") translate([s[0]/2,s[1]/2,0]) ef_box(s[0],s[1],s[2],r,edge_c);
 if(axis=="y") translate([0,s[1],0]) rotate([90,0,0])
  translate([s[0]/2,s[2]/2,0]) ef_box(s[0],s[2],s[1],r,edge_c);
}
one_stop();
'''
