// 2026-10-01: broader printed roots; battery interfaces remain in place.
include <../../../../../scad/lib/child_interior_mounts.scad>
// 2026-09-27: lower rib and deck tail retired; material begins at Z20.
// =====================================================================
// child_vtray_deck.scad — 子機 縦置き構成 (構成B) 内装スレッドの背骨
//
// WTE4 アクリルチューブ (ID 101.6) へ「立てたまま」上から落とし込む内装。
// 配置は実基板の 3D モデル (parts/child/interior/pcb/) の**実測プロファイル**から
// 決めている (docs/子機内装_収まり検討.md)。
//
//   デッキ上面 下部 : CHILD_MAIN 112 x 88            — M3 ボス ×4 (h=7)
//   デッキ上面 上部 : CHILD_PWR (**縮小版**)          — M3 ボス ×4 (h=10)
//   デッキ下面 下部 : child_vtray_batt_box (LiPo)      — M3 ×4 でボルト留め
//   デッキ下面 上部 : RX_improved_mini を **90度回して** — M3 スペーサ ×4 で吊る
//   左右のすきま    : ケーブル通路 (デッキのスリットで上下面をつなぐ)
//
// **RX をデッキ下面へ移したのが CHILD_PWR の面積を稼ぐ肝。**
// 3 枚とも上面に並べると PWR の軸長が 18mm しか残らない。
//
// 軸方向の位置決め: 幅 93mm の中央部はフランジ貫通口 Ø88.5 を通らないので、
// **上下フランジのピストン内端面 (z = 19 / tube_len-19) に突き当たって止まる**。
// 両端の幅 76mm の細い部分だけが貫通口へ入る。
//
// 座標: 原点 = チューブ軸心。X = 幅 / Y = 積み方向 / Z = チューブ軸
//       (**Z=0 はアクリルチューブの下端面**。child_vertical_assembly と同じ)
//
// 印刷向き: デッキ板をベッドに寝かせ、ボス側を上。サポート不要。ブリム必須。
//
// Fusion 編集用に cube / cylinder のみ (角丸は Fusion 側で)。
// =====================================================================

/* [容器 (実測値)] */
tube_id     = 101.6;  // アクリルチューブ内径
tube_len    = 200;    // 使うチューブ長 (200 / 300)
flange_bore = 88.5;   // フランジ貫通口Ø
flange_ins  = 19;     // フランジピストンがチューブ内へ入る深さ
cap_free    = 3.7;    // キャッププラグ内端までの余裕 (チューブ端から外へ)
wall_clear  = 2.5;    // アクリル内壁と内装・部品の最小すきま
bore_clear  = 1.0;    // 貫通口と、そこへ入る部分の径クリアランス

/* [デッキ] */
deck_w      = 93;     // 中央部の幅 (>貫通口Ø88.5 = 軸方向ストッパを兼ねる)
deck_wn     = 76;     // 両端 (貫通口へ入る部分) の幅
sh_w        = 84;     // リブ位置決めショルダーの幅 (貫通口は通り、リブは止める)
sh_t        = 2;      // 同 長さ (Z)
deck_t      = 4;      // 板厚
deck_y0     = -10;    // デッキ下面 Y
pad_x       = 48.5;   // 振れ止めパッドの外端 X
pad_len     = 12;     // 同 長さ (Z)

/* [CHILD_MAIN  **104 x 88** / 上18.49・下4.75 (_mech.stl 実測 2026-08-01)] */
// v4.0 (2026-08-01): 外形 112 -> 104。C-PWR との接続を XH9 1本に統合し、
//  J_RXA1/J_I2CP/J_LIGHT1 と J_TETH1 の予備ピンを削って軸長を 8mm 詰めた。
//  ★取付穴は KiCad 盤内座標をそのまま持ち、**変換式で** ボス位置を導く (下記)。
//    南辺 (y=80) には穴を置けない (Waveshare RS485 crtyd x53-99/y70-86 が SE 隅を
//    占有する)。実基板の第2列は **y=66**。南 22mm が片持ちになるので、
//    振れ止めパッドを1つ USB/microSD 辺の下へ足してある。
main_l      = 104;
main_w      = 88;
main_z0     = 20;
main_boss_h = 9;      // 裏面リード 4.75 の逃げ
// CHILD_MAIN.kicad_pcb の H1..H4 実座標 (基板左下が原点 / Y 上向き正 / Ø3.2 = M3)
main_h_kx   = [4.5, 99.5];     // → チューブ Z
main_h_ky   = [4.5, 66.0];     // → 機体 X   ピッチ 95 x 61.5
main_hi_x   = [8, 42];         // 高背ゾーン(DS3231/BNO085) の X 範囲 (軸心側, 外側)
main_hi_h   = 20.1;            // 同 高さ (基板下面から)
main_lo_h   = 8.6;             // 低背ゾーンの高さ
main_under  = 4.8;             // 裏面リード突出

