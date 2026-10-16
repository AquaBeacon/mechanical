// =====================================================================
// parent_float_yoke.scad — 親機 浮子ヨーク (紐通し式フロートの端受け、1 浮子に 2 個)
//
// 役割 (2026-09-05 人間決定: 浮子は円筒ではなく挟めない → 中心の空洞に紐を通して固定):
//   parent_deck の側壁 HP40 座 (Y ±70, z −25) にアダプタ板でボルト留めし、その板をそのまま
//   浮子の端まで縦板 (フィン、t14 × h56) として伸ばし、端の「柱」で受ける
//   (2026-09-05: 水平の腕 t10 は FEA でたわみ 1.9〜3.9 mm と柔らかすぎたためフィンに変更)。柱の内面に 45° の円錐座 (浮子の先細り端が自動調心で座る)、
//   軸上に紐穴 Ø10。紐は「前ヨーク → 浮子の空洞 → 後ヨーク」と通して張り、浮子は
//   端面だけで受ける (胴には触れない)。柱の外面下部に紐の端を留める Ø8 ×2。
//   浮子の浮力は円錐座 → 柱 → 腕 (曲げ) → アダプタ → デッキ HP40 の経路で伝わる。
//
// 4 個の内訳: hand=+1 (腕が +Y) = 右舷後 / 左舷前 (180° 回転)、hand=−1 (Y ミラー) = 右舷前 / 左舷後。
//   variants.txt: a = hand 1 / b = hand -1。
//
// 座標系 (ローカル): 原点 = デッキ側壁 HP40 座の中心 (座面上)。X = 外向き (側壁法線)、
//   Y = 浮子の端の方向 (hand で反転)、Z = 上。デッキ上面はローカル z = +25。
// 印刷向き: **フィンの内面 (X=0 面) をベッドに、+X を上** (= 横倒し)。フィンは寝た板、柱は
//   ベッドから立つ壁。円錐座は 45° で自己支持。サポート不要。PETG / 壁 4 / インフィル 25 %。
// 規約: cube / cylinder + ブーリアンのみ。
// =====================================================================

/* [向き] */
hand = 1;             // +1 = 腕が +Y、-1 = Y ミラー

/* [浮子 (parent_fender.scad と二重定義 — 実測後に両方直す)] */
fender_d   = 100;
fender_len = 300;
taper_len  = 40;
end_d      = 40;
bore_d     = 15;
end_slack  = 2;       // 浮子が中央にあるとき、端面リムと円錐座の当たりまでの片側余裕 (紐で片側に引き寄せて詰める)

/* [デッキ側 (parent_deck.scad と二重定義)] */
hp_y       = 70;      // デッキ側壁 HP40 座の中心 Y (±)
hp_z       = -25;     // 同 z (デッキ上面基準) → ローカルのデッキ上面 = -hp_z
deck_lip_z0 = -50;    // デッキ側壁下端 (デッキ上面基準)
deck_rope_y = 108;    // デッキ側壁の紐穴 (±)、z -35 → ローカル (38, -10)
deck_rope_z = -35;
deck_rope_d = 8;

/* [HP40 アダプタ (hardpoint.scad と二重定義)] */
hp_pitch   = 40;
hp_pad     = 50;
hp_bolt_d  = 5.4;
ad_pad     = 56;      // アダプタ板の一辺 (HP 座 50 より大きく: ざぐりの縁を残す。デッキ板の縁の外側なので上に 3 出てよい)
ad_t       = 18;      // アダプタ板 = フィンの厚さ (X)。頭のざぐりを持つ。t14 は紐張力 100 N でフィンが Z 軸回りに曲がりたわみ 1.4 (FEA) → 18
cb_d       = 9.5;     // M5 キャップ頭ざぐり Ø (頭 8.5)
cb_depth   = 8;       // ざぐり深さ (外面から)

/* [フィン (アダプタ板を柱まで延ばした縦板)] */
fin_gap    = 2;       // フィン外面 (X = ad_t) と浮子の隙間 (フィン高さ範囲での最小)

/* [浮子の高さと喫水 (2026-09-05 人間要望: 浮子を箱と同じ高さに。箱は防水なので浸かってよい、転倒しないことが優先)] */
z_f_global = 0;       // 浮子軸 z (デッキ上面 = 箱底 基準)。spec/parent_hydrostatics.py で縦揺れ GM が最大になる高さ
waterline_z = -2.7;   // 喫水線 (同スクリプトの出力を転記。質量 3.14 kg・箱/デッキ/ヨークの排水量込み)
pen_z      = 65;      // 南壁ペネトレータの軸 (bcas212310g.scad pen_z)
pen_margin = 30;      // ペネトレータ軸が喫水線より上に残す最小高さ
lid_z      = 80;      // 箱の蓋の合わせ目 (本体上端)

