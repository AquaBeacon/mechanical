// =====================================================================
// parent_exterior_view.scad
// !! 自動生成ファイル - 編集しないこと。placement.json を直して
//    build.ps1 -Assemblies で再生成する。
// Rev.7 flat lower plate, four removable vessel locators; retain printed upper clamp/skids and current integral camera. Side M4x20 x4, end M4x25 x4, M4 nuts x8.
// 座標系: Box datums Z=0; main plate top -0.8, flat underside/end-arm bottoms -20; end arms -20..-8; rope axes X=+/-111.5,Y=+/-23 along Z; C interface -30; ground -72. Spare nut floors -7.3, example screw tips -2.
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
if (show_vessel) color("LightSteelBlue") translate([0, 0, 97.3])  import("../../parts/common/exterior/cots/parent_clamp_hardware/lid_envelope.stl");
if (show_pads) color("DimGray") translate([-98, -55, 100.3])  import("../../parts/common/exterior/cots/parent_clamp_hardware/rubber_pad.stl");
if (show_pads) color("DimGray") translate([98, -55, 100.3])  import("../../parts/common/exterior/cots/parent_clamp_hardware/rubber_pad.stl");
if (show_hardware) color("Silver") translate([-110, -55, 142])  import("../../parts/common/interior/cots/screw/screw_rod_m5x180.stl");
if (show_hardware) color("Silver") translate([-110, -55, -31])  import("../../parts/common/exterior/cots/parent_clamp_hardware/washer_M5.stl");
if (show_hardware) color("Silver") translate([-110, -55, 122.3])  import("../../parts/common/exterior/cots/parent_clamp_hardware/washer_M5.stl");
if (show_hardware) color("Silver") translate([-110, -55, -35])  import("../../parts/common/interior/cots/screw/screw_nut_m5_4.stl");
if (show_hardware) color("Silver") translate([-110, -55, 123.3])  import("../../parts/common/interior/cots/screw/screw_nut_m5_4.stl");
if (show_hardware) color("Silver") translate([110, -55, 142])  import("../../parts/common/interior/cots/screw/screw_rod_m5x180.stl");
if (show_hardware) color("Silver") translate([110, -55, -31])  import("../../parts/common/exterior/cots/parent_clamp_hardware/washer_M5.stl");
if (show_hardware) color("Silver") translate([110, -55, 122.3])  import("../../parts/common/exterior/cots/parent_clamp_hardware/washer_M5.stl");
if (show_hardware) color("Silver") translate([110, -55, -35])  import("../../parts/common/interior/cots/screw/screw_nut_m5_4.stl");
if (show_hardware) color("Silver") translate([110, -55, 123.3])  import("../../parts/common/interior/cots/screw/screw_nut_m5_4.stl");
if (show_pads) color("DimGray") translate([-98, 55, 100.3])  import("../../parts/common/exterior/cots/parent_clamp_hardware/rubber_pad.stl");
if (show_pads) color("DimGray") translate([98, 55, 100.3])  import("../../parts/common/exterior/cots/parent_clamp_hardware/rubber_pad.stl");
if (show_hardware) color("Silver") translate([-110, 55, 142])  import("../../parts/common/interior/cots/screw/screw_rod_m5x180.stl");
if (show_hardware) color("Silver") translate([-110, 55, -31])  import("../../parts/common/exterior/cots/parent_clamp_hardware/washer_M5.stl");
if (show_hardware) color("Silver") translate([-110, 55, 122.3])  import("../../parts/common/exterior/cots/parent_clamp_hardware/washer_M5.stl");
if (show_hardware) color("Silver") translate([-110, 55, -35])  import("../../parts/common/interior/cots/screw/screw_nut_m5_4.stl");
if (show_hardware) color("Silver") translate([-110, 55, 123.3])  import("../../parts/common/interior/cots/screw/screw_nut_m5_4.stl");
if (show_hardware) color("Silver") translate([110, 55, 142])  import("../../parts/common/interior/cots/screw/screw_rod_m5x180.stl");
if (show_hardware) color("Silver") translate([110, 55, -31])  import("../../parts/common/exterior/cots/parent_clamp_hardware/washer_M5.stl");
if (show_hardware) color("Silver") translate([110, 55, 122.3])  import("../../parts/common/exterior/cots/parent_clamp_hardware/washer_M5.stl");
if (show_hardware) color("Silver") translate([110, 55, -35])  import("../../parts/common/interior/cots/screw/screw_nut_m5_4.stl");
if (show_hardware) color("Silver") translate([110, 55, 123.3])  import("../../parts/common/interior/cots/screw/screw_nut_m5_4.stl");
// 25 mm clamp shifted 12 mm right from front-view left edge; rear lower 20 mm keepout; 41 mm measured case thickness. Physical fit pending.
if (show_envelope) color("SteelBlue") translate([-40, -40, -91.95]) rotate([-90, 0, 0])  import("../../parts/child/exterior/printed/dji_osmo_action6_mount_m3/camera_mount_twist.stl");
// Depth 41 mm measured; case rear is aligned to original backplate -23.45. Actual M5-axis offset remains unmeasured.
if (show_envelope) color("DimGray") translate([-40, -40, -91.95]) rotate([-90, 0, 0])  import("../../parts/child/exterior/printed/dji_osmo_action6_mount_m3/camera_case_41mm.stl");
if (show_hardware) color("Silver") translate([65, -55, -0.8])  import("../../parts/common/interior/cots/screw/screw_m5x40_flat.stl");
if (show_hardware) color("Silver") translate([65, -55, -26])  import("../../parts/common/exterior/cots/parent_clamp_hardware/washer_M5.stl");
if (show_hardware) color("Silver") translate([65, -55, -30])  import("../../parts/common/interior/cots/screw/screw_nut_m5_4.stl");
if (show_hardware) color("Silver") translate([85, -55, -0.8])  import("../../parts/common/interior/cots/screw/screw_m5x40_flat.stl");
if (show_hardware) color("Silver") translate([85, -55, -26])  import("../../parts/common/exterior/cots/parent_clamp_hardware/washer_M5.stl");
if (show_hardware) color("Silver") translate([85, -55, -30])  import("../../parts/common/interior/cots/screw/screw_nut_m5_4.stl");
if (show_exterior) color("MediumSeaGreen") translate([105, -38, 12]) rotate([0, 90, 0])  import("../../parts/parent/exterior/printed/parent_oneplate_box_locator/parent_oneplate_box_locator_pressure_pad.stl");
if (show_exterior) color("MediumSeaGreen") translate([105, 38, 12]) rotate([0, 90, 0])  import("../../parts/parent/exterior/printed/parent_oneplate_box_locator/parent_oneplate_box_locator_pressure_pad.stl");
if (show_exterior) color("MediumSeaGreen") translate([-94, -115, 9]) rotate([90, 0, 0])  import("../../parts/parent/exterior/printed/parent_oneplate_box_locator/parent_oneplate_box_locator_pressure_pad.stl");
if (show_hardware) color("Silver") translate([110.2, -38, 12]) rotate([0, -90, 0])  import("../../parts/common/interior/cots/screw/screw_m4x25_socket.stl");
if (show_hardware) color("Silver") translate([112.6, -38, 12]) rotate([0, 90, 0])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_hardware) color("Silver") translate([116, -38, 12]) rotate([0, 90, 0])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_hardware) color("Silver") translate([110.2, 38, 12]) rotate([0, -90, 0])  import("../../parts/common/interior/cots/screw/screw_m4x25_socket.stl");
if (show_hardware) color("Silver") translate([112.6, 38, 12]) rotate([0, 90, 0])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_hardware) color("Silver") translate([116, 38, 12]) rotate([0, 90, 0])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_hardware) color("Silver") translate([-94, -120.2, 9]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m4x25_socket.stl");
if (show_hardware) color("Silver") translate([-94, -127, 9]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_hardware) color("Silver") translate([-94, -130.2, 9]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_exterior) color("Orange") translate([-116, 0, 0]) rotate([0, 0, 180])  import("../../parts/parent/exterior/printed/parent_oneplate_stand/parent_oneplate_stand.stl");
if (show_exterior) color("Orange") translate([116, 0, 0]) rotate([0, 0, 0])  import("../../parts/parent/exterior/printed/parent_oneplate_stand/parent_oneplate_stand.stl");
if (show_exterior) color("Orange") translate([-40, 0, -30]) rotate([180, 0, 90])  import("../../parts/parent/exterior/printed/parent_oneplate_camera_qr/parent_oneplate_camera_qr_female.stl");
if (show_hardware) color("Silver") translate([-60, -20, -27.4]) rotate([180, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m3x25_socket.stl");
if (show_hardware) color("Silver") translate([-60, -20, -6.5])  import("../../parts/common/interior/cots/screw/screw_nut_m3.stl");
if (show_hardware) color("Silver") translate([-60, 20, -27.4]) rotate([180, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m3x25_socket.stl");
if (show_hardware) color("Silver") translate([-60, 20, -6.5])  import("../../parts/common/interior/cots/screw/screw_nut_m3.stl");
if (show_hardware) color("Silver") translate([-20, -20, -27.4]) rotate([180, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m3x25_socket.stl");
if (show_hardware) color("Silver") translate([-20, -20, -6.5])  import("../../parts/common/interior/cots/screw/screw_nut_m3.stl");
if (show_hardware) color("Silver") translate([-20, 20, -27.4]) rotate([180, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m3x25_socket.stl");
if (show_hardware) color("Silver") translate([-20, 20, -6.5])  import("../../parts/common/interior/cots/screw/screw_nut_m3.stl");
if (show_exterior) color("Orange") translate([0, 0, 102.3])  import("../../parts/parent/exterior/printed/parent_oneplate_bar/parent_oneplate_bar.stl");
if (show_exterior) color("MediumSeaGreen")  import("../../parts/parent/exterior/printed/parent_oneplate_box_locator/parent_oneplate_box_locator_side_left.stl");
if (show_exterior) color("MediumSeaGreen")  import("../../parts/parent/exterior/printed/parent_oneplate_box_locator/parent_oneplate_box_locator_side_right.stl");
if (show_exterior) color("MediumSeaGreen")  import("../../parts/parent/exterior/printed/parent_oneplate_box_locator/parent_oneplate_box_locator_end_fixed.stl");
if (show_exterior) color("MediumSeaGreen")  import("../../parts/parent/exterior/printed/parent_oneplate_box_locator/parent_oneplate_box_locator_end_push.stl");
if (show_hardware) color("Silver") translate([-110, -8, 1.3])  import("../../parts/common/interior/cots/screw/screw_m4x20_socket.stl");
if (show_hardware) color("Silver") translate([-110, -8, -15.5])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_hardware) color("Silver") translate([-110, 8, 1.3])  import("../../parts/common/interior/cots/screw/screw_m4x20_socket.stl");
if (show_hardware) color("Silver") translate([-110, 8, -15.5])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_hardware) color("Silver") translate([110, -8, 1.3])  import("../../parts/common/interior/cots/screw/screw_m4x20_socket.stl");
if (show_hardware) color("Silver") translate([110, -8, -15.5])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_hardware) color("Silver") translate([110, 8, 1.3])  import("../../parts/common/interior/cots/screw/screw_m4x20_socket.stl");
if (show_hardware) color("Silver") translate([110, 8, -15.5])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_hardware) color("Silver") translate([-94, -52, -27.3]) rotate([180, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m4x25_socket.stl");
if (show_hardware) color("Silver") translate([-94, -52, -7.3])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_hardware) color("Silver") translate([-94, -62, -27.3]) rotate([180, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m4x25_socket.stl");
if (show_hardware) color("Silver") translate([-94, -62, -7.3])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_hardware) color("Silver") translate([94, 52, -27.3]) rotate([180, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m4x25_socket.stl");
if (show_hardware) color("Silver") translate([94, 52, -7.3])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_hardware) color("Silver") translate([94, 62, -27.3]) rotate([180, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m4x25_socket.stl");
if (show_hardware) color("Silver") translate([94, 62, -7.3])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
// Rev.6; sensor ear thickness 3 mm is provisional; rejected body model omitted.
if (show_exterior) color("DarkOrange") translate([53, -55, -20]) rotate([0, 0, -90]) translate([45, 0, 0]) translate([-45, 0, 0])  import("../../parts/common/exterior/printed/td04a_bracket_mount/td04a_bracket_mount_parent_down.stl");
// Rev.6; sensor ear thickness 3 mm is provisional; rejected body model omitted.
if (show_hardware) color("Silver") translate([53, -55, -20]) rotate([0, 0, -90]) translate([45, 0, 0]) translate([-51, 5.8, -65]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m4x14_socket.stl");
// Rev.6; sensor ear thickness 3 mm is provisional; rejected body model omitted.
if (show_hardware) color("Silver") translate([53, -55, -20]) rotate([0, 0, -90]) translate([45, 0, 0]) translate([-51, -3, -65]) rotate([90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_washer_m4_08.stl");
// Rev.6; sensor ear thickness 3 mm is provisional; rejected body model omitted.
if (show_hardware) color("Silver") translate([53, -55, -20]) rotate([0, 0, -90]) translate([45, 0, 0]) translate([-51, 5, -65]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_washer_m4_08.stl");
// Rev.6; sensor ear thickness 3 mm is provisional; rejected body model omitted.
if (show_hardware) color("Silver") translate([53, -55, -20]) rotate([0, 0, -90]) translate([45, 0, 0]) translate([-51, -3.8, -65]) rotate([90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
// Rev.6; sensor ear thickness 3 mm is provisional; rejected body model omitted.
if (show_hardware) color("Silver") translate([53, -55, -20]) rotate([0, 0, -90]) translate([45, 0, 0]) translate([-39, 5.8, -65]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m4x14_socket.stl");
// Rev.6; sensor ear thickness 3 mm is provisional; rejected body model omitted.
if (show_hardware) color("Silver") translate([53, -55, -20]) rotate([0, 0, -90]) translate([45, 0, 0]) translate([-39, -3, -65]) rotate([90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_washer_m4_08.stl");
// Rev.6; sensor ear thickness 3 mm is provisional; rejected body model omitted.
if (show_hardware) color("Silver") translate([53, -55, -20]) rotate([0, 0, -90]) translate([45, 0, 0]) translate([-39, 5, -65]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_washer_m4_08.stl");
// Rev.6; sensor ear thickness 3 mm is provisional; rejected body model omitted.
if (show_hardware) color("Silver") translate([53, -55, -20]) rotate([0, 0, -90]) translate([45, 0, 0]) translate([-39, -3.8, -65]) rotate([90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_accessories) color("Orange") translate([-40, -40, -91.95]) rotate([-90, 0, 0])  import("../../parts/child/exterior/printed/dji_osmo_action6_mount_m3/camera_front_clamp.stl");
if (show_fasteners) color("Silver") translate([-40, -40, -91.95]) rotate([-90, 0, 0]) translate([11.5, 11.5, 4]) rotate([180, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m4x16_socket.stl");
if (show_fasteners) color("Silver") translate([-40, -40, -91.95]) rotate([-90, 0, 0]) translate([11.5, 11.5, 4])  import("../../parts/common/interior/cots/screw/screw_washer_m4_08.stl");
if (show_fasteners) color("Silver") translate([-40, -40, -91.95]) rotate([-90, 0, 0]) translate([11.5, 11.5, 10.6]) rotate([0, 0, 30])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_fasteners) color("Silver") translate([-40, -40, -91.95]) rotate([-90, 0, 0]) translate([24.5, 11.5, 4]) rotate([180, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m4x16_socket.stl");
if (show_fasteners) color("Silver") translate([-40, -40, -91.95]) rotate([-90, 0, 0]) translate([24.5, 11.5, 4])  import("../../parts/common/interior/cots/screw/screw_washer_m4_08.stl");
if (show_fasteners) color("Silver") translate([-40, -40, -91.95]) rotate([-90, 0, 0]) translate([24.5, 11.5, 10.6]) rotate([0, 0, 30])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_fasteners) color("Silver") translate([-40, 0, -30]) rotate([180, 0, 90]) translate([0, -52, 31.5])  import("../../parts/child/exterior/printed/dji_osmo_action6_mount_m3/camera_m3x30_hex.stl");
if (show_fasteners) color("Silver") translate([-40, 0, -30]) rotate([180, 0, 90]) translate([0, -52, 2.4]) rotate([0, 0, 30])  import("../../parts/common/interior/cots/screw/screw_nut_m3.stl");
if (show_accessories) color("Orange") translate([-40, 0, -30]) rotate([180, 0, 90]) translate([0, -52, 8])  import("../../parts/child/exterior/printed/dji_osmo_action6_mount_m3/camera_hand_spacer.stl");
if (show_accessories) color("SeaGreen") translate([-40, 0, -30]) rotate([180, 0, 90]) translate([0, -52, 30.5])  import("../../parts/child/exterior/printed/dji_osmo_action6_mount_m3/camera_hand_knob.stl");
if (show_accessories) color("SeaGreen") translate([-40, 0, -30]) rotate([180, 0, 90]) translate([0, -52, 33.5])  import("../../parts/child/exterior/printed/dji_osmo_action6_mount_m3/camera_hand_knob_cap.stl");
if (show_fasteners) color("Silver") translate([-40, 0, -30]) rotate([180, 0, 90]) translate([0, 52, 31.5])  import("../../parts/child/exterior/printed/dji_osmo_action6_mount_m3/camera_m3x30_hex.stl");
if (show_fasteners) color("Silver") translate([-40, 0, -30]) rotate([180, 0, 90]) translate([0, 52, 2.4]) rotate([0, 0, 30])  import("../../parts/common/interior/cots/screw/screw_nut_m3.stl");
if (show_accessories) color("Orange") translate([-40, 0, -30]) rotate([180, 0, 90]) translate([0, 52, 8])  import("../../parts/child/exterior/printed/dji_osmo_action6_mount_m3/camera_hand_spacer.stl");
if (show_accessories) color("SeaGreen") translate([-40, 0, -30]) rotate([180, 0, 90]) translate([0, 52, 30.5])  import("../../parts/child/exterior/printed/dji_osmo_action6_mount_m3/camera_hand_knob.stl");
if (show_accessories) color("SeaGreen") translate([-40, 0, -30]) rotate([180, 0, 90]) translate([0, 52, 33.5])  import("../../parts/child/exterior/printed/dji_osmo_action6_mount_m3/camera_hand_knob_cap.stl");
if (show_vessel) color("LightSteelBlue", 0.65) translate([0, 0, -460]) translate([0, 0, 460]) translate([-105, -115, 0])  import("../../parts/parent/exterior/cots/bcas212310g/bcas212310g.stl");