/* [CHILD_PWR v2.1 — **縮小版 62 x 70** をデッキ上面へ] */
// 2026-08-01: KiCad 側を 100.35x70 -> 62x70 に作り直した(旧予算 56 に対し、
//  CHILD_MAIN を 112->104 に詰めた 8mm のうち 6mm を C-PWR に回して 62 とした。
//  56 だと 2.0mm 幅の電池配線が通らず DRC が収束しなかった)。
have_pwr    = true;
pwr_l       = 62;     // 実基板 (pcb/build_child_pwr.py v2.1)
pwr_w       = 70;
// 2026-08-03: 128 -> 126。デッキ下面の RX 取付ねじ (Z=136.5) の頭が
//  PWR の H1 列ボス (旧 Z=132) の足元に乗っていたため 2mm 下げた。
//  MAIN(..124) との軸方向すきまは 2mm。下限 125 / 上限 129 の間で 126 だけが成立する。
pwr_z0      = 126;
pwr_boss_h  = 10;     // 裏面リード 8.15 の逃げ
// CHILD_PWR.kicad_pcb の H1..H4 実座標 (基板左下が原点 / Y 上向き正 / Ø3.2 = M3)
pwr_h_kx    = [4.0, 58.0];     // → チューブ Z   ピッチ 54.0
pwr_h_ky    = [4.0, 66.0];     // → 機体 X       ピッチ 62.0
pwr_hi_h    = 25.2;   // **全幅にわたる**最大部品高さ = 2MD1 トグル 25.12 (安全側で全幅と見なす)
// ★AE-LXDC55 降圧モジュール(11x25mm)は SIP3 で**縦挿し**するので実高 35.09mm。
//   2026-08-01 まで KiCad の 3D にソケット(8.5)しか出ておらず、mech.stl の 25.12 は
//   **10mm 過小**だった (pcb/mkmodel3d.py に LXDC55_AE_body を追加して解消)。
//   幅方向は軸心付近 ±5.5mm しか占めないので、そこだけ別に検査する。
pwr_vhi_x   = 6.0;    // 高背モジュールの X 外端 (軸心から)
pwr_vhi_h   = 35.1;   // 同 高さ (基板下面から)
pwr_tip_h   = 21.0;   // 貫通口へ出る先端側の最大部品高さ (実測 20.37 @ x>=52)
pwr_under   = 8.2;    // 裏面リード突出

/* [RX_improved_mini  68 x 46 / 上13.79・下1.91] — 90度回して**デッキ下面**へ */
// ★この基板は 2026-07-12 に発注済みで穴を開け直せない。取付穴は **M2 (Ø2.2 NPTH)**
//   であって M3 ではない。2026-08-03 まで deck も .md も M3 前提だった (実物は通らない)。
rx_w        = 68;     // 幅方向 (X)
rx_l        = 46;     // 軸方向 (Z)
rx_z0       = 134;
rx_stand    = 6;      // M2 オスメススペーサ (購入品) の長さ
// RX_improved_mini.kicad_pcb の H1..H4 実座標 (基板左下が原点 / Y 上向き正)
rx_h_kx     = [2.5, 65.5];     // → 機体 X (rx_w/2 - x)。180度回しても同じ (四隅 inset 2.5)
rx_h_ky     = [2.5, 43.5];     // → チューブ Z (rx_z0 から)
rx_hi_h     = 15.4;   // 部品高さ (基板下面から。幅方向のプロファイルは未計測なので全幅で見る)
rx_under    = 1.9;    // 裏面リード突出

/* [LiPo ベイ (child_vtray_batt_box を吊る)] */
box_z0      = 20;
// 2026-09-03: 電池 35x26x110 (lipo_35x26x110) に合わせて箱を作り直した。ゲート板は廃止し、
//  +Z 端は床から立つリップ (1.5t) で押え、床は着脱板 (child_vtray_batt_floor)。原点 (z=20) から上端 (リップ含む) までが box_len、
//  −Z の固定端壁は幅広部の外 (貫通口の中、z 16..20) へ box_below だけ出る。
box_len     = 113.5;  // child_vtray_batt_box の cav_l + lip_t と一致させること
box_below   = 6;      // 同 end_t (箱の −Z 端壁が box_z0 より下へ出る量。皿ねじ下穴が入るので 6)
box_hx      = ci_box_hx;
// 2026-08-03: 94 -> 90。世界 Z=114 のねじ頭が MAIN の H3 ボス (X=-22, Z=119.5) に
//  乗っていた。batt_box の ear_hz と**両方**直すこと。
box_hz      = ci_box_hz;

/* [ケーブルレール (child_vtray_cable_rail) 固定 — 2026-08-03 追加] */
// 旧設計はレールのボルトが配線スリットの**中**に落ちていて締める相手が無かった。
// スリットを外した実肉部へ移し、デッキ側にバカ穴を開ける (レール側は M3 セルフタップ)。
rail_x      = 36;     // レール中心 X (±) = cable_x と一致させること
rail_hx     = 5.7;    // レール中心からのねじ間隔 (±) — cable_rail の mount_x と共通
rail_hz     = [37, 77];  // ねじ Z。cable_rail の mount_y + 20 と一致させること

/* [締結・配線] */
boss_d      = 8;      // スタンドオフ ボス外径
pilot_d     = 2.8;    // M3 セルフタップ下穴
clear_d     = 3.4;    // M3 バカ穴
rx_clear_d  = 3.4;    // M3 for separate edge-clamp bases; PCB holes unused
rx_clamp_x = 37.5;
rx_clamp_mount_z = [134.5,180.5];
m3_head_d   = 5.5;    // M3 なべ/キャップ頭Ø — デッキ上面に出る座面
m2_head_d   = 4.0;    // M2 なべ頭Ø

