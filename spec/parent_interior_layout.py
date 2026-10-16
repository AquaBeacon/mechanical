# -*- coding: utf-8 -*-
"""parent_interior_layout.py — 親機防水ボックス内装の配置検討 (2パターン)

容器: タカチ BCAS212310G (外形210x230x100.3 / 有効内寸197.8x193.2x87.1)
      プレートは BMP2123Z 互換 183x203 がボス上 (z~10) に載る。
      ボスピッチ 160x180、四隅 M4 インサート。 ※ボス高さ10は仮値 (現物実測で確定)

実寸ソース:
  - 基板外形/穴: hardware/pcb/{PARENT_MAIN,PARENT_PWR,TX_improved}/*.kicad_pcb
  - P-MAIN 実装位置: PARENT_MAIN_pos.csv (ボタン/SD/DS3231/XH の平面座標)
  - LiPo: parts/common/interior/cots/lipo_3s_2200_zeee (102x34x23, ~170g)
  - SPRESENSE: 拡張ボード CXD5602PWBEXT1 68.6x53.5 (Sony 公称) + メイン + Multi-IMU
  - 容器: タカチ寸法図 BCAS212310G.pdf / BMP2123Z カタログ

共通の骨格 (両パターン同一):
  - P-MAIN (2,2)  ボタン/LED/DS3231 縁を北向き、microSD 縁を南向き
  - P-PWR  (2,95) トグル SW 上向き
  - LiPo は P-MAIN 上のブリッジトレイ parent_lipo_tray (MAIN の取付穴 103x75.5 に
    M3 MF25 スペーサ ×4 を立てて架ける)。**最上段 = 蓋を開ければベルクロを外して
    真上に抜ける** (2026-08-28 人間指示: 交換しやすさ優先。床置き案は取り下げ)
  - SPRESENSE モジュール (55x70 に 90°回転) 右下 — microSD へ上からアクセス可
  - LCD (NHD-C0216CiZ) は北縁ストリップに傾斜ブラケット (未設計・ゾーン予約)

パターン1: 親機カメラ = DJI Osmo Action 6 (外付け) → TX はプレート直付け
パターン2: 親機カメラ = Pi Zero 2W + GS Camera 内蔵
  - 底面 Ø30 ビューポート: 箱中心から +X 53mm (マストフランジ 70 角 +2mm を回避
    しつつ浮子開口 Ø140 内に収まる唯一の帯域 52..55)
  - Pi Zero はプレート直付け、TX を 30mm スタンドオフで Pi Zero の上に高架

貫通部: 南壁 (Y=0) に WetLink M10 x2 (z=65, 箱 x=85/120)。check_penetrators() が
  内側ナットの突出と内装の当たりを見る。bcas212310g.scad と三重定義。

実行: python spec/parent_interior_layout.py → spec/_work/images/parent_layout_p1.png / _p2.png
重なり・はみ出し・高さ超過があると AssertionError で落ちる。
"""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

# ---------------------------------------------------------------- 容器・プレート
# iw/id はプレート搭載高さ (z~10, ボス上) での有効内寸。底面 (床) は 173.2x193.2 に
# 絞られる (内部ボスせり出し)。BMP2123Z (183x203) が公式対応 = この搭載面で成立。
BOX = dict(name="BCAS212310G", iw=197.8, id=217.8, ih=87.1)
PLATE_W, PLATE_D = 183.0, 203.0   # BMP2123Z 互換
BOSS_H = 10.0                     # 仮値: 現物実測で確定 (parent_plate.scad boss_h / bcas212310g.scad boss_h と連動)
PLATE_Z = BOSS_H                  # プレート下面 (箱内床基準)
PLATE_T = 5.0                     # parent_plate.scad pt
STANDOFF = 6.0                    # 基板スタンドオフ
PCB_T = 1.6
LIPO_SPACER = 25.0                # parent_lipo_tray: MAIN 穴に立てる M3 MF スペーサ (hex_spacer m3_mf25)
TRAY_FLOOR_T = 3.0                # parent_lipo_tray floor_t
MAIN_TOP_COMP = 18.49             # parent_main.md 最高部品 (トレイ下面との隙間検査)
TX_RAISE = 31.0                   # P2: TX 高架 = ボス 6 + M3 MF スペーサ 25 (hex_spacer m3_mf25)
CLEAR = 3.0
EDGE = 2.0

