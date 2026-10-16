"""sync_child_interior.py - run from the repo root.

Regenerate the child interior item list (fasteners included) and write it into
assemblies/child_interior/placement.json and the interior group of
assemblies/child_vertical_assembly/placement.json (the two are a deliberate
double definition; this script is the single source that keeps them equal)."""
import json
from pathlib import Path

SCREW = "parts/common/interior/cots/screw"
SPACER = "parts/common/interior/cots/hex_spacer"
FOAM = "parts/common/interior/cots/foam_pad"
P = "parts/child/interior/printed/"

# orientation helpers (screw model: shank -Z, head +Z)
NEG_Y = [{"rotate": [-90, 0, 0]}]   # shank -> -Y
POS_Y = [{"rotate": [90, 0, 0]}]    # shank -> +Y
POS_Z = [{"rotate": [180, 0, 0]}]   # shank -> +Z


def item(label, part, ops, color, note, file=None, alpha=1.0, group="interior"):
    d = {"label": label, "part": part}
    if file:
        d["file"] = file
    d.update({"group": group, "color": color, "alpha": alpha, "note": note, "ops": ops})
    return d


def screw(label, variant, seat, direction, note, color="Silver"):
    return item(label, SCREW, [{"translate": seat}] + direction, color, note, file=variant)


items = []
A = items.append

# ---------------- structure (unchanged positions) ----------------
A(item("vtray_deck", P + "child_vtray_deck", [], "Orange",
       "縦置きトレイ本体 t200。両端が上下フランジ貫通口に入り、幅広部 (20..180) がフランジ内端面に突き当たる。下フランジ BCD94 固定ラグ付き (2026-08-28 batt_box から移設)",
       file="child_vtray_deck_t200", alpha=0.9))
# 2026-09-03: リブはデッキ先端から差し込み、内側ショルダー (z 9.5..11.5 / 188.5..190.5) に当てる。
# 先端側の抜け止めはデッキ板を貫く M2.5×6 なべ (頭 Ø4.5、板上面)。旧: 両側ショルダー = 嵌められなかった
A(item("vtray_rib_bot", P + "child_vtray_rib", [{"translate": [0, 0, 2.5]}], "DarkOrange",
       "下センタリングリブ (Ø87.5) z 2.5..8.5。デッキ先端から差し込み、内側ショルダー (z 9.5) に当てる。外周 0.8 面取り = 挿入ガード", alpha=0.9))
A(item("vtray_rib_top", P + "child_vtray_rib", [{"translate": [0, 0, 191.5]}], "DarkOrange",
       "上センタリングリブ z 191.5..197.5。内側ショルダー (z 190.5) に当てる", alpha=0.9))
A(screw("rib_stop_screw_bot", "screw_m2_5x6", [0, -6, 0], NEG_Y,
        "M2.5×6 なべ。デッキ先端 (z=0) の板を上面から貫く抜け止め。頭 Ø4.5 が板上面 (y −6..−4.3)、先端が下面に 2mm 出て、下リブ (z ≥ 2.5) を止める"))
A(screw("rib_stop_screw_top", "screw_m2_5x6", [0, -6, 200], NEG_Y,
        "M2.5×6 なべ。デッキ先端 (z=200) の抜け止め。上リブ (z ≤ 197.5) を止める"))
for sx, lab, note in ((1, "cable_rail_power", "+X 側: 電池 XT30 ペア (z 25..55) + 電池ピグテール + J_PRS1"), (-1, "cable_rail_signal", "-X 側: RX / テザー / 水温 / 漏水 / ライトのハーネス")):
    A(item(lab, P + "child_vtray_cable_rail", [{"translate": [36 * sx, -10, 20]}, {"rotate": [90, 0, 0]}], "Gainsboro",
           f"ケーブルレール。{note}。デッキ実肉部 Z=37/77 へ M3×10 ×4 でセルフタップ"))
# 2026-09-03: 電池 35x26x110 (リード -Z 出し)。箱は ∩ チャンネル + 着脱床板 (皿ねじ 1 本) で電池だけを取り出せる
A(item("vtray_batt_box", P + "child_vtray_batt_box", [{"translate": [0, 0, 20]}], "Chocolate",
       "LiPo ∩ ベイ (2026-09-03 作り直し: 35×26×110 用)。デッキ下面へ耳 M3×8 ×4。−Z 端壁 (z 14..20、両端にリード切欠き) は貫通口の中、+Z はリップ (z 132..133.5、床板フックのスロット付き)。床は別部品", alpha=0.9))
