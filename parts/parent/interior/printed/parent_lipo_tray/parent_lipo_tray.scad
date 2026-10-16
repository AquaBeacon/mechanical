// =====================================================================
// parent_lipo_tray.scad — 親機 LiPo ブリッジトレイ (P-MAIN 上・最上段・交換しやすさ優先)
//
// 役割: LiPo Zeee 3S 2200 (102×34×23, ~170g) を P-MAIN の上に架けるトレイ。
//   P-MAIN の取付穴 4 点 (kicad 103×75.5 → プレート (6.5,10)(109.5,10)(6.5,85.5)
//   (109.5,85.5)) に M3 オス-メス スペーサ 25 mm (hex_spacer m3_mf25) を立て、
//   その上に本トレイを M3×6 ×4 で固定する。**LiPo は最上段** = 蓋を開ければ
//   ベルクロ帯を外して真上に抜ける (毎セッションの電池交換動線)。
// 高さ (箱底外面基準): プレート上面 18.8 → MAIN 基板上面 26.4 → スペーサ 25 →
//   トレイ下面 51.4 → 床 t3 → LiPo 下面 54.4 → LiPo 上面 77.4 (蓋パッキン面 90.9)。
//   MAIN の最高部品 (DS3231 スタック 18.5 → z 44.9) との隙間 6.5。
// 原点: MAIN 南西取付穴の中心 (プレート (6.5,10)) の直上、トレイ下面 z=0。
//   X = MAIN 穴ピッチ 103 方向、Y = 75.5 方向 (北)。
// 構造: ベイ (内寸 106×40, 壁 2.5, 床 3) を南側 2 穴の上に置き、東西 2 本の
//   レール (幅 8 × 高さ 12) で北側 2 穴へ架ける (4 点支持)。レールは MAIN の東西縁の上
//   z=51.4 を通る。リードは西端壁の切欠きから出て P-PWR J_BAT へ。
// 印刷向き: 平置き (+Z 上)。サポート不要。PETG / インフィル 30%。
// =====================================================================

/* [LiPo (lipo_3s_2200_zeee.md と二重定義 — 片方だけ直さない)] */
lipo_l   = 102;
lipo_w   = 34;
lipo_h   = 23;
end_pad  = 2;      // 長さ方向の片側余裕
side_pad = 3;      // 幅方向の片側余裕 (発泡パッド代)

/* [P-MAIN 取付穴 (PARENT_MAIN.kicad_pcb 実座標 → ピッチ)] */
hole_px  = 103;    // kicad (4.5→107.5)
hole_py  = 75.5;   // kicad (4.5→80)
hole_d   = 3.4;    // M3 通し
pad_d    = 9;      // 穴まわりの座

/* [トレイ] */
wall     = 2.5;
floor_t  = 3;
wall_h   = 14;     // 側壁高さ (LiPo 23 の 60%)
bay_x0   = -4;     // ベイ外形の X 開始 (穴中心基準)。ベイ中心 = 穴スパン中心 (51.5)
bay_y0   = 5;      // ベイ外形の Y 開始 (南穴の座 pad_d/2=4.5 の外)
rail_w   = 8;      // 東西レール幅 (穴中心線に載せる)
rail_h   = 12;     // レール高さ (t3 では落下 10G でたわみ 37mm → 12 で 0.6mm。quick_strength beam)
rail_y1  = 4.5;    // レール北端の穴からのはみ出し
drain_d  = 4;

/* [ベルクロ帯スロット] */
strap_w  = 20;
strap_t  = 4;
strap_x  = [24, 79];   // ベイ原点 (bay_x0) 基準の帯中心

/* [リード切欠き (西端壁)] */
lead_w   = 20;

/* [高さ検査 (spec/parent_interior_layout.py と二重定義)] */
spacer_l = 25;     // hex_spacer m3_mf25
main_top_comp = 18.49;   // MAIN 基板上面からの最高部品 (parent_main.md)
pcb_t    = 1.6;
plate_top_z = 18.8;      // 箱底外面基準
lid_z    = 90.9;         // 蓋パッキン面

$fn = 48;

// ---- 導出 -----------------------------------------------------------
in_l = lipo_l + 2*end_pad;      // 106
in_w = lipo_w + 2*side_pad;     // 40
L    = in_l + 2*wall;           // 111
W    = in_w + 2*wall;           // 45
holes = [[0, 0], [hole_px, 0], [0, hole_py], [hole_px, hole_py]];
tray_z0 = plate_top_z + 6 + pcb_t + spacer_l;   // 51.4 (ボス 6 + 基板 + スペーサ)
lipo_top_z = tray_z0 + floor_t + lipo_h;        // 77.4

