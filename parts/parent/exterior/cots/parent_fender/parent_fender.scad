// =====================================================================
// parent_fender.scad — 親機 浮子 (市販の紡錘形フロート、中心に紐通しの空洞) 仮モデル (購入品)
//
// 配置検討・アセンブリ表示用。印刷対象ではない。
// **寸法はすべて仮値** (2026-09-04/05 人間回答: 「現物があるが寸法は後で測る」
//   「完全な円筒ではない (挟めない)」「中に空洞があるので紐を通して固定」)。
// 実測後に parent_fender.md と本ファイル、parent_float_yoke.scad の同名変数を同時に更新する (二重定義)。
//
// 座標系: 浮子の軸 = Y、原点 = 胴の中心。両端は円錐で先細り、中心に貫通穴 (紐通し)。
// =====================================================================

/* [外形 (仮値・要実測)] */
fender_d   = 100;   // 胴の最大外径
fender_len = 300;   // 全長 (端面から端面)
taper_len  = 40;    // 先細り部の長さ (片側)
end_d      = 40;    // 端面の径
bore_d     = 15;    // 中心空洞 (紐通し) の径

$fn = 96;

cyl_len = fender_len - 2*taper_len;
vol_l = (PI*pow(fender_d/2,2)*cyl_len
         + 2 * PI*taper_len/3 * (pow(fender_d/2,2) + fender_d/2*end_d/2 + pow(end_d/2,2))
         - PI*pow(bore_d/2,2)*fender_len) / 1e6;
assert(cyl_len > 0, "先細り部が全長より長い");
assert(end_d > bore_d + 6, "端面が空洞に対して薄い");
echo(str("parent_fender: d=", fender_d, " len=", fender_len, " taper=", taper_len, " end_d=", end_d,
         " bore=", bore_d, " displacement=", vol_l, " L/pc (provisional)"));

rotate([-90, 0, 0]) difference() {
    union() {
        translate([0, 0, -cyl_len/2]) cylinder(d = fender_d, h = cyl_len);
        translate([0, 0,  cyl_len/2]) cylinder(d1 = fender_d, d2 = end_d, h = taper_len);
        translate([0, 0, -cyl_len/2]) mirror([0, 0, 1]) cylinder(d1 = fender_d, d2 = end_d, h = taper_len);
    }
    cylinder(d = bore_d, h = fender_len + 2, center = true);
}
