// Open lower clamp frame; box bottom Z=0. mm.
width=236; depth=236; rail=24; thick=12;
clamp_x=112; clamp_y=55;
lug_y=85; lug_pitch=16;
carrier_x=[-85,-65,65,85];
$fn=48;
module hole(d,h){cylinder(d=d/cos(180/32),h=h,$fn=32);}
assert(rail>=24 && thick>=12);
assert(clamp_x+5<width/2);
difference(){
 union(){
  for(x=[-width/2,width/2-rail])translate([x,-depth/2,-thick])cube([rail,depth,thick]);
  for(y=[-clamp_y,clamp_y])translate([-width/2,y-rail/2,-thick])cube([width,rail,thick]);
 }
 for(x=[-clamp_x,clamp_x]){
  for(y=[-clamp_y,clamp_y])translate([x,y,-thick-.02])hole(5.5,thick+.04);
  for(c=[-lug_y,lug_y],dy=[-lug_pitch/2,lug_pitch/2])translate([x,c+dy,-thick-.02])hole(5.5,thick+.04);
 }
 for(x=carrier_x){
  translate([x,-clamp_y,-thick-.02])hole(5.5,thick+.04);
  translate([x,-clamp_y,-6])hole(10,6.02); // recessed M5 head; box stays flat
 }
}
