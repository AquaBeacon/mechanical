// Compact L carrier: horizontal flange meets frame Z=-12; mounting face Y=0.
width=210; wall=8; rear_y=-67; top_z=-12; bottom_z=-100;
camera_x=-48; camera_z=-66; camera_pitch=[22,32];
td_x=55; td_z=-35; td_bolt_pitch=36;
frame_x=[-85,-65,65,85];
$fn=48;
module hole(d,h){cylinder(d=d/cos(180/32),h=h,$fn=32);}
module yh(d,h){rotate([-90,0,0])hole(d,h);}
assert(camera_z+camera_pitch[1]/2+5<top_z);
assert(camera_z-camera_pitch[1]/2-5>bottom_z);
assert(td_x+td_bolt_pitch/2+5<width/2);
difference(){
 union(){
  translate([-width/2,rear_y,top_z-wall])rb([width,-rear_y,wall],2);
  translate([-width/2,-wall,bottom_z])rb([width,wall,top_z-bottom_z],2,"y");
 }
 // Flange windows retain ribs between wall and the mounting row.
 for(x=[-50,-8,34])translate([x,0,top_z-wall-.02])linear_extrude(height=wall+.04)
 polygon([[0,-16],[20,-16],[20,-33],[10,-43],[0,-33]]); // 45-degree roof, print up=-Y
 // Preserve camera bolt pads and TD bracket landing; remove unloaded sheet.
 for(c=[[-97,-92,24,62],[-20,-92,42,50],[26,-92,69,39]])
  translate([c[0],-wall-.02,c[1]])rb([c[2],wall+.04,c[3]],2,"y");
 translate([-51,-wall-.02,-73])rb([6,wall+.04,14],2,"y");
 for(x=frame_x)translate([x,-55,top_z-wall-.02])roof(5.5,wall+.04,-90);
 for(x=[-camera_pitch[0]/2,camera_pitch[0]/2],z=[-camera_pitch[1]/2,camera_pitch[1]/2])
  translate([camera_x+x,-wall-.02,camera_z+z])yh(5.5,wall+.04);
 for(x=[-td_bolt_pitch/2,td_bolt_pitch/2])translate([td_x+x,-wall-.02,td_z])yh(4.5,wall+.04);
 // Open routing around side; these are lacing eyes, not connector pass-throughs.
 for(z=[-35])translate([15,-wall-.02,z])yh(5,wall+.04);
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