A(item("vtray_batt_floor", P + "child_vtray_batt_floor", [{"translate": [0, 0, 20]}], "Peru",
       "着脱床板 3t。下端Z22.5、側面X22.5/Z36のM3×8サービスねじ。-Zへ2 mmスライドしてから-Yへ抜く。下フランジ固定を外さず交換可能（チューブは外す）"))
A(item("lipo", "parts/child/interior/cots/lipo_35x26x110", [{"translate": [-17.5, -14, 131]}, {"rotate": [0, 90, -90]}], "Crimson",
       "LiPo 35×26×110 (ユーザー指定 2026-09-03、型番要確認)。リード側端面 (モデル +X) を −Z に向けて z 21..131。床板に載り、上 3 / 側 2 / 端 1 のフォームで拘束。リードスタブ ×2 は端壁の切欠きへ",
       file="lipo_35x26x110_leads"))
A(item("child_main", "parts/child/interior/pcb/child_main", [{"translate": [44, 1, 20]}, {"rotate": [0, -90, -90]}], "ForestGreen",
       "CHILD_MAIN v4.1 (104×88)。基板下面 y=1 (ボス 7)。4 穴は LCD スペーサ (M3 MF30/17) のオスで共締め = 固定ねじ兼用"))
A(item("child_pwr", "parts/child/interior/pcb/child_pwr", [{"translate": [35, 4, 126]}, {"rotate": [0, -90, -90]}], "SeaGreen",
       "CHILD_PWR v2.1 (62×70)。基板下面 y=4 (ボス 10)。M3×8 ×4"))
A(item("lcd_support_lower", P + "child_lcd_support", [{"translate": [0, 0, 22]}], "Gold",
       "LCD 支持アーチ 下 (z 22..27 = MAIN 穴 z=24.5)。スペーサ端面にボスを載せ M3×10 皿ねじを +Y 面から面一に沈める。"
       "2026-09-03: 下フランジ BCD94 90° (0,+47) の固定耳付きバリアント — 足は z 19.3 (フランジ内面 19 + 0.3)、M3×12 を上から入れてフランジのタップ穴へ 4mm",
       file="child_lcd_support_lower"))
A(item("lcd_support_upper", P + "child_lcd_support", [{"translate": [0, 0, 117]}], "Gold",
       "LCD 支持アーチ 上 (z 117..122 = MAIN 穴 z=119.5)。耳無しバリアント", file="child_lcd_support_upper"))
A(item("lcd_hinge_frame", P + "child_lcd_hinge_frame", [{"translate": [0, 27, 72]}, {"rotate": [-90, 0, 0]}], "DarkGoldenrod",
       "LCD ドア固定 C フレーム。ラグはアーチ内側面 (z 27..32 / 112..117) に載り M3×10 を軸方向に締める (2026-08-28 修正)"))
A(item("lcd_cradle", P + "child_lcd_cradle", [{"translate": [0, 43.5, 72]}, {"rotate": [90, 0, 0]}], "Khaki",
       "LCD ドア (ベゼル)。前面 y=43.5。左ヒンジ M3 全ねじロッド (両アーチ受け) + 右 M2.5×12 ラッチ。ナックル逃げ切欠きあり。ヒンジ葉は ±8..20.5 に短縮 (クランプ棒の逃げ)", file="child_lcd_cradle_bezel"))
A(item("lcd_module", "parts/child/interior/cots/nhd_c0216ciz", [{"translate": [0, 40.7, 72]}, {"rotate": [90, 0, 0]}], "DimGray",
       "NHD-C0216CiZ。前面 = ベゼル前板 2 + フォーム 0.8 の奥 (y=40.7)。2026-08-28 まで前板と同位置に置かれていた (2mm 貫通) のを修正"))
A(item("rx_improved_mini", "parts/child/interior/pcb/rx_improved_mini", [{"translate": [34, -16, 134]}, {"rotate": [-90, 0, 180]}], "MediumSeaGreen",
       "RX_improved_mini (68×46)。デッキ下面に M2 FF6 スペーサ ×4 で吊る (基板上面 y=-16、部品は -Y)"))

