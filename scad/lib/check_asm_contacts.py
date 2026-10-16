"""Contact / penetration / floating check for an assembly placement.json.

  python scad/lib/check_asm_contacts.py assemblies/child_interior/placement.json \
         --root . [--groups interior] [--touch 0.3] [--json out.json]

For every pair of parts it reports the minimum surface distance and, when the
surfaces are closer than --touch, whether one part's surface samples lie INSIDE
the other (= penetration).  A part whose closest neighbour is farther than
--touch is reported as FLOATING.  The vertical assembly convention of
placement.json (ops applied outside-in) is shared with verify_child_interior.py.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import trimesh
from scipy.spatial import cKDTree

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_child_interior import translate, rotate, mirror, scale  # noqa: E402

OPS = {"translate": translate, "rotate": rotate, "mirror": mirror, "scale": scale}


def matrix(ops):
    m = np.eye(4)
    for op in ops or []:
        (k, v), = op.items()
        m = m @ OPS[k](v)
    return m


def load(root: Path, item) -> trimesh.Trimesh:
    name = item.get("file") or item["part"].split("/")[-1]
    mesh = trimesh.load(root / item["part"] / f"{name}.stl", force="mesh")
    mesh.apply_transform(matrix(item.get("ops")))
    return mesh


def surface_samples(mesh: trimesh.Trimesh, per_mm2=0.15, cap=20000):
    n = int(min(cap, max(2000, mesh.area * per_mm2)))
    pts, _ = trimesh.sample.sample_surface_even(mesh, n)
    return np.vstack([mesh.vertices, pts])


def inset_samples(mesh: trimesh.Trimesh, depth=0.1, per_mm2=0.15, cap=20000):
    """Surface samples pushed `depth` mm INTO the part along the face normal.
    Used for the penetration test so that coplanar contact faces (a boss top
    against a board, a pad against a wall) do not count as penetration."""
    n = int(min(cap, max(2000, mesh.area * per_mm2)))
    pts, fid = trimesh.sample.sample_surface_even(mesh, n)
    return pts - mesh.face_normals[fid] * depth


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("placement")
    ap.add_argument("--root", default=".")
    ap.add_argument("--groups", default="interior", help="comma list; 'all' = everything")
    ap.add_argument("--touch", type=float, default=0.3, help="mm; closer = contact")
    ap.add_argument("--json")
    ap.add_argument("--ignore-threads", action="store_true",
                    help="do not report penetrations between a screw/spacer and the part it threads into "
                         "(self-tap pilots and modelled thread bores are smaller than the shank by design)")
    a = ap.parse_args()
    root = Path(a.root)
    asm = json.load(open(a.placement, encoding="utf-8"))
    groups = None if a.groups == "all" else set(a.groups.split(","))
    items = [it for it in asm["items"] if groups is None or it.get("group") in groups]

    meshes, samples, trees = {}, {}, {}
    for it in items:
        m = load(root, it)
        meshes[it["label"]] = m
        samples[it["label"]] = surface_samples(m)
        trees[it["label"]] = cKDTree(samples[it["label"]])

    names = list(meshes)
    inset = {}
    nearest = {n: (None, np.inf) for n in names}
    pairs = []
    for i, x in enumerate(names):
        for y in names[i + 1:]:
            bx, by = meshes[x].bounds, meshes[y].bounds
            if np.any(bx[0] > by[1] + 10) or np.any(by[0] > bx[1] + 10):
                continue
            d1, _ = trees[y].query(samples[x], distance_upper_bound=10)
            d2, _ = trees[x].query(samples[y], distance_upper_bound=10)
            d = float(min(d1.min(), d2.min()))
            if d == np.inf:
                continue
            pen = 0.0
            if d < a.touch:
                # depth of penetration: samples of x inside y and vice versa
                for src, dst in ((x, y), (y, x)):
                    if not meshes[dst].is_watertight:
                        continue
                    if src not in inset:
                        inset[src] = inset_samples(meshes[src])
                    inside = meshes[dst].contains(inset[src])
                    if inside.sum() >= 3:
                        dd, _ = trees[dst].query(inset[src][inside])
                        pen = max(pen, float(dd.max()))
            pairs.append((x, y, d, pen))
            for s, o in ((x, y), (y, x)):
                if d < nearest[s][1]:
                    nearest[s] = (o, d)

    print(f"{'part':28s} {'nearest':28s} {'gap':>7s}  status")
    floating = []
    for n in names:
        o, d = nearest[n]
        st = "ok"
        if d > a.touch:
            st = "FLOATING"
            floating.append(n)
        print(f"{n:28s} {str(o):28s} {d:7.2f}  {st}")
    print()
    print("penetrations (surface samples inside the other part):")
    fast = {it["label"] for it in items if "/cots/screw" in it["part"] or "/cots/hex_spacer" in it["part"]}
    bad = [p for p in pairs if p[3] > 0.05 and not (a.ignore_threads and (p[0] in fast or p[1] in fast))]
    for x, y, d, pen in sorted(bad, key=lambda p: -p[3]):
        print(f"  {x} <-> {y}: depth ~{pen:.2f} mm")
    if not bad:
        print("  none")
    if a.json:
        json.dump({"floating": floating,
                   "pairs": [dict(a=x, b=y, gap=d, penetration=pen) for x, y, d, pen in pairs]},
                  open(a.json, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    return 1 if (floating or bad) else 0


if __name__ == "__main__":
    raise SystemExit(main())
