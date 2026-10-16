"""Draw a provisional design-review diagram; never generates production CAD."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'assemblies/over_center_latch/_work/images/recessed_receiver_concept.png'
plt.rcParams['font.family'] = 'Yu Gothic'
fig, ax = plt.subplots(figsize=(12, 6.2))
fig.patch.set_facecolor('#fafaf7')
ax.set_facecolor('#fafaf7')
gray, orange, blue, green = '#657583', '#df9a32', '#3579a0', '#46836b'

# Schematic shapes only; contact and pivot dimensions are not design values.
ax.add_patch(Rectangle((-42, -5), 50, 5, facecolor=gray))
ax.add_patch(Rectangle((9, -7), 34, 7, facecolor=green))
# A shallow undercut pocket with a steep load-bearing step, cut into the plate.
ax.add_patch(Polygon([(24, -4.5), (38, -4.5), (38, 1), (29, 1),
                     (29, -1.4), (24, -1.4)], facecolor='#fafaf7'))
ax.add_patch(Polygon([(-5, 0), (-4, 4), (4, 4), (5, 0)], facecolor=gray))
ax.add_patch(Circle((0, 4), 3.2, facecolor=gray))
ax.plot([0, -11.6], [4, 2.9], color=orange, lw=15, solid_capstyle='round')
ax.plot([-37, -15, -8, 33, 33, 26.3], [11, 11, 11, 11, -3, -3],
        color=blue, lw=10, solid_capstyle='round', solid_joinstyle='round')
ax.plot([-11.6, -8], [2.9, 11], color=blue, lw=10, solid_capstyle='round')
ax.add_patch(Rectangle((24, -4.4), .6, 2.9, facecolor='#333333'))
ax.add_patch(Circle((26.3, -3), 1.4, facecolor=blue, edgecolor='white', lw=1))
for label, p in [('A', (0, 4)), ('B', (-11.6, 2.9))]:
    ax.add_patch(Circle(p, .9, color='#e8ecef', ec='#333333'))
    ax.text(p[0]-1, p[1]+3.6, label, fontsize=12, weight='bold')

def note(text, xy, at, color='#29333b'):
    ax.annotate(text, xy=xy, xytext=at, fontsize=11, color=color,
                arrowprops=dict(arrowstyle='-', color=color), ha='center')

note('左右リンク', (-6, 3.5), (-17, -11), orange)
note('Bより爪と反対側へ操作部を延長\n同じ手の力で大きな操作モーメント', (-30, 11), (-28, 23), blue)
note('爪付きの上蓋レバー', (33, 8), (27, 22), blue)
note('台に浅いくぼみ\n荷重側はほぼ垂直の段', (24.4, -2.9), (48, 10), green)
note('EPDM：ガタ取り・予圧', (24.3, -3.5), (49, -7))
note('一般部4〜5 mmを目標\n受け部は底肉と保持縁を残す', (7, -5), (11, -13))
ax.annotate('', xy=(-37, 4), xytext=(-37, 16),
            arrowprops=dict(arrowstyle='->', color='#b75242', lw=2))
ax.text(-40, 17, '手で押す', color='#b75242', fontsize=11)
ax.annotate('', xy=(-44, -2.5), xytext=(-35, -2.5),
            arrowprops=dict(arrowstyle='->', color='#b75242', lw=2))
ax.annotate('', xy=(45, -2.5), xytext=(39, -2.5),
            arrowprops=dict(arrowstyle='->', color='#b75242', lw=2))
ax.text(-44, 30.5, '修正案：台のくぼみで保持＋Bの外側へ操作部を延長', fontsize=16, weight='bold')
ax.text(-44, -19, '断面概念図・寸法未確定／独立ストッパーなし。閉じ終わりはレバー下面と台の接触を候補とする。\n死点・干渉・底肉・保持縁・強度は未検証。目標：ラッチ1個で引離し外力40 N。',
        fontsize=10, color='#59636b')
ax.set_xlim(-48, 63)
ax.set_ylim(-23, 34)
ax.set_aspect('equal')
ax.axis('off')
fig.tight_layout()
OUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT, dpi=170, facecolor=fig.get_facecolor())
print(OUT)
