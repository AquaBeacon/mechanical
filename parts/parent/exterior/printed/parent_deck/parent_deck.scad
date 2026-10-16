// =====================================================================
// parent_deck.scad — 親機 デッキ (防水ボックス台 + 浮子クレードル取付 + 下面ハードポイント)
//
// 役割 (2026-09-04 人間決定: 浮子 2 個・支柱 (マスト) 無し・カメラは Osmo 外付け):
//   - タカチ BCAS212310G を上に載せ、箱底コーナーの外部取付穴 Ø4.2 ×4 (図面 E-E、
//     箱中心から (±96, ±106)) に上から M4 を通し、デッキの M4 熱圧入インサートで受ける
//   - 左右 (±X) の側壁外面に HP40 座 ×2/側 → parent_float_cradle (浮子クレードル) を
//     M5×4 ×2 で締結。クレードルを外せば同じ座に別のアクセサリを付けられる (拡張性)
//   - 下面中央のキール (2 枚壁 + 座 3 枚) の底面に HP40 座 ×3 (Y = -70 / 0 / +70)
//     → TD04A ソケット (xdcr_socket, 開口下向き)、Osmo 固定ジグ (後日)、予備
//   - 紐穴: 側壁両端 Ø8 (X 貫通) ×4 = 浮子端アイ / 吊り索の結び点
//   - 南縁 (Y-) の切欠き: 南壁ペネトレータ ×2 (箱 x=85/120 → デッキ X=-20/+15) から
//     降りるケーブルをデッキ下へ回す。キール南端の壁に Ø8 フェアリード ×2 (張力止め)
//
// 座標系: 箱中心 = 原点、デッキ上面 (= 箱底外面) z=0、+Y = 北 (箱の北壁側)。
//   箱座標 (x, y) → デッキ (x - 105, y - 115)。
// 印刷向き: **上下反転** (デッキ上面をベッドに)。側壁・キール壁・座がベッドから
//   立ち上がる。キール座 (t10) は壁間 34 mm を橋渡し (X1C ブリッジ可)。
//   側壁の軽量窓は 45° 屋根。PETG / 壁 4 / インフィル 25% / サポート不要。
// 規約: cube / cylinder / polygon + ブーリアンのみ (hull/offset 不使用)。
// =====================================================================

use <../../../../../scad/lib/hardpoint.scad>

/* [箱 (bcas212310g.md / .scad と二重定義)] */
box_x      = 210;    // カバー外形 X (箱底の胴体は約 204)
box_y      = 230;    // カバー外形 Y (同 約 224)
ear_x      = 96;     // 外部取付穴 Ø4.2 の中心 (箱中心基準, ±)。図面 (±106, ±96) → 本座標 (±96, ±106)
ear_y      = 106;
ear_hole_d = 4.2;    // 箱側の穴 (M4 通し)
pen_x      = [-20, 15];   // 南壁ペネトレータの X (箱 x=85/120 - 105)
pen_head_y = 22;          // ペネトレータ頭の南壁からの突出し (y = -137..-115)

/* [デッキ板] */
plate_x    = 216;
plate_y    = 236;
plate_t    = 6;

/* [箱固定: M4 熱圧入インサート (上から)] */
ear_pilot_d = 5.6;   // M4 インサート下穴
ear_pilot_h = 9;     // 深さ (インサート 8 + 1)

/* [側壁 (±X)。外面に HP40 座 ×2] */
lip_t      = 17;     // 板厚 (HP40 インサート 9 深 + 残り 8。箱取付穴 x=96 の下穴 Ø5.6 が板内に収まる下限 16)
lip_h      = 50;     // 高さ (= HP40 座 50)
hp_lip_y   = [-70, 70];   // 座中心 Y
hp_lip_z   = -25;         // 座中心 z (側壁の中央)
rope_d     = 8;      // 紐穴 (X 貫通)
rope_y     = 108;    // 紐穴中心 (±)
rope_z     = -35;
win_w      = 36;     // 軽量窓 (Y 幅)。45° 屋根の頂点 = win_z0 + win_h + win_w/2 が板下面より 4 下
win_h      = 14;     // 同 (Z 高さ、45° 屋根を含まない直壁部)
win_z0     = -44;    // 同 下端 z

