// =====================================================================
// child_cam_bridge.scad — 子機 カメラブリッジ (HP4/HP5 に M5×8 で外付け)
//
//   v2 (2026-09-06): `topo_v1/` のトポロジー最適化 (SIMP, 181.4 cm³) の結果を
//   cube/cylinder のパラメトリック形状に作り直したもの。v1 (328.1 cm³) からの
//   主な変更:
//     - 高さ 115mm の後ウェブ (x27..120, y67..73, z44.95..160) を廃止し、
//       **中央柱と同一面 (y 74.35..80.35) の深いスパインウェブ** に置き換えた。
//       最適化はこの面に材料を集中させた (y73..79 の帯だけで 47.8 cm³ = 全体の
//       26%) 一方、y67..73 の後ウェブ面には一切材料を置かなかった。
//     - 全面デッキ (x−120..120, y67..124, t8 = 109 cm³) を、荷重経路に沿う
//       帯だけ (後レール / マウント座 / 内側パネル / 外側パネル / 前レール) に
//       削った。最適化のデッキ層 (z44.95..53.95) は 782→628 ボクセルと
//       穴だらけだった。
//     - 最適化が中央上部に作ったアーチ (x±55, z45 → x0, z105) は、工具アクセス
//       Ø12 (x±20, z80/120/150/190) を厳密に避けると cube では通せないため、
//       **インボードリブ (x±(50..57) の YZ 縦板、z44.95..81.95)** と
//       **スパイン深部** で置き換えた。垂直荷重 (L1/L6) の余裕は解析で確認する。
//
//   子機外装_改善要件 (2026-09-04) §3.2、コーディネータ 2026-09-04 決定 1/2/3。
//   `child_jaw_gate` の HP4/HP5 (共通座面 y=74.35、法線 +Y、M5 熱圧入インサート
//   ×4 @ ±20 の HP40 規格) に左右各 4 本、計 8 本のボルトで留まる。
//   輸送時はこの 8 本を外してブリッジごと取り外す (C7)。
//
//   荷重経路 (最適化が選んだもの):
//     L4 正面衝突 (−Y)  : 前縁バンパ → 前レール/インボードリブ/端板 →
//                          スパイン (y74.35..80.35 の面内) → 中央柱 → HP4/HP5
//     L1/L6 上下        : マウント座 → デッキ → スパイン深部 (z44.95..81.95、
//                          x±57 と x±93..120) → 中央柱
//     L2s 側面衝突 (−X) : 端板 → スパイン (軸力) → 中央柱
//
//   機体座標: X 左右 (基線) / Y 前後 (+Y 前 = カメラ向き) / Z 上。
//   印刷向き: 中央柱を床にした +Y up (build_axis = Y、最適化と同じ)。
//
//   規約: cube/cylinder + boolean のみ (STEP を汚さない)。
// =====================================================================

/* [HP40 (child_jaw_gate 側, 2026-09-04 確定 — 二重定義: child_jaw_gate.scad)] */
hp4_z        = 170;    // HP4 (カメラブリッジ上) 座中心 z
hp5_z        = 100;    // HP5 (カメラブリッジ下) 座中心 z
hpl_z        = 15;     // HP-L (前向きライト) 座中心 z
hp_half      = 25;     // 座 (シェルフ) 半幅 (x, z とも) — child_jaw_gate.scad と同値
hp_seat_y    = 74.35;  // 座面 (共通平面)。法線 +Y — child_jaw_gate.scad の hp_seat_y
hp_shelf_dep = 12;     // シェルフ奥行き — child_jaw_gate.scad の hp_shelf_dep
hp_pitch_half = 20;    // M5 穴オフセット (hardpoint.scad HP_PITCH/2)
hp_bolt_d    = 5.4;    // M5 クリアランス (hardpoint.scad HP_BOLT_D)
adapter_t    = 6;      // 中央柱の板厚 (hardpoint.scad HP_ADAPTER_T)
gate_r_out   = 64.35;  // ゲート殻外径半径 (child_jaw_gate.scad r_out)
tool_d       = 12;     // HP4/HP5 の M5×8 を差す/回す直線アクセス径 (topo_v1 と同値)

