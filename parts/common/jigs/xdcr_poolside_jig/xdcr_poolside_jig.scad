// =====================================================================
// xdcr_poolside_jig.scad — TD04A プールサイド L 字治具 (実験用)
// プールの縁にまたがせ、デッキ側の水平板におもりを載せて押さえる。
// 支柱がプール内壁に沿って下り、下端の水平棚に xdcr_clamp を M5×4 で
// 載せる。棚には 0°/90° の 2 組のボルトパターンがあり、音響ビームを
// 壁に対して垂直 (対面測距) にも平行 (同一壁面上での測距) にも向けられる。
//
//   part="hook" : デッキ板 + 縁の立ち上がり/ガセット + 支柱 (上半分)
//   part="foot" : 立ち下がり (下半分) + 振動子棚
//   2 つを重ね継ぎ (foot が hook の池側面に重なる) して M5×4 で締結する。
//   2 分割なのは、必要な水深 (デッキ面下 ~290mm) が印刷ベッドに載らないため。
//
// 座標系: X = 幅(0 が中心) / Y = プール方向(+Y が水側、Y=0 が壁面) /
//         Z = 0 がデッキ面、下が -Z。
// 印刷向き: hook / foot とも「幅 X を Z 方向に立てて」印刷する。
//   断面 (YZ の L 形) がそのままベッドに載り、全層が同じ断面になるので
//   サポートは一切要らず、曲げ荷重も層内で受けられる。
//   → スライサで X 軸まわりに 90° 回してから配置すること。
// 要実測: lip_y(縁のせり出し) / freeboard(デッキ面→水面) / TD04A 実寸
// =====================================================================

/* [部品選択] */
part      = "hook";   // [hook, foot]

/* [プール縁 (要実測)] */
lip_y     = 0;        // 縁のせり出し量。壁面 Y=0 に対し支柱をこれだけ外に出す
                      // (オーバーフロー溝の庇/グレーチングがある場合はその幅)
freeboard = 100;      // デッキ面 → 水面 (深さの計算・表示にのみ使う)
corner_rl = 4;        // 縁の丸み逃げ (支柱の壁側かどをこれだけ欠く)

/* [共通] */
width     = 90;       // 幅 (X) ※印刷時はこれが Z 高さになる
plate_t   = 12;       // 構造板厚 (支柱 / 立ち下がり / 棚)
deck_t    = 8;        // デッキ板厚 (下は地面なので薄くてよい)
m5_d      = 5.3;      // M5 クリアランス穴
m5_wash   = 10;       // M5 平座金の外径 (干渉チェック用)

/* [hook: デッキ側] */
deck_len  = 150;      // デッキ板の長さ (Y、縁から陸側へ)
gus_run   = 40;       // ガセットがデッキ板を這う長さ
gus_rise  = 40;       // 縁の立ち上がり高さ (おもりのプール側ストッパ兼用)
rib_t     = 10;       // 陸側端リブの厚み (おもりの陸側ストッパ)
rib_h     = 25;       // 同 高さ
hook_drop = 150;      // デッキ面 → 支柱下端
strap_y   = [-55, -120];  // おもり固定ストラップのスロット中心 Y
strap_w   = 30;       // スロット長 (X)
strap_t   = 5;        // スロット幅 (Y)
lany_d    = 8;        // 安全ロープ穴
lany_y    = -130;

/* [継手 (hook ⇄ foot の重ね継ぎ)] */
lap_len   = 60;       // 重ね代
lap_x     = 25;       // 継手ボルトの X (±)
lap_edge  = 10;       // 重ね代の端 → 一番端のボルト中心
lap_dz    = 40;       // 継手ボルトの Z 間隔

/* [foot: 棚側] */
foot_rise = 200;      // foot の全高 (継手上端 → 棚下面)
foot_len  = 90;       // 棚の張り出し (Y)

