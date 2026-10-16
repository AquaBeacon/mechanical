// =====================================================================
// parent_float_cradle.scad — 親機 浮子クレードル (円筒フェンダー受け、左右共通)
//
// 役割: 市販円筒フェンダー (parent_fender、仮 Ø100 × 300) を上から被せて保持し、
//   parent_deck の側壁 HP40 座 ×2 に内壁 (アダプタ板) で M5×4 ×2 締結する。
//   - 3 枚のアーチリブ (両端 + 中央) が胴を受ける (紐が無くても落ちない ±80° の抱え込み)
//   - 紐穴: 両端リブ Ø7 ×2 (Y 貫通、胴の両脇) = 胴を下から回す掛け紐
//           外壁側の両端ラグ Ø8 (Y 貫通) = 浮子端アイ → ラグ / デッキ側壁の紐穴 へのブライドル
//   - 天板中央に HP40 座 ×1 (上向き) = ライト・GPS ポール等の拡張
//   - 左右は同一部品 (Y 対称なので 180° 回して反対側に付く)
//
// 座標系: X=0 = デッキ側壁の外面 (座面)、外向き +X。Y = 浮子軸。z=0 = デッキ上面。
// 印刷向き: **上下反転** (天板をベッドに)。リブのアーチは上に行くほど狭まる形なので
//   オーバーハング無し。PETG / 壁 4 / インフィル 25% / サポート不要。
// 規約: cube / cylinder / polygon + ブーリアンのみ。
// =====================================================================

use <../../../../../scad/lib/hardpoint.scad>

/* [浮子 (parent_fender.scad と二重定義 — 実測後に両方直す)] */
fender_d     = 100;
fender_len   = 300;
fender_clear = 3;      // 胴とアーチの片側隙間

/* [デッキ側 (parent_deck.scad と二重定義)] */
hp_lip_y     = [-70, 70];   // デッキ側壁の HP40 座中心 Y
hp_lip_z     = -25;         // 同 z
deck_lip_h   = 50;          // デッキ側壁の高さ

/* [内壁 = HP40 アダプタ板] */
wall_in_t    = 8;      // 板厚 (HP_ADAPTER_T 6 より厚く: 引張はこの板の面内)
wall_gap     = 6;      // 内壁外面と胴の隙間 (掛け紐 Ø5 の通り代)

/* [天板・リブ・外壁] */
top_t        = 5;
cradle_len   = 200;    // Y 全長 (浮子 300 の中央 200 を抱える)
rib_t        = 8;
rib_y        = [-96, 0, 96];   // リブ中心 Y
rib_h        = 60;     // リブ高さ (z -60..0)
wall_out_t   = 9;
wall_out_gap = 2;      // アーチ半径と外壁内面の隙間 (0 だと薄片が出る)

/* [天板 HP40 座 (上向き)] */
top_pad_boss = 10;     // 天板下のボス厚 (インサート 9 深)
arc_gap      = 2;      // アーチ頂点とボス下面の間に残す肉

/* [紐穴] */
cord_d       = 7;      // 端リブの掛け紐穴
cord_dx      = 46;     // 胴中心からの X オフセット (±)
cord_z       = -12;
lug_d        = 8;      // 外側ラグの穴
lug_w        = 20;
lug_drop     = 26;     // リブ下端からの垂れ (ラグ高さ)

/* [HP40 (hardpoint.scad と二重定義)] */
hp_pitch     = 40;
hp_bolt_d    = 5.4;
hp_ins_d     = 6.4;
hp_ins_h     = 8;
hp_pad       = 50;
hp_cable_d   = 14;

$fn = 96;

