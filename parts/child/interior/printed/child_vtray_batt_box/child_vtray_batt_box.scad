include <../../../../../scad/lib/child_interior_mounts.scad>
// 2026-10-01: through-bolts and side-loaded captive M3 nuts, reinforced pads.
// =====================================================================
// child_vtray_batt_box.scad — 子機 縦置き内装 LiPo ベイ (∩ チャンネル + 着脱床板)
//
// child_vtray_deck の**下面**にボルト留めして、LiPo (35 x 26 x 110、
// parts/child/interior/cots/lipo_35x26x110) を抱える箱。**床は別部品**
// (child_vtray_batt_floor) で、皿ねじ 1 本を外すと床板が −Y へ抜け、電池だけを
// すぐに取り出せる (箱も MAIN も外さない)。
//
// ★2026-09-03 作り直し (電池 102x34x23 → 35x26x110、リード制約、頻繁な電池交換):
//   ・電池は **リード側 (両端に充電線 / 電源線) を −Z (下) に向けて** 入れる。
//     −Z 側の固定端壁 (z 14..20、貫通口 Ø88.5 の中なので外形を円で切る) は
//     中央の柱 (|x| < slot_x0) だけが電池の重量を受け、両端は**横 (±X) に抜ける
//     リード切欠き**。リードはここで曲がって ±X へ出る (下ポケットに落とさない)。
//   ・+Z 側はゲート板を廃止。RX 基板 (z=134) まで 0.5mm なので、床から立つ
//     低い**リップ** (`lip_t` x `lip_h`) で電池端面の下側 7mm だけを押える。
//     リップの両端には床板のフック (2mm) が入るスロットがあり、床板の +Z 端は
//     ねじ無しで −Y に抜けないよう保持する。床板の −Z 端は端壁の柱へ M3 皿ねじ 1 本。
//   ・床板の着脱: 皿ねじを外す → 床板を −Z へ 2mm ずらしてフックを外す → −Y へ抜く
//     → 電池が −Y へ出る (XT30 を先に抜く)。
//   ・取付耳は 4t の角形 (楔なし)。
//
// 座標: child_vtray_deck と同じ (X=幅 / Y=積み方向 / Z=チューブ軸)。
//       原点は箱の Z 始点 (=幅広部下端 z=20)・軸心。端壁はここから −Z へ end_t 出る。
//
// 印刷向き: **耳の面 (y = deck_y0) を下にして印刷**。壁・端壁・柱は垂直、
//           リップ (38 幅 x 1.5t) だけが壁間をブリッジする。サポート不要。
// =====================================================================

/* [容器 (干渉検査用。deck と同じ値にすること)] */
tube_id     = 101.6;
wall_clear  = 2.5;
flange_bore = 88.5;   // 下フランジ貫通口Ø (端壁はこの中に入る)
bore_clear  = 1.0;
bore_margin = 0.25;   // 端壁外形の円を貫通口許容半径よりさらに絞る量

/* [デッキ側の座標 (child_vtray_deck と一致させること)] */
deck_y0     = -10;    // デッキ下面 Y (= 箱の開口面)
box_z0      = 20;     // この箱の原点の世界 Z (= wide_z0)
deck_band_lo = 11.5;  // デッキ下リブ帯の上端 = deck の band_lo (2026-09-03: 9 → 11.5、リブ座を先端から 4.5 内側へ)
rx_z0       = 134;    // RX 基板 (デッキ下面) の Z 始点
rx_comp_y   = -31.4;  // RX 部品の先端 Y (rx_y - rx_hi_h)