MAST_FLANGE_SQ = 70.0             # parent_mast_clamp フランジ (箱底外側中央)
MAST_BOLT = 28.0                  # M5x4 (±28,±28)
FLOAT_OPEN_R = 70.0               # parent_float_segment ID140/2
VIEWPORT_D = 30.0                 # P2 底面ビューポート (M12 系レンズ前提)
VP_OFF = 54.0                     # 箱中心からのオフセット (成立域 52..55。54 = cam_mount 脚と TX ボスの離隔)

# ------------------------------------------- 南壁 WetLink M10 ペネトレータ (2026-08-29)
# bcas212310g.scad の pen_x / pen_z / pen_in / pen_seat と **三重定義**。片方だけ直さないこと。
# 座標変換: 本スクリプトはプレート原点・箱内床基準。
#   プレート座標 = 箱座標 - PLATE_ORG_BOX / z = 箱z - BOX_FLOOR_T
PEN_X_BOX = [85.0, 120.0]   # bcas212310g.scad pen_x  (85=TD04A / 120=テザー)
PEN_Z_BOX = 65.0            # bcas212310g.scad pen_z  (軸高さ, 箱底外面基準)
PEN_NUT_D = 19.7            # bcas212310g.scad pen_in   内側ナット外接
PEN_SEAT_D = 18.5           # bcas212310g.scad pen_seat 六角頭外接
PEN_TIP_Y_BOX = 14.5        # 箱内へ出る先端 y (モデル壁 6.1 + ナット厚 8.4)
BOX_FLOOR_T = 3.84          # bcas212310g.scad floor_t
BOX_OH, BOX_COVER_H = 100.3, 20.0   # 外形高さ / うちカバー
PLATE_ORG_BOX = (13.5, 13.5)        # placement.json の plate translate
PEN_LABEL = {85.0: "TD04A", 120.0: "tether"}

# --------------------------------------------- 部品 (幅w, 奥行d, 高h, 表示名)
PARTS = {
    "MAIN":   dict(w=112.0, d=88.0,  h=24.84, label="P-MAIN 112x88\n(btn/LED N, SD S)"),
    "PWR":    dict(w=100.0, d=84.0,  h=33.27, label="P-PWR 100x84\n(toggle h23.5)"),
    "TX":     dict(w=74.0,  d=50.0,  h=21.13, label="TX_improved\n74x50 (rot90)"),
    "SPR":    dict(w=68.6,  d=53.5,  h=30.0,  label="SPRESENSE ext\n68.6x53.5 (rot90)\nh30*"),
    "LIPO":   dict(w=102.0, d=34.0,  h=23.0,  label="LiPo tray z46"),
    "PIZERO": dict(w=65.0,  d=30.0,  h=13.0,  label="Pi Zero 2W\n(under TX)"),
    "CAM":    dict(w=42.0,  d=42.0,  h=45.0,  label="GS cam\nlens down"),
    "LCD":    dict(w=85.0,  d=18.0,  h=30.0,  label="LCD bracket (tilted)"),
}

# 配置 {部品: (x, y, rot)}。rot=1 で w/d 入替。CAM は箱中心 +X VP_OFF に自動。
LAYOUT_P1 = {
    "MAIN":  (2.0, 2.0, 0),
    "PWR":   (2.0, 95.0, 0),
    "SPR":   (121.0, 2.0, 1),     # 53.5x68.6
    "TX":    (121.0, 77.0, 1),    # 50x74 プレート直付け
    "LCD":   (30.0, 183.0, 0),
}
LAYOUT_P2 = {
    "MAIN":  (2.0, 2.0, 0),
    "PWR":   (2.0, 95.0, 0),
    "SPR":   (121.0, 2.0, 1),
    "CAM":   (None, None, 0),
    "TX":    (117.0, 127.0, 1),   # Pi Zero の上に z+30 高架 (NE 皿ねじ回避で x117)
    "PIZERO": (127.0, 135.0, 1),  # TX 直下 (30x65 縦)
    "LCD":   (30.0, 183.0, 0),
}
# LiPo (両パターン共通): P-MAIN 上のブリッジトレイ (parent_lipo_tray)。
# トレイ原点 = MAIN 南西穴 (6.5,10)。ベイ外形 111x45 @ (-4,5)、セルは壁 2.5 + 余裕 (2,3) 内側
LIPO_TRAY = (7.0, 20.5, 102.0, 34.0)   # セル本体 (プレート座標)。リードは -X (西) 端
LIPO_TRAY_OUTER = (2.5, 15.0, 111.0, 45.0)

# P2 で高さ方向に共存するペア (平面重なりを許す)
P2_STACKED = {("TX", "PIZERO")}


