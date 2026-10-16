// =====================================================================
// child_tray_deck.scad — 子機 電子部トレイ デッキ (BlueRobotics WTE4 4")
// フランジ開口(実測 Ø88.5)から挿入するスレッドの上板。下面に
// child_tray_rib(半円リブ)を3枚 M3 で固定してチューブ内で支持する。
// 前端: ケーブル/ペネトレータ余裕ゾーン、中央: RX基板ベイ(内寸28×84)、
// 後方: LiPo 3S 5000mAh ベイ(内寸46×138、面ファスナースロット)。
// 印刷向き: このまま(デッキ上面が上)。全フィーチャ上向きでサポート不要。
// Fusion編集用に cube/cylinder ブーリアンのみ(角丸はFusion側で)。
// =====================================================================

/* [容器 (実測値)] */
flange_bore  = 88.5;   // フランジ貫通口 実測Ø
glide_clear  = 1.0;    // リブ外径と開口の径クリアランス

/* [デッキ] */
deck_t       = 4;      // デッキ板厚
deck_drop    = 18;     // チューブ軸心からデッキ上面までの落ち込み
deck_w       = 75;     // デッキ幅 (弦長以下であること: assertで検査)

/* [ゾーン寸法 (前端y=0)] */
front_zone   = 30;     // 前端ケーブル余裕(ペネトレータ後方空間)
rib_t        = 6;      // リブ板厚
card_in_w    = 28;     // RX基板ベイ 内幅 (断面25+余裕)
card_in_l    = 84;     // RX基板ベイ 内長 (基板80+余裕)
card_wall    = 3;      // ベイ壁厚
card_h       = 20;     // ベイ壁高さ
bat_in_w     = 46;     // 電池ベイ 内幅 (43+余裕)
bat_in_l     = 138;    // 電池ベイ 内長 (135+余裕)
bat_wall     = 3;      // 電池ベイ壁厚
bat_h        = 15;     // 電池ベイ壁高さ

/* [固定・配線] */
rib_screw_d  = 3.4;    // リブ固定 M3 クリアランス穴
rib_screw_x  = 25;     // リブ固定穴の中心振り分け(±)
cable_d      = 9;      // 前端ケーブル通し穴Ø ×2
strap_w      = 14;     // 面ファスナースロット幅(帯方向)
strap_t      = 4;      // スロット厚
std_d        = 2.8;    // ベイ床のM3セルフタップ下穴(スタンドオフ用)

$fn = 64;

// ---- 導出 -----------------------------------------------------------
rib_r     = (flange_bore - glide_clear) / 2;          // リブ半径 43.75
chord_h   = deck_drop + deck_t;                        // 軸心→デッキ下面
half_chd  = sqrt(rib_r*rib_r - chord_h*chord_h);       // デッキ下面での半弦長
card_y0   = front_zone;                                // 基板ベイ 前壁始点
card_y1   = card_y0 + 2*card_wall + card_in_l;         // 基板ベイ 後壁終点
mid_rib_c = card_y1 + rib_t/2 + 1;                     // 中リブ中心
bat_y0    = mid_rib_c + rib_t/2 + 1;                   // 電池ベイ 前壁始点
bat_y1    = bat_y0 + 2*bat_wall + bat_in_l;            // 電池ベイ 後壁終点
rear_rib_c= bat_y1 + rib_t/2 + 1;                      // 後リブ中心
deck_len  = rear_rib_c + rib_t/2 + 2;                  // デッキ全長
rib_cs    = [front_zone - rib_t/2, mid_rib_c, rear_rib_c]; // リブ3枚の中心y
strap_y   = [bat_y0 + bat_wall + bat_in_l*0.25,
             bat_y0 + bat_wall + bat_in_l*0.75];       // ストラップ位置
strap_x   = bat_in_w/2 + bat_wall + 3 + strap_t/2;     // スロット中心(±)

// ---- 干渉・成立性チェック --------------------------------------------
assert(deck_w/2 <= half_chd + 0.01,
       str("デッキ幅", deck_w, "が弦長", 2*half_chd, "を超過"));
