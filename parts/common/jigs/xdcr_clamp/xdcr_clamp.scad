// =====================================================================
// xdcr_clamp.scad — TD04A 振動子 固定治具 (共通マウント面つき)
// 半円クレードル(本体)とクランプ蓋を M4×4 で締めて TD04A の胴を掴む。
// ベース裏面が取付面で、M5×4 (mount_x × mount_y) で任意の平面に固定する。
// ボルトパターンは相手側に 0°/90° の2組を用意してあるので、音響ビームの
// 向きを壁に対して垂直/平行に切り替えられる (xdcr_poolside_jig の棚)。
// 座標系: +X = 音響放射面の向き(ビーム方向)、Y = 幅、Z=0 = 取付面(裏面)。
// 印刷向き: body / cap ともこの姿勢のまま平置き。溝が上を向くので無サポート。
//           cap は組立時には上下逆さに載る (印刷姿勢 = 組立姿勢ではない)。
// 要実測: xdcr_d(胴径) / xdcr_len(胴長) / cable_d(ケーブル外径)
//         → 実測したら値を直して再ビルドすること。
// =====================================================================

/* [部品選択] */
part      = "body";   // [body, cap]

/* [TD04A (すべて要実測)] */
xdcr_d    = 26.0;     // 胴径の仮定値 ※xdcr_socket の 26.4 は +0.4 クリア込みの値
xdcr_len  = 55;       // 胴長の仮定値 (掴み代のチェックに使う)
cable_d   = 9;        // ケーブル外径の仮定値 ※xdcr_socket の cable_d と同値

/* [保持] */
squeeze   = 1.0;      // 締め代: 溝径を胴径よりこれだけ小さくする(蓋が底付きしない量)
liner_t   = 0;        // 溝に敷くゴムシートの厚み (0 = 無し)
grip_len  = 40;       // クレードルが胴を掴む長さ (X)
end_t     = 6;        // ケーブル側 端壁の厚み (挿入深さの当り面を兼ねる)
min_wall  = 3;        // 溝と穴の間に残す最小肉厚 (干渉チェック用)

/* [クランプ蓋 M4] */
cap_top   = 6;        // 蓋の溝上肉厚
m4_d      = 4.5;      // 蓋の通し穴
m4_head   = 8.6;      // 蓋の頭座グリ径
m4_cb     = 4;        // 同 深さ
m4_pilot  = 3.4;      // 本体側 自己タップ下穴 (M4 熱圧入インサートなら 5.6)
pilot_dep = 16;       // 同 深さ
bolt_sp   = 24;       // 蓋ボルトの X 間隔
bolt_y    = 19;       // 蓋ボルトの Y (±)

/* [取付ベース M5] */
base_w    = 56;       // ベース X ※xdcr_poolside_jig の clamp_base_w と一致
base_d    = 84;       // ベース Y ※xdcr_poolside_jig の clamp_base_d と一致
base_t    = 8;        // ベース厚 (= 溝底の肉厚)
mount_x   = 40;       // M5 ピッチ X (±20) ※xdcr_poolside_jig の mount_x と一致
mount_y   = 68;       // M5 ピッチ Y (±34) ※xdcr_poolside_jig の mount_y と一致
m5_d      = 5.3;      // M5 クリアランス穴
m5_wash   = 10;       // M5 平座金の外径 (干渉チェック用)

/* [予備保持 / 水抜き] */
tie_w     = 5.5;      // 結束バンド幅 (4.8mm 帯)
tie_t     = 2.5;      // 同 厚み
tie_x     = [-12, 12];// 結束スロットの X
drain_d   = 6;        // 水抜き穴 (溝底 → 取付面)
drain_x   = [-10, 16];

$fn = 64;

// ---- 導出寸法 ---------------------------------------------------------
bore_d   = xdcr_d + 2*liner_t - squeeze;  // クレードル溝の直径
bore_r   = bore_d/2;
axis_z   = base_t + bore_r;               // 溝軸の高さ = 本体ブロック上面
blk_w    = grip_len + end_t;              // クレードルブロック長 (X)
blk_d    = 2*(bolt_y + m4_head/2 + 3);    // 同 幅 (Y)
blk_x0   = -blk_w/2;                      // ブロック -X 端 (ケーブル側)
grip_x0  = blk_x0 + end_t;                // 溝の開始 X (= 胴の当り面)
grip_c   = (grip_x0 + blk_w/2)/2;         // 溝の中心 X
bolt_x   = [grip_c - bolt_sp/2, grip_c + bolt_sp/2];
cap_h    = cap_top + bore_r;              // 蓋の高さ
cbl_w    = cable_d + 1.5;                 // ケーブル溝の幅
tie_y    = blk_d/2 + tie_t/2 + 3;         // 結束スロットの Y (ブロックの外)
face_off = grip_x0 + xdcr_len;            // マウント中心 → 音響放射面 の X

// ---- 干渉チェック -----------------------------------------------------
assert(squeeze > 0, "squeeze<=0 だと蓋が底付きして締め付け力がゼロになる");
assert(bore_d > 0, "bore_d が負。squeeze が大きすぎる");
// 蓋ボルトが溝に食い込まない (下穴・通し穴の太いほうで見る)
assert(bolt_y - max(m4_pilot, m4_d)/2 >= bore_r + min_wall,
       str("蓋ボルトが溝に近すぎ: 残り肉厚 ",
           bolt_y - max(m4_pilot, m4_d)/2 - bore_r, " < ", min_wall));
