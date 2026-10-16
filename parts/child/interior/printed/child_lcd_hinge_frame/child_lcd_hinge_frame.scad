// =====================================================================
// child_lcd_hinge_frame.scad — fixed C-frame behind the hinged LCD door
//
// Print flat as modelled. In the assembly rotate([-90,0,0]); the base remains
// behind the LCD, while vertical lugs reach the existing support arches and
// hinge axis. The open C-frame leaves C-MAIN accessible when the door swings.
// =====================================================================

include <../../../../../scad/lib/util.scad>;

/* [Existing support interface] */
mount_pitch = 95.0;
mount_y = mount_pitch/2;
support_world_y = 39.6;
assembly_origin_y = 27.0;
mount_axis_z = support_world_y-assembly_origin_y; // 12.6 in print coordinates
mount_clear_d = 3.4;
mount_lug_w = 9.0;
mount_lug_len = 5.0;
mount_lug_h = 15.5;
arch_t = 5.0;                  // child_lcd_support rib_t: the arches occupy |y| = mount_y ± arch_t/2
// 2026-08-28: lugs used to sit IN the arch band (penetration 2.6 mm). They now
// sit on the arch inner faces and the M3x10 screw runs axially into the arch pilot.
lug_y1 = mount_y - arch_t/2;    // outer face of each lug = arch inner face (|y| = 45)
lug_yc = lug_y1 - mount_lug_len/2;
assert(lug_y1 <= mount_y - arch_t/2 + 0.01, "mount lug overlaps the support arch");

/* [Frame] */
base_t = 3.0;
beam_w = 6.0;
hinge_x = -18.5;
hinge_axis_z = 9.5;
hinge_pin_d = 3.4;
hinge_y0 = -7.5;
hinge_y1 = 7.5;
hinge_block_w = 6.4;
hinge_block_h = 13.0;

/* [Latch — M2.5 heat-set insert] */
latch_x = 16.5;
latch_boss_d = 6.2;
latch_top_z = 7.7;             // reaches door rear face at assembly Y=34.7
insert_d = 4.0;
insert_depth = 4.0;

$fa = 4;
$fs = 0.3;

assert(abs((assembly_origin_y+hinge_axis_z)-36.5)<0.01,
       "Frame hinge axis must match LCD door world Y=36.5");
assert(latch_x-latch_boss_d/2 > 13.1,
       "Latch boss overlaps the LCD module envelope");

module pad(p,d,h=base_t) {
    translate([p[0],p[1],0]) cylinder(d=d,h=h,$fn=32);
}

module beam(a,b,d=beam_w,h=base_t) {
    hull() { pad(a,d,h); pad(b,d,h); }
}

module mount_lug(sy) {
    difference() {
        translate([-mount_lug_w/2,
                   sy>0 ? lug_y1-mount_lug_len : -lug_y1,
                   0])
            cube([mount_lug_w,mount_lug_len,mount_lug_h]);
        // bore starts at the lug inner face and runs outward through the whole lug
        translate([0,sy*(lug_y1-mount_lug_len-0.1),mount_axis_z])
            rotate([0,0,sy>0 ? 90 : -90])
                teardrop_bore(mount_clear_d,mount_lug_len+0.2);
    }
}

difference() {
    union() {
        // Left spine and three arms form an open C/E frame behind the display.
        beam([hinge_x,-34],[hinge_x,34]);
        beam([hinge_x,-32],[0,-lug_yc]);
        beam([hinge_x, 32],[0, lug_yc]);
        beam([hinge_x,0],[latch_x,0]);

        for (sy=[-1,1]) mount_lug(sy);

        // Central stationary hinge knuckle interleaves with the two door leaves.
        translate([hinge_x-hinge_block_w/2,hinge_y0,0])
            cube([hinge_block_w,hinge_y1-hinge_y0,hinge_block_h]);

        // Latch boss accepts a reusable M2.5 heat-set insert from the top.
        translate([latch_x,0,0]) cylinder(d=latch_boss_d,h=latch_top_z,$fn=32);
    }

    translate([hinge_x,hinge_y0-0.1,hinge_axis_z])
        rotate([0,0,90]) teardrop_bore(hinge_pin_d,hinge_y1-hinge_y0+0.2);

    translate([latch_x,0,latch_top_z-insert_depth])
        hole(insert_d,insert_depth+0.2,fn=8);
}

echo(str("child_lcd_hinge_frame: mount pitch=",mount_pitch,
         " hinge=",hinge_x," latch=",latch_x));
