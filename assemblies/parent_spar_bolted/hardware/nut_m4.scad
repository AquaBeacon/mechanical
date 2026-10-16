// Purchased hardware envelope; no modeled threads, not print.
$fn=32;
difference(){cylinder(d=7/cos(30),h=3.2,$fn=6);translate([0,0,-1])cylinder(d=4,h=5.2);}