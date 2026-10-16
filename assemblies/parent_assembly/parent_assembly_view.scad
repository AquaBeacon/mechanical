// =====================================================================
// parent_assembly_view.scad
// !! 自動生成ファイル - 編集しないこと。placement.json を直して
//    build.ps1 -Assemblies で再生成する。
// 親機 (水上ユニット) 全体アセンブリ (2026-09-04 新規)。
// 構成 (人間決定 2026-09-04): 市販の紡錘形フロート ×2 (仮 Ø100×300、中心に紐通しの空洞) を parent_float_yoke ×4 (デッキ側壁 HP40 座) の両端の柱で受け、空洞に通した紐で引き寄せて固定 (2026-09-05: 胴は挟まない)。デッキ上にタカチ BCAS212310G (箱底コーナー外部取付穴 Ø4.2 ×4 → デッキ M4 インサート)。支柱 (マスト) 無し。TD04A は デッキ下面キールの HP40 座 (南, Y=-70) に xdcr_socket_parent (tilt 0) を開口下向きで固定。Osmo Action 6 (防水ケース) の固定ジグは後日 → 北座 (Y=+70) を予約。中央座 (Y=0) は予備。
// 内装は parent_interior_p1 (Osmo 外付け) と同一 (箱原点をデッキ座標 (-105,-115,0) へ平行移動)。
// 座標系: 箱中心 = 原点、デッキ上面 = 箱底外面 z=0、+Y = 北 (箱の北壁側)、+Z = 上。箱座標 (x,y,z) → 本座標 (x-105, y-115, z)。浮子軸 = Y、浮子中心 X=±178 / z=0 (2026-09-05: 浮子軸 = 箱底。縦揺れ GM 最大)。
// =====================================================================

show_vessel = true;
show_interior = true;
show_exterior = true;

