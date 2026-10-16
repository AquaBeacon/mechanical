// =====================================================================
// child_interior_view.scad
// !! 自動生成ファイル - 編集しないこと。placement.json を直して
//    build.ps1 -Assemblies で再生成する。
// 2026-09-26: LCD撤去。下側は専用フランジブレースへ置換。左右ラグは接線方向へ拡幅し斜めリブを追加。旧記述は履歴。
// 子機 (水中ユニット) 内装のみのサブアセンブリ。親機の parent_interior_p1 と同じ位置づけ。
// 容器: WTE4 4in × 200mm アクリルチューブ + 上下フランジ BR-101040 (透明表示・取合い確認用)。下エンドキャップ (5×M10) と上ドーム (仮モデル) も透明表示 (2026-09-03 追加)。外装シェル / カメラは表示しない。
// 2026-08-28: 浮いていた部品を全部固定 — スペーサ・ねじ・ワッシャ・シム・フォームパッドを実体化し、貫通していた 4 箇所 (LCD/ベゼル前板、電池箱アンカー/デッキ、ヒンジ枠ラグ/アーチ、ナックル/ドア板) を部品形状で修正。
// 2026-09-03: 電池を 35×26×110 (リード −Z 出し) に変更。電池箱を ∩ チャンネル + 着脱床板 (皿ねじ 1 本) に作り直し、電池だけを取り出せるようにした。電源リードは切って XT30 メスを付け、基板側は J_BAT パッド直付けのピグテール (XT30 ペアは +X レール z 25..55)。基板間 XH ハーネスをモデル化 (parts/common/cabling/child_harness)。
// 2026-09-03: 下フランジ固定を 3 点化 — 0°/180° (デッキラグ + MF10) に加え、90° (0,+47) を下 LCD アーチ (child_lcd_support_lower) の耳で直接フランジ内面へ M3×12。270° は電池箱床が塞ぐため未使用。上フランジ 4 穴は内側からねじが回せないので使わない。穴の根拠: parts/child/exterior/cots/wte4_flange/_work/images/ref/BR-101040_hole_map.png + WTE データシート Rev C.5。
// interior グループは assemblies/child_vertical_assembly/placement.json と同一 (生成元: 本 placement を正とし、scad/lib/sync_child_interior.py で複製)。
// 配置根拠: docs/子機内装_収まり検討.md / docs/子機内装_サービス設計.md。検証: scad/lib/verify_child_interior.py, scad/lib/check_asm_contacts.py。
// 座標系: X=左右(カメラ基線) / Y=前後(+Y が前・カメラとライトの向き) / Z=上。アクリルチューブ下端面が z=0。
// =====================================================================

show_vessel = true;
show_interior = true;
show_penetrators = true;
show_keepout = true;

// 着脱床板 (37.4 × 3)。+Z 端のフック 2 個がリップのスロットへ、−Z 端のタブ (z 14..20) を端壁の柱へ M3×8 皿ねじ 1 本。外すと電池が −Y へ出る
if (show_interior) color("Peru", 1) translate([0, 0, 20])  import("../../parts/child/interior/printed/child_vtray_batt_floor/child_vtray_batt_floor.stl");
// M3×8 皿。床板の −Z タブ (y -43) から +Y へ、端壁の柱の下穴 Ø2.5 (深さ 6) にセルフタップ。サービスねじ Z36、+X 側壁。フランジ固定後も -Y 側からアクセス可能
if (show_interior) color("Silver", 1) translate([22.5, -43, 36]) rotate([90, 0, 0])  import("../../parts/common/interior/cots/screw/screw_m3x8_flat.stl");
// M3 MF10。下フランジ内面 (z=19) の BCD94 M3 穴へオスを 4〜5mm ねじ込む (6 を超えない)。オス部はフランジ金属の中 = 包絡検証対象外
if (show_interior) color("Goldenrod", 1) translate([47, 0, 19])  import("../../parts/common/interior/cots/hex_spacer/hex_spacer_m3_mf10.stl");
// M3x18: printed 12 mm bearing seat, MF10 engagement 6 mm
if (show_interior) color("Silver", 1) translate([47, 0, 41])  import("../../parts/common/interior/cots/screw/screw_m3x18.stl");
// M3 MF10。下フランジ内面 (z=19) の BCD94 M3 穴へオスを 4〜5mm ねじ込む (6 を超えない)。オス部はフランジ金属の中 = 包絡検証対象外
if (show_interior) color("Goldenrod", 1) translate([-47, 0, 19])  import("../../parts/common/interior/cots/hex_spacer/hex_spacer_m3_mf10.stl");
// M3x18: printed 12 mm bearing seat, MF10 engagement 6 mm
if (show_interior) color("Silver", 1) translate([-47, 0, 41])  import("../../parts/common/interior/cots/screw/screw_m3x18.stl");
// M3x18: printed 12 mm bearing seat, flange engagement 6 mm
if (show_interior) color("Silver", 1) translate([0, 47, 31])  import("../../parts/common/interior/cots/screw/screw_m3x18.stl");
// Printed brace: closed 12 mm bearing seat, rounded beams, pan screws
if (show_interior) color("Gold", 1) translate([0, 0, 22])  import("../../parts/child/interior/printed/child_flange_brace/child_flange_brace.stl");
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
// Printed closed seats, rounded roots spread over Z20..51
if (show_interior) color("Orange", 0.9)  import("../../parts/child/interior/printed/child_vtray_deck/child_vtray_deck_t200.stl");
// LiPo ∩ ベイ (2026-09-03 作り直し: 35×26×110 用)。デッキ下面へ耳 M3×8 ×4。−Z 端壁 (z 14..20、両端にリード切欠き) は貫通口の中、+Z はリップ (z 132..133.5、床板フックのスロット付き)。床は別部品
if (show_interior) color("Chocolate", 0.9) translate([0, 0, 20])  import("../../parts/child/interior/printed/child_vtray_batt_box/child_vtray_batt_box.stl");
if (show_keepout) color("Red", 0.55)  import("../../spec/child_interior_reinforcement/service_tool_keepout.stl");
if (show_keepout) color("LimeGreen", 0.35)  import("../../spec/child_interior_reinforcement/service_wire_keepout.stl");
// 下アルミキャップ (M10 x5 / BCD56)。プラグ(局所 z0..4.2)を下フランジ口へ差し込み、外面が z=-13.8。キャップ固定ねじ 6× M3×12 は BCD108 (フランジ外面)。内装固定はこのキャップではなくフランジ内面 BCD94
if (show_vessel) color("LightSteelBlue", 0.22) translate([0, 0, -3.8]) rotate([180, 0, 0]) translate([-60.15, -57.15, 0])  import("../../parts/child/exterior/cots/wte4_end_cap_5xm10/WTE4-M-END-CAP-5XM10-R2.stl");
