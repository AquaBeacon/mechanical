// =====================================================================
// hex_spacer.scad — 六角スペーサ 簡易モデル (購入品)
//
// 親機・子機内装で使う市販スペーサのプレースホルダ。印刷対象ではない。
//   kind = "mf" : オス-メス (胴 +Z、オスねじ -Z)
//   kind = "ff" : メス-メス (胴だけ。両端にメスねじ)
//
//   m3_mf25 : P-MAIN 取付穴 ×4 → parent_lipo_tray / p2 の TX 高架 ×4
//   m3_mf32 / m3_mf17 : C-MAIN 取付穴に立てて child_lcd_support アーチを受ける
//                       (オスは基板穴 Ø3.2 を通って child_vtray_deck のボス下穴へ)
//   m3_mf10 : WTE4 下フランジ BCD94 の M3 穴に立て、child_vtray_deck のラグを受ける
//   m2_ff6  : child_vtray_deck 下面 ↔ RX_improved_mini (Ø2.2 穴、M2 ねじ両側)
//
// 原点: 六角胴の下端面中心。胴は +Z、オスねじは -Z へ伸びる。
// 寸法は一般的な黄銅六角スペーサ (廣杉計器 BSB/ASB 系相当) の公称値。
// =====================================================================

/* [呼び] */
size    = 3;      // ねじ呼び (2, 3, 4)
body_l  = 25;     // 六角胴の長さ
stud_l  = 6;      // オスねじ長 (M2 は 4, M3 は 6, M4 は 8 が標準)。ff では無視
kind    = "mf";   // [mf, ff]

/* [導出 (JIS 二面幅)] */
af      = size == 2 ? 4 : size == 3 ? 5.5 : 7;      // 二面幅
bore_d  = size == 2 ? 1.6 : size == 3 ? 2.5 : 3.3;  // メスねじ下穴 (表示用)
bore_l  = min(body_l, size == 2 ? 5 : 10);          // メスねじ深さ (表示用)

$fn = 6;

assert(body_l > 0, "長さが不正");
assert(kind == "ff" || stud_l > 0, "mf にはオスねじ長が要る");

difference() {
    // 六角胴 (二面幅 af → 外接円径 af/cos30)
    cylinder(d = af / cos(30), h = body_l);
    // 上端のメスねじ
    translate([0, 0, body_l - bore_l]) cylinder(d = bore_d, h = bore_l + 1, $fn = 24);
    // ff は下端にもメスねじ
    if (kind == "ff") translate([0, 0, -1]) cylinder(d = bore_d, h = bore_l + 1, $fn = 24);
}
// オスねじ
if (kind == "mf")
    translate([0, 0, -stud_l]) cylinder(d = size, h = stud_l + 0.01, $fn = 24);

echo(str("hex_spacer M", size, " ", kind, " body ", body_l, " stud ", kind == "mf" ? stud_l : 0, " af ", af));