// TD04A ソケット parent バリアント (2026-09-04: tilt 0, base 50 = HP40 互換。child と同形状)。キール南座 (Y=-70, 座面 z=-60) に開口下向き: X 軸 180° 回転でベース底面 (local z=0) を座面へ。M5×4 @ ±20。振動子面は z≈-104 (ソケット 38 + 底 6)
if (show_exterior) color("Gold", 1) translate([0, -70, -60]) rotate([180, 0, 0])  import("../../parts/common/exterior/printed/xdcr_socket/xdcr_socket_parent.stl");
// 南壁 x=120 (デッキ X=+15), z=65。C1 テザー。頭は箱外 y=-137..-115 (デッキ南縁 -118 の外)
if (show_vessel) color("Silver", 1) translate([15, -115, 65]) rotate([-90, 0, 0])  import("../../parts/common/exterior/cots/wetlink_penetrator_m10/wetlink_penetrator_m10_ref_bcas.stl");
// 南壁 x=85 (デッキ X=-20), z=65。C3 TD04A → 南縁切欠き (X -30..25) → キール南端フェアリード → 南座のソケットへ
if (show_vessel) color("Silver", 1) translate([-20, -115, 65]) rotate([-90, 0, 0])  import("../../parts/common/exterior/cots/wetlink_penetrator_m10/wetlink_penetrator_m10_ref_bcas.stl");
// p1 と同一 (箱 (15.5,103.5,24.8))
if (show_interior) color("SteelBlue", 1) translate([-89.5, -11.5, 24.8])  import("../../parts/parent/interior/pcb/parent_main/parent_main.stl");
// p1 と同一 (箱 (15.5,192.5,24.8))
if (show_interior) color("MediumSeaGreen", 1) translate([-89.5, 77.5, 24.8])  import("../../parts/parent/interior/pcb/parent_pwr/parent_pwr.stl");
// p1 と同一 (箱 (134.5,94.5,24.8) rot 90)
if (show_interior) color("Gold", 1) translate([29.5, -20.5, 24.8]) rotate([0, 0, 90])  import("../../parts/parent/interior/pcb/tx_improved/tx_improved.stl");
// p1 と同一 (箱 (188,15.5,24.8) rot 90)
if (show_interior) color("SandyBrown", 1) translate([83, -99.5, 24.8]) rotate([0, 0, 90])  import("../../parts/parent/interior/cots/spresense_logger/spresense_logger.stl");
// p1 と同一 (箱 (122.5,68,54.4) rot 180)
if (show_interior) color("IndianRed", 1) translate([17.5, -47, 54.4]) rotate([0, 0, 180])  import("../../parts/common/interior/cots/lipo_3s_2200_zeee/lipo_3s_2200_zeee_pack.stl");
// p1 と同一
if (show_interior) color("Goldenrod", 1) translate([-85, -91.5, 26.4])  import("../../parts/common/interior/cots/hex_spacer/hex_spacer_m3_mf25.stl");
// p1 と同一
if (show_interior) color("Goldenrod", 1) translate([18, -91.5, 26.4])  import("../../parts/common/interior/cots/hex_spacer/hex_spacer_m3_mf25.stl");
// p1 と同一
if (show_interior) color("Goldenrod", 1) translate([-85, -16, 26.4])  import("../../parts/common/interior/cots/hex_spacer/hex_spacer_m3_mf25.stl");
// p1 と同一
if (show_interior) color("Goldenrod", 1) translate([18, -16, 26.4])  import("../../parts/common/interior/cots/hex_spacer/hex_spacer_m3_mf25.stl");
// デッキ本体 (原点)。216×236、側壁 z-50、キール座面 z-60
if (show_exterior) color("DarkOrange", 0.95) translate([0, 0, 0])  import("../../parts/parent/exterior/printed/parent_deck/parent_deck.stl");
// 右舷後 (hand +1、腕 +Y)。アダプタ面 = デッキ側壁 X=108 の HP40 (Y +70, z -25)。柱内面 Y 153 = 浮子端 150 + 3
if (show_exterior) color("Orange", 0.95) translate([108, 70, -25])  import("../../parts/parent/exterior/printed/parent_float_yoke/parent_float_yoke_a.stl");
// 右舷前 (hand -1、腕 -Y)
if (show_exterior) color("Orange", 0.95) translate([108, -70, -25])  import("../../parts/parent/exterior/printed/parent_float_yoke/parent_float_yoke_b.stl");
// 左舷後 = b を Z 軸 180° 回転 (腕 +Y、X 外向き -X)
if (show_exterior) color("Orange", 0.95) translate([-108, 70, -25]) rotate([0, 0, 180])  import("../../parts/parent/exterior/printed/parent_float_yoke/parent_float_yoke_b.stl");
// 左舷前 = a を Z 軸 180° 回転
if (show_exterior) color("Orange", 0.95) translate([-108, -70, -25]) rotate([0, 0, 180])  import("../../parts/parent/exterior/printed/parent_float_yoke/parent_float_yoke_a.stl");
// parent_interior_p1 と同一配置 (箱 (13.5,13.5,13.8))
if (show_interior) color("Orange", 0.9) translate([-91.5, -101.5, 13.8])  import("../../parts/parent/interior/printed/parent_plate/parent_plate_p1.stl");
// p1 と同一 (箱 (20,23.5,51.4))
if (show_interior) color("DarkOrange", 0.9) translate([-85, -91.5, 51.4])  import("../../parts/parent/interior/printed/parent_lipo_tray/parent_lipo_tray.stl");
// 紡錘形フロート (仮 Ø100×300、先細り 40、端面 Ø40、空洞 Ø15)。軸 X=±(108+70)=±178、z=0 (浮子 -50..+50 = 箱の下半分と同じ高さ。喫水線 -2.7 = 箱底がほぼ水面。spec/parent_hydrostatics.py で縦揺れ GM 最大)。紐で片側 (+Y) の円錐座に引き寄せた状態 (中央から +2 の余裕のうち 1.95 だけ寄せ、リムと座の接線接触 0.05 を残す = 検査の誤判定回避)
if (show_exterior) color("LightSkyBlue", 0.6) translate([178, 1.95, 0])  import("../../parts/parent/exterior/cots/parent_fender/parent_fender.stl");
// 紡錘形フロート (仮 Ø100×300、先細り 40、端面 Ø40、空洞 Ø15)。軸 X=±(108+70)=±178、z=0 (浮子 -50..+50 = 箱の下半分と同じ高さ。喫水線 -2.7 = 箱底がほぼ水面。spec/parent_hydrostatics.py で縦揺れ GM 最大)。紐で片側 (+Y) の円錐座に引き寄せた状態 (中央から +2 の余裕のうち 1.95 だけ寄せ、リムと座の接線接触 0.05 を残す = 検査の誤判定回避)
if (show_exterior) color("LightSkyBlue", 0.6) translate([-178, 1.95, 0])  import("../../parts/parent/exterior/cots/parent_fender/parent_fender.stl");
// タカチ BCAS212310G。箱原点 (外形左下・箱底外面) をデッキ座標 (-105,-115,0) へ。外部取付穴 (箱 (9,9)(201,9)(9,221)(201,221)) = デッキ (±96, ±106)
if (show_vessel) color("LightSteelBlue", 0.22) translate([-105, -115, 0])  import("../../parts/parent/exterior/cots/bcas212310g/bcas212310g.stl");
