// Bambu Studio: import together with deck as one object; change this mesh
// to Modifier. Coordinates match child_vtray_deck_t200.stl.
// This is a slicer volume, not an additional printed structural part.
for (sx=[-1,1])
    translate([sx>0 ? 27 : -51,-11,18]) cube([24,25,85]);