assert(deck_len <= 288,
       str("デッキ全長", deck_len, "がチューブ内有効長(~288, 要実測)を超過"));
// 収容物の外接チェック(ベイ壁外側の角がリブ円に収まるか)
card_corner = sqrt(pow(card_in_w/2 + card_wall, 2) + pow(55 - deck_drop, 2));
assert(card_corner < rib_r,
       str("RX基板(高55)の外接半径", card_corner, "がリブ半径", rib_r, "を超過"));
bat_corner = sqrt(pow(strap_x + strap_t/2 + 2, 2) + pow(35 - deck_drop, 2));
assert(bat_corner < rib_r, "電池+ストラップスロットがリブ円を超過");
// リブ固定穴とベイ壁の干渉(穴は壁の外側にあること)
assert(rib_screw_x - rib_screw_d/2 > card_in_w/2 + card_wall + 1,
       "リブ固定穴が基板ベイ壁と干渉");
// ストラップスロットとリブ固定穴のyクリアランス
for (sy = strap_y) for (ry = rib_cs)
    assert(abs(sy - ry) > strap_w/2 + rib_t/2 + rib_screw_d/2,
           "ストラップスロットとリブ位置が干渉");

// ---- 本体 -------------------------------------------------------------
difference() {
    union() {
        // デッキ板
        translate([-deck_w/2, 0, 0]) cube([deck_w, deck_len, deck_t]);
        // RX基板ベイ壁 (ロの字)
        translate([0, card_y0, 0]) {
            for (sx=[-1,1]) translate([sx*(card_in_w/2 + card_wall/2), 0, 0])
                translate([-card_wall/2, 0, deck_t])
                    cube([card_wall, 2*card_wall + card_in_l, card_h]);
            for (yy=[0, card_wall + card_in_l])
                translate([-card_in_w/2 - card_wall, yy, deck_t])
                    cube([card_in_w + 2*card_wall, card_wall, card_h]);
        }
        // 電池ベイ壁 (ロの字)
        translate([0, bat_y0, 0]) {
            for (sx=[-1,1]) translate([sx*(bat_in_w/2 + bat_wall/2), 0, 0])
                translate([-bat_wall/2, 0, deck_t])
                    cube([bat_wall, 2*bat_wall + bat_in_l, bat_h]);
            for (yy=[0, bat_wall + bat_in_l])
                translate([-bat_in_w/2 - bat_wall, yy, deck_t])
                    cube([bat_in_w + 2*bat_wall, bat_wall, bat_h]);
        }
    }
    // リブ固定 M3 貫通穴 (リブ上端のパイロットへ)
    for (ry = rib_cs) for (sx=[-1,1])
        translate([sx*rib_screw_x, ry, -0.5])
            cylinder(d=rib_screw_d, h=deck_t+1);
    // 前端ケーブル穴 ×2
    for (sx=[-1,1])
        translate([sx*15, front_zone/2 + 3, -0.5])
            cylinder(d=cable_d, h=deck_t+1);
    // 基板ベイ床: スタンドオフ用 M3 下穴 4個
    for (sx=[-1,1]) for (yy=[card_y0+card_wall+15, card_y1-card_wall-15])
        translate([sx*10, yy, -0.5]) cylinder(d=std_d, h=deck_t+1);
    // 電池 面ファスナースロット (ベイ壁の外側、左右貫通)
    for (sy = strap_y) for (sx=[-1,1])
        translate([sx*strap_x - strap_t/2, sy - strap_w/2, -0.5])
            cube([strap_t, strap_w, deck_t+1]);
    // 電池ベイ床の軽量化穴 兼 ケーブル通し
    for (yy=[bat_y0+35, bat_y0+105])
        translate([0, yy, -0.5]) cylinder(d=16, h=deck_t+1);
}

echo(str("deck_len=", deck_len, "  rib centers y=", rib_cs,
         "  rib_r=", rib_r, "  half_chord=", half_chd));
