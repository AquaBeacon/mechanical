// P1 integration prototype. Flat +Z printing, same footprint as parent_plate.
// Measured hardware dimensions remain pending; see assembly measurement list.
include <../parent_plate/parent_plate.scad>
pattern = 1;
pwr_boss_h = 9.5;
assert(pwr_boss_h >= 8.15 + 1.0, "PWR underside lead clearance below 1 mm");
