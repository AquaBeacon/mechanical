// =====================================================================
// child_osmo_holder.scad — 子機 Osmo Action 6 防水ケース ホルダ (2セット)
//
// DJI Osmo Action 6 + 純正防水ケース(60m) を child_osmo_arm の
// GoPro互換2フィンガーに固定する。下向き 20° を部品側に作り込むので
// GoProナックルは不要 (アーム側は水平のまま)。
//
// 座標系: 原点 = ピン軸中心。X = ピン軸 = 基線方向 (外向き)、
//         Y = 前後 (+Y が前 = レンズが向く側)、Z = 上。設置姿勢のまま。
//         アセンブリでは translate([base_line, 0, arm_t + arm_pin_z]) で載る。
//
// バリアント: part="cradle" (クレードル本体) / part="strap" (上ストラップ)
// 印刷向き: 後壁の外面を下にして寝かせる (下部の「印刷向き」コメント参照)。
// =====================================================================

part = "cradle";   // "cradle" | "strap"

/* [相手部品: child_osmo_arm と一致させること (二重定義)] */
arm_fin_t    = 3.0;    // アーム側フィンガー厚
arm_fin_gap  = 3.4;    // アーム側フィンガー間隔 (ここに中央プロングが入る)
arm_fin_w    = 15;     // アーム側フィンガー奥行(Y)
arm_fin_h    = 16;     // アーム側フィンガー高さ (ビーム上面から)
arm_t        = 6;      // アーム板厚 (= ビーム上面の高さ)
arm_pin_z    = 10;     // ピン中心高さ (ビーム上面から)
arm_beam_w   = 40;     // アーム ビーム幅(Y)
arm_rib_t    = 4;      // アーム 縁リブ厚
arm_rib_h    = 10;     // アーム 縁リブ高さ (ビーム上面から)
arm_pitch    = 25;     // フィンガー位置ピッチ (125/150/175)
base_line_min = 125;   // 最内フィンガーの X (基線 250 のとき)
pin_d        = 5.2;    // M5 ノブボルト穴 (アームと同じ)

/* [耐圧チューブとクランプ: child_clamp_base / placement.json と一致 (二重定義)] */
tube_od      = 114.3;  // 干渉チェック用にだけ使う
clamp_y      = 60;     // 前後チューブクランプの Y 位置(±)  ← placement.json
clamp_band   = 26;     // クランプのサドル/ボルト柱の Y 幅 (saddle_d / band_w)
// クランプのボルト柱は X=±90 まで伸びていて、ホルダ (最内基線で X=64〜186) と
// **X 方向では必ず重なる**。したがって Y 方向で逃げ切る必要がある。

/* [防水ケース: DJI Osmo Action 6 防水ケース — 公称値。要実測] */
// DJI 公称 94.7 x 45.9 x 84.1 mm。どの軸がどれかは公称表記が
// カメラ本体と揃っていないため、下記のように解釈している (要現物確認)。
case_w    = 94.7;   // X = 基線方向 (ケースの一番長い辺)
case_d    = 45.9;   // Y = 前後 (レンズ〜背面)
case_h    = 84.1;   // Z = 上下。**底面のクイックリリースタブを含む全高**
tab_w     = 40;     // 底面タブの X 幅   (仮値・要実測)
tab_h     = 18;     // 底面タブの突出高さ (仮値・要実測)
lens_z    = 52;     // ケース底面からレンズ中心までの高さ (仮値・要実測)
fov_half  = 77.5;   // 対角画角 155° の半値 (DJI 公称 FOV 155°)

/* [はめあい・クランプ] */
fit_c     = 0.6;    // ケース周りのクリアランス(片側)
pad_t     = 2.0;    // クランプ面に貼る EVA/ゴムシート厚
preload   = 0.8;    // シート圧縮による締め代
tab_clear = 1.5;    // 底面タブと床上面のすきま

/* [クレードル] */
wall      = 5;      // 端壁・後壁の肉厚
floor_t   = 6;      // 床板厚
rear_h    = 40;     // 後壁の高さ (床上面から)
front_t   = 4;      // 前リップ厚 (レンズ画角に入るので薄く)
front_h   = 31.5;   // 前リップ高さ (床上面から)
lip_len   = 22;     // 前リップの長さ (端壁側から内側へ)
rail_x0   = 22;     // 床レールの内側 X (底面タブの外)
boss_x    = 8;      // 端壁外面のボルト柱の張出し(X)
boss_y    = 20;     // 同 Y 幅
win_w     = 40;     // 後壁の肉抜き窓 (X)
win_h     = 22;     // 同 (Z)
drain_d   = 5;      // 床の水抜き穴
drain_x   = [8, 16];   // 同 X 位置(±)。レール(±rail_x0)より内側に置く
drain_y   = 20.5;   // 同 Y 位置(±)。ステム奥行(±stem_d/2)の外に出す

