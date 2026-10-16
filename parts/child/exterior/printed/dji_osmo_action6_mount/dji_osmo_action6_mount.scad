// DJI osmo Action 6固定部品: rear plate + front support, one FDM solid.
// mm; +Y camera front; X screw axis; Z print up. Case shape provisional.
show_case=false;
tab_t=3; tab_gap=3; case_hole=5; body_to_axis=12.5;
fit=0.3; hole_allow=0.2;
case_w=95; case_d=45.9; case_h=75;
rear_gap=0.5; // fit with measured shim/liner, not an operating gap
base_w=104; base_t=8; axis_z=24;
plate_w=84; plate_t=8; plate_above_bottom=48;
rear_gusset_run=18; gusset_t=8; gusset_x=30;
front_y=19; front_wall_t=8; front_span=84;
front_pad_w=16; front_pad_d=6; front_pad_x=30;
front_pad_raise=4; front_gap=0.3;
lug_r=7; nut_side_t=6; head_side_t=3;
nut_af=8.2; nut_depth=4.2; tool_r=14;
$fn=64; eps=0.02;
mid=tab_gap-fit; slot=tab_t+fit;
stack=nut_side_t+2*slot+mid+head_side_t;
left=-(slot+mid/2+nut_side_t);
body_z=axis_z+body_to_axis;
contact_z=body_z-front_gap;
front_top=contact_z-front_pad_raise;
rear_face=-case_d/2-rear_gap; rear_back=rear_face-plate_t;
base_y0=rear_back-rear_gusset_run-3;
base_y1=front_y+front_wall_t/2+4;
plate_top=body_z+plate_above_bottom;
assert(mid>0 && nut_depth<nut_side_t-1);
assert(front_y-front_wall_t/2>tool_r && axis_z-tool_r>base_t);
assert(plate_above_bottom<case_h-15);
assert(gusset_x+gusset_t/2<plate_w/2);
assert(front_pad_x+front_pad_w/2<front_span/2);
assert(rear_gap>=0 && front_gap>=0);
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
 linear_extrude(gusset_t)
 polygon([[rear_back-rear_gusset_run,base_t],[rear_back+eps,base_t],[rear_back+eps,plate_top-8]]);
}
module body() {
 difference() {
  union() {
   translate([-base_w/2,base_y0,0]) cube([base_w,base_y1-base_y0,base_t]);
   translate([-plate_w/2,rear_back,base_t]) cube([plate_w,plate_t,plate_top-base_t]);
   for(s=[-1,1]) rear_gusset(s*gusset_x);
   translate([-front_span/2,front_y-front_wall_t/2,base_t]) cube([front_span,front_wall_t,front_top-base_t]);
   for(s=[-1,1]) translate([s*front_pad_x-front_pad_w/2,front_y-front_pad_d/2,front_top]) cube([front_pad_w,front_pad_d,front_pad_raise]);
   // Minimum screw fingers only: rear under-case pedestal removed.
   starts=[left,-mid/2,mid/2+slot]; ts=[nut_side_t,mid,head_side_t];
   for(i=[0:2]) {
    translate([starts[i],-lug_r,base_t]) cube([ts[i],2*lug_r,axis_z-base_t]);
    translate([starts[i],0,axis_z]) rotate([0,90,0]) cylinder(r=lug_r,h=ts[i]);
   }
  }
  translate([left-eps,0,axis_z]) roof_hole_x(case_hole+hole_allow,stack+2*eps);
  translate([left-eps,0,axis_z]) rotate([0,90,0]) cylinder(d=nut_af/cos(30),h=nut_depth+eps,$fn=6);
  for(x=[-11,11],y=[-16,16]) {
   translate([x,y,-eps]) hole(5.4,base_t+2*eps);
   translate([x,y,base_t]) hole(10.4,plate_top);
  }
 }
}
color("SteelBlue") body();
if(show_case) %translate([-case_w/2,-case_d/2,body_z]) cube([case_w,case_d,case_h]);