/* [柱 (浮子端の受け)] */
post_t     = 32;      // Y 厚 (円錐座 20 + 背 12)。柱は X 0..post_x1、z post_z0..+ad_pad/2 (フィン上端と面一)。t26 は紐張力 100 N でたわみ 1.4 (FEA) → 32
seat_od    = 70;      // 円錐座の口径 (柱内面)
seat_depth = 20;      // 円錐座の深さ (45° → 底径 = seat_od - 2*seat_depth)
rope_d     = 10;      // 紐穴 (軸上)
tie_d      = 8;       // 紐端の留め穴 ×2
tie_dx     = 35;      // 同 軸からの X オフセット (±)。円錐座との間の肉 7 (30 だと 3.4 で FEA のメッシュ検査に掛かる)
tie_dz     = -30;     // 同 軸からの Z オフセット
post_margin = 8;      // 円錐座の外側に残す肉 (紐留め穴の端距離を確保)

$fn = 96;

// ---- 導出 -----------------------------------------------------------
x_f      = ad_t + fin_gap + fender_d/2;                // 66: 浮子軸 X (浮子はフィンの高さ帯にあるので最大半径で逃がす)
z_f      = z_f_global - hp_z;                          // +25 (ローカル)。浮子は z −50..+50 (箱の下半分と重なる)
cyl_len  = fender_len - 2*taper_len;
vol_l    = (PI*pow(fender_d/2,2)*cyl_len + 2*PI*taper_len/3*(pow(fender_d/2,2) + fender_d/2*end_d/2 + pow(end_d/2,2))
            - PI*pow(bore_d/2,2)*fender_len) / 1e6;    // 浮子 1 本の全没排水量 (spec/parent_hydrostatics.py の V_FLOAT と二重定義)
fin_top  = z_f + seat_od/2 + post_margin;               // フィンと柱の上端 (ローカル +68 = グローバル +43)。蓋の張出し (z 80) より下
seat_engage = (seat_od - end_d)/2;                     // 15: 端面リム (Ø end_d) が円錐座に入る深さ
y_p0     = fender_len/2 - seat_engage + end_slack - hp_y;   // 67: 柱内面 Y (リムが座の深さ 15 で当たる位置 + 余裕 2)
y_p1     = y_p0 + post_t;                              // 109
post_x1  = x_f + seat_od/2 + post_margin;              // 84
post_z0  = z_f - seat_od/2 - post_margin;              // -98
seat_id  = seat_od - 2*seat_depth;                     // 30
lip_z0_l = deck_lip_z0 - hp_z;                         // -25: 側壁下端 (ローカル)
// フィン (X 0..ad_t、z ±ad_pad/2) の高さ範囲での浮子の最大半幅 → フィン外面 (X=ad_t) との隙間
zz       = max(-ad_pad/2, z_f);
w_at_lip = sqrt(max(0, pow(fender_d/2, 2) - pow(zz - z_f, 2)));
lip_clear = x_f - w_at_lip - ad_t;
// デッキ側壁の紐穴 (ローカル) — フィンに同位置の通し穴を開ける
drope_y  = deck_rope_y - hp_y;                          // 38
drope_z  = deck_rope_z - hp_z;                          // -10

// ---- 成立性チェック --------------------------------------------------
assert(lip_clear >= fin_gap - 0.01, str("浮子がフィンに近すぎる: 隙間 ", lip_clear, " (2026-09-05 に板厚を見ていなくて貫通 7.6 を出した)"));
assert(pen_z - waterline_z >= pen_margin, str("ペネトレータが喫水線に近い: ", pen_z - waterline_z, " < ", pen_margin));
assert(lid_z - waterline_z >= pen_margin, "蓋の合わせ目が喫水線に近い");
assert(fin_top + hp_z < lid_z - 2, "フィン上端が蓋の張出し (z 80) に掛かる (フィンは箱の胴体の脇 X 108.. にある)");
assert(z_f_global + fender_d/2 <= lid_z, "浮子上端が蓋の張出しより上 (浮子は X 128.. なので当たらないが、意図は箱の下半分と同じ高さ)");
assert(y_p0 >= hp_pad/2 + 10, "柱がアダプタに近すぎる (腕が短い)");
assert(seat_id > bore_d + 4 && seat_id < end_d, "円錐座の底径: 空洞より大きく、端面径より小さいこと (端面のリムで座る)");
assert(seat_engage > 0 && seat_engage < seat_depth, "浮子端が円錐座に入る深さが座の深さを超える");
assert(end_slack >= 0 && end_slack < seat_engage, "余裕は 0 以上、座の深さ未満");
// 浮子の先細り (半角) が円錐座 (45°) より緩いこと → 端面リムだけで当たり、先細り面は座に触れない
assert((fender_d - end_d)/2 <= taper_len, "浮子の先細りが 45° より急: 先細り面が円錐座に先に当たる (seat_od/seat_depth を見直す)");
assert(post_t - seat_depth >= 5, "円錐座の背が薄い");
assert(ad_t - cb_depth >= 5, "ざぐり下の板が薄い");
assert(cb_d/2 + 2 < hp_pitch/2 && hp_pitch/2 + cb_d/2 + 1.5 <= ad_pad/2, "ざぐりがアダプタ板からはみ出す/互いに近い");
assert(ad_pad/2 - hp_pad/2 <= 3, "アダプタ板が座より 3 以上大きい (デッキ板の上に出すぎ)");
// フィンの紐通し穴がざぐり・フィン縁から離れる
for (sy = [-1, 1]) for (sz = [-1, 1])
    assert(sqrt(pow(drope_y - sy*hp_pitch/2, 2) + pow(drope_z - sz*hp_pitch/2, 2)) >= cb_d/2 + deck_rope_d/2 + 2,
           "フィンの紐通し穴がざぐりに近い");
