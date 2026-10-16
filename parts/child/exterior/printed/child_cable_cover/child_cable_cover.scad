// =====================================================================
// child_cable_cover.scad — 子機 下部ケーブルカバー (新規、2026-09-04)
//
// 役割: child_guard_ring 後部開放セクタ (方位角 230..310 = -Y ±40°) を覆い、
// アルミキャップ露出面・ペネトレータ・ケーブルを後方/側方からの衝撃から守る。
// テザー張力はカバー内面のクランプ座 (EVA t2 挟み込み) で受ける。
// トルクレンチのアクセスは**カバーを外して**確保する (中央 r<55 素通しは維持)。
//
// 構成 (Customizer 変数 part、variants.txt で出し分け):
//   part="cover": 円弧殻本体 + 出口穴 ×3 + 取付フランジ ×2 (guard_ring インサートへ)
//                 + クランプ座 下半分 (半割トラフ + M5 ナットトラップ ×2)
//   part="clamp": クランプ押え板 (半割トラフの相手側。M5 ×2 クリアランス穴)
//
// 座標系: 機体グローバル。チューブ軸 = Z、+Y = 前。child_guard_ring と共有する
// 変数はすべて「二重定義」節に集約し、guard_ring 側の値と揃える。
//
// 印刷向き・荷重ケース・造形性は .md 参照。
// =====================================================================

part = "cover";   // "cover" | "clamp"

/* [取合い (child_guard_ring と共有 — 二重定義。値を変えたら両方直す)] */
ring_z0    = -60;      // guard_ring スキッド下端
ring_h     = 6;        // guard_ring スキッド厚
ring_z1    = ring_z0 + ring_h;   // -54 (カバー下端 = スキッド上面)
top_z      = -17.2;    // カバー上端 (コアフレーム下端 -17 に遊び0.2、guard_ring と同じ)
wall_r0    = 58.35;    // シェル内径 (guard_ring 後部ウォールと同径)
wall_r1    = 64.35;    // シェル外径
open_sec   = [230, 310]; // 対象セクタ (guard_ring の後方開放セクタと同じ)
tab_r0     = 70;       // guard_ring 取付タブ内面 (干渉検査用、二重定義)

/* [取付フランジ (guard_ring の cover_bolt_* と共有 — 二重定義、値は必ず揃える)] */
cover_bolt_az        = [230, 310];  // guard_ring インサートの方位角
cover_bolt_dir       = [1, -1];     // guard_ring と同じ符号 (ボア方向)
cover_bolt_r         = 64;          // インサート中心半径
cover_bolt_z         = -26;         // インサート中心 z (2026-09-04: -35→-26。
                                     // 出口穴 z=-40 と z 方向に分離。詳細は guard_ring 側コメント参照)
cover_bolt_pad_deg   = 11;          // guard_ring ボス角度幅 (フランジもこれに合わせる)
cover_bolt_r1        = 68;          // guard_ring ボス外径
m5_clear_d           = 5.4;         // M5 バカ穴
m5_cb_d              = 9;           // 座ぐり径
m5_cb_h              = 5;           // 座ぐり深さ

/* [出口穴 ×3 (Ø14、側面。真後ろ 270±10° は開口しない)]
   フランジは全高厚肉化 (guard_ring と同じ理由) なので、出口穴がフランジの角度域を
   通っても cover_bolt_z (z=-26) と exit_z (z=-40) が z 方向に分離していれば
   物理的な干渉はない (穴は単にフランジぶん長く貫通するだけ)。そのためフランジは
   出口穴の角度域を制約しない。制約するのはクランプ座 (同じ z 帯) だけ。 */
exit_az     = [238, 253, 292];  // テザー / TD04A / ライト
exit_d      = 14;
exit_z      = -40;
exit_r_mean = (wall_r0 + wall_r1) / 2;

/* [クランプ座 (2ピース、EVA t2 挟み込み、M5 ナットトラップ ×2)]
   内側 (トラフ) は狭く (半径方向 58.35..70.35、接線 ±10)、外側 (ボルト) は
   広く (70.35..84、接線 ±17) の 2 段構成。出口穴が届く半径 (<=cover_bolt_r1=68) と
   重なるのは内側の狭い区画だけなので、出口穴の方位角除外ゾーンは内側区画の
   footprint だけで決まる (260..280 相当)。
   ナットトラップのピッチは 24 ではなく **18** に変更 (2026-09-04)。理由:
   Ø14 チャンネルからナット外接円まで ≥2mm を確保しつつ、狭い後方セクタ
   (80° 全体からフランジ×2とホール×3を引くと残りは限られる) に収めるため。
   ピッチ 24 が必須の相手部品はない (このカバー内で完結する自己参照)。 */