# ---------------- fasteners: LCD arches (spacers stand on C-MAIN top face y=2.6) ----------------
for z in (24.5, 119.5):
    A(item(f"lcd_spacer_l_z{z:g}", SPACER, [{"translate": [-22, 2.6, z]}, {"rotate": [-90, 0, 0]}], "Goldenrod",
           "M3 MF30。オスは MAIN 穴 Ø3.2 → デッキ MAIN ボス下穴へ (MAIN 固定兼用)。メス端面 y=32.6 にアーチのボスが載る", file="hex_spacer_m3_mf30"))
    A(item(f"lcd_spacer_r_z{z:g}", SPACER, [{"translate": [39.5, 2.6, z]}, {"rotate": [-90, 0, 0]}], "Goldenrod",
           "M3 MF17。同上、メス端面 y=19.6", file="hex_spacer_m3_mf17"))
    A(screw(f"lcd_arch_screw_l_z{z:g}", "screw_m3x10_flat", [-22, 35.35 + 2.75, z], NEG_Y,
            "JIS M3×10 皿。アーチ左ボス +Y 面 (y=38.1) に面一、スペーサに 4.5mm かかる"))
    A(screw(f"lcd_arch_screw_r_z{z:g}", "screw_m3x10_flat", [39.5, 22.35 + 2.75, z], NEG_Y,
            "JIS M3×10 皿。アーチ右ボス +Y 面 (y=25.1) に面一"))

# hinge frame lugs -> arch pilots (0, 39.6), axial
A(screw("hinge_frame_screw_lower", "screw_m3x10", [0, 39.6, 32], [],
        "M3×10 なべ。下ラグ (z 27..32) 上面から -Z へ、下アーチ下穴 Ø2.8 にセルフタップ"))
A(screw("hinge_frame_screw_upper", "screw_m3x10", [0, 39.6, 112], POS_Z,
        "M3×10 なべ。上ラグ (z 112..117) 下面から +Z へ"))

# door hinge pin + latch
A(screw("lcd_hinge_rod", "screw_m3x105_rod", [-18.5, 36.5, 124.5], [],
        "M3 全ねじ 105mm (切断)。上下アーチのヒンジボス (Ø3.4) → ドア葉 z 51.5..64 / 80..92.5 → 枠ナックル z 64.5..79.5 を貫き、両アーチの外側でナット止め。頭が無いのでドア板端と干渉しない"))
A(screw("lcd_hinge_nut_lower", "screw_nut_m3", [-18.5, 36.5, 22 - 2.4], [], "M3 ナイロックナット。下アーチ下面 (z=22) の下"))
A(screw("lcd_hinge_nut_upper", "screw_nut_m3", [-18.5, 36.5, 122], [], "M3 ナット。上アーチ上面 (z=122) の上 (PWR 基板 z=126 まで 1.6mm)"))
A(screw("lcd_latch_screw", "screw_m2_5x12_low", [16.5, 43.5 - 2.2, 72], NEG_Y,
        "M2.5×12 低頭。ベゼル前面の座ぐり (深さ 2.2) に沈み、枠のヒートセットインサートへ"))

# rear clamp bars + screws (in the bezel's frame: print z 8.0 = world y 35.5)
for sy in (1, -1):
    zc = 72 + sy * 23.4
    A(item(f"lcd_clamp_bar_{'p' if sy > 0 else 'n'}", P + "child_lcd_cradle",
           [{"translate": [0, 43.5, 72]}, {"rotate": [90, 0, 0]}, {"translate": [0, sy * 23.4, 8.8]}], "Khaki",
           "LCD 後クランプ棒 (2.5t)。ベゼルのボス座 (前面から 8.8) に載り、0.8 フォーム (圧縮 0.5) 越しに LCD 背面を押す。ヒンジピン下面 35.0 まで 0.3", file="child_lcd_cradle_bar"))
    for sx in (1, -1):
        A(screw(f"lcd_clamp_screw_{'p' if sy > 0 else 'n'}{'p' if sx > 0 else 'n'}", "screw_m2_5x6",
                [sx * 14.9, 34.7 - 2.5, zc], POS_Y, "M2.5×6。クランプ棒背面 (y=32.2) から +Y へ、ベゼルの盲下穴 Ø2.0 にセルフタップ"))
    A(item(f"lcd_rear_foam_{'p' if sy > 0 else 'n'}", FOAM, [{"translate": [0, 34.7, zc]}, {"rotate": [-90, 0, 0]}], "LightPink",
           "独立気泡フォーム 0.8t (26×5、圧縮 0.5 でモデル化)。クランプ棒と LCD 背面 (y=35.2) の間", file="foam_pad_lcd_rear", alpha=0.8))

