// Parent oneplate TD04A support with flat frame seat and bracket datums.
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
