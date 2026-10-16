"""Draw an illustrative locating proposal; this does not generate release CAD."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from matplotlib import font_manager


def main():
    root = Path(__file__).resolve().parents[1]
    out = root / "assemblies/parent_oneplate/_work/images/repeatable_mount_concept.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    for name in ("Yu Gothic", "Meiryo", "Noto Sans CJK JP"):
        if any(f.name == name for f in font_manager.fontManager.ttflist):
            plt.rcParams["font.family"] = name
            break
    plt.rcParams["axes.unicode_minus"] = False
    fig, ax = plt.subplots(figsize=(11, 8.5), facecolor="#f7f8fa")
    ax.set_facecolor("#f7f8fa")
    orange, blue, green = "#e3ac52", "#227da5", "#208568"
    # Nominal CAD dimensions; drawing omits float lugs, hardware and sensor bodies.
    for x, y, w, h in [(-116, -67, 24, 134), (92, -67, 24, 134),
                        (-116, -67, 232, 24), (-116, 43, 232, 24),
                        (-70, -67, 60, 134)]:
        ax.add_patch(Rectangle((x, y), w, h, facecolor=orange, edgecolor="none"))
    ax.add_patch(Rectangle((-52, -50), 24, 100, facecolor="#f7f8fa", edgecolor="none"))
    ax.add_patch(Rectangle((-105, -115), 210, 230, facecolor="#76889a", alpha=.10))
    ax.add_patch(Rectangle((-105, -115), 210, 230, fill=False, edgecolor="#526170", lw=2))
    for x in (-110, 110):
        for y in (-55, 55):
            ax.add_patch(Circle((x, y), 3, color="#58606c"))
    # Proposed small, hard side locators and a keyed, retained extension stop.
    for y in (-38, 38):
        ax.add_patch(Rectangle((-109, y-7), 4, 14, color=blue))
    ax.add_patch(Rectangle((90, 55), 12, 64, color=blue, alpha=.75))
    ax.add_patch(Rectangle((88, 115), 17, 4, color=blue))
    for x, y in [(-96, -55), (96, -55), (96, 55)]:
        ax.add_patch(Circle((x, y), 5, color=green))
    for y in (-38, 38):
        ax.annotate("", xy=(102, y), xytext=(137, y),
                    arrowprops=dict(arrowstyle="->", color=blue, lw=2))
    ax.annotate("", xy=(60, -111), xytext=(60, -145),
                arrowprops=dict(arrowstyle="->", color=blue, lw=2))
    ax.annotate("側面の基準 2か所\n左右位置・向きを決める", xy=(-107, 38), xytext=(-190, 95),
                fontsize=12, color=blue, arrowprops=dict(arrowstyle="-", color=blue))
    ax.annotate("端面の基準 1か所\n細い延長ストッパー", xy=(96, 117), xytext=(20, 153),
                fontsize=12, color=blue, arrowprops=dict(arrowstyle="-", color=blue))
    ax.annotate("底面の硬い基準 3か所\n高さ・傾きを決める", xy=(-96, -55), xytext=(-190, -143),
                fontsize=12, color=green, arrowprops=dict(arrowstyle="-", color=green))
    ax.text(140, 0, "反対側から\n基準へ押す", color=blue, fontsize=12, va="center")
    ax.text(65, -142, "端面の基準へ押す", color=blue, fontsize=11)
    ax.text(0, 84, "箱：210 × 230 mm", ha="center", fontsize=13, color="#526170")
    ax.text(0, -87, "既存フレーム：232 × 134 mm", ha="center", fontsize=12, color="#96641c")
    ax.text(-40, 0, "カメラ\n取付部", ha="center", va="center", fontsize=10, color="#96641c")
    ax.set_title("位置決め案：上から見た概念図", fontsize=19, loc="left", pad=18)
    ax.text(0.0, -0.025,
            "既存寸法を使用。基準点・押付機構・延長部は提案位置。実物適合・強度・スライスは未検証。",
            transform=ax.transAxes, fontsize=10, color="#596572")
    ax.set(xlim=(-200, 205), ylim=(-162, 180))
    ax.set_aspect("equal")
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(out, dpi=160)
    plt.close(fig)
    print(out)


if __name__ == "__main__":
    main()