/* [xdcr_clamp とのインタフェース ※向こうの値と一致させること] */
mount_x   = 40;       // xdcr_clamp の M5 ピッチ X
mount_y   = 68;       // 同 Y
clamp_bw  = 56;       // xdcr_clamp の base_w (X)
clamp_bd  = 84;       // 同 base_d (Y)
clamp_axz = 20.5;     // 同 取付面 → 振動子軸 (base_t + bore_d/2)
clamp_fx  = 38;       // 同 マウント中心 → 音響放射面 (grip_x0 + xdcr_len)
beam_deg  = 22;       // TD04A 指向角 (全角)

/* [xdcr_socket も載せられるようにする] */
sock_p    = 40;       // xdcr_socket の hole_p と一致 (40 角)

/* [ケーブル固定] */
tie_w     = 5.5;      // 結束バンド幅 (4.8mm 帯)
tie_t     = 2.5;      // 同 厚み
hook_tz   = [-25, -55, -80];    // hook 支柱のスロット Z
foot_tz   = [-180, -240];       // foot 立ち下がりのスロット Z

/* [印刷ベッド] */
bed_xy    = 220;      // ベッド一辺 (断面がこれに収まること)
bed_h     = 250;      // ビルド高さ (width がこれに収まること)

$fn = 64;

// ---- 導出寸法 ---------------------------------------------------------
arm_y0   = lip_y;                 // 支柱の壁側面
arm_y1   = arm_y0 + plate_t;      // 支柱の池側面 (= 継手面)
deck_y0  = arm_y0 - deck_len;     // デッキ板の陸側端
post_top = deck_t + gus_rise;     // 縁の立ち上がり天端

foot_y0  = arm_y1;                // foot 立ち下がりの壁側面 (継手で重なる)
foot_y1  = foot_y0 + plate_t;     // 同 池側面
foot_top = -hook_drop + lap_len;  // foot の上端 Z
shelf_tz = foot_top - foot_rise + plate_t;   // 棚の上面 Z (= xdcr_clamp 取付面)
shelf_y0 = foot_y1;
shelf_y1 = foot_y1 + foot_len;
shelf_cy = (shelf_y0 + shelf_y1)/2;          // 棚の中心 Y (= マウント中心)

lap_z    = [-hook_drop + lap_edge, -hook_drop + lap_edge + lap_dz];

axis_z   = shelf_tz + clamp_axz;             // 振動子軸 (デッキ面基準)
depth_dk = -axis_z;                          // デッキ面下の深さ
depth_wt = depth_dk - freeboard;             // 水面下の深さ
face_y   = shelf_cy + clamp_fx;              // 放射面の Y (0° 取付時)

// 断面 (印刷時にベッドへ載る面) の大きさ
hook_py  = arm_y1 - deck_y0;
hook_pz  = hook_drop + post_top;
foot_py  = plate_t + foot_len;
foot_pz  = foot_rise;

// 棚のボルト穴 (棚中心からの相対座標)
shelf_holes = concat(
    [for (sx=[-1,1], sy=[-1,1]) [sx*mount_x/2, sy*mount_y/2]],   // xdcr_clamp 0°
    [for (sx=[-1,1], sy=[-1,1]) [sx*mount_y/2, sy*mount_x/2]],   // xdcr_clamp 90°
    [for (sx=[-1,1], sy=[-1,1]) [sx*sock_p/2,  sy*sock_p/2]]);   // xdcr_socket

// ---- 干渉チェック -----------------------------------------------------
// 印刷ベッド
assert(hook_py <= bed_xy && hook_pz <= bed_xy,
       str("hook の断面 ", hook_py, " x ", hook_pz, " がベッド ", bed_xy, " 角に載らない"));
assert(foot_py <= bed_xy && foot_pz <= bed_xy,
       str("foot の断面 ", foot_py, " x ", foot_pz, " がベッド ", bed_xy, " 角に載らない"));
assert(width <= bed_h, "width がビルド高さを超える");