/* [child_cam_mount 側 (2026-09-04 確定 — 二重定義: child_cam_mount.scad)] */
cm_lens_off_bot = 42.05; // レジスタ面→レンズ軸 (cam_mount ローカル X)
cm_fin_x1       = 30;    // レジスタ面 = plate_t(8) + fin_len(22) (cam_mount ローカル X)
cm_case_d       = 45.9;  // ケース奥行 (Y、cam_mount の case_d)
cm_case_w       = 94.7;  // ケース幅 (横向きでは機体 X 方向、cam_mount の case_w)
cm_case_h       = 84.1;  // ケース高さ (縦=タブ軸方向、横向きでは機体 Z 方向)
cm_plate_hw     = 22;    // 背面プレート半幅 (cam_mount ローカル Y = 機体 Y)
cm_plate_hh     = 17;    // 背面プレート半高 (cam_mount ローカル Z = 機体 X オフセット)
cm_fh_y         = 16;    // フレーム穴 Y オフセット (cam_mount ローカル Y = 機体 Y)
cm_fh_z         = 11;    // フレーム穴 Z オフセット (cam_mount ローカル Z = 機体 X オフセット)

/* [カメラ配置 (2026-09-04 決定 1/2)] */
lens_z      = 125;   // レンズ中心 z (不変)
lens_x      = 75;    // レンズ中心 |x| (基線 150/2、不変)
cam_y_shift = 14;     // レンズを +Y へ前進 (決定 2)
lens_y      = 106 + cam_y_shift; // レンズ面 y = 120 (仮値、cam_mount 実測待ちで変動)

/* [デッキ面 (決定 1: lens_z=125 のまま、deck_top = lens_z - lens_off_bot - fin_x1)] */
deck_t   = 8;
deck_top = lens_z - cm_lens_off_bot - cm_fin_x1;  // 52.95 (= register 面の下)
deck_bot = deck_top - deck_t;                     // 44.95 (ブリッジ最下面)

/* [中央柱: HP4/HP5 座 (preserve) を含む XZ 板] */
col_hw  = hp_half;                 // 25
col_y0  = hp_seat_y;                // 74.35
col_y1  = hp_seat_y + adapter_t;    // 80.35
col_z0  = deck_bot;                 // 44.95
col_z1  = hp4_z + hp_half;          // 195 (HP4 座上端)

/* [ウイング外形 / 端板 / 前縁バンパ (preserve、二重定義: child_side_bumper.scad)] */
wing_x1      = 120;    // ウイング外端 x (= ブリッジ全幅/2)
end_plate_t  = 6;      // 端板 (X 法線)。外面 x=±120 がバンパ L 形フットの密着面
end_plate_z1 = 80;     // 端板/前縁バンパ 上端 (ケース底 82.95 の 2.95mm 手前)
rear_y0      = 67;     // 端板の後端 = 設計空間後端 (topo_v1 ds_y0)
front_web_y0 = lens_y + 2;   // 122 (レンズ面より 2mm 前) = 前縁バンパ後面
front_web_y1 = lens_y + 8;   // 128 (フード限界) = 前縁バンパ前面
fb_x0        = 30;     // 前縁バンパ preserve の内端 (工具アクセス x26 から 4mm)

/* [スパイン: 中央柱と同一面 (y 74.35..80.35) の深いウェブ — 最適化の主部材]
   最適化は y73..79 (= 中央柱面) に 47.8 cm³、すなわち自由材料の 8 割超を置いた。
   z 上限はカメラケース底 (82.95) の 1mm 手前。x はマウント本体 (58..92) を避けて
   内側 (|x| <= 57) と外側 (93..120) の 2 区間に分かれる。 */
spine_z0     = deck_bot;              // 44.95
spine_z1     = 76.95;                 // 箱桁の後ウェブ (ケース底 82.95 に余裕)
spine_in_x   = 57;                    // mp_x0(58) の 1mm 手前
// 根元 (|x|<=57) のスパインは y67..80.35 の 13.35mm 厚にする。6mm 板のままだと
// ねじり定数 J=(1/3)bt³ が 11 倍小さく、ウイングの M_x / Mz が柱をねじって逃げる。
// y67 は設計空間後端 (ゲート殻から 2.65mm)、z 上限はアッパーデッキ上面。
spine_thick_y0 = rear_y0;             // 67
spine_thick_z1 = 72.95;               // = ud_z1
spine_out_x0 = 93;                    // mp_x1(92) の 1mm 外
spine_out_x1 = wing_x1;               // 120