/* [キール (下面中央)。底面に HP40 座 ×3] */
keel_wall_t = 8;
keel_wall_x = 16;    // 壁の内面 X (±) → 壁は X 16..24 (HP40 インサート穴 Ø6.4 @ ±20 が壁の真下に収まる)
keel_y      = 105;   // 壁の半長 (±)。座 (Y ±70, 50 角) の外側に端壁 6 + 余裕 2
keel_wall_z = -50;   // 壁下端 z (板下面 -6 から)
pad_t       = 10;    // 座板厚 (壁の下に架ける)
pad_w       = 50;    // 座の一辺 (HP_PAD)
hp_keel_y   = [-70, 0, 70];
end_wall_t  = 6;     // キール両端の壁 (フェアリード)
fair_d      = 8;
fair_x      = [-9, 9];
fair_z      = -30;

/* [南縁ケーブル切欠き] */
notch_x0   = -30;
notch_x1   = 25;
notch_d    = 8;      // Y 方向の深さ (南縁から)

/* [HP40 (hardpoint.scad と二重定義。use なので定数は見えない)] */
hp_pitch   = 40;
hp_ins_d   = 6.4;
hp_ins_h   = 8;
hp_pad     = 50;
hp_cable_d = 14;

$fn = 48;

// ---- 導出 -----------------------------------------------------------
lip_x0   = plate_x/2 - lip_t;          // 94 (側壁内面)
lip_x1   = plate_x/2;                  // 108 (側壁外面 = HP40 座面)
keel_z1  = keel_wall_z - pad_t;        // -60 (座面 z)
pad_z    = keel_z1;
box_body_x = box_x/2 - 3;              // 102 (箱底の胴体外面。カバーより 3 内側)
box_body_y = box_y/2 - 3;              // 112

// ---- 成立性チェック --------------------------------------------------
// 箱がデッキ板に載る / 外部取付穴が側壁 (インサート母材) の中にある
assert(plate_x >= box_x && plate_y >= box_y, "デッキ板が箱のカバー外形より小さい");
assert(ear_x - ear_pilot_d/2 > lip_x0 + 1 && ear_x + ear_pilot_d/2 < lip_x1 - 1,
       str("箱の取付穴が側壁の板厚に収まらない: ear_x=", ear_x, " lip ", lip_x0, "..", lip_x1));
assert(ear_y + ear_pilot_d/2 < plate_y/2 - 2, "箱の取付穴がデッキ端に近すぎる");
assert(ear_pilot_h < plate_t + lip_h - 2, "インサート下穴が側壁を突き抜ける");
// 側壁 HP40 座: 座が側壁に収まる / インサート穴が側壁を貫通しない
for (y = hp_lip_y) {
    assert(abs(y) + hp_pad/2 <= plate_y/2, "側壁 HP40 座が側壁からはみ出す");
    assert(hp_lip_z - hp_pad/2 >= -lip_h && hp_lip_z + hp_pad/2 <= 0, "側壁 HP40 座が側壁高さに収まらない");
}
assert(lip_t - (hp_ins_h + 1) >= 3, "側壁が薄い: HP40 インサート下穴の残り肉が 3 未満");
// フィーチャ表 (側壁の YZ 面): [Y, Z, 半径, 名前] — 総当りで離隔を検査
lip_feats = concat(
    [for (y = hp_lip_y, sy = [-1, 1], sz = [-1, 1]) [y + sy*hp_pitch/2, hp_lip_z + sz*hp_pitch/2, hp_ins_d/2, "hp40"]],
    [for (y = hp_lip_y) [y, hp_lip_z, hp_cable_d/2, "hp40_cable"]],
    [for (s = [-1, 1]) [s*rope_y, rope_z, rope_d/2, "rope"]],
    [for (s = [-1, 1]) [s*ear_y, -ear_pilot_h/2, max(ear_pilot_d/2, ear_pilot_h/2), "ear_insert"]]);
