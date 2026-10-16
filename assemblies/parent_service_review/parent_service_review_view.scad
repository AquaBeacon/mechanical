// =====================================================================
// parent_service_review_view.scad
// !! 自動生成ファイル - 編集しないこと。placement.json を直して
//    build.ps1 -Assemblies で再生成する。
// 2026-09-26 revision: lid-open service. Official Sony CAD; IMU envelope pending CAD/stack measurement. LCD support not yet designed.
// 座標系: 箱外形の左下手前が原点。X=210 / Y=230 / Z=上 (箱底外面 z=0, 内床 z=3.8, プレート下面 z=13.8 (ボス 10 仮))。ビューポート方位 (+X) は浮子/マストに対する箱の向き基準。
// =====================================================================

show_vessel = true;
show_interior = true;

// 2026-09-26 service placement; モデルは Y=-88..0。プレート (2,2)-(114,90)、ボタン/LED/DS3231 縁が北 (+Y)。基板下面 z=24.8 (プレート上面18.8+ボス6)。取付ねじの代わりに M3 MF25 スペーサ ×4 (LiPo トレイ支持)
if (show_interior) color("SteelBlue", 1) translate([15.5, 128.5, 24.8])  import("../../parts/parent/interior/pcb/parent_main/parent_main.stl");
// 2026-09-26 service placement; モデルは Y=-84..0。プレート (2,95)-(102,179)
if (show_interior) color("MediumSeaGreen", 1) translate([19.5, 217.5, 28.3])  import("../../parts/parent/interior/pcb/parent_pwr/parent_pwr.stl");
// 2026-09-26 service placement; 90度回転でプレート (121,77)-(171,151)。プレート直付け (p1)
if (show_interior) color("Gold", 1) translate([134.5, 144.5, 24.8]) rotate([0, 0, 90])  import("../../parts/parent/interior/pcb/tx_improved/tx_improved.stl");
// 2026-09-26 service placement; Sony STEP coordinates normalized so EXT PCB underside Z=0. IMU is an explicitly provisional envelope, not vendor CAD.
if (show_interior) color("SandyBrown", 1) translate([134.5, 41, 24.8])  import("../../parts/parent/interior/cots/spresense_service_stack/spresense_service_stack.stl");
// 2026-09-26 service placement; parent_lipo_tray 内 (セル下面 z=54.4、上面 77.4、蓋パッキン面 90.9)。180°回転でリードを -X (西) へ → P-PWR J_BAT
if (show_interior) color("IndianRed", 1) translate([122.5, 93, 54.4]) rotate([0, 0, 180])  import("../../parts/common/interior/cots/lipo_3s_2200_zeee/lipo_3s_2200_zeee_pack.stl");
// 2026-09-26 service placement; M3 MF 25。MAIN 取付穴を通してプレートのボス下穴へ (MAIN 固定ねじ兼用)。胴下端 = MAIN 基板上面 z=26.4
if (show_interior) color("Goldenrod", 1) translate([20, 48.5, 26.4])  import("../../parts/common/interior/cots/hex_spacer/hex_spacer_m3_mf25.stl");
// 2026-09-26 service placement; M3 MF 25。MAIN 取付穴を通してプレートのボス下穴へ (MAIN 固定ねじ兼用)。胴下端 = MAIN 基板上面 z=26.4
if (show_interior) color("Goldenrod", 1) translate([123, 48.5, 26.4])  import("../../parts/common/interior/cots/hex_spacer/hex_spacer_m3_mf25.stl");
// 2026-09-26 service placement; M3 MF 25。MAIN 取付穴を通してプレートのボス下穴へ (MAIN 固定ねじ兼用)。胴下端 = MAIN 基板上面 z=26.4
if (show_interior) color("Goldenrod", 1) translate([20, 124, 26.4])  import("../../parts/common/interior/cots/hex_spacer/hex_spacer_m3_mf25.stl");
// 2026-09-26 service placement; M3 MF 25。MAIN 取付穴を通してプレートのボス下穴へ (MAIN 固定ねじ兼用)。胴下端 = MAIN 基板上面 z=26.4
if (show_interior) color("Goldenrod", 1) translate([123, 124, 26.4])  import("../../parts/common/interior/cots/hex_spacer/hex_spacer_m3_mf25.stl");
// 2026-09-26 service placement; WetLink Penetrator M10 (参考モデル・仮寸)。南壁 (Y=0) x=120, 軸 z=65。C1 テザー → P-MAIN J_TETH1 (箱 x≈123 の直下)。頭+プラグは箱外 y=-22..0、ねじ+ナットが箱内 y=0..14.5 (モデル壁 6.1 基準。実壁 3.08 なら 11.5)。容器内に出るのは素の導体 (外被は濡れ側で終端)。型番 -045..-085 はテザー外径待ち
if (show_vessel) color("Silver", 1) translate([120, 0, 65]) rotate([-90, 0, 0])  import("../../parts/common/exterior/cots/wetlink_penetrator_m10/wetlink_penetrator_m10_ref_bcas.stl");
// 2026-09-26 service placement; WetLink Penetrator M10 (参考モデル・仮寸)。南壁 (Y=0) x=85, 軸 z=65。C3 TD04A → TX (右列)。3P プラグは通らないのでケーブルを切って容器内で端子台に落とす前提 (td04a_transducer.md)。テザー側とのピッチ 35 = 16mm トルクレンチの振り代。東へ寄せられないのは SPRESENSE (箱 X 134.5-188) の天面が仮値 30 で、その上を通すと隙間 0.3 になるため (spec/parent_interior_layout.py check_penetrators)
if (show_vessel) color("Silver", 1) translate([85, 0, 65]) rotate([-90, 0, 0])  import("../../parts/common/exterior/cots/wetlink_penetrator_m10/wetlink_penetrator_m10_ref_bcas.stl");
if (show_interior) color("Orange") translate([20, 48.5, 80.4])  import("../../parts/parent/interior/printed/parent_lipo_retainer/parent_lipo_retainer_lid.stl");
if (show_interior) color("LightPink") translate([20, 48.5, 51.4])  import("../../parts/parent/interior/printed/parent_lipo_retainer/parent_lipo_retainer_pads.stl");
if (show_interior) color("Silver") translate([32, 53.5, 83.4])  import("../../parts/common/interior/cots/screw/screw_m3x12.stl");
if (show_interior) color("Silver") translate([32, 53.5, 73])  import("../../parts/common/interior/cots/screw/screw_nut_m3.stl");
if (show_interior) color("Silver") translate([111, 53.5, 83.4])  import("../../parts/common/interior/cots/screw/screw_m3x12.stl");
if (show_interior) color("Silver") translate([111, 53.5, 73])  import("../../parts/common/interior/cots/screw/screw_nut_m3.stl");
if (show_interior) color("Silver") translate([32, 98.5, 83.4])  import("../../parts/common/interior/cots/screw/screw_m3x12.stl");
if (show_interior) color("Silver") translate([32, 98.5, 73])  import("../../parts/common/interior/cots/screw/screw_nut_m3.stl");
if (show_interior) color("Silver") translate([111, 98.5, 83.4])  import("../../parts/common/interior/cots/screw/screw_m3x12.stl");
if (show_interior) color("Silver") translate([111, 98.5, 73])  import("../../parts/common/interior/cots/screw/screw_nut_m3.stl");
if (show_interior) color("Silver") translate([20, 48.5, 54.4])  import("../../parts/common/interior/cots/screw/screw_m3x8.stl");
if (show_interior) color("Silver") translate([123, 48.5, 54.4])  import("../../parts/common/interior/cots/screw/screw_m3x8.stl");
if (show_interior) color("Silver") translate([20, 124, 54.4])  import("../../parts/common/interior/cots/screw/screw_m3x8.stl");
if (show_interior) color("Silver") translate([123, 124, 54.4])  import("../../parts/common/interior/cots/screw/screw_m3x8.stl");
// 2026-09-26 service placement; 183x203 t5。プレート左下 = 箱 (13.5,13.5)、下面 z=13.8 (床3.8+ボス10 仮)
if (show_interior) color("Orange", 0.9) translate([13.5, 13.5, 13.8])  import("../../parts/parent/interior/printed/parent_plate_service/parent_plate_service.stl");
// 6-face retained battery; rigid lid stops, compliant pads; same 4 MAIN spacers
if (show_interior) color("DarkOrange", 0.9) translate([20, 48.5, 51.4])  import("../../parts/parent/interior/printed/parent_lipo_retainer/parent_lipo_retainer_base.stl");
// タカチ図面 DXF 実座標モデル: 床 3.84 + リブ台 3 (193.2×173.2)、M4 インサート ×4、タッピングボス ×10、カバービス柱。ボス高さ 10 は仮値 (要実測)。3D STEP は会員 DL 待ち
if (show_vessel) color("LightSteelBlue", 0.22) translate([0, 0, 0])  import("../../parts/parent/exterior/cots/bcas212310g/bcas212310g.stl");
