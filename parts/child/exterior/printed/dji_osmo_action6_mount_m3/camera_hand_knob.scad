// Hand knob for ordinary M3x30 hex head. Direct metal bearing is replaced by
// a 1 mm PETG floor in the clamp load path. Snap cap is retention only.
use <../../../../../scad/lib/edge_finished_profiles.scad>
$fn=64;
knob_d=20; knob_h=3.8; floor_t=1;
head_af=5.8; head_top=3.15; edge_chamfer=.2;
cap_bore_d=12; cap_groove_d=12.4;
module camera_hand_knob(){
 difference(){
  ef_convex_profile(knob_h,edge_chamfer) circle(d=knob_d,$fn=64);
  translate([0,0,-.01]) ef_poly_bore(3.6,floor_t+.03,.2,8);
  translate([0,0,floor_t+.1]) ef_cut(head_top-floor_t-.1,.12) ef_hex(head_af);
  translate([0,0,2.98]) cylinder(d=cap_bore_d,h=1,$fn=64);
  translate([0,0,3.1]) cylinder(d=cap_groove_d,h=.35,$fn=64);
  // Shallow fingertip scallops stay within the 20 mm outside envelope.
  for(a=[0:30:330]) rotate(a) translate([10.6,0,-.01])
   ef_cut(knob_h+.02,.15) circle(d=2,$fn=32);
 }
}
camera_hand_knob();