clamp_az        = 270;
channel_d       = 14;     // クランプ内径。EVA t2 の圧縮代を Ø14 に含めて簡略化
channel_len     = 12;     // トラフ区画の半径方向長さ (58.35..70.35)
inner_half_w    = 10;     // トラフ区画の接線方向半幅 (channel_r=7 に 3mm 肉厚)
bolt_gap        = 0;      // トラフ区画とボルト区画のすきま (0 = 隙間なく接続。
                           // 隙間を空けると clamp 側が浮遊ソリッドになり STEP 変換が壊れる)
bolt_len        = 14;     // ボルト区画の半径方向長さ
outer_half_w    = 17;     // ボルト区画の接線方向半幅
channel_z       = -34;    // チャンネル中心 z
seat_depth      = 14;     // 座 (下半分) の高さ (z 方向、チャンネル中心から下)
plate_t         = 10;     // 押え板 (上半分) の厚さ (チャンネル中心から上)
nut_af          = 8;      // M5 ナット 二面幅
nut_h           = 4.5;    // ナットポケット深さ
clamp_bolt_y    = 9;      // ナットトラップ ×2 のオフセット (ピッチ 18)

/* [Hidden] */
fudge = 0.01;
$fn = 96;

// ---- 導出値 -----------------------------------------------------------
channel_r    = channel_d / 2;
channel_x0   = wall_r0;
channel_x1   = wall_r0 + channel_len;         // 70.35
bolt_x0      = channel_x1 + bolt_gap;         // 76.35
bolt_x1      = bolt_x0 + bolt_len;            // 90.35 (envelope 内かは assert で検査)
clamp_bolt_x = bolt_x0 + bolt_len/2;
nut_r        = nut_af / 2 / cos(30);          // 六角ナット外接円半径 (af=8 → 4.62)
exit_bore_len = (cover_bolt_r1 - wall_r0) + 2*fudge; // フランジ域も貫通できる長さで統一
// 出口穴の方位角除外ゾーン = トラフ区画 (内側、狭い) の footprint (innermost = channel_x0)
clamp_excl_half_deg = atan(inner_half_w / channel_x0);
clamp_az0   = clamp_az - clamp_excl_half_deg;
clamp_az1   = clamp_az + clamp_excl_half_deg;
exit_half_deg = (exit_d/2) / exit_r_mean * 180 / 3.14159265;

// ---- 干渉・成立性チェック ----------------------------------------------
assert(part == "cover" || part == "clamp", "part は cover か clamp");
assert(wall_r1 <= tab_r0 - 2, "シェル外径がタブに 2mm 未満で近接");

// 出口穴: シェル内に収まり (端から 1mm 以上)、真後ろクランプゾーンを避ける
for (a = exit_az) {
    assert(a - exit_half_deg >= open_sec[0] + 1 && a + exit_half_deg <= open_sec[1] - 1,
           "出口穴がシェル端からはみ出す");
    assert(a <= clamp_az0 - exit_half_deg || a >= clamp_az1 + exit_half_deg,
           "出口穴が真後ろクランプゾーンに掛かる");
}
// 出口穴どうしの周方向すきま (穴縁 + 2mm)
for (i = [0 : len(exit_az) - 2])
    for (j = [i + 1 : len(exit_az) - 1])
        assert(abs(exit_az[i] - exit_az[j]) * 3.14159265/180 * exit_r_mean
               >= exit_d + 1,
               "出口穴どうしのすきま < 1mm");
// 出口穴とフランジのボア (z=cover_bolt_z) が z 方向に分離していること
assert(abs(exit_z - cover_bolt_z) >= (exit_d/2 + m5_cb_d/2 + 2),
       "出口穴とフランジボアの z 方向すきま不足");

// クランプ トラフ区画がセクタ内 (フランジに掛からない)
assert(clamp_az0 >= open_sec[0] + 1 && clamp_az1 <= open_sec[1] - 1,
       "クランプ座 (トラフ) がシェル端からはみ出す");
// クランプ ボルト区画が包絡内 (env_half=125 相当、余裕をみて 100)
assert(bolt_x1 <= 100, "クランプボルト区画が半径方向に張り出しすぎ (envelope > 100)");
// チャンネルとトラフ区画側面の肉厚
assert(inner_half_w - channel_r >= 3, "トラフ区画の側面肉厚 < 3");
// ナットトラップとボルト区画側面/チャンネルとのすきま
assert(clamp_bolt_y + nut_r <= outer_half_w - 2, "ナットトラップがボルト区画側面に近すぎる");
assert(clamp_bolt_x - nut_r >= channel_x1, "ナットトラップがトラフ区画に掛かる");
// チャンネル z がカバー高さ内に収まる (上下とも 3mm 以上の肉厚)
assert(channel_z - seat_depth >= ring_z1 + 3, "クランプ座下端がカバー下端に近すぎる");
assert(channel_z + plate_t <= top_z - 3, "クランプ押え板上端がカバー上端に近すぎる");
assert(nut_h + 2 <= seat_depth, "ナットポケット深さが座の高さを超える");

