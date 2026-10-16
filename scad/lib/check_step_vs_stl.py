# check_step_vs_stl.py - 部品ごとの STEP と STL が同じ形・同じ座標系かを突き合わせる。
#
# アセンブリのプレビュー (OpenSCAD, STL を import) とアセンブリ STEP (asm_to_step.py,
# 各部品の STEP を合成) は同じ placement.json を使うので、部品の STEP と STL の
# 原点が違えば STEP 側だけ黙ってずれる。2026-09-02 に子機内装で発覚:
#   - Blue Robotics WTE4 系 (チューブ/フランジ/エンドキャップ) は STL が角原点、
#     STEP が断面中心原点で配布されていた (-> scad/lib/step_reframe.py で STL 側へ)
#   - hull()/teardrop を含む printed 部品は FreeCAD の CSG 取り込みで形が壊れていた
#     (-> csg_to_step.py が STL_REF と照合し、違えば STL->STEP フォールバック)
#
# 環境変数:
#   ASM_ROOT = リポジトリルート (必須)
#   ASM_JSON = 特定アセンブリの placement.json だけを見る (省略時は assemblies/*/placement.json 全部)
# Run: ASM_ROOT=... freecadcmd check_step_vs_stl.py
# NG が 1 つでもあれば exit 1。
import glob
import json
import os
import sys

import FreeCAD
import Mesh
import Part

BBOX_TOL = 0.5     # mm
VOL_TOL = 0.05     # 5 %

root = os.environ["ASM_ROOT"]
one = os.environ.get("ASM_JSON")
jsons = [one] if one else sorted(glob.glob(os.path.join(root, "assemblies", "*", "placement.json")))

seen = {}
for asm_json in jsons:
    asm = json.load(open(asm_json, encoding="utf-8"))
    aname = os.path.basename(os.path.dirname(asm_json))
    for it in asm.get("items", []):
        part = it["part"].strip("/").replace("/", os.sep)
        stem = it.get("file") or os.path.basename(part)
        seen.setdefault((part, stem), set()).add(aname)

ng = 0
for (part, stem), asms in sorted(seen.items()):
    d = os.path.join(root, part)
    sp = next((os.path.join(d, stem + e) for e in (".step", ".stp", ".STEP") if os.path.exists(os.path.join(d, stem + e))), None)
    tp = os.path.join(d, stem + ".stl")
    tag = "%-30s" % stem
    if sp is None or not os.path.exists(tp):
        print("[step-vs-stl] %s MISSING step=%s stl=%s   <- %s" % (tag, sp is not None, os.path.exists(tp), ",".join(sorted(asms))))
        ng += 1
        continue
    sh = Part.Shape()
    sh.read(sp)
    m = Mesh.Mesh(tp)
    # BoundBox は円筒面などで公差分ふくらむ (チューブで 1 mm)。optimalBoundingBox で実外形をとる
    try:
        bs = sh.optimalBoundingBox()
    except Exception:
        bs = sh.BoundBox
    bm = m.BoundBox
    dbox = max(abs(a - b) for a, b in ((bs.XMin, bm.XMin), (bs.YMin, bm.YMin), (bs.ZMin, bm.ZMin),
                                       (bs.XMax, bm.XMax), (bs.YMax, bm.YMax), (bs.ZMax, bm.ZMax)))
    # 基板 (KiCad 書き出し) は部品ソリッドが基板と重なっていて STEP の体積が合計値になるため
    # 体積では比べられない。外形だけ見る。
    is_pcb = (os.sep + "pcb" + os.sep) in (os.sep + part + os.sep)
    dvol = 0.0 if is_pcb else abs(sh.Volume - m.Volume) / max(m.Volume, 1e-9)
    bad = dbox > BBOX_TOL or dvol > VOL_TOL
    ng += int(bad)
    print("[step-vs-stl] %s %s bbox_maxdiff=%.2f vol_diff=%.1f%%%s   <- %s" % (
        tag, "NG" if bad else "ok", dbox, dvol * 100, " (pcb: bbox only)" if is_pcb else "", ",".join(sorted(asms))))
    sys.stdout.flush()

print("[step-vs-stl] %d part(s) checked, %d NG" % (len(seen), ng))
sys.stdout.flush()   # freecadcmd は sys.exit 時に最終行を落とすことがある
sys.exit(1 if ng else 0)
