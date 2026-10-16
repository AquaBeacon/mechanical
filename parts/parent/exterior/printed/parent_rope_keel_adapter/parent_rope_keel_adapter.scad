// Central HP40 deck to 32 mm printed keel. No connection to floats.
part="assembly"; // [assembly,print]
plate_w=60; plate_t=8; socket_w=48; arm_half=14;
socket_h=40; beam_w=32; fit=0.5; hp=40; pin_z=-20;
$fn=64;e=0.03;
assert(hp/2-5.5>arm_half,"Driver/washer access intersects socket arm");
assert(socket_w/2-(beam_w+fit)/2>=6);
module hole(d,h){cylinder(d=d/cos(180/32),h=h,$fn=32);}
module body(){difference(){
 union(){
  translate([-plate_w/2,-plate_w/2,0])cube([plate_w,plate_w,plate_t]);
  translate([-socket_w/2,-arm_half,-socket_h])cube([socket_w,2*arm_half,socket_h+e]);
  translate([-arm_half,-socket_w/2,-socket_h])cube([2*arm_half,socket_w,socket_h+e]);
 }
 translate([-(beam_w+fit)/2,-(beam_w+fit)/2,-socket_h-e])cube([beam_w+fit,beam_w+fit,socket_h+e]);
 for(x=[-hp/2,hp/2],y=[-hp/2,hp/2])translate([x,y,-e])hole(5.5,plate_t+2*e);
 translate([-socket_w/2-e,0,pin_z])rotate([0,90,0])hole(6.5,socket_w+2*e);
}}
if(part=="print")translate([0,0,plate_t])rotate([180,0,0])body();else body();