# PWR board screws (head on board top y=5.6)
for sx in (1, -1):
    for z in (130, 184):
        A(screw(f"pwr_screw_{'p' if sx > 0 else 'n'}_z{z}", "screw_m3x8", [31 * sx, 5.6, z], NEG_Y,
                "M3×8。CHILD_PWR 取付穴 → デッキ PWR ボス (10) 下穴へセルフタップ"))

# LiPo bay ears (head on deck top y=-6, through deck 4 into ear 3)
for sx in (1, -1):
    for z in (32, 110):
        A(screw(f"batt_box_screw_{'p' if sx > 0 else 'n'}_z{z}", "screw_m3x8", [24 * sx, -6, z], NEG_Y,
                "M3×8。デッキ上面 → Ø3.4 → ベイ取付耳の下穴 Ø2.8 へセルフタップ (先端 y=-14、クレードルのポケット上面 -14.5 の手前)"))

# cable rail screws (head on deck top; 4 per rail)
for sx in (1, -1):
    for dx in (-5.7, 5.7):
        for z in (37, 77):
            x = 36 * sx + dx
            A(screw(f"rail_screw_x{x:g}_z{z}", "screw_m3x10", [x, -6, z], NEG_Y,
                    "M3×10。デッキ上面 → Ø3.4 → レール側壁 Ø2.8 へセルフタップ (6mm かかる)"))

# battery floor plate: one M3x8 countersunk from below (y=-43) into the end-wall column pilot (z=17)
A(screw("batt_floor_screw", "screw_m3x8_flat", [22.5, -43, 36], POS_Y,
        "M3×8 皿。サービスねじX22.5/Z36、+X側壁の下穴Ø2.5へ5 mm掛かる。チューブを外せばフランジ固定後も-Y側からアクセス可能"))

# RX: M2 FF6 spacers under the deck, M2 screws from both sides
for sx in (1, -1):
    for z in (136.5, 177.5):
        A(item(f"rx_spacer_{'p' if sx > 0 else 'n'}_z{z:g}", SPACER, [{"translate": [31.5 * sx, -10, z]}, {"rotate": [90, 0, 0]}], "Goldenrod",
               "M2 メスメス 6mm。デッキ下面 (y=-10) と RX 基板上面 (y=-16) の間", file="hex_spacer_m2_ff6"))
        A(screw(f"rx_screw_top_{'p' if sx > 0 else 'n'}_z{z:g}", "screw_m2x6", [31.5 * sx, -6, z], NEG_Y,
                "M2×6。デッキ上面 → Ø2.4 → スペーサ上端 (2mm かかる)"))
        A(screw(f"rx_screw_bot_{'p' if sx > 0 else 'n'}_z{z:g}", "screw_m2x5", [31.5 * sx, -17.6, z], POS_Y,
                "M2×5。RX 基板下面 (y=-17.6) → Ø2.2 → スペーサ下端 (3.4mm かかる)"))

# bottom flange anchors: MF10 spacer on flange face z=19, deck lug 29..34.5 directly on it, M3x10
for sx in (1, -1):
    s = "p" if sx > 0 else "n"
    sp = item(f"flange_spacer_{s}", SPACER, [{"translate": [47 * sx, 0, 19]}], "Goldenrod",
              "M3 MF10。下フランジ内面 (z=19) の BCD94 M3 穴へオスを 4〜5mm ねじ込む (6 を超えない)。オス部はフランジ金属の中 = 包絡検証対象外", file="hex_spacer_m3_mf10")
    sp["skip_envelope"] = True
    A(sp)
    A(screw(f"flange_screw_{s}", "screw_m3x10", [47 * sx, 0, 34.5], [], "M3×10 なべ (ワッシャ無し: Ø7 は MAIN 基板端に当たる)。ラグ 5.5 を貫きスペーサのメスに 4.5mm"))
