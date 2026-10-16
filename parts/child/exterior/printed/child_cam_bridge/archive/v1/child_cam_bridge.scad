// =====================================================================
// child_cam_bridge.scad — 子機 カメラブリッジ (HP4/HP5 に M5×8 で外付け)
//
//   子機外装_改善要件 (2026-09-04) §3.2、コーディネータ 2026-09-04 決定 1/2/3 と
//   同日の取合い修正決定 (後ウェブ/デッキ/中央柱/キール再設計、ケース幅の変数
//   誤り、端板高さ) に基づく。`child_jaw_gate` の HP4/HP5 (共通座面 y=74.35、
//   法線 +Y、M5 熱圧入インサート×4 @ ±20 の HP40 規格) に左右各 4 本、計 8 本の
//   ボルトで留まる。輸送時はこの 8 本を外してブリッジごと取り外す (C7)。
//
//   荷重経路: ウイング −Z 荷重 → 後ウェブ (面内) → キール → 中央柱
//   (XZ 板、M_y に対し面内) → HP5/HP4。
//
//   機体座標: X 左右 (基線) / Y 前後 (+Y 前 = カメラ向き) / Z 上。
//   印刷向き: 中央柱を床にした +Y up。全板が印刷の垂直板になり、
//   −Z 荷重の曲げ引張が層面内 (面内許容 12MPa) に載る。
//
//   規約: cube/cylinder + boolean のみ (STEP を汚さない)。
// =====================================================================

/* [HP40 (child_jaw_gate 側, 2026-09-04 確定 — 二重定義: child_jaw_gate.scad)] */
hp4_z        = 170;    // HP4 (カメラブリッジ上) 座中心 z
hp5_z        = 100;    // HP5 (カメラブリッジ下) 座中心 z
hpl_z        = 15;     // HP-L (前向きライト) 座中心 z
hp_half      = 25;     // 座 (シェルフ) 半幅 (x, z とも) — child_jaw_gate.scad と同値
hp_seat_y    = 74.35;  // 座面 (共通平面)。法線 +Y — child_jaw_gate.scad の hp_seat_y
hp_shelf_dep = 12;     // シェルフ奥行き — child_jaw_gate.scad の hp_shelf_dep
hp_pitch_half = 20;    // M5 穴オフセット (hardpoint.scad HP_PITCH/2)
hp_bolt_d    = 5.4;    // M5 クリアランス (hardpoint.scad HP_BOLT_D)
adapter_t    = 6;      // 中央柱の板厚 (hardpoint.scad HP_ADAPTER_T)
gate_r_out   = 64.35;  // ゲート殻外径半径 (child_jaw_gate.scad r_out)

/* [child_cam_mount 側 (2026-09-04 確定 — 二重定義: child_cam_mount.scad)] */
cm_lens_off_bot = 42.05; // レジスタ面→レンズ軸 (cam_mount ローカル X)
cm_fin_x1       = 30;    // レジスタ面 = plate_t(8) + fin_len(22) (cam_mount ローカル X)
cm_case_d       = 45.9;  // ケース奥行 (Y、cam_mount の case_d)
cm_case_w       = 94.7;  // ケース幅 (横向きでは機体 X 方向、cam_mount の case_w)
cm_case_h       = 84.1;  // ケース高さ (縦=タブ軸方向、横向きでは機体 Z 方向)
cm_plate_hw     = 22;    // 背面プレート半幅 (cam_mount ローカル Y = 機体 Y)
cm_plate_hh     = 17;    // 背面プレート半高 (cam_mount ローカル Z = 機体 X オフセット)
cm_fh_y         = 16;    // フレーム穴 Y オフセット (cam_mount ローカル Y = 機体 Y)
cm_fh_z         = 11;    // フレーム穴 Z オフセット (cam_mount ローカル Z = 機体 X オフセット)

/* [カメラ配置 (2026-09-04 決定 1/2)] */
lens_z      = 125;   // レンズ中心 z (不変)
lens_x      = 75;    // レンズ中心 |x| (基線 150/2、不変)
cam_y_shift = 14;     // レンズを +Y へ前進 (決定 2)
lens_y      = 106 + cam_y_shift; // レンズ面 y = 120 (仮値、cam_mount 実測待ちで変動)

