// =====================================================================
// child_tray_rib.scad — 子機トレイ バルクヘッドリブ (3枚印刷)
// 半円板(Ø87.5 = フランジ開口88.5 − 1.0)。上端フラット面を
// child_tray_deck の下面に当て、デッキ上から M3×2 で固定する。
// 中央切欠きは配線通し兼軽量化。前リブはペネトレータ後方空間に
// 干渉しない位置(デッキ側 front_zone)に付くこと(要実測確認)。
// 印刷向き: 平置き(円板面を下)。M3下穴は層内水平だがØ2.5なので実用上OK。
// =====================================================================

/* [容器 (実測値)] */
flange_bore  = 88.5;   // フランジ貫通口 実測Ø
glide_clear  = 1.0;    // 開口との径クリアランス

/* [デッキとの関係 (child_tray_deck と一致させる)] */
deck_drop    = 18;     // 軸心→デッキ上面
deck_t       = 4;      // デッキ板厚
rib_t        = 6;      // リブ厚
screw_x      = 25;     // M3位置(±)  ※deck の rib_screw_x と一致
pilot_d      = 2.5;    // M3 セルフタップ下穴
pilot_depth  = 10;

/* [切欠き] */
cut_w        = 40;     // 配線切欠き幅
cut_h        = 14;     // 配線切欠き高さ

$fn = 96;

// ---- 導出 -----------------------------------------------------------
rib_r   = (flange_bore - glide_clear) / 2;   // 43.75
top_y   = -(deck_drop + deck_t);             // 上端フラット面 (軸心基準 -22)
cut_y0  = top_y - 4;                          // 切欠き上端(上端から4下げ)

// ---- 干渉チェック -----------------------------------------------------
assert(abs(screw_x) - pilot_d/2 > cut_w/2 + 2,
       "M3下穴が配線切欠きと干渉");
assert(cut_y0 - cut_h > -rib_r + 3,
       str("配線切欠き下端が外周に接近(残り",
           (cut_y0 - cut_h) - (-rib_r), "mm)"));
assert(sqrt(pow(screw_x,2) + pow(abs(top_y)+pilot_depth,2)) < rib_r - 1.5,
       "M3下穴の先端が外周を突き抜け");

// ---- 本体 (軸心=原点、y負側が下、板厚は+Z) ----------------------------
difference() {
    linear_extrude(height = rib_t)
        difference() {
            intersection() {
                circle(r = rib_r);
                translate([-rib_r, top_y - rib_r]) square([2*rib_r, rib_r]); // y<=top_y
            }
            // 配線切欠き
            translate([-cut_w/2, cut_y0 - cut_h]) square([cut_w, cut_h + 1]);
        }
    // M3 セルフタップ下穴 ×2 (上端フラット面から半径方向内向きに)
    for (sx=[-1,1])
        translate([sx*screw_x, top_y + 0.5, rib_t/2])
            rotate([90, 0, 0])
                cylinder(d = pilot_d, h = pilot_depth + 0.5);
}