// 継手
assert(lap_len >= 4*plate_t, "重ね代が板厚の4倍未満。継手が効かない");
assert(hook_drop > lap_len + 40, "支柱が短く、重ね代でほぼ埋まってしまう");
assert(lap_edge >= m5_d/2 + 4, "継手ボルトの端距離不足");
assert(lap_edge + lap_dz + m5_d/2 + 4 <= lap_len, "継手ボルトが重ね代からはみ出す");
assert(lap_x + m5_wash/2 + 4 <= width/2, "継手ボルトの座金が幅からはみ出す");
// 支柱の結束スロットは中央、継手ボルトは端 → X で離れていること
assert(lap_x - m5_d/2 >= tie_w/2 + 3, "継手ボルトと結束スロットが接近");
for (tz = hook_tz)
    assert(tz > -hook_drop + lap_len + 2,
           str("hook の結束スロット z=", tz, " が継手の重ね代に隠れる"));
for (tz = foot_tz)
    assert(tz < foot_top - lap_len - 2 && tz > shelf_tz + 10,
           str("foot の結束スロット z=", tz, " が継手/棚に掛かる"));

// デッキ板まわり
assert(corner_rl < plate_t - 4, "縁の丸み逃げが深すぎて支柱が痩せる");
assert(corner_rl < deck_t, "縁の丸み逃げがデッキ板厚以上");
for (sy = strap_y) {
    assert(sy + strap_t/2 < arm_y0 - gus_run - 3,
           str("ストラップスロット y=", sy, " がガセットの下に潜って抜けない"));
    assert(sy - strap_t/2 > deck_y0 + rib_t + 3,
           str("ストラップスロット y=", sy, " が端リブに掛かる"));
}
assert(lany_y - lany_d/2 > deck_y0 + rib_t + 2, "安全ロープ穴が端リブに掛かる");
for (sy = strap_y)
    assert(abs(lany_y - sy) >= lany_d/2 + strap_t/2 + 2,
           "安全ロープ穴とストラップスロットが接近");
assert(deck_len - rib_t - gus_run >= 80, "おもりを置く平面が狭すぎる");
assert(strap_w + 2*4 <= width, "ストラップスロットの X 縁距離不足");

// 棚 (ボルト穴同士・縁距離・立ち下がりとの逃げ)
for (i = [0:len(shelf_holes)-2]) for (j = [i+1:len(shelf_holes)-1])
    assert(norm(shelf_holes[i] - shelf_holes[j]) >= m5_d + 3,
           str("棚のボルト穴が接近: ", shelf_holes[i], " と ", shelf_holes[j]));
for (h = shelf_holes) {
    assert(abs(h[0]) + m5_d/2 + 4 <= width/2,
           str("棚のボルト穴 ", h, " の X 縁距離不足"));
    assert(abs(h[1]) + m5_d/2 + 4 <= foot_len/2,
           str("棚のボルト穴 ", h, " の Y 縁距離不足 (foot_len を増やす)"));
    // 座金が立ち下がりの根元に乗り上げないこと
    assert(foot_len/2 + h[1] - m5_wash/2 >= 2,
           str("棚のボルト穴 ", h, " の座金が立ち下がりに干渉"));
}
// xdcr_clamp のベースが棚に収まること (0° / 90° 両方)
assert(clamp_bw <= foot_len - 4 && clamp_bd + 4 <= width,
       str("xdcr_clamp のベース ", clamp_bw, "x", clamp_bd, " が棚に収まらない"));
assert(clamp_bd <= foot_len - 4 && clamp_bw + 4 <= width,
       "xdcr_clamp を 90° 回すと棚に収まらない");
// 音響ビーム (半角 beam_deg/2) が棚の前縁に当たらないこと
assert(clamp_axz > (foot_len/2 - clamp_fx) * tan(beam_deg/2),
       str("棚の前縁が音響ビームに掛かる: 軸高さ ", clamp_axz, " < ",
           (foot_len/2 - clamp_fx) * tan(beam_deg/2)));

