// =====================================================================
// child_clamp_base.scad — 子機 耐圧チューブ クランプ ベース (2個印刷)
// BlueRobotics WTE4 4"チューブ(実測OD114.3)を下から受けるサドル。
// child_clamp_strap(上バンド)と左右の M4 ボルトで締結し、
// ベース底面の M5×4 で child_frame_plate に固定する。
// チューブ保護に薄ゴム/EVAシートをサドル面に貼ること。
// 印刷向き: このまま(底面が下)。サドル曲面は上向きでサポート不要。
// =====================================================================

/* [チューブ (実測値)] */
tube_od    = 114.3;   // チューブ実測OD
fit_clear  = 0.5;     // 径クリアランス(保護シート厚を含めて調整)

/* [ベース] */
plate_w    = 180;     // 底板幅 (X, チューブ直交)
plate_d    = 54;      // 底板奥行 (Y, チューブ軸方向)
plate_t    = 8;       // 底板厚
block_w    = 132;     // サドルブロック幅
block_h    = 60;      // サドルブロック上面高さ (底面基準)
saddle_d   = 26;      // サドル幅 (Y)

/* [締結] */
m5_x       = 80;      // フレームプレートへのM5位置(±) ※20mmグリッド上
m5_y       = 20;      // 同(±) ※ボルト柱(y±13)の外側に置くこと
m5_d       = 5.3;     // M5クリアランス
ear_w      = 24;      // ストラップボルト柱 幅
m4_x       = 78;      // ストラップM4位置(±)
m4_d       = 4.5;     // M4クリアランス
nut_w      = 7.8;     // M4ナット二面幅+余裕
nut_t      = 3.6;     // ナットスロット厚
nut_z      = 38;      // ナットスロット高さ

$fn = 96;

// ---- 導出 -----------------------------------------------------------
tube_r   = (tube_od + fit_clear) / 2;        // 57.4
center_z = plate_t + tube_r;                 // チューブ軸心高さ = サドル底が底板上面
half_top = sqrt(tube_r*tube_r - pow(center_z - block_h, 2)); // ブロック上面での切り欠き半幅

// ---- 干渉・成立性チェック --------------------------------------------
assert(block_w/2 > half_top + 6,
       str("ブロック上端の壁厚不足: 必要 ", half_top + 6, " 実際 ", block_w/2));
assert(m4_x - m4_d/2 > block_w/2 + 2, "M4ボルトがサドルブロックと干渉");
assert(m4_x + ear_w/2 <= plate_w/2, "ボルト柱が底板からはみ出し");
assert(m5_y - 4.5 >= saddle_d/2,
       "M5頭(Ø8.5+余裕)がサドル/ボルト柱と干渉: m5_y を外へ");
assert(plate_d/2 - m5_y - m5_d/2 >= 4, "M5穴の端距離不足(Y)");
assert(plate_w/2 - m5_x - m5_d/2 >= 4, "M5穴の端距離不足(X)");

// ---- 本体 -------------------------------------------------------------
difference() {
    union() {
        // 底板
        translate([-plate_w/2, -plate_d/2, 0]) cube([plate_w, plate_d, plate_t]);
        // サドルブロック
        translate([-block_w/2, -saddle_d/2, plate_t])
            cube([block_w, saddle_d, block_h - plate_t]);
        // ストラップボルト柱 (左右フルハイト)。ボルトは上から通し、
        // ナットは側面スロットから挿入するナットトラップで保持。
        for (sx=[-1,1])
            translate([sx*m4_x - ear_w/2, -saddle_d/2, plate_t])
                cube([ear_w, saddle_d, block_h - plate_t]);
    }
    // サドル (チューブ断面)
    translate([0, -saddle_d/2 - 1, center_z])
        rotate([-90, 0, 0]) cylinder(r=tube_r, h=saddle_d + 2);
    // フレームプレートへの M5 ×4
    for (sx=[-1,1]) for (sy=[-1,1])
        translate([sx*m5_x, sy*m5_y, -0.5]) cylinder(d=m5_d, h=plate_t + 1);
    // ストラップ M4 ×2 (上から) + 外側面から横挿しのナットトラップ
    for (sx=[-1,1]) mirror([sx < 0 ? 1 : 0, 0, 0])
        translate([m4_x, 0, 0]) {
            translate([0, 0, nut_z - 6]) cylinder(d=m4_d, h=block_h);  // ボルト穴
            translate([-4.5, -nut_w/2, nut_z])                          // ナットスロット
                cube([plate_w/2 - m4_x + 4.5 + 1, nut_w, nut_t]);
        }
}

echo(str("tube_r=", tube_r, " center_z=", center_z, " half_top=", half_top));