def rects(layout):
    out = {}
    cx, cy = PLATE_W / 2.0, PLATE_D / 2.0
    for n, (x, y, rot) in layout.items():
        p = PARTS[n]
        w, d = (p["d"], p["w"]) if rot else (p["w"], p["d"])
        if n == "CAM":
            x, y = cx + VP_OFF - w / 2.0, cy - d / 2.0
        out[n] = (x, y, w, d)
    return out


def check(items, stacked=frozenset(), soft_pairs=frozenset()):
    for n, (x, y, w, d) in items.items():
        assert x >= EDGE - 0.01 and y >= EDGE - 0.01, f"{n} 縁マージン不足"
        assert x + w <= PLATE_W - EDGE + 0.01 and y + d <= PLATE_D - EDGE + 0.01, \
            f"{n} がプレート外 ({x:.1f},{y:.1f})+({w}x{d})"
    names = list(items)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            if (a, b) in stacked or (b, a) in stacked:
                continue
            ax, ay, aw, ad = items[a]
            bx, by, bw, bd = items[b]
            gap = max(max(ax - (bx + bw), bx - (ax + aw)),
                      max(ay - (by + bd), by - (ay + ad)))
            need = 2.0 if (a, b) in soft_pairs or (b, a) in soft_pairs else CLEAR - 0.5
            assert gap >= need, f"{a}-{b} クリアランス不足 gap={gap:.1f} (要 {need})"


def check_viewport():
    r = VIEWPORT_D / 2.0
    assert VP_OFF >= MAST_FLANGE_SQ / 2.0 + r + 2.0, "VP がマストフランジと干渉"
    assert VP_OFF + r <= FLOAT_OPEN_R, "VP が浮子開口 Ø140 の外"
    db = ((VP_OFF - MAST_BOLT) ** 2 + MAST_BOLT ** 2) ** 0.5
    assert db >= r + 5.0 + 2.0, "VP が M5 ボルト頭と干渉"


def check_penetrators(items, tray_top):
    """南壁ペネトレータ (WetLink M10) の内側突出が内装と当たらないこと。

    平面で逃げているか、高さで逃げているか、どちらかを満たせば OK。
    ナットの外接円 (Ø19.7) を軸まわりの占有として扱う。"""
    pz = PEN_Z_BOX - BOX_FLOOR_T                       # 床基準の軸高さ
    r = PEN_NUT_D / 2.0
    py_max = PEN_TIP_Y_BOX - PLATE_ORG_BOX[1]          # プレート座標での先端 y
    boxes = dict(items)
    boxes["LIPO_TRAY"] = LIPO_TRAY_OUTER
    for xb in PEN_X_BOX:
        px = xb - PLATE_ORG_BOX[0]
        tag = PEN_LABEL.get(xb, str(xb))
        # 高さ: 床リブ台より上 / 内腔の天井より下 / 外側は本体上端 (カバー線) より下
        assert pz - r >= 3.0 + CLEAR, f"pen {tag} が床に近すぎる"
        assert pz + r <= BOX["ih"] - 2.0, f"pen {tag} のナットが蓋内面に近すぎる"
        assert PEN_Z_BOX + PEN_SEAT_D / 2.0 <= BOX_OH - BOX_COVER_H - 3.0,             f"pen {tag} の六角頭が本体上端 (カバー) に近すぎる"
        for n, (x, y, w, d) in boxes.items():
            if x + w < px - r - CLEAR or x > px + r + CLEAR:
                continue                                # X で逃げている
            if y > py_max + CLEAR:
                continue                                # 南壁側に無い
            if n == "LIPO_TRAY":
                bot, top = tray_top - PARTS["LIPO"]["h"] - TRAY_FLOOR_T, tray_top
            else:
                bot = PLATE_Z + PLATE_T + (TX_RAISE if (n == "TX" and "PIZERO" in items) else STANDOFF)
                top = bot + PARTS[n]["h"]
            assert bot - (pz + r) >= CLEAR or (pz - r) - top >= CLEAR,                 f"pen {tag} が {n} と当たる (pen z {pz - r:.1f}..{pz + r:.1f} / {n} {bot:.1f}..{top:.1f})"
    for i in range(len(PEN_X_BOX) - 1):
        assert PEN_X_BOX[i + 1] - PEN_X_BOX[i] >= 30.0, "ペネトレータのピッチ < 30 = トルクレンチが振れない"


def check_stack_p2(items):
    tx, pz = items["TX"], items["PIZERO"]
    assert tx[0] <= pz[0] and pz[0] + pz[2] <= tx[0] + tx[2] + 10 and \
           tx[1] <= pz[1] and pz[1] + pz[3] <= tx[1] + tx[3], "PiZero が TX 高架の外"
    pz_top = PLATE_Z + PLATE_T + STANDOFF + PARTS["PIZERO"]["h"]
    tx_bot = PLATE_Z + PLATE_T + TX_RAISE - 5.74          # TX 裏面リード
    assert tx_bot - pz_top >= 3.0, f"TX 高架と PiZero の隙間不足 {tx_bot - pz_top:.1f}"


