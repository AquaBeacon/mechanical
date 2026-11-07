"""Read-only location diagram for the parent floor access revision."""
from pathlib import Path
import hashlib
import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.patches import Rectangle, Circle
import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parents[1]
ASM = ROOT / 'assemblies/parent_hand_service'


def main():
    images = ASM / '_work/images'
    work = ASM / '_work/analysis/plate_access_20261027'
    images.mkdir(parents=True, exist_ok=True)
    work.mkdir(parents=True, exist_ok=True)
    source = ROOT / 'parts/parent/interior/printed/parent_hand_service/floor_plate.stl'
    mesh = trimesh.load_mesh(source)
    placement = json.loads((ASM / 'placement.json').read_text(encoding='utf-8'))
    plt.rcParams['font.family'] = 'Meiryo'
    fig, ax = plt.subplots(figsize=(8, 9))
    # Top-facing triangles show the actual mesh rather than a second floor design.
    faces = mesh.triangles[mesh.face_normals[:, 2] > .01, :, :2]
    ax.add_collection(PolyCollection(faces, facecolor='#adb7bf', edgecolor='none'))
    ax.add_patch(Rectangle((0, 0), 210, 230, fill=False, ec='#46545f', lw=1.3))
    ax.add_patch(Rectangle((148.8, 134.7), 53.6, 73.3, fill=True,
                           fc='#dc8b40', alpha=.18, ec='#b46621', ls='--'))
    ax.text(174, 176, 'SPRESENSE\n（上段）', ha='center', va='center', color='#914a16')
    for i, (x, y) in enumerate([(25, 25), (185, 25), (25, 205), (185, 205)]):
        ax.add_patch(Circle((x, y), 5, fill=False, ec='#b34136', lw=1.5))
        ax.text(x, y - 11, 'M4' if i < 3 else 'M4 未使用', ha='center', fontsize=9)
    ax.plot([140, 210], [230, 230], color='#327d9d', lw=7, solid_capstyle='butt')
    ax.plot([210, 210], [130, 223], color='#48864b', lw=7, solid_capstyle='butt')
    ax.text(175, 241, 'A：上の側面', ha='center', color='#21637f', fontsize=12)
    ax.text(225, 178, 'B：右の側面', rotation=90, va='center', color='#326537', fontsize=12)
    ax.text(105, -16, 'ケース外形 210 × 230 mm ／ 真上から', ha='center', fontsize=11)
    ax.set(xlim=(-16, 243), ylim=(-28, 253), aspect='equal', xlabel='X [mm]', ylabel='Y [mm]')
    ax.set_xticks(np.arange(0, 211, 25))
    ax.set_yticks(np.arange(0, 231, 25))
    ax.grid(alpha=.16)
    ax.set_title('現行の床板：ペネトレータ位置の確認用', pad=22, fontsize=15)
    fig.tight_layout()
    image = images / 'plate_access_20261027_location.png'
    fig.savefig(image, dpi=160)
    plt.close(fig)
    report = dict(status='inspection_only_pending_interface_dimensions',
                  source=str(source.relative_to(ROOT)),
                  source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                  source_watertight=bool(mesh.is_watertight),
                  bounds_mm=mesh.bounds.tolist(), volume_mm3=float(mesh.volume),
                  user_confirmed=dict(penetrators='two, case side below SPRESENSE',
                                      screw='M4, approximately 10 mm head, floor-to-case'),
                  current_counterbore_d_mm=8.2,
                  proposed_counterbore_d_mm=10.8,
                  pending=['side A or B and two hole positions/heights',
                           'penetrator dry-side projection and nut envelope',
                           'M4 head height and under-head length'],
                  existing_penetrators=[row for row in placement['items']
                                        if row['label'] in ['pen_tether', 'pen_td04a']],
                  manufacturing_release=False,
                  note='No CAD or print set has been modified by this inspection.')
    (work / 'inspection.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(image)


if __name__ == '__main__':
    main()
