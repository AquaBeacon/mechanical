// =====================================================================
// parent_simple_view.scad
// !! 自動生成ファイル - 編集しないこと。placement.json を直して
//    build.ps1 -Assemblies で再生成する。
// Simple deck with reserved underside mount holes. Floats are reference envelopes; ropes and accessory mounts are not modelled.
// 座標系: Box bottom Z=0. Deck Z=-12..0.
// =====================================================================

show_exterior = true;
show_vessel = true;
show_floats = true;

if (show_exterior) color("Orange")  import("../../parts/parent/exterior/printed/parent_simple_deck/parent_simple_deck.stl");
if (show_vessel) color("Silver", 1) translate([0, 0, -460]) translate([0, 0, 460]) translate([15, -115, 65]) rotate([-90, 0, 0])  import("../../parts/common/exterior/cots/wetlink_penetrator_m10/wetlink_penetrator_m10_ref_bcas.stl");
if (show_vessel) color("Silver", 1) translate([0, 0, -460]) translate([0, 0, 460]) translate([-20, -115, 65]) rotate([-90, 0, 0])  import("../../parts/common/exterior/cots/wetlink_penetrator_m10/wetlink_penetrator_m10_ref_bcas.stl");
if (show_floats) color("LightSkyBlue") translate([-178, 0, 0])  import("../../parts/parent/exterior/cots/parent_fender/parent_fender.stl");
if (show_floats) color("LightSkyBlue") translate([178, 0, 0])  import("../../parts/parent/exterior/cots/parent_fender/parent_fender.stl");
if (show_vessel) color("LightSteelBlue", 0.22) translate([0, 0, -460]) translate([0, 0, 460]) translate([-105, -115, 0])  import("../../assemblies/parent_bottom_sensors/reference/bcas_mounting_reference.stl");