assert(abs(drope_z) + deck_rope_d/2 + 3 <= ad_pad/2 && drope_y + deck_rope_d/2 + 3 <= y_p0, "フィンの紐通し穴がフィンの縁/柱に近い");
// 紐留め穴が円錐座・柱の縁から離れる
for (s = [-1, 1]) {
    d_seat = sqrt(pow(s*tie_dx, 2) + pow(tie_dz, 2));
    assert(d_seat >= seat_od/2 + tie_d/2 + 2, "紐留め穴が円錐座に掛かる");
    assert(x_f + s*tie_dx - tie_d/2 >= 3 && x_f + s*tie_dx + tie_d/2 <= post_x1 - 3, "紐留め穴が柱の X 範囲外");
    assert(z_f + tie_dz - tie_d/2 >= post_z0 + 3, "紐留め穴が柱下端に近い");
}
// 250³ 造形枠 (印刷は X を上に: 高さ = post_x1)
assert(post_x1 <= 250 && (y_p1 + ad_pad/2) <= 250 && (fin_top - post_z0) <= 250, "X1C 250 枠を超える");

echo(str("parent_float_yoke: fender displacement ", 2*vol_l, " L (x2), waterline global z=", waterline_z,
         " (spec/parent_hydrostatics.py), penetrator above water ", pen_z - waterline_z, " mm, fin/post top global z=", fin_top + hp_z));
echo(str("parent_float_yoke: hand=", hand, " fender axis local (x,z)=(", x_f, ",", z_f, ") global X=", 108 + x_f,
         " z=", hp_z + z_f, "  post Y ", y_p0, "..", y_p1, " (global ", hp_y + y_p0, "..", hp_y + y_p1, ") rim contact at global Y ", hp_y + y_p0 + seat_engage - end_slack,
         "  lip clearance=", lip_clear, "  seat engage=", seat_engage));
echo(str("parent_float_yoke: HOLETABLE hp40_adapter(face x=0)=", [for (sy=[-1,1], sz=[-1,1]) [0, sy*hp_pitch/2, sz*hp_pitch/2]],
         " rope(dia ", rope_d, ")=", [[x_f, y_p0, z_f]], " tie(dia ", tie_d, ")=", [for (s=[-1,1]) [x_f + s*tie_dx, y_p0, z_f + tie_dz]]));
echo(str("parent_float_yoke: bbox ", post_x1, " x ", y_p1 + ad_pad/2, " x ", fin_top - min(post_z0, -ad_pad/2)));

module yoke() {
    difference() {
        union() {
            // フィン = アダプタ板 (HP40) を柱まで延ばした縦板。柱の上端まで高くする (深い梁)
            translate([0, -ad_pad/2, -ad_pad/2]) cube([ad_t, y_p1 + ad_pad/2, fin_top + ad_pad/2]);
            // 柱
            translate([0, y_p0, post_z0]) cube([post_x1, post_t, fin_top - post_z0]);
        }
        // M5 通し穴 + 外面ざぐり ×4
        for (sy = [-1, 1]) for (sz = [-1, 1]) {
            translate([-1, sy*hp_pitch/2, sz*hp_pitch/2]) rotate([0, 90, 0]) cylinder(d = hp_bolt_d, h = ad_t + 2);
            translate([ad_t - cb_depth, sy*hp_pitch/2, sz*hp_pitch/2]) rotate([0, 90, 0]) cylinder(d = cb_d, h = cb_depth + post_x1);
        }
        // フィンの紐通し穴 (デッキ側壁 Ø8 と同軸、X 貫通)
        translate([-1, drope_y, drope_z]) rotate([0, 90, 0]) cylinder(d = deck_rope_d, h = ad_t + 2);
        // 円錐座 (柱内面から 45°)
        translate([x_f, y_p0 - 0.01, z_f]) rotate([-90, 0, 0])
            cylinder(d1 = seat_od, d2 = seat_id, h = seat_depth + 0.01);
        // 紐穴 (軸上、柱を貫通)
        translate([x_f, y_p0 - 1, z_f]) rotate([-90, 0, 0]) cylinder(d = rope_d, h = post_t + 2);
        // 紐留め穴 ×2
        for (s = [-1, 1])
            translate([x_f + s*tie_dx, y_p0 - 1, z_f + tie_dz]) rotate([-90, 0, 0]) cylinder(d = tie_d, h = post_t + 2);
    }
}

if (hand < 0) mirror([0, 1, 0]) yoke(); else yoke();   // mirror([0,0,0]) は零ベクトルで非マニフォールドになる
