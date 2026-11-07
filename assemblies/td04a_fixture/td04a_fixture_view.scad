// =====================================================================
// td04a_fixture_view.scad
// !! 自動生成ファイル - 編集しないこと。placement.json を直して
//    build.ps1 -Assemblies で再生成する。
// 12 mm approximate M4 through-hole pitch; 60 mm cable space from hole baseline; old sensor model excluded. Parent M5/20; child side M3/20.
// 座標系: Global +Z up. Parent exterior plane Z0; child exterior side plane X0. Display origins separate comparison examples.
// =====================================================================

show_parent = true;
show_child = true;

if (show_parent) color("DarkOrange") translate([-45, 0, 0])  import("../../parts/common/exterior/printed/td04a_bracket_mount/td04a_bracket_mount_parent_down.stl");
if (show_parent) color("Silver") translate([-51, 5.8, -65]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m4x14_socket.stl");
if (show_parent) color("Silver") translate([-51, -3, -65]) rotate([90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_washer_m4_08.stl");
if (show_parent) color("Silver") translate([-51, 5, -65]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_washer_m4_08.stl");
if (show_parent) color("Silver") translate([-51, -3.8, -65]) rotate([90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_parent) color("Silver") translate([-39, 5.8, -65]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m4x14_socket.stl");
if (show_parent) color("Silver") translate([-39, -3, -65]) rotate([90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_washer_m4_08.stl");
if (show_parent) color("Silver") translate([-39, 5, -65]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_washer_m4_08.stl");
if (show_parent) color("Silver") translate([-39, -3.8, -65]) rotate([90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_child) color("DarkOrange") translate([45, 0, 0])  import("../../parts/common/exterior/printed/td04a_bracket_mount/td04a_bracket_mount_child_side_up.stl");
if (show_child) color("Silver") translate([71, 5.8, 65]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m4x14_socket.stl");
if (show_child) color("Silver") translate([71, -3, 65]) rotate([90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_washer_m4_08.stl");
if (show_child) color("Silver") translate([71, 5, 65]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_washer_m4_08.stl");
if (show_child) color("Silver") translate([71, -3.8, 65]) rotate([90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_child) color("Silver") translate([83, 5.8, 65]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m4x14_socket.stl");
if (show_child) color("Silver") translate([83, -3, 65]) rotate([90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_washer_m4_08.stl");
if (show_child) color("Silver") translate([83, 5, 65]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_washer_m4_08.stl");
if (show_child) color("Silver") translate([83, -3.8, 65]) rotate([90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_child) color("Silver") translate([50.5, 14, 12]) rotate([0, 90, 0])  import("../../parts/common/interior/cots/screw/screw_m3x20.stl");
if (show_child) color("Silver") translate([50, 14, 12]) rotate([0, 90, 0])  import("../../parts/common/interior/cots/screw/screw_washer_m3_05.stl");
if (show_child) color("Silver") translate([35.8, 14, 12]) rotate([0, -90, 0]) rotate([0, 0, 30])  import("../../parts/common/interior/cots/screw/screw_nut_m3.stl");
if (show_child) color("Silver") translate([50.5, 14, 32]) rotate([0, 90, 0])  import("../../parts/common/interior/cots/screw/screw_m3x20.stl");
if (show_child) color("Silver") translate([50, 14, 32]) rotate([0, 90, 0])  import("../../parts/common/interior/cots/screw/screw_washer_m3_05.stl");
if (show_child) color("Silver") translate([35.8, 14, 32]) rotate([0, -90, 0]) rotate([0, 0, 30])  import("../../parts/common/interior/cots/screw/screw_nut_m3.stl");

// View-only sensor/exterior SCHEMATICS, not measured fit models or print parts.

if(show_parent) translate([-45,0,0]) {
    // Symbolic acoustic direction only: no TD04A body or ear geometry.
    color("DodgerBlue") translate([0,-30,-65]) rotate([180,0,0]) { cylinder(d=1.5,h=14,$fn=20); translate([0,0,14]) cylinder(d1=5,d2=0,h=6,$fn=32); }
    color([0.1,0.8,0.6,0.25]) translate([-6,-25,-65]) cube([12,15,60]);
    color([.65,.72,.78,.35]) translate([-13,8,0]) cube([26,34,6]);
}


if(show_child) translate([45,0,0]) {
    // Symbolic acoustic direction only: no TD04A body or ear geometry.
    color("DodgerBlue") translate([32,-30,65]) rotate([0,0,0]) { cylinder(d=1.5,h=14,$fn=20); translate([0,0,14]) cylinder(d1=5,d2=0,h=6,$fn=32); }
    color([0.1,0.8,0.6,0.25]) translate([26,-25,5]) cube([12,15,60]);
    color([.65,.72,.78,.55]) import("_work/intermediate/child_side_reference.stl");
}
