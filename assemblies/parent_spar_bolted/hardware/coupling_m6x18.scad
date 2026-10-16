// Purchased hardware envelope; no modeled threads, not print.
$fn=32;
difference(){cylinder(d=10/cos(30),h=18,$fn=6);translate([0,0,-1])cylinder(d=6,h=20);}