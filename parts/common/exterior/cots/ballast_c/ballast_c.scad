// Owned ballast C, 1000 g per item (user statement).
// Reference CAD only. Axis Z; origin at centre of bottom face.
/* [Dimensions read from IMG_4269 (mm)] */
body_d = 48.5;
body_height = 53;
total_height = 76;
neck_d = 36;
// Head diameter equals body diameter (confirmed by user).
/* [Provisional head height - not given in photo] */
head_height_provisional = 8;
/* [Hidden] */
$fn = 128;
epsilon = 0.01;

// Sharp shoulders approximate the undimensioned rounded transitions.
module ballast_c(body_d, body_height, total_height, neck_d, head_d, head_height) {
    neck_height = total_height-body_height-head_height;
    assert(body_d > 0 && body_height > 0 && neck_d > 0);
    assert(head_height > 0 && neck_height > 0 && neck_d < body_d && head_d > neck_d);
    union() {
        cylinder(d=body_d, h=body_height);
        translate([0,0,body_height-epsilon])
            cylinder(d=neck_d, h=neck_height+2*epsilon);
        translate([0,0,total_height-head_height])
            cylinder(d=head_d, h=head_height);
    }
}
ballast_c(body_d, body_height, total_height, neck_d,
          body_d, head_height_provisional);
