// Parent modular exterior v2. mm. Geometry shared by individual part wrappers.
// Metal fasteners, ballast, Takachi box and electronics are purchased items.
/* [Dimensions] */
disk_d=225; disk_t=5;
fin_h=125; fin_w=65; fin_t=4;
beam_w=32; clearance=0.5;
float_r=100; flange_r=112.5; float_bore_r=30;
float_wall=4; float_h=180; lid_t=6;
rod_r=105.5; flange_t=6;
hub_h=32; root_x=30; root_depth=14;
$fn=96; e=0.03;
assert(disk_d<=225 && 2*flange_r<=225);
assert(fin_h>=100 && fin_h<=150 && fin_w>=50 && fin_w<=80);
assert(root_x+fin_w<disk_d/2-5);
module bore(d,h) { cylinder(d=d/cos(180/32),h=h,$fn=32); }
module bore_x(d,l) { rotate([0,90,0]) bore(d,l); }
module bore_y(d,l) { rotate([-90,0,0]) bore(d,l); }
module square_bore(h) { translate([-(beam_w+clearance)/2,-(beam_w+clearance)/2,-e]) cube([beam_w+clearance,beam_w+clearance,h+2*e]); }
module rods(h,d=6.5) { for(a=[45:90:315]) rotate([0,0,a]) translate([rod_r,0,-e]) bore(d,h+2*e); }
module lid_bolts(h) { for(a=[22.5:45:359]) rotate([0,0,a]) translate([rod_r,0,-e]) bore(4.5,h+2*e); }
module hub_pin(z) { translate([-46,10,z]) bore_x(6.5,92); }
module disk() {
 difference() { cylinder(d=disk_d,h=disk_t); square_bore(disk_t);
  for(x=[-23,23],y=[-23,23]) translate([x,y,-e]) bore(5.5,disk_t+2*e);
 }
}
module fin() {
 difference() { cube([fin_w,fin_t,fin_h]);
  for(z=[10,fin_h-hub_h+10]) translate([root_depth/2,-e,z]) bore_y(5.5,fin_t+2*e);
 }
}
module hub() {
 difference() {
  union() { translate([-30,-30,0]) cube([60,60,hub_h]);
   for(a=[0:90:270]) rotate([0,0,a]) translate([28,-16,0]) cube([16,32,hub_h]);
  }
  square_bore(hub_h);
  for(a=[0:90:270]) rotate([0,0,a]) {
   translate([root_x-clearance/2,-(fin_t+clearance)/2,-e]) cube([root_depth+clearance,fin_t+clearance,hub_h+2*e]);
   translate([root_x+root_depth/2,-17,10]) bore_y(5.5,34);
  }
  for(x=[-23,23],y=[-23,23]) translate([x,y,-e]) bore(5.5,hub_h+2*e);
  hub_pin(24);
 }
}
module beam(lower=true) {
 len=lower?180:107;
 difference() { translate([-beam_w/2,-beam_w/2,0]) cube([beam_w,beam_w,len]);
  if(lower) { for(z=[24,117]) hub_pin(z); translate([-20,0,160]) bore_x(6.5,40); translate([0,0,-e]) bore(16,8); }
  else for(z=[20,87]) translate([-20,0,z]) bore_x(6.5,40);
 }
}
module coupler() {
 // One half of a screwed split coupler. Mirror Y for the second half.
 difference() { translate([-27,0.25,0]) cube([54,26.75,64]); square_bore(64);
  for(z=[12,52]) translate([-28,0,z]) bore_x(6.5,56);
  for(x=[-22,22],z=[24,40]) translate([x,-1,z]) bore_y(5.5,29);
 }
}
module float_body() {
 difference() {
  union() { cylinder(r=float_r,h=float_h);
   translate([0,0,float_h-flange_t]) cylinder(r=flange_r,h=flange_t);
   // 45-degree underside of the flange instead of a 15 mm unsupported ledge.
   translate([0,0,float_h-flange_t-(flange_r-float_r)]) cylinder(r1=float_r,r2=flange_r,h=flange_r-float_r);
  }
  translate([0,0,-e]) cylinder(r=float_bore_r,h=float_h+2*e);
  translate([0,0,float_wall]) difference() {
   cylinder(r=float_r-float_wall,h=float_h);
   cylinder(r=float_bore_r+float_wall,h=float_h+e);
  }
  // Coupling-nut clearance; nearest cavity wall remains >=3 mm thick.
  rods(float_h,13); lid_bolts(float_h);
  for(a=[22.5:45:359]) rotate([0,0,a]) translate([rod_r,0,-e]) bore(10,float_h-flange_t+e);
 }
}
module float_lid() {
 difference() {
  cylinder(r=flange_r,h=lid_t);
  translate([0,0,-e]) cylinder(r=float_bore_r,h=lid_t+2*e);
  rods(lid_t,13); lid_bolts(lid_t);
  // Continuous face seals: 2 mm cord, 2.4 wide x 1.5 deep grooves.
  for(r=[float_bore_r+float_wall/2,float_r-float_wall/2]) translate([0,0,-e]) difference() {
   cylinder(r=r+1.2,h=1.5+e); cylinder(r=r-1.2,h=1.5+2*e);
  }
 }
}
module float_end(top=true) {
 difference() {
  union() { cylinder(r=flange_r,h=8);
   if(top) translate([-30,-30,8-e]) cube([60,60,20+e]);
   else translate([-23,-23,-40]) cube([46,46,40+e]);
  }
  rods(8);
  if(top) for(x=[-20,20],y=[-20,20]) {
   translate([x,y,-e]) bore(5.5,29);
   translate([x,y,-e]) bore(11,18+e);
  }
  if(top) for(a=[22.5:45:359]) rotate([0,0,a]) translate([rod_r,0,-e]) bore(12,8+2*e);
  else { translate([0,0,-40]) square_bore(40-e);
   translate([-24,0,-20]) bore_x(6.5,48);
  }
 }
}
module ballast_body() {
 // Open upward in print orientation. In the assembly this cup is inverted.
 difference() {
  union() { cylinder(r=45,h=51); translate([0,0,45]) cylinder(r=60,h=6);
   translate([0,0,30]) cylinder(r1=45,r2=60,h=15);
  }
  translate([0,0,6]) cylinder(r=40,h=46);
  for(x=[-23,23],y=[-23,23]) translate([x,y,-e]) bore(5.5,7);
  translate([0,0,-e]) bore(8.5,7);
  for(a=[0:90:270]) rotate([0,0,a]) translate([52,0,29]) { bore(5.5,23); bore(12,16); }
 }
}
module ballast_lid() {
 difference() { cylinder(r=60,h=6);
  for(a=[0:90:270]) rotate([0,0,a]) translate([52,0,-e]) bore(5.5,7);
  // Flooded ballast compartment: drainage, no trapped air assumption.
  for(x=[-20,0,20]) translate([x,0,-e]) bore(6,7);
 }
}
module camera_bridge() {
 // Assembly frame: local top z=78; camera seat z=8. +Y faces camera front.
 difference() {
  union() {
   translate([-30,45,70]) cube([60,90,8]);
   translate([-70,125,0]) cube([140,100,8]);
   translate([-70,125,0]) cube([140,10,78]);
   for(x=[-64,56]) translate([x,0,0]) rotate([90,0,90]) linear_extrude(8)
    polygon([[135,8],[215,8],[135,70]]);
  }
  for(x=[-20,20],y=[50,90]) translate([x,y,69]) bore(5.5,10);
  for(x=[-11,11],y=[174,206]) translate([x,y,-e]) bore(5.5,10);
 }
}
module gps_bridge() {
 // Local attachment face X=0 at deck +X; top shelf z=175.
 difference() {
  union() { translate([0,-25,0]) cube([10,50,183]);
   translate([-90,-48,175]) cube([100,96,8]);
   for(y=[-17,25]) translate([0,y,0]) rotate([90,0,0]) linear_extrude(8)
    polygon([[e,155],[e,175+e],[-80,175+e]]);
  }
  for(y=[-20,20],z=[5,45]) translate([-e,y,z]) bore_x(5.5,11);
  for(y=[-34,34]) translate([-43,y,174]) bore(4.5,10);
 }
}
// Reference antenna envelope, correct mounting ears, not a printable antenna.
module gps_reference() {
 difference() {
  union() { translate([-30,-28,0]) cube([60,56,22.5]);
   translate([-10,-41,0]) cube([20,82,6]); }
  for(y=[-34,34]) translate([0,y,-e]) bore(4.5,7);
 }
}
