// =====================================================================
// child_vtray_cable_rail.scad - removable longitudinal cable restraint
//
// Two identical rails are bolted below the vertical tray through the existing
// 16 x 30 mm cable slots.  One rail is power, the other signal/sensor.  Zip
// ties pass through paired slots every <=30 mm and positively retain the cable.
// Print flat as modelled, channel facing up.  No supports are required.
// =====================================================================

include <../../../../../scad/lib/util.scad>;

/* [Rail] */
rail_w = 16.0;
rail_l = 110.0;
base_t = 2.4;                 // 6 layers at 0.2 mm plus margin
channel_w = 8.0;              // bundle OD up to about 8 mm with foam liner
wall_h = 6.5;

/* [Fasteners] */
// 2026-08-03: the old mount_y = [40, 80] put every bolt in mid-air — it landed
// inside the deck's own 16 x 30 mm cable slot, so there was nothing to clamp and
// no washer can bridge the opening. The bolts now sit on the deck's solid webs
// and self-tap into these side walls (base_t + wall_h = 8.9 mm of material).
// Keep in step with child_vtray_deck: rail_hz = mount_y + rail_z0(20), rail_hx = mount_x.
rail_z0 = 20;                 // assembly Z of this rail's local y = 0
mount_y = [17, 57];           // assembly Z = 37 / 77, both clear of every deck slot
mount_x = 5.7;                // through the side walls, not the channel floor
mount_d = 2.8;                // M3 self-tap pilot (the deck carries the Ø3.4 clearance)

/* [Drop window] */
// 2026-09-03: the deck's middle cable slit (world z 83..109, rail-local y 63..89) was
// covered by this solid base, so nothing could actually drop from the deck top into the
// trough there. A window through the channel floor (rail-local y 70..84 = world z 90..104)
// lets the MAIN-side harnesses (RX / tether / temp / leak / pressure) enter the trough.
// It sits inside the deck slit and between the tie stations.
drop_y = 77;                  // window centre (rail-local y) = world z 97
drop_l = 14;                  // window length (Y); the deck slit is 26 long

/* [Cable ties] */
// 2026-09-03: 70 -> 62 / 92, 100 -> 105 to clear the drop window (spacing still <= 30 mm)
tie_y = [10, 35, 62, 92, 105];
tie_slot_x = 2.2;             // passage for tie thickness
tie_slot_y = 4.2;             // up to 4 mm reusable/nylon tie width
tie_x = (channel_w/2 + rail_w/2)/2;

/* [Print] */
bottom_chamfer = 0.5;
$fa = 4;
$fs = 0.3;

assert(rail_w-channel_w >= 2*3.5, "Cable rail side walls are too thin");
assert(max(tie_y[1]-tie_y[0], tie_y[2]-tie_y[1], tie_y[3]-tie_y[2], tie_y[4]-tie_y[3]) <= 30,
       "Cable restraint spacing exceeds 30 mm");
// drop window must stay inside the deck slit (rail-local y 63..89) and clear ties / bolts
assert(drop_y - drop_l/2 >= 63 && drop_y + drop_l/2 <= 89, "drop window is outside the deck slit");
for (y = tie_y) assert(abs(y - drop_y) >= drop_l/2 + tie_slot_y/2 + 1, str("tie slot y=", y, " runs into the drop window"));
for (y = mount_y) assert(abs(y - drop_y) >= drop_l/2 + mount_d/2 + 1, str("mount hole y=", y, " runs into the drop window"));
assert(mount_x + mount_d/2 < rail_w/2-0.3, "M3 hole breaks the outer wall");
// The bolt must go through a side wall, never through the open channel floor,
// or there is only base_t (2.4 mm) of thread engagement.
assert(mount_x - mount_d/2 > channel_w/2,
       "M3 pilot falls into the cable channel - no thread engagement");
for (y = mount_y) assert(y > mount_d && y < rail_l - mount_d,
                         "mount hole runs off the end of the rail");

module chamfered_base() {
    hull() {
        translate([-rail_w/2+bottom_chamfer, bottom_chamfer, 0])
            cube([rail_w-2*bottom_chamfer, rail_l-2*bottom_chamfer, 0.01]);
        translate([-rail_w/2, 0, bottom_chamfer])
            cube([rail_w, rail_l, base_t-bottom_chamfer]);
    }
}

difference() {
    union() {
        chamfered_base();
        for (sx=[-1,1])
            translate([sx>0 ? channel_w/2 : -rail_w/2, 0, base_t])
                cube([(rail_w-channel_w)/2, rail_l, wall_h]);
    }

    // Two M3 bolts per station, driven from the deck's top face into these walls.
    for (y=mount_y, sx=[-1,1])
        translate([sx*mount_x, y, -0.1]) hole(mount_d, base_t+wall_h+0.2, fn=8);

    // Drop window through the channel floor (cables come down from the deck slit here)
    translate([-channel_w/2, drop_y - drop_l/2, -0.1]) cube([channel_w, drop_l, base_t + 0.2]);

    // Paired passages let a tie wrap completely around the bundle and rail.
    for (y=tie_y, sx=[-1,1])
        translate([sx*tie_x-tie_slot_x/2, y-tie_slot_y/2, -0.1])
            cube([tie_slot_x, tie_slot_y, base_t+wall_h+0.2]);
}

echo(str("child_vtray_cable_rail: ",rail_w," x ",rail_l,
         " / channel ",channel_w," / tie spacing <=30 mm"));
