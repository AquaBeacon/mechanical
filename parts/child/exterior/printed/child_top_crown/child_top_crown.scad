// =====================================================================
// child_top_crown.scad — 子機 トップクラウン (吊り耳 ×2 一体 + ドーム根元カラー)
//
// docs/子機外装_改善要件.md §3.5 (G2/G4, C3)。`child_lug` ×2 を置き換える。
// コアフレームの吊り耳ボス (頂面 z=218、M5 熱圧入インサート ×4 @ x=±lug_x,
// y=lug_bolt_y) に M5 ×4 で載る。ドーム押えリング (wte4_dome_cap, OD=dome_ring_od
// 仮 120.3、座面 z=208) を囲む C 形カラーと、左右の吊り耳 (シャックル Ø16) を
// 一体化した部品。**ドーム上半球は覆わない** (C3, 将来 LED で照らす)。
//
// 座標系: 機体グローバル (チューブ軸=Z, z=0 チューブ下端, +Y=前)。
// 取合い (二重定義。child_core_frame.scad と一致させること):
//   lug_x = 66 / lug_bolt_y = [-4,-16] / 台座取付面 z = 218 (frame_z1)
//   dome_ring_od = 120.3 (child_core_frame / child_jaw_gate と同じ仮値)
//   パイロン屋根 y -101..-50 / z 182..190 (child_core_frame, 干渉しない高さ差)
//   xdcr_socket 座 中心 (0, -75)、外径 ~36 (r18) 高さ38 → 上端 z228
//     (child_core_frame xd_cy / xd_p, xdcr_socket.md)
// ゲート (可動側、y>=0) 頂面も z218 なので、y>0 領域は z>=218.5 に浮かせて
// 開閉時に擦らないようにする。
//
// 荷重: L1 吊り 99N/耳 (全備 5.7kg x 3g, ブライドル ~30°) / L2 輸送 300N
// (2026-09-04 緩和, 5g)。quick_strength で確認 (このファイル末尾コメント参照)。
//   lug  (シャックル穴 ベアリング/ネット断面/ティアアウト): hole16 edge10 t22
//     F=300N -> 0.68/0.85/0.68 MPa (limit 12/18/7.2) PASS
//     F=99N  -> さらに余裕 PASS
//   beam (耳根元 曲げ、L=22 (根元→シャックル穴中心), b=22(y), t=17(x)):
//     F=300N -> 曲げ 6.23 MPa (limit 12) / たわみ 0.127mm (limit 1) PASS
//     F=99N  -> PASS (さらに余裕)
//   ※ シャックル穴中心は当初案 z=248 から z=240 に下げてある。z248/Φ16 だと
//     穴の上端がちょうど耳上端 z=256 と一致し実質マージン 0 になるため
//     (child_lug の assert はこの base_t 二重加算バグで見かけ上 8mm と出ていた)。
//     z=240 なら上端マージン 8mm・下端 (台座天面 z=222) までも 10mm 確保できる。
//
// 印刷: 左右の耳は .scad 内で mirror([1,0,0]) して 1 部品 (STL 1 個) にまとめて
// ある (placement.json ではミラー不要、1 インスタンスを配置するだけでよい)。
// カラー (単独円環) は +Z 直立で層がフープ荷重に沿う。耳板のシャックル穴軸=Y・
// 主荷重(Z 方向近似)は層面内にならないので、耳の根元断面は layer-across
// (量子 12MPa) で評価している (十分な安全率で PASS、上記コメント参照)。
// 1 部品で印刷 (+Z up)。耳の張り出しは下部が r63..75 の環状部に連続しており
// オーバーハングは目視で確認 (printability.py 参照)。
// =====================================================================

/* [取付 (child_core_frame と二重定義)] */
lug_x      = 66;          // 耳ボルト列の x (±)
lug_bolt_y = [-4, -16];   // M5 ×2 (机体 y)
mount_z    = 218;         // 台座取付面 (= frame_z1)

/* [ドーム根元カラー] */
dome_ring_od = 120.3;      // 押えリング OD (仮。child_core_frame/child_jaw_gate と同じ)
r_in       = 63;           // カラー内径 = Ø126
r_out      = 75;           // カラー外径 = Ø150 (<= 152 上限)
ring_z0    = 218;          // カラー下端 (機体固定側、y<=0)
ring_z1    = 232;          // カラー上端 (高さ 14)
front_raise = 0.5;         // y>0 (ゲート側) は下端をこれだけ浮かせる
aft_az0    = 225;          // 後方カットアウト (xdcr_socket 逃げ) 開始方位角
aft_az1    = 315;          // 終了方位角 (-Y ±45°)

/* [xdcr_socket / パイロン 逃げ確認用 (child_core_frame と二重定義)] */
xd_cx      = 0;
xd_cy      = -75;
xd_r_clear = 21;           // ソケット半径 ~18 + 余裕3
pyl_roof_z1 = 190;         // パイロン屋根上端

/* [吊り耳]  local: x = lug_x を中心に -8..+9 (機体 x = 58..75) */
ear_x0     = 58;           // 耳 内側端 (機体 x)
ear_x1     = 75;           // 耳 外側端 (= r_out)
ear_y0     = -22;          // 耳 奥行 (フレームボスと同じ y -22..0)
ear_y1     = 0;
ear_z1     = 256;          // 耳上端 <= 256 (ドーム頂点 261.25 手前)
foot_z1    = 222;          // 台座 (M5 クリアランス穴の厚み) z218..222
bolt_d     = 5.4;          // M5 クリアランス穴
hole_d     = 16;           // シャックル穴 (Ø10 ロープ / M10 シャックル)
hole_z     = 240;          // シャックル穴中心 (機体 z)

