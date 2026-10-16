// =====================================================================
// parent_rope_float_view.scad
// !! 自動生成ファイル - 編集しないこと。placement.json を直して
//    build.ps1 -Assemblies で再生成する。
// Two adjacent bought fenders attached ONLY by ropes. No float yokes, collars, rigid links, or cylindrical printed float stack.
// 座標系: Box bottom Z=0. Float placements and rope curves are a nominal illustration, not constrained rigid placements.
// =====================================================================

show_exterior = true;
show_interior = false;
show_vessel = true;
show_reference = true;
show_envelope = true;
show_hardware = true;
show_floats = true;
show_ropes = true;

if (show_exterior) color("Orange") translate([0, 0, -60]) translate([0, 0, -300])  import("../../parts/parent/exterior/printed/parent_spar_disk/parent_spar_disk.stl");
if (show_exterior) color("Gold") translate([0, 0, -60]) translate([30, -2, -295]) rotate([0, 0, 0])  import("../../parts/parent/exterior/printed/parent_spar_fin/parent_spar_fin.stl");
if (show_exterior) color("Gold") translate([0, 0, -60]) translate([2, 30, -295]) rotate([0, 0, 90])  import("../../parts/parent/exterior/printed/parent_spar_fin/parent_spar_fin.stl");
if (show_exterior) color("Gold") translate([0, 0, -60]) translate([-30, 2, -295]) rotate([0, 0, 180])  import("../../parts/parent/exterior/printed/parent_spar_fin/parent_spar_fin.stl");
if (show_exterior) color("Gold") translate([0, 0, -60]) translate([-2, -30, -295]) rotate([0, 0, 270])  import("../../parts/parent/exterior/printed/parent_spar_fin/parent_spar_fin.stl");
if (show_exterior) color("DarkOrange") translate([0, 0, -60]) translate([0, 0, -295])  import("../../parts/parent/exterior/printed/parent_spar_hub/parent_spar_hub.stl");
if (show_exterior) color("DarkOrange") translate([0, 0, -60]) translate([0, 0, -202])  import("../../parts/parent/exterior/printed/parent_spar_hub/parent_spar_hub.stl");
if (show_exterior) color("DarkSlateGray") translate([0, 0, -60]) translate([0, 0, -295])  import("../../parts/parent/exterior/printed/parent_spar_beam_lower/parent_spar_beam_lower.stl");
if (show_exterior) color("DarkSlateGray") translate([0, 0, -60]) translate([0, 0, -115])  import("../../parts/parent/exterior/printed/parent_spar_beam_upper/parent_spar_beam_upper.stl");
if (show_exterior) color("DarkOrange") translate([0, 0, -60]) translate([0, 0, -147])  import("../../parts/parent/exterior/printed/parent_spar_coupler_half/parent_spar_coupler_half.stl");
if (show_exterior) color("DarkOrange") translate([0, 0, -60]) translate([0, 0, -147]) mirror([0, 1, 0])  import("../../parts/parent/exterior/printed/parent_spar_coupler_half/parent_spar_coupler_half.stl");
if (show_exterior) color("SlateGray") translate([0, 0, -60]) translate([0, 0, -300]) rotate([180, 0, 0])  import("../../parts/parent/exterior/printed/parent_spar_ballast_body/parent_spar_ballast_body.stl");
if (show_exterior) color("SlateGray") translate([0, 0, -60]) translate([0, 0, -357])  import("../../parts/parent/exterior/printed/parent_spar_ballast_lid/parent_spar_ballast_lid.stl");
if (show_exterior) color("DarkOrange") translate([0, 0, -460]) translate([0, 0, 322])  import("../../parts/parent/exterior/printed/parent_spar_camera_bridge/parent_spar_camera_bridge.stl");
if (show_exterior) color("DarkOrange") translate([0, 0, -460]) translate([108, 70, 410])  import("../../parts/parent/exterior/printed/parent_spar_gps_bridge/parent_spar_gps_bridge.stl");
if (show_exterior) color("DarkOrange") translate([0, 0, -460]) translate([0, 0, 460])  import("../../parts/parent/exterior/printed/parent_deck/parent_deck.stl");
if (show_exterior) color("SteelBlue") translate([0, 0, -460]) translate([0, 190, 330])  import("../../parts/child/exterior/printed/dji_osmo_action6_mount/dji_osmo_action6_mount.stl");
// 南壁 x=120 (デッキ X=+15), z=65。C1 テザー。頭は箱外 y=-137..-115 (デッキ南縁 -118 の外)
if (show_vessel) color("Silver", 1) translate([0, 0, -460]) translate([0, 0, 460]) translate([15, -115, 65]) rotate([-90, 0, 0])  import("../../parts/common/exterior/cots/wetlink_penetrator_m10/wetlink_penetrator_m10_ref_bcas.stl");
// 南壁 x=85 (デッキ X=-20), z=65。C3 TD04A → 南縁切欠き (X -30..25) → キール南端フェアリード → 南座のソケットへ
if (show_vessel) color("Silver", 1) translate([0, 0, -460]) translate([0, 0, 460]) translate([-20, -115, 65]) rotate([-90, 0, 0])  import("../../parts/common/exterior/cots/wetlink_penetrator_m10/wetlink_penetrator_m10_ref_bcas.stl");
// p1 と同一 (箱 (15.5,103.5,24.8))
if (show_interior) color("SteelBlue", 1) translate([0, 0, -460]) translate([0, 0, 460]) translate([-89.5, -11.5, 24.8])  import("../../parts/parent/interior/pcb/parent_main/parent_main.stl");
// p1 と同一 (箱 (15.5,192.5,24.8))
if (show_interior) color("MediumSeaGreen", 1) translate([0, 0, -460]) translate([0, 0, 460]) translate([-89.5, 77.5, 24.8])  import("../../parts/parent/interior/pcb/parent_pwr/parent_pwr.stl");
// p1 と同一 (箱 (134.5,94.5,24.8) rot 90)
if (show_interior) color("Gold", 1) translate([0, 0, -460]) translate([0, 0, 460]) translate([29.5, -20.5, 24.8]) rotate([0, 0, 90])  import("../../parts/parent/interior/pcb/tx_improved/tx_improved.stl");
// p1 と同一 (箱 (188,15.5,24.8) rot 90)
if (show_interior) color("SandyBrown", 1) translate([0, 0, -460]) translate([0, 0, 460]) translate([83, -99.5, 24.8]) rotate([0, 0, 90])  import("../../parts/parent/interior/cots/spresense_logger/spresense_logger.stl");
// p1 と同一 (箱 (122.5,68,54.4) rot 180)
if (show_interior) color("IndianRed", 1) translate([0, 0, -460]) translate([0, 0, 460]) translate([17.5, -47, 54.4]) rotate([0, 0, 180])  import("../../parts/common/interior/cots/lipo_3s_2200_zeee/lipo_3s_2200_zeee_pack.stl");
// p1 と同一
if (show_interior) color("Goldenrod", 1) translate([0, 0, -460]) translate([0, 0, 460]) translate([-85, -91.5, 26.4])  import("../../parts/common/interior/cots/hex_spacer/hex_spacer_m3_mf25.stl");
// p1 と同一
if (show_interior) color("Goldenrod", 1) translate([0, 0, -460]) translate([0, 0, 460]) translate([18, -91.5, 26.4])  import("../../parts/common/interior/cots/hex_spacer/hex_spacer_m3_mf25.stl");
// p1 と同一
if (show_interior) color("Goldenrod", 1) translate([0, 0, -460]) translate([0, 0, 460]) translate([-85, -16, 26.4])  import("../../parts/common/interior/cots/hex_spacer/hex_spacer_m3_mf25.stl");
// p1 と同一
if (show_interior) color("Goldenrod", 1) translate([0, 0, -460]) translate([0, 0, 460]) translate([18, -16, 26.4])  import("../../parts/common/interior/cots/hex_spacer/hex_spacer_m3_mf25.stl");
if (show_reference) color("Black") translate([0, 0, -460]) translate([65, 70, 593])  import("../../assemblies/parent_spar_bolted/reference/gps_ann_mb1.stl");
if (show_envelope) color("DimGray") translate([0, 0, -460]) translate([0, 190, 366.5])  import("../../assemblies/parent_spar_bolted/reference/camera_case_envelope.stl");
if (show_envelope) color("LightSteelBlue") translate([0, 0, -460]) translate([-105, -115, 556.3])  import("../../assemblies/parent_spar_bolted/reference/box_lid_envelope.stl");
if (show_reference) color("Gray") translate([0, 0, -60]) translate([0, 0, -336])  import("../../assemblies/parent_spar_bolted/reference/ballast_rings.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([37, -17, -285]) rotate([-90, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m5x40.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([37, -17, -285]) rotate([-90, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([37, 16, -285]) rotate([-90, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([37, 17, -285]) rotate([-90, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/nut_m5.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([37, -17, -192]) rotate([-90, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m5x40.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([37, -17, -192]) rotate([-90, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([37, 16, -192]) rotate([-90, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([37, 17, -192]) rotate([-90, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/nut_m5.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([17, 37, -285]) rotate([-90, 0, 90])  import("../../assemblies/parent_spar_bolted/hardware/screw_m5x40.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([17, 37, -285]) rotate([-90, 0, 90])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-16, 37, -285]) rotate([-90, 0, 90])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-17, 37, -285]) rotate([-90, 0, 90])  import("../../assemblies/parent_spar_bolted/hardware/nut_m5.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([17, 37, -192]) rotate([-90, 0, 90])  import("../../assemblies/parent_spar_bolted/hardware/screw_m5x40.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([17, 37, -192]) rotate([-90, 0, 90])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-16, 37, -192]) rotate([-90, 0, 90])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-17, 37, -192]) rotate([-90, 0, 90])  import("../../assemblies/parent_spar_bolted/hardware/nut_m5.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-37, 17, -285]) rotate([-90, 0, 180])  import("../../assemblies/parent_spar_bolted/hardware/screw_m5x40.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-37, 17, -285]) rotate([-90, 0, 180])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-37, -16, -285]) rotate([-90, 0, 180])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-37, -17, -285]) rotate([-90, 0, 180])  import("../../assemblies/parent_spar_bolted/hardware/nut_m5.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-37, 17, -192]) rotate([-90, 0, 180])  import("../../assemblies/parent_spar_bolted/hardware/screw_m5x40.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-37, 17, -192]) rotate([-90, 0, 180])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-37, -16, -192]) rotate([-90, 0, 180])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-37, -17, -192]) rotate([-90, 0, 180])  import("../../assemblies/parent_spar_bolted/hardware/nut_m5.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-17, -37, -285]) rotate([-90, 0, 270])  import("../../assemblies/parent_spar_bolted/hardware/screw_m5x40.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-17, -37, -285]) rotate([-90, 0, 270])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([16, -37, -285]) rotate([-90, 0, 270])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([17, -37, -285]) rotate([-90, 0, 270])  import("../../assemblies/parent_spar_bolted/hardware/nut_m5.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-17, -37, -192]) rotate([-90, 0, 270])  import("../../assemblies/parent_spar_bolted/hardware/screw_m5x40.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-17, -37, -192]) rotate([-90, 0, 270])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([16, -37, -192]) rotate([-90, 0, 270])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([17, -37, -192]) rotate([-90, 0, 270])  import("../../assemblies/parent_spar_bolted/hardware/nut_m5.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-45, 10, -271]) rotate([0, 90, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m6x100.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-45, 10, -271]) rotate([0, 90, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m6x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([44, 10, -271]) rotate([0, 90, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m6x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([45, 10, -271]) rotate([0, 90, 0])  import("../../assemblies/parent_spar_bolted/hardware/nut_m6.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-45, 10, -178]) rotate([0, 90, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m6x100.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-45, 10, -178]) rotate([0, 90, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m6x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([44, 10, -178]) rotate([0, 90, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m6x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([45, 10, -178]) rotate([0, 90, 0])  import("../../assemblies/parent_spar_bolted/hardware/nut_m6.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-28, 0, -135]) rotate([0, 90, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m6x70.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-28, 0, -135]) rotate([0, 90, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m6x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([27, 0, -135]) rotate([0, 90, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m6x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([28, 0, -135]) rotate([0, 90, 0])  import("../../assemblies/parent_spar_bolted/hardware/nut_m6.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-28, 0, -95]) rotate([0, 90, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m6x70.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-28, 0, -95]) rotate([0, 90, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m6x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([27, 0, -95]) rotate([0, 90, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m6x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([28, 0, -95]) rotate([0, 90, 0])  import("../../assemblies/parent_spar_bolted/hardware/nut_m6.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-22, -28, -123]) rotate([-90, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m5x65.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-22, -28, -123]) rotate([-90, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-22, 27, -123]) rotate([-90, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-22, 28, -123]) rotate([-90, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/nut_m5.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-22, -28, -107]) rotate([-90, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m5x65.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-22, -28, -107]) rotate([-90, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-22, 27, -107]) rotate([-90, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-22, 28, -107]) rotate([-90, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/nut_m5.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([22, -28, -123]) rotate([-90, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m5x65.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([22, -28, -123]) rotate([-90, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([22, 27, -123]) rotate([-90, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([22, 28, -123]) rotate([-90, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/nut_m5.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([22, -28, -107]) rotate([-90, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m5x65.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([22, -28, -107]) rotate([-90, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([22, 27, -107]) rotate([-90, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([22, 28, -107]) rotate([-90, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/nut_m5.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-23, -23, -262]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m5x55.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-23, -23, -262]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-23, -23, -306]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-23, -23, -307]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/nut_m5.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-23, 23, -262]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m5x55.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-23, 23, -262]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-23, 23, -306]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-23, 23, -307]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/nut_m5.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([23, -23, -262]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m5x55.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([23, -23, -262]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([23, -23, -306]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([23, -23, -307]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/nut_m5.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([23, 23, -262]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m5x55.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([23, 23, -262]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([23, 23, -306]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([23, 23, -307]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/nut_m5.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([52, 0, -358]) rotate([0, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m5x20.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([52, 0, -358]) rotate([0, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([52, 0, -345]) rotate([0, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([52, 0, -344]) rotate([0, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/nut_m5.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([3.18408e-15, 52, -358]) rotate([0, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m5x20.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([3.18408e-15, 52, -358]) rotate([0, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([3.18408e-15, 52, -345]) rotate([0, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([3.18408e-15, 52, -344]) rotate([0, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/nut_m5.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-52, 6.36816e-15, -358]) rotate([0, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m5x20.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-52, 6.36816e-15, -358]) rotate([0, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-52, 6.36816e-15, -345]) rotate([0, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-52, 6.36816e-15, -344]) rotate([0, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/nut_m5.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-9.55225e-15, -52, -358]) rotate([0, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m5x20.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-9.55225e-15, -52, -358]) rotate([0, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-9.55225e-15, -52, -345]) rotate([0, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([-9.55225e-15, -52, -344]) rotate([0, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/nut_m5.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([0, 1.22465e-16, -299]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m8x50.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([0, 1.22465e-16, -299]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m8x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([0, -4.40873e-15, -336]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m8x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -60]) translate([0, -4.53119e-15, -337]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/nut_m8.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([-20, 50, 391]) rotate([0, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m5x16.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([-20, 50, 391]) rotate([0, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([-20, 90, 391]) rotate([0, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m5x16.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([-20, 90, 391]) rotate([0, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([20, 50, 391]) rotate([0, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m5x16.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([20, 50, 391]) rotate([0, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([20, 90, 391]) rotate([0, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m5x16.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([20, 90, 391]) rotate([0, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([-11, 174, 339]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m5x25.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([-11, 174, 339]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([-11, 174, 322]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([-11, 174, 321]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/nut_m5.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([-11, 206, 339]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m5x25.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([-11, 206, 339]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([-11, 206, 322]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([-11, 206, 321]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/nut_m5.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([11, 174, 339]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m5x25.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([11, 174, 339]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([11, 174, 322]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([11, 174, 321]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/nut_m5.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([11, 206, 339]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m5x25.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([11, 206, 339]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([11, 206, 322]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([11, 206, 321]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/nut_m5.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([119, 50, 415]) rotate([0, -90, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m5x20.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([119, 50, 415]) rotate([0, -90, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([119, 50, 455]) rotate([0, -90, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m5x20.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([119, 50, 455]) rotate([0, -90, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([119, 90, 415]) rotate([0, -90, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m5x20.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([119, 90, 415]) rotate([0, -90, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([119, 90, 455]) rotate([0, -90, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m5x20.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([119, 90, 455]) rotate([0, -90, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([65, 36, 600]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m4x25.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([65, 36, 600]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m4x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([65, 36, 585]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m4x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([65, 36, 584]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/nut_m4.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([65, 104, 600]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m4x25.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([65, 104, 600]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m4x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([65, 104, 585]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m4x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([65, 104, 584]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/nut_m4.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([-96, -106, 467]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m4x16.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([-96, -106, 467]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m4x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([-96, 106, 467]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m4x16.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([-96, 106, 467]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m4x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([96, -106, 467]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m4x16.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([96, -106, 467]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m4x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([96, 106, 467]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m4x16.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([96, 106, 467]) rotate([180, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m4x1.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([7.65, 190, 354]) rotate([0, -90, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m5x20.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([-10.65, 190, 354]) rotate([0, 90, 0])  import("../../assemblies/parent_spar_bolted/hardware/nut_m5.stl");
if (show_exterior) color("DarkOrange") translate([0, 0, -68])  import("../../parts/parent/exterior/printed/parent_rope_keel_adapter/parent_rope_keel_adapter.stl");
if (show_hardware) color("Silver") translate([-20, -20, -69]) rotate([0, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m5x16.stl");
if (show_hardware) color("Silver") translate([-20, -20, -69]) rotate([0, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([-20, 20, -69]) rotate([0, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m5x16.stl");
if (show_hardware) color("Silver") translate([-20, 20, -69]) rotate([0, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([20, -20, -69]) rotate([0, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m5x16.stl");
if (show_hardware) color("Silver") translate([20, -20, -69]) rotate([0, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([20, 20, -69]) rotate([0, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m5x16.stl");
if (show_hardware) color("Silver") translate([20, 20, -69]) rotate([0, 0, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
if (show_hardware) color("Silver") translate([-25, 0, -88]) rotate([0, 90, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m6x60.stl");
if (show_hardware) color("Silver") translate([-25, 0, -88]) rotate([0, 90, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m6x1.stl");
if (show_hardware) color("Silver") translate([24, 0, -88]) rotate([0, 90, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m6x1.stl");
if (show_hardware) color("Silver") translate([25, 0, -88]) rotate([0, 90, 0])  import("../../assemblies/parent_spar_bolted/hardware/nut_m6.stl");
// Existing fender envelope, diameter100 x length300 provisional; free to move on rope.
if (show_floats) color("LightSkyBlue") translate([-178, 0, 0])  import("../../parts/parent/exterior/cots/parent_fender/parent_fender.stl");
// Existing fender envelope, diameter100 x length300 provisional; free to move on rope.
if (show_floats) color("LightSkyBlue") translate([178, 0, 0])  import("../../parts/parent/exterior/cots/parent_fender/parent_fender.stl");
if (show_ropes) color("BurlyWood")  import("../../assemblies/parent_rope_float/rope_routes.stl");
// parent_interior_p1 と同一配置 (箱 (13.5,13.5,13.8))
if (show_interior) color("Orange", 0.9) translate([0, 0, -460]) translate([0, 0, 460]) translate([-91.5, -101.5, 13.8])  import("../../parts/parent/interior/printed/parent_plate/parent_plate_p1.stl");
// p1 と同一 (箱 (20,23.5,51.4))
if (show_interior) color("DarkOrange", 0.9) translate([0, 0, -460]) translate([0, 0, 460]) translate([-85, -91.5, 51.4])  import("../../parts/parent/interior/printed/parent_lipo_tray/parent_lipo_tray.stl");
// タカチ BCAS212310G。箱原点 (外形左下・箱底外面) をデッキ座標 (-105,-115,0) へ。外部取付穴 (箱 (9,9)(201,9)(9,221)(201,221)) = デッキ (±96, ±106)
if (show_vessel) color("LightSteelBlue", 0.22) translate([0, 0, -460]) translate([0, 0, 460]) translate([-105, -115, 0])  import("../../parts/parent/exterior/cots/bcas212310g/bcas212310g.stl");
