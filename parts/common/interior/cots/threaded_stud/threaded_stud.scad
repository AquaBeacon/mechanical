// Purchased M3 metal headless set screw / threaded stud, smooth envelope only.
// Origin = lower end; cylinder extends +Z. Placement supplies the protrusion.
length=8;
diameter=3;
assert(length>0 && diameter>0);
cylinder(d=diameter,h=length,$fn=32,center=false);
