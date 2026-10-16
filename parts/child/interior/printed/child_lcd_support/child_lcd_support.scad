// =====================================================================
// child_lcd_support.scad — one of two LCD support arches
//
// Two copies are used at the C-MAIN axial mounting-hole planes. M3 metal
// spacers connect the arch to C-MAIN:
//   X=-22.0 : 30 mm spacer, X=+39.5 : 17 mm spacer (M3 male-female, standing on
//   the C-MAIN top face; the arch boss sits on the spacer's female end face).
// The asymmetric arch follows the circular tube instead of wasting radial room
// on a flat panel. Horizontal screw holes are teardrops for clean PLA printing.
//
// Variants (variants.txt):
//   lower  have_ear=true   — z 22..27 in the assembly. Carries the 90° anchor ear:
//                            a foot at (0, 47) that stands on the bottom flange's
//                            inner face (world z=19) and takes an M3x12 into the
//                            flange's 4x M3 BCD94 tapped hole (90° position).
//                            Together with the deck lugs at 0°/180° this gives a
//                            3-point clamp of the whole interior to the flange.
//   upper  have_ear=false  — z 117..122, plain arch.
//
// Print orientation:
//   upper : flat, as modelled (z=0 on the bed).
//   lower : FLIPPED — the arch top face (z=5) on the bed, so the ear foot
//           (which reaches 2.7 mm below the arch) grows upward. The teardrop
//           apexes are mirrored automatically when have_ear=true.
//
// Primitives only (cube / cylinder / polygon extrusions) so csg_to_step keeps
// true faces — 2026-09-03: replaced the hull() capsules and hull() teardrops
// that made FreeCAD drop 94 % of the volume and fall back to a faceted STEP.
// =====================================================================

include <../../../../../scad/lib/util.scad>;

/* [C-MAIN transformed hole positions] */
left_x = -22.0;                 // H3/H4 row (KiCad y=66)
right_x = 39.5;                 // H1/H2 row (KiCad y=4.5)
board_y = 2.6;                  // board top face in assembly
left_spacer = 30.0;             // was 35: boss centre = board_y + spacer + boss_d/2. 30 (not 32) so the
                                // hinge-rod boss (bottom y 33.0) clears the spacer's hex top (y 32.6)
right_spacer = 17.0;            // was 20

/* [LCD interface] */
lcd_anchor_x = 0;
lcd_anchor_y = 39.6;
lcd_pilot_d = 2.8;              // M3 self-tap from cradle end

/* [Hinge rod] */
// 2026-08-28: the door hinge is an M3 threaded rod (~105 mm) captured by BOTH arches
// (nut under the lower arch, nut above the upper arch). No pin head next to the door
// plate any more. Axis = child_lcd_cradle hinge_x / world Y 36.5.
hinge_x = -18.5;
hinge_y = 36.5;
hinge_boss_d = 7.0;
hinge_clear_d = 3.4;

/* [Part] */
rib_t = 5.0;                    // axial thickness / print height
beam_w = 4.8;
mount_boss_d = 5.5;             // common M3 hex-spacer envelope
mount_clear_d = 3.4;
tube_id = 101.6;
wall_clear = 2.5;

/* [Bottom-flange anchor ear (lower variant only)] */
// 2026-09-03: 3-point fixing of the interior to the bottom flange. The 4x M3 BCD94
// tapped holes are on the FLANGE inner face (BR-101040, verified from the STEP and
// the WTE datasheet Rev C.5 — see parts/child/exterior/cots/wte4_flange/). 0°/180°
// are taken by child_vtray_deck lugs on MF10 spacers; 90° (0, +47) is the only hole
// the deck cannot reach (C-MAIN sits between), so this arch carries it. 270° is
// blocked by the battery box floor.
have_ear      = false;          // variants.txt sets this
flange_bcd    = 94;             // BR-101040 inner-face M3 hole circle (STEP: 94.000)
flange_face_z = 19;             // world z of the bottom flange inner face (piston length 19.1)
arch_z0       = 22;             // world z of this arch's bottom face (lower arch placement)
ear_gap       = 0.3;            // nominal gap foot→flange: the metal spacers at 0°/180° stay the datum,
                                // this screw only snugs the arch down (0.3 mm over a 40 mm beam)
