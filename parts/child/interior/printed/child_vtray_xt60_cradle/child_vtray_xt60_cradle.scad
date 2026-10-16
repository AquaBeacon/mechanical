// =====================================================================
// child_vtray_xt60_cradle.scad — 子機 縦置き内装 電池リード硬直部 (XT60) クレードル
//
// 電池 (lipo_35x26x110) の電源リードは「可撓 60mm → 硬直 50mm → XT60 プラグ」で、
// 硬直部と XT60 嵌合ペア (parts/child/interior/cots/xt60_rigid_run、8.2 x 15.6 x 95)
// は曲げられない。この直線 95mm を、デッキ下面の +X 側 (電池箱の外壁と
// アクリル内壁の間) に **Z 方向 (チューブ軸) に沿って** 収めるのがこの部品。
//
// 断面 (X 右 / Y 上 = デッキ側):
//
//     デッキ下面 y=-10 ─────────────────────────────────────
//     [電池箱の耳]  ┃   天板 (plate)  x 27.5..44                ┃
//     電池箱外壁    ┃ 硬直部ポケット ┃ 外壁 ┃ ハーネス溝 ┃ リップ ┃
//     x=22          ┃ x 22..30.6     ┃30.6..┃ 33..41     ┃41..43 ┃ y -19
//                   ┃ y -14.5..-30.5 ┃ 33   ┃(結束スロット付き)
//                   ┗━━━━ 棚 (ledge) y -30.5..-33.5 ━━┛
//
//   ・ポケットの −X 側の面は **電池箱の外壁 (x=22)** が受ける (この部品には無い)。
//   ・硬直部は上 (+Z) から RX 基板を付ける前に差し込み、下端タブ (tab) に載る。
//     上端は結束バンド 1 本 (外壁の Ø3.2 穴 2 個に通し、端面の前を横切らせる) で止める。
//   ・ハーネス溝: 旧 +X ケーブルレールの代わり。Ø6 までのケーブルをリップの
//     結束スロット (2 個 1 組) で結束する。
//   ・デッキへの固定は旧 +X レールと同じ 4 穴 (x 30.3 / 41.7, 世界 z 37 / 77) を使い、
//     デッキ上面から M3×8 で天板にセルフタップする (M3×10 だと先端がポケットに出る)。
//
// 座標: X, Y は child_vtray_deck と同じ世界座標。Z はこの部品の下端 (世界 z = cradle_z0) を 0。
//
// 印刷向き: **Z を上に立てて印刷** (下端タブがベッド)。板はすべて垂直でサポート不要。
//           足場が 22 x 24 mm で高さ 102 なので **ブリム 8mm 以上**。
// =====================================================================

/* [容器 (干渉検査用。deck と同じ値にすること)] */
tube_id    = 101.6;
wall_clear = 2.5;

/* [取合い (child_vtray_deck / child_vtray_batt_box と一致させること)] */
deck_y0    = -10;     // デッキ下面 Y
deck_t     = 4;       // デッキ板厚
box_out_x  = 22;      // 電池箱外壁の X (= ポケットの −X 面)
box_ear_x  = 27;      // 電池箱 +X 耳の外端 X
rail_hx    = [30.3, 41.7];  // デッキの旧レール用 Ø3.4 穴 X (deck: rail_x ± rail_hx)
rail_hz    = [37, 77];      // 同 世界 Z
cradle_z0  = 27;      // この部品の下端の世界 Z
rx_z0      = 134;     // RX 基板 (デッキ下面) の Z 始点
screw_l    = 8;       // 固定ねじ M3×8 (デッキ 4 + 天板 4)

/* [硬直部 (parts/child/interior/cots/xt60_rigid_run と一致させること)] */
run_w      = 8.2;     // X
run_h      = 15.6;    // Y
run_l      = 95;      // Z
run_clear  = 0.4;     // ポケットの遊び (X, Y とも)
gap_box    = 0.3;     // 電池箱外壁との隙間 (部品同士を密着させない)