# 90° anchor (2026-09-03): the lower LCD arch's ear stands on the flange face; no spacer
sy = screw("flange_screw_y", "screw_m3x12", [0, 47, 27], [],
           "M3×12 なべ/キャップ (頭Ø5.5)。下フランジ BCD94 の 90° 穴 (0, +47)。下 LCD アーチの固定耳 (z 19.3..27) を貫き、"
           "フランジ内面 (z=19) のタップ穴へ 4mm ねじ込む (制限 4〜5)。頭は z 27..29、ヒンジ枠ラグ (y≤42.5) まで 1.75。"
           "270° は電池箱床が塞ぐため未使用。先端 z 15..19 はフランジ金属の中 = 包絡検証対象外")
sy["skip_envelope"] = True
A(sy)

# LiPo foam pads (closed-cell foam, not printed). 2026-09-03: clipo_* variants for the 35x26x110 cell
A(item("lipo_foam_top", FOAM, [{"translate": [0, -14, 76]}, {"rotate": [-90, 0, 0]}], "LightPink",
       "独立気泡フォーム 3t (106×33)。LiPo 上面 (y=-14) とデッキ下面 (-10) の間 (残り 1mm = 公差代)", file="foam_pad_clipo_top", alpha=0.8))
A(item("lipo_foam_side_p", FOAM, [{"translate": [18, -27, 74]}, {"rotate": [0, 90, 0]}], "LightPink",
       "独立気泡フォーム2t 102×24、Z23..125。側面サービスねじボスの逃げ切欠き付き", file="foam_pad_clipo_side_service", alpha=0.8))
A(item("lipo_foam_side_n", FOAM, [{"translate": [-18, -27, 74]}, {"rotate": [0, -90, 0]}], "LightPink",
       "同 -X 側", file="foam_pad_clipo_side_short", alpha=0.8))
A(item("lipo_foam_end_bot", FOAM, [{"translate": [0, -27, 21]}, {"rotate": [180, 0, 0]}], "LightPink",
       "独立気泡フォーム 1t (20×24)。LiPo -Z 端 (リード側) と端壁の中央柱 (z=20) の間。リード出口 (|x|>10.5) は覆わない", file="foam_pad_clipo_end", alpha=0.8))
A(item("lipo_foam_end_top", FOAM, [{"translate": [0, -27, 131]}], "LightPink",
       "独立気泡フォーム 1t。LiPo +Z 端 (z=131) とリップ (z=132) の間", file="foam_pad_clipo_end", alpha=0.8))

# ---------------- harnesses (parts/common/cabling/child_harness, modelled in world coords) ----------------
HARN = "parts/common/cabling/child_harness"
for var, note in (
    ("xh9_pwr", "C-MAIN J_PWR1 ↔ C-PWR J_MAIN (XH9 ストレート 9 芯、Ø5.5)。MAIN 低背部の上 (x≈4, y≈15) を +Z へ"),
    ("xh6_rx", "C-MAIN J_RX1 ↔ RX J2 (XH6、Ø4.5)。−X スリット (z 96) → −X レール溝 → RX 下面"),
    ("xh7_lcd", "C-MAIN J_LCD1 → LCD 小基板 (XH7、Ø5)。小基板の位置未定なのでスタブ + サービスループ"),
    ("xh3_teth", "C-MAIN J_TETH1 → 下キャップ ペネトレータ (XH3、Ø3)。−X スリット → −X レール溝 → 下リブ開口"),
    ("xh4_temp", "C-MAIN J_TEMP1 → ペネトレータ (XH4、Ø3.5)。teth と同経路"),
    ("xh2_leak", "C-MAIN J_LEAK1 → ペネトレータ (XH2、Ø2.5)。teth と同経路"),
    ("xh4_prs", "C-MAIN J_PRS1 → ペネトレータ (XH4、Ø3.5)。+X スリット → +X レール溝 → 下リブ開口"),
    ("bat", "電池リード (切って XT30 メス) → XT30 嵌合ペア (+X レール溝 z 25..55) → ピグテール → +X スリット (z 157) → C-PWR J_BAT パッド直付け。充電リード (XH4) は −X 側で下リブに結束"),
    ("led", "C-PWR J_LED パッド直付けピグテール → −X スリット (z 157) → −X レール溝 → 下リブ開口 → ライト"),
):
    A(item(f"harness_{var}", HARN, [], "DarkSlateGray", note, file=f"child_harness_{var}", alpha=0.9))

