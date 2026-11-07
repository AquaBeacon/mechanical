// Slotted snap cap: four independent arc arms; cap carries no clamp preload.
// PETG arm flex and fatigue are not certified by the geometric model.
use <../../../../../scad/lib/edge_finished_profiles.scad>
$fn=64;
cap_h=.8; core_r=3.5; arm_inner=4.1; arm_outer=5.85;
arm_span=78; arm_round=.15; cap_chamfer=.1;
module annular_arc(start,span){
 polygon(concat([for(a=[start:3:start+span]) [arm_outer*cos(a),arm_outer*sin(a)]],
                [for(a=[start+span:-3:start]) [arm_inner*cos(a),arm_inner*sin(a)]]));
}
module camera_hand_knob_cap(){
 union(){
  ef_convex_profile(cap_h,cap_chamfer) circle(r=core_r,$fn=64);
  for(a=[0,90,180,270]) rotate(a){
   // Rounded arc is anchored at its start and free at the nub end.
   ef_profile(cap_h,cap_chamfer) offset(r=arm_round) offset(delta=-arm_round) annular_arc(0,arm_span);
   translate([3.75,0,0]) ef_box(1,1.2,cap_h,.2,.1);
   rotate(75) translate([5.95,0,.15]) ef_box(.4,1,.25,.08,.05);
  }
 }
}
camera_hand_knob_cap();
