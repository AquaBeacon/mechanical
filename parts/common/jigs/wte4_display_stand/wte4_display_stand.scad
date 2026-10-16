// =====================================================================
// wte4_display_stand.scad - WTE4 耐圧容器 展示用 転がり止め台
//
// Blue Robotics WTE4 アクリルチューブ (OD 114.3, 200mm) をフランジ+エンド
// キャップ付きのまま横置きで展示するための台。円筒部だけを 2 枚の受け板で
// 受け、2 本の横桟と十字相欠き (cross-lap) で組む。ねじ・接着なし。
//
//   part="cradle"  受け板  ×2 (YZ 面、円弧受け)
//   part="rail"    横桟    ×2 (XZ 面、受け板をつなぐ)
//   part="asm"     組立状態 (プレビュー用。相欠きのクリアランス 0 で融合)
//   part="demo"    組立状態 + チューブ (PNG プレビュー専用。STL にしない)
//
// 座標系: X = チューブ軸、Y = 幅、Z = 上。原点 = 台の底面中心。
// 印刷向き: どちらの板も平置き (最も広い面を下)。サポート不要。
// 取合い: parts/child/exterior/cots/wte4_acrylic_tube (interfaces.json で固定)
// =====================================================================

/* [部品選択] */
part = "cradle";      // [cradle, rail, asm, demo]

/* [相手部品 (wte4_acrylic_tube)] */
tube_od   = 114.3;    // チューブ外径 (公称 114.3 ± 0.8)
tube_len  = 200;      // チューブ長 (BR-101052-200)
fit_clear = 0.5;      // 半径方向の余裕 (EVA/フェルトを貼るなら厚み分を足す)

/* [板] */
t          = 4;       // 板厚 (全板共通)
slot_clear = 0.2;     // 相欠きスロットの総クリアランス (要フィットテスト)

/* [受け板 (cradle)] */
cr_w      = 150;      // 受け板の幅 (Y)
cr_h      = 48;       // 受け板の高さ (Z)
arc_rise  = 20;       // 円弧中心を板上端からどれだけ上に置くか (大きいほど抱き角が浅い)
cradle_x  = 55;       // 受け板の位置 (中心から ±X)。間隔 = 2*cradle_x

/* [横桟 (rail)] */
rail_len  = 160;      // 横桟の長さ (X)
rail_h    = 35;       // 横桟の高さ (Z)
rail_y    = 65;       // 横桟の位置 (中心から ±Y)

/* [検査] */
min_wall  = 6;        // スロットと縁/円弧の間に残す最小肉
lig_min   = 8;        // 円弧最下部と底面の間に残す最小肉
end_keep  = 10;       // 受け板はチューブ端からこれ以上内側
x1c_max   = 250;      // X1C 実用造形枠

$fn = 180;

// --- 導出値 ------------------------------------------------------------
r_fit    = tube_od/2 + fit_clear;          // 受け円弧の半径
z_c      = cr_h + arc_rise;                // チューブ中心高さ (= 円弧中心)
slot_w   = t + slot_clear;                 // スロット幅
lap      = rail_h/2;                       // 相欠き深さ (横桟の半分)
arc_half = sqrt(r_fit*r_fit - arc_rise*arc_rise);  // 板上端での円弧半幅
wrap_deg = 2*acos(arc_rise/r_fit);         // 抱き角
gap_z    = z_c - r_fit;                    // チューブ最下点と底面の隙間

// --- 干渉・成立チェック ------------------------------------------------
assert(arc_rise >= 0, "arc_rise < 0: 円弧が 180° を超え、チューブを上から入れられない");
assert(gap_z >= lig_min,
       str("円弧最下部の肉が薄すぎる: ", gap_z, " < ", lig_min, " (cr_h か arc_rise を増やす)"));
assert(rail_y - slot_w/2 - arc_half >= min_wall,
       str("横桟スロットが円弧に近すぎる: 肉 ", rail_y - slot_w/2 - arc_half, " < ", min_wall));
assert(cr_w/2 - (rail_y + slot_w/2) >= min_wall,
       str("横桟スロットが受け板の外縁に近すぎる: 肉 ", cr_w/2 - rail_y - slot_w/2, " < ", min_wall));
assert(rail_len/2 - (cradle_x + slot_w/2) >= min_wall,
       str("受け板スロットが横桟の端に近すぎる: 肉 ", rail_len/2 - cradle_x - slot_w/2, " < ", min_wall));
assert(cr_h - lap >= min_wall, "相欠きが受け板の高さに対して深すぎる");
assert(rail_y - slot_w/2 >= tube_od/2,
       "横桟がチューブの真下に入る (rail_y を増やす)");   // 横桟上端はチューブに触れない
assert(cradle_x + t/2 <= tube_len/2 - end_keep,
       str("受け板がチューブ端に近すぎる: ", cradle_x + t/2, " > ", tube_len/2 - end_keep));
assert(max(cr_w, cr_h, rail_len, rail_h) <= x1c_max, "X1C の造形枠を超える");

// --- 部品 --------------------------------------------------------------
module cradle(clear = slot_clear) {
    // YZ 面の板。ローカル座標: X = 板厚方向 (-t/2..t/2), Y 幅, Z 高さ
    sw = t + clear;
    difference() {
        translate([-t/2, -cr_w/2, 0]) cube([t, cr_w, cr_h]);
        // チューブ受け円弧
        translate([0, 0, z_c]) rotate([0, 90, 0])
            cylinder(r = r_fit, h = t + 2, center = true);
        // 横桟用スロット (下から lap まで)
        for (sy = [-rail_y, rail_y])
            translate([-t/2 - 1, sy - sw/2, -1]) cube([t + 2, sw, lap + 1]);
    }
}

module rail(clear = slot_clear) {
    // XZ 面の板。ローカル座標: X 長さ, Y = 板厚方向 (-t/2..t/2), Z 高さ
    sw = t + clear;
    difference() {
        translate([-rail_len/2, -t/2, 0]) cube([rail_len, t, rail_h]);
        // 受け板用スロット (上から lap まで)
        for (sx = [-cradle_x, cradle_x])
            translate([sx - sw/2, -t/2 - 1, lap]) cube([sw, t + 2, rail_h]);
    }
}

module stand(clear = slot_clear) {
    for (x = [-cradle_x, cradle_x]) translate([x, 0, 0]) cradle(clear);
    for (y = [-rail_y, rail_y])     translate([0, y, 0]) rail(clear);
}

module tube_ghost() {
    // 円筒部のみ (フランジ/キャップは省略)
    translate([0, 0, z_c]) rotate([0, 90, 0])
        cylinder(d = tube_od, h = tube_len, center = true);
}

// --- 出力 --------------------------------------------------------------
if (part == "cradle")      cradle();
else if (part == "rail")   rail();
else if (part == "asm")    stand(0);          // 融合させて 1 ソリッドに
else if (part == "demo") {
    color("Orange") stand();
    color("LightSkyBlue", 0.5) tube_ghost();
}

echo(str("wte4_display_stand: r_fit=", r_fit, " z_c=", z_c, " gap_z=", gap_z,
         " wrap=", wrap_deg, "deg arc_half=", arc_half, " slot_w=", slot_w));
