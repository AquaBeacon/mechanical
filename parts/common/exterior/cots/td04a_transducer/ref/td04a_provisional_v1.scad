// HONDEX TD04A: photo-based, provisional COTS exterior, units mm.
// NOT a manufacturer CAD model. ALL dimensions require measurement.
// Origin: acoustic face centre; face at Z=0, cable exits toward +Z.
/* [Provisional body dimensions] */
face_d = 26; // Existing project assumption, NOT confirmed diameter
lip_h = 1.5;
body_d = 23;
rear_d = 21;
body_h = 18; // Photo-based proportion, replaces no assembly dimensions
/* [Provisional mounting ear] */
ear_w = 15;
ear_t = 3;
ear_extension = 10;
slot_w = 3;
slot_length = 5;
slot_pitch = 7;
/* [Provisional cable stub] */
show_cable = true;
cable_d = 5;
cable_stub = 25; // Display only; supplied cable is 3000 mm
boot_d = 7;
boot_h = 5;
cable_y = -6;
/* [Resolution] */
$fn = 96;

assert(face_d >= body_d && body_d >= rear_d && rear_d > 0);
assert(body_h > lip_h && lip_h > 0);
assert(ear_t > 0 && ear_t < rear_d/2 && ear_w < rear_d);
assert(slot_length >= slot_w && slot_w > 0);
assert(slot_pitch + slot_w < ear_w);
assert(ear_extension > slot_length + 2);
assert(cable_d > 0 && boot_d >= cable_d && boot_h > 0 && cable_stub > 0);
assert(abs(cable_y) + boot_d/2 < rear_d/2);

module slot_y(w, length, depth) {
    // Analytic primitives keep STEP faces editable (no hull).
    union() {
        cube([w, depth, length-w], center=true);
        for (z = [-(length-w)/2, (length-w)/2])
            translate([0,0,z]) rotate([90,0,0])
                cylinder(d=w,h=depth,center=true);
    }
}

module td04a_transducer() {
    union() {
        cylinder(d=face_d, h=lip_h);
        translate([0,0,lip_h])
            cylinder(d1=body_d,d2=rear_d,h=body_h-lip_h);
        difference() {
            translate([-ear_w/2,rear_d/2-ear_t,lip_h])
                cube([ear_w,ear_t,body_h+ear_extension-lip_h]);
            for (x=[-slot_pitch/2,slot_pitch/2])
                translate([x,rear_d/2-ear_t/2,body_h+ear_extension/2])
                    slot_y(slot_w,slot_length,ear_t+2);
        }
        translate([0,cable_y,body_h-0.5])
            cylinder(d1=boot_d,d2=cable_d+1,h=boot_h+0.5);
        if (show_cable)
            translate([0,cable_y,body_h+boot_h-0.5])
                cylinder(d=cable_d,h=cable_stub+0.5);
    }
}

td04a_transducer();