/* [デッキ帯 (z deck_bot..deck_top)] */
deck_rear_y0 = 71;                    // 後レール後端 (ゲート殻 x=0 で 64.35 → 5.65mm)
deck_rear_y1 = col_y1;                // 80.35
mp_x0     = lens_x - cm_plate_hh;     // 58  (マウント座 = preserve)
mp_x1     = lens_x + cm_plate_hh;     // 92
mount_y0  = lens_y - cm_case_d / 2;   // 97.05 (レンズはケース中央にあると仮定)
mp_y0     = mount_y0 - cm_plate_hw;   // 75.05
mp_y1     = mount_y0 + cm_plate_hw;   // 119.05
deck_in_x0  = 46;    deck_in_x1  = mp_x0 + 2;   // 46..60 (座と 2mm 重ねる)
// 内側パネルはインボードリブの座 + マウント座とスパインを繋ぐせん断板。
// 根元の Mz はアッパーデッキが受け持つので x=40 から内側は不要。
deck_in_y0  = col_y0;                            // 74.35
deck_in_y1  = front_web_y0 + 2;                  // 124 (前縁バンパと 2mm 重ねる)
deck_out_x0 = mp_x1 - 2;  deck_out_x1 = wing_x1 - end_plate_t + 2;  // 90..116
deck_out_y0 = deck_rear_y0;  deck_out_y1 = 92;
deck_fr_y0  = 114;   deck_fr_y1  = front_web_y0 + 2;   // 114..124 (前縁バンパの下フランジ)

/* [アッパーデッキ (UD): z 64.95..72.95 の水平板。最適化のアーチ / クラウンと
   同じ役割 — ウイングの Mz (L4 の −Y 荷重 × 腕 95mm) を「y 方向の深さを持った
   まま」中央柱の HP5 座 (z75..125) の直下まで運ぶ。
   これが無いと Mz は中央柱 (y74.35..80.35 の 6mm 板) を Z 軸まわりに**ねじる**
   経路になり、薄板のねじり定数 J=(1/3)bt³=3600mm⁴ しかないため先端が 8〜10mm
   振れる (v2a/v2b/v2c で L4 たわみ 11.8/9.5/7.8mm を計測)。
   z は工具アクセス Ø12 の下端 (z74) より下に置く。こうすると x 14..26 を
   避けずに x −57..57 を連続で渡せる (x58..92 はマウント本体があるので不可)。
   y は設計空間後端 67 まで伸ばす — ケース (y74.1..120) は z82.95 以上なので
   この高さでは効かず、y 深さ 57mm ぶんの I_zz が只で手に入る。 */
ud_z0 = 64.95;
ud_z1 = 72.95;                        // 工具アクセス下端 (74) の 1mm 手前
ud_y0 = rear_y0;                      // 67
ud_y1 = front_web_y0 + 2;             // 124
ud_hx = spine_in_x;                   // 57 (マウント本体 x58 の 1mm 手前)
// 肉抜き窓: 支持部 (|x|<=25) の外、y の中央 (中立軸付近) を抜く。I_zz への寄与が
// 最も小さい領域。x22..27 / x55..57 に縦のリブが残るようにする。
udw_x0 = 27;  udw_x1 = 55;  udw_y0 = 88;  udw_y1 = 110;
// 外側 (x 57..120) はマウント本体 (y75.05..119.05) を避けて後ろ 8mm だけ張る。
// これでウイング外側の「上面が開いた溝形断面」が閉じ、L6 のねじれが減る。
ud_out_x0 = spine_in_x;               // 57
ud_out_y1 = mp_y0;                    // 75.05
// 外側は z44.95..72.95 の縦ウェブにする (デッキと ud_out の間 z52.95..64.95 が
// 空だと外側ウイングも 2 枚の独立した板になり、L6 のねじれ剛性が出ない)
ud_out_z0 = deck_bot;                 // 44.95

