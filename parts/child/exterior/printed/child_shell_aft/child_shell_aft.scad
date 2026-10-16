// =====================================================================
// child_shell_aft.scad — 子機 外装 後半シェル (1個印刷)
//
// 子機は耐圧容器(WTE4 4in x 200mm)を「縦置き・ドーム上向き」で吊り下げる。
// 容器を前後 2 枚の 3Dプリントシェルで挟む (ManaFish ROV 方式)。
// この後半シェルはフレーム本体で常設側。前半シェル(child_shell_fwd)を
// M5 蝶ボルト 4 本で外すと、容器を真上に抜ける。
//
//   持つもの: 吊り耳 x2 (ロープ 2点ブライドル) / 後部パイロン
//             (上面 = TD04A ソケット台 / 内部 = ケーブル導管 + 取っ手バー)
//             / 下部ガード取付ボス x4 / 合わせ面レール x2
//
// 座標系: Z = 上 (チューブ下端面が z=0)、+Y = カメラの向き(前)、X = 基線方向。
//         このシェルは y <= 0 側のみ。
// 印刷向き: このまま (Z が積層方向)。サポート不要。
//   底のフレア(z18..28)がベッド接地面。ブリム 3mm 推奨、PETG / X1-Carbon。
//   吊り耳は積層に垂直な引張を受けるので、壁 5 本以上・インフィル 40% 以上。
// =====================================================================

/* [耐圧容器 (STL 実測)] */
tube_od      = 114.3;   // アクリルチューブ OD
pad_t        = 1.2;     // 保護シート厚 (EVA/ゴム) 片側
dome_ring_od = 114.3;   // ドーム押えリング OD
dome_clear   = 8;       // ドームを真上に抜くための逃げ (直径あたり)

/* [シェル共通 — child_shell_fwd と同じ値にすること] */
skin_t    = 6;              // スキン肉厚
shell_z0  = 18;             // シェル下端 z
shell_z1  = 190;            // シェル上端 z
rail_x0   = 56;             // 合わせ面レール 内側 x
rail_x1   = 80;             // 同 外側 x
rail_t    = 10;             // 同 厚み (Y)
boss_t    = 24;             // ボルトボス厚み (Y)
bolt_x    = 70;             // 締結 M5 の x (±)
bolt_z    = [42, 150];
pin_z     = 100;            // 位置決めピン z
pin_d     = 6;
flare_r   = 78;             // 底フレア 外半径 (ベッド接地面 + 下部ガード取付座)
flare_h   = 10;             // 底フレア 高さ
m5_d      = 5.4;
nut_af    = 8.2;            // M5 ナット 二面幅 + 余裕
nut_t     = 4.4;

/* [吊り耳 (ロープ 2点ブライドル)] */
ear_y0    = -42;            // 耳板 y 範囲
ear_y1    = -26;
ear_x1    = 92;             // 耳板 外側 x
ear_z0    = 140;            // 耳板 下端 (スキン側)
ear_slp_x = 48;             // ここより外側は下面を 45deg に逃がす (無サポート)
eye_x     = 80;             // ロープ穴 x
eye_z     = 234;            // ロープ穴 z
eye_d     = 16;             // ロープ穴 Ø (10mm ロープ / M10 シャックル)
eye_boss  = 36;             // 穴まわりのボス Ø
eye_bos_t = 24;             // 同 厚み (Y)

/* [後部パイロン (TD04A 台 + 取っ手 + ケーブル導管)] */
py_x      = 50;             // パイロン半幅 (X)
py_y      = -115;           // パイロン後端 y (機体の最後端)
py_z1     = 182;            // = TD04A 取付パッド上面
py_wall   = 6;
und_y     = -64;            // 下面 45deg 斜面の基準点 (スキン外周)
und_z     = 26;             //   同上。z = und_z + (und_y - y) より下を削る
cav_y1    = -70;            // 内部空洞の前端 (スキンを残すためここで止める)
roof_t    = 16;             // 屋根厚 (TD04A の下穴タッピング代を確保)
rib_t     = 6;              // 屋根を支える中央リブ厚
rib_z0    = 145;            // 中央リブ 下端
open_z1   = 140;            // ここより下は後面も開放 (手を入れる / 排水 / 配線)
grip_y    = -98;            // 取っ手バー 中心 y
grip_z    = 118;            // 同 中心 z
grip_d    = 30;             // 同 対角径 (六角・頂点下向きで無サポート)

