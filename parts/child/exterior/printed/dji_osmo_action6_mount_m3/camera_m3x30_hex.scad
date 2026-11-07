// Purchased hex-head fastener proxy, M3x30; not a printed part.
$fn=48;
union(){ translate([0,0,-30]) cylinder(d=3,h=30.01); rotate([0,0,30]) cylinder(d=5.5/cos(30),h=2,$fn=6); }
