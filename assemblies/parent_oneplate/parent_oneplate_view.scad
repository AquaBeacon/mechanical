// =====================================================================
// parent_oneplate_view.scad
// !! 自動生成ファイル - 編集しないこと。placement.json を直して
//    build.ps1 -Assemblies で再生成する。
// Repeatable box locating: three bottom datums, left two-point datum, end datum, retained keyed stops. Sensor support and camera mount register to the same open frame.
// 座標系: Box bottom Z=0; datum seats Z=0, main deck top Z=-0.8, underside Z=-12.
// =====================================================================

show_exterior = true;
show_vessel = true;
show_floats = true;
show_hardware = true;
show_pads = true;
show_envelope = true;

if (show_exterior) color("Orange")  import("../../parts/parent/exterior/printed/parent_oneplate_frame/parent_oneplate_frame.stl");
if (show_vessel) color("Silver", 1) translate([0, 0, -460]) translate([0, 0, 460]) translate([15, -115, 65]) rotate([-90, 0, 0])  import("../../parts/common/exterior/cots/wetlink_penetrator_m10/wetlink_penetrator_m10_ref_bcas.stl");
if (show_vessel) color("Silver", 1) translate([0, 0, -460]) translate([0, 0, 460]) translate([-20, -115, 65]) rotate([-90, 0, 0])  import("../../parts/common/exterior/cots/wetlink_penetrator_m10/wetlink_penetrator_m10_ref_bcas.stl");
if (show_floats) color("LightSkyBlue") translate([-178, 0, 0])  import("../../parts/parent/exterior/cots/parent_fender/parent_fender.stl");
if (show_floats) color("LightSkyBlue") translate([178, 0, 0])  import("../../parts/parent/exterior/cots/parent_fender/parent_fender.stl");
if (show_vessel) color("LightSteelBlue") translate([0, 0, 97.3])  import("../../assemblies/parent_clamped/reference/lid_envelope.stl");
if (show_exterior) color("Orange") translate([0, -55, 102.3])  import("../../parts/parent/exterior/printed/parent_oneplate_bar/parent_oneplate_bar.stl");
if (show_pads) color("DimGray") translate([-98, -55, 100.3])  import("../../assemblies/parent_clamped/reference/rubber_pad.stl");
if (show_pads) color("DimGray") translate([98, -55, 100.3])  import("../../assemblies/parent_clamped/reference/rubber_pad.stl");
if (show_hardware) color("Silver") translate([-110, -55, -20])  import("../../assemblies/parent_clamped/reference/rod_M5_150.stl");
if (show_hardware) color("Silver") translate([-110, -55, -13])  import("../../assemblies/parent_clamped/reference/washer_M5.stl");
if (show_hardware) color("Silver") translate([-110, -55, 114.3])  import("../../assemblies/parent_clamped/reference/washer_M5.stl");
if (show_hardware) color("Silver") translate([-110, -55, -18])  import("../../assemblies/parent_clamped/reference/nut_M5.stl");
if (show_hardware) color("Silver") translate([-110, -55, 115.3])  import("../../assemblies/parent_clamped/reference/nut_M5.stl");
if (show_hardware) color("Silver") translate([110, -55, -20])  import("../../assemblies/parent_clamped/reference/rod_M5_150.stl");
if (show_hardware) color("Silver") translate([110, -55, -13])  import("../../assemblies/parent_clamped/reference/washer_M5.stl");
if (show_hardware) color("Silver") translate([110, -55, 114.3])  import("../../assemblies/parent_clamped/reference/washer_M5.stl");
if (show_hardware) color("Silver") translate([110, -55, -18])  import("../../assemblies/parent_clamped/reference/nut_M5.stl");
if (show_hardware) color("Silver") translate([110, -55, 115.3])  import("../../assemblies/parent_clamped/reference/nut_M5.stl");
if (show_exterior) color("Orange") translate([0, 55, 102.3])  import("../../parts/parent/exterior/printed/parent_oneplate_bar/parent_oneplate_bar.stl");
if (show_pads) color("DimGray") translate([-98, 55, 100.3])  import("../../assemblies/parent_clamped/reference/rubber_pad.stl");
if (show_pads) color("DimGray") translate([98, 55, 100.3])  import("../../assemblies/parent_clamped/reference/rubber_pad.stl");
if (show_hardware) color("Silver") translate([-110, 55, -20])  import("../../assemblies/parent_clamped/reference/rod_M5_150.stl");
if (show_hardware) color("Silver") translate([-110, 55, -13])  import("../../assemblies/parent_clamped/reference/washer_M5.stl");
if (show_hardware) color("Silver") translate([-110, 55, 114.3])  import("../../assemblies/parent_clamped/reference/washer_M5.stl");
if (show_hardware) color("Silver") translate([-110, 55, -18])  import("../../assemblies/parent_clamped/reference/nut_M5.stl");
if (show_hardware) color("Silver") translate([-110, 55, 115.3])  import("../../assemblies/parent_clamped/reference/nut_M5.stl");
if (show_hardware) color("Silver") translate([110, 55, -20])  import("../../assemblies/parent_clamped/reference/rod_M5_150.stl");
if (show_hardware) color("Silver") translate([110, 55, -13])  import("../../assemblies/parent_clamped/reference/washer_M5.stl");
if (show_hardware) color("Silver") translate([110, 55, 114.3])  import("../../assemblies/parent_clamped/reference/washer_M5.stl");
if (show_hardware) color("Silver") translate([110, 55, -18])  import("../../assemblies/parent_clamped/reference/nut_M5.stl");
if (show_hardware) color("Silver") translate([110, 55, 115.3])  import("../../assemblies/parent_clamped/reference/nut_M5.stl");
if (show_exterior) color("Orange") translate([0, 0, 0])  import("../../parts/parent/exterior/printed/parent_oneplate_td_support/parent_oneplate_td_support.stl");
// Existing mount remains installed; seat its rear-plate end and right edge against the frame guides before tightening M3.
if (show_envelope) color("SteelBlue") translate([-40, -40, -55.45]) rotate([-90, 0, 0])  import("../../parts/child/exterior/printed/dji_osmo_action6_mount_m3/camera_mount.stl");
if (show_exterior) color("Orange") translate([55, 2, -35])  import("../../parts/parent/exterior/printed/parent_light_jaw/parent_light_jaw.stl");
if (show_envelope) color("DimGray") translate([55, 0, -100])  import("../../parts/common/exterior/cots/td04a_transducer/td04a_transducer.stl");
if (show_envelope) color("DimGray") translate([-40, -3.5, -55.45]) rotate([-90, 0, 0])  import("../../assemblies/parent_spar_bolted/reference/camera_case_envelope.stl");
if (show_hardware) color("Silver") translate([65, -55, 0])  import("../../assemblies/parent_light/reference/screw_M5_30_countersunk.stl");
if (show_hardware) color("Silver") translate([65, -55, -21])  import("../../assemblies/parent_clamped/reference/washer_M5.stl");
if (show_hardware) color("Silver") translate([65, -55, -26])  import("../../assemblies/parent_clamped/reference/nut_M5.stl");
if (show_hardware) color("Silver") translate([85, -55, 0])  import("../../assemblies/parent_light/reference/screw_M5_30_countersunk.stl");
if (show_hardware) color("Silver") translate([85, -55, -21])  import("../../assemblies/parent_clamped/reference/washer_M5.stl");
if (show_hardware) color("Silver") translate([85, -55, -26])  import("../../assemblies/parent_clamped/reference/nut_M5.stl");
if (show_hardware) color("Silver") translate([37, 10, -35]) rotate([-90, 0, 0])  import("../../assemblies/parent_clamped/reference/screw_M4_30.stl");
if (show_hardware) color("Silver") translate([73, 10, -35]) rotate([-90, 0, 0])  import("../../assemblies/parent_clamped/reference/screw_M4_30.stl");
if (show_exterior) color("MediumSeaGreen")  import("../../parts/parent/exterior/printed/parent_oneplate_box_locator/parent_oneplate_box_locator_side_left.stl");
if (show_exterior) color("MediumSeaGreen")  import("../../parts/parent/exterior/printed/parent_oneplate_box_locator/parent_oneplate_box_locator_side_right.stl");
if (show_exterior) color("MediumSeaGreen")  import("../../parts/parent/exterior/printed/parent_oneplate_box_locator/parent_oneplate_box_locator_end_fixed.stl");
if (show_exterior) color("MediumSeaGreen")  import("../../parts/parent/exterior/printed/parent_oneplate_box_locator/parent_oneplate_box_locator_end_push.stl");
if (show_exterior) color("MediumSeaGreen") translate([105, -38, 12]) rotate([0, 90, 0])  import("../../parts/parent/exterior/printed/parent_oneplate_box_locator/parent_oneplate_box_locator_pressure_pad.stl");
if (show_exterior) color("MediumSeaGreen") translate([105, 38, 12]) rotate([0, 90, 0])  import("../../parts/parent/exterior/printed/parent_oneplate_box_locator/parent_oneplate_box_locator_pressure_pad.stl");
if (show_exterior) color("MediumSeaGreen") translate([-94, -115, 9]) rotate([90, 0, 0])  import("../../parts/parent/exterior/printed/parent_oneplate_box_locator/parent_oneplate_box_locator_pressure_pad.stl");
// Fit adjustable contact tips to real case once; retain settings. Remove bridge before accessing rear M3 bolts.
if (show_exterior) color("MediumSeaGreen") translate([-40, -40, -55.45]) rotate([-90, 0, 0])  import("../../parts/parent/exterior/printed/parent_oneplate_camera_stop/parent_oneplate_camera_stop.stl");
if (show_hardware) color("Silver") translate([-110, -8, 1.4])  import("../../parts/common/interior/cots/screw/screw_m4x16_socket.stl");
if (show_hardware) color("Silver") translate([-110, -8, -12])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_hardware) color("Silver") translate([-110, 8, 1.4])  import("../../parts/common/interior/cots/screw/screw_m4x16_socket.stl");
if (show_hardware) color("Silver") translate([-110, 8, -12])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_hardware) color("Silver") translate([110, -8, 1.4])  import("../../parts/common/interior/cots/screw/screw_m4x16_socket.stl");
if (show_hardware) color("Silver") translate([110, -8, -12])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_hardware) color("Silver") translate([110, 8, 1.4])  import("../../parts/common/interior/cots/screw/screw_m4x16_socket.stl");
if (show_hardware) color("Silver") translate([110, 8, -12])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_hardware) color("Silver") translate([-94, -52, -14.4]) rotate([180, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m4x14_socket.stl");
if (show_hardware) color("Silver") translate([-94, -52, -4.2])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_hardware) color("Silver") translate([-94, -62, -14.4]) rotate([180, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m4x14_socket.stl");
if (show_hardware) color("Silver") translate([-94, -62, -4.2])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_hardware) color("Silver") translate([94, 52, -14.4]) rotate([180, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m4x14_socket.stl");
if (show_hardware) color("Silver") translate([94, 52, -4.2])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_hardware) color("Silver") translate([94, 62, -14.4]) rotate([180, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m4x14_socket.stl");
if (show_hardware) color("Silver") translate([94, 62, -4.2])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_hardware) color("Silver") translate([110.2, -38, 12]) rotate([0, -90, 0])  import("../../parts/common/interior/cots/screw/screw_m4x25_socket.stl");
if (show_hardware) color("Silver") translate([112.6, -38, 12]) rotate([0, 90, 0])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_hardware) color("Silver") translate([116, -38, 12]) rotate([0, 90, 0])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_hardware) color("Silver") translate([110.2, 38, 12]) rotate([0, -90, 0])  import("../../parts/common/interior/cots/screw/screw_m4x25_socket.stl");
if (show_hardware) color("Silver") translate([112.6, 38, 12]) rotate([0, 90, 0])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_hardware) color("Silver") translate([116, 38, 12]) rotate([0, 90, 0])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_hardware) color("Silver") translate([-94, -120.2, 9]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m4x25_socket.stl");
if (show_hardware) color("Silver") translate([-94, -127, 9]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_hardware) color("Silver") translate([-94, -130.2, 9]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_hardware) color("Silver") translate([-40, -40, -55.45]) rotate([-90, 0, 0]) translate([-20, 35, 20]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m4x20_socket.stl");
if (show_hardware) color("Silver") translate([-40, -40, -55.45]) rotate([-90, 0, 0]) translate([-20, 19.8, 20]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_hardware) color("Silver") translate([-40, -40, -55.45]) rotate([-90, 0, 0]) translate([-20, 20, 24.5]) rotate([180, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m4x12_socket.stl");
if (show_hardware) color("Silver") translate([-40, -40, -55.45]) rotate([-90, 0, 0]) translate([-20, 20, 32.2])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_hardware) color("Silver") translate([-40, -40, -55.45]) rotate([-90, 0, 0]) translate([-20, 20, 29])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_hardware) color("Silver") translate([-40, -40, -55.45]) rotate([-90, 0, 0]) translate([20, 35, 20]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m4x20_socket.stl");
if (show_hardware) color("Silver") translate([-40, -40, -55.45]) rotate([-90, 0, 0]) translate([20, 19.8, 20]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_hardware) color("Silver") translate([-40, -40, -55.45]) rotate([-90, 0, 0]) translate([20, 20, 24.5]) rotate([180, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m4x12_socket.stl");
if (show_hardware) color("Silver") translate([-40, -40, -55.45]) rotate([-90, 0, 0]) translate([20, 20, 32.2])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_hardware) color("Silver") translate([-40, -40, -55.45]) rotate([-90, 0, 0]) translate([20, 20, 29])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_vessel) color("LightSteelBlue", 0.65) translate([0, 0, -460]) translate([0, 0, 460]) translate([-105, -115, 0])  import("../../parts/parent/exterior/cots/bcas212310g/bcas212310g.stl");
