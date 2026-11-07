use <camera_left_clamp.scad>
// DJI osmo Action 6固定部品: rear plate + front support, one FDM solid.
// mm; +Y camera front; X screw axis; Z print up. Case shape provisional.
use <../../../../../scad/lib/edge_finished_profiles.scad>
show_case=false;
rear_bottom_keepout=20; // user: clear rear hinge/lower projection
rear_bottom_margin=.5; // additional manufacturing clearance
support_front_margin=1; // support stays within existing base
rear_support_width=12; rear_support_x=32;
rear_support_tip_t=6; support_edge_chamfer=0.6;
support_driver_d=12; // straight shaft/head access; large thumbscrews need fit check

tab_t=3; tab_gap=3; case_hole=5; body_to_axis=12.5;
fit=0.3; hole_allow=0.2;
case_w=95; case_d=45.9; case_h=75;
rear_gap=0.5; // fit with measured shim/liner, not an operating gap
base_side_margin=2; compact_front_margin=2;
base_edge_r=2; base_edge_chamfer=.6;
base_t=8; axis_z=24;
plate_w=84; plate_t=8; plate_above_bottom=48;
base_w=plate_w+2*base_side_margin;
rear_gusset_run=18; gusset_t=6; gusset_x=38;
// Outer front rotation-stop wall removed by user request.
// Front pads replaced by rear-origin case supports.

lug_r=7; nut_side_t=6; head_side_t=3;
nut_af=8.2; nut_depth=4.2; tool_r=14;
// CHILD-SIMPLE-M3-40x40 Rev.1: direct rear attachment.
mount_pitch=40; mount_center_z=40; mount_d=3.45;
head_d=6.8; head_depth=3.6; rear_clear_half=31;
$fn=64; eps=0.02;
assert(gusset_x-gusset_t/2>rear_clear_half);
assert(plate_t-head_depth>=4);
assert(mount_center_z-mount_pitch/2-head_d/2>base_t);
assert(mount_center_z+mount_pitch/2+head_d/2<84.5);
// Polygon roof points up in the Z print direction; circular clearance retained.
module roof_bore_y(x,y,z,d,depth) {
 r=d/2/cos(180/24);
 translate([x,y+eps,z]) rotate([90,0,0]) linear_extrude(depth+eps)
 polygon(concat([for(a=[135:15:405]) [r*cos(a),r*sin(a)]],[[0,r*sqrt(2)]]));
}
module rear_bore(x,z,d,depth) { roof_bore_y(x,rear_face,z,d,depth); }
mid=tab_gap-fit; slot=tab_t+fit;
stack=nut_side_t+2*slot+mid+head_side_t;
left=-(slot+mid/2+nut_side_t);
body_z=axis_z+body_to_axis;

rear_face=-case_d/2-rear_gap; rear_back=rear_face-plate_t;
base_y0=rear_back-rear_gusset_run-3;
base_y1=lug_r+compact_front_margin;
plate_top=body_z+plate_above_bottom;
assert(mid>0 && nut_depth<nut_side_t-1);
assert(axis_z-tool_r>base_t);
assert(plate_above_bottom<case_h-15);
assert(gusset_x+gusset_t/2<plate_w/2);

assert(rear_gap>=0);
module hole(d,h) { cylinder(d=d/cos(180/32),h=h,$fn=32); }
module roof_hole_x(d,h) {
 r=d/2;
 rotate([0,90,0]) linear_extrude(h) union() {
  circle(r=r/cos(180/32),$fn=32);
  polygon([[-sqrt(2)*r,0],[-r/sqrt(2),r/sqrt(2)],[-r/sqrt(2),-r/sqrt(2)]]);
 }
}
module rear_gusset(x) {
 translate([x-gusset_t/2,0,0])
 multmatrix([[0,0,1,0],[1,0,0,0],[0,1,0,0],[0,0,0,1]])
 ef_convex_profile(gusset_t,.6) offset(r=1) offset(delta=-1) polygon([[rear_back-rear_gusset_run,base_t],[rear_back+eps,base_t],[rear_back+eps,plate_top-8]]);
}
// Modest reliefs: roof slopes exceed 55 degrees above the bed.
module roof_window_y(w,z0,shoulder) {
 translate([0,rear_back+plate_t/2,0]) rotate([90,0,0])
 linear_extrude(plate_t+2*eps,center=true)
 polygon([[-w/2,z0],[w/2,z0],[w/2,shoulder],[0,shoulder+w*0.8],[-w/2,shoulder]]);
}
module body() {
 difference() {
  union() {
   translate([0,(base_y0+base_y1)/2,0])
    ef_box(base_w,base_y1-base_y0,base_t,base_edge_r,base_edge_chamfer);
   rounded_solid([-plate_w/2,rear_back,base_t],[plate_w,plate_t,plate_top-base_t],1);
   for(s=[-1,1]) rear_gusset(s*gusset_x);

   // Former left/right bottom supports removed; front/rear jaws stop rotation.
   // Minimum screw fingers only: rear under-case pedestal removed.
   starts=[left,-mid/2,mid/2+slot]; ts=[nut_side_t,mid,head_side_t];
   for(i=[0:2]) {
    translate([starts[i],-lug_r,base_t]) cube([ts[i],2*lug_r,axis_z-base_t]);
    translate([starts[i],0,axis_z]) rotate([0,90,0]) cylinder(r=lug_r,h=ts[i]);
   }
  }
  roof_window_y(36,34,43);
  // Clear the original rear base overhang so the rear face sits flush on the frame.
  translate([-rear_clear_half,base_y0-eps,-eps])
   cube([2*rear_clear_half,rear_back-base_y0+eps,base_t+2*eps]);
  for(x=[-mount_pitch/2,mount_pitch/2],z=[mount_center_z-mount_pitch/2,mount_center_z+mount_pitch/2]) {
   rear_bore(x,z,mount_d,plate_t+2*eps);
   // Recess M3 socket heads below the existing camera contact surface.
   rear_bore(x,z,head_d,head_depth);
  }
  // Front M3 tool access is open; front wall and its floor slots removed.
  translate([left-eps,0,axis_z]) roof_hole_x(case_hole+hole_allow,stack+2*eps);
  translate([left-eps,0,axis_z]) rotate([0,90,0]) cylinder(d=nut_af/cos(30),h=nut_depth+eps,$fn=6);
  // Obsolete underside M5 attachment and its tool recesses removed.
 }
}
module camera_mount() { difference() { union() { body(); clamp_base(); } clamp_base_holes(); } }
color("SteelBlue") camera_mount();
if(show_case) %translate([-case_w/2,-case_d/2,body_z]) cube([case_w,case_d,case_h]);
