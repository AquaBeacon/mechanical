// Purchased hardware envelope; no modeled threads, not print.
$fn=32;
difference(){cylinder(d=8/cos(30),h=4,$fn=6);translate([0,0,-1])cylinder(d=5,h=6);}