/* [下フランジ固定ラグ (BCD94 M3 ×2)] */
// 2026-08-28: child_vtray_batt_box のアンカー腕がデッキ板とレールを貫通していたので
// デッキ側へ移設。フランジ内面 (z=flange_ins) に立てた M3 MF10 スペーサ + 0.5 シムの
// 上にラグを載せ、M3×10 なべで締める (ワッシャ Ø7 は MAIN 基板端 44 に当たるので使わない)。
// docs/子機フランジねじ穴検証.md のねじ込み深さ制限 (4〜5mm) はスペーサのオス側に適用する。
flange_bcd    = 94;     // 下フランジ M3 穴 BCD (STEP 実測)
anchor_spacer = 10;     // M3 オスメススペーサ長
anchor_shim   = 0;      // シム無し (ラグをスペーサ上端 z=29 に直接載せる。旧案の 0.5 シムはラグ厚に吸収)
anchor_t      = 12;    // bearing seat Z29..41
anchor_od     = 5.4;      // 丸端幅。内側をX44.5で切り、穴まわり最小肉厚0.8、接線方向4.0以上
anchor_x_in   = 42.5;   // ラグ根元ブロックの内端 X (MAIN 基板端 44 + 0.8)
anchor_x_out  = 48.7;   // 根元の外端。チューブまで1 mm以上を確保
anchor_tangent = 20; // tangential extension between rounded ends
anchor_root_x = 28; // broaden root behind PCB, outside battery head reserve
anchor_root_y = -2.5; // 7.5 mm depth from bed; check actual PCB underside
anchor_bore = 3.4; // closed M3 clearance hole; no custom metal inserts
anchor_root_len=80;
heel_z0=19;
heel_r_in=44.6;
heel_y_span=10;
anchor_rib_z = 20; // start of the broad root reinforcement
main_edge_x   = 44.0;   // CHILD_MAIN 基板端 X (実基板 bbox ±44)
min_web     = 1.5;    // 穴の縁に残す最小肉厚
cable_w     = 14;     // デッキの配線/水抜きスリット 幅 (16 -> 14: 下記 assert のため)
// 2026-08-03: 30 -> 26。スリット間の桟が 8mm しかなく、そこへ移したレールの
//  ねじ頭 (Ø5.5) の縁の肉が取れなかった。桟 12mm になり板の曲げ剛性も上がる。
cable_l     = 26;     // 同 長さ (Z)
cable_x     = 36;     // 同 中心 X (±)
// 2026-08-03: [60,100,159] -> [58,96,157]。100 のスリット縁が MAIN H2/H4 ボスの
//  足元まで 0.5mm しか離れておらず、159 は RX 取付穴の縁と同着だった。
cable_z     = [58, 96, 157];   // 同 中心 Z。**ボス/穴の足元を抜かないこと** (assert)

/* [センタリングリブ (child_vtray_rib) の座] */
// 2026-09-03: **先端側ショルダーを廃止**。以前は両側にショルダー (幅 84) があったが、
// リブのスロットは 76.4 なので先端側ショルダーを越えられず、リブをデッキに嵌められなかった
// (人間指摘)。リブは先端から差し込んで内側ショルダーに当て、先端側は板を貫く
// **M2.5×6 なべ (頭 Ø4.5、板上面に座る) を抜け止め**にする。ねじ 1 本外せばリブが抜ける。
rib_thk     = 6;      // リブ板厚 = child_vtray_rib.rib_t (二重定義)
rib_off     = 4.5;    // デッキ端からリブ座 (リブの Z 始点) まで = 止めねじ頭の逃げ
rib_gap     = 7;      // リブ座から内側ショルダーまで (リブ 6 + 遊び 1)
stop_off    = 2.0;    // 止めねじ軸のデッキ端からの距離
stop_head_d = 4.5;    // M2.5 なべ頭Ø (screw_m2_5x6)
stop_pilot_d = 2.5;   // M3 self-tap pilot
stop_top_extension=0.5; // preserve M3 edge ligament without moving upper rib

$fn = 48;

// ---- 基板取付穴の変換 --------------------------------------------------
// KiCad 盤内座標 (基板左下原点 / Y 上向き正) から、この .scad の座標
// (X=機体幅 / Z=チューブ軸) への写像。**placement.json の ops と同じ式であること。**
//
//   MAIN / PWR : ops = translate([w/2, y0, z0]) → rotate([0,-90,-90])
//                STEP/STL は x=0..l, y=-w..0 なので (kx, ky) → X = w/2 - ky, Z = z0 + kx
//   RX         : ops = translate([w/2, y0, z0]) → rotate([-90,0,180])
//                                              → X = w/2 - kx, Z = z0 + ky
// この 3 行を書き換えるときは scad/lib/verify_child_holes.py も一緒に直すこと。
// 同スクリプトが .kicad_pcb の実座標と下の echo を突き合わせて DRIFT を検出する。
main_hx  = [for (ky = main_h_ky) main_w/2 - ky];   // → [ 39.5, -22.0 ]
main_hu  = main_h_kx;                              // → [  4.5,  99.5 ]
pwr_hx   = [for (ky = pwr_h_ky)  pwr_w/2  - ky];   // → [ 31.0, -31.0 ]
pwr_hu   = pwr_h_kx;                               // → [  4.0,  58.0 ]
rx_hx    = [for (kx = rx_h_kx)   rx_w/2   - kx];   // → [ 31.5, -31.5 ]
rx_hv    = rx_h_ky;                                // → [  2.5,  43.5 ]

