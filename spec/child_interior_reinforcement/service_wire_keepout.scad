// Unprinted service clearance: 5.7 mm bundle + 1.65 mm radial allowance.
$fn=48;
for(a=[90,18,-54,-126,162]) {
 x=28*cos(a);y=28*sin(a);
 hull() for(z=[6.2,14]) translate([x,y,z]) sphere(r=4.5);
}