// クランプチャンネル (cover 側トラフ + clamp 側トラフ) が実際に合わさって
// Ø14 の通り道になること (2026-09-05: cover/clamp が円弧殻本体と重なっていた
// 不具合の修正に伴い追加)。
assert(channel_r <= seat_depth, "トラフの円が座の下端よりはみ出す (cover 側)");
assert(channel_r <= plate_t, "トラフの円が押え板の上端よりはみ出す (clamp 側)");
assert(channel_len > 0, "トラフの半径方向長さが0以下");

// 取付フランジ: 座ぐりのボルト頭が ring_z0 未満に出ないこと
assert(cover_bolt_z - m5_cb_h/2 >= ring_z0 + 3,
       "座ぐりが ring_z0 未満 (機体最下端) に出る");
echo(str("child_cable_cover: シェル r", wall_r0, "..", wall_r1,
         " az", open_sec, " z", ring_z1, "..", top_z));
echo(str("出口穴 az=", exit_az, " d=", exit_d, " z=", exit_z));
echo(str("フランジ (guard_ring インサートへ) az=", cover_bolt_az, " r=", cover_bolt_r,
         " z=", cover_bolt_z));
echo(str("クランプ座 az=", clamp_az, " channel d=", channel_d,
         " x=", channel_x0, "..", channel_x1, " ボルト x=", bolt_x0, "..", bolt_x1,
         " y=±", clamp_bolt_y, " z=", channel_z));

// ---- モジュール ---------------------------------------------------------
module wedge(az0, az1, z0, h) {
    intersection() {
        rotate([0, 0, az0]) translate([0, 0, z0]) cube([200, 200, h]);
        rotate([0, 0, az1 - 90]) translate([0, 0, z0 - fudge])
            cube([200, 200, h + 2*fudge]);
    }
}
module ring_sector(r0, r1, az0, az1, z0, h) {
    intersection() {
        difference() {
            translate([0, 0, z0]) cylinder(r = r1, h = h);
            translate([0, 0, z0 - fudge]) cylinder(r = r0, h = h + 2*fudge);
        }
        wedge(az0, az1, z0 - fudge, h + 2*fudge);
    }
}