// ---- 導出 -------------------------------------------------------------
r_use    = tube_id/2 - wall_clear;          // 幅広部で使える半径
r_bore   = (flange_bore - bore_clear)/2;    // 貫通口へ入る部分の許容半径
anchor_z0 = flange_ins + anchor_spacer + anchor_shim;   // ラグ下面 Z (= 29.5)
deck_y1  = deck_y0 + deck_t;
main_y   = deck_y1 + main_boss_h;           // MAIN 基板 下面 Y
pwr_y    = deck_y1 + pwr_boss_h;            // PWR 基板 下面 Y
rx_y     = deck_y0 - rx_stand;              // RX 基板 下面 Y (下向き = 部品は -Y)
wide_z0  = flange_ins + 1;
wide_z1  = tube_len - flange_ins - 1;
deck_z0  = -(cap_free - 1.7);
deck_z1  = tube_len + (cap_free - 1.7);
deck_len = deck_z1 - deck_z0;
pad_z    = [wide_z0 + (wide_z1-wide_z0)*0.25,
            wide_z0 + (wide_z1-wide_z0)*0.50,
            wide_z0 + (wide_z1-wide_z0)*0.75];
// リブ帯: リブは先端側から rib_off 内側に座り、内側ショルダー 1 本で止める (先端側は止めねじ)
rib_play = rib_gap - rib_thk;                              // 軸方向の遊び (1)
rib_z    = [deck_z0 + rib_off, deck_z1 - rib_off - rib_thk];   // リブの座 (Z 始点)
rib_sh_z = [rib_z[0] + rib_gap, rib_z[1] - rib_play - sh_t];   // 内側ショルダーの Z 始点
stop_z   = [deck_z0 + stop_off, deck_z1 - stop_off];           // 止めねじ軸 (板を Y に貫く)
band_lo  = rib_sh_z[0] + sh_t;               // ここから下は何も置けない
band_hi  = rib_sh_z[1];                      // ここから上は何も置けない
pwr_tip  = have_pwr ? max(0, pwr_z0 + pwr_l - wide_z1) : 0;  // 貫通口へ出る長さ

// ---- デッキ上面のフィーチャ一覧 ---------------------------------------
// 「デッキ板の上面で場所を取るもの」を 1 つの表にして総当りで検査する。
// 過去の不具合はどれもこの表が無かったことが原因:
//   ・MAIN のボスが実基板と 17.5mm ずれていた (誰も突き合わせていなかった)
//   ・RX のバカ穴が PWR ボスの足元に食い込んでいた
//   ・LiPo ベイのねじ頭が MAIN のボスに乗っていた
//   ・レールのボルトが配線スリットの空中に落ちていた
//
//   tops  = [X, Z, 半径, 名前]  デッキ上面に立つ材料 (スタンドオフ ボス)
//   holes = [X, Z, 半径, 名前]  貫通穴。半径は **バカ穴とねじ頭座の大きい方**
//                                (頭がデッキ上面に座るので、そこが場所を取る)
tops = concat(
    [for (i=[0:len(main_hx)-1]) for (j=[0:len(main_hu)-1])
        [main_hx[i], main_z0 + main_hu[j], boss_d/2, str("MAIN boss ", i, j)]],
    have_pwr ? [for (i=[0:len(pwr_hx)-1]) for (j=[0:len(pwr_hu)-1])
        [pwr_hx[i], pwr_z0 + pwr_hu[j], boss_d/2, str("PWR boss ", i, j)]] : []);

holes = concat(
    [for (sx=[-1,1]) for (zz=rx_clamp_mount_z)
        [sx*rx_clamp_x, zz, 3.3, "RX M3 edge clamp"]],
    [for (sx = [-1,1]) for (z = box_hz)
        [sx*box_hx, box_z0 + z, max(clear_d, m3_head_d)/2, str("LiPoベイ M3 Z", z)]],
    [for (sx = [-1,1]) for (dx = [-rail_hx, rail_hx]) for (z = rail_hz)
        [sx*rail_x + dx, z, max(clear_d, m3_head_d)/2, str("レール M3 X", sx*rail_x+dx)]]);

function rad(x, y) = sqrt(x*x + y*y);
function dist2d(a, b) = sqrt(pow(a[0]-b[0], 2) + pow(a[1]-b[1], 2));
// 点 (x,z) から、中心 (cx,cz) / 幅 w / 長さ l の矩形スリットまでの距離 (内側は 0)
function slot_gap(x, z, cx, cz, w, l) =
    let (dx = max(0, abs(x-cx) - w/2), dz = max(0, abs(z-cz) - l/2)) sqrt(dx*dx + dz*dz);

// ---- 干渉・成立性チェック ---------------------------------------------
// (1) チューブ内壁とのすきま — 断面の角をすべて軸心距離で見る
assert(rad(deck_w/2, deck_y0) <= r_use,
       str("デッキ中央部の隅がチューブに接触 r=", rad(deck_w/2, deck_y0), " > ", r_use));
assert(rad(pad_x, deck_y0 + 1) <= tube_id/2 - 1.0,
       str("振れ止めパッドがチューブに当たる r=", rad(pad_x, deck_y0 + 1)));
assert(rad(main_w/2, main_y - main_under) <= r_use, "MAIN 裏面リードの縁がチューブに接触");
assert(rad(main_w/2, main_y + main_lo_h) <= r_use,
       str("MAIN 低背ゾーンの縁がチューブに接触 r=", rad(main_w/2, main_y + main_lo_h)));