ear_x         = 0;
ear_od        = 5.2;            // hole 3.4 → 0.9 mm wall; outer edge r 49.6 (tube ID/2 − 1.0 = 49.8 max)
ear_clear_d   = 3.4;            // M3 clearance
ear_web_w     = 5.2;            // web between the LCD anchor boss and the ear (X width)
screw_head_d_ear = 5.5;         // M3 pan / socket head on top of the arch (z 27..30 world)
hinge_lug_y_max  = 42.5;        // child_lcd_hinge_frame lower lug, max +Y at z 27..32 (assembly measurement)
frame_screw_head_y_max = 42.35; // its M3x10 head, z 32..35

$fa = 4;
$fs = 0.3;

// Spacer end face touches the boss cylinder, so the boss centre is boss_d/2 further out.
left_y = board_y + left_spacer + mount_boss_d/2;
right_y = board_y + right_spacer + mount_boss_d/2;
screw_head_d = 5.5;             // JIS M3 flat (countersunk) head, flush with the boss +Y face
screw_csk_h = (screw_head_d - mount_clear_d)/2;   // 90 deg countersink depth (1.05)
r_use = tube_id/2-wall_clear;
ear_y  = flange_bcd/2;                           // 47
ear_z0 = -(arch_z0 - flange_face_z) + ear_gap;   // -2.7 (world 19.3)
ear_h  = rib_t - ear_z0;                         // 7.7
apex   = have_ear ? -1 : 1;                      // teardrop apex direction in print orientation

function rad(x,y)=sqrt(x*x+y*y);
assert(rad(abs(hinge_x)+hinge_boss_d/2, hinge_y+hinge_boss_d/2) < r_use, "hinge rod boss touches tube");
spacer_ac = 5.5/cos(30);        // M3 hex spacer across-corners
assert(hinge_y - hinge_boss_d/2 >= board_y + left_spacer + 0.3 || abs(hinge_x - left_x) > (hinge_boss_d + spacer_ac)/2,
       "hinge rod boss overlaps the left spacer top");
// The spacer screws are JIS M3 flat heads (d 5.5) countersunk flush into the +Y
// face of each boss, so nothing protrudes beyond the boss corner toward the tube.
assert(rad(abs(left_x) + mount_boss_d/2, left_y + mount_boss_d/2) < tube_id/2 - 1.5,
       "left spacer boss corner (flush screw head) too close to tube");
assert(rad(abs(right_x) + mount_boss_d/2, right_y + mount_boss_d/2) < tube_id/2 - 1.5,
       "right spacer boss corner (flush screw head) too close to tube");
assert(rad(left_x,left_y)+mount_boss_d/2 < r_use,
       "35 mm LCD spacer boss touches tube");
assert(rad(right_x,right_y)+mount_boss_d/2 < r_use,
       "20 mm LCD spacer boss touches tube");

// Anchor ear (checked even when have_ear=false so the numbers stay honest)
assert(ear_y + ear_od/2 <= tube_id/2 - 1.0,
       str("anchor ear touches tube r=", ear_y + ear_od/2, " > ", tube_id/2 - 1.0));
assert(rad(ear_web_w/2, ear_y + ear_od/2) <= tube_id/2 - 1.0, "anchor ear corner touches tube");
assert(ear_y - ear_clear_d/2 - (lcd_anchor_y + lcd_pilot_d/2) >= 1.5,
       "anchor ear hole too close to the LCD anchor pilot");
assert(ear_y - screw_head_d_ear/2 >= hinge_lug_y_max + 1.0,
       str("anchor screw head hits the hinge-frame lug: ", ear_y - screw_head_d_ear/2, " vs ", hinge_lug_y_max));
assert(ear_y - screw_head_d_ear/2 >= frame_screw_head_y_max + 1.0, "anchor screw head hits the frame screw head");
assert(ear_z0 <= 0 && ear_gap >= 0 && ear_gap <= 0.5, "ear foot must reach the flange face (gap 0..0.5)");
flange_bore_r = 88.5/2;         // the foot only bears where r >= bore radius (44.25)
assert(ear_y + ear_od/2 - flange_bore_r >= 4.0,
       str("anchor foot bears on only ", ear_y + ear_od/2 - flange_bore_r, " mm of flange face"));