/* [LiPo (parts/child/interior/cots/lipo_35x26x110)] */
lipo_w     = 35;      // 幅 (X)
lipo_h     = 26;      // 厚み (Y)
lipo_l     = 110;     // 長さ (Z)
lipo_tol   = 1;       // 公称に対するばらつき (ユーザー指定値。実測で確定)
pad_t      = 3;       // 上面の発泡パッド代 (Y)
fit_clear  = 4;       // 幅方向の遊び = 側面フォーム 2 x2 が埋める (tol は圧縮で吸収)。床板フックが電池の外 (|x|>18) に入る幅
end_slack  = 2;       // 長さ方向の遊び = 端面フォーム 1 x2。tol は フォームの圧縮で吸収

/* [箱] */
wall_t     = 3;
floor_t    = 3;       // 床板 (child_vtray_batt_floor) の厚み。壁はこの分だけ下へ伸びる
end_t      = 6;       // −Z 固定端壁の厚み。原点から −Z へ出る (z 14..20)。皿ねじ下穴が入る
chamfer    = 3;       // 壁の外側下角の 45° 面取り

/* [リード切欠き (−Z 端壁)] */
// 電池上面 (取付では −Z 端面) の 35mm 辺の両端からリードが出る。
// 中央の柱 (|x| < slot_x0) が電池の重量を受け、両端の切欠きは壁の外 (±X) まで抜ける。
slot_x0    = 10.5;    // 切欠きの内側 X (±)。外側は箱の外壁 out_x まで貫通

/* [+Z リップ (旧ゲートの代わり) と床板フックのスロット] */
lip_t      = 1.5;     // 厚み (Z)
lip_h      = 7;       // 床板上面からの高さ (Y)。RX 部品の Y 帯 (≥ -31.4) に入らないこと
rx_clear_z = 0.5;     // リップ上面と RX 基板下端 (z=134) のすきま
hook_w     = 1.3;     // 床板フックの厚み (X)。child_vtray_batt_floor と一致させること
hook_h     = 3;       // 同 高さ (Y): 床板上面 -40 の 0.5mm 下 (-40.5) から -37.5 まで
hook_clear = 0.3;     // スロットの片側クリアランス

/* [床板の固定 (−Z 端壁の柱へ皿ねじ)] */
service_x=ci_service_x;
service_z=ci_service_z;
service_r=2.8; // historical boss reference; reinforced pad replaces this cylinder
floor_pilot_d = 2.5;  // M3 セルフタップ下穴 (端壁の柱の下面から +Y へ)
floor_pilot_l = ci_service_depth;

/* [取付耳] */
ear_x      = ci_ear_outer_x;
ear_t      = 4;       // 耳の板厚 (Y)。角形 (楔なし)。M3×8 = デッキ 4 + 耳 4 で先端が面一
ear_hx     = ci_box_hx;
edge_min   = 0.6;     // ねじ穴と耳の縁の最小残り肉
ear_hz     = ci_box_hz;
pad_transition = ci_ear_depth-ear_t; // 45 degree axial transitions to the ear.
pilot_d    = ci_clear_d; // through-bolt clearance, not a self-tap pilot

$fn = 96;

// ---- 導出 -------------------------------------------------------------
r_use    = tube_id/2 - wall_clear;             // 幅広部で使える半径 48.3
r_end    = (flange_bore - bore_clear)/2 - bore_margin;   // 端壁の外形半径 43.5
cav_w    = lipo_w + lipo_tol + fit_clear;      // 内幅  38
cav_h    = lipo_h + lipo_tol + pad_t;          // 内高さ 30
cav_l    = lipo_l + end_slack;                 // 端壁上面からリップまで 112
cav_x    = cav_w/2;
out_x    = cav_x + wall_t;                     // 外壁 X 22
box_len  = cav_l + lip_t;                      // 原点から上端 (リップ含む) 113.5
floor_y1 = deck_y0 - cav_h;                    // LiPo が載る面 (床板上面) -40
floor_y0 = floor_y1 - floor_t;                 // 床板下面 = 壁の下端 -43
ear_y0   = deck_y0 - ear_t;
slot_y1  = deck_y0 - pad_t - lipo_tol;         // 電池上面 (取付で +Y 側) = 切欠きの上端 -14
lip_y1   = floor_y1 + lip_h;
hook_y0  = floor_y1 - 0.5;                     // フックの下面 -40.5 (床板上面の 0.5mm 下)
hook_slot_x0 = cav_x - hook_w - hook_clear;    // スロット内側 X 17.3