assert(rad(main_hi_x[1], main_y + main_hi_h) <= r_use,
       str("MAIN 高背ゾーン(DS3231スタック)がチューブに接触 r=",
           rad(main_hi_x[1], main_y + main_hi_h)));
// RX は幅方向のプロファイル未計測 → 全幅が最大高さと見なす (安全側)
assert(rad(rx_w/2, rx_y - rx_hi_h) <= r_use,
       str("RX (デッキ下面) の部品がチューブに接触 r=", rad(rx_w/2, rx_y - rx_hi_h)));
assert(rad(rx_w/2, rx_y + rx_under) <= r_use, "RX 裏面リードの縁がチューブに接触");
assert(!have_pwr || rad(pwr_w/2, pwr_y + pwr_hi_h) <= r_use,
       str("PWR 高背部がチューブに接触 r=", rad(pwr_w/2, pwr_y + pwr_hi_h)));
// LXDC55 は軸心付近だけ 35.1mm と突出する → 幅を絞って別に検査する
assert(!have_pwr || rad(pwr_vhi_x, pwr_y + pwr_vhi_h) <= r_use,
       str("PWR の LXDC55 縦挿しモジュールがチューブに接触 r=",
           rad(pwr_vhi_x, pwr_y + pwr_vhi_h), " > ", r_use));
assert(!have_pwr || rad(pwr_w/2, pwr_y - pwr_under) <= r_use, "PWR 裏面リードの縁がチューブに接触");

// (2) 貫通口 (Ø88.5) を通る部分
assert(rad(deck_wn/2, deck_y0) <= r_bore,
       str("デッキ端部 (幅", deck_wn, ") が貫通口を通らない r=", rad(deck_wn/2, deck_y0)));
assert(rad(sh_w/2, deck_y0) <= r_bore,
       str("リブ位置決めショルダー (幅", sh_w, ") が貫通口を通らない r=", rad(sh_w/2, deck_y0)));
assert(sh_w > deck_wn + 4, "ショルダーとデッキ端部の幅の差が無く、リブを止められない");
assert(deck_w > flange_bore, "デッキ中央部が貫通口より狭い — 軸方向のストッパにならない");
// PWR の先端が貫通口へ出るなら、そこは低背であること
assert(!have_pwr || pwr_tip == 0 || rad(pwr_w/2, pwr_y + pwr_tip_h) <= r_bore,
       str("PWR 先端 ", pwr_tip, "mm が貫通口へ出るのに、高さ ", pwr_tip_h,
           " では入らない r=", rad(pwr_w/2, pwr_y + pwr_tip_h), " > ", r_bore));

// (3) ボス/スペーサと基板裏の干渉
assert(main_boss_h > main_under + 1,
       str("MAIN のボス高さ ", main_boss_h, " が裏面リード ", main_under, " を逃げていない"));
assert(!have_pwr || pwr_boss_h > pwr_under + 1,
       str("PWR のボス高さ ", pwr_boss_h, " が裏面リード ", pwr_under, " を逃げていない"));
assert(rx_stand > rx_under + 1,
       str("RX のスペーサ長 ", rx_stand, " が裏面リード ", rx_under, " を逃げていない"));
for (x = concat(main_hx, have_pwr ? pwr_hx : [])) {
    assert(abs(x) + boss_d/2 <= deck_w/2, str("ボス (X=", x, ") がデッキ幅からはみ出す"));
    assert(rad(abs(x) + boss_d/2, deck_y1) <= r_use, str("ボス (X=", x, ") がチューブに接触"));
}

// (3b) 下フランジ固定ラグ
assert(rad(anchor_x_out, 0) <= tube_id/2 - 1.0 && rad(anchor_x_out, deck_y0 + deck_t) <= tube_id/2 - 1.0,
       str("フランジ固定ラグの根元がチューブに接触 r=", rad(anchor_x_out, deck_y0 + deck_t)));
assert(flange_bcd/2 + anchor_od/2 <= tube_id/2 - 1.0, "フランジ固定ラグの外周がチューブに接触");
assert(anchor_x_in >= main_edge_x - 1.5,
       "フランジ固定ラグが CHILD_MAIN 基板端に当たる");
assert(anchor_x_in < deck_w/2, "フランジ固定ラグの根元がデッキ板に乗っていない");
assert(anchor_z0 >= wide_z0 && anchor_z0 + anchor_t <= wide_z1, "フランジ固定ラグが幅広部の外");
for (t = tops)
    assert(abs(t[0]) + t[2] + 0.5 < anchor_x_in || t[1] + t[2] + 0.5 <= anchor_z0 || t[1] - t[2] - 0.5 > anchor_z0 + anchor_t,
           str("フランジ固定ラグが ", t[3], " と干渉"));

// (3c) リブ座と止めねじ
assert(stop_off + stop_top_extension - stop_pilot_d/2 >= 0.8, "止めねじ下穴がデッキ先端の縁を抜く");
assert(stop_off + stop_head_d/2 + 0.25 <= rib_off,
       str("止めねじの頭 (縁 z=", stop_off + stop_head_d/2, ") がリブ座 ", rib_off, " に掛かる"));
assert(rib_z[0] + rib_thk <= flange_ins && rib_z[1] >= tube_len - flange_ins,
       "リブがフランジ貫通口の中に入っていない");
assert(sh_w > deck_wn + 4 && sh_w > deck_wn, "内側ショルダーがリブのスロットより広くない (止まらない)");
assert(rad(stop_head_d/2, deck_y1 + 2) <= r_bore, "止めねじの頭が貫通口に当たる");

