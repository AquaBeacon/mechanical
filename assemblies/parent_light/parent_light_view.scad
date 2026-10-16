// =====================================================================
// parent_light_view.scad
// !! 自動生成ファイル - 編集しないこと。placement.json を直して
//    build.ps1 -Assemblies で再生成する。
// Integrated downward float lugs and lightened members. Camera mount is existing hardware, not a new print.
// 座標系: Box bottom Z=0. Deck Z=-12..0.
// =====================================================================

show_exterior = true;
show_vessel = true;
show_floats = true;
show_hardware = true;
show_pads = true;
show_envelope = true;

if (show_exterior) color("Orange")  import("../../parts/parent/exterior/printed/parent_light_frame/parent_light_frame.stl");
if (show_vessel) color("Silver", 1) translate([0, 0, -460]) translate([0, 0, 460]) translate([15, -115, 65]) rotate([-90, 0, 0])  import("../../parts/common/exterior/cots/wetlink_penetrator_m10/wetlink_penetrator_m10_ref_bcas.stl");
if (show_vessel) color("Silver", 1) translate([0, 0, -460]) translate([0, 0, 460]) translate([-20, -115, 65]) rotate([-90, 0, 0])  import("../../parts/common/exterior/cots/wetlink_penetrator_m10/wetlink_penetrator_m10_ref_bcas.stl");
if (show_floats) color("LightSkyBlue") translate([-178, 0, 0])  import("../../parts/parent/exterior/cots/parent_fender/parent_fender.stl");
if (show_floats) color("LightSkyBlue") translate([178, 0, 0])  import("../../parts/parent/exterior/cots/parent_fender/parent_fender.stl");
if (show_vessel) color("LightSteelBlue") translate([0, 0, 97.3])  import("../../assemblies/parent_clamped/reference/lid_envelope.stl");
if (show_exterior) color("Orange") translate([0, -55, 102.3])  import("../../parts/parent/exterior/printed/parent_light_bar/parent_light_bar.stl");
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
if (show_exterior) color("Orange") translate([0, 55, 102.3])  import("../../parts/parent/exterior/printed/parent_light_bar/parent_light_bar.stl");
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
if (show_exterior) color("Orange") translate([0, 0, 0])  import("../../parts/parent/exterior/printed/parent_light_carrier/parent_light_carrier.stl");
// Existing mount; do not print again.
if (show_envelope) color("SteelBlue") translate([-48, 0, -66]) rotate([-90, 0, 0])  import("../../parts/parent/exterior/printed/parent_camera_mount/parent_camera_mount.stl");
if (show_exterior) color("Orange") translate([55, 2, -35])  import("../../parts/parent/exterior/printed/parent_light_jaw/parent_light_jaw.stl");
if (show_envelope) color("DimGray") translate([55, 0, -100])  import("../../parts/common/exterior/cots/td04a_transducer/td04a_transducer.stl");
if (show_envelope) color("DimGray") translate([-48, 36.5, -66]) rotate([-90, 0, 0])  import("../../assemblies/parent_spar_bolted/reference/camera_case_envelope.stl");
if (show_hardware) color("Silver") translate([-85, -55, 0])  import("../../assemblies/parent_light/reference/screw_M5_30_countersunk.stl");
if (show_hardware) color("Silver") translate([-85, -55, -21])  import("../../assemblies/parent_clamped/reference/washer_M5.stl");
if (show_hardware) color("Silver") translate([-85, -55, -26])  import("../../assemblies/parent_clamped/reference/nut_M5.stl");
if (show_hardware) color("Silver") translate([-65, -55, 0])  import("../../assemblies/parent_light/reference/screw_M5_30_countersunk.stl");
if (show_hardware) color("Silver") translate([-65, -55, -21])  import("../../assemblies/parent_clamped/reference/washer_M5.stl");
if (show_hardware) color("Silver") translate([-65, -55, -26])  import("../../assemblies/parent_clamped/reference/nut_M5.stl");
if (show_hardware) color("Silver") translate([65, -55, 0])  import("../../assemblies/parent_light/reference/screw_M5_30_countersunk.stl");
if (show_hardware) color("Silver") translate([65, -55, -21])  import("../../assemblies/parent_clamped/reference/washer_M5.stl");
if (show_hardware) color("Silver") translate([65, -55, -26])  import("../../assemblies/parent_clamped/reference/nut_M5.stl");
if (show_hardware) color("Silver") translate([85, -55, 0])  import("../../assemblies/parent_light/reference/screw_M5_30_countersunk.stl");
if (show_hardware) color("Silver") translate([85, -55, -21])  import("../../assemblies/parent_clamped/reference/washer_M5.stl");
if (show_hardware) color("Silver") translate([85, -55, -26])  import("../../assemblies/parent_clamped/reference/nut_M5.stl");
if (show_hardware) color("Silver") translate([-59, 8, -82]) rotate([-90, 0, 0])  import("../../assemblies/parent_clamped/reference/screw_M5_25.stl");
if (show_hardware) color("Silver") translate([-59, -9, -82]) rotate([-90, 0, 0])  import("../../assemblies/parent_clamped/reference/washer_M5.stl");
if (show_hardware) color("Silver") translate([-59, -14, -82]) rotate([-90, 0, 0])  import("../../assemblies/parent_clamped/reference/nut_M5.stl");
if (show_hardware) color("Silver") translate([-59, 8, -50]) rotate([-90, 0, 0])  import("../../assemblies/parent_clamped/reference/screw_M5_25.stl");
if (show_hardware) color("Silver") translate([-59, -9, -50]) rotate([-90, 0, 0])  import("../../assemblies/parent_clamped/reference/washer_M5.stl");
if (show_hardware) color("Silver") translate([-59, -14, -50]) rotate([-90, 0, 0])  import("../../assemblies/parent_clamped/reference/nut_M5.stl");
if (show_hardware) color("Silver") translate([-37, 8, -82]) rotate([-90, 0, 0])  import("../../assemblies/parent_clamped/reference/screw_M5_25.stl");
if (show_hardware) color("Silver") translate([-37, -9, -82]) rotate([-90, 0, 0])  import("../../assemblies/parent_clamped/reference/washer_M5.stl");
if (show_hardware) color("Silver") translate([-37, -14, -82]) rotate([-90, 0, 0])  import("../../assemblies/parent_clamped/reference/nut_M5.stl");
if (show_hardware) color("Silver") translate([-37, 8, -50]) rotate([-90, 0, 0])  import("../../assemblies/parent_clamped/reference/screw_M5_25.stl");
if (show_hardware) color("Silver") translate([-37, -9, -50]) rotate([-90, 0, 0])  import("../../assemblies/parent_clamped/reference/washer_M5.stl");
if (show_hardware) color("Silver") translate([-37, -14, -50]) rotate([-90, 0, 0])  import("../../assemblies/parent_clamped/reference/nut_M5.stl");
if (show_hardware) color("Silver") translate([37, 10, -35]) rotate([-90, 0, 0])  import("../../assemblies/parent_clamped/reference/screw_M4_30.stl");
if (show_hardware) color("Silver") translate([73, 10, -35]) rotate([-90, 0, 0])  import("../../assemblies/parent_clamped/reference/screw_M4_30.stl");
if (show_vessel) color("LightSteelBlue", 0.65) translate([0, 0, -460]) translate([0, 0, 460]) translate([-105, -115, 0])  import("../../parts/parent/exterior/cots/bcas212310g/bcas212310g.stl");