// ---- primitives-only helpers ---------------------------------------
// Straight bar of width w between two points, with round ends (= old capsule).
module bar(a, b, w, h) {
    L = rad(b[0]-a[0], b[1]-a[1]);
    ang = atan2(b[1]-a[1], b[0]-a[0]);
    translate([a[0],a[1],0]) rotate([0,0,ang]) translate([0,-w/2,0]) cube([L, w, h]);
    for (p=[a,b]) translate([p[0],p[1],0]) cylinder(d=w,h=h,$fn=32);
}
// Teardrop prism (circle + 50° self-supporting roof), axis along Z, apex to +Y.
// ONE polygon: FreeCAD's CSG importer returns a null shape for any boolean of a
// cylinder with an overlapping extruded polygon (tested 2026-09-03), so the arc
// is discretised into the same polygon as the roof.
module teardrop_prism(d, len, fn=24) {
    r = d/2; D = 1.55*r; th = acos(r/D);
    pts = concat([[0, D]],
                 [for (i=[0:fn]) let(a = 90 + th + i*(360 - 2*th)/fn) [r*cos(a), r*sin(a)]]);
    linear_extrude(len) polygon(pts);
}
// Horizontal bore along +Y through a +Y/-Y wall; apex faces +Z (dir=1) or -Z (dir=-1).
module teardrop_bore_y(d, len, dir=1) {
    rotate([-90,0,0]) rotate([0,0,dir > 0 ? 180 : 0]) teardrop_prism(d, len);
}

difference() {
    union() {
        bar([left_x,left_y],[lcd_anchor_x,lcd_anchor_y],beam_w,rib_t);
        bar([lcd_anchor_x,lcd_anchor_y],[right_x,right_y],beam_w,rib_t);
        for (p=[[left_x,left_y],[right_x,right_y]])
            translate([p[0],p[1],0]) cylinder(d=mount_boss_d,h=rib_t,$fn=32);
        translate([lcd_anchor_x,lcd_anchor_y,0]) cylinder(d=9,h=rib_t,$fn=32);
        translate([hinge_x,hinge_y,0]) cylinder(d=hinge_boss_d,h=rib_t,$fn=32);
        if (have_ear) {
            // foot + web: from the LCD anchor boss out to the flange hole circle,
            // full height from the flange face (z -2.7) to the arch top (z 5)
            translate([ear_x,ear_y,ear_z0]) cylinder(d=ear_od,h=ear_h,$fn=32);
            translate([ear_x-ear_web_w/2,lcd_anchor_y,ear_z0]) cube([ear_web_w, ear_y-lcd_anchor_y, ear_h]);
        }
    }
    // Hinge rod bore (axial, prints clean)
    translate([hinge_x,hinge_y,-0.1]) hole(hinge_clear_d,rib_t+0.2,fn=24);

    // Spacer screws run horizontally in assembly and in this print orientation.
    for (p=[[left_x,left_y],[right_x,right_y]])
        translate([p[0],p[1]-mount_boss_d/2-0.2,rib_t/2]) {
            teardrop_bore_y(mount_clear_d,mount_boss_d+0.4,apex);
            // 90 deg countersink on the +Y face for the flush flat-head screw
            translate([0,mount_boss_d+0.4-screw_csk_h,0]) rotate([-90,0,0])
                cylinder(d1=mount_clear_d,d2=screw_head_d+0.2,h=screw_csk_h+0.01,$fn=24);
        }

    // Cradle attaches axially; this pilot is vertical and prints accurately.
    // Runs through the ear web too, so the hinge-frame screw tip never bottoms out.
    translate([lcd_anchor_x,lcd_anchor_y,min(0,ear_z0)-0.1])
        hole(lcd_pilot_d,rib_t-min(0,ear_z0)+0.2,fn=8);

    // Anchor ear: M3 clearance, axial (screw from the top into the flange)
    if (have_ear)
        translate([ear_x,ear_y,ear_z0-0.1]) cylinder(d=ear_clear_d,h=ear_h+0.2,$fn=24);
}

if (have_ear)
    echo(str("child_lcd_support lower: anchor ear at (", ear_x, ", ", ear_y, ") foot z ",
             arch_z0 + ear_z0, " (flange face ", flange_face_z, " + gap ", ear_gap, "), screw head top z ",
             arch_z0 + rib_t + 2.0, ", M3x12 engages flange ", 12 - (rib_t - ear_z0) - ear_gap, " mm"));