// (4) 軸方向の収まり
assert(main_z0 >= max(wide_z0, band_lo), "MAIN が幅広部/リブ帯より下から始まっている");
assert(main_z0 + main_l <= wide_z1, "MAIN が幅広部の上端を超えている");
assert(!have_pwr || pwr_z0 >= main_z0 + main_l + 1, "MAIN と CHILD_PWR が軸方向で重なる");
assert(!have_pwr || pwr_z0 + pwr_l <= band_hi,
       str("CHILD_PWR (Z ", pwr_z0, "..", pwr_z0 + pwr_l, ") が上リブ帯 ", band_hi,
           " に食い込む。→ 軸長は最大 ", band_hi - pwr_z0, "mm"));
assert(box_z0 >= wide_z0 && box_z0 + box_len <= wide_z1,
       "LiPo ベイ (幅広断面の部分) が幅広部からはみ出す");
assert(box_z0 - box_below >= band_lo,
       str("LiPo ベイの −Z 端壁 (z ", box_z0 - box_below, ") が下リブ帯 ", band_lo, " に入る"));
assert(rx_z0 >= box_z0 + box_len, "RX と LiPo ベイがデッキ下面で重なる");
assert(rx_z0 + rx_l <= wide_z1,
       str("RX (デッキ下面, Z ..", rx_z0 + rx_l, ") が幅広部 ", wide_z1,
           " を超える。下面の RX は断面が大きく貫通口へ出せない"));

// (5) デッキ上面のフィーチャ総当り検査 (過去の不具合はすべてここで止まる)
//     ボス同士は「くっついてよい」ので見ない。それ以外は必ず離す。

// 5a. 貫通穴 (ねじ頭座) 同士 — 縁の肉が残ること
for (i = [0:len(holes)-2]) for (j = [i+1:len(holes)-1])
    assert(dist2d(holes[i], holes[j]) >= holes[i][2] + holes[j][2] + min_web,
           str("貫通穴どうしが近すぎる: ", holes[i][3], " (X=", holes[i][0], ", Z=", holes[i][1],
               ") と ", holes[j][3], " (X=", holes[j][0], ", Z=", holes[j][1],
               ")  距離 ", dist2d(holes[i], holes[j]), " < ",
               holes[i][2] + holes[j][2] + min_web));

// 5b. ボス vs 貫通穴 — 穴とねじ頭がボスの足元を欠かないこと
for (b = tops) for (h = holes)
    assert(dist2d(b, h) >= b[2] + h[2],
           str("ボス ", b[3], " (X=", b[0], ", Z=", b[1], ") の足元を ",
               h[3], " (X=", h[0], ", Z=", h[1], ") が欠く。距離 ",
               dist2d(b, h), " < ", b[2] + h[2],
               "  → 基板の軸位置 (main_z0 / pwr_z0 / rx_z0) をずらすこと"));

// 5c. 配線スリット vs ボス / 貫通穴
for (cz = cable_z) for (sx = [-1, 1]) {
    for (b = tops)
        assert(slot_gap(b[0], b[1], sx*cable_x, cz, cable_w, cable_l) >= b[2],
               str("配線スリット (X=", sx*cable_x, ", Z=", cz, ") がボス ", b[3],
                   " (X=", b[0], ", Z=", b[1], ") の足元を抜いている。すきま ",
                   slot_gap(b[0], b[1], sx*cable_x, cz, cable_w, cable_l), " < ", b[2]));
    for (h = holes)
        assert(slot_gap(h[0], h[1], sx*cable_x, cz, cable_w, cable_l) >= h[2] + min_web,
               str("配線スリット (X=", sx*cable_x, ", Z=", cz, ") が ", h[3],
                   " (X=", h[0], ", Z=", h[1], ") の縁を欠いている。すきま ",
                   slot_gap(h[0], h[1], sx*cable_x, cz, cable_w, cable_l), " < ", h[2] + min_web));
}
for (cz = cable_z) {
    assert(cable_x + cable_w/2 < deck_w/2, "配線スリットがデッキ幅からはみ出す");
    assert(cz - cable_l/2 > wide_z0 && cz + cable_l/2 < wide_z1,
           str("配線スリット (Z=", cz, ") が幅広部の外に出ている"));
}

// 5d. 貫通穴がデッキ板の中に収まること (レールのボルトが板の外へ出ていた)
for (h = holes) {
    assert(abs(h[0]) + h[2] + min_web <= (h[1]>wide_z1 ? 42.5 : deck_w/2),
           str(h[3], " (X=", h[0], ") がデッキ幅 ", deck_w, " からはみ出す"));
    assert(h[1] - h[2] > wide_z0 && h[1] + h[2] < (h[3]=="RX M3 edge clamp" ? 188.5 : wide_z1),
           str(h[3], " (Z=", h[1], ") が幅広部 ", wide_z0, "..", wide_z1, " の外にある"));
    assert(rad(abs(h[0]) + h[2], deck_y0) <= r_use,
           str(h[3], " (X=", h[0], ") の縁がチューブに接触"));
}