/* [ジョイント (プロング・ヨーク・足)] */
fit_j     = 0.4;    // GoProジョイントのクリアランス(合計)
prong_r   = 10;     // プロング半径 (ピン中心)
prong_bot = 1.0;    // プロング下端とビーム上面のすきま
yoke_gap  = 2.0;    // ヨーク下面とアームフィンガー上端のすきま
yoke_z1   = 20;     // ヨーク上面 (ピン中心基準)
foot_y0   = 9.0;    // 足の内側 Y (アームフィンガーの外)
foot_y1   = 15.0;   // 足の外側 Y (アーム縁リブの内)

/* [ステム] */
stem_z    = 30;     // ピン中心 → クレードル床上面 の高さ
stem_y    = -14;    // 同 前後オフセット (重心をピンに寄せる)
stem_w    = 34;     // ステム幅(X)
stem_len  = 14;     // ステム長さ (床下面から下へ。長すぎると前下角がフィンガーに当たる)
stem_d    = 34;     // ステム奥行(Y)
gus_leg   = 12;     // 床下ガセットの脚長
gus_t     = 6;      // 同 厚さ
gus_y     = 12;     // 同 Y 位置(±)

/* [ストラップ] */
strap_t   = 7;      // ストラップ肉厚
strap_w   = 26;     // ストラップ幅(Y)
strap_y   = -8;     // ストラップ中心 Y (ケース上面のラッチを避ける)
m4_d      = 4.5;    // M4 クリアランス
head_d    = 8.5;    // M4 頭径 + 余裕
head_t    = 4.5;    // 座グリ深さ
nut_w     = 7.8;    // M4 ナット二面幅 + 余裕
nut_t     = 3.6;    // ナットスロット厚
nut_drop  = 18;     // 端壁上面 → ナットスロットまでの深さ

tilt      = 20;     // 下向き角 (X軸まわり)

$fn = 64;
// union する立体どうしは必ず ov だけ食い込ませる。面どうしがちょうど接する
// (体積の重なりが 0 の) union は STL に開いたエッジを残すことがある。
ov  = 1.0;

// ---- 導出: アーム形状をホルダ座標へ ----------------------------------
beam_top_z = -arm_pin_z;                    // ビーム上面 (= 足の着座面) -10
fin_top_z  = arm_fin_h - arm_pin_z;         // アームフィンガー上端      +6
fin_y      = arm_fin_w / 2;                 // 同 Y 半幅                7.5
rib_in_y   = arm_beam_w / 2 - arm_rib_t;    // 縁リブ内側 Y             16
rib_top_z  = arm_rib_h - arm_pin_z;         // 縁リブ上端                0
adj_fin_x  = arm_pitch - (arm_fin_gap / 2 + arm_fin_t);  // 隣フィンガー内側X 20.3

// ---- 導出: プロング (アームの2フィンガーと噛み合う3枚) ---------------
prong_t     = arm_fin_gap - fit_j;              // 3.0 : アームの隙間に入る
prong_gap   = arm_fin_t  + fit_j;               // 3.4 : アームの爪を受ける
prong_pitch = prong_t + prong_gap;              // 6.4
stack_w     = 3 * prong_t + 2 * prong_gap;      // 15.8
prong_z0    = beam_top_z + prong_bot;           // プロング下端 -9
yoke_z0     = fin_top_z + yoke_gap;             // ヨーク下面   +8

// ---- 導出: ケースとクレードル ----------------------------------------
rail_h  = tab_h + tab_clear;              // レール上面 = ケース肩の高さ 19.5
body_h  = case_h - tab_h;                 // ケース本体高さ (肩から上)  66.1
cav_w   = case_w + 2 * fit_c;             // 95.9
cav_d   = case_d + 2 * fit_c;             // 47.1
wall_h  = rail_h + body_h + pad_t - preload;   // 端壁上面 (床上面から) 86.8
out_w   = cav_w + 2 * wall;               // 端壁外面まで 105.9
out_d   = cav_d + 2 * wall;               // 57.1
max_w   = cav_w + 2 * (wall + boss_x);    // ボルト柱を含む最大幅 121.9
m4_x    = cav_w / 2 + wall + boss_x / 2;  // ボルト中心 X 56.95
case_bot_z = rail_h - tab_h;              // ケース底面 (床上面基準) 1.5
lens_zz    = case_bot_z + lens_z;         // レンズ中心高さ (床上面基準)
front_y    = cav_d / 2;                   // ケース前面 = 前リップ内面