/* [TD04A ソケット取付 (xdcr_socket の base_w=60 / hole_p=40 と一致)] */
// 空洞の奥行(39)より穴ピッチ(40)が広く、前側 2 穴の裏側は中実になる。
// そのためナットではなく「下穴 + M5 タッピングねじ」で留める。
// 着脱を繰り返すなら Ø6.4x9.5 の M5 熱圧入インサートに置換すること。
xd_y      = -86;            // ソケット中心 y
xd_pitch  = 40;             // M5 4穴ピッチ
xd_pilot  = 4.3;            // M5 タッピング下穴 Ø
xd_pilot_h = 12;            // 同 深さ
xd_cbl_d  = 14;             // 屋根のケーブル通し穴

/* [下部ガード取付] */
guard_r   = 70;                   // 取付ボス 半径位置
guard_a   = [40, -40, 68, -68];   // 同 方位角 (0 = 真後ろ -Y)
guard_bd  = 22;                   // ボス Ø
guard_bh  = 14;                   // ボス 高さ (shell_z0 から)

/* [通水・結束] */
vent_d    = 12;
vent_a    = [66, -66];
vent_z    = [45, 78, 111];
tie_w     = 4;                    // 結束バンド 4.8mm 帯
tie_h     = 12;
tie_y     = [-85, -100];
tie_z     = [74, 92, 158];
pvent_d   = 16;                   // パイロン前面の通水・軽量化穴 (Y方向)
pvent_x   = [-22, 22];
pvent_z   = [60, 100, 140];

$fn = 96;

// ---- 導出 -----------------------------------------------------------
bore_d   = tube_od + 2*pad_t;          // 116.7
bore_r   = bore_d/2;                   // 58.35
skin_r   = bore_r + skin_t;            // 64.35
dclr_d   = dome_ring_od + dome_clear;  // 122.3
dclr_r   = dclr_d/2;
ear_ym   = (ear_y0 + ear_y1)/2;        // 耳板 中心 y
eye_xi   = eye_x - eye_boss/2;         // 耳ボス 内側 x
grip_af  = grip_d*cos(30);             // 取っ手 二面幅 (握り径)
py_a     = asin(py_x/skin_r);          // スキン上でパイロンが占める方位角
und_at   = function (y) und_z + (und_y - y);   // 下面斜面の高さ

// ---- 干渉・成立性チェック --------------------------------------------
// 1) ドームを真上に抜けること (吊り耳ボスの最内点が逃げ円の外)
assert(sqrt(pow(eye_xi,2) + pow(ear_y1,2)) > dclr_r + 1,
       str("吊り耳ボスがドーム抜き取り経路と干渉: 最内 r=",
           sqrt(pow(eye_xi,2) + pow(ear_y1,2)), " 必要 >", dclr_r + 1));
// 2) 締結ボルト/ナットがチューブ穴に噛まないこと
assert(bolt_x - m5_d/2 > bore_r + 2, "締結M5がチューブ穴と干渉");
assert(bolt_x - nut_af/(2*cos(30)) > bore_r + 1, "M5ナットがチューブ穴と干渉");
assert(bolt_x + nut_af/(2*cos(30)) < rail_x1, "M5ナットがレール外へはみ出し");
// 3) ボルトボス(y -boss_t..0) と 吊り耳(ear_y0..ear_y1) が重ならないこと
//    重なるとナットの横挿しスロットが耳板で塞がれて組めない
assert(ear_y1 <= -boss_t, str("吊り耳がボルトボスと重なる: ear_y1=", ear_y1,
                              " boss は y=", -boss_t, " まで"));
