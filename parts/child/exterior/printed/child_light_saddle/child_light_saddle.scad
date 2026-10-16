// =====================================================================
// child_light_saddle.scad — 子機 水中ライト鞍座 (再設計版・汎用)
//
// 旧 child_light_clamp の置き換え。ワニ顎ゲート (child_jaw_gate) の前面
// ライトパッド (平面 y=67、M4 下穴 x=±18 / z=46,74) に M4 ×4 で締結し、
// 円筒ライト (Ø light_d 仮 40 — **未選定、要実測**) を Y 軸方向に差し込んで
// 結束バンド 2 本で固定する。ライトの向き = +Y (カメラと同方向)。
//
// 座標系: 機体グローバル (チューブ軸 z、+Y 前)。
// 印刷向き: 背面 (y=67 の取付面) をベッドへ。ボアが垂直になりサポートレス。
// 荷重: ライト 0.3 kg × 10g ≈ 30 N (L2 輸送)。M4 ×4 と 30mm 幅ブロックには
//   桁違いに小さい (ネジ面圧 < 1 MPa)。FEA 不要 (全体系 FEA はコアフレーム側)。
// =====================================================================

/* [ライト (未選定 — 仮値)] */
light_d   = 40;      // 胴径。選定後に実測で置換
light_clr = 0.5;

/* [ゲートのライトパッド (二重定義 — child_jaw_gate と揃える)] */
pad_y     = 67;      // 取付面
lm4_x     = 18;      // M4 位置 (±)
lm4_z     = [46, 74];

/* [ブロック] */
blk_hw    = 26;      // 半幅 (x)
blk_d     = 30;      // 奥行 (y): 67..97
blk_z0    = 36;
blk_z1    = 78;
ax_z      = 60;      // ライト軸の z (ゲートの M4 パターン中心)

/* [締結] */
m4_d      = 4.5;     // M4 クリアランス
cb_d      = 8.6;     // 頭座ぐり
cb_dep    = 12;

/* [結束バンド スロット] */
tie_x     = [10, 14];       // |x| 範囲
tie_y     = [[71, 77], [85, 91]];
tie_z0    = 35;

/* [Hidden] */
fudge = 0.01;
$fn = 96;

// ---- 導出値 ----------------------------------------------------------
bore_r  = (light_d + light_clr) / 2;
blk_y1  = pad_y + blk_d;

// ---- 検査 ------------------------------------------------------------
assert(abs(lm4_z[1] - ax_z) - m4_d/2 - sqrt(max(bore_r*bore_r - lm4_x*lm4_x, 0)) >= 2,
       "M4 穴とライトボアの壁 < 2mm");
assert(blk_hw - lm4_x - cb_d/2 >= 3, "座ぐりの x 端距離不足");
assert(ax_z - bore_r > blk_z0 + 3,  "ボア底の床厚 < 3mm (床を下げよ)");
assert(ax_z + bore_r > blk_z1,      "上スロットが開いていない (挿入は軸方向の想定)");
assert(tie_x[0] > 4 && tie_x[1] < lm4_x - m4_d/2 - 1, "結束スロットが M4 に掛かる");
assert(blk_y1 <= 125 - 5, "鞍座が 250 枠 (保護代) を超える");
echo(str("ボア z ", ax_z - bore_r, " .. ", ax_z + bore_r, " / ブロック ", 2*blk_hw,
         " x ", blk_d, " x ", blk_z1 - blk_z0));

// ---- 形状 ------------------------------------------------------------
difference() {
    translate([-blk_hw, pad_y, blk_z0])
        cube([2*blk_hw, blk_d, blk_z1 - blk_z0]);

    // ライトボア (軸 Y、上に開口)
    translate([0, pad_y - fudge, ax_z])
        rotate([-90, 0, 0]) cylinder(r = bore_r, h = blk_d + 2*fudge);

    // M4 ×4 (軸 Y) + 前面座ぐり (天井 45° コーン)
    for (sx = [-1, 1], z = lm4_z) {
        translate([sx*lm4_x, pad_y - fudge, z])
            rotate([-90, 0, 0]) cylinder(d = m4_d, h = blk_d + 2*fudge, $fn = 32);
        translate([sx*lm4_x, blk_y1 - cb_dep, z])
            rotate([-90, 0, 0]) cylinder(d = cb_d, h = cb_dep + fudge, $fn = 32);
        translate([sx*lm4_x, blk_y1 - cb_dep - (cb_d - m4_d)/2, z])
            rotate([-90, 0, 0]) cylinder(d1 = m4_d, d2 = cb_d, h = (cb_d - m4_d)/2 + fudge, $fn = 32);
    }

    // 結束バンド スロット ×4 (床貫通、バンドはライトに 2 周)
    for (sx = [-1, 1], ty = tie_y)
        translate([sx > 0 ? tie_x[0] : -tie_x[1], ty[0], tie_z0 - fudge])
            cube([tie_x[1] - tie_x[0], ty[1] - ty[0], ax_z - tie_z0]);
}