function rad(x, y) = sqrt(x*x + y*y);

// ---- 干渉・成立性チェック ---------------------------------------------
// 容器
assert(chamfer <= wall_t && chamfer <= floor_t, "面取りが壁の厚み/床板厚を超えている");
assert(rad(out_x, floor_y0 + chamfer) <= r_use && rad(out_x - chamfer, floor_y0) <= r_use,
       str("壁の底の角がチューブに接触 r=", max(rad(out_x, floor_y0 + chamfer), rad(out_x - chamfer, floor_y0)),
           " > ", r_use));
assert(rad(ear_x, ear_y0) <= r_use, "取付耳の角がチューブに接触");
// LiPo
assert(cav_w >= lipo_w + lipo_tol, str("内幅 ", cav_w, " が LiPo 最大幅より狭い"));
assert(cav_h >= lipo_h + lipo_tol, str("内高さ ", cav_h, " が LiPo 最大高さより低い"));
assert(cav_l >= lipo_l + lipo_tol, str("端壁〜リップ ", cav_l, " が LiPo 最大長より短い"));
// −Z 端壁: 貫通口の中 (z < 20) にあるので円で切る。中央柱と上の桁が残ること
assert(box_z0 - end_t >= deck_band_lo,
       str("端壁 (世界 z ", box_z0 - end_t, ") がデッキ下リブ帯 ", deck_band_lo, " に入る"));
assert(sqrt(r_end*r_end - floor_y1*floor_y1) > slot_x0 + 2,
       "端壁の中央柱が円で削られて細くなりすぎる (slot_x0 を小さくするか床を上げる)");
assert(rad(ear_x, ear_y0) < r_end, "端壁上部の桁 (耳の帯まで) が貫通口に入らない");
assert(slot_x0 + 2 < cav_x, "リード切欠きが狭すぎる");
assert(slot_x0 < lipo_w/2 - 2, "リード切欠きが電池の縁 (リード出口) を覆っている");
// 床板の皿ねじ下穴が柱の中に収まること (柱の厚み end_t の中心、両側に 1.5mm 以上)
assert((end_t - floor_pilot_d)/2 >= 1.5, str("皿ねじ下穴の周りの肉が ", (end_t - floor_pilot_d)/2, " しか無い"));
assert(floor_pilot_d/2 + 1.5 < slot_x0, "皿ねじ下穴が柱の縁に近すぎる");
// +Z リップ: RX 基板・RX 部品を避ける
assert(box_z0 + box_len + rx_clear_z <= rx_z0,
       str("箱の上端 ", box_z0 + box_len, " が RX 基板 ", rx_z0, " に近すぎる"));
assert(lip_y1 <= rx_comp_y - 1,
       str("リップ上面 y=", lip_y1, " が RX 部品の Y 帯 (", rx_comp_y, ") に入る"));
assert(lip_h < lipo_h, "リップが電池端面より高い");
// フックスロット: リップの中に収まり、下 (−Y) に肉が残ること
assert(hook_y0 - hook_clear - floor_y0 >= 2.0, "フックスロットの下 (リップの床板側) の肉が薄い (片持ち 1.7 で 25N 落下に耐える最小 2.0)");
assert(hook_y0 + hook_h + hook_clear < lip_y1 - 1, "フックスロットがリップ上面を抜く");
assert(hook_slot_x0 > slot_x0, "フックスロットが柱の範囲に入っている");
assert(hook_slot_x0 >= lipo_w/2 + lipo_tol/2 + 0.3, str("床板フック (x ≥ ", hook_slot_x0, ") が電池 (半幅 ", lipo_w/2 + lipo_tol/2, ") に当たる"));
// 耳のねじ穴が耳の中に収まること (縁抜けの防止)
assert(ear_hx - pilot_d/2 - edge_min >= cav_x + 1 && ear_hx + pilot_d/2 + edge_min < ear_x,
       str("耳のねじ穴 X=", ear_hx, " が耳 (", out_x, "..", ear_x, ") の縁に近すぎる"));