// 4) 吊り耳の肉厚・端距離
assert((eye_boss - eye_d)/2 >= 8, "ロープ穴まわりの肉厚不足 (8mm 以上)");
assert(ear_x1 >= eye_x + eye_d/2 + 4, "ロープ穴の外側端距離不足");
// 5) TD04A 取付穴がパイロン屋根に収まり、チューブ穴に抜けないこと
assert(xd_y - xd_pitch/2 - 4 > py_y, "TD04A の後側取付穴がパイロン後端からはみ出し");
assert(xd_pitch/2 + 4 < py_x, "TD04A の取付穴がパイロン側壁からはみ出し");
assert(sqrt(pow(xd_pitch/2,2) + pow(xd_y + xd_pitch/2,2)) > bore_r + 4,
       str("TD04A の前側取付穴がチューブ穴に掛かる: r=",
           sqrt(pow(xd_pitch/2,2) + pow(xd_y + xd_pitch/2,2)), " 必要 >", bore_r + 4));
assert(xd_y < cav_y1 - 5 && xd_y > py_y + py_wall + 5,
       "TD04A のケーブル穴が空洞(導管)に通じていない");
assert(roof_t - xd_pilot_h >= 3, "TD04A 下穴で屋根を抜く (屋根厚を増やすこと)");
// 下穴の真上に何も無いこと。スキン外周(や外向きカラー)が被ると下穴が
// 「閉じた空洞」になり、ソリッドが分離して組立もできなくなる (実際に踏んだ)
assert(sqrt(pow(xd_pitch/2,2) + pow(xd_y + xd_pitch/2,2)) > skin_r + 2,
       str("TD04A の前側取付穴がスキン外周に掛かる: r=",
           sqrt(pow(xd_pitch/2,2) + pow(xd_y + xd_pitch/2,2)), " 必要 >", skin_r + 2));
// 6b) 吊り耳の 45deg 逃げは、支えのある範囲 (パイロン側壁の内側) から始めること
assert(ear_slp_x <= py_x, "吊り耳の45deg逃げ開始が外すぎる (下面が宙に浮く)");
// 6) 取っ手の成立性
assert(grip_z - grip_d/2 - und_at(grip_y) >= 35,
       str("取っ手の指スペース不足: ", grip_z - grip_d/2 - und_at(grip_y), "mm"));
assert(grip_z + grip_d/2 < rib_z0, "取っ手バーが中央リブと干渉");
assert(grip_af >= 24 && grip_af <= 34, "取っ手の握り径が手に合わない");
assert(cav_y1 - (grip_y + grip_d/2) >= 10, "取っ手バーの前に指先の逃げがない");
assert(grip_y - grip_d/2 >= py_y, "取っ手バーがパイロン後端からはみ出し");
// 7) 空洞がスキンを食わないこと (食うとチューブが露出して保護にならない)
assert(cav_y1 < -skin_r - 4, str("空洞前端がスキンに掛かる: cav_y1=", cav_y1,
                                 " スキン外周 ", -skin_r));
