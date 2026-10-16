// =====================================================================
// parent_pod_body.scad — 親機 カメラポッド本体 (深度~0.5m用)
// Pi Zero 2W + GSカメラ + 4mmレンズ + 520nmBPF を同軸実装する円筒。
// 前面: アクリルフラットポート(Ø72×t4) + 面シールOリング + ベゼル
// (parent_pod_bezel) を M3×6 で締結。後面: WetLink M10 ペネトレータ×1
// (電源2線)。側面: マストヘッドへの M4 セルフタップボス×4。
// ★3Dプリント防水の注意: PETG/ASA・壁4mm・内面エポキシコート+気密試験
//   必須(詳細設計書1.6節)。
// 印刷向き: 後面(閉端)を下に立てて印刷。フランジ下の45°コーンで無サポート。
// =====================================================================

/* [内容積] */
in_d      = 60;      // 内径 (カメラ+Pi Zeroスタック用)
in_len    = 90;      // 内長

/* [壁] */
wall      = 4;       // 円筒壁厚
rear_t    = 8;       // 後端閉止板厚

/* [前面フランジ / 窓] */
flange_od = 94;      // フランジ外径 (= bezel と一致)
flange_t  = 8;       // フランジ厚
win_d     = 76;      // アクリル窓Ø (bezel のポケットと一致)
gro_mid   = 68;      // Oリング溝の中心径 (AS568-235相当は要選定)
gro_w     = 2.8;     // 溝幅
gro_dp    = 1.8;     // 溝深さ (Oリング線径2.62の~70%)
m3_bcd    = 84;      // ベゼル固定 M3 BCD
m3_pilot  = 2.5;     // M3セルフタップ下穴
m3_depth  = 7;

/* [後面ペネトレータ] */
pen_d     = 10.2;    // WetLink M10 通し穴 (要: 実物で確認)

/* [側面マウントボス] */
boss_d    = 10;
boss_h    = 6;       // 外周からの張り出し
boss_pilot= 3.4;     // M4セルフタップ下穴
boss_y    = 15;      // ボス位置: 円筒軸方向オフセット(下記 boss_z)
boss_z    = [30, 75];// ボス高さ2段 (後端基準)

$fn = 128;

// ---- 導出 -----------------------------------------------------------
out_d   = in_d + 2*wall;              // 68
body_h  = rear_t + in_len;            // 98 (内腔は rear_t から)
cone_h  = (flange_od - out_d) / 2;    // 45°コーン高さ = 11
total_h = body_h + flange_t;          // フランジ上面まで

// ---- チェック ---------------------------------------------------------
assert(gro_mid + gro_w < win_d - 2,  "Oリング溝が窓Øの外");
assert(gro_mid - gro_w > in_d + 2,   "Oリング溝が内腔に接近");
assert(m3_bcd/2 - 2.75 > win_d/2 + 0.3, "M3頭が窓と干渉");
assert(m3_bcd/2 + 2.75 < flange_od/2 - 1, "M3がフランジ縁と干渉");
assert(m3_depth < flange_t - 0.8, "M3下穴がフランジを貫通");
assert(pen_d < in_d - 10, "ペネトレータ穴が後端板に対して大きすぎ");
for (bz=boss_z) assert(bz > rear_t + boss_pilot && bz < body_h - cone_h - boss_d/2 - 1,
                       "ボスがコーン/後端に干渉");

// ---- 本体 -------------------------------------------------------------
difference() {
    union() {
        // 円筒本体
        cylinder(d=out_d, h=body_h);
        // フランジ + 45°コーン
        translate([0, 0, body_h - cone_h])
            cylinder(d1=out_d, d2=flange_od, h=cone_h);
        translate([0, 0, body_h]) cylinder(d=flange_od, h=flange_t);
        // 側面マウントボス ×4 (-X側 2段×Y±)
        // 円筒面はY=±boss_y で x=-sqrt(r²-y²) まで後退しているので
        // 壁の中まで届く長さにする(壁内面は貫かない)。
        for (bz=boss_z) for (sy=[-1,1])
            translate([-out_d/2 - boss_h, sy*boss_y, bz])
                rotate([0, 90, 0])
                    cylinder(d=boss_d,
                             h=boss_h + out_d/2
                               - sqrt(pow(in_d/2,2) - boss_y*boss_y) - 1);
    }
    // 内腔
    translate([0, 0, rear_t]) cylinder(d=in_d, h=in_len + flange_t + 1);
    // 後面ペネトレータ M10
    translate([0, 0, -0.5]) cylinder(d=pen_d, h=rear_t + 1);
    // 前面 Oリング溝 (面シール)
    translate([0, 0, total_h - gro_dp])
        difference() {
            cylinder(d=gro_mid + gro_w, h=gro_dp + 0.5);
            translate([0, 0, -0.5]) cylinder(d=gro_mid - gro_w, h=gro_dp + 1.5);
        }
    // ベゼル M3 下穴 ×6
    for (a=[0:60:300])
        rotate([0, 0, a]) translate([m3_bcd/2, 0, total_h - m3_depth])
            cylinder(d=m3_pilot, h=m3_depth + 0.5);
    // 側面ボス M4 下穴
    for (bz=boss_z) for (sy=[-1,1])
        translate([-out_d/2 - boss_h - 0.5, sy*boss_y, bz])
            rotate([0, 90, 0]) cylinder(d=boss_pilot, h=boss_h + 4);
}

echo(str("外径=", out_d, " 全高=", total_h, " コーン高=", cone_h));