for (i = [0 : len(lip_feats) - 2]) for (j = [i + 1 : len(lip_feats) - 1]) {
    a = lip_feats[i]; b = lip_feats[j];
    d = sqrt(pow(a[0] - b[0], 2) + pow(a[1] - b[1], 2));
    assert(d >= a[2] + b[2] + 3, str("側壁フィーチャが接近: ", a[3], " vs ", b[3], " (", d, ")"));
}
// 軽量窓は座・穴と離れていること
assert(win_w/2 + 3 < min([for (y = hp_lip_y) abs(y)]) - hp_pad/2, "軽量窓が HP40 座に掛かる");
assert(win_z0 >= -lip_h + 4, "軽量窓が側壁下端に近すぎる");
assert(win_z0 + win_h + win_w/2 <= -plate_t - 4, "軽量窓の 45° 屋根の頂点がデッキ板に近すぎる");
// キール: 座が壁の間に架かる / 座の HP40 インサート穴が壁の中にある / 端壁が座と重ならない
assert(pad_w/2 >= keel_wall_x + keel_wall_t - 0.01, "キール座が壁の外まで届いていない");
assert(hp_pitch/2 - hp_ins_d/2 >= keel_wall_x - 0.01 && hp_pitch/2 + hp_ins_d/2 <= keel_wall_x + keel_wall_t + 0.01,
       "キール座のインサート穴が壁の真下に無い (母材不足)");
for (y = hp_keel_y) assert(abs(y) + pad_w/2 <= keel_y - end_wall_t - 2, "キール座が端壁に掛かる");
for (i = [0 : len(hp_keel_y) - 2])
    assert(hp_keel_y[i+1] - hp_keel_y[i] >= pad_w + 10, "キール座同士が近い (ケーブルの逃げ 10 未満)");
assert(pad_t >= hp_ins_h + 1, "キール座がインサート深さより薄い");
assert(keel_wall_x + keel_wall_t < lip_x0 - 20, "キールと側壁の間が狭い");
for (x = fair_x) assert(abs(x) + fair_d/2 < keel_wall_x - 1, "フェアリード穴がキール壁に掛かる");
assert(fair_z - fair_d/2 > keel_wall_z + 2 && fair_z + fair_d/2 < -plate_t - 2, "フェアリード穴の高さが端壁に収まらない");
// 南縁切欠き: 箱の胴体壁の下を 3 mm 以上残す (箱の縁はデッキに載る) / ペネトレータ直下を覆う
assert(plate_y/2 - notch_d >= box_body_y - 3, "切欠きが箱の胴体壁の下に深く入りすぎ");
for (x = pen_x) assert(x > notch_x0 + 5 && x < notch_x1 - 5, str("ペネトレータ x=", x, " が切欠きの外"));
assert(notch_x1 < lip_x0 - 5 && notch_x0 > -lip_x0 + 5, "切欠きが側壁に掛かる");
// 250³ 造形枠
assert(plate_x <= 250 && plate_y <= 250 && (plate_t + lip_h + 0) <= 250, "X1C 250 枠を超える");

// 機械可読な穴表 (デッキ座標)
echo(str("parent_deck: HOLETABLE ear_M4_insert=", [for (sx=[-1,1], sy=[-1,1]) [sx*ear_x, sy*ear_y, 0]],
         " hp40_lip(face x=±", lip_x1, ")=", [for (s=[-1,1], y=hp_lip_y) [s*lip_x1, y, hp_lip_z]],
         " hp40_keel(face z=", pad_z, ")=", [for (y=hp_keel_y) [0, y, pad_z]],
         " rope(dia ", rope_d, ")=", [for (s=[-1,1], t=[-1,1]) [s*lip_x1, t*rope_y, rope_z]]));
