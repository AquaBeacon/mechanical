// Open lower clamp frame; box bottom Z=0. mm.
width=236; depth=236; rail=24; thick=12;
clamp_x=112; clamp_y=55;
lug_y=85; lug_hole=10.5; lug_z=-26;
carrier_x=[65,85];
$fn=48;
module hole(d,h){cylinder(d=d/cos(180/32),h=h,$fn=32);}
assert(rail>=24 && thick>=12);
assert(clamp_x+5<width/2);
difference(){
 union(){
  // Horizontal camera attachment integrated with frame; M3 40x40 rear mount.
  translate([-70,-67,-12])difference(){
   rb([60,134,12],3);
   translate([18,17,-.02])rb([24,100,12.04],3);
  }
  for(x=[-60,-20],y=[-20,20])translate([x,y,-24])cylinder(d=12,h=14,$fn=48);

  // Four integral downward lugs, below the box for nut/rope access.
  for(x=[-118,110],y=[-lug_y,lug_y])translate([x,y-16,-42])rb([8,32,32],3,"x");
  for(x=[-width/2,width/2-rail])translate([x,-depth/2,-thick])rb([rail,depth,thick],3);
  for(y=[-clamp_y,clamp_y])translate([-width/2,y-rail/2,-thick])rb([width,rail,thick],3);
 }
 for(x=[-clamp_x,clamp_x]){
  for(y=[-clamp_y,clamp_y])translate([x,y,-thick-.02])hole(5.5,thick+.04);

 }
 for(x=[-118,110],y=[-lug_y,lug_y])translate([x-.02,y,lug_z])rotate([0,90,0])roof(lug_hole,8.04);
 // Through-windows leave 7 mm ribs; keep bolt-bearing zones solid.
 for(x=[-111,101])translate([x,-30,-thick-.02])rb([10,60,thick+.04],3);
 for(y=[-clamp_y,clamp_y])translate([-54,y-5,-thick-.02])rb([108,10,thick+.04],3);
 // M3 heat-set insert pilots open toward existing mount; 7 mm deep.
 for(x=[-60,-20],y=[-20,20])translate([x,y,-24.02])hole(4.2,7.02);
 for(x=carrier_x){
  translate([x,-clamp_y,-thick-.02])hole(5.5,thick+.04);
  translate([x,-clamp_y,-2.45])cylinder(d1=5.5/cos(180/32),d2=10.4/cos(180/32),h=2.45+.02,$fn=32); // recessed M5 head; box stays flat
 }
}

// Rounded profile extrusions preserve planar mating faces and bed contact.
module rz(s,r){
 assert(r>0 && 2*r<min(s[0],s[1]));
 union(){
  translate([r,0,0])cube([s[0]-2*r,s[1],s[2]]);
  translate([0,r,0])cube([s[0],s[1]-2*r,s[2]]);
  for(x=[r,s[0]-r],y=[r,s[1]-r])translate([x,y,0])cylinder(r=r,h=s[2],$fn=32);
 }
}
module rb(s,r=2,axis="z"){
 if(axis=="z")rz(s,r);
 if(axis=="y")translate([0,s[1],0])rotate([90,0,0])rz([s[0],s[2],s[1]],r);
 if(axis=="x")translate([0,0,s[2]])rotate([0,90,0])rz([s[2],s[1],s[0]],r);
}
// +X peak; rotate in bore plane so peak points upward in the supplied print STL.
module roof(d,h,angle=0){
 r=d/2/cos(180/32);
 rotate([0,0,angle])linear_extrude(height=h)union(){
  circle(r=r,$fn=32);
  polygon([[r/sqrt(2),-r/sqrt(2)],[sqrt(2)*r,0],[r/sqrt(2),r/sqrt(2)]]);
 }
}
