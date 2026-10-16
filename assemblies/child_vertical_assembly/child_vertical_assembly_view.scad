// =====================================================================
// child_vertical_assembly_view.scad
// !! 自動生成ファイル - 編集しないこと。placement.json を直して
//    build.ps1 -Assemblies で再生成する。
// 2026-10-01 bolted revision: battery M3x12/nut x4, floor M3x10 flat/nut, printed broader roots, front flange M3x16. Earlier notes below are history.
// AquaBeacon 子機 縦置き(吊り下げ)構成の組立モデル。
// 耐圧容器 WTE4 4in x 200mm を縦に立て、ドームを上・アルミキャップ(ペネトレータ)を下にする。
// 容器は child_shell_aft / child_shell_fwd の2枚で挟み、M5蝶ボルト4本で締結する。
// 前半シェルを外すと容器を真上に抜ける。ロープは上部の吊り耳2点にブライドルで掛ける。
// 
// 横置き構成 (assemblies/child_assembly) とは別系統。両方を同時に成立させることはできない。
// 
// 内装は2026-08-02の実基板 CHILD_MAIN v4.1(104x88) / CHILD_PWR v2.1(62x70)を使用。
// 外向きLCD、軸方向LiPoゲート、下フランジM3 BCD94アンカー、面取りグライドリブを含む。
// 詳細は docs/子機内装_サービス設計.md。
// 座標系: X=左右(カメラ基線) / Y=前後(+Y が前・カメラとライトの向き) / Z=上。アクリルチューブ下端面が z=0。
// =====================================================================

show_vessel = true;
show_shell = true;
show_camera = true;
show_interior = true;
show_penetrators = true;

