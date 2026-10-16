"""Summarize topopt/CalculiX output; use its own convergence judge per case."""
from pathlib import Path
import hashlib
import json
import re
from topopt.ccx import mesh_convergence

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/"parts/child/exterior/printed/child_wte4_suspension_clamp"
SUMMARY=PART/"_work/analysis/mount_ccx/series_summary.json"
REPORT=ROOT/"assemblies/child_clamp_suspension/STRENGTH.md"
LABELS={"static_1g_50percent":"偏荷重1g（締付け荷重なし）",
        "axial_4g_50percent":"軸方向4g（締付け荷重なし）",
        "preload_plus_static_1g":"締付け150 N/本＋偏荷重1g",
        "preload_plus_axial_4g":"締付け＋軸方向4g",
        "preload_plus_lateral_4g":"締付け＋横方向4g",
        "cap_axial_4g_to_clamp_bolts":"前半体から締結M3へ軸方向4g",
        "cap_pressure_plus_static_1g":"前半体の締付け圧力＋偏荷重1g",
        "cap_pressure_plus_axial_4g":"前半体の締付け圧力＋軸方向4g"}


def main():
    result=json.loads(SUMMARY.read_text(encoding="utf-8"))
    runs=result["runs"]
    supplement=PART/"_work/analysis/intermediate_3mm_ccx/ccx_summary.json"
    if supplement.exists():
        added=json.loads(supplement.read_text(encoding="utf-8"))
        assert added["stl"]==result["stl"] and added["study"]==result["study"]
        runs=runs+added["runs"]
    complete=[r for r in runs if r.get("cases") and
              all(c.get("max_disp_mm") is not None and c.get("safety_factor_p99_5") is not None
                  for c in r["cases"])]
    if not complete:
        raise RuntimeError("No complete solved mesh: do not report strength")
    last=complete[-1]
    study=json.loads((PART/"_work/analysis/study_mount.json").read_text(encoding="utf-8"))
    shape=PART/"child_wte4_suspension_clamp_half.stl"
    assert hashlib.sha256(shape.read_bytes()).hexdigest()==study["_part_sha256"],"Analysis STL changed"
    comparison=json.loads((PART/"_work/analysis/surface_remesh/geometry_comparison.json").read_text(encoding="utf-8"))
    assert comparison["pass_check"] and comparison["source_sha256"]==study["_part_sha256"]
    actual=Path(result["stl"])
    assert hashlib.sha256(actual.read_bytes()).hexdigest()==comparison["remeshed_sha256"]
    comparisons={}
    solved_comparisons={}
    for c in last["cases"]:
        series=[]
        for r in runs:
            rc=next(x for x in r["cases"] if x["case"]==c["case"])
            series.append(dict(target_mm=r["mesh_target_mm"],nodes=r["nodes"],max_disp_mm=rc.get("max_disp_mm"),
                               p99_5_stress_MPa=rc.get("von_mises_p99_5_MPa"),
                               hotspot_xyz_mm=(rc.get("hotspot") or {}).get("xyz_mm"),
                               max_stress_MPa=rc.get("von_mises_max_MPa")))
        comparisons[c["case"]]=mesh_convergence(series)
        solved_series=[s for s in series if s.get("max_disp_mm") is not None and s.get("p99_5_stress_MPa") is not None]
        solved_comparisons[c["case"]]=mesh_convergence(solved_series)
    deflection_ok=all(c["max_disp_mm"]<=study["max_deflection_mm"] for c in last["cases"])
    passed=all(r.get("pass") for r in runs) and all(c.get("pass") for c in comparisons.values()) and deflection_ok
    checks=dict(source=str(SUMMARY),cases=comparisons,solved_mesh_cases=solved_comparisons,pass_check=bool(passed),
                note="Uses installed topopt.ccx.mesh_convergence, no new convergence rule.")
    (PART/"_work/analysis/case_convergence.json").write_text(json.dumps(checks,indent=2)+"\n",encoding="utf-8")
    lines=["**弾性解析の判定: "+("合格" if passed else "未合格（詳細を下表と生データで確認）")+"。ゴムの滑り/クリープの実物判定は別途必要。**\n",
           f"下表の応力・変位は、全ケースの結果が得られた最後の **{last['mesh_target_mm']:g} mm** メッシュの値。未完了・欠損の細かい解析を合格値として扱わない。",
           "| ケース | p99.5相当応力 MPa | 最大相当応力 MPa | 異方性安全率p99.5 | 最悪局所安全率 | 最大変位 mm | ケース合否 | メッシュ収束 |",
           "|---|---:|---:|---:|---:|---:|---|---|"]
    for c in last["cases"]:
        lines.append(f"| {LABELS.get(c['case'],c['case'])} | {c['von_mises_p99_5_MPa']:.3f} | {c['von_mises_max_MPa']:.3f} | {c['safety_factor_p99_5']:.2f} | {c['worst_element_safety_factor']:.2f} | {c['max_disp_mm']:.4f} | {'PASS' if c['pass'] else 'FAIL'} | {'PASS' if comparisons[c['case']]['pass'] else 'FAIL'} |")
    lines.extend(["\n相当応力は表示用von Mises値。安全率は各方向の引張・圧縮・せん断を用いた最大応力則であり、相当応力に単一のPETG強度を割った値ではない。最悪局所は除外なしで記載。通常ケースのp99.5要求は5、全ケースの最悪局所下限は1.5。",
                  "\n| メッシュ目標 mm | 節点数 | 二次四面体数 | メッシュ品質 | 実行合否 |",
                  "|---|---:|---:|---|---|"])
    for r in runs:
        lines.append(f"| {r['mesh_target_mm']:g} | {r['nodes']} | {r['elements']} | {'PASS' if r['mesh_quality'].get('pass') else 'FAIL'} | {'PASS' if r.get('pass') else 'FAIL'} |")
    lines.extend(["\n既存topoptの収束判定（変位5%、p99.5応力10%、最大応力点の位置移動）を各ケースに適用した。最細2段階の値を比較する。",
                  "\n[CalculiX結果の集約と原本パス](../../parts/child/exterior/printed/child_wte4_suspension_clamp/_work/analysis/mount_ccx/series_summary.json) · [ケース別収束判定](../../parts/child/exterior/printed/child_wte4_suspension_clamp/_work/analysis/case_convergence.json)",
                  f"\n最大変位の仮基準 {study['max_deflection_mm']:g} mm: {'PASS' if deflection_ok else 'FAIL'}。変位には締付けによる初期変形も含む。",
                  "\n前半体も軸方向荷重と締付け圧力を検証した。ボルト/フレームの弾性、ゴムの接触非線形、経時・濡れたPETGは実物検証が残る。"])
    if supplement.exists():
        lines.extend(["\n[追加3 mm解析の生結果](../../parts/child/exterior/printed/child_wte4_suspension_clamp/_work/analysis/intermediate_3mm_ccx/ccx_summary.json)。成功した8/4/3 mmだけに同じ既存の収束判定を適用した参考結果は以下。失敗した2 mmを成功に置き換えたものではなく、最終精度の確認は未完了。",
                      "\n| ケース | 成功したメッシュ範囲のみの収束判定 |",
                      "|---|---|"])
        for name,check in solved_comparisons.items():
            lines.append(f"| {LABELS[name]} | {'PASS' if check['pass'] else 'FAIL'} |")
    content=REPORT.read_text(encoding="utf-8")
    content=re.sub(r"<!-- RESULTS_START -->.*?<!-- RESULTS_END -->",
                   "<!-- RESULTS_START -->\n"+"\n".join(lines)+"\n<!-- RESULTS_END -->",content,flags=re.S)
    REPORT.write_text(content,encoding="utf-8")
    print(json.dumps(checks,indent=2))
    raise SystemExit(0 if passed else 1)


if __name__=="__main__":
    main()
