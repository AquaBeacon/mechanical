// Parent oneplate TD04A support with frame key and bracket locating seat.
// Units mm. TD bracket width and end position are provisional values from the
// current visual proxy; verify against the metal bracket before final use.
use <../../../../../scad/lib/edge_finished_profiles.scad>
$fn=48;
wall=8; x0=25; width=80; rear_y=-67; top_z=-12; bottom_z=-54;
td_x=55; td_z=-35; pitch=36;
frame_key=11.6; frame_key_r=1.2; frame_key_h=1.95;
frame_key_xy=[75,-55]; frame_recess=12; // 0.2 mm clearance per side
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
  polygon([[r/sqrt(2),-r/sqrt(2)],[sqrt(2)*r,0],[r/sqrt(2),r/sqrt(2)]]);
 }
}
module key_profile() translate(frame_key_xy) ef_round_rect(frame_key,frame_key,frame_key_r);
module main_support() {
 difference() {
  union() {
   // Preserve the existing 80 x 67 x 42 mm support envelope below Z=-12.
   translate([x0,rear_y,top_z-wall]) rbox([width,-rear_y,wall],2);
   translate([x0,-wall,bottom_z]) rbox([width,wall,top_z-bottom_z],2,"y");
   // Registration key enters the frame's 12 x 12 x 2 mm underside recess.
   translate([0,0,top_z-0.1]) ef_convex_profile(frame_key_h,0.3) key_profile();
   // Left bracket datum (contact at x=43) and top-end insertion stop (z=-27).
   translate([td_bracket_left-datum_t,-0.2,td_bracket_top-16])
    rbox([datum_t,datum_y,18],datum_r,"y");
   translate([td_bracket_left+2,-0.2,td_bracket_top])
    rbox([td_bracket_width-4,datum_y,2],datum_r,"y");
   // Fixed right cheek leaves a 0.4 mm nominal shim allowance for bracket width.
   translate([td_bracket_left+td_bracket_width+td_bracket_gap,-0.2,td_bracket_top-16])
    rbox([datum_t,datum_y,18],datum_r,"y");
  }
  // Original M5 carrier attachment: x=65/85, y=-55, vertical axis.
 for(x=[65,85]) translate([x,-55,top_z-wall-0.02]) {
  roof(5.5,wall+0.04,-90);
  translate([0,0,-0.01]) cylinder(d1=6.1,d2=5.5,h=0.31,$fn=32);
  translate([0,0,wall-0.30]) cylinder(d1=5.5,d2=6.1,h=0.31,$fn=32);
 }
  // Original M4 TD clamp holes: x=37/73, z=-35, axis Y.
  for(x=[td_x-pitch/2,td_x+pitch/2])
   translate([x,-wall-0.02,td_z]) rotate([-90,0,0]) fit_hole(4.5,wall+0.04);
 }
}
main_support();
