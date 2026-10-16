// r2 inspection view: crop of +X/+Y joint with exposed fasteners.
// Hardware is illustrative nominal geometry, not a manufacturing specification.
$fn=48;
module crop() { translate([88,-2,-40]) cube([27,60,56]); }
color("SteelBlue") render() intersection() {
    crop();
    import("../../parts/child/exterior/printed/child_simple_front/child_simple_front.stl");
}
color("Gray") render() intersection() {
    crop();
    import("../../parts/child/exterior/printed/child_simple_guard/child_simple_guard.stl");
}
module along_y(x,y,z) { translate([x,y,z]) rotate([-90,0,0]) children(); }
for(z=[-7,5]) {
    color("Silver") along_y(100,10.5,z) cylinder(d=3,h=35);
    color("DimGray") along_y(100,45.5,z) difference() {
        cylinder(d=5.5,h=3);
        translate([0,0,1]) cylinder(r=1.25/cos(30),h=3,$fn=6);
    }
    color("Goldenrod") along_y(100,14.1,z) difference() {
        cylinder(r=2.75/cos(30),h=2.4,$fn=6);
        translate([0,0,-0.1]) cylinder(d=3,h=3);
    }
    for(y=[16.5,45]) color("Silver") along_y(100,y,z) difference() {
        cylinder(d=7,h=0.5);
        translate([0,0,-0.1]) cylinder(d=3.2,h=1);
    }
}