// 傾斜フレーム (y,z) → ピン中心基準の Z / Y。y が前(+)ほど下がる。
function tz(y, z) = stem_z - y * sin(tilt) + z * cos(tilt);
function ty(y, z) = stem_y + y * cos(tilt) + z * sin(tilt);
// ホルダの前後端 (後端 = 床の後下角、前端 = 端壁の前上角)
hold_y_aft  = ty(-out_d / 2, -floor_t);
hold_y_fwd  = ty( out_d / 2, wall_h);
// クレードル床下面の最低点 (前下角)
floor_low_z = tz(out_d / 2, -floor_t);
// ステム下端の最低点 (前下角)。ここが自分の載るフィンガー上端に最も近い。
stem_low_z  = tz(stem_d / 2, -stem_len);
// 床下ガセットが隣のフィンガー X 位置まで垂れ下がる量と、その最低点
gus_over    = max(0, gus_leg - (adj_fin_x - stem_w / 2));
gus_low_z   = tz(gus_y + gus_t / 2, -(floor_t + gus_over));
// 前リップ内側上角がレンズ光軸となす角 (対角で最も小さくなる点)
lip_in_x    = cav_w / 2 - lip_len;
lip_ang     = atan(sqrt(pow(lip_in_x, 2) + pow(lens_zz - front_h, 2)) / front_t);

// ---- 干渉・成立性チェック --------------------------------------------
// ジョイント
assert(prong_t > 2.0, "中央プロングが薄すぎる: fit_j を減らすか arm_fin_gap を確認");
assert(prong_r > arm_pin_z - prong_bot,
       "プロング半径がビーム上面に届かない(下端が浮く)");
assert(prong_r > pin_d / 2 + 3, "ピン穴まわりの肉厚不足");
assert(yoke_z0 > fin_top_z + 1.5, "ヨーク下面がアームのフィンガー上端に干渉");
assert(yoke_z1 > yoke_z0 + 6, "ヨークが薄すぎる");
// 足 (アームのビーム上面に着座して 20° を出す回り止め)
assert(foot_y0 > fin_y + 1.0, "足がアームのフィンガーに干渉");
assert(foot_y1 < rib_in_y - 0.8, "足がアームの縁リブに干渉");
assert(foot_y1 > foot_y0 + 4, "足の幅不足");
// 隣の未使用フィンガー (基線を変えても当たらないこと)
assert(stem_w / 2 < adj_fin_x - 2, "ステムが隣のフィンガーに干渉");
assert(floor_low_z > fin_top_z + 2, "クレードル床が隣のフィンガーに干渉");
assert(gus_low_z  > fin_top_z + 2, "床下ガセットが隣のフィンガーに干渉");
assert(stem_low_z > fin_top_z + 2, "ステム前下角が自分の載るフィンガー上端に干渉");
assert(stem_low_z < yoke_z1, "ステムがヨークに届かない(union が分離する)");
assert(floor_low_z > rib_top_z + 3, "クレードル床がアームの縁リブに干渉");
// ケース保持
assert(rail_x0 > tab_w / 2 + 1.5, "床レールが底面タブに干渉");
assert(cav_w / 2 - rail_x0 > 8, "床レールの幅不足");
assert(front_h < rail_h + 20, "前リップが高すぎる(ケース本体を覆う)");
assert(win_h < rear_h - 10, "後壁の肉抜き窓が高すぎる");
assert(win_w / 2 < rail_x0 - 1, "後壁の肉抜き窓が床レールを削る");
// 水抜き穴: ステムの真上を外し、レールも削らないこと
assert(drain_y - drain_d / 2 > stem_d / 2 + 0.5, "水抜き穴がステムで塞がれる");
assert(drain_y + drain_d / 2 < cav_d / 2, "水抜き穴がキャビティ外へ抜ける");
assert(max(drain_x) + drain_d / 2 < rail_x0 - 1, "水抜き穴が床レールを削る");
// カメラ画角 (155°)。ケース前面より前に出る構造は前リップだけ。
assert(lip_ang > fov_half + 2,
       str("前リップがレンズ画角に入る: ", lip_ang, "° <= ", fov_half + 2, "°"));
