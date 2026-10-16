// =====================================================================
// parent_integrated_closeup_view.scad
// !! 自動生成ファイル - 編集しないこと。placement.json を直して
//    build.ps1 -Assemblies で再生成する。
// P1 + latest bottom-sensor exterior; prototype pending measurements. SPRESENSE placeholder contact unresolved.
// 座標系: Box bottom Z=0; camera optical axis and TD04A acoustic axis -Z. TD04A d26 x55 is provisional.
// =====================================================================

show_cabling = true;
show_envelope = false;
show_exterior = true;
show_floats = true;
show_hardware = true;
show_interior = true;
show_reference = true;
show_ropes = true;
show_vessel = true;

if (show_exterior) color("DarkOrange") translate([0, 0, -460]) translate([108, 70, 410])  import("../../parts/parent/exterior/printed/parent_spar_gps_bridge/parent_spar_gps_bridge.stl");
if (show_exterior) color("DarkOrange") translate([0, 0, -460]) translate([0, 0, 460])  import("../../parts/parent/exterior/printed/parent_deck/parent_deck.stl");
if (show_reference) color("Black") translate([0, 0, -460]) translate([65, 70, 593])  import("../../assemblies/parent_spar_bolted/reference/gps_ann_mb1.stl");
if (show_envelope) color("LightSteelBlue") translate([0, 0, -460]) translate([-105, -115, 556.3])  import("../../assemblies/parent_spar_bolted/reference/box_lid_envelope.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([119, 50, 455]) rotate([0, -90, 0])  import("../../assemblies/parent_spar_bolted/hardware/screw_m5x20.stl");
if (show_hardware) color("Silver") translate([0, 0, -460]) translate([119, 50, 455]) rotate([0, -90, 0])  import("../../assemblies/parent_spar_bolted/hardware/washer_m5x1.stl");
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
// モデルは Y=-88..0。プレート (2,2)-(114,90)、ボタン/LED/DS3231 縁が北 (+Y)。基板下面 z=24.8 (プレート上面18.8+ボス6)。取付ねじの代わりに M3 MF25 スペーサ ×4 (LiPo トレイ支持)
if (show_interior) color("SteelBlue", 1) translate([-105, -115, 0]) translate([15.5, 103.5, 24.8])  import("../../parts/parent/interior/pcb/parent_main/parent_main.stl");
// モデルは Y=-84..0。プレート (2,95)-(102,179)
if (show_interior) color("MediumSeaGreen", 1) translate([0, 0, 3.5]) translate([-105, -115, 0]) translate([15.5, 192.5, 24.8])  import("../../parts/parent/interior/pcb/parent_pwr/parent_pwr.stl");
// 90度回転でプレート (121,77)-(171,151)。プレート直付け (p1)
if (show_interior) color("Gold", 1) translate([-105, -115, 0]) translate([134.5, 94.5, 24.8]) rotate([0, 0, 90])  import("../../parts/parent/interior/pcb/tx_improved/tx_improved.stl");
// 簡易モデル (穴・スタック高は仮)。90度回転でプレート (121,2)-(174.5,70.6)
if (show_interior) color("SandyBrown", 1) translate([-105, -115, 0]) translate([188, 15.5, 24.8]) rotate([0, 0, 90])  import("../../parts/parent/interior/cots/spresense_logger/spresense_logger.stl");
// parent_lipo_tray 内 (セル下面 z=54.4、上面 77.4、蓋パッキン面 90.9)。180°回転でリードを -X (西) へ → P-PWR J_BAT
if (show_interior) color("IndianRed", 1) translate([-105, -115, 0]) translate([122.5, 68, 54.4]) rotate([0, 0, 180])  import("../../parts/common/interior/cots/lipo_3s_2200_zeee/lipo_3s_2200_zeee_pack.stl");
// M3 MF 25。MAIN 取付穴を通してプレートのボス下穴へ (MAIN 固定ねじ兼用)。胴下端 = MAIN 基板上面 z=26.4
if (show_interior) color("Goldenrod", 1) translate([-105, -115, 0]) translate([20, 23.5, 26.4])  import("../../parts/common/interior/cots/hex_spacer/hex_spacer_m3_mf25.stl");
// M3 MF 25。MAIN 取付穴を通してプレートのボス下穴へ (MAIN 固定ねじ兼用)。胴下端 = MAIN 基板上面 z=26.4
if (show_interior) color("Goldenrod", 1) translate([-105, -115, 0]) translate([123, 23.5, 26.4])  import("../../parts/common/interior/cots/hex_spacer/hex_spacer_m3_mf25.stl");
// M3 MF 25。MAIN 取付穴を通してプレートのボス下穴へ (MAIN 固定ねじ兼用)。胴下端 = MAIN 基板上面 z=26.4
if (show_interior) color("Goldenrod", 1) translate([-105, -115, 0]) translate([20, 99, 26.4])  import("../../parts/common/interior/cots/hex_spacer/hex_spacer_m3_mf25.stl");
// M3 MF 25。MAIN 取付穴を通してプレートのボス下穴へ (MAIN 固定ねじ兼用)。胴下端 = MAIN 基板上面 z=26.4
if (show_interior) color("Goldenrod", 1) translate([-105, -115, 0]) translate([123, 99, 26.4])  import("../../parts/common/interior/cots/hex_spacer/hex_spacer_m3_mf25.stl");
// WetLink Penetrator M10 (参考モデル・仮寸)。南壁 (Y=0) x=120, 軸 z=65。C1 テザー → P-MAIN J_TETH1 (箱 x≈123 の直下)。頭+プラグは箱外 y=-22..0、ねじ+ナットが箱内 y=0..14.5 (モデル壁 6.1 基準。実壁 3.08 なら 11.5)。容器内に出るのは素の導体 (外被は濡れ側で終端)。型番 -045..-085 はテザー外径待ち
if (show_vessel) color("Silver", 1) translate([-105, -115, 0]) translate([120, 0, 65]) rotate([-90, 0, 0])  import("../../parts/common/exterior/cots/wetlink_penetrator_m10/wetlink_penetrator_m10_ref_bcas.stl");
// WetLink Penetrator M10 (参考モデル・仮寸)。南壁 (Y=0) x=85, 軸 z=65。C3 TD04A → TX (右列)。3P プラグは通らないのでケーブルを切って容器内で端子台に落とす前提 (td04a_transducer.md)。テザー側とのピッチ 35 = 16mm トルクレンチの振り代。東へ寄せられないのは SPRESENSE (箱 X 134.5-188) の天面が仮値 30 で、その上を通すと隙間 0.3 になるため (spec/parent_interior_layout.py check_penetrators)
if (show_vessel) color("Silver", 1) translate([-105, -115, 0]) translate([85, 0, 65]) rotate([-90, 0, 0])  import("../../parts/common/exterior/cots/wetlink_penetrator_m10/wetlink_penetrator_m10_ref_bcas.stl");
// 183x203 t5。プレート左下 = 箱 (13.5,13.5)、下面 z=13.8 (床3.8+ボス10 仮)
if (show_interior) color("Orange", 0.9) translate([-105, -115, 0]) translate([13.5, 13.5, 13.8])  import("../../parts/parent/interior/printed/parent_plate_integrated/parent_plate_integrated.stl");
// ブリッジトレイ。原点 = MAIN 南西穴 (箱 20,23.5)、下面 z=51.4 (MAIN 基板上面 26.4 + スペーサ 25)。M3×6 ×4 でスペーサへ
if (show_interior) color("DarkOrange", 0.9) translate([-105, -115, 0]) translate([20, 23.5, 51.4])  import("../../parts/parent/interior/printed/parent_lipo_tray/parent_lipo_tray.stl");
// タカチ BCAS212310G。箱原点 (外形左下・箱底外面) をデッキ座標 (-105,-115,0) へ。外部取付穴 (箱 (9,9)(201,9)(9,221)(201,221)) = デッキ (±96, ±106); E-E mounting bores restored in display model; upper well D9.4 provisional.
if (show_vessel) color("LightSteelBlue", 0.16) translate([0, 0, -460]) translate([0, 0, 460]) translate([-105, -115, 0])  import("../../assemblies/parent_bottom_sensors/reference/bcas_mounting_reference.stl");