// 蓋ボルトの頭座グリがブロック側面/端面から抜けない
assert(blk_d/2 - bolt_y - m4_head/2 >= 2.5, "蓋ボルト座グリがブロック側面に近すぎ");
assert(blk_w/2 - bolt_x[1] - m4_head/2 >= 2.5, "蓋ボルト座グリがブロック +X 端に近すぎ");
assert(bolt_x[0] - m4_head/2 >= grip_x0, "蓋ボルトがケーブル端壁に掛かっている");
// 下穴が取付面を貫通しない
assert(axis_z - pilot_dep >= 3,
       str("蓋ボルト下穴が取付面まで残り ", axis_z - pilot_dep, "mm しかない"));
// M5 の座金がクレードルブロックに乗り上げない (乗ると締結面が浮く)
assert(mount_y/2 - m5_wash/2 >= blk_d/2 + 1,
       str("M5 座金がブロックに干渉: 座金内縁 ", mount_y/2 - m5_wash/2,
           " < ブロック半幅 ", blk_d/2, " + 1"));
// M5 の縁距離
assert(base_d/2 - mount_y/2 - m5_d/2 >= 4, "M5 の Y 縁距離不足 (base_d を増やす)");
assert(base_w/2 - mount_x/2 - m5_d/2 >= 4, "M5 の X 縁距離不足 (base_w を増やす)");
assert(base_w >= blk_w && base_d >= blk_d, "ベースがクレードルブロックより小さい");
// 水抜き穴が溝底の内側に入っていること
for (dx = drain_x)
    assert(dx - drain_d/2 >= grip_x0 && dx + drain_d/2 <= blk_w/2,
           str("水抜き穴 x=", dx, " が溝の範囲 [", grip_x0, ", ", blk_w/2, "] の外"));
assert(drain_d/2 + min_wall <= bore_r, "水抜き穴が溝底より広い");
// 結束スロットと M5 穴が X で離れていること (Y は近いので X で逃がす)
for (tx = tie_x)
    assert(abs(abs(tx) - mount_x/2) >= tie_w/2 + m5_d/2 + 1,
           str("結束スロット x=", tx, " と M5 穴 x=", mount_x/2, " が接近"));
assert(tie_y + tie_t/2 <= base_d/2 - 3, "結束スロットがベース縁に近すぎ");
// 胴長がクレードルに届くこと
assert(xdcr_len >= grip_len + end_t,
       str("胴長 ", xdcr_len, " がクレードル全長 ", grip_len + end_t, " に足りない"));

echo(str("[xdcr_clamp] 溝径 ", bore_d, " / 軸高さ(取付面から) ", axis_z,
         " / ベース ", base_w, "x", base_d, "x", base_t,
         " / マウント中心→放射面 ", face_off));

// ---- 本体 -------------------------------------------------------------
module clamp_body() {
    difference() {
        union() {
            translate([-base_w/2, -base_d/2, 0]) cube([base_w, base_d, base_t]);
            translate([blk_x0, -blk_d/2, 0])     cube([blk_w, blk_d, axis_z]);
        }
        // クレードル溝 (X軸の半円樋・上開放 → 無サポート)
        translate([grip_x0, 0, axis_z]) rotate([0, 90, 0])
            cylinder(d=bore_d, h=grip_len + 1);
        // ケーブル溝 (端壁を上から切り欠く。下側は胴の当り面として残す)
        translate([blk_x0 - 1, -cbl_w/2, axis_z - cbl_w/2])
            cube([end_t + 1, cbl_w, axis_z]);
        // 蓋ボルトの自己タップ下穴
        for (bx = bolt_x) for (sy = [-1, 1])
            translate([bx, sy*bolt_y, axis_z - pilot_dep])
                cylinder(d=m4_pilot, h=pilot_dep + 1);
        // M5 取付穴 ×4
        for (sx = [-1, 1]) for (sy = [-1, 1])
            translate([sx*mount_x/2, sy*mount_y/2, -0.5])
                cylinder(d=m5_d, h=base_t + 1);
        // 水抜き穴 (溝底 → 取付面)
        for (dx = drain_x)
            translate([dx, 0, -0.5]) cylinder(d=drain_d, h=base_t + 1);
        // 結束バンドスロット (予備保持: 蓋の上を回して締める)
        for (tx = tie_x) for (sy = [-1, 1])
            translate([tx - tie_w/2, sy*tie_y - tie_t/2, -0.5])
                cube([tie_w, tie_t, base_t + 1]);
    }
}

// ---- クランプ蓋 (印刷姿勢: 外面が下、溝が上) ---------------------------
module clamp_cap() {
    difference() {
        translate([blk_x0, -blk_d/2, 0]) cube([blk_w, blk_d, cap_h]);
        // 溝 (組立時は下向きになる)
        translate([grip_x0, 0, cap_h]) rotate([0, 90, 0])
            cylinder(d=bore_d, h=grip_len + 1);
        // ケーブル逃げ (本体側の溝と合わせて cbl_w 角の開口になる)
        translate([blk_x0 - 1, -cbl_w/2, cap_h - cbl_w/2])
            cube([end_t + 1, cbl_w, cap_h]);
        // 通し穴 + 頭座グリ (座グリは印刷時の底面側 = 組立時の外面)
        for (bx = bolt_x) for (sy = [-1, 1]) {
            translate([bx, sy*bolt_y, -0.5])  cylinder(d=m4_d,    h=cap_h + 1);
            translate([bx, sy*bolt_y, -0.01]) cylinder(d=m4_head, h=m4_cb);
        }
    }
}

if (part == "body") clamp_body();
else                clamp_cap();
