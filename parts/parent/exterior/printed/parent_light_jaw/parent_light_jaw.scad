// Sandwich the existing metal TD04A bracket, not the sensor body.
width=50; height=14; thick=8; bolt_pitch=36; bolt_d=4.5;
$fn=48;
assert(bolt_pitch/2-bolt_d/2>12+2);
difference(){
 translate([-width/2,0,-height/2])rb([width,thick,height],2,"y");
 for(x=[-bolt_pitch/2,bolt_pitch/2])translate([x,-.02,0])rotate([-90,0,0])cylinder(d=bolt_d/cos(180/32),h=thick+.04,$fn=32);
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