/* [前縦ウェブ: デッキ (z44.95..52.95) とアッパーデッキ (z64.95..72.95) の
   2 フランジを y=114..124 で結ぶ XZ 面のせん断ウェブ。
   これが無いと 2 枚の 8mm 板は y74..80 のスパイン付近でしか繋がらず、根元の
   有効 I_yy が 10,500mm⁴ (= 8mm 板 2 枚ぶん) しか出ない (v2g の L6 たわみ
   1.069mm から逆算)。前縁側に置くのは前縁バンパ/前レールと同一面だから。 */
webf_hx = spine_in_x;                 // 57
webf_y0 = 114;
webf_y1 = front_web_y0 + 2;           // 124
webf_z0 = deck_bot;                   // 44.95 (デッキと一体)
webf_z1 = ud_z1;                      // 72.95 (アッパーデッキと一体)

/* [インボードリブ: YZ 面の縦板。最適化のアーチ脚 (x±55 → 中央上部) の代替]
   スパイン (後) と前縁バンパ (前) を x≈54 で結ぶ深さ 37mm の板。
   工具アクセス Ø12 (x 14..26) の外、マウント本体 (x 58..92) の内。 */
rib_x1 = spine_in_x;                  // 57
rib_t  = 6;
rib_x0 = rib_x1 - rib_t;              // 50
rib_y0 = 76;                          // スパイン (74.35..80.35) と 4.35mm 重ねる
rib_y1 = 116;                         // 前は web_front が受ける
rib_z0 = deck_bot;                    // 44.95
rib_z1 = spine_z1;                    // 76.95

/* [マウント取付穴 (child_cam_mount 背面プレート M5×4 を横向きで受ける)] */
m5_clear = 5.4;
nut_af   = 8.2;    // M5 ナット 二面幅 +0.1
nut_dep  = 4.0;
mount_hole_y = [mount_y0 - cm_fh_y, mount_y0 + cm_fh_y]; // 81.05, 113.05
mount_hole_dx = cm_fh_z;                    // 11 (レンズ x からのオフセット)

/* [側面バンパ取合い (二重定義: child_side_bumper.scad)] */
bumper_t     = 9;
case_gap     = 2;               // ケース側面とバンパ内面のクリアランス
case_outer_x = lens_x + cm_case_w / 2;  // 122.35
bump_bolt_y  = [80, 116];        // 端板フランジへの M5×2 (y 位置、両ファイルで同値)
bump_bolt_z  = 65;               // 端板フランジ z 中心 (z<=78)

/* [ケース/マウント本体の干渉除外ボックス (2026-09-04 コーディネータ指示)] */
case_x0   = lens_x - cm_case_w / 2;         // 27.65 (ケース内側端)
case_x1   = case_outer_x;                   // 122.35
case_y0   = mount_y0 - cm_case_d / 2;       // 74.1 (ケース背面)
case_y1   = lens_y;                         // 120 (ケース前面 = レンズ面)
case_z0   = deck_top + cm_fin_x1;           // 82.95 (register 面 = ケース底)
case_z1   = case_z0 + cm_case_h;            // 167.05 (ケース上端)
mp_z0     = deck_top;                       // 52.95 (マウント本体の下端)
mp_z1     = case_z0;                        // 82.95
shelf_y0  = hp_seat_y - hp_shelf_dep;       // 62.35
shelf_y1  = hp_seat_y;                      // 74.35
tool_x    = [-hp_pitch_half, hp_pitch_half];                   // ±20
tool_z    = [hp5_z - hp_pitch_half, hp5_z + hp_pitch_half,
             hp4_z - hp_pitch_half, hp4_z + hp_pitch_half];    // 80,120,150,190

/* [機体レベル検査] */
env_half = 140;   // 全幅 280 の半分 (C5)
hpl_top  = hpl_z + hp_half;   // 40 (HP-L 座上端)
fov_half = 77.5;  // 対角 FOV 155° の半角 (水平 145° を内包する保守側)
hood_len = front_web_y1 - lens_y;   // 8

