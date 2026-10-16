// Two identical upper clamp bars. Flat underside Z=0. mm.
/* [Dimensions] */
width=236;
depth=24;
thickness=12;
rod_pitch=224;
rod_hole=5.5;
$fn=48;
assert((width-rod_pitch-rod_hole)/2>=3);
assert(depth>=20 && thickness>=10);
module hole(d,h){cylinder(d=d/cos(180/32),h=h,$fn=32);}
difference(){
 translate([-width/2,-depth/2,0])cube([width,depth,thickness]);
 for(x=[-rod_pitch/2,rod_pitch/2])translate([x,0,-0.02])hole(rod_hole,thickness+0.04);
}
