// Purchased hardware envelope; no modeled threads, not print.
$fn=32;
difference(){cylinder(d=13/cos(30),h=6.5,$fn=6);translate([0,0,-1])cylinder(d=8,h=8.5);}