/* [Hidden] */
fudge = 0.01;
$fn = 64;

// ---- 干渉・成立性チェック -------------------------------------------
assert(deck_bot >= hpl_top + 2, "デッキ下端が HP-L 座 (z<=40) に 2mm 未満で接近");
assert(col_z1 <= 195, "ブリッジ最上端が 195 (HP4 座上端) を超える");
assert(wing_x1 <= 120, "ウイング先端が 240 枠 (半幅 120) を超える");
assert(deck_out_x1 <= wing_x1, "外側デッキが 240 枠を超える");
// ゲート殻 (r64.35) からの離隔: |x| < 64.35 で最も後ろにあるのは後デッキレール
assert(deck_rear_y0 - gate_r_out >= 2.6, "後デッキレールがゲート殻 (x=0) に 2.6mm 未満で接近");
// スパイン: ケース底 (82.95) の 1mm 手前で止まる / マウント本体 (x 58..92) を避ける
assert(spine_z1 <= case_z0 - 1, "スパイン上端がケース底面に 1mm 未満で接近");
assert(spine_in_x <= mp_x0 - 1, "スパイン内側区間がマウント本体 (x58) に 1mm 未満で接近");
assert(spine_out_x0 >= mp_x1 + 1, "スパイン外側区間がマウント本体 (x92) に 1mm 未満で接近");
assert(rib_x1 <= mp_x0 - 1, "インボードリブがマウント本体 (x58) に 1mm 未満で接近");
assert(rib_x0 >= max(tool_x) + tool_d / 2 + 3,
       "インボードリブが工具アクセス Ø12 (x<=26) に 3mm 未満で接近");
assert(ud_z1 <= min(tool_z) - tool_d / 2 - 1,
       "アッパーデッキ上端が工具アクセス Ø12 (z>=74) に 1mm 未満で接近");
assert(ud_hx <= mp_x0 - 1, "アッパーデッキがマウント本体 (x58) に 1mm 未満で接近");
assert(ud_z0 >= deck_top + 6, "アッパーデッキとデッキ上面の間が 6mm 未満");
assert(ud_y0 - gate_r_out >= 2.6, "アッパーデッキ後端がゲート殻 (x=0) に 2.6mm 未満で接近");
assert(fb_x0 >= max(tool_x) + tool_d / 2 + 3,
       "前縁バンパ内端が工具アクセス Ø12 (x<=26) に 3mm 未満で接近");
// 最小肉厚 (FEA の 2.0mm ボクセルで 3 要素以上を確保するため 6mm 以上)
assert(min(rib_t, adapter_t, end_plate_t, deck_t,
           front_web_y1 - front_web_y0) >= 6, "最小肉厚が 6mm を下回る");
// マウント M5 穴が座パッド内に縁距離 >=3 で収まる
assert(mount_hole_y[0] - mp_y0 >= 3, "マウント穴 (後側) の座パッド縁距離 < 3mm");
assert(mp_y1 - mount_hole_y[1] >= 3, "マウント穴 (前側) の座パッド縁距離 < 3mm");
assert(lens_x - mount_hole_dx - mp_x0 >= 3, "マウント穴 (内側) の座パッド縁距離 < 3mm");
assert(mp_x1 - (lens_x + mount_hole_dx) >= 3, "マウント穴 (外側) の座パッド縁距離 < 3mm");
// FOV: 前縁バンパ/端板の上端が視野円錐の外
fov_dz  = lens_z - end_plate_z1;        // 45 (下方)
fov_ang = atan(fov_dz / hood_len);      // atan(45/8) ~= 79.9°
assert(fov_ang > fov_half, "前縁バンパ上端が FOV (対角半角 77.5°) の内側に入る");
// バンパ外面 <= 280 枠
assert(case_outer_x + case_gap + bumper_t <= env_half,
       "側面バンパ外面が 280 枠を超える");
assert(bump_bolt_z <= end_plate_z1 - 2, "バンパ締結穴が端板上端に 2mm 未満で接近");
// preserve (最適化で固定した機能面) が新形状にそのまま入っていること
assert(col_y0 == 74.35 && col_y1 == 80.35 && col_hw == 25 && col_z1 == 195,
       "preserve: HP4/HP5 中央柱 (x±25, y74.35..80.35, z..195) が変わった");
