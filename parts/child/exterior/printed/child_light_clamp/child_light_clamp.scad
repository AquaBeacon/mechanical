// =====================================================================
// child_light_clamp.scad — 水中ライト 割りクランプ 上半分 (1個印刷)
//
// 下半分は child_shell_fwd の鞍座 (light_saddle) と一体。この部品を
// M4 x4 で締めてライト胴を挟む。ライトの前後位置は鞍座の長さ 40mm の
// 範囲で自由に決められる (ライト軸 = Y なので、軸方向にスライドするだけ)。
//
// ★ ライトは未選定。light_d は仮値。製品決定後に light_d を実測値に
//   置き換え、child_shell_fwd と**両方**再ビルドすること。
//
// 座標系 (この部品のローカル):
//   x = 0 : 機体中心   y = 0 : 鞍座の後端 (light_y0)   z = 0 : ライト軸
//   → アセンブリでは translate([0, 78, 58]) で置く
//
// 印刷向き: **上下逆さま** (z=blk_h の平面をベッドに置く)。
//   鞍の半円が上を向くのでサポート不要。
// =====================================================================

/* [ライト (未選定 — 要実測)] */
light_d   = 40;             // 胴径 **要選定・要実測**
grip_clr  = 0.4;            // 締め代を残すためのすきま (ゴムシート前提)

/* [クランプ (child_shell_fwd と一致させること)] */
light_y0  = 78;             // 鞍座 y 範囲 (グローバル)
light_y1  = 118;
light_m4x = 28;             // M4 の x (±)
light_m4y = [86, 110];      // 同 y (グローバル)
light_blk = 35;             // ブロック 半幅
blk_h     = 30;             // ブロック 高さ (ライト軸から上)
m4_d      = 4.5;
gap_z     = 1.5;            // 合わせ面のすきま (締めるとゴムが潰れて効く)

/* [結束] */
// M4 の外側には入らないので、前後の M4 の**間** (y 中央) に置く
tie_w     = 4;              // 帯の厚み方向 (Y)
tie_h     = 8;              // 帯の幅方向 (X)
tie_x     = 30;             // 結束スロット x (±)

$fn = 96;

// ---- 導出 -----------------------------------------------------------
blk_len = light_y1 - light_y0;              // 40
sc_y    = [light_m4y[0] - light_y0, light_m4y[1] - light_y0];   // 8, 32
bore_r  = (light_d + grip_clr)/2;

// ---- 干渉・成立性チェック --------------------------------------------
assert(blk_h - bore_r >= 8, str("鞍の頂部肉厚不足: ", blk_h - bore_r, "mm"));
assert(light_m4x - m4_d/2 > bore_r + 3,
       str("M4 が鞍の半円に掛かる: ", light_m4x - m4_d/2, " <= ", bore_r + 3));
assert(light_m4x + m4_d/2 < light_blk - 2, "M4 の外側端距離不足");
for (y = sc_y) assert(y > 5 && y < blk_len - 5, "M4 の Y 端距離不足");
assert(tie_x + tie_h/2 <= light_blk - 0.5,
       str("結束スロットがブロックからはみ出し: 外端 ", tie_x + tie_h/2, " > ", light_blk));
for (y = sc_y)
    assert(abs(blk_len/2 - y) > (tie_w + m4_d)/2 + 2,
           str("結束スロット (y=", blk_len/2, ") が M4 (y=", y, ") に掛かる"));
assert(gap_z > 0.8, "合わせ面のすきまが小さく、締め代が取れない");

// ---- 本体 -------------------------------------------------------------
difference() {
    translate([-light_blk, 0, gap_z]) cube([2*light_blk, blk_len, blk_h - gap_z]);
    // ライト胴の鞍 (下向きの半円。印刷時は上向きになる)
    translate([0, -2, 0]) rotate([-90,0,0]) cylinder(d=light_d + grip_clr, h=blk_len+4);
    // M4 通し穴 x4
    for (sx=[-1,1]) for (y=sc_y)
        translate([sx*light_m4x, y, -2]) cylinder(d=m4_d, h=blk_h+4);
    // 結束バンド スロット (ライトの配線を機体側へ寄せる)。前後 M4 の中間に置く
    for (sx=[-1,1])
        translate([sx*tie_x - tie_h/2, blk_len/2 - tie_w/2, -2])
            cube([tie_h, tie_w, blk_h+4]);
}

echo(str("クランプ ", 2*light_blk, " x ", blk_len, " x ", blk_h - gap_z,
         " / 鞍 Ø", light_d + grip_clr));
echo(str("アセンブリ配置: translate([0, ", light_y0, ", 58])"));
