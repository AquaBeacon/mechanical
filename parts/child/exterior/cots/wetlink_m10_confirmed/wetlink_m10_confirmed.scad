// Child endcap envelope: local Z0 = outside face; +Z = dry side.
// M10 thread20, nutAF16/h8 per official WLP datasheet v1.5.
// Outside head/plug split is illustrative; total envelope uses upper limit26.
$fn=64;
module hex(af,h){cylinder(d=af/cos(30),h=h,$fn=6);}
difference(){
 union(){
  cylinder(d=10,h=20);
  translate([0,0,-8]) hex(16,8);
  translate([0,0,-26]) hex(14,18);
  translate([0,0,10]) hex(16,8);
 }
 translate([0,0,-27]) cylinder(d=5.7,h=48);
}