assert(deck_bot == 44.95 && deck_top == 52.95, "preserve: cam_mount 座の厚み範囲が変わった");
assert(end_plate_z1 == 80 && rear_y0 == 67, "preserve: 端板/前縁バンパの z/y 範囲が変わった");

// ---- (a)(b)(c)(d) 総当り AABB 干渉検査 -------------------------------
// box = [x0,x1,y0,y1,z0,z1]。厳密不等号なので面接触 (共有面) は非干渉扱い。
function box_overlap(a, b) =
    (a[0] < b[1]) && (b[0] < a[1]) &&
    (a[2] < b[3]) && (b[2] < a[3]) &&
    (a[4] < b[5]) && (b[4] < a[5]);

bridge_boxes = [
    ["column",       [-col_hw, col_hw, col_y0, col_y1, col_z0, col_z1]],
    ["spine_in",     [-spine_in_x, spine_in_x, col_y0, col_y1, spine_z0, spine_z1]],
    ["spine_thick",  [-spine_in_x, spine_in_x, spine_thick_y0, col_y1, spine_z0, spine_thick_z1]],
    ["spine_out_R",  [spine_out_x0, spine_out_x1, col_y0, col_y1, spine_z0, spine_z1]],
    ["spine_out_L",  [-spine_out_x1, -spine_out_x0, col_y0, col_y1, spine_z0, spine_z1]],
    ["deck_rear",    [-wing_x1, wing_x1, deck_rear_y0, deck_rear_y1, deck_bot, deck_top]],
    ["deck_pad_R",   [mp_x0, mp_x1, mp_y0, mp_y1, deck_bot, deck_top]],
    ["deck_pad_L",   [-mp_x1, -mp_x0, mp_y0, mp_y1, deck_bot, deck_top]],
    ["deck_in_R",    [deck_in_x0, deck_in_x1, deck_in_y0, deck_in_y1, deck_bot, deck_top]],
    ["deck_in_L",    [-deck_in_x1, -deck_in_x0, deck_in_y0, deck_in_y1, deck_bot, deck_top]],
    ["deck_out_R",   [deck_out_x0, deck_out_x1, deck_out_y0, deck_out_y1, deck_bot, deck_top]],
    ["deck_out_L",   [-deck_out_x1, -deck_out_x0, deck_out_y0, deck_out_y1, deck_bot, deck_top]],
    ["deck_front_R", [fb_x0, wing_x1, deck_fr_y0, deck_fr_y1, deck_bot, deck_top]],
    ["deck_front_L", [-wing_x1, -fb_x0, deck_fr_y0, deck_fr_y1, deck_bot, deck_top]],
    ["upper_deck",   [-ud_hx, ud_hx, ud_y0, ud_y1, ud_z0, ud_z1]],
    ["rib_R",        [rib_x0, rib_x1, rib_y0, rib_y1, rib_z0, rib_z1]],
    ["rib_L",        [-rib_x1, -rib_x0, rib_y0, rib_y1, rib_z0, rib_z1]],
    ["fbump_R",      [fb_x0, wing_x1, front_web_y0, front_web_y1, deck_bot, end_plate_z1]],
    ["fbump_L",      [-wing_x1, -fb_x0, front_web_y0, front_web_y1, deck_bot, end_plate_z1]],
    ["end_plate_R",  [wing_x1 - end_plate_t, wing_x1, rear_y0, front_web_y1, deck_bot, end_plate_z1]],
    ["end_plate_L",  [-wing_x1, -(wing_x1 - end_plate_t), rear_y0, front_web_y1, deck_bot, end_plate_z1]],
    ["web_front",    [-webf_hx, webf_hx, webf_y0, webf_y1, webf_z0, webf_z1]],
    ["web_out_R",    [ud_out_x0, wing_x1, ud_y0, ud_out_y1, ud_out_z0, ud_z1]],
    ["web_out_L",    [-wing_x1, -ud_out_x0, ud_y0, ud_out_y1, ud_out_z0, ud_z1]],
];

