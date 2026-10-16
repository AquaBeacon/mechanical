# 親機内装：容器固定ねじ3本の工具アクセス

2026-10-12。ユーザー指定は「内装を組み付けたまま3本を操作、LiPo下は電池を外して操作、最下段の部品は変更しない」。北東の基板下の1本は使わず、M4×12低頭ボタンを南西・南東・北西に各1本使う。3点固定の耐荷重・波浪・クリープを認定したものではない。

最下段 `floor_plate` のSCAD・STEP・STLは変更前と同じSHA-256。4取付穴、ねじ座、ボス接触面、床格子、他の取付座とナット穴を維持した。部品配置と基板・電池の高さも維持する。

| ねじ | 箱座標XY mm | 操作条件 |
|---|---|---|
| 南西 | 25 / 25 | 全モジュールを取り付けたまま、長軸2.5 mmボールポイント六角レンチを南西へ10°傾けて差し込む |
| 南東 | 185 / 25 | 電源を切りリードを外す。蓋のねじ4本・電池蓋・LiPo・上面フォームを外し、電池台の工具穴へ垂直に差し込む。台と台固定ねじは外さない |
| 北西 | 25 / 205 | 全モジュールを取り付けたまま、同レンチを西へ10°傾けて差し込む |
| 北東 | 185 / 205 | TX/Sony基板下。ねじを入れない。床の既存穴は残す |

工具は有効軸長95 mm以上を想定。対辺2.5の六角軸の外接径2.887 mmに対し、直径3.5 mmの経路をZ110まで検査した。工具穴はØ4.2。ねじ頭は穴を通らないため、緩めたM4ねじは床板側に残る。ボールポイントの実先端、ソケットへの入り方、締付け操作とトルクは現物確認する。

## 変更する印刷部品

- `main_mount_plate`：南西工具経路の逃げ。入口と切欠き縁を0.15 mm面取り。基板穴・柱座・基板高さは維持。
- `battery_base`：LiPo下のØ4.2貫通工具穴。両入口0.2 mm面取り。床厚3 mm、電池の収納と着脱口、蓋・固定穴は維持。
- `ann_mb1_coax_ring`：南西工具穴と外径11.4 mmの囲い。口と囲い外周0.2 mm、長い縦の根元0.1 mm面取り。既存のM4ねじ頭下面逃げとリング／ラックのキー・4長ねじを維持。

**この3種類を各1個だけ再印刷する。床板の再印刷は不要。** 9種類各1個という印刷一式の構成は維持する。入口は [parts/PRINT.md](parts/PRINT.md)。設計元は既存 `spec/build_parent_hand_service.py`・`spec/build_parent_gnss.py`、工具条件は共通 `scad/lib/parent_case_access.py`。出力SCADを手編集しない。

同軸束は新しい囲いの外側へ収め、工具口の上にも糸・結び目・コードを置かない。巻き束の最大外径100、内孔75、高さ10 mmは維持し、囲い外周から0.2 mmを空ける局所領域を予約から除く。元の全周円環をそのまま巻ける形ではない。5 mを切らずに収められる容量、尾線とR20以上の曲げは実巻きで確認する。細い囲いへ同軸を巻き付けない。実ハーネスは未選定であり、今回の検査はモデルにある部品・配線包絡に限る。

## 検証と印刷

工具と床板不変の結果は [case_screw_access_checks.json](case_screw_access_checks.json)。変更3部品と他部品の干渉が変更前より増えていないことも照合した。CADの工具経路検査は物理的な操作試験ではない。

全変更部品は有効な1ソリッド／閉じたSTL。OpenSCADを独立レンダリングしSTEPの外形・体積と照合。記録は `scad_step_checks.json` と `_work/analysis/case_screw_access_20261012/mesh_checks.json`。確認画像は `_work/images/case_screw_access_top.png`、`case_screw_access_sw.png`、`case_screw_access_se.png`。表示用画像では南東の取り出し状態を示すためLiPo・蓋・上面フォームを非表示にしている。

PETG、X1C 0.4 mmノズル、0.2 mm積層、4周壁、100%インフィル。3部品とも既存の下面をベッドへ向ける姿勢を維持。自動支持を有効にし、45°閾値、ブリッジ除外でスライス成功。MAIN固定板は11.79 g／支持0 g、電池台は約45.15 g／支持約1.89 g、同軸リングは30.20 g／支持約0.50 g。支持は電池台のナット座などとリング下面・囲い付近で除去し、工具穴が開いていることを確認する。支持材除去と実印刷の成功は未検証。結果は `_work/analysis/case_screw_access_20261012/slicing/after_slicing.json`。

元の `parts/ann_mb1_coax_ring.3mf` は旧形状のため、モデルを変更せず `print_jobs/history_case_screw_access_20261012/` へ保管した。今回のスライスは検証用で、印刷入口のSTLを正本とする。

## 再生成

既存FreeCAD 1.0の `bin/python.exe` で以下を順に実行する。床板を作り直す `--floor-only` と全体生成は今回不要。

```text
spec/build_parent_gnss.py --case-access-only
spec/build_parent_hand_service.py --case-access-only
spec/refresh_parent_case_screw_meshes.py
spec/validate_parent_case_screw_revision.py
```

通常Pythonで `spec/slice_parent_simple_stack.py --case-screw-access after main_mount_plate battery_base ann_mb1_coax_ring`、`spec/render_parent_case_screw_access.py`、`tools/assembly_parts.py sync parent_hand_service`、`tools/assembly_parts.py check parent_hand_service` を実行する。最下段のバイト一致確認は検証コードと今回の変更前記録に対する確認であり、過去の強度評価を現行の3点固定へ適用するものではない。

全体検査の開始時には、他assemblyの旧ソース／未管理3MFと、子機材料カードの欠落による既存テストエラーがあった。今回の親機工具アクセスの結果と混同しない。詳細は同解析フォルダの `repository_checks.log`。

最終集約：7種の機能・組立検査がすべてPASS。連続組立経路は93項目PASS。斜め穴の面取りで通常BoundBoxがZ方向へ過大に広がるため、組立の保守的な囲いをoptimalBoundingBoxへ修正し再検査した。ガイド最小肉厚の寸法下限0.934 mm、隣のMAIN柱との公称隙間0.194 mmを確認。両組立STEPの配置照合、親機印刷一式の同期検査、画像・中間ファイルの配置検査もPASS。最終集約はvalidation_current.json。

電池蓋は同日の後続改訂で3爪＋ねじ1本へ変更した。蓋を南4 mm解除して上へ抜く。現在の蓋と電池台はbattery_slide_lid_report.mdを優先する。ここで記録した容器固定ねじ3本の工具姿勢と床板不変は維持。
