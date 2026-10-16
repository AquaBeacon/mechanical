// =====================================================================
// parent_clamped_view.scad
// !! 自動生成ファイル - 編集しないこと。placement.json を直して
//    build.ps1 -Assemblies で再生成する。
// External rod clamp. Hardware, rubber pads and lid are schematic references. Remove upper bars to open lid.
// 座標系: Box bottom Z=0. Deck Z=-12..0.
// =====================================================================

show_exterior = true;
show_vessel = true;
show_floats = true;
show_hardware = true;
show_pads = true;

if (show_exterior) color("Orange")  import("../../parts/parent/exterior/printed/parent_clamped_deck/parent_clamped_deck.stl");
if (show_vessel) color("Silver", 1) translate([0, 0, -460]) translate([0, 0, 460]) translate([15, -115, 65]) rotate([-90, 0, 0])  import("../../parts/common/exterior/cots/wetlink_penetrator_m10/wetlink_penetrator_m10_ref_bcas.stl");
if (show_vessel) color("Silver", 1) translate([0, 0, -460]) translate([0, 0, 460]) translate([-20, -115, 65]) rotate([-90, 0, 0])  import("../../parts/common/exterior/cots/wetlink_penetrator_m10/wetlink_penetrator_m10_ref_bcas.stl");
if (show_floats) color("LightSkyBlue") translate([-178, 0, 0])  import("../../parts/parent/exterior/cots/parent_fender/parent_fender.stl");
if (show_floats) color("LightSkyBlue") translate([178, 0, 0])  import("../../parts/parent/exterior/cots/parent_fender/parent_fender.stl");
if (show_exterior) color("Orange") translate([0, -85, 0]) mirror([1, 0, 0])  import("../../parts/parent/exterior/printed/parent_float_lug/parent_float_lug.stl");
if (show_exterior) color("Orange") translate([0, 85, 0]) mirror([1, 0, 0])  import("../../parts/parent/exterior/printed/parent_float_lug/parent_float_lug.stl");
if (show_exterior) color("Orange") translate([0, -85, 0])  import("../../parts/parent/exterior/printed/parent_float_lug/parent_float_lug.stl");
if (show_exterior) color("Orange") translate([0, 85, 0])  import("../../parts/parent/exterior/printed/parent_float_lug/parent_float_lug.stl");
if (show_vessel) color("LightSteelBlue") translate([0, 0, 97.3])  import("../../assemblies/parent_clamped/reference/lid_envelope.stl");
if (show_hardware) color("Silver") translate([-112, -93, 0])  import("../../assemblies/parent_clamped/reference/screw_M5_30.stl");
if (show_hardware) color("Silver") translate([-112, -93, -21])  import("../../assemblies/parent_clamped/reference/washer_M5.stl");
if (show_hardware) color("Silver") translate([-112, -93, -26])  import("../../assemblies/parent_clamped/reference/nut_M5.stl");
if (show_hardware) color("Silver") translate([-112, -77, 0])  import("../../assemblies/parent_clamped/reference/screw_M5_30.stl");
if (show_hardware) color("Silver") translate([-112, -77, -21])  import("../../assemblies/parent_clamped/reference/washer_M5.stl");
if (show_hardware) color("Silver") translate([-112, -77, -26])  import("../../assemblies/parent_clamped/reference/nut_M5.stl");
if (show_hardware) color("Silver") translate([-112, 77, 0])  import("../../assemblies/parent_clamped/reference/screw_M5_30.stl");
if (show_hardware) color("Silver") translate([-112, 77, -21])  import("../../assemblies/parent_clamped/reference/washer_M5.stl");
if (show_hardware) color("Silver") translate([-112, 77, -26])  import("../../assemblies/parent_clamped/reference/nut_M5.stl");
if (show_hardware) color("Silver") translate([-112, 93, 0])  import("../../assemblies/parent_clamped/reference/screw_M5_30.stl");
if (show_hardware) color("Silver") translate([-112, 93, -21])  import("../../assemblies/parent_clamped/reference/washer_M5.stl");
if (show_hardware) color("Silver") translate([-112, 93, -26])  import("../../assemblies/parent_clamped/reference/nut_M5.stl");
if (show_hardware) color("Silver") translate([112, -93, 0])  import("../../assemblies/parent_clamped/reference/screw_M5_30.stl");
if (show_hardware) color("Silver") translate([112, -93, -21])  import("../../assemblies/parent_clamped/reference/washer_M5.stl");
if (show_hardware) color("Silver") translate([112, -93, -26])  import("../../assemblies/parent_clamped/reference/nut_M5.stl");
if (show_hardware) color("Silver") translate([112, -77, 0])  import("../../assemblies/parent_clamped/reference/screw_M5_30.stl");
if (show_hardware) color("Silver") translate([112, -77, -21])  import("../../assemblies/parent_clamped/reference/washer_M5.stl");
if (show_hardware) color("Silver") translate([112, -77, -26])  import("../../assemblies/parent_clamped/reference/nut_M5.stl");
if (show_hardware) color("Silver") translate([112, 77, 0])  import("../../assemblies/parent_clamped/reference/screw_M5_30.stl");
if (show_hardware) color("Silver") translate([112, 77, -21])  import("../../assemblies/parent_clamped/reference/washer_M5.stl");
if (show_hardware) color("Silver") translate([112, 77, -26])  import("../../assemblies/parent_clamped/reference/nut_M5.stl");
if (show_hardware) color("Silver") translate([112, 93, 0])  import("../../assemblies/parent_clamped/reference/screw_M5_30.stl");
if (show_hardware) color("Silver") translate([112, 93, -21])  import("../../assemblies/parent_clamped/reference/washer_M5.stl");
if (show_hardware) color("Silver") translate([112, 93, -26])  import("../../assemblies/parent_clamped/reference/nut_M5.stl");
if (show_exterior) color("Orange") translate([0, -55, 102.3])  import("../../parts/parent/exterior/printed/parent_clamp_bar/parent_clamp_bar.stl");
if (show_pads) color("DimGray") translate([-98, -55, 100.3])  import("../../assemblies/parent_clamped/reference/rubber_pad.stl");
if (show_pads) color("DimGray") translate([98, -55, 100.3])  import("../../assemblies/parent_clamped/reference/rubber_pad.stl");
if (show_hardware) color("Silver") translate([-112, -55, -20])  import("../../assemblies/parent_clamped/reference/rod_M5_150.stl");
if (show_hardware) color("Silver") translate([-112, -55, -13])  import("../../assemblies/parent_clamped/reference/washer_M5.stl");
if (show_hardware) color("Silver") translate([-112, -55, 114.3])  import("../../assemblies/parent_clamped/reference/washer_M5.stl");
if (show_hardware) color("Silver") translate([-112, -55, -18])  import("../../assemblies/parent_clamped/reference/nut_M5.stl");
if (show_hardware) color("Silver") translate([-112, -55, 115.3])  import("../../assemblies/parent_clamped/reference/nut_M5.stl");
if (show_hardware) color("Silver") translate([112, -55, -20])  import("../../assemblies/parent_clamped/reference/rod_M5_150.stl");
if (show_hardware) color("Silver") translate([112, -55, -13])  import("../../assemblies/parent_clamped/reference/washer_M5.stl");
if (show_hardware) color("Silver") translate([112, -55, 114.3])  import("../../assemblies/parent_clamped/reference/washer_M5.stl");
if (show_hardware) color("Silver") translate([112, -55, -18])  import("../../assemblies/parent_clamped/reference/nut_M5.stl");
if (show_hardware) color("Silver") translate([112, -55, 115.3])  import("../../assemblies/parent_clamped/reference/nut_M5.stl");
if (show_exterior) color("Orange") translate([0, 55, 102.3])  import("../../parts/parent/exterior/printed/parent_clamp_bar/parent_clamp_bar.stl");
if (show_pads) color("DimGray") translate([-98, 55, 100.3])  import("../../assemblies/parent_clamped/reference/rubber_pad.stl");
if (show_pads) color("DimGray") translate([98, 55, 100.3])  import("../../assemblies/parent_clamped/reference/rubber_pad.stl");
if (show_hardware) color("Silver") translate([-112, 55, -20])  import("../../assemblies/parent_clamped/reference/rod_M5_150.stl");
if (show_hardware) color("Silver") translate([-112, 55, -13])  import("../../assemblies/parent_clamped/reference/washer_M5.stl");
if (show_hardware) color("Silver") translate([-112, 55, 114.3])  import("../../assemblies/parent_clamped/reference/washer_M5.stl");
if (show_hardware) color("Silver") translate([-112, 55, -18])  import("../../assemblies/parent_clamped/reference/nut_M5.stl");
if (show_hardware) color("Silver") translate([-112, 55, 115.3])  import("../../assemblies/parent_clamped/reference/nut_M5.stl");
if (show_hardware) color("Silver") translate([112, 55, -20])  import("../../assemblies/parent_clamped/reference/rod_M5_150.stl");
if (show_hardware) color("Silver") translate([112, 55, -13])  import("../../assemblies/parent_clamped/reference/washer_M5.stl");
if (show_hardware) color("Silver") translate([112, 55, 114.3])  import("../../assemblies/parent_clamped/reference/washer_M5.stl");
if (show_hardware) color("Silver") translate([112, 55, -18])  import("../../assemblies/parent_clamped/reference/nut_M5.stl");
if (show_hardware) color("Silver") translate([112, 55, 115.3])  import("../../assemblies/parent_clamped/reference/nut_M5.stl");
if (show_vessel) color("LightSteelBlue", 0.65) translate([0, 0, -460]) translate([0, 0, 460]) translate([-105, -115, 0])  import("../../parts/parent/exterior/cots/bcas212310g/bcas212310g.stl");