keepout_boxes = concat([
    ["case_R",         [case_x0, case_x1, case_y0, case_y1, case_z0, case_z1]],
    ["case_L",         [-case_x1, -case_x0, case_y0, case_y1, case_z0, case_z1]],
    ["mount_body_R",   [mp_x0, mp_x1, mp_y0, mp_y1, mp_z0, mp_z1]],
    ["mount_body_L",   [-mp_x1, -mp_x0, mp_y0, mp_y1, mp_z0, mp_z1]],
    ["hp_shelf_HP4",   [-hp_half, hp_half, shelf_y0, shelf_y1, hp4_z - hp_half, hp4_z + hp_half]],
    ["hp_shelf_HP5",   [-hp_half, hp_half, shelf_y0, shelf_y1, hp5_z - hp_half, hp5_z + hp_half]],
    ["hp_shelf_HPL",   [-hp_half, hp_half, shelf_y0, shelf_y1, hpl_z - hp_half, hpl_z + hp_half]],
], [ for (sx = tool_x, tz = tool_z)
       [str("tool_", sx, "_", tz),
        [sx - tool_d/2, sx + tool_d/2, col_y1, front_web_y1 + 1, tz - tool_d/2, tz + tool_d/2]] ]);

for (bb = bridge_boxes)
    for (kb = keepout_boxes)
        assert(!box_overlap(bb[1], kb[1]), str(bb[0], " が ", kb[0], " と交差する"));

echo(str("deck z ", deck_bot, " .. ", deck_top, " / spine z ", spine_z0, " .. ", spine_z1));
echo(str("lens_y = ", lens_y, " (cam_y_shift = ", cam_y_shift, ")"));
echo(str("FOV 半角 (前縁バンパ) = ", fov_ang, "° (限界 ", fov_half, "°)"));
echo(str("AABB 検査: ", len(bridge_boxes), " 部材 × ", len(keepout_boxes), " 除外 = ",
         len(bridge_boxes) * len(keepout_boxes), " 組 PASS"));

// ---- モジュール -----------------------------------------------------

// 左右対称に置く直方体 (x0/x1 は +X 側の値。sign=-1 で鏡像)
module mirror_box(sign, x0, x1, y0, y1, z0, z1) {
    translate([sign > 0 ? x0 : -x1, y0, z0])
        cube([x1 - x0, y1 - y0, z1 - z0]);
}
// x について中心対称な直方体
module span_box(hx, y0, y1, z0, z1) {
    translate([-hx, y0, z0]) cube([2 * hx, y1 - y0, z1 - z0]);
}

// マウント M5 通し穴 + 下面ナットトラップ (垂直穴、軸 Z)
module mount_bolt(x, y) {
    translate([x, y, deck_bot - fudge])
        cylinder(d = m5_clear, h = deck_t + 2 * fudge, $fn = 32);
    translate([x, y, deck_bot - fudge])
        cylinder(d = nut_af / cos(30), h = nut_dep + fudge, $fn = 6);
    translate([x, y, deck_bot + nut_dep - fudge])
        cylinder(d1 = nut_af / cos(30), d2 = m5_clear,
                 h = (nut_af / cos(30) - m5_clear) / 2 + fudge, $fn = 32);
}

// バンパ締結: 端板フランジ側のナットトラップ (水平穴、軸 X、開口 = 端板外面)
module bump_nut(sign, y) {
    ang = -90 * sign;   // 右 (sign=+1): 局所+Z→機体−X (内向き)
    translate([sign * (wing_x1 + fudge), y, bump_bolt_z])
        rotate([0, ang, 0])
            cylinder(d = m5_clear, h = end_plate_t + 2 * fudge, $fn = 32);
    translate([sign * (wing_x1 + fudge), y, bump_bolt_z])
        rotate([0, ang, 0])
            cylinder(d = nut_af / cos(30), h = nut_dep + fudge, $fn = 6);
}

// 中央柱の M5×8 (HP4/HP5 各 4 本、軸 Y)
module column_holes() {
    for (hz = [hp4_z, hp5_z], sx = tool_x, sz = [-hp_pitch_half, hp_pitch_half])
        translate([sx, col_y0 - fudge, hz + sz])
            rotate([-90, 0, 0])
                cylinder(d = hp_bolt_d, h = adapter_t + 2 * fudge, $fn = 32);
}

