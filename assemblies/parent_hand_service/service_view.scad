// =====================================================================
// parent_hand_service_view.scad
// !! 自動生成ファイル - 編集しないこと。placement.json を直して
//    build.ps1 -Assemblies で再生成する。
// Interior moved aside after vertical extraction with both M10 penetrators retained.
// 座標系: Box nominal lid-envelope southwest lower datum; mm. North body wallY228.3, lid rimY230. Floor top18.8; TX origin147/135.5/24.8.
// =====================================================================

show_vessel = true;
show_interior = true;

if (show_interior) color("SteelBlue", 1) translate([240, 0, 0]) translate([0, 0, 3]) translate([18, 112, 42]) rotate([0, 0, 0])  import("../../parts/parent/interior/pcb/parent_main/parent_main.stl");
if (show_interior) color("MediumSeaGreen", 1) translate([240, 0, 0]) translate([0, -11, 5.5]) translate([25.8, 115, 28.3]) rotate([0, 0, 90])  import("../../parts/parent/interior/pcb/parent_pwr/parent_pwr.stl");
if (show_interior) color("Gold", 1) translate([240, 0, 0]) translate([147, 135.5, 24.8]) rotate([0, 0, 90])  import("../../parts/parent/interior/pcb/tx_improved/tx_improved.stl");
if (show_interior) color("SandyBrown", 1) translate([240, 0, 0]) translate([0, 0, 8.3]) translate([0, 0, 1.6]) translate([202.34, 208, 65.6]) rotate([0, 0, 180])  import("../../parts/parent/interior/cots/spresense_service_stack/spresense_service_stack.stl");
if (show_interior) color("IndianRed", 1) translate([240, 0, 0]) translate([153, 124.6, 23]) rotate([0, 0, 270])  import("../../parts/common/interior/cots/lipo_3s_2200_zeee/lipo_3s_2200_zeee_pack.stl");
// Pair confirmed at X150/175, center height30..35;32.5 nominal. Cable identity at each hole not specified. Existing SCAD body reference and separate vendor16mm nut; wet-end cable size unconfirmed.
if (show_vessel) color("Silver", 1) translate([150, 228.3, 32.5]) rotate([90, 0, 0])  import("../../parts/common/exterior/cots/wetlink_penetrator_m10/wetlink_m10_bcas_reference.stl");
// Pair confirmed at X150/175, center height30..35;32.5 nominal. Cable identity at each hole not specified. Existing SCAD body reference and separate vendor16mm nut; wet-end cable size unconfirmed.
if (show_vessel) color("Silver", 1) translate([175, 228.3, 32.5]) rotate([90, 0, 0])  import("../../parts/common/exterior/cots/wetlink_penetrator_m10/wetlink_m10_bcas_reference.stl");
// 2026-10-29 vertical-removal lid revision; reprint base and lid together.
if (show_interior) color("Orange") translate([240, 0, 0]) translate([197.5, 22.1, 49]) rotate([0, 0, 90])  import("../../parts/parent/interior/printed/parent_lipo_retainer/parent_lipo_retainer_lid_slide.stl");
if (show_interior) color("LightPink") translate([240, 0, 0]) translate([197.5, 22.1, 20]) rotate([0, 0, 90])  import("../../parts/parent/interior/printed/parent_hand_service/battery_pads_open_end.stl");
// M3x12, 9mm engagement in2.8mm plastic pilot; no nut.
if (show_interior) color("Silver") translate([240, 0, 0]) translate([192.5, 72.1, 52])  import("../../parts/common/interior/cots/screw/screw_m3x12.stl");
if (show_interior) color("Silver") translate([240, 0, 0]) translate([197.5, 22.1, 23])  import("../../parts/common/interior/cots/screw/screw_m3x8.stl");
if (show_interior) color("Silver") translate([240, 0, 0]) translate([197.5, 125.1, 23])  import("../../parts/common/interior/cots/screw/screw_m3x8.stl");
if (show_interior) color("Silver") translate([240, 0, 0]) translate([142, 22.1, 23])  import("../../parts/common/interior/cots/screw/screw_m3x8.stl");
if (show_interior) color("Silver") translate([240, 0, 0]) translate([142, 125.1, 23])  import("../../parts/common/interior/cots/screw/screw_m3x8.stl");
// Conservative head10/H5, length12 inherited assumption; actual screw height and length unmeasured.
if (show_interior) color("Silver") translate([240, 0, 0]) translate([25, 25, 16.8])  import("../../parts/common/interior/cots/screw/screw_m4x12_head10_h5_envelope.stl");
// Conservative head10/H5, length12 inherited assumption; actual screw height and length unmeasured.
if (show_interior) color("Silver") translate([240, 0, 0]) translate([185, 25, 16.8])  import("../../parts/common/interior/cots/screw/screw_m4x12_head10_h5_envelope.stl");
// Conservative head10/H5, length12 inherited assumption; actual screw height and length unmeasured.
if (show_interior) color("Silver") translate([240, 0, 0]) translate([25, 205, 16.8])  import("../../parts/common/interior/cots/screw/screw_m4x12_head10_h5_envelope.stl");
if (show_interior) color("Silver") translate([240, 0, 0]) translate([0, 0, 8.3]) translate([0, 0, 1.6]) translate([199.8, 153.39, 67.2])  import("../../parts/common/interior/cots/screw/screw_m2_5x6.stl");
if (show_interior) color("Silver") translate([240, 0, 0]) translate([0, 0, 8.3]) translate([0, 0, 1.6]) translate([151.54, 154.66, 67.2])  import("../../parts/common/interior/cots/screw/screw_m2_5x6.stl");
if (show_interior) color("Silver") translate([240, 0, 0]) translate([0, 0, 8.3]) translate([0, 0, 1.6]) translate([194.72, 205.46, 67.2])  import("../../parts/common/interior/cots/screw/screw_m2_5x6.stl");
if (show_interior) color("Silver") translate([240, 0, 0]) translate([0, 0, 8.3]) translate([0, 0, 1.6]) translate([166.78, 205.46, 67.2])  import("../../parts/common/interior/cots/screw/screw_m2_5x6.stl");
if (show_interior) color("Silver") translate([240, 0, 0]) translate([193, 201.5, 26.4])  import("../../parts/common/interior/cots/screw/screw_m3x8.stl");
if (show_interior) color("Silver") translate([240, 0, 0]) translate([193, 135.5, 26.4])  import("../../parts/common/interior/cots/screw/screw_m3x8.stl");
if (show_interior) color("Silver") translate([240, 0, 0]) translate([151, 201.5, 26.4])  import("../../parts/common/interior/cots/screw/screw_m3x8.stl");
if (show_interior) color("Silver") translate([240, 0, 0]) translate([151, 135.5, 26.4])  import("../../parts/common/interior/cots/screw/screw_m3x8.stl");
if (show_interior) color("Green") translate([240, 0, 0]) translate([0, 0, 18.8]) translate([113.5, 205, 64.6]) rotate([0, 0, 180])  import("../../parts/parent/interior/cots/sparkfun_neo_f9p/sparkfun_neo_f9p.stl");
if (show_interior) color("Green") translate([240, 0, 0]) translate([0, 0, 18.8]) translate([113.5, 205, 64.6]) rotate([0, 0, 180])  import("../../parts/parent/interior/cots/sparkfun_neo_f9p/sma_plug_envelope.stl");
if (show_interior) color("Green") translate([240, 0, 0]) translate([0, 0, 18.8]) translate([113.5, 205, 64.6]) rotate([0, 0, 180])  import("../../parts/parent/interior/cots/sparkfun_neo_f9p/gnss_pin_headers.stl");
if (show_interior) color("Olive") translate([240, 0, 0]) translate([0, 0, 18.8]) translate([69, 139, 56])  import("../../parts/parent/interior/cots/sparkfun_neo_f9p/universal_pcb_60x80.stl");
// Existing geometry, no reprint needed if already made. Included so the portable set contains the complete interior.
if (show_interior) color("Orange") translate([240, 0, 0]) translate([0, 0, 18.8])  import("../../parts/parent/interior/printed/gnss_universal_carrier/gnss_universal_carrier.stl");
// Reprint with open-top lead entry; original footprint, case-tool paths and floor holes retained.
if (show_interior) color("Orange") translate([240, 0, 0]) translate([60, 60, 18.8])  import("../../parts/parent/interior/printed/ann_mb1_internal_rack/ann_mb1_coax_ring_service.stl");
if (show_interior) color("Silver") translate([240, 0, 0]) translate([0, -12, 8.8]) translate([60, 60, 63.6])  import("../../parts/parent/interior/cots/ann_mb1/ground_plate_internal.stl");
if (show_interior) color("DimGray") translate([240, 0, 0]) translate([0, -12, 8.8]) translate([60, 60, 64.6]) rotate([0, 0, 90])  import("../../parts/parent/interior/cots/ann_mb1/ann_mb1.stl");
if (show_interior) color("MediumSeaGreen") translate([240, 0, 0]) translate([0, 0, 18.8]) translate([62.78, 195, 56]) rotate([0, 0, 90])  import("../../parts/parent/interior/cots/adafruit_lis3mdl/adafruit_lis3mdl.stl");
if (show_interior) color("Ivory") translate([240, 0, 0]) translate([0, 0, 18.8]) translate([47.54, 197.54, 57.57])  import("../../parts/parent/interior/cots/adafruit_lis3mdl/nylon_screw_m2x10_envelope.stl");
if (show_interior) color("Ivory") translate([240, 0, 0]) translate([47.54, 197.54, 66.7])  import("../../parts/parent/interior/cots/adafruit_lis3mdl/nylon_nut_m2_envelope.stl");
if (show_interior) color("Ivory") translate([240, 0, 0]) translate([0, 0, 18.8]) translate([47.54, 217.86, 57.57])  import("../../parts/parent/interior/cots/adafruit_lis3mdl/nylon_screw_m2x10_envelope.stl");
if (show_interior) color("Ivory") translate([240, 0, 0]) translate([47.54, 217.86, 66.7])  import("../../parts/parent/interior/cots/adafruit_lis3mdl/nylon_nut_m2_envelope.stl");
if (show_interior) color("Ivory") translate([240, 0, 0]) translate([0, 0, 18.8]) translate([60.24, 197.54, 57.57])  import("../../parts/parent/interior/cots/adafruit_lis3mdl/nylon_screw_m2x10_envelope.stl");
if (show_interior) color("Ivory") translate([240, 0, 0]) translate([60.24, 197.54, 66.7])  import("../../parts/parent/interior/cots/adafruit_lis3mdl/nylon_nut_m2_envelope.stl");
if (show_interior) color("Ivory") translate([240, 0, 0]) translate([0, 0, 18.8]) translate([60.24, 217.86, 57.57])  import("../../parts/parent/interior/cots/adafruit_lis3mdl/nylon_screw_m2x10_envelope.stl");
if (show_interior) color("Ivory") translate([240, 0, 0]) translate([60.24, 217.86, 66.7])  import("../../parts/parent/interior/cots/adafruit_lis3mdl/nylon_nut_m2_envelope.stl");
if (show_interior) color("Silver") translate([240, 0, 0]) translate([0, 0, 18.8]) translate([71.5, 141.5, 57.6])  import("../../parts/common/interior/cots/screw/screw_m3x12.stl");
if (show_interior) color("Silver") translate([240, 0, 0]) translate([0, 0, 18.8]) translate([71.5, 141.5, 47.6])  import("../../parts/common/interior/cots/screw/screw_nut_m3.stl");
if (show_interior) color("Silver") translate([240, 0, 0]) translate([0, 0, 18.8]) translate([126.5, 141.5, 57.6])  import("../../parts/common/interior/cots/screw/screw_m3x12.stl");
if (show_interior) color("Silver") translate([240, 0, 0]) translate([0, 0, 18.8]) translate([126.5, 141.5, 47.6])  import("../../parts/common/interior/cots/screw/screw_nut_m3.stl");
if (show_interior) color("Silver") translate([240, 0, 0]) translate([0, 0, 18.8]) translate([71.5, 216.5, 57.6])  import("../../parts/common/interior/cots/screw/screw_m3x12.stl");
if (show_interior) color("Silver") translate([240, 0, 0]) translate([0, 0, 18.8]) translate([71.5, 216.5, 47.6])  import("../../parts/common/interior/cots/screw/screw_nut_m3.stl");
if (show_interior) color("Silver") translate([240, 0, 0]) translate([0, 0, 18.8]) translate([126.5, 216.5, 57.6])  import("../../parts/common/interior/cots/screw/screw_m3x12.stl");
if (show_interior) color("Silver") translate([240, 0, 0]) translate([0, 0, 18.8]) translate([126.5, 216.5, 47.6])  import("../../parts/common/interior/cots/screw/screw_nut_m3.stl");
if (show_interior) color("DarkOrange") translate([240, 0, 0])  import("../../parts/parent/interior/printed/parent_hand_service/main_service_frame.stl");
if (show_interior) color("DarkOrange") translate([240, 0, 0])  import("../../parts/parent/interior/printed/ann_mb1_internal_rack/antenna_service_shelf.stl");
if (show_interior) color("DarkOrange") translate([240, 0, 0])  import("../../parts/parent/interior/printed/ann_mb1_internal_rack/cradle_floor_foot_0.stl");
if (show_interior) color("DarkOrange") translate([240, 0, 0])  import("../../parts/parent/interior/printed/ann_mb1_internal_rack/cradle_floor_foot_1.stl");
if (show_interior) color("DarkOrange") translate([240, 0, 0])  import("../../parts/parent/interior/printed/ann_mb1_internal_rack/cradle_floor_foot_2.stl");
if (show_interior) color("DarkOrange") translate([240, 0, 0])  import("../../parts/parent/interior/printed/ann_mb1_internal_rack/cradle_floor_foot_3.stl");
if (show_interior) color("DarkOrange") translate([240, 0, 0])  import("../../parts/parent/interior/printed/parent_hand_service/power_adapter.stl");
if (show_interior) color("DarkOrange") translate([240, 0, 0]) translate([0, 0, 8.3])  import("../../parts/parent/interior/printed/parent_hand_service/sony_mount_plate.stl");
if (show_interior) color("DimGray") translate([240, 0, 0])  import("../../parts/parent/interior/cots/ann_mb1/coax_service_loop.stl");
if (show_interior) color("DimGray") translate([240, 0, 0])  import("../../parts/parent/interior/cots/ann_mb1/coax_receiver_service.stl");
if (show_interior) color("Orange") translate([240, 0, 0]) translate([0, 0, 0])  import("../../parts/parent/interior/printed/parent_hand_service/sony_support_frame.stl");
if (show_interior) color("Orange") translate([240, 0, 0]) translate([0, 0, 0])  import("../../parts/parent/interior/printed/gnss_universal_carrier/gnss_support_frame.stl");
if (show_interior) translate([240, 0, 0]) translate([47.54, 197.54, 68.3])  import("../../parts/parent/interior/cots/adafruit_lis3mdl/nylon_washer_m2_05_envelope.stl");
if (show_interior) translate([240, 0, 0]) translate([47.54, 217.86, 68.3])  import("../../parts/parent/interior/cots/adafruit_lis3mdl/nylon_washer_m2_05_envelope.stl");
if (show_interior) translate([240, 0, 0]) translate([60.24, 197.54, 68.3])  import("../../parts/parent/interior/cots/adafruit_lis3mdl/nylon_washer_m2_05_envelope.stl");
if (show_interior) translate([240, 0, 0]) translate([60.24, 217.86, 68.3])  import("../../parts/parent/interior/cots/adafruit_lis3mdl/nylon_washer_m2_05_envelope.stl");
if (show_interior) translate([240, 0, 0]) translate([12, 25, 35.6])  import("../../parts/common/interior/cots/screw/screw_m3x30.stl");
if (show_interior) translate([240, 0, 0]) translate([12, 25, 9.04]) rotate([0, 0, 30])  import("../../parts/common/interior/cots/screw/screw_nut_m3.stl");
if (show_interior) translate([240, 0, 0]) translate([134, 25, 35.6])  import("../../parts/common/interior/cots/screw/screw_m3x30.stl");
if (show_interior) translate([240, 0, 0]) translate([134, 25, 9.04]) rotate([0, 0, 30])  import("../../parts/common/interior/cots/screw/screw_nut_m3.stl");
if (show_interior) translate([240, 0, 0]) translate([12, 95, 35.6])  import("../../parts/common/interior/cots/screw/screw_m3x30.stl");
if (show_interior) translate([240, 0, 0]) translate([12, 95, 9.04]) rotate([0, 0, 30])  import("../../parts/common/interior/cots/screw/screw_nut_m3.stl");
if (show_interior) translate([240, 0, 0]) translate([134, 95, 35.6])  import("../../parts/common/interior/cots/screw/screw_m3x30.stl");
if (show_interior) translate([240, 0, 0]) translate([134, 95, 9.04]) rotate([0, 0, 30])  import("../../parts/common/interior/cots/screw/screw_nut_m3.stl");
if (show_interior) translate([240, 0, 0]) translate([13, 145, 71.3])  import("../../parts/common/interior/cots/screw/screw_m3x65.stl");
if (show_interior) translate([240, 0, 0]) translate([13, 145, 9.04]) rotate([0, 0, 30])  import("../../parts/common/interior/cots/screw/screw_nut_m3.stl");
if (show_interior) translate([240, 0, 0]) translate([135, 145, 71.3])  import("../../parts/common/interior/cots/screw/screw_m3x65.stl");
if (show_interior) translate([240, 0, 0]) translate([135, 145, 9.04]) rotate([0, 0, 30])  import("../../parts/common/interior/cots/screw/screw_nut_m3.stl");
if (show_interior) translate([240, 0, 0]) translate([22.6, 219, 71.3])  import("../../parts/common/interior/cots/screw/screw_m3x65.stl");
if (show_interior) translate([240, 0, 0]) translate([22.6, 219, 9.04]) rotate([0, 0, 30])  import("../../parts/common/interior/cots/screw/screw_nut_m3.stl");
if (show_interior) translate([240, 0, 0]) translate([135, 219, 71.3])  import("../../parts/common/interior/cots/screw/screw_m3x65.stl");
if (show_interior) translate([240, 0, 0]) translate([135, 219, 9.04]) rotate([0, 0, 30])  import("../../parts/common/interior/cots/screw/screw_nut_m3.stl");
if (show_interior) translate([240, 0, 0]) translate([142.5, 134.5, 72])  import("../../parts/common/interior/cots/screw/screw_m3x65.stl");
if (show_interior) translate([240, 0, 0]) translate([142.5, 134.5, 9.04]) rotate([0, 0, 30])  import("../../parts/common/interior/cots/screw/screw_nut_m3.stl");
if (show_interior) translate([240, 0, 0]) translate([201, 134.5, 72])  import("../../parts/common/interior/cots/screw/screw_m3x65.stl");
if (show_interior) translate([240, 0, 0]) translate([201, 134.5, 9.04]) rotate([0, 0, 30])  import("../../parts/common/interior/cots/screw/screw_nut_m3.stl");
if (show_interior) translate([240, 0, 0]) translate([142.5, 202.5, 72])  import("../../parts/common/interior/cots/screw/screw_m3x10.stl");
if (show_interior) translate([240, 0, 0]) translate([201, 204.5, 72])  import("../../parts/common/interior/cots/screw/screw_m3x65.stl");
if (show_interior) translate([240, 0, 0]) translate([201, 204.5, 9.04]) rotate([0, 0, 30])  import("../../parts/common/interior/cots/screw/screw_nut_m3.stl");
if (show_interior) translate([240, 0, 0]) translate([22.5, 107.5, 46.6])  import("../../parts/common/interior/cots/screw/screw_m3x8.stl");
if (show_interior) translate([240, 0, 0]) translate([22.5, 32, 46.6])  import("../../parts/common/interior/cots/screw/screw_m3x8.stl");
if (show_interior) translate([240, 0, 0]) translate([125.5, 32, 46.6])  import("../../parts/common/interior/cots/screw/screw_m3x8.stl");
if (show_interior) translate([240, 0, 0]) translate([125.5, 107.5, 46.6])  import("../../parts/common/interior/cots/screw/screw_m3x8.stl");
if (show_interior) translate([240, 0, 0]) translate([30.8, 120, 30.25])  import("../../parts/common/interior/cots/screw/screw_m3x8.stl");
if (show_interior) translate([240, 0, 0]) translate([104.8, 199, 35.4])  import("../../parts/common/interior/cots/screw/screw_m3x6.stl");
if (show_interior) translate([240, 0, 0]) translate([104.8, 210, 30.25])  import("../../parts/common/interior/cots/screw/screw_m3x8.stl");
if (show_interior) translate([240, 0, 0]) translate([30.8, 109, 35.4])  import("../../parts/common/interior/cots/screw/screw_m3x6.stl");
if (show_interior) translate([240, 0, 0]) translate([30.8, 210, 30.25])  import("../../parts/common/interior/cots/screw/screw_m3x8.stl");
if (show_interior) translate([240, 0, 0]) translate([104.8, 109, 35.4])  import("../../parts/common/interior/cots/screw/screw_m3x6.stl");
if (show_interior) translate([240, 0, 0]) translate([104.8, 120, 30.25])  import("../../parts/common/interior/cots/screw/screw_m3x8.stl");
if (show_interior) translate([240, 0, 0]) translate([30.8, 199, 35.4])  import("../../parts/common/interior/cots/screw/screw_m3x6.stl");
if (show_interior) translate([240, 0, 0]) translate([12, 35, 72.4])  import("../../parts/common/interior/cots/screw/screw_m3x30.stl");
if (show_interior) translate([240, 0, 0]) translate([12, 75, 72.4])  import("../../parts/common/interior/cots/screw/screw_m3x30.stl");
if (show_interior) translate([240, 0, 0]) translate([137.5, 35, 72.4])  import("../../parts/common/interior/cots/screw/screw_m3x30.stl");
if (show_interior) translate([240, 0, 0]) translate([137.5, 75, 72.4])  import("../../parts/common/interior/cots/screw/screw_m3x30.stl");
if (show_interior) translate([240, 0, 0]) translate([20, 26.5, 73.4])  import("../../parts/common/interior/cots/screw/screw_m3x10.stl");
if (show_interior) translate([240, 0, 0]) translate([20, 26.5, 64.5]) rotate([0, 0, 30])  import("../../parts/common/interior/cots/screw/screw_nut_m3.stl");
if (show_interior) translate([240, 0, 0]) translate([20, 26.5, 66.9])  import("../../parts/common/interior/cots/screw/screw_washer_m3_05.stl");
if (show_interior) translate([240, 0, 0]) translate([100, 23, 73.4])  import("../../parts/common/interior/cots/screw/screw_m3x10.stl");
if (show_interior) translate([240, 0, 0]) translate([100, 23, 64.5]) rotate([0, 0, 30])  import("../../parts/common/interior/cots/screw/screw_nut_m3.stl");
if (show_interior) translate([240, 0, 0]) translate([100, 23, 66.9])  import("../../parts/common/interior/cots/screw/screw_washer_m3_05.stl");
if (show_interior) translate([240, 0, 0]) translate([20, 73, 73.4])  import("../../parts/common/interior/cots/screw/screw_m3x10.stl");
if (show_interior) translate([240, 0, 0]) translate([20, 73, 64.5]) rotate([0, 0, 30])  import("../../parts/common/interior/cots/screw/screw_nut_m3.stl");
if (show_interior) translate([240, 0, 0]) translate([20, 73, 66.9])  import("../../parts/common/interior/cots/screw/screw_washer_m3_05.stl");
if (show_interior) translate([240, 0, 0]) translate([100, 63, 73.4])  import("../../parts/common/interior/cots/screw/screw_m3x10.stl");
if (show_interior) translate([240, 0, 0]) translate([100, 63, 64.5]) rotate([0, 0, 30])  import("../../parts/common/interior/cots/screw/screw_nut_m3.stl");
if (show_interior) translate([240, 0, 0]) translate([100, 63, 66.9])  import("../../parts/common/interior/cots/screw/screw_washer_m3_05.stl");
if (show_interior) translate([240, 0, 0]) translate([26, 48, 79.4])  import("../../parts/common/interior/cots/screw/screw_m4x18_socket.stl");
if (show_interior) translate([240, 0, 0]) translate([26, 48, 63.4]) rotate([0, 0, 30])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_interior) translate([240, 0, 0]) translate([26, 48, 66.6])  import("../../parts/common/interior/cots/screw/screw_washer_m4_08.stl");
if (show_interior) translate([240, 0, 0]) translate([94, 48, 79.4])  import("../../parts/common/interior/cots/screw/screw_m4x18_socket.stl");
if (show_interior) translate([240, 0, 0]) translate([94, 48, 63.4]) rotate([0, 0, 30])  import("../../parts/common/interior/cots/screw/screw_nut_m4.stl");
if (show_interior) translate([240, 0, 0]) translate([94, 48, 66.6])  import("../../parts/common/interior/cots/screw/screw_washer_m4_08.stl");
// Plain through holes and external underside heads; no embedded nuts. North M10 relief and10.8mm M4 clearance retained.
if (show_interior) color("Orange", 0.9) translate([240, 0, 0])  import("../../parts/parent/interior/printed/parent_hand_service/floor_plate.stl");
// 2026-10-29 vertical-removal lid revision; reprint base and lid together.
if (show_interior) color("DarkOrange", 0.9) translate([240, 0, 0]) translate([197.5, 22.1, 20]) rotate([0, 0, 90])  import("../../parts/parent/interior/printed/parent_hand_service/battery_base.stl");
if (show_interior) color("Yellow", 0.3) translate([240, 0, 0]) translate([0, 0, 18.8]) translate([60.7, 168, 57.6])  import("../../parts/parent/interior/cots/sparkfun_neo_f9p/xh_plug_keepout.stl");
// 2026-10-10 drawing-derived body: floor3, boss top10, 4 inserts/12 tapping bosses, drafted walls and corner bays; vendor STEP and physical fit pending.
if (show_vessel) color("LightSteelBlue", 0.22) translate([0, 0, 0])  import("../../parts/parent/exterior/cots/bcas212310g/bcas212310g.stl");
if (show_interior) color("Purple", 0.2) translate([240, 0, 0]) translate([60, 60, 18.8])  import("../../parts/parent/interior/cots/ann_mb1/coax_coil_keepout.stl");
if (show_interior) color("Cyan", 0.15) translate([240, 0, 0]) translate([-1, -5, 0])  import("../../parts/parent/interior/printed/parent_hand_service/tx_top_keepout.stl");