assert(front_y + front_t < front_y + 6, "前リップが厚すぎる(画角)");
// ボルト・ナット
assert(wall + boss_x - nut_w > 2.0, "ボルト柱がナット二面幅に対して薄い");
assert(m4_x - m4_d / 2 > cav_w / 2 + 1.0, "M4 穴が内側キャビティに抜ける");
assert(nut_drop > head_t + 4 && nut_drop < wall_h - 10, "ナットスロット位置が不適");
// 耐圧チューブ (最内基線 250 のとき)
assert(base_line_min - max_w / 2 > tube_od / 2 + 1.5,
       str("最内基線でケースが耐圧チューブと干渉: すきま ",
           base_line_min - max_w / 2 - tube_od / 2, "mm"));
// 前後のチューブクランプ (ボルト柱が X=±90 まで来るので Y で逃げる)
assert(hold_y_aft > -(clamp_y - clamp_band / 2) + 2,
       str("ホルダ後端が後方チューブクランプに干渉: すきま ",
           hold_y_aft + clamp_y - clamp_band / 2, "mm"));
assert(hold_y_fwd <  (clamp_y - clamp_band / 2) - 2,
       str("ホルダ前端が前方チューブクランプに干渉: すきま ",
           clamp_y - clamp_band / 2 - hold_y_fwd, "mm"));

// =====================================================================
// 部品
// =====================================================================

// 直角三角形リブ。直角が原点、脚が +X と +Z、厚さ t は +Y。
module rib45(leg, t, big = 400) {
    difference() {
        cube([leg, t, leg]);
        translate([leg, -0.5, 0]) rotate([0, -45, 0]) cube([big, t + 1, big]);
    }
}

// ---- クレードル (傾斜フレーム内で構築。原点 = 床上面の中心) ----------
module cradle_body() {
    difference() {
        union() {
            // 床板
            translate([-out_w / 2, -out_d / 2, -floor_t])
                cube([out_w, out_d, floor_t]);
            // 端壁 ×2 (床に ov 食い込ませる)
            for (sx = [-1, 1])
                translate([sx * (cav_w / 2 + wall) - (sx > 0 ? 0 : wall), -out_d / 2, -ov])
                    cube([wall, out_d, wall_h + ov]);
            // ボルト柱 ×2 (端壁の外面、全高。端壁の補強を兼ねる)
            for (sx = [-1, 1])
                translate([sx * (cav_w / 2 + wall) - (sx > 0 ? ov : boss_x),
                           strap_y - boss_y / 2, -ov])
                    cube([boss_x + ov, boss_y, wall_h + ov]);
            // 後壁
            translate([-out_w / 2, -out_d / 2, -ov])
                cube([out_w, wall, rear_h + ov]);
            // 床レール ×2 (底面タブの外側でケースの肩を受ける)
            for (sx = [-1, 1])
                translate([sx * rail_x0 - (sx > 0 ? 0 : cav_w / 2 - rail_x0 + ov),
                           -cav_d / 2 - ov, -ov])
                    cube([cav_w / 2 - rail_x0 + ov, cav_d + 2 * ov, rail_h + ov]);
            // 前リップ ×2 (端壁側だけ。中央は空けてレンズ画角を確保)
            for (sx = [-1, 1])
            // (前面 y=front_y はケース前面なので内側へは寄せない。画角の assert が効く)
                translate([sx * (cav_w / 2 + ov) - (sx > 0 ? lip_len + ov : 0),
                           front_y, -ov])
                    cube([lip_len + ov, front_t, front_h + ov]);
            // ステム (床下。ヨークまで伸ばして union で繋ぐ)
            translate([-stem_w / 2, -stem_d / 2, -stem_len])
                cube([stem_w, stem_d, stem_len]);
            // 床下ガセット ×4 (幅広クレードルの片持ちを支える)
            // 直角の角を ov だけステム/床へ食い込ませる (脚長は同じに保つ)
            for (sx = [-1, 1]) for (sy = [-1, 1])
                translate([sx * (stem_w / 2 - ov), sy * gus_y - gus_t / 2, -floor_t + ov])
                    mirror([sx > 0 ? 0 : 1, 0, 0]) mirror([0, 0, 1])
                        rib45(gus_leg + ov, gus_t);
        }
        // 後壁の肉抜き窓 (軽量化 + 水抜き + ケーブル視認)
        translate([-win_w / 2, -out_d / 2 - 1, rear_h - win_h - 6])
            cube([win_w, wall + 2, win_h]);
        // 床の水抜き穴。ステムの真上を外して床下へ抜けるようにする
        for (sx = [-1, 1]) for (sy = [-1, 1]) for (dx = drain_x)
            translate([sx * dx, sy * drain_y, -floor_t - 1])
                cylinder(d = drain_d, h = floor_t + 2);
        // M4 ボルト穴 + ナットスロット ×2
        for (sx = [-1, 1]) {
            translate([sx * m4_x, strap_y, wall_h - nut_drop - 12])
                cylinder(d = m4_d, h = nut_drop + 14);
            translate([sx * (cav_w / 2 + wall + boss_x) - (sx > 0 ? 0 : nut_w + 6),
                       strap_y - nut_w / 2, wall_h - nut_drop])
                cube([nut_w + 6, nut_w, nut_t]);
        }
    }
}