// ---- 部材 -----------------------------------------------------------

// 中央柱 (HP40 アダプタ板)。preserve: 座 z75..125 / 145..195 を含む連続板
module column_solid() { span_box(col_hw, col_y0, col_y1, col_z0, col_z1); }

// スパイン: 中央柱と同一面の深いウェブ (最適化の主部材)
module spine_solid() {
    span_box(spine_in_x, col_y0, col_y1, spine_z0, spine_z1);
    span_box(spine_in_x, spine_thick_y0, col_y1, spine_z0, spine_thick_z1);
    for (s = [-1, 1])
        mirror_box(s, spine_out_x0, spine_out_x1, col_y0, col_y1, spine_z0, spine_z1);
}

// デッキ帯 (z deck_bot..deck_top)
module deck_solid() {
    // 後レール (全幅) — 端板・スパイン外側区間を繋ぎ、L2s の軸力経路になる
    span_box(wing_x1, deck_rear_y0, deck_rear_y1, deck_bot, deck_top);
    for (s = [-1, 1]) {
        // cam_mount 座 (preserve、上面が register 面 / 下面がナットトラップ開口)
        mirror_box(s, mp_x0, mp_x1, mp_y0, mp_y1, deck_bot, deck_top);
        // 内側パネル (インボードリブの座 + せん断板)
        // 内側パネル (インボードリブの座 + せん断板)
        mirror_box(s, deck_in_x0, deck_in_x1, deck_in_y0, deck_in_y1, deck_bot, deck_top);
        // 外側パネル (座と端板を繋ぐ)
        mirror_box(s, deck_out_x0, deck_out_x1, deck_out_y0, deck_out_y1, deck_bot, deck_top);
        // 前レール (前縁バンパ下フランジ。前縁バンパの面外曲げを止める)
        mirror_box(s, fb_x0, wing_x1, deck_fr_y0, deck_fr_y1, deck_bot, deck_top);
    }
}

// アッパーデッキ (XY 面の水平板。L4 の −Y 荷重を HP5 座の高さで中央柱へ渡す)
module upper_deck_solid() {
    difference() {
        span_box(ud_hx, ud_y0, ud_y1, ud_z0, ud_z1);
        for (s = [-1, 1])
            mirror_box(s, udw_x0, udw_x1, udw_y0, udw_y1, ud_z0 - fudge, ud_z1 + fudge);
    }
    span_box(webf_hx, webf_y0, webf_y1, webf_z0, webf_z1);   // 前縦ウェブ
    // 外側ウイングの後縦ウェブ (マウント本体 y75.05 の手前まで)
    for (s = [-1, 1]) mirror_box(s, ud_out_x0, wing_x1, ud_y0, ud_out_y1, ud_out_z0, ud_z1);
}

// インボードリブ (YZ 面の縦板。スパイン ↔ 前縁バンパ)
module rib_solid() {
    for (s = [-1, 1]) mirror_box(s, rib_x0, rib_x1, rib_y0, rib_y1, rib_z0, rib_z1);
}

// 前縁バンパ (preserve、L4 の荷重導入面) と 端板 (preserve、側面バンパ密着面)
module bumper_faces_solid() {
    for (s = [-1, 1]) {
        mirror_box(s, fb_x0, wing_x1, front_web_y0, front_web_y1, deck_bot, end_plate_z1);
        mirror_box(s, wing_x1 - end_plate_t, wing_x1, rear_y0, front_web_y1,
                   deck_bot, end_plate_z1);
    }
}

// ---- 形状 -----------------------------------------------------------
difference() {
    union() {
        column_solid();
        spine_solid();
        deck_solid();
        upper_deck_solid();
        rib_solid();
        bumper_faces_solid();
    }
    column_holes();
    for (s = [-1, 1]) {
        for (dx = [-mount_hole_dx, mount_hole_dx], y = mount_hole_y)
            mount_bolt(s * lens_x + dx, y);
        for (y = bump_bolt_y) bump_nut(s, y);
    }
}
