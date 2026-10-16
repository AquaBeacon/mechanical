// LCD service-motion check. This is a diagnostic view, not a printable part.
// Pull the interior at least 70 mm out of the acrylic tube before opening.

door_angle = 100;              // [0:closed,100:service-open]
hinge_axis = [-18.5,36.5,72];

module around_hinge(a) {
    translate(hinge_axis) rotate([0,0,a]) translate(-hinge_axis) children();
}

module lcd_door() {
    color("White")
        translate([0,43.5,72]) rotate([90,0,0])
            import("../../parts/child/interior/printed/child_lcd_cradle/child_lcd_cradle_bezel.stl");
    color("LightSkyBlue",0.75)
        translate([0,43.5,72]) rotate([90,0,0])
            import("../../parts/child/interior/cots/nhd_c0216ciz/nhd_c0216ciz.stl");
}

// Fixed C-MAIN, support arches and hinge frame.
color("DarkGreen",0.25)
    translate([44,1,20]) rotate([0,-90,-90])
        import("../../parts/child/interior/pcb/child_main/child_main.stl");
for (z=[22,117])
    color("DarkOrange") translate([0,0,z])
        import("../../parts/child/interior/printed/child_lcd_support/child_lcd_support.stl");
color("Gainsboro")
    translate([0,27,72]) rotate([-90,0,0])
        import("../../parts/child/interior/printed/child_lcd_hinge_frame/child_lcd_hinge_frame.stl");

around_hinge(door_angle) lcd_door();

// M3 hinge pin reference (not printed).
color("Silver") translate([-18.5,36.5,43.5]) cylinder(d=3,h=57,$fn=24);