// 下アルミキャップ (M10 x5 / BCD56)。プラグ(局所 z0..4.2)を下フランジ口へ差し込み、外面が z=-13.8。ここから全ケーブルが下へ出る
if (show_vessel) color("Gainsboro") translate([0, 0, -3.8]) rotate([180, 0, 0]) translate([-60.15, -57.15, 0])  import("../../parts/child/exterior/cots/wte4_end_cap_5xm10/WTE4-M-END-CAP-5XM10-R2.stl");
// 右舷カメラ押え蓋 (M4 蝶ボルト x2)
if (show_camera) color("Tomato") translate([75, 70.3, 145])  import("../../parts/child/exterior/printed/child_cam_lid/child_cam_lid.stl");
// 左舷カメラ押え蓋 (形状は X 対称なので同じ物)
if (show_camera) color("Tomato") translate([-75, 70.3, 145])  import("../../parts/child/exterior/printed/child_cam_lid/child_cam_lid.stl");
// 水中ライトの割りクランプ 上半分。下半分は shell_fwd と一体。ライト軸 z=58、前面はレンズ面より後ろ
if (show_camera) color("Gold") translate([0, 78, 58])  import("../../parts/child/exterior/printed/child_light_clamp/child_light_clamp.stl");
// TD04A ソケット (上向き / tilt_deg=0)。パイロン屋根 z=182 の上、y=-86。振動子の放射面は z≈243 でドーム頂点(261)より低い
if (show_camera) color("Orange") translate([0, -86, 182])  import("../../parts/common/exterior/printed/xdcr_socket/xdcr_socket_child.stl");
// M3x6 top rib stop, M3 pilot and exposed 6.6 mm head/tool reserve
if (show_interior) color("Silver", 1) translate([0, -6, 200]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m3x6.stl");
// 3 mm removable floor with 14 mm service tab, M3x10 flat and captive nut; slide -Z2 then withdraw -Y
if (show_interior) color("Peru", 1) translate([0, 0, 20])  import("../../parts/child/interior/printed/child_vtray_batt_floor/child_vtray_batt_floor.stl");
// LiPo 35×26×110 (ユーザー指定 2026-09-03、型番要確認)。リード側端面 (モデル +X) を −Z に向けて z 21..131。床板に載り、上 3 / 側 2 / 端 1 のフォームで拘束。リードスタブ ×2 は端壁の切欠きへ
if (show_interior) color("Crimson", 1) translate([-17.5, -14, 131]) rotate([0, 90, -90])  import("../../parts/child/interior/cots/lipo_35x26x110/lipo_35x26x110_leads.stl");
// C-MAIN 104x88: lower two holes secured by brace MF30/12; upper two by M3x8
if (show_interior) color("ForestGreen", 1) translate([44, 3, 20]) rotate([0, -90, -90])  import("../../parts/child/interior/pcb/child_main/child_main.stl");
// CHILD_PWR v2.1 (62×70)。基板下面 y=4 (ボス 10)。M3×8 ×4
if (show_interior) color("SeaGreen", 1) translate([35, 4, 126]) rotate([0, -90, -90])  import("../../parts/child/interior/pcb/child_pwr/child_pwr.stl");
// RX_improved_mini (68×46)。デッキ下面に M2 FF6 スペーサ ×4 で吊る (基板上面 y=-16、部品は -Y)
if (show_interior) color("MediumSeaGreen", 1) translate([34, -16, 134]) rotate([-90, 0, 180])  import("../../parts/child/interior/pcb/rx_improved_mini/rx_improved_mini.stl");
// M3×8。CHILD_PWR 取付穴 → デッキ PWR ボス (10) 下穴へセルフタップ
if (show_interior) color("Silver", 1) translate([31, 5.6, 130]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m3x8.stl");
// M3×8。CHILD_PWR 取付穴 → デッキ PWR ボス (10) 下穴へセルフタップ
if (show_interior) color("Silver", 1) translate([31, 5.6, 184]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m3x8.stl");
// M3×8。CHILD_PWR 取付穴 → デッキ PWR ボス (10) 下穴へセルフタップ
if (show_interior) color("Silver", 1) translate([-31, 5.6, 130]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m3x8.stl");
// M3×8。CHILD_PWR 取付穴 → デッキ PWR ボス (10) 下穴へセルフタップ
if (show_interior) color("Silver", 1) translate([-31, 5.6, 184]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m3x8.stl");
// M3x12 through deck 4 mm and bay pad 8 mm; captive nut, no plastic thread
if (show_interior) color("Silver", 1) translate([24, -6, 32]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m3x12.stl");
// M3x12 through deck 4 mm and bay pad 8 mm; captive nut, no plastic thread
if (show_interior) color("Silver", 1) translate([24, -6, 110]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m3x12.stl");
// M3x12 through deck 4 mm and bay pad 8 mm; captive nut, no plastic thread
if (show_interior) color("Silver", 1) translate([-24, -6, 32]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m3x12.stl");
// M3x12 through deck 4 mm and bay pad 8 mm; captive nut, no plastic thread
if (show_interior) color("Silver", 1) translate([-24, -6, 110]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m3x12.stl");
// M3x10 flat: reinforced service tab and captive M3 nut; 1.1 mm nominal tip projection
if (show_interior) color("Silver", 1) translate([22.5, -43, 36]) rotate([90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m3x10_flat.stl");
// M3 MF10。下フランジ内面 (z=19) の BCD94 M3 穴へオスを 4〜5mm ねじ込む (6 を超えない)。オス部はフランジ金属の中 = 包絡検証対象外
if (show_interior) color("Goldenrod", 1) translate([47, 0, 19])  import("../../parts/common/interior/cots/hex_spacer/hex_spacer_m3_mf10.stl");
// M3x18: printed 12 mm bearing seat, MF10 engagement 6 mm
if (show_interior) color("Silver", 1) translate([47, 0, 41])  import("../../parts/common/interior/cots/screw/screw_m3x18.stl");
// M3 MF10。下フランジ内面 (z=19) の BCD94 M3 穴へオスを 4〜5mm ねじ込む (6 を超えない)。オス部はフランジ金属の中 = 包絡検証対象外
if (show_interior) color("Goldenrod", 1) translate([-47, 0, 19])  import("../../parts/common/interior/cots/hex_spacer/hex_spacer_m3_mf10.stl");
// M3x18: printed 12 mm bearing seat, MF10 engagement 6 mm
if (show_interior) color("Silver", 1) translate([-47, 0, 41])  import("../../parts/common/interior/cots/screw/screw_m3x18.stl");
// M3x16 through 12 mm printed seat; flange engagement 4 mm, blind-hole depth respected
if (show_interior) color("Silver", 1) translate([0, 47, 31])  import("../../parts/common/interior/cots/screw/screw_m3x16.stl");
// M3 MF30: C-MAIN and lower flange brace mounting
if (show_interior) color("Goldenrod", 1) translate([-22, 4.6, 24.5]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/hex_spacer/hex_spacer_m3_mf30.stl");
// M3x12 pan screw: flat printed seat, spacer engagement 6.5 mm
if (show_interior) color("Silver", 1) translate([-22, 40.1, 24.5]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m3x12.stl");
// M3 MF12: C-MAIN and lower flange brace mounting
if (show_interior) color("Goldenrod", 1) translate([39.5, 4.6, 24.5]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/hex_spacer/hex_spacer_m3_mf12.stl");
// M3x12 pan screw: flat printed seat, spacer engagement 6.5 mm
if (show_interior) color("Silver", 1) translate([39.5, 22.1, 24.5]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m3x12.stl");
// M3x8: board 1.6 mm + deck boss engagement 6.4 mm
if (show_interior) color("Silver", 1) translate([-22, 4.6, 119.5]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m3x8.stl");
// M3x8: board 1.6 mm + deck boss engagement 6.4 mm
if (show_interior) color("Silver", 1) translate([39.5, 4.6, 119.5]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m3x8.stl");
// Printed brace: 12 mm beams, 24 mm webs, 20 mm tangential flange seat, existing M3 spacers
if (show_interior) color("Gold", 1) translate([0, 0, 22])  import("../../parts/child/interior/printed/child_flange_brace/child_flange_brace.stl");
// Paired RX clamp: original Z140.5/174.5 contacts and screw axes retained; bridge outside PCB
if (show_interior) color("Orange", 1) translate([0, 0, 140.5]) scale([-1, 1, 1])  import("../../parts/child/interior/printed/child_rx_edge_clamp/child_rx_edge_clamp_base_pair.stl");
// Paired RX clamp: original Z140.5/174.5 contacts and screw axes retained; bridge outside PCB
if (show_interior) color("Orange", 1) translate([0, 0, 140.5]) scale([-1, 1, 1])  import("../../parts/child/interior/printed/child_rx_edge_clamp/child_rx_edge_clamp_cap_pair.stl");
// M3x8: deck 4 mm, printed base engagement 4 mm
if (show_interior) color("Silver", 1) translate([-37.5, -6, 134.5]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m3x8.stl");
// M3x8: cap 2.6 mm, base engagement 5.4 mm; 6 mm offset from mounting screw
if (show_interior) color("Silver", 1) translate([-37.5, -20.6, 140.5]) rotate([90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m3x8.stl");
// M3x8: deck 4 mm, printed base engagement 4 mm
if (show_interior) color("Silver", 1) translate([-37.5, -6, 180.5]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m3x8.stl");
// M3x8: cap 2.6 mm, base engagement 5.4 mm; 6 mm offset from mounting screw
if (show_interior) color("Silver", 1) translate([-37.5, -20.6, 174.5]) rotate([90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m3x8.stl");
// Paired RX clamp: original Z140.5/174.5 contacts and screw axes retained; bridge outside PCB
if (show_interior) color("Orange", 1) translate([0, 0, 140.5]) scale([1, 1, 1])  import("../../parts/child/interior/printed/child_rx_edge_clamp/child_rx_edge_clamp_base_pair.stl");
// Paired RX clamp: original Z140.5/174.5 contacts and screw axes retained; bridge outside PCB
if (show_interior) color("Orange", 1) translate([0, 0, 140.5]) scale([1, 1, 1])  import("../../parts/child/interior/printed/child_rx_edge_clamp/child_rx_edge_clamp_cap_pair.stl");
// M3x8: deck 4 mm, printed base engagement 4 mm
if (show_interior) color("Silver", 1) translate([37.5, -6, 134.5]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m3x8.stl");
// M3x8: cap 2.6 mm, base engagement 5.4 mm; 6 mm offset from mounting screw
if (show_interior) color("Silver", 1) translate([37.5, -20.6, 140.5]) rotate([90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m3x8.stl");
// M3x8: deck 4 mm, printed base engagement 4 mm
if (show_interior) color("Silver", 1) translate([37.5, -6, 180.5]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m3x8.stl");
// M3x8: cap 2.6 mm, base engagement 5.4 mm; 6 mm offset from mounting screw
if (show_interior) color("Silver", 1) translate([37.5, -20.6, 174.5]) rotate([90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m3x8.stl");
// WetLink M10: thread20, cap10, nutAF16 height8; dry tip Z6.2
if (show_penetrators) color("SlateGray", 1) translate([1.71451e-15, 28, -13.8])  import("../../parts/child/exterior/cots/wetlink_m10_confirmed/wetlink_m10_confirmed.stl");
// WetLink M10: thread20, cap10, nutAF16 height8; dry tip Z6.2
if (show_penetrators) color("SlateGray", 1) translate([26.6296, 8.65248, -13.8])  import("../../parts/child/exterior/cots/wetlink_m10_confirmed/wetlink_m10_confirmed.stl");
// WetLink M10: thread20, cap10, nutAF16 height8; dry tip Z6.2
if (show_penetrators) color("SlateGray", 1) translate([16.458, -22.6525, -13.8])  import("../../parts/child/exterior/cots/wetlink_m10_confirmed/wetlink_m10_confirmed.stl");
// WetLink M10: thread20, cap10, nutAF16 height8; dry tip Z6.2
if (show_penetrators) color("SlateGray", 1) translate([-16.458, -22.6525, -13.8])  import("../../parts/child/exterior/cots/wetlink_m10_confirmed/wetlink_m10_confirmed.stl");
// WetLink M10: thread20, cap10, nutAF16 height8; dry tip Z6.2
if (show_penetrators) color("SlateGray", 1) translate([-26.6296, 8.65248, -13.8])  import("../../parts/child/exterior/cots/wetlink_m10_confirmed/wetlink_m10_confirmed.stl");
// Purchased plain M3 nut AF5.5/t2.4; insert before cable rails
if (show_interior) color("Silver", 1) translate([24, -15.5, 32]) rotate([90, 0, 0]) rotate([0, 0, 30])  import("../../parts/common/interior/cots/screw/screw_nut_m3.stl");
// Purchased plain M3 nut AF5.5/t2.4; insert before cable rails
if (show_interior) color("Silver", 1) translate([24, -15.5, 110]) rotate([90, 0, 0]) rotate([0, 0, 30])  import("../../parts/common/interior/cots/screw/screw_nut_m3.stl");
// Purchased plain M3 nut AF5.5/t2.4; insert before cable rails
if (show_interior) color("Silver", 1) translate([-24, -15.5, 32]) rotate([90, 0, 0]) rotate([0, 0, 30])  import("../../parts/common/interior/cots/screw/screw_nut_m3.stl");
// Purchased plain M3 nut AF5.5/t2.4; insert before cable rails
if (show_interior) color("Silver", 1) translate([-24, -15.5, 110]) rotate([90, 0, 0]) rotate([0, 0, 30])  import("../../parts/common/interior/cots/screw/screw_nut_m3.stl");
// Purchased plain M3 nut AF5.5/t2.4; insert before cable rails
if (show_interior) color("Silver", 1) translate([22.5, -36.5, 36]) rotate([-90, 0, 0]) rotate([0, 0, 30])  import("../../parts/common/interior/cots/screw/screw_nut_m3.stl");
// 後半シェル (常設側)。吊り耳 x2 / 後部パイロン(TD04A台・取っ手・ケーブル導管) / 下部ガード取付ボス x4
if (show_shell) color("SeaGreen", 0.9)  import("../../parts/child/exterior/printed/child_shell_aft/child_shell_aft.stl");
// 前半シェル (ゲート側)。M5 蝶ボルト 4 本で外れる。カメラポッド x2 を一体で持つ = 基線 150 が単一部品で決まる
if (show_shell) color("SteelBlue", 0.9)  import("../../parts/child/exterior/printed/child_shell_fwd/child_shell_fwd.stl");
// 下部ガード。キャップを 3 点パッド(r42..50)で受け、スキッドリング Ø198 で自立。中央 r<42 と後方 ±40deg はケーブル用に開けてある
if (show_shell) color("DarkSlateGray", 0.9)  import("../../parts/child/exterior/printed/child_bottom_guard/child_bottom_guard.stl");
// t200 deck: broadened printed flange roots X28..48.7, Z20..100, bed Y-10; confirmed battery hole locations
if (show_interior) color("Orange", 0.9)  import("../../parts/child/interior/printed/child_vtray_deck/child_vtray_deck_t200.stl");
// 上センタリングリブ z 191.5..197.5。内側ショルダー (z 190.5) に当てる
if (show_interior) color("DarkOrange", 0.9) translate([0, 0, 191.5])  import("../../parts/child/interior/printed/child_vtray_rib/child_vtray_rib.stl");
// Reinforced battery bay: four 8 mm pads, M3x12 through bolts and plain captive M3 nuts
if (show_interior) color("Chocolate", 0.9) translate([0, 0, 20])  import("../../parts/child/interior/printed/child_vtray_batt_box/child_vtray_batt_box.stl");
// C-MAIN J_PWR1 ↔ C-PWR J_MAIN (XH9 ストレート 9 芯、Ø5.5)。MAIN 低背部の上 (x≈4, y≈15) を +Z へ
if (show_interior) color("DarkSlateGray", 0.9)  import("../../parts/common/cabling/child_harness/child_harness_xh9_pwr.stl");
// C-MAIN J_RX1 ↔ RX J2 (XH6、Ø4.5)。−X スリット (z 96) → −X レール溝 → RX 下面
if (show_interior) color("DarkSlateGray", 0.9)  import("../../parts/common/cabling/child_harness/child_harness_xh6_rx.stl");
// C-MAIN J_TETH1 → 下キャップ ペネトレータ (XH3、Ø3)。−X スリット → −X レール溝 → 下リブ開口
if (show_interior) color("DarkSlateGray", 0.9)  import("../../parts/common/cabling/child_harness/child_harness_xh3_teth.stl");
// C-MAIN J_TEMP1 → ペネトレータ (XH4、Ø3.5)。teth と同経路
if (show_interior) color("DarkSlateGray", 0.9)  import("../../parts/common/cabling/child_harness/child_harness_xh4_temp.stl");
// C-MAIN J_LEAK1 → ペネトレータ (XH2、Ø2.5)。teth と同経路
if (show_interior) color("DarkSlateGray", 0.9)  import("../../parts/common/cabling/child_harness/child_harness_xh2_leak.stl");
// C-MAIN J_PRS1 → ペネトレータ (XH4、Ø3.5)。+X スリット → +X レール溝 → 下リブ開口
if (show_interior) color("DarkSlateGray", 0.9)  import("../../parts/common/cabling/child_harness/child_harness_xh4_prs.stl");
// 電池リード (切って XT30 メス) → XT30 嵌合ペア (+X レール溝 z 25..55) → ピグテール → +X スリット (z 157) → C-PWR J_BAT パッド直付け。充電リード (XH4) は −X 側で下リブに結束
if (show_interior) color("DarkSlateGray", 0.9)  import("../../parts/common/cabling/child_harness/child_harness_bat.stl");
// C-PWR J_LED パッド直付けピグテール → −X スリット (z 157) → −X レール溝 → 下リブ開口 → ライト
if (show_interior) color("DarkSlateGray", 0.9)  import("../../parts/common/cabling/child_harness/child_harness_led.stl");
// 独立気泡フォーム 3t (106×33)。LiPo 上面 (y=-14) とデッキ下面 (-10) の間 (残り 1mm = 公差代)
if (show_interior) color("LightPink", 0.8) translate([0, -14, 76]) rotate([-90, 0, 0])  import("../../parts/common/interior/cots/foam_pad/foam_pad_clipo_top.stl");
// 独立気泡フォーム2t 102×24、Z23..125。側面サービスねじボスの逃げ切欠き付き
if (show_interior) color("LightPink", 0.8) translate([18, -27, 74]) rotate([0, 90, 0])  import("../../parts/common/interior/cots/foam_pad/foam_pad_clipo_side_service.stl");
// 同 -X 側
if (show_interior) color("LightPink", 0.8) translate([-18, -27, 74]) rotate([0, -90, 0])  import("../../parts/common/interior/cots/foam_pad/foam_pad_clipo_side_short.stl");
// 独立気泡フォーム 1t (20×24)。LiPo -Z 端 (リード側) と端壁の中央柱 (z=20) の間。リード出口 (|x|>10.5) は覆わない
if (show_interior) color("LightPink", 0.8) translate([0, -27, 21]) rotate([180, 0, 0])  import("../../parts/common/interior/cots/foam_pad/foam_pad_clipo_end.stl");
// 独立気泡フォーム 1t。LiPo +Z 端 (z=131) とリップ (z=132) の間
if (show_interior) color("LightPink", 0.8) translate([0, -27, 131])  import("../../parts/common/interior/cots/foam_pad/foam_pad_clipo_end.stl");
// 下フランジ。ピストン(局所 z0..19)を上へ向けてチューブ座ぐりへ 19mm 挿入 → カラー(Ø114.3)が z -8..0 に露出
if (show_vessel) color("LightSteelBlue", 0.6) translate([0, 0, 19]) rotate([180, 0, 0]) translate([-57.15, -57.15, 0])  import("../../parts/child/exterior/cots/wte4_flange/BR-101040_RevC.stl");
// 上フランジ。ピストンを下へ向けて挿入 → カラー上面が z=208 (= ドームの座面)
if (show_vessel) color("LightSteelBlue", 0.6) translate([0, 0, 181]) translate([-57.15, -57.15, 0])  import("../../parts/child/exterior/cots/wte4_flange/BR-101040_RevC.stl");
// 上ドーム BR-100495 の **参考モデル(仮)**。座面 z=208、頂点 z=261.25。dome_h=53.25 は要実測 — ここが全高の唯一の未確定要素
if (show_vessel) color("PowderBlue", 0.35) translate([0, 0, 208])  import("../../parts/child/exterior/cots/wte4_dome_cap/wte4_dome_cap_ref.stl");
// アクリルチューブ 4in x 200mm。元モデルは軸=X(0..200)/断面中心(57.15,57.15) → 軸を Z へ立てる。下端面が z=0
if (show_vessel) color("LightSteelBlue", 0.3) rotate([0, -90, 0]) translate([0, -57.15, -57.15])  import("../../parts/child/exterior/cots/wte4_acrylic_tube/BR-101052-200_RevB.stl");