// ---- 導出 -----------------------------------------------------------
arc_r    = fender_d/2 + fender_clear;                 // 53
x_f      = wall_in_t + wall_gap + fender_d/2;         // 64 (胴中心 X)
z_c      = -(top_t + top_pad_boss + arc_gap) - arc_r;            // -70 (胴中心 z)。胴上面 = -20
x_out0   = x_f + arc_r + wall_out_gap;                // 119 (外壁内面)
x_out1   = x_out0 + wall_out_t;                       // 128 (外壁外面)
x_lug0   = x_out0 - 2;                                // ラグ X 範囲 (外壁の足を広げる)
x_lug1   = x_lug0 + lug_w;
z_rib0   = -rib_h;                                    // -60
lug_z    = z_rib0 - lug_drop/2;                       // ラグ穴 z (-73)
chord_half = sqrt(arc_r*arc_r - pow(z_rib0 - z_c, 2)); // リブ下端でのアーチ半幅 (52.4)

// ---- 成立性チェック --------------------------------------------------
assert(z_c + arc_r <= -(top_t + top_pad_boss) - 0.01, "胴上面 (アーチ頂点) が天板ボスに当たる");
assert(x_f - fender_d/2 >= wall_in_t + wall_gap - 0.01, "胴が内壁に当たる");
assert(x_f - arc_r > wall_in_t + 1, "アーチが内壁を削る");
assert(z_rib0 > z_c, "リブ下端が胴中心より下 (差し込めない)");
assert(chord_half < x_f - wall_in_t - 2, "リブ下端でアーチが内壁の足を残さない");
assert(x_out0 - (x_f + chord_half) >= 2, "リブ下端でアーチが外壁の足を残さない");
// 内壁 HP40 アダプタ: 穴が内壁に収まる / デッキ側壁の座と同じ位置
for (y = hp_lip_y) {
    assert(abs(y) + hp_pad/2 <= cradle_len/2, "HP40 アダプタ穴が内壁の Y 範囲外");
    assert(hp_lip_z - hp_pad/2 >= z_rib0 && hp_lip_z + hp_pad/2 <= 0, "HP40 アダプタ穴が内壁の高さ範囲外");
}
assert(deck_lip_h <= rib_h, "デッキ側壁がクレードル内壁より高い (座面が合わない)");
// 端リブの掛け紐穴: 天板・アーチ・ボスから離れる
cord_arc_z = z_c + sqrt(arc_r*arc_r - cord_dx*cord_dx);
assert(cord_z + cord_d/2 <= -top_t - 3, "掛け紐穴が天板に近すぎる");
assert(cord_z - cord_d/2 >= cord_arc_z + 3, str("掛け紐穴がアーチに近すぎる: ", cord_z - cord_d/2 - cord_arc_z));
assert(cord_dx - cord_d/2 > hp_pad/2 + 2, "掛け紐穴が天板ボスの真下");
assert(x_f - cord_dx - cord_d/2 > wall_in_t + 2 && x_f + cord_dx + cord_d/2 < x_out0 - 2, "掛け紐穴が壁に掛かる");
// 外側ラグ: 胴 (X > x_f - fender_d/2 .. x_f + fender_d/2) に当たらない / 穴の端距離
assert(x_lug0 >= x_f + fender_d/2 + 2, "ラグが胴に当たる");
assert(lug_w >= lug_d + 2*5, "ラグの穴端距離不足 (片側 5 以上)");
assert(lug_drop >= lug_d + 2*4, "ラグの垂れが穴に対して短い");
// 中央リブと天板ボス・ケーブル穴: リブは cable 穴で切れる (天板が繋ぐ) — 意図どおり。中央リブが座の中にあること
assert(len([for (y = rib_y) if (abs(y) < 0.01) y]) == 1, "中央リブが Y=0 に無い (天板ボスの支え)");
// 250³ 造形枠
assert(x_lug1 <= 250 && cradle_len <= 250 && rib_h + lug_drop <= 250, "X1C 250 枠を超える");
// 抱え込み角 (リブ下端でのアーチの半角) — 紐なしでも落ちない目安 ≥ 70°
wrap_half_deg = 90 - asin((z_rib0 - z_c) / arc_r);
assert(wrap_half_deg >= 70, str("抱え込み角が浅い: ", wrap_half_deg));
echo(str("parent_float_cradle: fender centre X=", x_f, " (global ", 108 + x_f, ") z=", z_c,
         " arc_r=", arc_r, " wrap half-angle at rib foot=", 90 - asin((z_rib0 - z_c)/arc_r), " deg"));