def draw(fname, title, items, viewport=False, heights=()):
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(13.5, 7), width_ratios=[1.5, 1])
    colors = {"MAIN": "#7fb3d5", "PWR": "#a9dfbf", "TX": "#f9e79f", "LIPO": "#f1948a",
              "PIZERO": "#bb8fce", "CAM": "#85c1e9", "SPR": "#f5cba7", "LCD": "#d5dbdb"}
    ox, oy = (BOX["iw"] - PLATE_W) / 2.0, (BOX["id"] - PLATE_D) / 2.0
    ax.add_patch(Rectangle((-ox, -oy), BOX["iw"], BOX["id"], fill=False, ec="k", lw=2))
    ax.add_patch(Rectangle((0, 0), PLATE_W, PLATE_D, fill=False, ec="green", lw=1.2, ls="--"))
    cx, cy = PLATE_W / 2.0, PLATE_D / 2.0
    ax.add_patch(Rectangle((cx - 35, cy - 35), 70, 70, fill=False, ec="red", ls=":"))
    ax.add_patch(Circle((cx, cy), FLOAT_OPEN_R, fill=False, ec="red", ls=":", lw=0.8))
    for s in (-1, 1):
        for t in (-1, 1):
            ax.add_patch(Circle((cx + s * MAST_BOLT, cy + t * MAST_BOLT), 5, fill=False, ec="red", lw=0.8))
    order = [n for n in items if n != "TX"] + (["TX"] if "TX" in items else [])
    for n in order:
        x, y, w, d = items[n]
        alpha = 0.55 if n == "TX" and "PIZERO" in items else 0.85
        hatch = "//" if n == "TX" and "PIZERO" in items else None
        ax.add_patch(Rectangle((x, y), w, d, fc=colors[n], ec="k", alpha=alpha, hatch=hatch))
        lbl = PARTS[n]["label"] + ("\n(raised z30)" if n == "TX" and "PIZERO" in items else "")
        ax.text(x + w / 2, y + d / 2, lbl, ha="center", va="center", fontsize=7.5)
    ox_, oy_, ow_, od_ = LIPO_TRAY_OUTER
    ax.add_patch(Rectangle((ox_, oy_), ow_, od_, fill=False, ec="brown", ls="--", lw=1.2))
    tx_, ty_, tw_, td_ = LIPO_TRAY
    ax.add_patch(Rectangle((tx_, ty_), tw_, td_, fc=colors["LIPO"], ec="brown", alpha=0.7, hatch=".."))
    ax.text(tx_ + tw_ / 2, ty_ + td_ / 2, "LiPo 102x34 on bridge tray\n(M3 MF25 spacers on MAIN holes)", ha="center", va="center", fontsize=7.5)
    if viewport:
        ax.add_patch(Circle((cx + VP_OFF, cy), VIEWPORT_D / 2, fill=False, ec="blue", lw=2))
        ax.text(cx + VP_OFF, cy - 26, "viewport Ø30 (bottom)", ha="center", fontsize=7, color="blue")
    ax.annotate("S wall: WetLink M10 x2 @ z=65 (TD04A x85 / tether x120, box coords)", (cx, -oy - 7), ha="center", fontsize=7.5, color="dimgray")
    for xb in PEN_X_BOX:
        ax.add_patch(Circle((xb - PLATE_ORG_BOX[0], PEN_TIP_Y_BOX - PLATE_ORG_BOX[1] - PEN_NUT_D / 2),
                            PEN_NUT_D / 2, fill=False, ec="dimgray", lw=1.0))
    ax.annotate("N wall: gland x1 (GPS ANN-MB1)", (cx, PLATE_D + oy + 3), ha="center", fontsize=7.5, color="dimgray")
    ax.set_xlim(-ox - 10, BOX["iw"] - ox + 10)
    ax.set_ylim(-oy - 16, BOX["id"] - oy + 10)
    ax.set_aspect("equal")
    ax.set_title(f"{title}\n{BOX['name']} inner {BOX['iw']}x{BOX['id']}x{BOX['ih']} / plate {PLATE_W:.0f}x{PLATE_D:.0f} (BMP2123Z compat)", fontsize=9)
    ax2.axhline(0, color="k")
    ax2.axhline(BOX["ih"], color="r", ls="--")
    ax2.text(0.1, BOX["ih"] + 1, f"lid inner {BOX['ih']}", fontsize=8, color="r")
    ax2.bar(0, PLATE_T, bottom=PLATE_Z, width=0.8, color="#ccc")
    ax2.text(0, PLATE_Z + PLATE_T + 1, f"plate\n@{PLATE_Z:.0f}", ha="center", fontsize=7)
    for i, (n, zt, note) in enumerate(heights):
        ax2.bar(i + 1, zt, width=0.8, color=colors[n], alpha=0.8)
        ax2.text(i + 1, zt + 1.5, f"{zt:.0f}{note}", ha="center", fontsize=8)
    ax2.set_xticks(range(1, len(heights) + 1))
    ax2.set_xticklabels([h[0] for h in heights], fontsize=7)
    ax2.set_ylim(0, BOX["ih"] + 20)
    ax2.set_title("height budget (mm, box floor = 0)", fontsize=9)
    fig.tight_layout()
    fig.savefig(fname, dpi=130)
    print("wrote", fname)


