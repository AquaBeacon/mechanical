# verify_asm_step.py - 書き出したアセンブリ STEP の各部品が placement.json どおりの
# 位置にあるかを検証する。「プレビュー PNG (STL) は正しいのに Fusion で開いた STEP
# だけずれている」を機械的に捕まえる (2026-09-02 の子機内装で発覚)。
#
# 期待値: 各部品の STL を placement.json の行列で移した bbox
# 実測値: アセンブリ STEP を読み戻した各オブジェクトの bbox (ラベルで対応付け)
#
# 環境変数: ASM_JSON / ASM_ROOT / STEP_IN
# Run: ASM_JSON=... ASM_ROOT=... STEP_IN=... freecadcmd verify_asm_step.py
import json
import os
import re
import sys

import FreeCAD
import Import
import Mesh
import Part

TOL = 0.5  # mm

asm_json = os.environ["ASM_JSON"]
root = os.environ["ASM_ROOT"]
step_in = os.environ["STEP_IN"]

# asm_to_step.py と同じ行列合成 (あちらは import 時に実行されるので関数だけ複製)


def m_translate(v):
    m = FreeCAD.Matrix()
    m.move(FreeCAD.Vector(float(v[0]), float(v[1]), float(v[2])))
    return m


def m_rotate(v):
    return FreeCAD.Rotation(float(v[2]), float(v[1]), float(v[0])).toMatrix()


def m_mirror(v):
    n = [float(x) for x in v]
    d = n[0] ** 2 + n[1] ** 2 + n[2] ** 2
    if d == 0:
        return FreeCAD.Matrix()
    a = [[(1.0 if i == j else 0.0) - 2.0 * n[i] * n[j] / d for j in range(3)] for i in range(3)]
    return FreeCAD.Matrix(a[0][0], a[0][1], a[0][2], 0, a[1][0], a[1][1], a[1][2], 0,
                          a[2][0], a[2][1], a[2][2], 0, 0, 0, 0, 1)


def m_scale(v):
    return FreeCAD.Matrix(float(v[0]), 0, 0, 0, 0, float(v[1]), 0, 0, 0, 0, float(v[2]), 0, 0, 0, 0, 1)


BUILDERS = {"translate": m_translate, "rotate": m_rotate, "mirror": m_mirror, "scale": m_scale}


def total_matrix(ops):
    m = FreeCAD.Matrix()
    for op in ops or []:
        for kind, val in op.items():
            m = m.multiply(BUILDERS[kind](val))
    return m


def bbox_of_points(pts):
    xs = [p.x for p in pts]; ys = [p.y for p in pts]; zs = [p.z for p in pts]
    return (min(xs), max(xs), min(ys), max(ys), min(zs), max(zs))


asm = json.load(open(asm_json, encoding="utf-8"))

# 期待 bbox
expected = {}
for it in asm.get("items", asm.get("parts", [])):
    part = it["part"].strip("/").replace("/", os.sep)
    stem = it.get("file") or os.path.basename(part)
    tp = os.path.join(root, part, stem + ".stl")
    if not os.path.exists(tp):
        continue
    m = Mesh.Mesh(tp)
    mat = total_matrix(it.get("ops"))
    pts = [mat.multVec(FreeCAD.Vector(p.x, p.y, p.z)) for p in m.Points]
    expected[it.get("label") or stem] = bbox_of_points(pts)

# 実測 bbox。Import.export で書いた STEP は Label が製品名として戻る。
#  - 複数ソリッドの部品 (基板、2 ピースのリブ) は App::Part グループになり、その Name が
#    ラベル (英数字以外は '_')。子の Label は "tray_rib_002" のように末尾の数字が
#    付け替えられて当てにならないので、グループの Shape で bbox をとる。
#  - 単一ソリッドの部品は素の Part::Feature で、Label がそのまま残る。
doc = FreeCAD.newDocument("verify")
Import.insert(step_in, doc.Name)


def bbox_of_shape(sh):
    try:
        b = sh.optimalBoundingBox()
    except Exception:
        b = sh.BoundBox
    return (b.XMin, b.XMax, b.YMin, b.YMax, b.ZMin, b.ZMax)


def sanitize(s):
    return re.sub(r"[^A-Za-z0-9_]", "_", s)


by_name = {sanitize(label): label for label in expected}
actual = {}
grouped = set()
for o in doc.Objects:
    if o.TypeId == "App::Part" and o.Name in by_name:
        sh = getattr(o, "Shape", None)
        if sh is not None and not sh.isNull() and sh.Solids:
            actual[by_name[o.Name]] = bbox_of_shape(sh)
            grouped.update(c.Name for c in o.OutList)
for o in doc.Objects:
    if o.TypeId != "Part::Feature" or o.Name in grouped:
        continue
    sh = getattr(o, "Shape", None)
    if sh is None or sh.isNull() or not sh.Solids:
        continue
    if o.Label in expected and o.Label not in actual:
        actual[o.Label] = bbox_of_shape(sh)

ng = 0
for label, e in expected.items():
    a = actual.get(label)
    if a is None:
        print("[verify-asm] %-28s MISSING in STEP" % label); ng += 1; continue
    d = max(abs(x - y) for x, y in zip(e, a))
    bad = d > TOL
    ng += int(bad)
    print("[verify-asm] %-28s %s maxdiff=%.2f  expect=[%.1f..%.1f, %.1f..%.1f, %.1f..%.1f]  step=[%.1f..%.1f, %.1f..%.1f, %.1f..%.1f]"
          % ((label, "NG" if bad else "ok", d) + tuple(e) + tuple(a)))
    sys.stdout.flush()

print("[verify-asm] %d item(s), %d NG" % (len(expected), ng))
sys.stdout.flush()   # freecadcmd は sys.exit 時に最終行を落とすことがある
sys.exit(1 if ng else 0)
