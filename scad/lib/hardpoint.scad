// =====================================================================
// hardpoint.scad — AquaBeacon 取付規格 HP40 (2026-09-04, docs/子機外装_改善要件.md §3.1)
//
//   M5 熱圧入インサート ×4 を 40×40 の正方に置く共通パターン。
//   フレーム側 = hp40_pad() + hp40_cut()  /  アクセサリ側 = hp40_adapter()
//
//   ローカル座標: 座面 = z=0 の XY 平面、法線 = +Z (インサート穴は −Z へ掘る)。
//   使う側で translate/rotate して機体座標へ置く。
//   `use <../../../../../scad/lib/hardpoint.scad>` (parts/<unit>/<ext>/printed/<name>/ から)
//
//   規約: cube/cylinder のみ (STEP を汚さない)。hull/offset は使わない。
// =====================================================================

HP_PITCH    = 40;    // 穴ピッチ (±20)
HP_INSERT_D = 6.4;   // M5 熱圧入インサート下穴 Ø
HP_INSERT_H = 8;     // 下穴深さ (インサート長 8 用、底に 1mm 余裕 → 9 掘る)
HP_PAD      = 50;    // 座面の推奨一辺
HP_RECESS   = 2;     // 包絡からの引っ込み量 (何も付けないとき突出しない)
HP_CABLE_D  = 14;    // 中央ケーブル穴 Ø
HP_BOLT_D   = 5.4;   // アダプタ側 M5 バカ穴
HP_ADAPTER_T = 6;    // アダプタ板の標準厚

function hp40_xy() = [[-HP_PITCH/2, -HP_PITCH/2], [ HP_PITCH/2, -HP_PITCH/2],
                      [-HP_PITCH/2,  HP_PITCH/2], [ HP_PITCH/2,  HP_PITCH/2]];

// フレーム側の座 (足す方): 座面 z=0、厚さ t を −Z 側に持つ角ブロック。
// pad_x/pad_y は座の一辺 (既定 50)。座面の Y 方向を示す矢印 (刻印) 付き。
module hp40_pad(t=10, pad_x=HP_PAD, pad_y=HP_PAD, arrow=false) {
    difference() {
        translate([-pad_x/2, -pad_y/2, -t]) cube([pad_x, pad_y, t]);
        if (arrow) hp40_arrow();
    }
}

// フレーム側の穴 (引く方): インサート下穴 ×4 (+1mm 底余裕) と中央ケーブル穴。
// cable=false で中央穴なし。through_t を与えると中央穴をその厚さぶん貫通させる。
module hp40_cut(cable=true, through_t=HP_INSERT_H + 4, insert_h=HP_INSERT_H) {
    for (p = hp40_xy())
        translate([p[0], p[1], -(insert_h + 1)])
            cylinder(d=HP_INSERT_D, h=insert_h + 1 + 0.01, $fn=32);
    if (cable)
        translate([0, 0, -through_t - 0.01])
            cylinder(d=HP_CABLE_D, h=through_t + 0.02, $fn=48);
}

// 座面の +Y を示す矢印 (deboss 0.6)。座面 z=0 から −0.6 まで削る。
// cube のみで作る (linear_extrude(polygon) は csg_to_step.py が STEP 化できず
// ファセット STEP にフォールバックした実例あり 2026-09-04)。
// 既定は arrow=false。向きの管理はアクセサリ側の .md で行う。
module hp40_arrow(depth=0.6) {
    translate([0, 0, -depth]) {
        translate([-1.5, 6, 0]) cube([3, 8, depth + 0.01]);              // 軸
        translate([0, 16, 0]) rotate([0, 0, 45])  translate([-1.5, -7, 0]) cube([3, 7, depth + 0.01]);  // 矢尻 右
        translate([0, 16, 0]) rotate([0, 0, -45]) translate([-1.5, -7, 0]) cube([3, 7, depth + 0.01]);  // 矢尻 左
    }
}

// アクセサリ側のアダプタ板: 座面に密着する面が z=0、板は +Z 側に厚さ t。
// M5 バカ穴 Ø5.4 ×4 と中央ケーブル穴。アクセサリ本体は z=t の上に union する。
module hp40_adapter(t=HP_ADAPTER_T, pad_x=HP_PAD, pad_y=HP_PAD, cable=true) {
    difference() {
        translate([-pad_x/2, -pad_y/2, 0]) cube([pad_x, pad_y, t]);
        for (p = hp40_xy())
            translate([p[0], p[1], -0.01]) cylinder(d=HP_BOLT_D, h=t + 0.02, $fn=32);
        if (cable)
            translate([0, 0, -0.01]) cylinder(d=HP_CABLE_D, h=t + 0.02, $fn=48);
    }
}

// 干渉検査用: 座の外形 (pad_x × pad_y × 深さ insert_h+1) を返す関数
function hp40_envelope(pad_x=HP_PAD, pad_y=HP_PAD) = [pad_x, pad_y, HP_INSERT_H + 1];
