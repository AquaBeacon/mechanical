"""Rev.2 additions; existing C twist mating geometry is used without modification."""
from parent_oneplate_frame_sources import HEADER

def bar_source():
    return HEADER + r'''
// One-piece upper clamp: retained beams and four M5 axes, joined by side rails.
// Flat bed face Z=0. Open centre keeps the middle of the lid accessible.
bar_w=244; bar_d=36; bar_t=20; rail_w=16; rail_x=98;
module clamp_plan(){
 ef_plan_finish(4)union(){
  for(y=[-po_rod_y,po_rod_y])translate([0,y])ef_round_rect(bar_w,bar_d,4);
  for(x=[-rail_x,rail_x])translate([x,0])square([rail_w,2*po_rod_y],center=true);
 }
}
difference(){
 ef_profile(bar_t,0.6)clamp_plan();
 for(x=[-po_rod_x,po_rod_x])for(y=[-po_rod_y,po_rod_y])
  translate([x,y,0])bore(5.5,bar_t);
}
'''

def stand_source():
    return HEADER + r'''
// Two identical skids. Model local X=0; top Z=-20; ground Z=-72.
// Print on the X side (Y90); bolt/nut access remains between the feet.
stand_width=20; stand_length=180; stand_drop=52;
module side_profile(){
 ef_plan_finish(2)union(){
  translate([-90,-30])square([180,10]);
  for(s=[-1,1])hull(){
   translate([s*75,-27])circle(r=3,$fn=32);
   translate([s*75,-62])circle(r=7,$fn=32);
   translate([s*60,-27])circle(r=3,$fn=32);
  }
  for(s=[-1,1])translate([s*75-15,-72])square([30,10]);
 }
}
difference(){
 translate([-stand_width/2,0,0])multmatrix([[0,0,1,0],[1,0,0,0],[0,1,0,0],[0,0,0,1]])
 ef_profile(stand_width,0.6)side_profile();
 // Single polygon avoids tangential circle/triangle slivers. -X becomes +Z
 // after manufacturing Y90 rotation, so the roof points up on the bed.
 for(y=[-po_rod_y,po_rod_y])translate([-6,y,-30])ef_cut(10,0.3)
  rotate(180)let(r=2.75/cos(180/32))polygon(concat(
   [for(a=[45:11.25:315])[r*cos(a),r*sin(a)]],[[sqrt(2)*r,0]]));
 // Clear existing rope eyes; keep a continuous 9 mm outer spine.
 for(y=[-31,31])translate([-16,y,-43])ef_box(34,34,24,2,0.4);
 // Socket access below each rod nut, clear of the diagonal leg roots.
 for(y=[-po_rod_y,po_rod_y])translate([-6,y,-73])bore(12,43);
}
'''

def qr_source():
    return HEADER + r'''
use <../../../../common/jigs/quick_release_prototypes/quick_release_prototypes.scad>
use <../../../../../scad/lib/camera_rotary_joint.scad>
part="female"; // [female,male]
adapter_w=60; adapter_t=part=="female"?10:6;
// The 10 mm adapter preserves the exterior mounting face and 40 mm axes.
// The camera-only rotary receiver has two axial clamp ears.
module adapter(){
 difference(){
  translate([0,0,-adapter_t])ef_box(adapter_w,adapter_w,adapter_t+0.05,3,0.5);
  for(x=[-20,20],y=[-20,20])translate([x,y,-adapter_t])bore(3.5,adapter_t+0.05);
 }
}
if(part=="female")difference(){
 union(){camera_qr_female();adapter();}
 // Socket heads are outside the C mating ring; insert bolts before mating.
 for(x=[-20,20],y=[-20,20])translate([x,y,-2.5])bore(6.8,6.5);
}
else if(part=="male")difference(){
 union(){twist_male();adapter();}
 // Open nut seats on the opposite side of the camera contact face.
 for(x=[-20,20],y=[-20,20])translate([x,y,-2.6])nut(5.7,6.7);
 for(x=[-20,20],y=[-20,20])translate([x,y,-6])bore(3.5,12.1);
}
else assert(false,"Unknown QR variant");
'''
