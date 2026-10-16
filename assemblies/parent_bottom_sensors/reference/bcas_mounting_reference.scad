// Purchased box display correction, not a printable or machining part.
// Drawing E-E: external bore D4.2, seat height6. Access well D9.4 is provisional.
$fn=64;
difference(){
 union(){include <../../../parts/parent/exterior/cots/bcas212310g/bcas212310g.scad>}
 for(x=[9,201])for(y=[9,221]){
  translate([x,y,-1])cylinder(d=4.2,h=8);
  translate([x,y,6])cylinder(d=9.4,h=76);
 }
}