// ---- part = "cover" ------------------------------------------------------
module cover_body() {
    difference() {
        union() {
            // 円弧殻本体
            ring_sector(wall_r0, wall_r1, open_sec[0], open_sec[1], ring_z1, top_z - ring_z1);
            // 取付フランジ ×2 (guard_ring ボスに突き合わせ、全高で厚肉化。
            // 全高にするのは printability: 局所的な帯だけ厚肉化すると下面が宙に浮くため)
            for (i = [0, 1]) {
                az0 = cover_bolt_az[i];
                az1 = cover_bolt_dir[i] > 0 ? az0 + cover_bolt_pad_deg : az0 - cover_bolt_pad_deg;
                ring_sector(wall_r0, cover_bolt_r1, min(az0, az1), max(az0, az1),
                            ring_z1, top_z - ring_z1);
            }
            // クランプ座 下半分: トラフ区画 (狭) + ボルト区画 (広) の 2 段構成
            rotate([0, 0, clamp_az]) {
                translate([channel_x0, -inner_half_w, channel_z - seat_depth])
                    cube([channel_len, 2*inner_half_w, seat_depth + fudge]);
                translate([bolt_x0, -outer_half_w, channel_z - seat_depth])
                    cube([bolt_len, 2*outer_half_w, seat_depth + fudge]);
            }
        }

        // 出口穴 ×3 (半径方向貫通。フランジ域も貫通できる長さで統一)
        for (a = exit_az)
            rotate([0, 0, a]) translate([wall_r0 - fudge, 0, exit_z])
                rotate([0, 90, 0])
                    cylinder(d = exit_d, h = exit_bore_len, $fn = 48);

        // 取付フランジ M5 バカ穴 + 座ぐり (接線方向、guard_ring インサートへ届く)
        // 注意: フランジ本体は cover_bolt_dir[i] の符号方向へ伸びる (このカバー自身の
        // 材内)。ボア方向はその「伸びる向き」と同じでなければならないが、
        // rotate([90*k,0,0]) は k=+1 で -Y、k=-1 で +Y に掘るため、実際に渡す係数は
        // 符号を反転した -cover_bolt_dir[i] になる (guard_ring 側は逆に材が az の
        // 反対側にあるため cover_bolt_dir をそのまま使う。二重定義だが向きが逆)。
        for (i = [0, 1]) {
            az0 = cover_bolt_az[i];
            dir = -cover_bolt_dir[i];
            len = cover_bolt_pad_deg * 3.14159265/180 * cover_bolt_r + 2*fudge;
            // バカ穴 (フランジを貫通)
            rotate([0, 0, az0]) translate([cover_bolt_r, 0, cover_bolt_z])
                rotate([90 * dir, 0, 0])
                    cylinder(d = m5_clear_d, h = len, $fn = 32);
            // 座ぐり (アクセス側の端、guard_ring から遠い側)
            rotate([0, 0, az0]) translate([cover_bolt_r, dir * (len - m5_cb_h), cover_bolt_z])
                rotate([90 * dir, 0, 0])
                    cylinder(d = m5_cb_d, h = m5_cb_h + fudge, $fn = 32);
        }

        // クランプ座トラフ (半割、上半分は開放)。cylinder は rotate([0,90,0]) 後
        // translate 点から +X 方向へ伸びる (中心ではなく始点)。channel_x0 を始点にする。
        rotate([0, 0, clamp_az])
            translate([channel_x0 - fudge, 0, channel_z])
                rotate([0, 90, 0])
                    cylinder(d = channel_d, h = channel_len + 2*fudge, $fn = 48);

        // ナットトラップ ×2 (六角、座の上面から下向きにブラインド) + M5 通し穴
        for (s = [-1, 1])
            rotate([0, 0, clamp_az])
                translate([clamp_bolt_x, s * clamp_bolt_y, channel_z - fudge])
                    rotate([0, 0, 90]) cylinder(d = nut_af/cos(30), h = nut_h + fudge, $fn = 6);
        for (s = [-1, 1])
            rotate([0, 0, clamp_az])
                translate([clamp_bolt_x, s * clamp_bolt_y, channel_z - seat_depth - fudge])
                    cylinder(d = m5_clear_d, h = seat_depth - nut_h + 2*fudge, $fn = 32);

        // クランプ押え板 (clamp) の占有域からシェル本体 (ring_sector, 全高で存在) を
        // 避ける。押え板は channel_z..channel_z+plate_t に座るが、円弧殻本体は
        // 方位角 230..310 の全高 (ring_z1..top_z) に渡って存在するため、そのままでは
        // 押え板とシェル本体が r 58.35..64.35 で丸ごと重なる (2026-09-05 発覚:
        // check_asm_contacts で 3.4mm 貫通)。押え板の外形 (内側+外側区画の和) と
        // 同じ範囲をここで削り、押え板が収まる空洞を作る。
        rotate([0, 0, clamp_az]) {
            relief = 0.3; // fudge (0.01) だけだと稜線のメッシュ精度で貫通誤検出が
                          // 出た (2026-09-05, check_asm_contacts で 0.52mm)。実クリアランスを持たせる。
            translate([channel_x0 - relief, -outer_half_w - relief, channel_z - relief])
                cube([(bolt_x1 - channel_x0) + 2*relief, 2*(outer_half_w + relief),
                      plate_t + 2*relief]);
        }
    }
}

// ---- part = "clamp" -------------------------------------------------------
module clamp_plate() {
    difference() {
        union() {
            rotate([0, 0, clamp_az])
                translate([channel_x0, -inner_half_w, channel_z])
                    cube([channel_len, 2*inner_half_w, plate_t + fudge]);
            rotate([0, 0, clamp_az])
                translate([bolt_x0, -outer_half_w, channel_z])
                    cube([bolt_len, 2*outer_half_w, plate_t + fudge]);
        }

        // クランプ座トラフ (半割、下半分が開放 = cover 側と合わさって全周になる)。
        // cover 側と同じ始点補正 (channel_x0 起点、+X へ伸びる)。
        rotate([0, 0, clamp_az])
            translate([channel_x0 - fudge, 0, channel_z])
                rotate([0, 90, 0])
                    cylinder(d = channel_d, h = channel_len + 2*fudge, $fn = 48);

        // M5 クリアランス穴 ×2 (板厚方向、頭は上面)
        for (s = [-1, 1])
            rotate([0, 0, clamp_az])
                translate([clamp_bolt_x, s * clamp_bolt_y, channel_z - fudge])
                    cylinder(d = m5_clear_d, h = plate_t + 2*fudge, $fn = 32);
    }
}

// ---- 出力 -----------------------------------------------------------------
if (part == "cover") cover_body();
else clamp_plate();
