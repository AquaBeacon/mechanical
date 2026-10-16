// =====================================================================
// parent_interior_p1_view.scad
// !! 自動生成ファイル - 編集しないこと。placement.json を直して
//    build.ps1 -Assemblies で再生成する。
// 親機 防水ボックス内装 パターン1 (親機カメラ = DJI Osmo Action 6 外付け)。
// 容器: タカチ BCAS212310G (選定案 2026-08-28, 人間確認待ち)。
// 配置根拠: docs/親機内装_収まり検討.md / spec/parent_interior_layout.py。
// 蓋は表示しない (BCAS はビス止め蓋)。
// LiPo は P-MAIN 上のブリッジトレイ parent_lipo_tray (M3 MF25 スペーサ ×4) に上固定 = 最上段で交換しやすい (2026-08-28)。
// 箱モデルはタカチ図面 DXF 実座標 (ref/BCAS212310G.dxf)。
// 南壁 (Y=0) 上部 z=65 に WetLink M10 ペネトレータ ×2 (x=120 テザー / x=85 TD04A) を追加 (2026-08-29)。箱側の Ø10.2 追加工は bcas212310g.scad の pen_x/pen_z。
// 座標系: 箱外形の左下手前が原点。X=210 / Y=230 / Z=上 (箱底外面 z=0, 内床 z=3.8, プレート下面 z=13.8 (ボス 10 仮))。ビューポート方位 (+X) は浮子/マストに対する箱の向き基準。
// =====================================================================

show_vessel = true;
show_interior = true;

// 183x203 t5。プレート左下 = 箱 (13.5,13.5)、下面 z=13.8 (床3.8+ボス10 仮)
if (show_interior) color("Orange", 0.9) translate([13.5, 13.5, 13.8])  import("../../parts/parent/interior/printed/parent_plate/parent_plate_p1.stl");
// モデルは Y=-88..0。プレート (2,2)-(114,90)、ボタン/LED/DS3231 縁が北 (+Y)。基板下面 z=24.8 (プレート上面18.8+ボス6)。取付ねじの代わりに M3 MF25 スペーサ ×4 (LiPo トレイ支持)
if (show_interior) color("SteelBlue", 1) translate([15.5, 103.5, 24.8])  import("../../parts/parent/interior/pcb/parent_main/parent_main.stl");
// モデルは Y=-84..0。プレート (2,95)-(102,179)
if (show_interior) color("MediumSeaGreen", 1) translate([15.5, 192.5, 24.8])  import("../../parts/parent/interior/pcb/parent_pwr/parent_pwr.stl");
// 90度回転でプレート (121,77)-(171,151)。プレート直付け (p1)
if (show_interior) color("Gold", 1) translate([134.5, 94.5, 24.8]) rotate([0, 0, 90])  import("../../parts/parent/interior/pcb/tx_improved/tx_improved.stl");
// 簡易モデル (穴・スタック高は仮)。90度回転でプレート (121,2)-(174.5,70.6)
if (show_interior) color("SandyBrown", 1) translate([188, 15.5, 24.8]) rotate([0, 0, 90])  import("../../parts/parent/interior/cots/spresense_logger/spresense_logger.stl");
// ブリッジトレイ。原点 = MAIN 南西穴 (箱 20,23.5)、下面 z=51.4 (MAIN 基板上面 26.4 + スペーサ 25)。M3×6 ×4 でスペーサへ
if (show_interior) color("DarkOrange", 0.9) translate([20, 23.5, 51.4])  import("../../parts/parent/interior/printed/parent_lipo_tray/parent_lipo_tray.stl");
// parent_lipo_tray 内 (セル下面 z=54.4、上面 77.4、蓋パッキン面 90.9)。180°回転でリードを -X (西) へ → P-PWR J_BAT
if (show_interior) color("IndianRed", 1) translate([122.5, 68, 54.4]) rotate([0, 0, 180])  import("../../parts/common/interior/cots/lipo_3s_2200_zeee/lipo_3s_2200_zeee_pack.stl");
// M3 MF 25。MAIN 取付穴を通してプレートのボス下穴へ (MAIN 固定ねじ兼用)。胴下端 = MAIN 基板上面 z=26.4
if (show_interior) color("Goldenrod", 1) translate([20, 23.5, 26.4])  import("../../parts/common/interior/cots/hex_spacer/hex_spacer_m3_mf25.stl");
// M3 MF 25。MAIN 取付穴を通してプレートのボス下穴へ (MAIN 固定ねじ兼用)。胴下端 = MAIN 基板上面 z=26.4
if (show_interior) color("Goldenrod", 1) translate([123, 23.5, 26.4])  import("../../parts/common/interior/cots/hex_spacer/hex_spacer_m3_mf25.stl");
// M3 MF 25。MAIN 取付穴を通してプレートのボス下穴へ (MAIN 固定ねじ兼用)。胴下端 = MAIN 基板上面 z=26.4
if (show_interior) color("Goldenrod", 1) translate([20, 99, 26.4])  import("../../parts/common/interior/cots/hex_spacer/hex_spacer_m3_mf25.stl");
// M3 MF 25。MAIN 取付穴を通してプレートのボス下穴へ (MAIN 固定ねじ兼用)。胴下端 = MAIN 基板上面 z=26.4
if (show_interior) color("Goldenrod", 1) translate([123, 99, 26.4])  import("../../parts/common/interior/cots/hex_spacer/hex_spacer_m3_mf25.stl");
// WetLink Penetrator M10 (参考モデル・仮寸)。南壁 (Y=0) x=120, 軸 z=65。C1 テザー → P-MAIN J_TETH1 (箱 x≈123 の直下)。頭+プラグは箱外 y=-22..0、ねじ+ナットが箱内 y=0..14.5 (モデル壁 6.1 基準。実壁 3.08 なら 11.5)。容器内に出るのは素の導体 (外被は濡れ側で終端)。型番 -045..-085 はテザー外径待ち
if (show_vessel) color("Silver", 1) translate([120, 0, 65]) rotate([-90, 0, 0])  import("../../parts/common/exterior/cots/wetlink_penetrator_m10/wetlink_penetrator_m10_ref_bcas.stl");
// WetLink Penetrator M10 (参考モデル・仮寸)。南壁 (Y=0) x=85, 軸 z=65。C3 TD04A → TX (右列)。3P プラグは通らないのでケーブルを切って容器内で端子台に落とす前提 (td04a_transducer.md)。テザー側とのピッチ 35 = 16mm トルクレンチの振り代。東へ寄せられないのは SPRESENSE (箱 X 134.5-188) の天面が仮値 30 で、その上を通すと隙間 0.3 になるため (spec/parent_interior_layout.py check_penetrators)
if (show_vessel) color("Silver", 1) translate([85, 0, 65]) rotate([-90, 0, 0])  import("../../parts/common/exterior/cots/wetlink_penetrator_m10/wetlink_penetrator_m10_ref_bcas.stl");
// タカチ図面 DXF 実座標モデル: 床 3.84 + リブ台 3 (193.2×173.2)、M4 インサート ×4、タッピングボス ×10、カバービス柱。ボス高さ 10 は仮値 (要実測)。3D STEP は会員 DL 待ち
if (show_vessel) color("LightSteelBlue", 0.22) translate([0, 0, 0])  import("../../parts/parent/exterior/cots/bcas212310g/bcas212310g.stl");