echo(str("[xdcr_poolside_jig] 総ドロップ(デッキ面→棚下面) ", -shelf_tz + plate_t,
         " / 振動子軸 デッキ面下 ", depth_dk, " (水面下 ", depth_wt, ")",
         " / 壁面→放射面 ", face_y,
         " / 断面 hook ", hook_py, "x", hook_pz, " foot ", foot_py, "x", foot_pz));

// ---- モジュール -------------------------------------------------------
// YZ 平面の直角三角形 (0,0)-(-run,0)-(0,rise) を +X へ w 押し出す
module gusset_yz(run, rise, w) {
    rotate([90, 0, 90])
        linear_extrude(height = w)
            polygon([[0, 0], [-run, 0], [0, rise]]);
}

// 板を Y 方向に貫く結束バンドスロット (X 中央、高さ z)
module tie_slot(y0, z, th) {
    translate([-tie_w/2, y0 - 0.5, z - tie_t/2]) cube([tie_w, th + 1, tie_t]);
}

// 継手ボルト穴 ×4 (Y 方向に貫通)
module lap_bolts(y0, th) {
    for (sx = [-1, 1]) for (z = lap_z)
        translate([sx*lap_x, y0 - 0.5, z]) rotate([-90, 0, 0])
            cylinder(d=m5_d, h=th + 1);
}

// ---- hook (デッキ板 + 縁の立ち上がり + 支柱上半分) ---------------------
module hook() {
    difference() {
        union() {
            // デッキ板
            translate([-width/2, deck_y0, 0])
                cube([width, arm_y1 - deck_y0, deck_t]);
            // 支柱 (下端 → 縁の立ち上がり天端)
            translate([-width/2, arm_y0, -hook_drop])
                cube([width, plate_t, hook_drop + post_top]);
            // ガセット (立ち上がり ⇄ デッキ板)
            translate([-width/2, arm_y0, deck_t]) gusset_yz(gus_run, gus_rise, width);
            // 陸側端リブ (おもりのストッパ)
            translate([-width/2, deck_y0, 0]) cube([width, rib_t, rib_h]);
        }
        // 縁の丸み逃げ (支柱の壁側かど)
        translate([-width/2 - 0.5, arm_y0 - 0.5, -corner_rl])
            cube([width + 1, corner_rl + 0.5, corner_rl + 0.5]);
        // おもり固定ストラップのスロット
        for (sy = strap_y)
            translate([-strap_w/2, sy - strap_t/2, -0.5])
                cube([strap_w, strap_t, deck_t + 1]);
        // 安全ロープ穴 (治具ごと落とさないための命綱)
        translate([0, lany_y, -0.5]) cylinder(d=lany_d, h=deck_t + 1);
        // 継手ボルト
        lap_bolts(arm_y0, plate_t);
        // ケーブル結束スロット
        for (tz = hook_tz) tie_slot(arm_y0, tz, plate_t);
    }
}

// ---- foot (立ち下がり下半分 + 振動子棚) --------------------------------
module foot() {
    difference() {
        union() {
            // 立ち下がり (上端 lap_len 分が hook の池側面に重なる)
            translate([-width/2, foot_y0, shelf_tz - plate_t])
                cube([width, plate_t, foot_rise]);
            // 振動子棚
            translate([-width/2, shelf_y0, shelf_tz - plate_t])
                cube([width, foot_len, plate_t]);
        }
        // 継手ボルト
        lap_bolts(foot_y0, plate_t);
        // ケーブル結束スロット
        for (tz = foot_tz) tie_slot(foot_y0, tz, plate_t);
        // 取付穴 (xdcr_clamp 0°/90° + xdcr_socket)。水抜きも兼ねる
        for (h = shelf_holes)
            translate([h[0], shelf_cy + h[1], shelf_tz - plate_t - 0.5])
                cylinder(d=m5_d, h=plate_t + 1);
    }
}

if (part == "hook") hook();
else                foot();
