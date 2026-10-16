// =====================================================================
// mount_detail_view.scad
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

// M3 MF10。下フランジ内面 (z=19) の BCD94 M3 穴へオスを 4〜5mm ねじ込む (6 を超えない)。オス部はフランジ金属の中 = 包絡検証対象外
if (show_interior) color("Goldenrod", 1) translate([47, 0, 19])  import("../../parts/common/interior/cots/hex_spacer/hex_spacer_m3_mf10.stl");
// M3x18: metal-to-metal preload, 0.2 mm plastic clearance; MF10 engagement 4.3 mm
if (show_interior) color("Silver", 1) translate([47, 0, 42.7])  import("../../parts/common/interior/cots/screw/screw_m3x18.stl");
// M3 MF10。下フランジ内面 (z=19) の BCD94 M3 穴へオスを 4〜5mm ねじ込む (6 を超えない)。オス部はフランジ金属の中 = 包絡検証対象外
if (show_interior) color("Goldenrod", 1) translate([-47, 0, 19])  import("../../parts/common/interior/cots/hex_spacer/hex_spacer_m3_mf10.stl");
// M3x18: metal-to-metal preload, 0.2 mm plastic clearance; MF10 engagement 4.3 mm
if (show_interior) color("Silver", 1) translate([-47, 0, 42.7])  import("../../parts/common/interior/cots/screw/screw_m3x18.stl");
// M3x18: steel sleeve and strap, flange thread engagement 4.3 mm
if (show_interior) color("Silver", 1) translate([0, 47, 32.7])  import("../../parts/common/interior/cots/screw/screw_m3x18.stl");
// Steel compression sleeve OD5 ID3.2 L12.2, cut ends flat; bears on metal
if (show_interior) color("Silver", 1) translate([47, 0, 29])  import("../../parts/common/interior/cots/child_mount_metal/child_mount_metal_sleeve_12_2.stl");
// Steel clamping strap 5x12x1.5; plastic clearance 0.2 mm
if (show_interior) color("Silver", 1) translate([47, 0, 41.2])  import("../../parts/common/interior/cots/child_mount_metal/child_mount_metal_flange_plate.stl");
// Steel compression sleeve OD5 ID3.2 L12.2, cut ends flat; bears on metal
if (show_interior) color("Silver", 1) translate([-47, 0, 29])  import("../../parts/common/interior/cots/child_mount_metal/child_mount_metal_sleeve_12_2.stl");
// Steel clamping strap 5x12x1.5; plastic clearance 0.2 mm
if (show_interior) color("Silver", 1) translate([-47, 0, 41.2])  import("../../parts/common/interior/cots/child_mount_metal/child_mount_metal_flange_plate.stl");
// Steel compression sleeve OD5 ID3.2 L12.2, cut ends flat; bears on metal
if (show_interior) color("Silver", 1) translate([0, 47, 19])  import("../../parts/common/interior/cots/child_mount_metal/child_mount_metal_sleeve_12_2.stl");
// Steel clamping strap 5x12x1.5; plastic clearance 0.2 mm
if (show_interior) color("Silver", 1) translate([0, 47, 31.2]) rotate([0, 0, 90])  import("../../parts/common/interior/cots/child_mount_metal/child_mount_metal_flange_plate.stl");
// t200 deck: 12 mm open forks, wide 8.7 mm roots over Z20..41; steel sleeves take preload
if (show_interior) color("Orange", 0.55)  import("../../parts/child/interior/printed/child_vtray_deck/child_vtray_deck_t200.stl");
// 下フランジ。ピストン(局所 z0..19)を上へ向けてチューブ座ぐりへ 19mm 挿入 → カラー(Ø114.3)が z -8..0 に露出
if (show_vessel) color("LightSteelBlue", 0.22) translate([0, 0, 19]) rotate([180, 0, 0]) translate([-57.15, -57.15, 0])  import("../../parts/child/exterior/cots/wte4_flange/BR-101040_RevC.stl");
