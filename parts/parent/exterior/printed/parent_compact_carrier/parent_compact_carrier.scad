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
  translate([-width/2,rear_y,top_z-wall])cube([width,-rear_y,wall]);
  translate([-width/2,-wall,bottom_z])cube([width,wall,top_z-bottom_z]);
 }
 for(x=frame_x)translate([x,-55,top_z-wall-.02])hole(5.5,wall+.04);
 for(x=[-camera_pitch[0]/2,camera_pitch[0]/2],z=[-camera_pitch[1]/2,camera_pitch[1]/2])
  translate([camera_x+x,-wall-.02,camera_z+z])yh(5.5,wall+.04);
 for(x=[-td_bolt_pitch/2,td_bolt_pitch/2])translate([td_x+x,-wall-.02,td_z])yh(4.5,wall+.04);
 // Open routing around side; these are lacing eyes, not connector pass-throughs.
 for(z=[-35,-60])translate([15,-wall-.02,z])yh(5,wall+.04);
}