/* [デッキ (決定 1: lens_z=125 のまま、deck_top = lens_z - lens_off_bot - fin_x1)] */
deck_t   = 8;
deck_top = lens_z - cm_lens_off_bot - cm_fin_x1;  // 52.95
deck_bot = deck_top - deck_t;                     // 44.95
// 2026-09-04 再修正: デッキは中央も含め x -120..120 で連続 (旧設計は柱と
// ウイングが 1mm 程度の細片でしか繋がらず非連結だった)。
deck_x0  = -120;
deck_x1  = 120;
deck_y0  = 67;     // ゲート殻 (r64.35, x=0 で y64.35) から 2.65mm 離す
deck_y1  = lens_y + 4;            // 124 (レンズ面 +4 まで)

/* [中央柱: HP4/HP5 座 + 下方キールまで一体の XZ 板 (2026-09-04 再修正)] */
col_hw  = hp_half;                 // 25
col_y0  = hp_seat_y;                // 74.35
col_y1  = hp_seat_y + adapter_t;    // 80.35
col_z0  = deck_bot;                 // 44.95 (デッキ面まで下へ延長、キールと union)
col_z1  = hp4_z + hp_half;          // 195 (HP4 座上端)

/* [キール: 後ウェブ〜中央柱の面接合材] */
keel_hw = hp_half;                  // 25 (中央柱と同じ半幅)
keel_y0 = deck_y0;                  // 67 (デッキ後端と同じ)
keel_y1 = col_y1;                   // 80.35 (中央柱前面まで)
keel_z0 = deck_bot;                 // 44.95
keel_z1 = hp5_z - hp_half - 1;      // 74 (HP5 座下端 75 の 1mm 手前)

/* [ウイング: デッキ(連続) + 後ウェブ + 前ウェブ + 端板] */
wing_x0      = 22;     // 前ウェブ/端板の内端の基準 (デッキは連続なので不使用)
wing_x1      = 120;    // ウイング外端 x (= ブリッジ全幅/2 の上限)
rear_web_x0  = 27;     // 後ウェブ内端 (ゲート殻から 8.6mm、中央柱/キールの外へ)
rear_web_y0  = 67;     // = deck_y0 (キールと面接合)
rear_web_y1  = 73;     // t=6。ケース背面 74.1 の 1.1mm 手前
rear_web_z0  = deck_bot;   // 44.95
rear_web_z1  = 160;
front_web_y0 = lens_y + 2;   // 122 (レンズ面より 2mm 前)
front_web_y1 = lens_y + 8;   // 128 (t=6)
front_web_z0 = deck_bot;    // 44.95
front_web_z1 = 80;          // 2026-09-04 修正: 85→80 (ケース底面 82.95 の下、FOV 余裕も改善)
end_plate_t  = 6;            // ウイング外端 (x=wing_x1) を閉じる板 (X 法線)
end_plate_y0 = rear_web_y0;  // 67
end_plate_y1 = front_web_y1; // 128
end_plate_z0 = deck_bot;
end_plate_z1 = front_web_z1; // 80 (2026-09-04 修正: ケース底面 82.95 と干渉しない)

/* [マウント取付穴 (child_cam_mount 背面プレート M5×4 を横向きで受ける)] */
m5_clear = 5.4;
nut_af   = 8.2;    // M5 ナット 二面幅 +0.1
nut_dep  = 4.0;
mount_y0 = lens_y - cm_case_d / 2;         // 97.05 (レンズはケース中央にあると仮定)
mount_hole_y = [mount_y0 - cm_fh_y, mount_y0 + cm_fh_y]; // 81.05, 113.05
mount_hole_dx = cm_fh_z;                    // 11 (レンズ x からのオフセット)

/* [側面バンパ取合い (二重定義: child_side_bumper.scad)] */
bumper_t     = 9;
case_gap     = 2;               // ケース側面とバンパ内面のクリアランス
// 2026-09-04 修正: 横向きでは「ケース幅」が機体 X 方向なので case_w (94.7) を使う。
// 旧式 (lens_x + cm_case_h/2 = 117.05) は「高さ」を使っていた誤り。
case_outer_x = lens_x + cm_case_w / 2;  // 122.35
bump_bolt_y  = [80, 116];        // 端板フランジへの M5×2 (y 位置、両ファイルで同値)
bump_bolt_z  = 65;               // 端板フランジ z 中心。2026-09-04: z<=78 に収める (end_plate_z1=80 の 2mm 手前)

