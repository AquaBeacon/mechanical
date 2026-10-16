// =====================================================================
// child_dome_cap_transport.scad — 子機 輸送専用 ドーム頂点キャップ
//
// docs/子機外装_改善要件.md §3.5 (G2/G4, C3)。運用時は取り外す (ドーム内
// から LED で照らすため、上半球を覆わない)。輸送 (パッド入りハードケース)
// のときだけ被せ、ドーム頂点への打痕を防ぐ。
//
// 座標系: 機体グローバル (チューブ軸=Z, z=0 チューブ下端, +Y=前)。
// 取合い (二重定義):
//   ドーム (wte4_dome_cap, 仮値): 座面 z=208, 押えリング OD=120.3, リング高6
//     (リング上面 z=214)。アクリルドーム本体 OD = (dome_ir+dome_t)*2 = 94.5
//     (wte4_dome_cap_ref.scad の式)。頂点 z = 208 + dome_h(53.25仮) = 261.25。
//     クリアランス計算は要件の「ドーム OD 114.3」の記述より広い 123mm 径の
//     筒で覆っており、実測差を吸収できる方へ振ってある (要確認 参照)。
//   child_top_crown: カラー外径 r_out=75 (Ø150)、耳上端 z=256、耳外側面
//     x=±cap_bolt_x(75) の z=cap_bolt_z(227) に M5 熱圧入インサート ×2
//     (child_top_crown.scad と一致させること)
//   xdcr_socket 座 中心 (0,-75) — 後方カットアウトで避ける
//
// 固定: M5 ノブボルト ×2 (工具レス)。スカートのバカ穴 Ø5.4 から
// child_top_crown の M5 インサートへ。
//
// 荷重: L2 輸送 300N を天板中央で受ける (四辺 [円周] 支持相当、
// quick_strength plate --a 123 --b 123 --t 6 で 曲げ3.05MPa/たわみ0.71mm PASS)。
//
// 印刷: topopt print 実測で **-Y up** (モデルの Z 軸を横に倒す) が最良
// (オーバーハング 9.9%、cos=0 で主荷重は層面内)。天板を下にした素直な
// 逆さ置き (+Y up 相当、オーバーハング 8.1%・1層目 0mm2) も同等に成立する
// ので、スライサでどちらか支持要否の少ない方を選べばよい。いずれも
// X1C 250mm^3 枠に収まる (実寸 158 x 134.9 x 53.25)。
// =====================================================================

/* [ドームクリアランス]  座標は wte4_dome_cap の座面 (z=208) 基準の絶対値 */
dome_apex_z = 261.25;      // 座面(208) + dome_h(53.25仮)
cover_r     = 61.5;        // 内筒半径 (ID123)。実ドーム r47.25 に対し +14.25 の余裕
cover_wall  = 4;
cover_z0    = 256;         // = child_top_crown 耳上端 (skirt との段差位置)
cover_z1    = 265.75;      // 頂点(261.25)まで 4.5mm クリア
plate_t     = 6;           // quick_strength plate --a123 --b123 --t6 PASS

/* [スカート]  child_top_crown のカラー/耳の外径 (r_out=75, ear_x1=75) に外嵌め */
crown_r_out = 75;          // child_top_crown r_out / ear_x1 と二重定義
skirt_r     = 76;          // ID152 (クラウン外径 150 + 1mm×2 のクリアランス)
skirt_wall  = 3;           // OD158 (<=160 上限)
skirt_z0    = 218.5;       // ゲート頂面 z218 に触れない (スカート内腔の下端)

/* [後方カットアウト (child_top_crown と同じ、xdcr_socket/TD04A 逃げ)] */
aft_az0 = 225;
aft_az1 = 315;
xd_cx = 0;
xd_cy = -75;
xd_r_clear = 21;

/* [固定用 M5 ノブボルト (child_top_crown と二重定義)] */
cap_bolt_x = 75;
cap_bolt_y = -11;   // = child_top_crown 耳の y 中心 ((ear_y0+ear_y1)/2)
cap_bolt_z = 227;
knob_hole_d = 5.4;

/* [Hidden] */
fudge = 0.01;
$fn = 64;

// ---- 検査 --------------------------------------------------------------
assert(cover_r*2 - 2*47.25 >= 4, "ドーム側面クリアランス不足 (< 4mm)");
assert(cover_z1 - dome_apex_z >= 4, "ドーム頂点クリアランス不足 (< 4mm)");
assert(cover_z1 + plate_t <= 275, "キャップ上端が 275 を超える");
assert(2*(skirt_r + skirt_wall) <= 160, "キャップ外径が X1C 実用枠を超える");
assert(skirt_z0 >= 218.5, "スカート下端がゲート頂面に近すぎる (擦る)");
assert(skirt_r >= crown_r_out + 0.5, "スカートがクラウンに嵌らない");
assert(cap_bolt_z > skirt_z0 && cap_bolt_z < cover_z0, "ノブボルト位置がスカート内腔の外");
aft_edge_x = skirt_r * cos(aft_az0);
aft_edge_y = skirt_r * sin(aft_az0);
aft_edge_dist = sqrt(pow(aft_edge_x - xd_cx, 2) + pow(aft_edge_y - xd_cy, 2));
assert(aft_edge_dist >= xd_r_clear,
       str("アフトカットアウト端が xdcr_socket に近すぎる: ", aft_edge_dist));
echo(str("キャップ上端 z = ", cover_z1 + plate_t, " / ドーム頂点クリアランス = ", cover_z1 - dome_apex_z));

// ---- モジュール ----------------------------------------------------------
module wedge(az0, az1, z0, h) {
    intersection() {
        rotate([0, 0, az0]) translate([0, 0, z0]) cube([400, 400, h]);
        rotate([0, 0, az1 - 90]) translate([0, 0, z0 - fudge]) cube([400, 400, h + 2*fudge]);
    }
}

// ---- 形状 -----------------------------------------------------------
// 段差 (スカート/カバー) を別ソリッドで作ると z 境界で面同士が接するだけに
// なり CGAL の boolean union が別ソリッドとして分離することがあったため、
// **外殻を単一円筒 (OD 一定 = skirt_r+skirt_wall) で通し、内側のボア半径だけ
// 高さで変える** 構成にした (段差は内側だけ、外周は継ぎ目なし)。
top_z = cover_z1 + plate_t;
difference() {
    // 外殻 (単一円筒、後方カットアウトを全高で貫通させる)
    difference() {
        translate([0, 0, skirt_z0]) cylinder(r = skirt_r + skirt_wall, h = top_z - skirt_z0);
        wedge(aft_az0, aft_az1, skirt_z0 - fudge, (top_z - skirt_z0) + 2*fudge);
    }
    // スカート内腔 (クラウンとの嵌合クリアランス、z218.5..cover_z0)
    translate([0, 0, skirt_z0 - fudge]) cylinder(r = skirt_r, h = (cover_z0 - skirt_z0) + 2*fudge);
    // 内筒の内腔 (ドームクリアランス、z cover_z0..cover_z1)
    translate([0, 0, cover_z0 - fudge]) cylinder(r = cover_r, h = (cover_z1 - cover_z0) + 2*fudge);
    // ノブボルト バカ穴 ×2 (軸 X)
    for (sx = [-1, 1])
        translate([sx * (skirt_r + skirt_wall + fudge), cap_bolt_y, cap_bolt_z])
            rotate([0, -90 * sx, 0]) cylinder(d = knob_hole_d, h = skirt_wall + 2*fudge, $fn = 32);
}
