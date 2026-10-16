// TD04A exterior reconstructed from user photos and uncalibrated scan.
// mm; front face Z=0; +Z rearward; X width; Y height above bottom.
// Approximate dimensions only. Not manufacturer CAD or a certified fit model.
/* [Scan estimated body] */
width = 46;
height = 48;
depth = 20;
lip = 2;
/* [Photo estimated details] */
mount_width = 22;
mount_height = 20;
mount_depth = 5;
screw_pitch = 12;
screw_d = 4;
boot_d = 9;
boot_length = 7;
cable_d = 5;
cable_stub = 25;
show_bracket = true;
bracket_width = 24;
bracket_thickness = 2;
bracket_reach = 48;
slot_w = 4;
slot_length = 15;
$fn=96;
assert(width>0 && height>=width/2 && depth>lip && lip>0);
assert(mount_width>screw_pitch+screw_d && mount_height>screw_d);
assert(bracket_reach>slot_length+15 && bracket_thickness>0);
assert(boot_d>cable_d && cable_d>0 && boot_length>0 && cable_stub>0);
module outline(w,h){
 union(){
  translate([-w/2,0]) square([w,h-w/2]);
  translate([0,h-w/2]) intersection(){circle(d=w);translate([-w/2,0])square([w,w/2]);}
 }
}
module bracket(){
 // Bent sheet approximation: low mounting foot and sloping neck.
 difference(){
  translate([-bracket_width/2,0,depth+mount_depth]) rotate([90,0,90])
   linear_extrude(height=bracket_width)
    polygon([[0,bracket_reach],[0,bracket_reach-18],[17,0],[19,0],[bracket_thickness,bracket_reach-18],[bracket_thickness,bracket_reach]]);
  translate([0,bracket_thickness/2,depth+mount_depth+bracket_reach-9])
   union(){
    cube([slot_length-slot_w,bracket_thickness+2,slot_w],center=true);
    for(x=[-(slot_length-slot_w)/2,(slot_length-slot_w)/2])
     translate([x,0,0])rotate([90,0,0])cylinder(d=slot_w,h=bracket_thickness+2,center=true);
   }
 }
}
module td04a_transducer(){
 union(){
  linear_extrude(height=lip) outline(width,height);
  translate([0,1,lip-.1])linear_extrude(height=depth-lip+.1)outline(width-2,height-2);
  translate([-mount_width/2,8,depth-.1])cube([mount_width,mount_height,mount_depth+.1]);
  for(x=[-screw_pitch/2,screw_pitch/2])translate([x,18,depth+mount_depth-.1])cylinder(d=screw_d+3,h=2.1);
  translate([0,height-boot_d/2-3,depth-.1])cylinder(d1=boot_d,d2=cable_d+1,h=boot_length+.1);
  translate([0,height-boot_d/2-3,depth+boot_length-.1])cylinder(d=cable_d,h=cable_stub+.1);
  if(show_bracket) bracket();
 }
}
td04a_transducer();
