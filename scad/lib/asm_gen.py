# asm_gen.py - placement.json からアセンブリ確認用の OpenSCAD ビューを生成する。
#   python asm_gen.py <placement.json> <out_view.scad>
#
# placement.json がアセンブリの唯一の情報源。同じ JSON を asm_to_step.py が読んで
# STEP を書き出すので、配置を二重管理しない。
#
# items[] の各要素:
#   part  : リポジトリルートからの部品フォルダ (例 "parts/child/interior/printed/child_tray_deck")
#   file  : 部品フォルダ内のファイル名(拡張子なし)。省略時は部品フォルダ名。
#   ops   : 外側から順に適用する変換のリスト
#           {"translate":[x,y,z]} / {"rotate":[rx,ry,rz]} / {"mirror":[nx,ny,nz]}
#   color : OpenSCAD の色名 (プレビュー用。STEP には反映されない)
#   alpha : 0..1 の不透明度
#   note  : 生成 .scad にコメントとして出る説明
import json
import os
import sys


def fmt_vec(v):
    return "[" + ", ".join(("%g" % x) for x in v) + "]"


def ops_to_scad(ops):
    out = []
    for op in ops:
        for kind, val in op.items():
            if kind not in ("translate", "rotate", "mirror", "scale"):
                raise SystemExit("unknown op: %s" % kind)
            out.append("%s(%s)" % (kind, fmt_vec(val)))
    return " ".join(out)


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: asm_gen.py <placement.json> <out_view.scad>")
    src, dst = sys.argv[1], sys.argv[2]
    with open(src, encoding="utf-8") as f:
        asm = json.load(f)

    asm_dir = os.path.dirname(os.path.abspath(src))
    # <root>/assemblies/<name>/ から見たリポジトリルート
    root = os.path.dirname(os.path.dirname(asm_dir))
    up = os.path.relpath(root, os.path.dirname(os.path.abspath(dst))).replace(os.sep, "/") + "/"

    L = []
    L.append("// =====================================================================")
    L.append("// %s_view.scad" % asm.get("name", "assembly"))
    L.append("// !! 自動生成ファイル - 編集しないこと。placement.json を直して")
    L.append("//    build.ps1 -Assemblies で再生成する。")
    if asm.get("note"):
        for line in asm["note"].splitlines():
            L.append("// %s" % line)
    if asm.get("coordinate_system"):
        L.append("// 座標系: %s" % asm["coordinate_system"])
    L.append("// =====================================================================")
    L.append("")

    groups = asm.get("groups") or {}
    for g, default in groups.items():
        L.append("show_%s = %s;" % (g, "true" if default else "false"))
    if groups:
        L.append("")

    # OpenSCAD のプレビューは宣言順に描画し、半透明の物体を先に描くと、その奥に
    # 後から描いた不透明部品が (深度バッファで) 隠れて見えなくなる。
    # 2026-09-03 に容器 (alpha 0.22) を先頭に置いた child_interior で内装が全く写らなかった。
    # → 不透明 (alpha 無し / 1.0) を先、半透明を後 (alpha の大きい順) に並べ替えて出力する。
    items = list(asm.get("items", asm.get("parts", [])))
    def _alpha(it):
        a = it.get("alpha")
        return 1.0 if a is None else float(a)
    items = ([it for it in items if _alpha(it) >= 1.0] +
             sorted([it for it in items if _alpha(it) < 1.0], key=_alpha, reverse=True))
    for it in items:
        part = it["part"].strip("/")
        stem = it.get("file") or os.path.basename(part)
        path = "%s%s/%s.stl" % (up, part, stem)
        if it.get("note"):
            L.append("// %s" % it["note"])
        color = it.get("color")
        alpha = it.get("alpha")
        prefix = ""
        if color:
            prefix = 'color("%s"%s) ' % (color, (", %g" % alpha) if alpha is not None else "")
        body = "%s%s import(\"%s\");" % (prefix, (ops_to_scad(it.get("ops", [])) + " ").lstrip(), path)
        g = it.get("group")
        if g:
            body = "if (show_%s) %s" % (g, body)
        L.append(body)
    L.append("")

    os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
    with open(dst, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L))
    print("[asm_gen] wrote %s (%d items)" % (dst, len(asm.get("items", asm.get("parts", [])))))


if __name__ == "__main__":
    main()
