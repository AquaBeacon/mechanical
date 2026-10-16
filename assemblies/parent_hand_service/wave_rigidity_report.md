> 履歴：2026-10-11の容器訂正前の形状・結果です。現行の床・台・支持位置の剛性根拠に使用しないでください。現行は[case_fit_report.md](case_fit_report.md)を参照。

# スペーサ積み上げ改訂の参考剛性解析

製造リリース・全体剛性保証は未成立。Sonyは実際の上台＋4本の印刷スペーサの接触面を理想接合して計算した。床は現行形状で再計算、MAINは形状一致を検証した前回解析。実ボルトの剛性・予圧・すべり・緩み、ケース／基板変形、樹脂クリープと実波浪は未検証。

暫定重力込み2gを±X/±Y/±Zへ適用。床搭載質量1510g、Sony基板40g、MAIN150gと実CAD自重。乾燥23℃の汎用直交異方性PETG、積層Z、0.2 mm・4周壁・100%インフィル、中実相当。従来のSD/USB20N、変位目標0.2 mm、SF3、最悪要素下限1.5を維持。Gmsh/CalculiX既存経路の3mm単一段階で、メッシュ密度収束は未認定。

| 現行モデル | 2g最大変位mm | 2gネイティブ判定 | 20N最大変位mm | 全ケースのネイティブ判定 |
|---|---:|---|---:|---|
| floor_plate | 0.16744 | PASS | — | PASS |
| main_carrier | 0.00988 | PASS | 0.19060 | PASS |
| sony_carrier | 0.06956 | PASS | 1.12878 | FAIL |

Sonyの20Nでは横方向の変位が約1.13 mmとなり0.2 mm目標を超え、一部ケースは最悪要素SFも下限未達。波2gの結果と20Nの結果を分けて表示し、強く押す操作の剛性保証へ転用しない。今回の4本スペーサ構成は操作・嵌合試作として扱い、実締結状態での操作と保持を測定する。

詳細・全ケース・未達は[print_rigidity_checks.json](print_rigidity_checks.json)と各ネイティブccx_summary.json。幾何一致は[wave_analysis_geometry_checks.json](wave_analysis_geometry_checks.json)。改訂前の壁付きモデルは`_work/analysis/simple_stack_20261010/history/`、ケース干渉を修正する前の床入力は`wave_rigidity_20261009/simple_stack/floor_plate`に履歴として保持し、現行床の解析へ使用しない。
