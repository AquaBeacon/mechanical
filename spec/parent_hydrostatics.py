# -*- coding: utf-8 -*-
"""parent_hydrostatics.py — 親機 (双胴) の喫水線と復原力 (GM) の試算

浮子だけでなく、水に浸かる箱・デッキ・ヨーク (プリント品はインフィル空洞が密閉なので
中実体積ぶん排水する) を全部入れて喫水線を解き、浮心・水線面二次モーメント・重心から
GM = z_B + I/V − z_G を横揺れ (roll, X 軸回り) と縦揺れ (pitch, Y 軸回り) で出す。

座標: デッキ上面 = 箱底 = z 0、+Z 上。長さ mm、体積 L、質量 kg。
使い方: python spec/parent_hydrostatics.py            (浮子高さの掃引表 + 採用値)
出力を parent_float_yoke.scad の `waterline_z` に転記する (2026-09-05)。

質量・寸法はすべて見積/仮値。浮子実測と実機の秤量で更新すること。
"""
import math

# ---- 見積質量 [kg] と重心 z [mm] (2026-09-05。4.0 kg 版は箱の二重計上で誤り) ----
def masses(zf, post_top):
    yoke_z = 0.5 * ((-53 + 3) / 2) + 0.5 * ((zf - 40 + post_top) / 2)   # フィン半分 + 柱半分
    return [
        ("箱 BCAS212310G (ABS)",      0.45, 50),
        ("内装 (基板3+SPRESENSE+LiPo+プレート+トレイ)", 0.60, 40),
        ("parent_deck (PETG 25%)",    0.40, -22),
        ("parent_float_yoke ×4",      0.68, yoke_z),
        ("浮子 ×2 (仮)",              0.25, zf),
        ("TD04A + ソケット",          0.20, -85),
        ("Osmo + ケース + ジグ (仮)", 0.36, -85),
        ("GPS アンテナ (蓋上)",       0.10, 105),
        ("ねじ・紐・インサート",       0.10, 0),
    ]

# ---- 浮子 (紡錘 仮値) ----
R = 50.0                       # 最大半径
V_FLOAT = 2.003e6              # 全没排水量 mm3 (parent_fender.scad の echo)
L_EQ = V_FLOAT / (math.pi * R * R)   # 円筒等価長 (255)
X_FLOAT = 178                  # 浮子軸 X (±)

def seg_area(r, h):            # 円の中心から高さ h までの下側の面積
    h = max(-r, min(r, h)); th = 2 * math.acos(h / r)
    return math.pi * r * r - r * r / 2 * (th - math.sin(th))

def seg_chord(r, h):
    h = max(-r, min(r, h)); return 2 * math.sqrt(max(0.0, r * r - h * h))

# ---- 浮子以外の浸水体 (name, z0, z1, 断面積, X オフセット列 (roll), Y オフセット列 (pitch), 自身の Ix, Iy) ----
def bodies(zf, post_top):
    return [
        ("box body",   0,    80,   204 * 224, [0],         [0],          224 * 204**3 / 12, 204 * 224**3 / 12),
        ("box cover",  80,   100.3, 230 * 210, [0],        [0],          210 * 230**3 / 12, 230 * 210**3 / 12),
        ("deck plate", -6,   0,    216 * 236, [0],         [0],          236 * 216**3 / 12, 216 * 236**3 / 12),
        ("deck lips",  -50,  -6,   17 * 236,  [-99.5, 99.5], [0],        236 * 17**3 / 12,  17 * 236**3 / 12),
        ("keel",       -60,  -6,   4600,      [0],         [0],          0, 0),
        ("yoke fins",  -53,  post_top, 18 * 127, [-117, 117], [-105, 105], 127 * 18**3 / 12, 18 * 127**3 / 12),
        ("yoke posts", zf - 40, post_top, 113 * 32 - 800, [-164, 164], [-153, 153], 32 * 113**3 / 12, 113 * 32**3 / 12),
        ("td04a",      -104, -60,  1500,      [0],         [-70],        0, 0),
    ]

def displacement(zw, zf, post_top):
    V = 0.0
    for n, z0, z1, A, xs, ys, ix, iy in bodies(zf, post_top):
        V += A * max(0.0, min(zw, z1) - z0) * len(xs)
    V += 2 * seg_area(R, zw - zf) * L_EQ
    return V

def hydro(zf, mass, post_top):
    lo, hi = -150.0, 150.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if displacement(mid, zf, post_top) < mass * 1e6: lo = mid
        else: hi = mid
    zw = (lo + hi) / 2
    V = Mz = Ir = Ip = 0.0
    for n, z0, z1, A, xs, ys, ix, iy in bodies(zf, post_top):
        top = min(zw, z1)
        if top > z0:
            v = A * (top - z0)
            V += v * len(xs); Mz += v * (z0 + top) / 2 * len(xs)
            if z1 > zw:
                for x in xs: Ir += ix + A * x * x
                for y in ys: Ip += iy + A * y * y
    h = zw - zf
    if h > -R:
        v = seg_area(R, h) * L_EQ
        s = m = 0.0; z = -R; dz = 0.5
        while z < min(h, R):
            c = seg_chord(R, z); s += c * dz; m += c * dz * z; z += dz
        zc = m / s if s else -R
        V += 2 * v; Mz += 2 * v * (zf + zc)
        if h < R:
            c = seg_chord(R, h)
            Ir += 2 * (L_EQ * c**3 / 12 + c * L_EQ * X_FLOAT**2)
            Ip += 2 * (c * L_EQ**3 / 12)
    zb = Mz / V
    return zw, V / 1e6, zb, Ir / V, Ip / V

def run(zf):
    post_top = zf + 40
    ms = masses(zf, post_top)
    m = sum(w for _, w, _ in ms); zg = sum(w * z for _, w, z in ms) / m
    zw, V, zb, bmr, bmp = hydro(zf, m, post_top)
    return dict(zf=zf, mass=m, zg=zg, zw=zw, V=V, zb=zb, gm_roll=zb + bmr - zg, gm_pitch=zb + bmp - zg)

if __name__ == "__main__":
    print("浮子軸 z_f   質量    重心 z_G   喫水線 z_w   浮心 z_B   GM_roll   GM_pitch   ペネトレータ (z 65) の水面上")
    for zf in [-40, -20, 0, 20, 40, 50]:
        r = run(zf)
        print(f"  {zf:5d}     {r['mass']:.2f}   {r['zg']:7.1f}   {r['zw']:8.1f}   {r['zb']:8.1f}   {r['gm_roll']:6.0f}    {r['gm_pitch']:6.0f}     {65 - r['zw']:6.1f}")
    r = run(0)
    print()
    print("採用 (2026-09-05): z_f = 0 (浮子軸 = デッキ上面 = 箱底。縦揺れ GM が最大、箱底がほぼ水面)")
    print(f"  waterline_z = {r['zw']:.1f}  → parent_float_yoke.scad の waterline_z に転記")
    print("  見積質量の内訳:")
    for n, w, z in masses(0, 40):
        print(f"    {n:44s} {w:.2f} kg @ z {z:+.0f}")