/* [ケース/マウント本体の干渉除外ボックス (2026-09-04 コーディネータ指示、総当り検査用)] */
case_x0   = lens_x - cm_case_w / 2;         // 27.65 (ケース内側端)
case_x1   = case_outer_x;                   // 122.35
case_y0   = mount_y0 - cm_case_d / 2;       // 74.1 (ケース背面)
case_y1   = lens_y;                         // 120 (ケース前面 = レンズ面)
case_z0   = deck_top + cm_fin_x1;           // 82.95 (register 面 = ケース底)
case_z1   = case_z0 + cm_case_h;            // 167.05 (ケース上端)
mp_x0     = lens_x - cm_plate_hh;           // 58
mp_x1     = lens_x + cm_plate_hh;           // 92
mp_y0     = mount_y0 - cm_plate_hw;         // 75.05
mp_y1     = mount_y0 + cm_plate_hw;         // 119.05
mp_z0     = deck_top;                       // 52.95
mp_z1     = case_z0;                        // 82.95 (プレート〜register 面〜ケース底までの全体を除外)
shelf_y0  = hp_seat_y - hp_shelf_dep;       // 62.35
shelf_y1  = hp_seat_y;                      // 74.35

/* [機体レベル検査] */
env_half = 140;   // 全幅 280 の半分 (C5)
hpl_top  = hpl_z + hp_half;   // 40 (HP-L 座上端)
fov_half = 77.5;  // 対角 FOV 155° の半角

/* [Hidden] */
fudge = 0.01;
$fn = 64;

// ---- 干渉・成立性チェック -------------------------------------------
// 決定 1: ブリッジ最下端は HP-L 座上端 (40) + 2mm
assert(deck_bot >= hpl_top + 2, "デッキ下端が HP-L 座 (z<=40) に 2mm 未満で接近");
assert(col_z1 <= 195, "ブリッジ最上端が 195 (HP4 座上端) を超える");
assert(rear_web_z1 <= 195, "後ウェブ上端が 195 を超える");
assert(wing_x1 <= 120, "ウイング先端が 240 枠 (半幅 120) を超える");
assert(deck_x1 <= wing_x1 && deck_x0 >= -wing_x1, "デッキが 240 枠を超える");
// デッキ/キールとゲート殻 (r64.35, x=0 で最接近) の離隔 (2026-09-04 修正: 67 に短縮)
gate_shell_y_at0 = gate_r_out;   // sqrt(r^2-0^2) = r
assert(deck_y0 - gate_shell_y_at0 >= 2.6, "デッキ後端がゲート殻 (x=0) に 2.6mm 未満で接近");
// 後ウェブ: ゲート殻から ≥8mm (2026-09-04 修正: x0=27)
gate_shell_y_at_rear = sqrt(gate_r_out * gate_r_out - rear_web_x0 * rear_web_x0);
assert(rear_web_y0 - gate_shell_y_at_rear >= 8,
       "後ウェブがゲート殻 (r64.35) に 8mm 未満で接近");
assert(rear_web_x0 >= wing_x0 - fudge, "後ウェブの内端がウイング開始点より内側にある");
// 後ウェブがケース背面 (case_y0) に食い込まない
assert(case_y0 - rear_web_y1 >= 1, "後ウェブがケース背面に 1mm 未満で接近/食い込む");
// キール: HP5 座下端 (75) と 1mm 以上、HP-L 座上端 (40) と 2mm 以上
assert((hp5_z - hp_half) - keel_z1 >= 1, "キール上端が HP5 座下端に 1mm 未満で接近");
assert(keel_z0 >= hpl_top + 2, "キール下端が HP-L 座に 2mm 未満で接近");
// マウント M5 穴がデッキ内に縁距離 >=3 で収まる
assert(mount_hole_y[0] - deck_y0 >= 3, "マウント穴 (後側) のデッキ縁距離 < 3mm");
assert(deck_y1 - mount_hole_y[1] >= 3, "マウント穴 (前側) のデッキ縁距離 < 3mm");
assert(front_web_y0 >= lens_y + 2, "前ウェブがレンズ面に 2mm 未満で接近");
assert(front_web_y1 <= 149, "前ウェブが奥行 250 枠 (前端 149) を超える");
assert(deck_y1 <= 149, "デッキが奥行 250 枠 (前端 149) を超える");
// 端板/前ウェブがケース底面 (case_z0=82.95) より下にあること (2026-09-04 修正)
assert(end_plate_z1 <= case_z0 - 1, "端板がケース底面に 1mm 未満で接近/食い込む");
assert(front_web_z1 <= case_z0 - 1, "前ウェブがケース底面に 1mm 未満で接近/食い込む");
// FOV: 前ウェブの最も干渉しやすい点 (x=lens_x 直下、z=front_web_z1、y=front_web_y1)
fov_dz = lens_z - front_web_z1;         // 45 (下方)
fov_dy = front_web_y1 - lens_y;         // 8  (前方)
fov_ang = atan(fov_dz / fov_dy);        // atan(45/8) ~= 79.9°
assert(fov_ang > fov_half, "前ウェブが FOV (対角半角 77.5°) の内側に入る");
// バンパ外面 <= 280 枠 (case_outer_x 修正後で再検査)
assert(case_outer_x + case_gap + bumper_t <= env_half,
       "側面バンパ外面が 280 枠を超える");