// 5e. ケーブルレールの取付ねじが「実肉」にあること = スリットの中に無いこと
//     (旧設計はここが空中だった。締める相手が無く、ワイドワッシャも 16mm 幅の
//      スリットを渡れない。)
for (sx = [-1,1]) for (dx = [-rail_hx, rail_hx]) for (z = rail_hz)
    for (cz = cable_z) for (sx2 = [-1,1])
        assert(slot_gap(sx*rail_x + dx, z, sx2*cable_x, cz, cable_w, cable_l)
                   >= clear_d/2 + min_web,
               str("ケーブルレールのねじ (X=", sx*rail_x + dx, ", Z=", z,
                   ") が配線スリット (X=", sx2*cable_x, ", Z=", cz, ") に落ちている"));
assert(rail_x == cable_x, "レール中心とスリット中心がずれている (レールが溝をまたげない)");

// ---- モジュール -------------------------------------------------------
module boss(x, z, h) {
    translate([x, deck_y1, z]) rotate([-90, 0, 0]) difference() {
        cylinder(d = boss_d, h = h);
        translate([0, 0, 1.5]) cylinder(d = pilot_d, h = h);
    }
}

// ---- 本体 -------------------------------------------------------------
difference() {
    intersection() {
    union() {
        // Round the outline after union: adjacent plate sections stay connected.
        translate([0,deck_y1,0]) rotate([90,0,0]) linear_extrude(deck_t)
            offset(r=0.6,$fn=24) offset(delta=-0.6) union() {
                translate([-deck_w/2,wide_z0]) square([deck_w,wide_z1-wide_z0]);
                translate([-deck_wn/2,wide_z0]) square([deck_wn,deck_z1+stop_top_extension-wide_z0]);
                // Upper RX M3 seat fits the end flange bore (R44.25).
                translate([-42.5,176]) square([85,12.5]);
            }

        // 振れ止めパッド
        for (sx = [-1, 1]) for (z = pad_z)
            translate([sx > 0 ? deck_w/2 - 1 : -pad_x, deck_y0 + 1, z - pad_len/2])
                edge_round_box([pad_x - deck_w/2 + 1, deck_t - 2, pad_len]);

        // child_vtray_rib の位置決めショルダー
        for (zz = [rib_sh_z[1]])
            translate([-sh_w/2, deck_y0, zz]) cube([sh_w, deck_t, sh_t]);

        // 基板スタンドオフ (デッキ上面)
        for (x = main_hx) for (u = main_hu) boss(x, main_z0 + u, main_boss_h);
        if (have_pwr) for (x = pwr_hx) for (u = pwr_hu) boss(x, pwr_z0 + u, pwr_boss_h);

        // Compression heels bear directly on the flange annulus. Two local feet,
        // not a lower circular frame. Clearance bore surrounds existing MF10s.
        for(sx=[-1,1]) difference(){
            intersection(){
                translate([0,0,heel_z0]) cylinder(r=tube_id/2-1,h=anchor_z0-heel_z0+0.1,$fn=180);
                translate([sx>0 ? anchor_root_x : -tube_id/2,-heel_y_span,heel_z0])
                    cube([tube_id/2-anchor_root_x,heel_y_span+anchor_tangent/2,anchor_z0-heel_z0+0.1]);
            }
            translate([0,0,heel_z0-0.1]) cylinder(r=heel_r_in,h=anchor_z0-heel_z0+0.3,$fn=180);
            translate([sx*flange_bcd/2,0,heel_z0-0.1]) roof_bore_z(6.8,anchor_z0-heel_z0+0.3);
        }
        // Longer, wider root increases bending depth from 4 to 6.5 mm.

        // Round the YZ profile before extrusion: R3 concave root, R0.8 exposed edges.
        for (sx=[-1,1]) difference() {
            intersection() {
                union() {
                    translate([sx>0 ? anchor_root_x : -anchor_x_out,0,0])
                        rotate([90,0,90]) ci_rounded_extrude(anchor_x_out-anchor_root_x)
                        offset(r=0.8,$fn=32) offset(delta=-0.8)
                        offset(r=-3,$fn=48) offset(delta=3)
                        polygon([[deck_y0,anchor_rib_z],[anchor_root_y,anchor_rib_z],
                                 [anchor_root_y,anchor_z0-3],[2.2,anchor_z0],[2.2,anchor_z0+anchor_t],
                                 [anchor_root_y,anchor_z0+anchor_t+3],[anchor_root_y,anchor_rib_z+anchor_root_len],[deck_y0,anchor_rib_z+anchor_root_len]]);
                    // Tangential width spreads screw pressure and bending load.
                    translate([sx*flange_bcd/2,0,anchor_z0]) linear_extrude(anchor_t)
                        hull() for (yy=[-anchor_tangent/2,anchor_tangent/2]) translate([0,yy]) circle(d=anchor_od,$fn=64);
                }
                cylinder(r=tube_id/2-1,h=tube_len,$fn=180);
            }
            translate([sx*47,0,19]) roof_bore_z(anchor_bore,34);
            // Flat bearing planes at Z29/41, with tool/spacer clearance.
            translate([sx*47,0,19]) roof_bore_z(6.6,10);
            translate([sx*47,0,41]) roof_bore_z(6.6,12);
        }

    }
    // All structural material starts on the same Y=-10 print bed plane.
    translate([-tube_id,deck_y0,-10]) cube([2*tube_id,2*tube_id,tube_len+30]);
    }

    for(x=main_hx) for(u=main_hu)
        translate([x,deck_y1+1.5,main_z0+u]) rotate([-90,0,0])
            cylinder(d=pilot_d,h=main_boss_h+0.2,$fn=48);
    for(sx=[-1,1]) for(dx=[-rail_hx,rail_hx]) for(zz=rail_hz)
        translate([sx*rail_x+dx,deck_y1,zz]) rotate([-90,0,0])
            cylinder(d=6.8,h=4,$fn=64);

    // M3 rail screws: a 4 mm driver shaft must pass the reinforced root.
    // Keep the original head seat and its 6.8 mm x 4 mm recess unchanged.
    // The 4.6 mm continuation provides 0.3 mm radial clearance above it.
    if(tube_len==200)
        for(sx=[-1,1]) for(dx=[-rail_hx,rail_hx]) for(zz=rail_hz)
            translate([sx*rail_x+dx,deck_y1+3.9,zz]) rotate([-90,0,0])
                cylinder(d=4.6,h=8,$fn=64);

    // Actual MAIN underside 2.54 mm pin row. Broader roots cover six positions.
    for (pin_x=[-40.6,-38.06,-35.52,-32.98,-30.44,-27.90])
        translate([pin_x,-2.2,32.22]) rotate([-90,0,0]) cylinder(d=3,h=5.5,$fn=48);

    // RX edge-clamp bases: M3 outside the board, no PCB drilling.
    for (sx=[-1,1]) for (zz=rx_clamp_mount_z)
        translate([sx*rx_clamp_x, deck_y0 - 0.5, zz])
            rotate([-90, 0, 0]) cylinder(d = rx_clear_d, h = deck_t + 1);

    // LiPo ベイ (child_vtray_batt_box) 取付 M3 バカ穴
    for (sx = [-1, 1]) for (z = box_hz)
        translate([sx * box_hx, deck_y0 - 0.5, box_z0 + z])
            rotate([-90, 0, 0]) cylinder(d = clear_d, h = deck_t + 1);

    // ケーブルレール (child_vtray_cable_rail) 取付 M3 バカ穴
    //   デッキ上面からねじを入れ、レール側壁 (肉 8.9mm) へセルフタップする
    for (sx = [-1, 1]) for (dx = [-rail_hx, rail_hx]) for (z = rail_hz)
        translate([sx * rail_x + dx, deck_y0 - 0.5, z])
            rotate([-90, 0, 0]) cylinder(d = clear_d, h = deck_t + 1);

    // リブ抜け止めねじ (M2.5×6 なべ、板上面から) の下穴 — 両先端
    for (z = [stop_z[1]])
        translate([0, deck_y0 - 0.5, z])
            rotate([-90, 0, 0]) cylinder(d = stop_pilot_d, h = deck_t + 1);

    // 配線 / 水抜きスリット (LiPo ベイ・RX の左右。デッキの上下面をつなぐ)
    for (sx = [-1, 1]) for (z = cable_z)
        translate([sx * cable_x - cable_w/2, deck_y0 - 0.5, z - cable_l/2])
            edge_round_box([cable_w, deck_t + 6, cable_l]);
}

