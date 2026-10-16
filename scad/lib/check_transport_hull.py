"""Transport-posture "who sticks out" check for an assembly placement.json.

  python scad/lib/check_transport_hull.py assemblies/child_frame2_assembly/placement.json --root . \
         [--exclude-groups attach] [--exclude-labels cam_mount_stbd,cam_mount_port,lug_stbd] \
         [--include-groups transport] [--removable lug_stbd,lug_port] [--tol 5] \
         [--limit 280,250,400] [--json out.json]

Purpose (docs/子機外装_改善要件.md 3.8, R4 "単独で突き出た部品を作らない"):
build the requested configuration (some parts removed for transport, a
transport cap/etc added via --include-groups) and, for each of the 26 unit
directions (6 face + 12 edge + 8 corner of a cube: every combination of
{-1,0,1} in X/Y/Z except all-zero), find which part's STL is farthest out
along that direction (its "support" vertex, i.e. an approximate convex-hull
face in that direction) and by how much it leads the second-farthest part.

Judgement per direction:
    lead_mm = support(1st part) - support(2nd part)   (mm, projected along d)
    NG   if lead_mm > --tol (default 5mm) AND the leading part's label is
         NOT listed in --removable (a part the crew can/does remove, or a
         sacrificial transport feature, so a solo protrusion there is fine)
    OK   otherwise

This is a per-vertex approximation of the true convex hull in each direction
(taking the STL vertex with the maximum dot product with the unit direction
vector), not a full 3D convex-hull construction -- adequate for "who is the
first thing to hit the ground / a wall from this direction" but it will not
notice a mid-edge overhang of a curved surface whose extreme point is not a
mesh vertex (STL facets are flat, so for this repo's meshes the two agree).

Group / label selection (mirrors asm_to_stl.py's MISSING-STL convention):
  - Parts are included by default if their item's "group" is listed True in
    placement.json's top-level "groups", or if that group name is passed via
    --include-groups (e.g. a normally-hidden "transport" group holding a cap).
  - --exclude-groups / --exclude-labels remove parts from that default set
    (e.g. drop lugs/cam mounts that are physically off the unit in transit).
  - Items with no "group" key are always included unless --exclude-labels
    names them.
  - A part whose STL file is missing on disk is skipped with a MISSING
    warning (script continues, matching asm_to_stl.py's behaviour) and is
    not counted for direction/bbox purposes.

After the 26-row table the script prints the overall bounding box (min/max
per axis and the resulting X/Y/Z dimensions across every included part) and,
if --limit X,Y,Z (mm) is given, flags any axis that exceeds it.

Exit code is 1 if any direction is NG or the bounding box exceeds --limit,
else 0. --json writes the same data as BOM-less UTF-8 JSON.

Reuses the same ops -> 4x4 matrix builders (translate/rotate/mirror/scale,
applied outside-in exactly like OpenSCAD / asm_gen.py / asm_to_stl.py) and
the pure-numpy STL loader from verify_child_interior.py -- no new transform
code, no trimesh/FreeCAD dependency.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_child_interior import load_stl, matrix  # noqa: E402


AXES = ("X", "Y", "Z")


def direction_list():
    """26 unit directions: 6 face, then 12 edge, then 8 corner (stable sort by
    the number of nonzero axes keeps itertools.product's natural order within
    each group)."""
    combos = [c for c in itertools.product((-1, 0, 1), repeat=3) if any(c)]
    combos.sort(key=lambda c: sum(1 for x in c if x != 0))
    out = []
    for c in combos:
        label = "".join(f"{'+' if s > 0 else '-'}{axis}" for s, axis in zip(c, AXES) if s != 0)
        vec = np.asarray(c, dtype=float)
        vec /= np.linalg.norm(vec)
        out.append((label, vec))
    return out


def select_items(asm, exclude_groups, exclude_labels, include_groups):
    groups = asm.get("groups") or {}
    default_true = {g for g, v in groups.items() if v}
    wanted = default_true | include_groups
    items = []
    for item in asm.get("items", []):
        label = item.get("label", "?")
        group = item.get("group")
        if group is not None and group not in wanted:
            continue
        if group is not None and group in exclude_groups:
            continue
        if label in exclude_labels:
            continue
        items.append(item)
    return items


def load_world_vertices(root: Path, item):
    part = Path(item["part"])
    stem = item.get("file") or part.name
    stl = root / part / f"{stem}.stl"
    if not stl.exists():
        return None
    verts = load_stl(stl)
    hom = np.column_stack([verts, np.ones(len(verts))])
    world = (matrix(item.get("ops")) @ hom.T).T[:, :3]
    return world


def parse_csv_set(value):
    if not value:
        return set()
    return {x.strip() for x in value.split(",") if x.strip()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("placement", type=Path)
    ap.add_argument("--root", type=Path, default=Path.cwd())
    ap.add_argument("--exclude-groups", default="")
    ap.add_argument("--exclude-labels", default="")
    ap.add_argument("--include-groups", default="")
    ap.add_argument("--removable", default="", help="labels allowed to be a solo protrusion")
    ap.add_argument("--tol", type=float, default=5.0, help="mm; lead over the 2nd part beyond this is NG")
    ap.add_argument("--limit", default="", help="X,Y,Z mm upper bound for the overall bounding box")
    ap.add_argument("--json")
    args = ap.parse_args()

    root = args.root
    asm = json.loads(args.placement.read_text(encoding="utf-8"))

    exclude_groups = parse_csv_set(args.exclude_groups)
    exclude_labels = parse_csv_set(args.exclude_labels)
    include_groups = parse_csv_set(args.include_groups)
    removable = parse_csv_set(args.removable)

    items = select_items(asm, exclude_groups, exclude_labels, include_groups)

    world = {}
    missing = []
    for item in items:
        label = item.get("label", "?")
        w = load_world_vertices(root, item)
        if w is None:
            missing.append(label)
            print(f"[check_transport_hull] MISSING STL for {label}, skipping")
            continue
        world[label] = w

    if not world:
        raise SystemExit("no parts loaded (check --root / group filters)")

    directions = direction_list()

    rows = []
    ng_count = 0
    print(f"{'dir':10s} {'first':22s} {'lead_mm':>8s}  {'second':22s} judge")
    for label, d in directions:
        supports = [(name, float(np.max(verts @ d))) for name, verts in world.items()]
        supports.sort(key=lambda t: -t[1])
        first_name, first_val = supports[0]
        second_name, second_val = supports[1] if len(supports) > 1 else (None, first_val)
        lead = first_val - second_val
        judge = "OK"
        if lead > args.tol and first_name not in removable:
            judge = "NG"
            ng_count += 1
        rows.append({
            "dir": label, "first": first_name, "lead_mm": lead,
            "second": second_name, "judge": judge,
        })
        print(f"{label:10s} {first_name:22s} {lead:8.2f}  {str(second_name):22s} {judge}")

    all_verts = np.vstack(list(world.values()))
    mins = all_verts.min(axis=0)
    maxs = all_verts.max(axis=0)
    dims = maxs - mins

    print()
    print(f"NG: {ng_count} / {len(rows)}")
    print("bbox (mm):")
    for i, axis in enumerate(AXES):
        print(f"  {axis}: {mins[i]:8.2f} .. {maxs[i]:8.2f}   dim={dims[i]:8.2f}")

    limit_ng = False
    limit_vals = None
    if args.limit:
        limit_vals = [float(x) for x in args.limit.split(",")]
        if len(limit_vals) != 3:
            raise SystemExit("--limit needs 3 comma-separated values X,Y,Z")
        over = [axis for i, axis in enumerate(AXES) if dims[i] > limit_vals[i]]
        limit_ng = bool(over)
        status = "NG" if limit_ng else "OK"
        print(f"limit {limit_vals}: {status}" + (f" (over: {','.join(over)})" if over else ""))

    if missing:
        print(f"MISSING parts (skipped): {', '.join(missing)}")

    if args.json:
        payload = {
            "directions": rows,
            "ng_count": ng_count,
            "bbox": {"min": mins.tolist(), "max": maxs.tolist(), "dim": dims.tolist()},
            "limit": limit_vals,
            "limit_ng": limit_ng,
            "missing": missing,
        }
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=1, ensure_ascii=False)

    return 1 if (ng_count or limit_ng) else 0


if __name__ == "__main__":
    raise SystemExit(main())
