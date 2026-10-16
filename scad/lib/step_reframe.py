# step_reframe.py - ベンダ配布の STEP を、同梱 STL と同じ座標系へ平行移動して書き直す。
#
# Blue Robotics の WTE4 系は STL が「原点 = 角、断面中心 (57.15, 57.15)」なのに
# STEP は「原点 = 断面中心」で配布されている。placement.json は STL 基準で書いて
# あるので、そのままだと OpenSCAD プレビュー (STL) は正しく、アセンブリ STEP
# (asm_to_step.py) だけ部品がずれる。STEP を STL 側へ合わせるのが最小の修正。
#
# 環境変数で渡す (freecadcmd がファイル引数を「開く文書」扱いするため):
#   STEP_IN   = 入力 .step (ref/ の原本)
#   STEP_OUT  = 出力 .step (部品フォルダの正)
#   TRANSLATE = "dx,dy,dz"  [mm]
#   STL_REF   = (任意) 突き合わせる STL。頂点→STEP 表面距離を出して 0.1mm 超なら失敗
# Run: STEP_IN=... STEP_OUT=... TRANSLATE=... freecadcmd step_reframe.py
import os
import random
import sys

import FreeCAD
import Part


def log(*a):
    print("[reframe]", *a)
    sys.stdout.flush()


src = os.environ["STEP_IN"]
dst = os.environ["STEP_OUT"]
dv = [float(v) for v in os.environ["TRANSLATE"].split(",")]
ref = os.environ.get("STL_REF")

sh = Part.Shape()
sh.read(src)
b = sh.BoundBox
log("in :", os.path.basename(src), "bbox=[%.2f..%.2f, %.2f..%.2f, %.2f..%.2f]" % (b.XMin, b.XMax, b.YMin, b.YMax, b.ZMin, b.ZMax))
sh.translate(FreeCAD.Vector(*dv))
b = sh.BoundBox
log("out:", os.path.basename(dst), "translate=", dv,
    "bbox=[%.2f..%.2f, %.2f..%.2f, %.2f..%.2f]" % (b.XMin, b.XMax, b.YMin, b.YMax, b.ZMin, b.ZMax))

if ref:
    import Mesh
    m = Mesh.Mesh(ref)
    random.seed(1)
    pts = random.sample(list(m.Points), min(60, m.CountPoints))
    worst = max(sh.distToShape(Part.Vertex(FreeCAD.Vector(p.x, p.y, p.z)))[0] for p in pts)
    log("STL vertex -> STEP surface max dist = %.3f mm" % worst)
    if worst > 0.1:
        log("ERROR: STL と一致しない (平行移動だけでは合わない)。書き出しません。")
        sys.exit(1)

doc = FreeCAD.newDocument("reframe")
obj = doc.addObject("Part::Feature", os.path.splitext(os.path.basename(dst))[0])
obj.Shape = sh
doc.recompute()
Part.export([obj], dst)
log("wrote", dst)
