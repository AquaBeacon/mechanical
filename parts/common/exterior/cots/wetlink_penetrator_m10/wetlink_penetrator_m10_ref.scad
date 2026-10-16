// =====================================================================
// wetlink_penetrator_m10_ref.scad — Blue Robotics WetLink Penetrator M10
//                                    **参考モデル (購入品の代用)**
//
// ベンダの 3D データは未入手。メーカー公開値 (製品ページ / 組立ガイド) から
// 起こした「場所を取るぶんだけ正しい」空間占有モデル。
//   確定値 (ベンダ公称):  M10x1.5 / ねじ長 20 / 六角 AF16 / 外側総高 18-26 /
//                        取付穴 10.0-10.2 / O リング AS568-013 (OD 15.98)
//   仮値   (**要確認**):  頭の高さ head_h、プラグ AF、ナット、導体ボア径
// 実物入手後は実測して直すこと。ベンダ STEP が出たら差し替える。
//
// ファイル名を意図的にフォルダ名と変えてある → build.ps1 の一括ビルド対象外。
// 個別ビルド:  .\build.ps1 parts\common\exterior\cots\wetlink_penetrator_m10\wetlink_penetrator_m10_ref.scad
//
// 座標系: 軸 = Z。**z=0 = 壁の外面 (= O リング座面)**、+Z が容器の内側。
//   z < 0        : 濡れ側 (六角頭 + プラグ)。ケーブルはここから入る
//   0 .. wall_t  : 壁の中 (バカ穴 Ø10.2)
//   wall_t ..    : 乾き側 (残ったねじ + ナット)。ここから出るのは**素の導体**
//
// !! 向きを間違えないこと: O リング座面 (頭側) は必ず**外**。
//    ガイド曰く "only the cable side of the penetrator is sealed.
//    The back side - where the wires exit - is not sealed and must stay dry."
//    → 容器内でケーブル外被は終わる。TD04A の 3P プラグは通らないので
//      ケーブルを切って容器内で端子台に落とす前提 (td04a_transducer.md 参照)。
// =====================================================================

/* [ベンダ公称値 (確定)] */
thread_d  = 10;      // M10 x 1.5 呼び径
thread_l  = 20;      // ねじ長 (製品ページ "20 mm")
hex_af    = 16;      // バルクヘッド六角 二面幅 (組立ガイド "Hex Size (Bulkhead) M10 = 16 mm")
plug_af   = 14;      // プラグ六角 二面幅 (同 "11-14 mm" の上限)
out_h     = 22;      // 壁外面から出る総高 (製品ページ "18-26 mm from Endcap" の中央)
hole_d    = 10.2;    // 相手側のバカ穴 (10.0-10.2)
oring_od  = 15.98;   // AS568-013 (ID 12.42 + 線径 1.78 x2)

/* [仮値 — **要確認** (実測 or ベンダ図面待ち)] */
head_h    = 8;       // 六角頭の高さ (**要確認**)。プラグ高 = out_h - head_h
nut_af    = 17;      // 付属ナット 二面幅 (ISO 4032 M10 = 17) (**要確認**)
nut_h     = 8.4;     // 同 厚さ (ISO 4032 M10 = 8.4) (**要確認**)
bore_d    = 5.7;     // 導体ボア (**ケーブル未選定**: 7.5mm シールの 5.7 を仮置き)
cable_d   = 7.5;     // プラグに入るケーブル外被 Ø (**未選定**: 4.5-8.5 のどれか)

/* [取付先の壁] — ナットの位置だけがこの値で決まる */
// **アセンブリでは「相手モデルの壁厚」に合わせること** (実壁厚ではない)。
//   タカチ BCAS212310G は実壁 3.08 だが、bcas212310g.scad の内腔は図面の
//   「有効内寸 217.8」基準なので**モデル上の壁は 6.1**。モデル整合を優先し、
//   variants.txt の bcas = 6.1 を親機アセンブリで使う。
//   → 実機ではナットが 3mm 外側 (箱内 y≈3.1..11.5) に来る。
//     内側クリアランスもねじ掛かりもモデルより広い = モデルは保守側。
//   子機 wte4_end_cap_5xm10 は t10 の M10 タップ穴なのでナット無し (別途モデル化)。
wall_t    = 3.1;

$fn = 48;

// ---- 導出値 ---------------------------------------------------------
plug_h  = out_h - head_h;          // 14
in_len  = thread_l - wall_t;       // 壁の内側に出るねじの長さ = 16.9
nut_z1  = wall_t + nut_h;          // ナット上端 (容器内へ 11.5)
hex_od  = hex_af / cos(30);        // 18.475 (製品ページの "Outer diameter 18 mm")

// ---- 整合チェック ---------------------------------------------------
assert(thread_l > wall_t + nut_h + 2,
       str("壁が厚すぎてナットが掛からない: ねじ長 ", thread_l, " / 壁 ", wall_t));
assert(out_h >= 18 && out_h <= 26, "外側総高がベンダ公称の 18-26 mm を外れている");
assert(head_h > 0 && plug_h > 0, "head_h が out_h を超えている");
assert(oring_od <= hex_af, "O リング (OD 15.98) が六角の二面幅に収まらない = 座面が足りない");
assert(hole_d > thread_d && hole_d - thread_d < 0.5, "取付穴がねじに対して不適切");
assert(cable_d < bore_d + 2.5 && bore_d < thread_d - 2.6, "ボア/ケーブル径がバルクヘッド肉厚を食う");
assert(nut_af > hex_af - 2, "ナットが頭より極端に小さい (モデルの取り違え)");

echo(str("wetlink_penetrator_m10_ref: 外 z=", -out_h, "..0 (Ø", hex_od,
         ") / 壁 0..", wall_t, " / 内 ねじ ", in_len, " ナット上端 z=", nut_z1,
         " (Ø", nut_af/cos(30), ")  取付穴 Ø", hole_d));

module hexp(af, h) cylinder(d = af / cos(30), h = h, $fn = 6);

difference() {
    union() {
        cylinder(d = thread_d, h = thread_l);              // ねじ部 (山は省略)
        translate([0, 0, -head_h])      hexp(hex_af,  head_h);   // 六角頭 (濡れ側)
        translate([0, 0, -out_h])       hexp(plug_af, plug_h);   // プラグ (濡れ側)
        translate([0, 0, wall_t])       hexp(nut_af,  nut_h);    // ナット (乾き側)
    }
    // 導体ボア (貫通)
    translate([0, 0, -out_h - 1]) cylinder(d = bore_d, h = out_h + thread_l + 2);
    // ケーブル外被が入るプラグ側のボア
    translate([0, 0, -out_h - 1]) cylinder(d = cable_d, h = plug_h + 1);
}