/* [板厚] */
plate_t    = 4.5;     // 天板 (ねじが 4mm かかる)
owall_t    = 2.4;     // ポケット外壁
ledge_t    = 3;       // 棚
tab_t      = 3;       // 下端タブ (硬直部の軸方向の座)
lip_t      = 2;       // ハーネス溝の外リップ (X)
lip_h      = 4.5;     // 同 高さ (Y)
duct_w     = 8;       // ハーネス溝の幅 (X)
plate_x1   = 44;      // 天板の外端 X

/* [結束・ストッパ] */
tie_z      = [16, 51, 86];   // 結束スロット組の中心 Z (組内 2 個は tie_gap 離す)
tie_gap    = 6;
tie_slot_z = 2.2;
tie_slot_h = 3.0;     // Y 方向の長さ
stop_d     = 3.2;     // 上端ストッパ用 結束バンド穴Ø
stop_y     = [-17, -28];
notch_w    = 7;       // 下端タブの可撓リード通し (硬直部の下から出る 2 本)
notch_h    = 11;

$fn = 48;

// ---- 導出 -------------------------------------------------------------
r_use     = tube_id/2 - wall_clear;
pocket_x0 = box_out_x + gap_box;             // 22.3 (部品の −X 端)
pocket_x1 = box_out_x + run_w + run_clear;   // 30.6 (硬直部が入る幅は箱外壁から測る)
owall_x1  = pocket_x1 + owall_t;             // 33.0
duct_x1   = owall_x1 + duct_w;               // 41.0
lip_x1    = duct_x1 + lip_t;                 // 43.0
plate_x0  = box_ear_x + 0.5;                 // 27.5
plate_y1  = deck_y0 - plate_t;               // -14.5 (ポケット上面)
pocket_y1 = plate_y1 - (run_h + run_clear);  // -30.5 (棚上面)
ledge_y0  = pocket_y1 - ledge_t;             // -33.5
lip_y0    = plate_y1 - lip_h;                // -19
cradle_len = tab_t + run_l + 4;              // 102: タブ + 硬直部 + ストッパ帯
stop_z    = tab_t + run_l + 1.6;             // 結束バンド穴の Z (端面から 1mm 上)
run_center = [(box_out_x + pocket_x1)/2, (plate_y1 + pocket_y1)/2];   // 硬直部の中心 (26.3, -22.5)
screw_tip_y = deck_y0 - (screw_l - deck_t);  // M3×8 の先端 Y = -14

function rad(x, y) = sqrt(x*x + y*y);

// ---- 干渉・成立性チェック ---------------------------------------------
assert(rad(owall_x1, ledge_y0) <= r_use, str("棚の外側下角がチューブに接触 r=", rad(owall_x1, ledge_y0)));
assert(rad(lip_x1, lip_y0) <= r_use, str("ハーネス溝リップがチューブに接触 r=", rad(lip_x1, lip_y0)));
assert(rad(plate_x1, plate_y1) <= r_use, str("天板の外端がチューブに接触 r=", rad(plate_x1, plate_y1)));
assert(plate_x1 >= lip_x1, "天板がリップより短い");
assert(plate_x0 > box_ear_x, "天板が電池箱の耳に当たる");
assert(plate_x0 < pocket_x1 - 2, "天板が硬直部の上を 2mm 以上覆っていない (硬直部が上へ逃げる)");
// ねじ: 天板の中にあり、先端がポケットに出ないこと
for (x = rail_hx) {
    assert(x - 1.7 > plate_x0 && x + 1.7 < plate_x1, str("固定ねじ X=", x, " が天板の外"));
}
assert(screw_tip_y >= plate_y1, str("固定ねじ先端 y=", screw_tip_y, " がポケット (", plate_y1, ") に出る → 短いねじにする"));
for (z = rail_hz) assert(z - cradle_z0 > 3 && z - cradle_z0 < cradle_len - 3, str("固定ねじ Z=", z, " が部品の外"));
// 硬直部
assert(pocket_x1 - box_out_x >= run_w + run_clear - 0.01, "ポケット幅が硬直部より狭い");
assert(plate_y1 - pocket_y1 >= run_h + run_clear - 0.01, "ポケット高さが硬直部より低い");
assert(stop_z > tab_t + run_l + 0.5 && stop_z + stop_d/2 < cradle_len, "ストッパ穴が硬直部の端面に重なる/部品の外");
for (y = stop_y) assert(y - stop_d/2 > pocket_y1 && y + stop_d/2 < plate_y1, "ストッパ穴がポケットの外");
assert(cradle_z0 + cradle_len + 5 <= rx_z0, str("クレードル上端 ", cradle_z0 + cradle_len, " が RX 基板 ", rx_z0, " に近すぎる"));
// 結束スロットがリップの中に収まること
for (zc = tie_z) for (dz = [-tie_gap/2, tie_gap/2])
    assert(zc + dz - tie_slot_z/2 > tab_t && zc + dz + tie_slot_z/2 < cradle_len,
           str("結束スロット Z=", zc + dz, " がリップの外"));