for (z = ear_hz) assert(z > 5 && z < box_len - lip_t - 5,
                        str("耳のねじ穴 Z=", z, " が端に近すぎる"));

// ---- 本体 -------------------------------------------------------------
difference() {
    union() {
        // 側壁 ×2 (床板下面からデッキ下面まで。床板は壁の間に入る)
        for (sx = [-1, 1])
            translate([sx > 0 ? cav_x : -out_x, floor_y0, 0])
                ci_chamfer_box([wall_t, deck_y0 - floor_y0, box_len]);
        // −Z 固定端壁: (箱の断面 (床板の上まで) + 耳の帯) ∩ 円 r_end (貫通口に入れる)
        intersection() {
            union() {
                translate([-out_x, floor_y1, -end_t]) ci_chamfer_box([2*out_x, deck_y0 - floor_y1, end_t]);
                translate([-ear_x, ear_y0, -end_t]) ci_chamfer_box([2*ear_x, ear_t, end_t]);
            }
            translate([0, 0, -end_t - 0.5]) cylinder(r = r_end, h = end_t + 1);
        }
        // Long service pad; bearing thickness 3.5 mm before nut pocket.
        // The cavity face X20 stays clear of the battery and its side foam.
        translate([cav_x,floor_y1,service_z-ci_service_half_z])
            ci_chamfer_box([ci_service_outer_x-cav_x,ci_service_depth,
                            2*ci_service_half_z]);
        // +Z リップ: 側壁の間に床板下面から lip_h + floor_t だけ立つ (床板の +Z 端も受ける)
        // Two end stops instead of a 40 mm unsupported crossbar.
        // 45 degree inner ramps grow from the sidewalls when printed -Y up.
        for(sx=[-1,1]) scale([sx,1,1]) translate([0,0,cav_l]) linear_extrude(lip_t)
            polygon([[cav_x,lip_y1+7],[cav_x,floor_y0],
                     [cav_x-7,floor_y0],[cav_x-7,lip_y1]]);
        // 取付耳 (角形フランジ)
        for (sx = [-1, 1])
            translate([sx > 0 ? cav_x : -ear_x, ear_y0, 0]) ci_chamfer_box([ear_x - cav_x, ear_t, box_len]);
        // Four 8 mm deep pads join the full-height sidewalls and mounting ears.
        // 5.2+ mm of printed bearing material above each 2.6 mm nut recess.
        for(sx=[-1,1]) for(z=ear_hz) {
            assert(z-ci_ear_half_z-pad_transition>=0 &&
                   z+ci_ear_half_z+pad_transition<=box_len);
            hull() {
                translate([sx>0 ? cav_x : -ear_x,deck_y0-ci_ear_depth,z-ci_ear_half_z])
                    ci_chamfer_box([ear_x-cav_x,ci_ear_depth,2*ci_ear_half_z]);
                translate([sx>0 ? cav_x : -ear_x,ear_y0,z-ci_ear_half_z-pad_transition])
                    ci_chamfer_box([ear_x-cav_x,ear_t,2*(ci_ear_half_z+pad_transition)]);
            }
        }
    }
    // 壁の外側下角 45° 面取り: 角を中心にした菱形 (半対角 = chamfer) で削る
    for (sx = [-1, 1])
        translate([sx * out_x, floor_y0, (box_len - end_t)/2]) rotate([0, 0, 45])
            cube([chamfer * sqrt(2), chamfer * sqrt(2), box_len + end_t + 2], center = true);
    // 耳の M3 セルフタップ下穴 (デッキ側から締める)
    for (sx = [-1, 1]) for (z = ear_hz)
        translate([sx * ear_hx, deck_y0 + 0.5, z])
            rotate([90, 0, 0]) cylinder(d = pilot_d, h = ci_ear_depth + 1, $fn = 48);
    // Hex pockets open sideways; rails are fitted after inserting nuts.
    // Mouth is intentionally open: no sub-mm radial retaining skin.
    for(sx=[-1,1]) for(z=ear_hz) {
        translate([sx*ear_hx,deck_y0-ci_ear_depth-0.1,z]) ci_nut_y();
        translate([sx>0 ? ear_hx : -ear_x-0.1,
                   deck_y0-ci_ear_depth-0.1,z-ci_nut_af/sqrt(3)])
            cube([ear_x-ear_hx+0.1,ci_nut_t,2*ci_nut_af/sqrt(3)]);
        // Lead-in relief on both axial ends of the through bore.
        translate([sx*ear_hx,deck_y0+0.01,z]) rotate([90,0,0])
            cylinder(d1=ci_clear_d+2*ci_edge_chamfer,d2=ci_clear_d,h=ci_edge_chamfer,$fn=48);
    }
    // −Z 端壁のリード切欠き (電池端面の両端。床板上面から電池上面まで、外壁まで貫通)
    for (sx = [-1, 1])
        translate([sx > 0 ? slot_x0 : -out_x - 0.5, floor_y1 - 0.01, -end_t - 0.5])
            cube([out_x - slot_x0 + 0.5, slot_y1 - floor_y1 + 0.01, end_t + 1]);
    // 床板の皿ねじ下穴 (柱の下面 y=floor_y1 から +Y へ)
    translate([service_x, floor_y1 - 0.5, service_z]) rotate([-90,0,0])
        cylinder(d=ci_clear_d,h=floor_pilot_l+0.8,$fn=48);
    translate([service_x,ci_service_nut_y,service_z]) ci_nut_y();
    translate([service_x,floor_y1-0.01,service_z]) rotate([-90,0,0])
        cylinder(d1=ci_clear_d+2*ci_edge_chamfer,d2=ci_clear_d,h=ci_edge_chamfer,$fn=48);
    translate([service_x,ci_service_nut_y,service_z-ci_nut_af/sqrt(3)])
        cube([ci_service_outer_x-service_x+0.2,ci_nut_t,2*ci_nut_af/sqrt(3)]);
    // Recess the sidewall beneath the removable floor tab (0.3 mm edge clearance).
    // Include the complete -Z2 service slide, not only the installed tab.
    translate([19.7,floor_y0-0.5,service_z-ci_service_half_z-2.3])
        cube([7,floor_t+0.5,2*ci_service_half_z+2.6]);
    // リップのフックスロット ×2
    for (sx = [-1, 1])
        translate([sx > 0 ? hook_slot_x0 : -cav_x - 0.2, hook_y0 - hook_clear, cav_l - 0.5])
            cube([cav_x + 0.2 - hook_slot_x0, hook_h + 2*hook_clear, lip_t + 1]);
}

echo(str("child_vtray_batt_box: 内 ", cav_w, " x ", cav_h, " x ", cav_l,
         " / 原点から上端 ", box_len, " (端壁 −", end_t, " → 世界 z ", box_z0 - end_t, "..", box_z0 + box_len, ")",
         " 外幅 ", 2*out_x, " / Y ", floor_y0, "..", deck_y0,
         "  端壁外形 r=", r_end, "  床板 ", 2*cav_x, " x ", floor_t, " (y ", floor_y0, "..", floor_y1, ")",
         "  最小チューブすきま=", tube_id/2 - max(rad(out_x, floor_y0 + chamfer), rad(out_x - chamfer, floor_y0))));