echo(str("parent_deck: bbox ", plate_x, " x ", plate_y, " x ", plate_t - keel_z1, " (z ", keel_z1, "..0)"));

// ---- 本体 -------------------------------------------------------------
module lip_window() {   // 45° 屋根の軽量窓 (X 貫通)。Y-Z 平面の多角形を X に押出す
    rotate([90, 0, 90])
        linear_extrude(height = lip_t + 2, center = true)
            polygon([[-win_w/2, win_z0], [win_w/2, win_z0], [win_w/2, win_z0 + win_h],
                     [0, win_z0 + win_h + win_w/2], [-win_w/2, win_z0 + win_h]]);
}

difference() {
    union() {
        // デッキ板
        translate([-plate_x/2, -plate_y/2, -plate_t]) cube([plate_x, plate_y, plate_t]);
        // 側壁 ×2 (±X)
        for (s = [-1, 1])
            translate([s > 0 ? lip_x0 : -lip_x1, -plate_y/2, -lip_h]) cube([lip_t, plate_y, lip_h]);
        // キール壁 ×2 + 端壁 ×2
        for (s = [-1, 1])
            translate([s > 0 ? keel_wall_x : -(keel_wall_x + keel_wall_t), -keel_y, keel_wall_z])
                cube([keel_wall_t, 2*keel_y, -keel_wall_z - plate_t]);
        for (s = [-1, 1])
            translate([-(keel_wall_x + keel_wall_t), s > 0 ? keel_y - end_wall_t : -keel_y, keel_wall_z])
                cube([2*(keel_wall_x + keel_wall_t), end_wall_t, -keel_wall_z - plate_t]);
        // キール座 ×3 (壁の下に架ける)
        for (y = hp_keel_y)
            translate([-pad_w/2, y - pad_w/2, pad_z]) cube([pad_w, pad_w, pad_t]);
    }
    // 箱固定 M4 インサート下穴 (上から) ×4
    for (sx = [-1, 1]) for (sy = [-1, 1])
        translate([sx*ear_x, sy*ear_y, -ear_pilot_h]) cylinder(d = ear_pilot_d, h = ear_pilot_h + 1);
    // 側壁 HP40 座 ×4 (外面法線 = ±X)。hardpoint.scad のローカル +Z を ±X へ
    for (s = [-1, 1]) for (y = hp_lip_y)
        translate([s*lip_x1, y, hp_lip_z]) rotate([0, s*90, 0]) {
            hp40_cut(cable = true, through_t = lip_t + 2, insert_h = hp_ins_h);
            hp40_arrow();
        }
    // 側壁 紐穴 ×4 (X 貫通)
    for (s = [-1, 1]) for (t = [-1, 1])
        translate([s*(lip_x0 + lip_t/2), t*rope_y, rope_z]) rotate([0, 90, 0])
            cylinder(d = rope_d, h = lip_t + 2, center = true);
    // 側壁 軽量窓 ×2
    for (s = [-1, 1]) translate([s*(lip_x0 + lip_t/2), 0, 0]) lip_window();
    // キール座 HP40 ×3 (座面法線 = -Z)。中央 Ø14 は座板を貫通してキール内へ
    for (y = hp_keel_y)
        translate([0, y, pad_z]) rotate([180, 0, 0]) {
            hp40_cut(cable = true, through_t = pad_t + 2, insert_h = hp_ins_h);
            hp40_arrow();
        }
    // キール端壁 フェアリード ×2/端 (Y 貫通)
    for (s = [-1, 1]) for (x = fair_x)
        translate([x, s*(keel_y - end_wall_t/2), fair_z]) rotate([90, 0, 0])
            cylinder(d = fair_d, h = end_wall_t + 2, center = true);
    // 南縁ケーブル切欠き
    translate([notch_x0, -plate_y/2 - 1, -plate_t - 1]) cube([notch_x1 - notch_x0, notch_d + 1, plate_t + 2]);
}
