// TD04A support only. Camera has no angle bracket.
wall=8; x0=20; width=85; rear_y=-67; top_z=-12; bottom_z=-54;
td_x=55; td_z=-35; pitch=36;
$fn=48;
module hole(d,h){cylinder(d=d/cos(180/32),h=h,$fn=32);}
difference(){
 union(){
  translate([x0,rear_y,top_z-wall])rb([width,-rear_y,wall],2);
  translate([x0,-wall,bottom_z])rb([width,wall,top_z-bottom_z],2,"y");
 }
 for(x=[65,85])translate([x,-55,top_z-wall-.02])roof(5.5,wall+.04,-90);
 for(x=[td_x-pitch/2,td_x+pitch/2])translate([x,-wall-.02,td_z])rotate([-90,0,0])hole(4.5,wall+.04);
 translate([32,0,top_z-wall-.02])linear_extrude(wall+.04)polygon([[0,-16],[20,-16],[20,-33],[10,-43],[0,-33]]);
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
