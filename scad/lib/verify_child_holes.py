"""Check that the tray's mounting features land on the real PCB mounting holes.

Ground truth is the ``.kicad_pcb`` itself (Edge.Cuts bounding box + MountingHole
footprint positions + drill diameter) -- not any ``.md``, which is how the 17.5 mm
CHILD_MAIN error survived: every document agreed with every other document and all
of them disagreed with the board.

The tray side is read from OpenSCAD's own ``HOLETABLE`` echo, so the check runs
against the geometry that will actually be built, including any ``variants.txt``
overrides.  The board side is transformed into assembly coordinates with the very
matrix ``asm_gen.py`` uses, straight out of ``placement.json``.

    python scad/lib/verify_child_holes.py assemblies/child_vertical_assembly/placement.json --root .

Exit status is non-zero if any hole is out of tolerance, if a screw does not fit
the drilled hole, or if a board named in the tray is missing from the assembly.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import subprocess
import sys
from pathlib import Path

OPENSCAD = os.environ.get(
    "OPENSCAD", r"C:\Program Files\OpenSCAD\openscad.exe")

# Nominal screw -> the clearance drill the board must have for it to pass.
SCREW_DRILL = {"M2": 2.2, "M2.5": 2.7, "M3": 3.2, "M4": 4.3}

# Which printed part carries the mounting features, and which variant to build.
TRAY_PART = "parts/child/interior/printed/child_vtray_deck"


# --------------------------------------------------------------------------
# .kicad_pcb  (a tiny s-expression reader; no KiCad install needed)
# --------------------------------------------------------------------------
def parse_sexp(text: str):
    tokens = re.findall(r'\(|\)|"(?:[^"\\]|\\.)*"|[^\s()]+', text)
    stack, cur = [], []
    for t in tokens:
        if t == "(":
            stack.append(cur)
            cur = []
        elif t == ")":
            done, cur = cur, stack.pop()
            cur.append(done)
        else:
            cur.append(t[1:-1].replace('\\"', '"') if t.startswith('"') else t)
    return cur


def walk(node):
    yield node
    for child in node:
        if isinstance(child, list):
            yield from walk(child)


def field(node, key):
    for child in node:
        if isinstance(child, list) and child and child[0] == key:
            return child
    return None


def read_board(path: Path):
    """-> (width, height, [(x, y_from_top, drill), ...]) in KiCad board coords."""
    root = parse_sexp(path.read_text(encoding="utf-8"))[0]

    xs, ys = [], []
    for node in walk(root):
        if not (node and isinstance(node[0], str)
                and node[0] in ("gr_line", "gr_rect", "gr_arc", "gr_circle")):
            continue
        layer = field(node, "layer")
        if not layer or layer[1] != "Edge.Cuts":
            continue
        for key in ("start", "end", "mid", "center"):
            pt = field(node, key)
            if pt:
                xs.append(float(pt[1]))
                ys.append(float(pt[2]))
    if not xs:
        raise SystemExit(f"{path.name}: no Edge.Cuts outline found")
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)

    holes = []
    for node in walk(root):
        if not (node and isinstance(node[0], str) and node[0] == "footprint"):
            continue
        lib = node[1] if len(node) > 1 and isinstance(node[1], str) else ""
        if "MountingHole" not in lib:
            continue
        at = field(node, "at")
        drill = None
        for pad in walk(node):
            if pad and isinstance(pad[0], str) and pad[0] == "pad":
                d = field(pad, "drill")
                if d:
                    drill = float(d[1])
        holes.append((float(at[1]) - x0, float(at[2]) - y0, drill))
    return x1 - x0, y1 - y0, sorted(holes)


# --------------------------------------------------------------------------
# placement.json -> the same 4x4 matrix asm_gen.py builds
# --------------------------------------------------------------------------
def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(4)) for j in range(4)]
            for i in range(4)]


def op_matrix(kind, v):
    m = [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]
    if kind == "translate":
        for i in range(3):
            m[i][3] = float(v[i])
        return m
    if kind == "rotate":
        a, b, c = (math.radians(float(x)) for x in v)
        ca, sa, cb, sb, cc, sc = (math.cos(a), math.sin(a), math.cos(b),
                                  math.sin(b), math.cos(c), math.sin(c))
        rx = [[1, 0, 0, 0], [0, ca, -sa, 0], [0, sa, ca, 0], [0, 0, 0, 1]]
        ry = [[cb, 0, sb, 0], [0, 1, 0, 0], [-sb, 0, cb, 0], [0, 0, 0, 1]]
        rz = [[cc, -sc, 0, 0], [sc, cc, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        return matmul(matmul(rz, ry), rx)
    if kind == "mirror":
        n = [float(x) for x in v]
        ln = math.sqrt(sum(x * x for x in n)) or 1.0
        n = [x / ln for x in n]
        for i in range(3):
            for j in range(3):
                m[i][j] -= 2 * n[i] * n[j]
        return m
    if kind == "scale":
        for i in range(3):
            m[i][i] = float(v[i])
        return m
    raise SystemExit(f"unknown placement op: {kind}")


def placement_matrix(ops):
    m = [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]
    for op in ops or []:
        for kind, value in op.items():
            m = matmul(m, op_matrix(kind, value))
    return m


def apply(m, p):
    return tuple(sum(m[i][k] * (list(p) + [1.0])[k] for k in range(4))
                 for i in range(3))


# --------------------------------------------------------------------------
# the tray's own view, straight from OpenSCAD
# --------------------------------------------------------------------------
def read_variant_defs(part_dir: Path, want_suffix: str | None):
    vf = part_dir / "variants.txt"
    if not vf.exists():
        return []
    for line in vf.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        tok = line.split()
        if want_suffix in (None, tok[0]):
            return tok[1:]
    return []


def read_hole_table(scad: Path, defs):
    cmd = [OPENSCAD]
    for d in defs:
        cmd += ["-D", d]
    cmd += ["-o", os.devnull + ".csg", str(scad)]
    proc = subprocess.run(cmd, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")
    out = proc.stdout + proc.stderr
    if "ERROR" in out:
        for line in out.splitlines():
            if "ERROR" in line:
                print(f"  openscad: {line.strip()}")
        raise SystemExit(f"{scad.name} did not build; fix it before checking holes")

    table = {}
    for m in re.finditer(r'(HOLETABLE|CLAMPTABLE) (\S+) (\S+?)\[(.*?)\]"', out):
        kind, board, screw, body = m.groups()
        if kind == "CLAMPTABLE":
            screw += "_EDGE_CLAMP"
        pts = []
        for chunk in re.findall(r'"\s*(-?[\d.]+),(-?[\d.]+)"', body):
            pts.append((float(chunk[0]), float(chunk[1])))
        table[board] = (screw, sorted(pts))
    if not table:
        raise SystemExit(f"{scad.name} printed no HOLETABLE echo -- did the "
                         f"machine-readable echo get removed?")
    return table


# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("placement", type=Path)
    ap.add_argument("--root", type=Path, default=Path.cwd())
    ap.add_argument("--kicad", type=Path,
                    default=Path("../hardware/pcb"),
                    help="folder holding <BOARD>/<BOARD>.kicad_pcb")
    ap.add_argument("--variant", default=None,
                    help="variants.txt suffix to check (default: the first line)")
    ap.add_argument("--tol", type=float, default=0.10,
                    help="max allowed in-plane offset, mm")
    args = ap.parse_args()

    root = args.root.resolve()
    kicad = (root / args.kicad).resolve()
    asm = json.loads(args.placement.read_text(encoding="utf-8"))
    items = {it["label"]: it for it in asm.get("items", [])}

    part_dir = root / TRAY_PART
    scad = part_dir / f"{part_dir.name}.scad"
    defs = read_variant_defs(part_dir, args.variant)
    print(f"tray : {part_dir.name}  [{' '.join(defs) or 'no variant'}]")
    tray = read_hole_table(scad, defs)

    for d in defs:
        name = d.split("=")[0]
        if name.endswith(("_hx", "_hu", "_hv", "_h_kx", "_h_ky")):
            print(f"  !! variants.txt overrides the hole position '{name}'. "
                  f"Hole positions must come from the .kicad_pcb, never a variant.")
            return 1

    failed = False
    for board, (screw, tray_pts) in sorted(tray.items()):
        item = items.get(board)
        if item is None:
            print(f"\n{board}: FAIL -- named by the tray but absent from "
                  f"{args.placement.name}")
            failed = True
            continue

        pcb = kicad / board.upper() / f"{board.upper()}.kicad_pcb"
        if not pcb.exists():
            hits = list(kicad.glob(f"*/*.kicad_pcb"))
            hits = [h for h in hits if h.stem.lower() == board.lower()]
            if not hits:
                print(f"\n{board}: FAIL -- no .kicad_pcb under {kicad}")
                failed = True
                continue
            pcb = hits[0]

        bw, bh, holes = read_board(pcb)
        m = placement_matrix(item.get("ops"))
        # Every PCB model in this repo exports as x = 0..w, y = -h..0, board z = 0.
        world = sorted((apply(m, (hx, -hy, 0.0))[0], apply(m, (hx, -hy, 0.0))[2])
                       for hx, hy, _ in holes)
        drills = [d for _, _, d in holes]

        if screw == "M3_EDGE_CLAMP":
            actual = sorted((it['ops'][0]['translate'][0],it['ops'][0]['translate'][2])
                            for label,it in items.items() if label.startswith('rx_clamp_mount_'))
            corners=[apply(m,(x,y,0)) for x in (0,bw) for y in (-bh,0)]
            xmin,xmax=min(p[0] for p in corners),max(p[0] for p in corners)
            zmin,zmax=min(p[2] for p in corners),max(p[2] for p in corners)
            stations=[]
            for label,it in items.items():
                if not label.startswith('rx_clamp_base_'):
                    continue
                offsets=[0.0]
                if it.get('file','').endswith('_base_pair'):
                    source=root/it['part']/(Path(it['part']).name+'.scad')
                    # This parameter is a literal in the authoritative source.
                    # Fail closed if the source becomes an expression/override.
                    matches=re.findall(r'^pair_pitch\s*=\s*([0-9.]+)\s*;',source.read_text(encoding='utf-8'),re.M)
                    if len(matches)!=1:
                        raise ValueError('Cannot read paired clamp pitch from source')
                    variants=(source.parent/'variants.txt').read_text(encoding='utf-8-sig')
                    if re.search(r'\bpair_pitch\s*=',variants):
                        raise ValueError('Paired clamp pitch override needs geometry verification')
                    offsets.append(float(matches[0]))
                cm=placement_matrix(it.get('ops'))
                stations.extend(apply(cm,(0,0,z))[2] for z in offsets)
            ok=(len(actual)==len(tray_pts)==4 and actual==tray_pts and
                len(stations)==4 and all(zmin<=z-3.5 and z+3.5<=zmax for z in stations) and
                all(x+3.3 < xmin or x-3.3 > xmax for x,z in tray_pts))
            print(f"\n{board}: M3 edge-clamp mounts {actual}; PCB edge X{xmin:g}..{xmax:g}")
            print(f"   -> {'PASS' if ok else 'FAIL'}: original Ø{min(drills):g} PCB holes unused; M3/head reserve outside PCB")
            failed |= not ok
            continue

        print(f"\n{board}  ({pcb.name}, {bw:g} x {bh:g} mm, {len(holes)} holes)")
        worst = 0.0
        for (bx, bz), (tx, tz) in zip(world, tray_pts):
            dx, dz = tx - bx, tz - bz
            off = math.hypot(dx, dz)
            worst = max(worst, off)
            state = "ok" if off <= args.tol else "MISMATCH"
            print(f"   board (X={bx:8.2f}, Z={bz:8.2f})   tray (X={tx:8.2f}, "
                  f"Z={tz:8.2f})   dX={dx:+6.2f} dZ={dz:+6.2f}  {state}")
        if worst > args.tol:
            print(f"   -> FAIL: worst offset {worst:.2f} mm > {args.tol} mm")
            failed = True

        need = SCREW_DRILL.get(screw)
        real = min(d for d in drills if d)
        if need is None:
            print(f"   -> FAIL: tray asks for an unknown screw '{screw}'")
            failed = True
        elif real + 1e-6 < need:
            print(f"   -> FAIL: tray fastens with {screw} (needs Ø{need}) but the "
                  f"board is drilled Ø{real} -- the screw does not fit")
            failed = True
        elif worst <= args.tol:
            print(f"   -> {screw} into Ø{real} drill, worst offset {worst:.2f} mm  PASS")

    print("\nFAIL" if failed else "\nAll tray mounting features match the boards.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
