// Sandwich the existing metal TD04A bracket, not the sensor body.
width=50; height=14; thick=8; bolt_pitch=36; bolt_d=4.5;
$fn=48;
assert(bolt_pitch/2-bolt_d/2>12+2);
difference(){
 translate([-width/2,0,-height/2])cube([width,thick,height]);
 for(x=[-bolt_pitch/2,bolt_pitch/2])translate([x,-.02,0])rotate([-90,0,0])cylinder(d=bolt_d/cos(180/32),h=thick+.04,$fn=32);
}