# LCD retired 2026-09-26; lower support becomes a structural flange brace.
items = [it for it in items if not (
    it['label'].startswith(('lcd_', 'hinge_frame_'))
    or it['label'] in ('vtray_rib_bot','rib_stop_screw_bot')
    or it['label'] == 'harness_xh7_lcd')]
A = items.append
for z in (24.5,):
    for x, side, length in ((-22,'l',30),(39.5,'r',12)):
        A(item(f'brace_spacer_{side}', SPACER,
               [{'translate':[x,4.6,z]},{'rotate':[-90,0,0]}], 'Goldenrod',
               f'M3 MF{length}: C-MAIN and lower flange brace mounting',
               file=f'hex_spacer_m3_mf{length}'))
        y=4.6+length+5.5
        A(screw(f'brace_screw_{side}', 'screw_m3x12', [x,y,z], NEG_Y,
                'M3x12 pan screw: flat printed seat, spacer engagement 6.5 mm'))
for x in (-22,39.5):
    A(screw(f'main_upper_screw_x{x:g}', 'screw_m3x8', [x,2.6,119.5], NEG_Y,
            'M3x8: board 1.6 mm + deck boss engagement 6.4 mm'))
A(item('flange_brace', P+'child_flange_brace', [{'translate':[0,0,22]}],
       'Gold', 'Printed brace: closed 12 mm bearing seat, 10 mm rounded beams, 20 mm webs, pan screws'))
for it in items:
    if it['label']=='child_main':
        it['ops'][0]['translate'][1]=3
        it['note']='C-MAIN 104x88: lower two holes secured by brace MF30/12; upper two by M3x8'
    if it['label'].startswith('main_upper_screw_'):
        it['ops'][0]['translate'][1]=4.6
    if it['label']=='flange_screw_y':
        it['file']='screw_m3x18'
        it['ops']=[{'translate':[0,47,31]}]
        it['note']='M3x18: printed 12 mm bearing seat, flange engagement 6 mm'
    if it['label'] in ('flange_screw_p','flange_screw_n'):
        x=47 if it['label'].endswith('_p') else -47
        it['file']='screw_m3x18'
        it['ops']=[{'translate':[x,0,41]}]
        it['note']='M3x18: printed 12 mm bearing seat, MF10 engagement 6 mm'
    if it['label']=='vtray_deck':
        it['note']='Printed closed 20 mm seats, rounded roots spread over Z20..80, local flange bearing heels at Z19'

# M3-only printed interior. RX PCB's original holes are retained but unused.
items=[it for it in items if not it['label'].startswith(('rx_spacer_','rx_screw_'))]
A=items.append
for sx in (-1,1):
    for z,sz in ((140.5,-1),(174.5,1)):
        tag=f'{sx}_{z:g}'
        ops=[{'translate':[0,0,z]},{'scale':[sx,1,sz]}]
        for variant in ('base','cap'):
            A(item(f'rx_clamp_{variant}_{tag}',P+'child_rx_edge_clamp',ops,'Orange',
                   'M3 printed edge clamp; original PCB holes unused',file=f'child_rx_edge_clamp_{variant}'))
        A(screw(f'rx_clamp_mount_{tag}','screw_m3x8',[sx*37.5,-6,z+sz*6],NEG_Y,
                'M3x8: deck 4 mm, printed base engagement 4 mm'))
        A(screw(f'rx_clamp_cap_screw_{tag}','screw_m3x8',[sx*37.5,-20.6,z],POS_Y,
                'M3x8: cap 2.6 mm, base engagement 5.4 mm; 6 mm offset from mounting screw'))
for it in items:
    if it['label']=='rib_stop_screw_top':
        it['file']='screw_m3x6'
        it['note']='M3x6 top rib stop, M3 pilot and exposed 6.6 mm head/tool reserve'

# Five confirmed WetLink M10s in the measured cap holes (BCD56, mirrored by cap RX180).
import math
PEN='parts/child/exterior/cots/wetlink_m10_confirmed'
for n,angle in enumerate((90,18,-54,-126,162),1):
    x=28*math.cos(math.radians(angle)); y=28*math.sin(math.radians(angle))
    A(item(f'penetrator_{n}',PEN,[{'translate':[x,y,-13.8]}],
           'SlateGray','WetLink M10: thread20, cap10, nutAF16 height8; dry tip Z6.2',
           file='wetlink_m10_confirmed',group='penetrators'))

