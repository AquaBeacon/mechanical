# asm_to_step.py - placement.json の配置どおりに各部品の STEP を読み込み、
# アセンブリ STEP (Fusion 360 で開ける B-Rep のまま) を書き出す。
# パスは freecadcmd がファイル引数を「開く文書」扱いするため環境変数で渡す:
#   ASM_JSON  = アセンブリの placement.json
#   ASM_ROOT  = リポジトリルート
#   STEP_OUT  = 出力する .step
# Run: ASM_JSON=... ASM_ROOT=... STEP_OUT=... freecadcmd asm_to_step.py
import json
import os
import sys

import FreeCAD
import Part


def log(*a):
    print("[asm2step]", *a)
    sys.stdout.flush()


asm_json = os.environ["ASM_JSON"]
root = os.environ["ASM_ROOT"]
dst = os.environ["STEP_OUT"]
group_filter = os.environ.get("ASM_GROUP", "").strip()

with open(asm_json, encoding="utf-8") as f:
    asm = json.load(f)


def m_translate(v):
    m = FreeCAD.Matrix()
    m.move(FreeCAD.Vector(float(v[0]), float(v[1]), float(v[2])))
    return m


def m_rotate(v):
    # OpenSCAD rotate([a,b,c]) == Rz(c)*Ry(b)*Rx(a) == FreeCAD.Rotation(yaw=c, pitch=b, roll=a)
    return FreeCAD.Rotation(float(v[2]), float(v[1]), float(v[0])).toMatrix()


def m_mirror(v):
    # 原点を通り法線 n の平面での鏡映: I - 2*n*n^T/(n.n)
    n = [float(x) for x in v]
    d = n[0] ** 2 + n[1] ** 2 + n[2] ** 2
    if d == 0:
        return FreeCAD.Matrix()
    a = [[(1.0 if i == j else 0.0) - 2.0 * n[i] * n[j] / d for j in range(3)] for i in range(3)]
    return FreeCAD.Matrix(a[0][0], a[0][1], a[0][2], 0,
                          a[1][0], a[1][1], a[1][2], 0,
                          a[2][0], a[2][1], a[2][2], 0,
                          0, 0, 0, 1)


def m_scale(v):
    return FreeCAD.Matrix(float(v[0]), 0, 0, 0,
                          0, float(v[1]), 0, 0,
                          0, 0, float(v[2]), 0,
                          0, 0, 0, 1)


BUILDERS = {"translate": m_translate, "rotate": m_rotate, "mirror": m_mirror, "scale": m_scale}


def total_matrix(ops):
    # OpenSCAD は外側の変換から順に入れ子になる → 記載順に右から掛けていく
    m = FreeCAD.Matrix()
    for op in ops or []:
        for kind, val in op.items():
            if kind not in BUILDERS:
                raise RuntimeError("unknown op: %s" % kind)
            m = m.multiply(BUILDERS[kind](val))
    return m


def is_rigid(m, tol=1e-6):
    """回転+平行移動だけ (鏡映・スケールなし) か。3x3 部分が正規直交で det=+1。"""
    a = [[m.A11, m.A12, m.A13], [m.A21, m.A22, m.A23], [m.A31, m.A32, m.A33]]
    for i in range(3):
        for j in range(3):
            dot = sum(a[i][k] * a[j][k] for k in range(3))
            if abs(dot - (1.0 if i == j else 0.0)) > tol:
                return False
    return abs(m.determinant() - 1.0) < tol


# Native in-process CAD pipelines may provide already validated source shapes
# (for example immediately after STL-to-STEP export). Ordinary CLI runs start
# with an empty cache and retain the existing file-loading behaviour.
_shape_cache = globals().get('_shape_cache', {})


def load_shape(part_dir, stem):
    """部品フォルダから STEP を優先して読む。無ければ STL をメッシュ→ソリッド化。"""
    for ext in (".step", ".stp", ".STEP"):
        p = os.path.join(part_dir, stem + ext)
        if os.path.exists(p):
            key = (os.path.normcase(os.path.abspath(p)), os.stat(p).st_mtime_ns)
            if key not in _shape_cache:
                _shape_cache[key] = Part.Shape(Part.read(p))
            # Separate topology/location, sharing immutable geometry. Each
            # instance receives its own placement; dense cage STEP imports
            # should run once rather than once for each identical half.
            return _shape_cache[key].copy(False, False), p
    for ext in (".stl", ".STL"):
        p = os.path.join(part_dir, stem + ext)
        if os.path.exists(p):
            import Mesh
            mesh = Mesh.Mesh(p)
            sh = Part.Shape()
            sh.makeShapeFromMesh(mesh.Topology, 0.05)
            # Closed STL references must be STEP solids too. Leaving a shell
            # here makes the exported product disappear from solid-only checks.
            try:
                candidate = Part.makeSolid(sh)
            except Exception:
                candidate = None
            if candidate is not None and candidate.isValid():
                sh = candidate
            else:
                solids = []
                for shell in sh.Shells:
                    if not shell.isClosed():
                        raise RuntimeError("STL reference has an open shell: %s" % p)
                    solid = Part.makeSolid(shell)
                    if not solid.isValid():
                        raise RuntimeError("STL reference solid is invalid: %s" % p)
                    solids.append(solid)
                sh = Part.makeCompound(solids)
            expected_volume = abs(mesh.Volume)
            relative_error = abs(abs(sh.Volume) - expected_volume) / max(expected_volume, 1e-12)
            if not sh.isValid() or not sh.Solids or relative_error > 0.0025:
                raise RuntimeError("STL reference STEP conversion changes volume: %s (%g)" % (p, relative_error))
            log("  (STEPが無いのでSTLから生成:", os.path.basename(p), ")")
            return sh, p
    return None, os.path.join(part_dir, stem)


doc = FreeCAD.newDocument("assembly")
made, missing = 0, []

for it in asm.get("items", asm.get("parts", [])):
    if group_filter and it.get("group", "") != group_filter:
        continue
    part = it["part"].strip("/").replace("/", os.sep)
    stem = it.get("file") or os.path.basename(part)
    part_dir = os.path.join(root, part)
    shape, tried = load_shape(part_dir, stem)
    if shape is None or shape.isNull():
        missing.append(os.path.relpath(tried, root))
        continue
    label = it.get("label") or stem
    mat = total_matrix(it.get("ops"))
    if is_rigid(mat):
        # 平行移動+回転だけなら面の幾何を作り直さない (transformGeometry は再構成で
        # "Geom_RectangularTrimmedSurface::U1==U2" を出すことがある。2026-09-02 に
        # 再フレームした WTE4 ベンダ STEP で発生)
        shape.transformShape(mat)
    else:
        try:
            shape = shape.transformGeometry(mat)
        except Exception as e:
            log("ERROR: %s: transformGeometry failed (%s)" % (label, e))
            raise
    obj = doc.addObject("Part::Feature", "p%03d" % made)
    obj.Label = label
    obj.Shape = shape
    made += 1

doc.recompute()

if missing:
    log("MISSING (先に build.ps1 で部品をビルドしてください):")
    for m in missing:
        log("   -", m)

if made == 0:
    log("ERROR: 配置できた部品が 0 個。STEP は書き出しません。")
    sys.exit(1)

# Part.export はラベルを捨てて「Open CASCADE STEP translator 7.8 N」という無名ボディ
# 2000 個超になり Fusion で部品を選べない。Import.export は Label を STEP の製品名に
# 書き、複数ソリッドの部品 (基板) は同名のグループにまとめる。
import Import
Import.export(doc.Objects, dst)
log("wrote", dst, "parts=", made, "missing=", len(missing))