// ---- 成立性チェック --------------------------------------------------
assert(abs((bay_x0 + L/2) - hole_px/2) < 0.01, "ベイ中心が穴スパン中心に無い");
assert(bay_y0 >= pad_d/2 - 0.01 || bay_y0 <= -W, "ベイ南壁が南穴の座に掛かる");
assert(bay_y0 + W < hole_py - pad_d/2, "ベイ北壁が北穴の座に掛かる");
assert(tray_z0 - (plate_top_z + 6 + pcb_t + main_top_comp) >= 3,
       str("トレイ下面と MAIN 最高部品の隙間不足: ", tray_z0 - (plate_top_z + 6 + pcb_t + main_top_comp)));
assert(lid_z - lipo_top_z >= 10, str("LiPo 上面と蓋の隙間不足 (交換時の手掛かり): ", lid_z - lipo_top_z));
assert(lead_w <= in_w - 2*8, "リード切欠きが広すぎ (端壁の残りが LiPo を止めない)");
for (x = strap_x)
    assert(x - strap_w/2 >= wall + 2 && x + strap_w/2 <= L - wall - 2, "帯スロットが端壁に接近");
assert(strap_x[1] - strap_x[0] >= strap_w + 2*drain_d + 6, "帯スロット同士が近い (水抜き穴が置けない)");
// 水抜き穴: 帯溝の間と両外側の帯溝を避けた位置
drain_xy = [for (x = [ (strap_x[0] + strap_x[1])/2 ], y = [wall + 8, W - wall - 8]) [x, y]];
for (d = drain_xy) for (x = strap_x)
    assert(abs(d[0] - x) >= strap_w/2 + drain_d/2 + 1, "水抜き穴が帯溝に掛かる");
// レールがベイ外形と重なって一体になること
assert(bay_x0 <= rail_w/2 && bay_x0 + L >= hole_px - rail_w/2, "レールがベイに接続しない");
assert(rail_h <= floor_t + wall_h, "レールがベイ壁より高い");
// レール (北穴への片持ち) の強度: 落下 10G で半分の LiPo 荷重 8.5 N、長さ 75.5
assert(rail_h >= 10, "レール高さ不足 (quick_strength: t>=10 でたわみ 1mm 以下)");

echo(str("parent_lipo_tray: bay ", L, "x", W, " at (", bay_x0, ",", bay_y0, "), tray z0=", tray_z0,
         " lipo top z=", lipo_top_z, " (lid ", lid_z, ")  cell plate-xy = ",
         [6.5 + bay_x0 + wall + end_pad, 10 + bay_y0 + wall + side_pad]));

// ---- 本体 -------------------------------------------------------------
difference() {
    union() {
        // ベイ
        translate([bay_x0, bay_y0, 0]) cube([L, W, floor_t + wall_h]);
        // 東西レール (南穴 → 北穴)
        for (x = [0, hole_px])
            translate([x - rail_w/2, -pad_d/2, 0]) cube([rail_w, hole_py + pad_d/2 + rail_y1, rail_h]);
        // 穴の座
        for (h = holes) translate([h[0], h[1], 0]) cylinder(d = pad_d, h = floor_t);
    }
    // ベイ内
    translate([bay_x0 + wall, bay_y0 + wall, floor_t]) cube([in_l, in_w, wall_h + 1]);
    // リード切欠き (西端壁)
    translate([bay_x0 - 0.5, bay_y0 + W/2 - lead_w/2, floor_t + 2]) cube([wall + 1, lead_w, wall_h + 1]);
    // M3 通し穴
    for (h = holes) translate([h[0], h[1], -0.5]) cylinder(d = hole_d, h = floor_t + 1);
    // ベルクロ帯: 側壁スロット + 床の浅い溝
    for (x = strap_x) {
        translate([bay_x0 + x - strap_w/2, bay_y0 - 0.5, floor_t]) cube([strap_w, W + 1, strap_t]);
        translate([bay_x0 + x - strap_w/2, bay_y0 + wall, floor_t - 1.0]) cube([strap_w, in_w, 1.5]);
    }
    // 水抜き穴
    for (d = drain_xy) translate([bay_x0 + d[0], bay_y0 + d[1], -0.5]) cylinder(d = drain_d, h = floor_t + 1);
}