// 8) 下部ガード取付ボスが空洞/レールに掛からないこと
for (a = guard_a) {
    gy = -guard_r*cos(a);
    gx = abs(guard_r*sin(a));
    assert(gy + guard_bd/2 > cav_y1 || gx - guard_bd/2 > py_x - py_wall,
           str("ガード取付ボス a=", a, " がパイロン空洞に掛かる"));
    assert(gy + guard_bd/2 < -rail_t - 3 || gx + guard_bd/2 < rail_x0,
           str("ガード取付ボス a=", a, " が合わせ面レールに掛かる"));
    assert(guard_r + guard_bd/2 <= flare_r + 3,
           str("ガード取付ボス a=", a, " が底フレアからはみ出し"));
}
// 9) 通水穴が合わせ面レール/パイロン/吊り耳に掛からないこと
for (a = vent_a) {
    assert(skin_r*abs(sin(a)) - vent_d/2 > py_x + 2,
           str("通水穴 a=", a, " がパイロン側壁に掛かる"));
    assert(skin_r*cos(abs(a)) - vent_d/2 > rail_t + 2,
           str("通水穴 a=", a, " が合わせ面レールに掛かる"));
    for (z = vent_z)
        assert(z + vent_d/2 < ear_z0 || skin_r*cos(abs(a)) - vent_d/2 > -ear_y1,
               str("通水穴 a=", a, " z=", z, " が吊り耳に掛かる"));
}
// 9b) 結束スロットがパイロン下面の 45deg 斜面/ 取っ手バーに接しないこと
//     斜面にちょうど接すると稜線が縮退して非マニフォールドになる (実際に踏んだ)
for (ty = tie_y) for (tz = tie_z) {
    assert(tz - tie_h/2 > und_at(ty - tie_w/2) + 2,
           str("結束スロット (y=", ty, " z=", tz, ") がパイロン下面の45deg斜面に掛かる"));
    assert(abs(tz - grip_z) > grip_d/2 + tie_h/2 + 2 || abs(ty - grip_y) > grip_d/2 + tie_w/2,
           str("結束スロット (y=", ty, " z=", tz, ") が取っ手バーと干渉"));
    assert(tz + tie_h/2 < py_z1 - roof_t + 2, "結束スロットが TD04A 取付パッドの直下を抜く");
}
// 9c) パイロン前面の通水穴が吊り耳/取っ手/ガードボスに掛からないこと
for (vx = pvent_x) for (vz = pvent_z) {
    assert(abs(vx) + pvent_d/2 < py_x - py_wall, "パイロン通水穴が側壁に掛かる");
    assert(vz - pvent_d/2 > und_at(cav_y1-8) + 2, "パイロン通水穴が下面の45deg斜面に掛かる");
    assert(vz + pvent_d/2 < ear_z0 || abs(vx) + pvent_d/2 < ear_slp_x,
           "パイロン通水穴が吊り耳に掛かる");
    assert(vz - pvent_d/2 > shell_z0 + guard_bh + 4, "パイロン通水穴がガード取付ボスに掛かる");
}
// 10) 250 x 250 x 300 の外形枠 (このシェル単独分)
assert(2*max(ear_x1, py_x, rail_x1) <= 250, "全幅が 250 超");
assert(-py_y <= 125, "後端が 125 超");

// ---- 共通モジュール ---------------------------------------------------
// 軸 = +Y (0..h)、稜が +Z を向くティアドロップ穴。横穴を無サポートで抜く。
// cube + cylinder だけで作る (linear_extrude(polygon) は FreeCAD の CSG→STEP で
// "Null input shape" になり STEP が出ない。実際に踏んだ)。
// 一辺 r の cube を 225deg 回すと、原点を頂点に、稜が -y 方向 r*sqrt(2) に立つ。
module teardrop_py(d, h) {
    r = d/2;
    rotate([-90,0,0]) union() {
        cylinder(d=d, h=h);
        rotate([0,0,225]) cube([r, r, h]);
    }
}
// z + y < und_z + und_y の半空間 (パイロン下面 45deg を作る)
module under_plane() {
    translate([0, und_y, und_z]) rotate([-45,0,0])
        translate([-300,-300,-600]) cube([600,600,600]);
}

// ---- 部品 -------------------------------------------------------------
// 半円筒スキン + 底フレア。
// 上端に外向きカラーを付けてはいけない: TD04A 取付パッド(パイロン屋根 z=py_z1)を
// 覆ってしまい、下穴が「閉じた空洞」になって組立もできなくなる。
// 上端の丸めは Fusion 側で付ける (CLAUDE.md の設計規約)。
module skin() {
    intersection() {
        union() {
            translate([0,0,shell_z0]) cylinder(r=skin_r, h=shell_z1-shell_z0);
            translate([0,0,shell_z0]) cylinder(r1=flare_r, r2=skin_r, h=flare_h);
        }
        translate([-200,-200,shell_z0]) cube([400,200,400]);   // y<=0 のみ
    }
}

