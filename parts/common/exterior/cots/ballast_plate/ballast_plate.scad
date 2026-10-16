// Owned ballast: reference CAD only, not a printed replacement.
// Origin: bottom face centre. X=length, Y=width, Z=thickness.
/* [Variant] */
variant = "A"; // [A,B]
/* [Confirmed dimensions (mm)] */
a_length = 142;
a_width = 19;
a_thickness = 4;
b_length = 163.5;
b_width = 16;
b_thickness = 3;
b_end_offset = 20;
b_hole_pitches = [37.5, 48.5, 37.5];
/* [Provisional dimension - measure actual ballast] */
b_hole_d_provisional = 5.5; // M5 clearance through hole; actual diameter not measured.
/* [Hidden] */
$fn = 128;
epsilon = 0.01;

// Generic plate module, usable with `use <ballast_plate.scad>`.
module ballast_plate(length, width, thickness, hole_x_from_left, hole_d) {
    assert(length > 0 && width > 0 && thickness > 0);
    assert(len(hole_x_from_left) == 0 || (hole_d > 0 && hole_d < width));
    difference() {
        translate([-length/2, -width/2, 0]) cube([length, width, thickness]);
        for (x = hole_x_from_left) {
            assert(x > hole_d/2 && x < length-hole_d/2);
            translate([x-length/2, 0, -epsilon])
                cylinder(d=hole_d, h=thickness+2*epsilon);
        }
    }
}

assert(variant == "A" || variant == "B", "variant must be A or B");
b_hole_x = [b_end_offset,
            b_end_offset+b_hole_pitches[0],
            b_end_offset+b_hole_pitches[0]+b_hole_pitches[1],
            b_end_offset+b_hole_pitches[0]+b_hole_pitches[1]+b_hole_pitches[2]];
assert(abs(b_hole_x[3]+b_end_offset-b_length) < 0.001, "B length/pitches inconsistent");
if (variant == "A")
    ballast_plate(a_length, a_width, a_thickness, [], 0);
else
    ballast_plate(b_length, b_width, b_thickness, b_hole_x, b_hole_d_provisional);
