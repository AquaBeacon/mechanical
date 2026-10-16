// =====================================================================
// child_vtray_batt_gate.scad — LiPo bay axial quick-release gate
// Print flat. Two accessible M3 screws release the battery along +Z while
// C-MAIN and the battery box remain installed.
// =====================================================================

include <../../../../../scad/lib/util.scad>;

gate_w = 54;
gate_h = 31;
gate_t = 3;
boss_x = 24;
boss_y = 6.5;
screw_d = 3.4;
wire_notch_w = 16;
wire_notch_h = 11;
finger_r = 5;

$fa=4;
$fs=0.3;

assert(boss_x+screw_d/2 < gate_w/2-0.5,"gate screw too close to edge");

difference() {
    box_rounded(gate_w,gate_h,gate_t,r=2,chamfer=0.5);
    for (sx=[-1,1])
        translate([gate_w/2+sx*boss_x,boss_y,-0.1])
            hole(screw_d,gate_t+0.2,fn=8);
    translate([(gate_w-wire_notch_w)/2,gate_h-wire_notch_h,-0.1])
        cube([wire_notch_w,wire_notch_h+0.2,gate_t+0.2]);
    translate([gate_w/2,gate_h-wire_notch_h,-0.1])
        cylinder(r=finger_r,h=gate_t+0.2,$fn=32);
}
