// CHILD-SIMPLE-M3-40x40 Rev.1 -> existing 22 x 32 M5 camera base.
// Assembly coordinates match camera_mount.scad. Print with +X up.
part="print"; // [print,assembly]
width=60; thickness=8;
rear_y=-60.45; shelf_front=23;
pad_center_z=40; pitch=40; pad_height=60;
m3_d=3.45; m5_d=5.4;
$fn=64; eps=0.02;
assert(width/2-pitch/2>m3_d/2+4);
assert(pad_center_z-pitch/2-5>8,"Bottom M3 tool clears camera base");
// All horizontal bores get a 45 degree roof facing +X (print up).
module roof2d(d) {
 r=d/2/cos(180/32);
 polygon(concat([for(a=[135:11.25:405]) [r*cos(a),r*sin(a)]],[[0,r*sqrt(2)]]));
}
module bore_y(x,y,z,d,h) {
 translate([x,y,z]) multmatrix([[0,1,0,0],[0,0,1,0],[1,0,0,0],[0,0,0,1]]) linear_extrude(h) roof2d(d);
}
module bore_z(x,y,z,d,h) {
 translate([x,y,z]) rotate([0,0,-90]) linear_extrude(h) roof2d(d);
}
module adapter() {
 difference() {
  union() {
   translate([-width/2,rear_y,-thickness]) cube([width,shelf_front-rear_y,thickness]);
   translate([-width/2,rear_y,0]) cube([width,thickness,pad_center_z+pad_height/2]);
  }
  for(x=[-pitch/2,pitch/2],z=[pad_center_z-pitch/2,pad_center_z+pitch/2])
   bore_y(x,rear_y-eps,z,m3_d,thickness+2*eps);
  for(x=[-11,11],y=[-16,16]) bore_z(x,y,-thickness-eps,m5_d,thickness+2*eps);
 }
}
if(part=="assembly") adapter();
else translate([0,0,width/2]) rotate([0,-90,0]) adapter();