assert(tie_slot_h < lip_h - 1, "結束スロットがリップより高い");
assert(notch_w < pocket_x1 - box_out_x - 1 && notch_h < plate_y1 - pocket_y1 - 2, "タブの切欠きが大きすぎる");

// ---- 本体 -------------------------------------------------------------
difference() {
    union() {
        // 天板 (デッキ下面に密着。ねじ受け)
        translate([plate_x0, plate_y1, 0]) cube([plate_x1 - plate_x0, plate_t, cradle_len]);
        // ポケット外壁
        translate([pocket_x1, ledge_y0, 0]) cube([owall_t, plate_y1 - ledge_y0, cradle_len]);
        // 棚 (硬直部の −Y 側の座。箱外壁の手前まで)
        translate([pocket_x0, ledge_y0, 0]) cube([owall_x1 - pocket_x0, ledge_t, cradle_len]);
        // ハーネス溝の外リップ
        translate([duct_x1, lip_y0, 0]) cube([lip_t, plate_y1 - lip_y0 + 0.01, cradle_len]);
        // 下端タブ (硬直部の座。ポケット断面を塞ぐ)
        translate([pocket_x0, pocket_y1, 0]) cube([owall_x1 - pocket_x0, plate_y1 - pocket_y1 + 0.01, tab_t]);
    }
    // 固定ねじ M3 セルフタップ下穴 (デッキ側から)
    for (x = rail_hx) for (z = rail_hz)
        translate([x, deck_y0 + 0.5, z - cradle_z0]) rotate([90, 0, 0]) cylinder(d = 2.8, h = plate_t + 1, $fn = 24);
    // 下端タブの可撓リード通し
    translate([run_center[0] - notch_w/2, run_center[1] - notch_h/2, -0.5]) cube([notch_w, notch_h, tab_t + 1]);
    // 上端ストッパ: 結束バンドを通す穴 ×2 (外壁を X 方向に貫通)
    for (y = stop_y)
        translate([pocket_x1 - 0.5, y, stop_z]) rotate([0, 90, 0]) cylinder(d = stop_d, h = owall_t + 1, $fn = 24);
    // ハーネス結束スロット (リップを X 方向に貫通、2 個 1 組)
    for (zc = tie_z) for (dz = [-tie_gap/2, tie_gap/2])
        translate([duct_x1 - 0.5, lip_y0 + 0.75, zc + dz - tie_slot_z/2])
            cube([lip_t + 1, tie_slot_h, tie_slot_z]);
}

echo(str("child_vtray_xt60_cradle: 世界 z ", cradle_z0, "..", cradle_z0 + cradle_len,
         " / ポケット x ", box_out_x, "..", pocket_x1, " y ", pocket_y1, "..", plate_y1,
         " (硬直部中心 ", run_center, ", 世界 z ", cradle_z0 + tab_t, "..", cradle_z0 + tab_t + run_l, ")",
         " / ハーネス溝 x ", owall_x1, "..", duct_x1,
         "  最小チューブすきま=", tube_id/2 - max(rad(owall_x1, ledge_y0), rad(lip_x1, lip_y0), rad(plate_x1, plate_y1))));