// バンパ締結穴が端板の高さ範囲内 (z<=78、端板 z1=80 の 2mm 手前)
assert(bump_bolt_z <= end_plate_z1 - 2, "バンパ締結穴が端板上端に 2mm 未満で接近");

// ---- (a)(b)(c) 総当り AABB 干渉検査 (2026-09-04 コーディネータ指示) --------
// box = [x0,x1,y0,y1,z0,z1]。厳密不等号なので面接触 (共有面) は非干渉扱い。
function box_overlap(a, b) =
    (a[0] < b[1]) && (b[0] < a[1]) &&
    (a[2] < b[3]) && (b[2] < a[3]) &&
    (a[4] < b[5]) && (b[4] < a[5]);

bridge_boxes = [
    ["deck",        [deck_x0, deck_x1, deck_y0, deck_y1, deck_bot, deck_top]],
    ["column",      [-col_hw, col_hw, col_y0, col_y1, col_z0, col_z1]],
    ["keel",        [-keel_hw, keel_hw, keel_y0, keel_y1, keel_z0, keel_z1]],
    ["rear_web_R",  [rear_web_x0, wing_x1, rear_web_y0, rear_web_y1, rear_web_z0, rear_web_z1]],
    ["rear_web_L",  [-wing_x1, -rear_web_x0, rear_web_y0, rear_web_y1, rear_web_z0, rear_web_z1]],
    ["front_web_R", [wing_x0, wing_x1, front_web_y0, front_web_y1, front_web_z0, front_web_z1]],
    ["front_web_L", [-wing_x1, -wing_x0, front_web_y0, front_web_y1, front_web_z0, front_web_z1]],
    ["end_plate_R", [wing_x1 - end_plate_t, wing_x1, end_plate_y0, end_plate_y1, end_plate_z0, end_plate_z1]],
    ["end_plate_L", [-wing_x1, -(wing_x1 - end_plate_t), end_plate_y0, end_plate_y1, end_plate_z0, end_plate_z1]],
];

keepout_boxes = [
    ["case_R",         [case_x0, case_x1, case_y0, case_y1, case_z0, case_z1]],
    ["case_L",         [-case_x1, -case_x0, case_y0, case_y1, case_z0, case_z1]],
    ["mount_plate_R",  [mp_x0, mp_x1, mp_y0, mp_y1, mp_z0, mp_z1]],
    ["mount_plate_L",  [-mp_x1, -mp_x0, mp_y0, mp_y1, mp_z0, mp_z1]],
    ["hp_shelf_HP4",   [-hp_half, hp_half, shelf_y0, shelf_y1, hp4_z - hp_half, hp4_z + hp_half]],
    ["hp_shelf_HP5",   [-hp_half, hp_half, shelf_y0, shelf_y1, hp5_z - hp_half, hp5_z + hp_half]],
    ["hp_shelf_HPL",   [-hp_half, hp_half, shelf_y0, shelf_y1, hpl_z - hp_half, hpl_z + hp_half]],
];

for (bb = bridge_boxes)
    for (kb = keepout_boxes)
        assert(!box_overlap(bb[1], kb[1]), str(bb[0], " が ", kb[0], " と交差する"));

echo(str("deck z ", deck_bot, " .. ", deck_top, " (deck_top = lens_z(", lens_z,
         ") - lens_off_bot(", cm_lens_off_bot, ") - fin_x1(", cm_fin_x1, "))"));
echo(str("lens_y = ", lens_y, " (cam_y_shift = ", cam_y_shift, ")"));
echo(str("FOV 半角 (前ウェブ) = ", fov_ang, "° (限界 ", fov_half, "°)"));
echo(str("ブリッジ半幅 = ", wing_x1, " (240 枠の半分 120)"));
echo(str("case_outer_x (修正後) = ", case_outer_x, " (旧誤値 lens_x+case_h/2=", lens_x + cm_case_h/2, ")"));

// ---- モジュール -----------------------------------------------------

