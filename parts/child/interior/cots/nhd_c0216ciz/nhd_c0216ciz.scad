// Mechanical keep-out for NHD-C0216CiZ-FSW-FBW-3V3 (2x16 COG, I2C).
// Reference model only; do not print. X=short side, Y=long side, Z=rear depth.
//
// 2026-08-28: rebuilt from the datasheet mechanical drawing (rev 1B):
//   body 56.8 x 26.2 x 5.5 (backlight included)
//   8 signal pins on ONE LONG EDGE (bottom edge of the drawing), pitch 1.5,
//   centred, protruding 8.0 IN THE MODULE PLANE (not rearward).
//   backlight K/A: 2 pins, 2.5 apart, at one short end (right edge of the drawing).
// In the AquaBeacon door the pins are bent 90 deg rearward at the edge and
// trimmed to pin_bent so they clear the fixed C-frame (child_lcd_hinge_frame)
// and the rear clamp bars. The old 20x50 "carrier PCB" envelope is gone:
// the charge-pump caps (VOUT/C1+/C1-) go on a small cap board on the harness.

lcd_w = 26.2;      // X, short side. Signal pins are on the -X edge.
lcd_l = 56.8;      // Y, long side
lcd_h = 5.5;       // Z, rear depth (front face z=0)
pin_n = 8;
pin_pitch = 1.5;
pin_w = 0.5;
pin_bent = 4.0;    // length after bending rearward and trimming (datasheet 8.0 straight)
bl_pin_gap = 2.5;  // K/A spacing
bl_x = -lcd_w/2 + 7.0;   // K/A position along the short side (drawing: 7.00 from the pin edge)
$fn = 24;

union() {
    translate([-lcd_w/2, -lcd_l/2, 0]) cube([lcd_w, lcd_l, lcd_h]);
    // 8 signal pins, bent rearward along the -X edge
    for (i = [0:pin_n-1])
        translate([-lcd_w/2, (i - (pin_n-1)/2) * pin_pitch - pin_w/2, lcd_h])
            cube([pin_w + 0.1, pin_w, pin_bent]);
    // backlight K/A, bent rearward along the +Y short end
    for (k = [0, 1])
        translate([bl_x + k*bl_pin_gap - pin_w/2, lcd_l/2 - pin_w - 0.1, lcd_h])
            cube([pin_w, pin_w + 0.1, pin_bent]);
}

echo(str("nhd_c0216ciz: ", lcd_w, " x ", lcd_l, " x ", lcd_h, " pins on -X long edge, bent rearward ", pin_bent));