module rail_pair() {                  // 合わせ面レール + ボルトボス
    for (s=[-1,1]) mirror([s<0?1:0,0,0]) {
        translate([rail_x0, -rail_t, shell_z0])
            cube([rail_x1-rail_x0, rail_t, shell_z1-shell_z0]);
        for (bz=bolt_z)
            translate([rail_x0, -boss_t, bz-16])
                cube([rail_x1-rail_x0, boss_t, 32]);
    }
}

module lift_ears() {                  // 吊り耳 (内側はチューブ穴/ドーム逃げで削る)
    for (s=[-1,1]) mirror([s<0?1:0,0,0]) difference() {
        union() {
            translate([40, ear_y0, ear_z0])
                cube([ear_x1-40, ear_y1-ear_y0, eye_z-ear_z0]);
            translate([eye_x, ear_ym + eye_bos_t/2, eye_z])
                rotate([90,0,0]) cylinder(d=eye_boss, h=eye_bos_t);
        }
        // 外側の下面を 45deg に逃がす (z < x + (ear_z0 - ear_slp_x) を削る)。
        // これを入れないと x>skin_r の範囲で水平オーバーハングになる。
        translate([ear_slp_x, 0, ear_z0]) rotate([0,-45,0])
            translate([-300,-300,-600]) cube([600,600,600]);
    }
}

module pylon() {                      // 後部パイロン (下面は 45deg でサポート不要)
    difference() {
        union() {
            translate([-py_x, py_y, shell_z0]) cube([2*py_x, -py_y+20, py_z1-shell_z0]);
            translate([-rib_t/2, py_y, rib_z0]) cube([rib_t, -py_y+20, py_z1-rib_z0]);
        }
        under_plane();
    }
}

module guard_bosses() {               // 下部ガード取付ボス
    for (a=guard_a)
        translate([guard_r*sin(a), -guard_r*cos(a), shell_z0])
            cylinder(d=guard_bd, h=guard_bh);
}

// ---- 切り欠き ---------------------------------------------------------
module cut_bore() {                   // チューブ穴 + ドーム抜き取り逃げ
    translate([0,0,shell_z0-6]) cylinder(d=bore_d, h=shell_z1-shell_z0+8);
    translate([0,0,shell_z1]) cylinder(d=dclr_d, h=140);
}

module cut_fwd_half() {               // 合わせ面 (y=0) より前を落とす
    translate([-300, 0, -50]) cube([600, 300, 500]);
}

module cut_bolts() {                  // 締結 M5 + 横挿しナットトラップ
    for (s=[-1,1]) mirror([s<0?1:0,0,0]) for (bz=bolt_z) {
        translate([bolt_x, -boss_t-3, bz]) teardrop_py(m5_d, boss_t+8);
        translate([bolt_x, -16, bz]) rotate([90,0,0])
            cylinder(d=nut_af/cos(30), h=nut_t, $fn=6);
        translate([bolt_x - nut_af/2, -16-nut_t, bz-nut_af/2])
            cube([rail_x1 - bolt_x + nut_af/2 + 3, nut_t, nut_af]);
    }
}

module cut_pylon_inside() {           // 導管 + 手入れ空間 + 屋根裏
    cw = py_x - py_wall;
    cd = cav_y1 - (py_y - 6);
    translate([-cw, py_y-6, shell_z0-8])                       // 下: 後面まで開放
        cube([2*cw, cd, open_z1-shell_z0+8]);
    translate([-cw, py_y+py_wall, open_z1])                    // 中: 後壁あり
        cube([2*cw, cav_y1-(py_y+py_wall), rib_z0-open_z1]);
    for (s=[-1,1])                                             // 上: 中央リブを残す
        translate([s<0 ? -cw : rib_t/2, py_y+py_wall, rib_z0])
            cube([cw-rib_t/2, cav_y1-(py_y+py_wall), py_z1-roof_t-rib_z0]);
}

