// =====================================================================
// child_vtray_rib.scad — 子機 縦置き内装 センタリング バルクヘッド
//
// child_vtray_deck の**両端 (幅 82mm の細い部分)** に挿して、内装を
// フランジ貫通口 (Ø88.5) の中心に保持する。上下 2 枚で内装の姿勢が決まる。
// 固定: ねじ無し。デッキ先端から差し込み、内側ショルダー (幅 84) に当てる。先端側は
// デッキ板を貫く M2.5×6 なべ (頭 Ø4.5) が抜け止め (2026-09-03: 以前は先端側にも
// ショルダーがあり、スロット 76.4 を通らず嵌められなかった)。
//
// 中央下寄りは**ケーブル通路**として大きく開けてある (下キャップの
// ペネトレータから来る全ケーブルがここを通る)。結束バンド用スロット付き。
//
// 座標: child_vtray_deck と同じ (X=幅 / Y=積み方向 / Z=チューブ軸)。
//       原点はリブの Z 始点・軸心。
//
// 印刷向き: 円板を寝かせて (Z を上に) 印刷。全フィーチャ貫通でサポート不要。
// =====================================================================

/* [容器] */
flange_bore = 88.5;   // フランジ貫通口Ø (実測)
bore_clear  = 1.0;    // 径クリアランス

/* [リブ] */
rib_t       = 6;      // 板厚 (Z)
lead_chamfer = 0.8;   // 両面外周45°面取り。挿入時にアクリル縁へ引っ掛けない

/* [デッキとの嵌合 (child_vtray_deck と一致させること)] */
deck_wn     = 76;     // デッキ端部の幅
deck_t      = 4;      // デッキ板厚
deck_y0     = -10;    // デッキ下面 Y
slot_clear  = 0.4;    // 嵌合クリアランス (片側 0.2)
min_web     = 4;      // スロット横に残す最小肉厚

/* [ケーブル通路] */
duct_w      = 40;     // 通路の幅 (X)
duct_y0     = -36;    // 通路の下端 Y
duct_y1     = -14;    // 通路の上端 Y (デッキ下面 -10 の少し下まで)
tie_w       = 3.5;    // 結束バンド スロット 幅
tie_l       = 10;     // 同 長さ (Y)
tie_x       = 26;     // 同 中心 X (±)
tie_y       = -19;    // 同 中心 Y
side_d      = 14;     // 上側の補助通し穴Ø
side_x      = 29;     // 同 中心 X (±)
side_y      = 12;     // 同 中心 Y

$fn = 96;

// ---- 導出 -------------------------------------------------------------
rib_r   = (flange_bore - bore_clear) / 2;      // 43.75
slot_w  = deck_wn + slot_clear;
slot_h  = deck_t  + slot_clear;
slot_y0 = deck_y0 - slot_clear/2;
duct_x  = duct_w/2;

function rad(x, y) = sqrt(x*x + y*y);

// ---- 干渉・成立性チェック ---------------------------------------------
// スロットの角が円板からはみ出さないこと (はみ出すとリブが 2 枚に割れる)
assert(rad(slot_w/2, slot_y0) < rib_r - 1,
       str("嵌合スロットの角が円板の縁に近すぎる r=", rad(slot_w/2, slot_y0),
           " / 半径 ", rib_r));
assert(rad(slot_w/2, slot_y0 + slot_h) < rib_r - 1, "嵌合スロット上側の角が円板の縁に近すぎる");
// スロットの左右に残る肉 (ここでリブの上下がつながっている)
web = rib_r - slot_w/2;
assert(web > min_web,
       str("スロット横の肉 ", web, "mm が薄すぎる (最低 ", min_web, "mm)"));
// ケーブル通路が円板の中に収まること
assert(rad(duct_x, duct_y0) < rib_r - 2,
       str("ケーブル通路の角が円板からはみ出す r=", rad(duct_x, duct_y0)));
assert(duct_y1 < slot_y0, "ケーブル通路がデッキ嵌合スロットに食い込んでいる");
// 結束スロットが通路と円板の間の肉に収まること
assert(tie_x - tie_w/2 > duct_x + 2,
       str("結束スロットがケーブル通路に近すぎる (肉 ", tie_x - tie_w/2 - duct_x, "mm)"));
assert(rad(tie_x + tie_w/2, tie_y - tie_l/2) < rib_r - 2,
       str("結束スロットが円板の縁に近すぎる r=", rad(tie_x + tie_w/2, tie_y - tie_l/2)));
assert(tie_y + tie_l/2 < slot_y0 - 2,
       str("結束スロットがデッキ嵌合スロットに近すぎる (", slot_y0 - (tie_y + tie_l/2), "mm)"));
// 上側の補助通し穴
assert(rad(side_x + side_d/2, side_y) < rib_r - 2,
       str("補助通し穴が円板の縁に近すぎる r=", rad(side_x + side_d/2, side_y)));
assert(side_y - side_d/2 > slot_y0 + slot_h + 2, "補助通し穴が嵌合スロットに食い込んでいる");

// ---- 本体 -------------------------------------------------------------
module glide_disc() {
    hull() {
        cylinder(r=rib_r-lead_chamfer,h=0.01);
        translate([0,0,lead_chamfer])
            cylinder(r=rib_r,h=rib_t-2*lead_chamfer);
        translate([0,0,rib_t-0.01])
            cylinder(r=rib_r-lead_chamfer,h=0.01);
    }
}

difference() {
    glide_disc();
    // M3 upper stop screw: 6.8 mm pan-head/tool clearance, open at top.
    translate([0,deck_y0+deck_t,8.5]) rotate([-90,0,0]) cylinder(d=6.8,h=6,$fn=64);

    // デッキが通るスロット
    translate([-slot_w/2, slot_y0, -0.5]) cube([slot_w, slot_h, rib_t + 1]);

    // ケーブル通路 (下側の大開口)
    translate([-duct_x, duct_y0, -0.5]) cube([duct_w, duct_y1 - duct_y0, rib_t + 1]);

    // 上側の補助通し穴 (基板側へ上げる線)
    for (sx = [-1, 1])
        translate([sx * side_x, side_y, -0.5]) cylinder(d = side_d, h = rib_t + 1);

    // 結束バンド スロット
    for (sx = [-1, 1])
        translate([sx * tie_x - tie_w/2, tie_y - tie_l/2, -0.5])
            cube([tie_w, tie_l, rib_t + 1]);
}

echo(str("child_vtray_rib: Ø", 2*rib_r, " x t", rib_t,
         "  スロット ", slot_w, " x ", slot_h, " @Y", slot_y0,
         "  通路 ", duct_w, " x ", duct_y1 - duct_y0, "  スロット横の肉 ", web));
