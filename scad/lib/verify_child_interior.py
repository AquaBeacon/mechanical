"""Verify every child-interior STL against the measured WTE4 radial envelope."""

from __future__ import annotations

import argparse
import json
import math
import struct
from pathlib import Path

import numpy as np


def load_stl(path: Path) -> np.ndarray:
    raw = path.read_bytes()
    if len(raw) >= 84:
        n = struct.unpack_from("<I", raw, 80)[0]
        if 84 + n * 50 == len(raw):
            rec = np.frombuffer(raw, dtype=np.dtype([
                ("normal", "<f4", 3), ("v", "<f4", (3, 3)), ("attr", "<u2")
            ]), offset=84, count=n)
            return rec["v"].reshape(-1, 3).astype(float)
    verts = []
    for line in raw.decode("utf-8", errors="ignore").splitlines():
        fields = line.strip().split()
        if len(fields) == 4 and fields[0].lower() == "vertex":
            verts.append([float(v) for v in fields[1:]])
    if not verts:
        raise ValueError(f"not an STL: {path}")
    return np.asarray(verts, dtype=float)


def translate(v):
    m = np.eye(4)
    m[:3, 3] = v
    return m


def rotate(v):
    a, b, c = np.radians(v)
    rx = np.array([[1, 0, 0, 0], [0, math.cos(a), -math.sin(a), 0],
                   [0, math.sin(a), math.cos(a), 0], [0, 0, 0, 1]])
    ry = np.array([[math.cos(b), 0, math.sin(b), 0], [0, 1, 0, 0],
                   [-math.sin(b), 0, math.cos(b), 0], [0, 0, 0, 1]])
    rz = np.array([[math.cos(c), -math.sin(c), 0, 0],
                   [math.sin(c), math.cos(c), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    return rz @ ry @ rx


def mirror(v):
    n = np.asarray(v, dtype=float)
    n /= np.linalg.norm(n)
    m = np.eye(4)
    m[:3, :3] -= 2 * np.outer(n, n)
    return m


def scale(v):
    return np.diag([*v, 1.0])


BUILDERS = {"translate": translate, "rotate": rotate, "mirror": mirror, "scale": scale}


def matrix(ops):
    m = np.eye(4)
    for op in ops or []:
        for kind, value in op.items():
            m = m @ BUILDERS[kind](value)
    return m


def allowed_radius(z):
    # Measured flange piston inner faces are z=19/181. The central tube ID is
    # 101.6; the end regions are the flange bore Ø88.5.
    return np.where((z >= 19.0) & (z <= 181.0), 50.8, 44.25)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("placement", type=Path)
    ap.add_argument("--root", type=Path, default=Path.cwd())
    ap.add_argument("--warn-clear", type=float, default=0.8)
    args = ap.parse_args()
    asm = json.loads(args.placement.read_text(encoding="utf-8"))

    failed = False
    print("label                              z range       min radial clearance")
    for item in asm.get("items", []):
        if item.get("group") != "interior" or item.get("skip_envelope"):
            continue
        part = Path(item["part"])
        stem = item.get("file") or part.name
        stl = args.root / part / f"{stem}.stl"
        verts = load_stl(stl)
        hom = np.column_stack([verts, np.ones(len(verts))])
        world = (matrix(item.get("ops")) @ hom.T).T[:, :3]
        radial = np.hypot(world[:, 0], world[:, 1])
        margin = allowed_radius(world[:, 2]) - radial
        min_margin = float(margin.min())
        state = "FAIL" if min_margin < -0.05 else ("WARN" if min_margin < args.warn_clear else "PASS")
        failed |= state == "FAIL"
        print(f"{item['label']:<34} {world[:,2].min():6.1f}..{world[:,2].max():6.1f}   "
              f"{min_margin:7.2f} mm  {state}")
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