module cut_eyes() {                   // ロープ穴 (ティアドロップで無サポート)
    for (s=[-1,1]) mirror([s<0?1:0,0,0])
        translate([eye_x, ear_ym - eye_bos_t/2 - 2, eye_z])
            teardrop_py(eye_d, eye_bos_t+4);
}

module cut_xdcr() {                   // TD04A ソケット 下穴 x4 + ケーブル穴
    for (sx=[-1,1]) for (sy=[-1,1])
        translate([sx*xd_pitch/2, xd_y + sy*xd_pitch/2, py_z1-xd_pilot_h])
            cylinder(d=xd_pilot, h=xd_pilot_h+1);
    translate([0, xd_y, py_z1-roof_t-2]) cylinder(d=xd_cbl_d, h=roof_t+4);
}

module cut_guard_holes() {            // 下部ガード M5 (上面にナットポケット)
    for (a=guard_a)
        translate([guard_r*sin(a), -guard_r*cos(a), shell_z0-2]) {
            cylinder(d=m5_d, h=guard_bh+4);
            translate([0,0,guard_bh+2-nut_t])
                cylinder(d=nut_af/cos(30), h=nut_t+3, $fn=6);
        }
}

module cut_vents() {                  // 通水・軽量化
    for (a=vent_a) for (z=vent_z)
        rotate([0,0,a]) translate([0, -(skin_r+16), z])
            teardrop_py(vent_d, skin_t+26);
}

// パイロン前面 (空洞前端〜スキン) の中実部を Y 方向に抜く。
// 排水・軽量化・チューブの目視点検を兼ねる。
module cut_pylon_vents() {
    for (vx=pvent_x) for (vz=pvent_z)
        translate([vx, cav_y1-8, vz]) teardrop_py(pvent_d, 40);
}

module cut_ties() {                   // 結束バンド (パイロン側壁を貫通)
    for (ty=tie_y) for (tz=tie_z)
        translate([-py_x-4, ty-tie_w/2, tz-tie_h/2])
            cube([2*py_x+8, tie_w, tie_h]);
}

// ---- 本体 -------------------------------------------------------------
union() {
    difference() {
        union() {
            skin();
            rail_pair();
            lift_ears();
            pylon();
            guard_bosses();
        }
        cut_bore();
        cut_fwd_half();
        cut_bolts();
        cut_pylon_inside();
        cut_eyes();
        cut_xdcr();
        cut_guard_holes();
        cut_vents();
        cut_pylon_vents();
        cut_ties();
    }
    // 取っ手バー: 空洞を横切るので空洞カットの後に足す。六角・頂点下向きで無サポート
    translate([0, grip_y, grip_z])
        rotate([0,90,0]) cylinder(d=grip_d, h=2*(py_x-py_wall)+6, $fn=6, center=true);
    // 位置決めピン: y>0 へ出るので合わせ面カットの後に足す。
    // y=-1 から生やしてレールと確実に融合させる (y=0 起点だと面接触で別ソリッドになる)
    for (s=[-1,1])
        translate([s*bolt_x, -1, pin_z]) rotate([-90,0,0])
            cylinder(d1=pin_d, d2=pin_d-1.2, h=7);
}

echo(str("bore=", bore_d, " skin_r=", skin_r));
echo(str("外形 W=", 2*ear_x1, "  y=", py_y, "..0  z=", shell_z0, "..", eye_z+eye_boss/2));
echo(str("取っ手 握り径=", grip_af, " 指スペース=", grip_z-grip_d/2-und_at(grip_y)));
echo(str("パイロン方位角=", py_a, "deg"));