def base_top(n):
    return PLATE_Z + PLATE_T + STANDOFF + PARTS[n]["h"]


def check_lipo_bridge(items):
    """LiPo ブリッジトレイが MAIN の穴 4 点の上に載り、MAIN の最高部品を越え、
    ベイが MAIN の外形内 (北縁のボタン/LED と南縁の SD を塞がない帯) にあること。"""
    tray_z0 = PLATE_Z + PLATE_T + STANDOFF + PCB_T + LIPO_SPACER   # トレイ下面 (床基準)
    main_top = PLATE_Z + PLATE_T + STANDOFF + PCB_T + MAIN_TOP_COMP
    assert tray_z0 - main_top >= 3.0, f"トレイ下面 {tray_z0} と MAIN 最高部品 {main_top:.1f} の隙間不足"
    lipo_top = tray_z0 + TRAY_FLOOR_T + PARTS["LIPO"]["h"]
    mx, my, mw, md = items["MAIN"]
    ox, oy, ow, od = LIPO_TRAY_OUTER
    assert mx - 6 <= ox and ox + ow <= mx + mw + 6, "トレイが MAIN の東西幅を大きく越える"
    assert oy >= my + 10 and oy + od <= my + md - 20, "トレイが MAIN の南縁 (SD) か北縁 (ボタン/LED) を塞ぐ"
    return lipo_top


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    lid_margin = 3.0

    # ---- パターン1
    p1 = rects(LAYOUT_P1)
    check(p1)
    lipo_top = check_lipo_bridge(p1)
    check_penetrators(p1, lipo_top)
    h1 = [("MAIN", base_top("MAIN"), ""), ("PWR", base_top("PWR"), ""),
          ("TX", base_top("TX"), ""), ("SPR", base_top("SPR"), "*"),
          ("LIPO", lipo_top, "^"), ("LCD", PLATE_Z + PLATE_T + 30.0, "*")]
    for n, zt, _ in h1:
        assert zt <= BOX["ih"] - lid_margin, f"P1 {n} 高さ超過 {zt}"
    draw(os.path.join(here, "parent_layout_p1.png"),
         "Pattern 1 — camera external (DJI Osmo Action 6)", p1, heights=h1)

    # ---- パターン2
    p2 = rects(LAYOUT_P2)
    check(p2, stacked=P2_STACKED,
          soft_pairs={("TX", "CAM"), ("PIZERO", "CAM"), ("TX", "LCD")})
    check_viewport()
    check_stack_p2(p2)
    check_penetrators(p2, lipo_top)
    h2 = [("MAIN", base_top("MAIN"), ""), ("PWR", base_top("PWR"), ""),
          ("TX", PLATE_Z + PLATE_T + TX_RAISE + 1.6 + 13.79, "R"), ("SPR", base_top("SPR"), "*"),
          ("LIPO", lipo_top, "^"), ("PIZERO", base_top("PIZERO"), ""),
          ("CAM", PLATE_Z + PLATE_T + 18.0 + 1.6 + 22.0, "")]   # parent_cam_mount 脚15+t3 + 基板 + CSI/部品 (仮)
    for n, zt, _ in h2:
        assert zt <= BOX["ih"] - lid_margin, f"P2 {n} 高さ超過 {zt}"
    draw(os.path.join(here, "parent_layout_p2.png"),
         "Pattern 2 — Pi Zero 2W + GS camera inside, bottom viewport Ø30 @ +X53", p2,
         viewport=True, heights=h2)
    print("all checks passed (*=height assumed, ^=on bridge tray over MAIN, R=raised)")
