// =====================================================================
// screw.scad — なべ小ねじ / ワッシャ / 平行ピン 簡易モデル (購入品)
//
// アセンブリで「ねじが実体として存在する」ことを示すためのプレースホルダ。
// 印刷対象ではない。ねじ山は表現しない (円柱)。
//
// 原点: 頭の座面中心。軸 (shank) は -Z、頭は +Z へ伸びる。
//   kind = "pan"    : なべ頭 (head_d / head_h)
//   kind = "flat"   : 皿頭 (原点 = 頭の上面中心 = 相手面。円錐頭 head_d→d を -head_h まで、以下軸)
//   kind = "washer" : 平ワッシャ / シム (内径 d、外径 head_d、厚 head_h。0..head_h)
//   kind = "rod"    : 全ねじ / 丸棒 (径 d、長さ l。原点 = 上端、-Z へ)
//   kind = "nut"    : 六角ナット (二面幅 head_d、厚 head_h、穴 d。0..head_h)
//
// placement.json での向き:
//   軸を -Y に向ける (デッキ上面から下へ締める等) → rotate([-90,0,0])
//   軸を +Y に向ける                              → rotate([ 90,0,0])
//   軸を +Z に向ける                              → rotate([180,0,0])
// =====================================================================

/* [呼び] */
kind    = "pan";  // [pan, flat, washer, rod, nut]
d       = 3;      // ねじ呼び径 (washer では内径)
l       = 8;      // 首下長 (washer では無視)
head_d  = 5.5;    // 頭Ø (washer では外径)
head_h  = 2.0;    // 頭高さ (washer では厚み)

$fn = 24;

assert(d > 0 && (kind == "rod" || head_d > d), "頭が軸より小さい");
assert(kind == "washer" || l > 0, "首下長が不正");

if (kind == "pan") {
    // 頭 (なべ: 上面をわずかに丸める代わりに単純円柱)
    cylinder(d = head_d, h = head_h);
    // 軸
    translate([0, 0, -l]) cylinder(d = d, h = l + 0.01);
} else if (kind == "flat") {
    translate([0, 0, -head_h]) cylinder(d1 = d, d2 = head_d, h = head_h);
    translate([0, 0, -l]) cylinder(d = d, h = l - head_h + 0.01);
} else if (kind == "rod") {
    translate([0, 0, -l]) cylinder(d = d, h = l);
} else if (kind == "nut") {
    difference() {
        cylinder(d = head_d / cos(30), h = head_h, $fn = 6);
        translate([0, 0, -1]) cylinder(d = d, h = head_h + 2);
    }
} else {
    difference() {
        cylinder(d = head_d, h = head_h);
        translate([0, 0, -1]) cylinder(d = d, h = head_h + 2);
    }
}

echo(str("screw ", kind, " M", d, (kind == "pan" ? str("x", l) : str(" od", head_d, " t", head_h))));