// 機械可読の取付穴テーブル。scad/lib/verify_child_holes.py が
// .kicad_pcb の実座標を同じ変換にかけて、この行と突き合わせる (DRIFT 検出)。
// 書式: HOLETABLE <基板名> <ねじ> <X>,<Z> ...
echo(str("HOLETABLE child_main M3",
         [for (x = main_hx) for (u = main_hu) str(" ", x, ",", main_z0 + u)]));
if (have_pwr)
    echo(str("HOLETABLE child_pwr M3",
             [for (x = pwr_hx) for (u = pwr_hu) str(" ", x, ",", pwr_z0 + u)]));
echo(str("CLAMPTABLE rx_improved_mini M3",
         [for (sx=[-1,1]) for (zz=rx_clamp_mount_z) str(" ", sx*rx_clamp_x, ",", zz)]));

echo(str("child_vtray_deck: tube_len=", tube_len, " deck material ", wide_z0, "..", deck_z1,
         " (幅広 ", wide_z0, "..", wide_z1, " / リブ帯外の使える範囲 ", band_lo, "..", band_hi,
         " / リブ座 ", rib_z, " 止めねじ ", stop_z, ")",
         "  MAIN ", main_z0, "..", main_z0+main_l,
         have_pwr ? str(" / PWR ", pwr_z0, "..", pwr_z0+pwr_l, " (先端 ", pwr_tip, " が貫通口)") : "",
         " / RX下面 ", rx_z0, "..", rx_z0+rx_l,
         "  PWR 軸長の上限=", band_hi - pwr_z0,
         "  最小チューブすきま=", tube_id/2 - max(
             rad(deck_w/2, deck_y0),
             rad(main_hi_x[1], main_y + main_hi_h),
             rad(rx_w/2, rx_y - rx_hi_h),
             have_pwr ? rad(pwr_w/2, pwr_y + pwr_hi_h) : 0)));

// R0.6 external edge rounds, kept inside the original interface envelope.
module edge_round_box(size) {
    r=min(0.6,min(size)/4);
    translate([r,r,r]) minkowski() {
        cube(size-[2*r,2*r,2*r]);
        sphere(r=r,$fn=16);
    }
}

// Horizontal screw/tool bores when deck is printed RX90: roof points +Y.
module roof_bore_z(d,h) {
    linear_extrude(h) union() {
        circle(d=d,$fn=64);
        polygon([[-d/sqrt(8),d/sqrt(8)],[0,d/sqrt(2)],[d/sqrt(8),d/sqrt(8)]]);
    }
}