echo(str("parent_float_cradle: HOLETABLE hp40_adapter(face x=0)=", [for (y = hp_lip_y, sy=[-1,1], sz=[-1,1]) [0, y + sy*hp_pitch/2, hp_lip_z + sz*hp_pitch/2]],
         " hp40_top(face z=0)=", [[x_f, 0, 0]],
         " cord(dia ", cord_d, ")=", [for (s=[-1,1], t=[-1,1]) [x_f + s*cord_dx, t*rib_y[2], cord_z]],
         " lug(dia ", lug_d, ")=", [for (t=[-1,1]) [(x_lug0 + x_lug1)/2, t*rib_y[2], lug_z]]));
echo(str("parent_float_cradle: bbox ", x_lug1, " x ", cradle_len, " x ", rib_h + lug_drop));

// ---- 本体 -------------------------------------------------------------
difference() {
    union() {
        // 天板
        translate([0, -cradle_len/2, -top_t]) cube([x_out1, cradle_len, top_t]);
        // 内壁 (HP40 アダプタ板)
        translate([0, -cradle_len/2, z_rib0]) cube([wall_in_t, cradle_len, rib_h]);
        // 外壁
        translate([x_out0, -cradle_len/2, z_rib0]) cube([wall_out_t, cradle_len, rib_h]);
        // リブ ×3
        for (y = rib_y)
            translate([0, y - rib_t/2, z_rib0]) cube([x_out1, rib_t, rib_h]);
        // 天板 HP40 ボス
        translate([x_f - hp_pad/2, -hp_pad/2, -top_t - top_pad_boss]) cube([hp_pad, hp_pad, top_pad_boss]);
        // 外側ラグ ×2 (両端リブの外壁側の足を下へ伸ばす)
        for (t = [-1, 1])
            translate([x_lug0, t*rib_y[2] - rib_t/2, z_rib0 - lug_drop]) cube([lug_w, rib_t, lug_drop + 1]);
    }
    // 浮子のアーチ (胴 + 隙間) を Y 全長で抜く
    translate([x_f, 0, z_c]) rotate([90, 0, 0]) cylinder(r = arc_r, h = cradle_len + 2, center = true);
    // 内壁 HP40 アダプタ穴 ×2 (M5 バカ穴 ×4 + 中央 Ø14)、X 貫通
    for (y = hp_lip_y) {
        for (sy = [-1, 1]) for (sz = [-1, 1])
            translate([-1, y + sy*hp_pitch/2, hp_lip_z + sz*hp_pitch/2]) rotate([0, 90, 0])
                cylinder(d = hp_bolt_d, h = wall_in_t + 2);
        translate([-1, y, hp_lip_z]) rotate([0, 90, 0]) cylinder(d = hp_cable_d, h = wall_in_t + 2);
    }
    // 天板 HP40 座 (上向き)
    translate([x_f, 0, 0]) {
        hp40_cut(cable = true, through_t = top_t + top_pad_boss + 2, insert_h = hp_ins_h);
        hp40_arrow();
    }
    // 端リブの掛け紐穴 ×4 (Y 貫通)
    for (t = [-1, 1]) for (s = [-1, 1])
        translate([x_f + s*cord_dx, t*rib_y[2], cord_z]) rotate([90, 0, 0])
            cylinder(d = cord_d, h = rib_t + 2, center = true);
    // 外側ラグ穴 ×2 (Y 貫通)
    for (t = [-1, 1])
        translate([(x_lug0 + x_lug1)/2, t*rib_y[2], lug_z]) rotate([90, 0, 0])
            cylinder(d = lug_d, h = rib_t + 2, center = true);
}
