# 小型脱着治具・比較試作

**印刷入口: [parts/PRINT.md](parts/PRINT.md)**。このpartsフォルダだけコピーして印刷できる。[設計元の説明](../../parts/common/jigs/quick_release_prototypes/quick_release_prototypes.md)、配置の正本はplacement.json。

2026-09-28修正: A/Cの突出した固定側頭受けを廃止し、本体内へ固定ナットを埋め込んだ。右側を手回しボルトに変更。上向き開放の六角ポケットへナットを入れ、少量のエポキシで脱落防止する。締付力は本体壁で受ける。緑ノブが取付面を越えないよう上側板をA=10 mm、C=6 mm厚にした。下側板4 mm。Cの爪下面と回転溝天井を斜面化し、内部サポートを減らした。

| 案 | 構成 | 素手で解除 |
|---|---|---|
| A | 蟻溝＋押さえ、横M3×40、内蔵固定ナット | 約3回転緩め、押さえを外へ1 mmずらしスライド |
| B | 窓から片側1.5 mm出る爪、爪の機能は維持、外周フィレット追加 | 両爪をつまんで引く |
| C | 整列板、横M3×40、内蔵固定ナット | 約5.2回転でねじを外し、ノブ付きボルトを右へ抜き、時計回り60°戻して持上げ |

9種類9点。金具はM3×40六角ボルト2本、M3ナット2個、平ワッシャ2枚。旧CのM3×50は使わない。初回にナットとノブ内ボルト頭へエポキシを点付け、ねじ山に付けず硬化させる。右ワッシャは脱落防止式ではない。接着なしの固定ふたは含まない。金具寸法は仮定で実測が必要。

ノブ回転包絡と取付面の空間: A上側2 mm／下側1 mm、C上側2.5 mm／下側6 mm。側方の指用空間約10 mmとCボルト抜去約45 mmを別途確保する。A引出し約23 mm、B約40 mm、C持上げ約10 mm。厚くした取付板のM3ねじ長さは取付先に合わせる。

PETG、0.4 mmノズル、0.2 mm層、5周壁、上下6層、40% infillを仮比較条件とする。A押さえは外側X面を下、Bメスは入口を上。同梱STLは姿勢・接地済み。まずサポートOFFで短い橋と爪の初層を確認し、必要なら外側だけ局所サポート。ナットポケット・横穴・C回転溝内はサポート禁止。

```powershell
python tools/build_quick_release_prototypes.py --no-step
python tools/build_quick_release_prototypes.py --steps-only
python tools/preview_quick_release_trials.py
python tools/assembly_parts.py check
python tools/tidy_workspace.py check
```

[プレビュー](_work/images/comparison.png)、[C蓋裏のゴムくぼみ](_work/images/preview_C_pocket_empty.png)、[ゴム装着例](_work/images/preview_C_rubber_bond.png)、[形状・干渉](_work/analysis/verification.json)、[締結接触](_work/analysis/locking_verification.json)、[ゴムくぼみ・受け面](_work/analysis/pad_bond_verification.json)、[上下取付面の空間](_work/analysis/top_mount_clearance.json)、[取付穴](_work/analysis/mounting_verification.json)、[STEP](_work/analysis/step_verification.json)。銀色金具は理想形状表示で印刷一式に含めない。組立STL/STEPは印刷部品9点、STEPは面分割ソリッド。

閉メッシュ・寸法・離散経路・ナット挿入・取付穴・組立干渉を検査する。Aは摩擦依存、Cはカム溝とゴムパッドの圧縮で軸方向の遊びを詰める構成。強度、接着保持、実公差、疲労、操作力は未検証。無荷重10回→100回で緩み・ガタ・脱落・白化・亀裂を確認する。

[print_jobs](print_jobs/README.md)の3MFは旧形状の履歴。最新STLから再配置する。

外周フィレット追加: 取付板の縦角R3、上縁R0.8、ナット受け・C側面受け・Bメス外周の縦角R1、ノブ自由端R0.8。取付面と印刷底面は平坦、嵌合・係止面とM3穴は維持する。

組立時に上を向くオス板の反対側の縁も丸め、印刷底面は45°面取りへ接続した。Aメス本体と後端ストッパの露出縁も丸めた。

フィレット版の干渉・接触検査は、レンダリング済みの閉メッシュとplacement.jsonの締結配置を再利用する。金具形状と押さえの運動はSCAD、Bの変形包絡は従来のせん断近似を使う。

Cのゴムくぼみ（2026-10-01）: **5×8×1 mm×2**をCオス（蓋）下面の5.4×8.4×0.4 mmの開放くぼみに薄く接着する。各ゴムは0.6 mm突出し、固定位置ではメスの平らな上面に公称0.10 mm圧縮される。合計貼付面積80 mm²。カム引込み0.60 mm、終端の蓋下面Z=18.5、上側取付面Z=24.5。横M3を抜いてから60°戻す。Cは0.1 mm層で試作する。ゴムはプレビューのみで印刷9部品には含めない。貼付位置と調整方法は設計元を参照する。