// マウント M5 通し穴 + 下面ナットトラップ (垂直穴、軸 Z)
module mount_bolt(x, y) {
    translate([x, y, deck_bot - fudge])
        cylinder(d = m5_clear, h = deck_t + 2 * fudge, $fn = 32);
    translate([x, y, deck_bot - fudge])
        cylinder(d = nut_af / cos(30), h = nut_dep + fudge, $fn = 6);
    translate([x, y, deck_bot + nut_dep - fudge])
        cylinder(d1 = nut_af / cos(30), d2 = m5_clear,
                 h = (nut_af / cos(30) - m5_clear) / 2 + fudge, $fn = 32);
}

// バンパ締結: 端板フランジ側のナットトラップ (水平穴、軸 X、開口 = 端板外面
// x=sign*wing_x1、そこからナットぶん nut_dep だけ内側へ)。
// 2026-09-04 修正: 旧コードは h = wing_x1-end_plate_t-nut_dep (=110mm!) という
// ミスで端板の厚さ (6mm) を大きく超えてウイング中央近くまで穴が貫通していた
// (ビルドは通っていたが意図しない長孔だった)。端板厚 (end_plate_t) の範囲内に
// 収まるよう修正: クリアランス穴は端板を貫通する end_plate_t のみ、
// ナットトラップは外面から nut_dep のみ。
module bump_nut(sign, y) {
    ang = -90 * sign;   // 右 (sign=+1): 局所+Z→機体−X (内向き)。左は符号反転で+X (内向き)
    translate([sign * (wing_x1 + fudge), y, bump_bolt_z])
        rotate([0, ang, 0])
            cylinder(d = m5_clear, h = end_plate_t + 2 * fudge, $fn = 32);
    translate([sign * (wing_x1 + fudge), y, bump_bolt_z])
        rotate([0, ang, 0])
            cylinder(d = nut_af / cos(30), h = nut_dep + fudge, $fn = 6);
}

// 中央柱の M5×8 (HP4/HP5 各 4 本、軸 Y)
module column_bolt(x, z) {
    translate([x, col_y0 - fudge, z])
        rotate([-90, 0, 0])
            cylinder(d = hp_bolt_d, h = adapter_t + 2 * fudge, $fn = 32);
}

module column_holes() {
    for (hz = [hp4_z, hp5_z], sx = [-1, 1], sz = [-1, 1])
        column_bolt(sx * hp_pitch_half, hz + sz * hp_pitch_half);
}

// 中央柱 (キールと union するデッキ面までの XZ 板。穴は含まない)
module column_solid() {
    translate([-col_hw, col_y0, col_z0])
        cube([2 * col_hw, col_y1 - col_y0, col_z1 - col_z0]);
}

// キール
module keel_solid() {
    translate([-keel_hw, keel_y0, keel_z0])
        cube([2 * keel_hw, keel_y1 - keel_y0, keel_z1 - keel_z0]);
}

// デッキ (連続)
module deck_solid() {
    translate([deck_x0, deck_y0, deck_bot])
        cube([deck_x1 - deck_x0, deck_y1 - deck_y0, deck_t]);
}

// 片側ウイング・本体 (sign = +1 右 / -1 左)。デッキ/柱/キールは含まない。
module wing_webs_solid(sign) {
    // 後ウェブ
    rw_xlo = min(sign * rear_web_x0, sign * wing_x1);
    rw_xhi = max(sign * rear_web_x0, sign * wing_x1);
    translate([rw_xlo, rear_web_y0, rear_web_z0])
        cube([rw_xhi - rw_xlo, rear_web_y1 - rear_web_y0, rear_web_z1 - rear_web_z0]);
    // 前ウェブ
    fw_xlo = min(sign * wing_x0, sign * wing_x1);
    fw_xhi = max(sign * wing_x0, sign * wing_x1);
    translate([fw_xlo, front_web_y0, front_web_z0])
        cube([fw_xhi - fw_xlo, front_web_y1 - front_web_y0, front_web_z1 - front_web_z0]);
    // 端板
    translate([sign > 0 ? wing_x1 - end_plate_t : -wing_x1, end_plate_y0, end_plate_z0])
        cube([end_plate_t, end_plate_y1 - end_plate_y0, end_plate_z1 - end_plate_z0]);
}

// 片側ウイング・穴 (マウント M5×4 + バンパ用ナットトラップ×2)
module wing_holes(sign) {
    for (dx = [-mount_hole_dx, mount_hole_dx], y = mount_hole_y)
        mount_bolt(sign * lens_x + dx, y);
    for (y = bump_bolt_y)
        bump_nut(sign, y);
}

// ---- 形状 -----------------------------------------------------------
difference() {
    union() {
        deck_solid();
        column_solid();
        keel_solid();
        wing_webs_solid(1);
        wing_webs_solid(-1);
    }
    column_holes();
    wing_holes(1);
    wing_holes(-1);
}