/* [輸送キャップ用インサート (child_dome_cap_transport と二重定義)] */
cap_bolt_x = 75;           // = ear_x1 (耳外側面)
cap_bolt_z = 227;          // 台座 (222) とシャックル穴下端 (232) の中間
cap_ins_d  = 6.4;          // M5 熱圧入インサート下穴
cap_ins_len = 9;

/* [Hidden] */
fudge = 0.01;
$fn = 64;

// ---- 検査 --------------------------------------------------------------
assert(2*r_in > dome_ring_od + 5,
       "カラー内径がドーム押えリング OD+5 を割り込む");
assert(ear_z1 <= 256, "耳上端が 256 を超える (ドーム頂点手前を割り込む)");
assert(hole_z - hole_d/2 - foot_z1 >= 6, "シャックル穴下端と台座の距離不足");
assert(ear_z1 - (hole_z + hole_d/2) >= 6, "シャックル穴上端と耳上端の距離不足");
assert(hole_z - hole_d/2 - cap_bolt_z >= 3, "キャップインサートとシャックル穴が近すぎる");
assert(cap_bolt_z - foot_z1 >= 3, "キャップインサートと台座が近すぎる");
assert(2*max(r_out, ear_x1) <= 152, "クラウン全幅が 152 を超える");
assert(ring_z0 > pyl_roof_z1, "カラー下端がパイロン屋根より低い");
assert(front_raise >= 0.5, "ゲート側クリアランスが 0.5mm 未満");
// アフトカットアウトの端 (r_out, aft_az0) から xdcr_socket 中心までの距離
aft_edge_x = r_out * cos(aft_az0);
aft_edge_y = r_out * sin(aft_az0);
aft_edge_dist = sqrt(pow(aft_edge_x - xd_cx, 2) + pow(aft_edge_y - xd_cy, 2));
assert(aft_edge_dist >= xd_r_clear,
       str("アフトカットアウト端が xdcr_socket に近すぎる: ", aft_edge_dist));
echo(str("aft_edge_dist(machine mm) = ", aft_edge_dist));
echo(str("crown 全幅 = ", 2*max(r_out, ear_x1), " / 耳上端 = ", ear_z1));

// ---- モジュール ----------------------------------------------------------
// 方位角 az0..az1 (deg, 0=+X, 90=+Y) の全径ウェッジ
module wedge(az0, az1, z0, h) {
    intersection() {
        rotate([0, 0, az0]) translate([0, 0, z0]) cube([400, 400, h]);
        rotate([0, 0, az1 - 90]) translate([0, 0, z0 - fudge]) cube([400, 400, h + 2*fudge]);
    }
}

module ear() {
    difference() {
        intersection() {
            // 箱: x [ear_x0..ear_x1] (機体 sx*lug_x を中心に外へ広げる) を
            // sx=-1 側は鏡像するので、ローカル形状は常に「外向き = +x 側」で作る
            translate([ear_x0, ear_y0, mount_z])
                cube([ear_x1 - ear_x0, ear_y1 - ear_y0, ear_z1 - mount_z]);
            // 外径 r_out を超える角 (y=-22 側) を丸める (カラーと同じ包絡に収める)
            translate([0, 0, mount_z - fudge]) cylinder(r = r_out, h = ear_z1 - mount_z + 2*fudge);
        }
        // ドーム/カラー内径の逃げ (z218..232 のみ有効。それ以上は自然と離れる)
        translate([0, 0, ring_z0 - fudge]) cylinder(r = r_in, h = (ring_z1 - ring_z0) + 2*fudge);
        // M5 クリアランス穴 (台座、機体 x=lug_x, y=lug_bolt_y)
        for (yy = lug_bolt_y)
            translate([lug_x, yy, mount_z - fudge])
                cylinder(d = bolt_d, h = foot_z1 - mount_z + 2*fudge, $fn = 32);
        // シャックル穴 (軸 Y、機体 x=lug_x, z=hole_z)
        translate([lug_x, ear_y0 - fudge, hole_z])
            rotate([-90, 0, 0]) cylinder(d = hole_d, h = (ear_y1 - ear_y0) + 2*fudge, $fn = 48);
        // 輸送キャップ用 M5 インサート下穴 (軸 X、外側面 x=cap_bolt_x から内向きに)
        translate([cap_bolt_x + fudge, (ear_y0 + ear_y1)/2, cap_bolt_z])
            rotate([0, -90, 0]) cylinder(d = cap_ins_d, h = cap_ins_len + fudge, $fn = 32);
    }
}

// ---- 形状 ---------------------------------------------------------------
union() {
    // カラー (C 形リング、アフトカットアウトあり、ゲート側 0.5mm 浮かせ)
    difference() {
        translate([0, 0, ring_z0]) cylinder(r = r_out, h = ring_z1 - ring_z0);
        translate([0, 0, ring_z0 - fudge]) cylinder(r = r_in, h = (ring_z1 - ring_z0) + 2*fudge);
        wedge(aft_az0, aft_az1, ring_z0 - fudge, (ring_z1 - ring_z0) + 2*fudge);
        // ゲート側 (y>0, az 0..180) の下端スライバを除去 -> 底面が 218.5 になる
        intersection() {
            wedge(0, 180, ring_z0 - fudge, front_raise + fudge);
            translate([-r_out - 1, -1, ring_z0 - fudge]) cube([2*r_out + 2, r_out + 2, front_raise + 2*fudge]);
        }
    }
    // 吊り耳 ×2 (機体 x=+lug_x と x=-lug_x を同一 .scad 内で mirror して 1 部品化)
    ear();
    mirror([1, 0, 0]) ear();
}
