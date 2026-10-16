// =====================================================================
// child_clamp_strap.scad — 子機チューブクランプ 上ストラップ (2個印刷)
// child_clamp_base に M4×2 で締結する上側半リング。
// クランプ面には薄ゴム/EVAシートを貼り、締め代はシート圧縮で確保。
// 印刷向き: 平置き(リング面を下)。 M4穴は垂直で綺麗に出る。
// =====================================================================

/* [チューブ (実測値) — child_clamp_base と一致させる] */
tube_od    = 114.3;
fit_clear  = 0.5;

/* [ストラップ] */
band_t     = 8;       // バンド肉厚(半径方向)
band_w     = 26;      // バンド幅(チューブ軸方向) = base saddle_d
m4_x       = 78;      // M4位置(±) = base と一致
m4_d       = 4.5;     // M4クリアランス
head_d     = 8.5;     // M4ナベ/キャップ頭径+余裕 (座グリ)
head_t     = 4.5;     // 座グリ深さ

$fn = 96;

// ---- 導出 -----------------------------------------------------------
tube_r  = (tube_od + fit_clear) / 2;   // 57.4
r_out   = tube_r + band_t;             // 65.4
// ベースブロック上面はチューブ中心から block_h - center_z = -5.4 (base側と整合)
chord_z = -5.4;                        // 耳の下面高さ(チューブ中心基準)
ear_w   = 24;
ear_t   = chord_z + 12;                // 耳上面 z=+6.6 → 耳厚12

// ---- チェック ---------------------------------------------------------
assert(m4_x - m4_d/2 > r_out + 2, "M4穴がリング外周と干渉");
assert(m4_x - head_d/2 > r_out + 0.5, "M4座グリがリング外周と干渉");
half_at_ear = sqrt(tube_r*tube_r - chord_z*chord_z);
assert(m4_x + ear_w/2 > half_at_ear, "耳がチューブ断面より内側");

// ---- 本体 -------------------------------------------------------------
// 2D: x=水平, y=組立時の上下(チューブ中心=原点)。Z にバンド幅を押し出す。
// 印刷はこの向きのまま平置き。M4は押し出し後に y 軸方向の真円で開ける。
difference() {
    linear_extrude(height = band_w)
        union() {
            // 上半リング (chord_z より上)
            intersection() {
                difference() { circle(r = r_out); circle(r = tube_r); }
                translate([-m4_x - ear_w/2, chord_z])
                    square([2*(m4_x + ear_w/2), r_out - chord_z + 1]);
            }
            // 左右の耳 (ベースのボルト柱上面に載る)。リング外周(r_out)と
            // 必ず重なるよう内側エッジをチューブ半径+0.5まで伸ばす。
            for (sx=[-1,1]) mirror([sx < 0 ? 1 : 0, 0, 0])
                translate([tube_r + 0.5, chord_z])
                    square([m4_x + ear_w/2 - tube_r - 0.5, 12]);
        }
    // M4 貫通穴 + 頭座グリ (組立時の垂直 = 2D y 方向)
    for (sx=[-1,1]) {
        translate([sx*m4_x, chord_z - 1, band_w/2])
            rotate([-90, 0, 0]) cylinder(d = m4_d, h = 14 + 2);
        translate([sx*m4_x, chord_z + 12 - head_t, band_w/2])
            rotate([-90, 0, 0]) cylinder(d = head_d, h = head_t + 1);
    }
}