# ---------------- write ----------------
ci = Path("assemblies/child_interior/placement.json")
asm = json.loads(ci.read_text(encoding="utf-8"))
asm.setdefault("groups",{})["penetrators"]=True
asm["items"] = [it for it in asm["items"] if it["group"] not in ("interior","penetrators")] + items
asm["note"] = ("2026-09-27: WetLink M10×5を実配置。下円形リブと下デッキ尾部を廃止。電池用ねじをZ36側面へ移動し、床板の下端Z22.5と解除ストロークを確保。旧記述は履歴。\n"
               "子機 (水中ユニット) 内装のみのサブアセンブリ。親機の parent_interior_p1 と同じ位置づけ。\n"
               "容器: WTE4 4in × 200mm アクリルチューブ + 上下フランジ BR-101040 (透明表示・取合い確認用)。下エンドキャップ (5×M10) と上ドーム (仮モデル) も透明表示 (2026-09-03 追加)。外装シェル / カメラは表示しない。\n"
               "2026-08-28: 浮いていた部品を全部固定 — スペーサ・ねじ・ワッシャ・シム・フォームパッドを実体化し、貫通していた 4 箇所 (LCD/ベゼル前板、電池箱アンカー/デッキ、ヒンジ枠ラグ/アーチ、ナックル/ドア板) を部品形状で修正。\n"
               "2026-09-03: 電池を 35×26×110 (リード −Z 出し) に変更。電池箱を ∩ チャンネル + 着脱床板 (皿ねじ 1 本) に作り直し、電池だけを取り出せるようにした。電源リードは切って XT30 メスを付け、基板側は J_BAT パッド直付けのピグテール (XT30 ペアは +X レール z 25..55)。基板間 XH ハーネスをモデル化 (parts/common/cabling/child_harness)。\n"
               "2026-09-03: 下フランジ固定を 3 点化 — 0°/180° (デッキラグ + MF10) に加え、90° (0,+47) を下 LCD アーチ (child_lcd_support_lower) の耳で直接フランジ内面へ M3×12。270° は電池箱床が塞ぐため未使用。上フランジ 4 穴は内側からねじが回せないので使わない。穴の根拠: parts/child/exterior/cots/wte4_flange/_work/images/ref/BR-101040_hole_map.png + WTE データシート Rev C.5。\n"
               "interior グループは assemblies/child_vertical_assembly/placement.json と同一 (生成元: 本 placement を正とし、scad/lib/sync_child_interior.py で複製)。\n"
               "配置根拠: docs/子機内装_収まり検討.md / docs/子機内装_サービス設計.md。検証: scad/lib/verify_child_interior.py, scad/lib/check_asm_contacts.py。")
ci.write_bytes(json.dumps(asm, ensure_ascii=False, indent=2).encode("utf-8"))

cv = Path("assemblies/child_vertical_assembly/placement.json")
asm2 = json.loads(cv.read_text(encoding="utf-8"))
asm2.setdefault("groups",{})["penetrators"]=True
asm2["items"] = [it for it in asm2["items"] if it["group"] not in ("interior","penetrators")] + items
cv.write_bytes(json.dumps(asm2, ensure_ascii=False, indent=2).encode("utf-8"))
print(len(items), "interior items ->", ci, "and", cv)

# Fusion manifest uses the same current placements, including retired LCD removal.
from verify_child_interior import matrix
import numpy as np
fusion_items = []
for it in asm['items']:
    stem = it.get('file') or Path(it['part']).name
    geometry = Path(it['part']) / (stem + '.step')
    if not geometry.exists():
        geometry = geometry.with_suffix('.stl')
    assert geometry.exists(), geometry
    m = matrix(it.get('ops'))
    fusion_items.append({
        **{k: it[k] for k in ('label','part','group','color','alpha','note') if k in it},
        'geometry': geometry.as_posix(), 'geometry_abs': str(geometry.resolve()),
        'matrix_mm': m.flatten().tolist(), 'translation_mm': m[:3,3].tolist(),
        'mirrored': bool(np.linalg.det(m[:3,:3]) < 0),
    })
fusion = {'assembly': asm['name'], 'coordinate_system': asm['coordinate_system'],
          'note': asm['note'], 'units': 'mm', 'source': ci.as_posix(), 'items': fusion_items}
Path('assemblies/child_interior/child_interior_fusion.json').write_text(
    json.dumps(fusion, ensure_ascii=False, indent=2), encoding='utf-8')