// ---- ヨークと足 (傾けない。ピン中心が原点) ---------------------------
module yoke_and_prongs() {
    difference() {
        union() {
            // プロング ×3 (ピンまわりの円板。下端はビーム上面の手前で切る)
            intersection() {
                for (i = [-1, 0, 1])
                    translate([i * prong_pitch - prong_t / 2, 0, 0])
                        rotate([0, 90, 0]) cylinder(r = prong_r, h = prong_t);
                translate([-stack_w, -prong_r - 1, prong_z0])
                    cube([2 * stack_w, 2 * prong_r + 2, 2 * prong_r + 2]);
            }
            // ヨーク (プロングの上でひと繋ぎにする)
            translate([-stack_w / 2, -foot_y1, yoke_z0])
                cube([stack_w, 2 * foot_y1, yoke_z1 - yoke_z0]);
            // 足 ×2 (ビーム上面に着座して 20° を positive に決める回り止め)
            for (sy = [-1, 1])
                translate([-stack_w / 2, sy * foot_y0 - (sy > 0 ? 0 : foot_y1 - foot_y0),
                           beam_top_z])
                    cube([stack_w, foot_y1 - foot_y0,
                          yoke_z0 - beam_top_z + ov]);   // ヨークへ ov 食い込ませる
        }
        // ピン穴 (X 方向貫通)
        translate([-stack_w / 2 - 1, 0, 0]) rotate([0, 90, 0])
            cylinder(d = pin_d, h = stack_w + 2);
    }
}

module holder_cradle() {
    union() {
        translate([0, stem_y, stem_z]) rotate([-tilt, 0, 0]) cradle_body();
        yoke_and_prongs();
    }
}

// ---- ストラップ (平置きで印刷。組付け時はクレードル上面に載る) --------
module holder_strap() {
    difference() {
        translate([-max_w / 2, -strap_w / 2, 0])
            cube([max_w, strap_w, strap_t]);
        for (sx = [-1, 1]) {
            translate([sx * m4_x, 0, -1]) cylinder(d = m4_d, h = strap_t + 2);
            translate([sx * m4_x, 0, strap_t - head_t])
                cylinder(d = head_d, h = head_t + 1);
        }
    }
}

if (part == "cradle") holder_cradle();
else if (part == "strap") holder_strap();
else assert(false, "part は \"cradle\" か \"strap\"");

echo(str("ケース収容 ", cav_w, " x ", cav_d, " / 端壁高 ", wall_h,
         " / 最大幅 ", max_w, " / 前リップ画角余裕 ", lip_ang - fov_half, "deg",
         " / チューブすきま ", base_line_min - max_w / 2 - tube_od / 2, "mm",
         " / クランプすきま 後 ", hold_y_aft + clamp_y - clamp_band / 2,
         " 前 ", clamp_y - clamp_band / 2 - hold_y_fwd, "mm"));

// ---- 印刷向き -------------------------------------------------------
// cradle: このモデルは「設置姿勢」なので、スライサで X 軸まわりに +90°
//   回して**後壁の外面をベッドに置く**。105.9 x 46 の平面が接地し、
//   端壁・床・ボルト柱はすべてベッドに垂直な壁になる。プロング板は
//   ベッドに垂直 = 曲げ方向が層内に入るので折れにくい。
//   ヨーク/プロング/床下ガセットは片持ちになるのでサポートを付ける。
// strap: そのまま平置き (座グリが上)。
// 素材は靭性のある PETG / ASA / PA。
