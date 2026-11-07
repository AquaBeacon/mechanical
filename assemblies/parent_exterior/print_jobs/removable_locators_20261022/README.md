# 後付け位置決め Rev.7：変更分5個の印刷

2026-10-22。印刷入口は[parts/PRINT.md](../../parts/PRINT.md)。**上側押さえ1個と脚2個は印刷済みで再印刷不要です。**
今回の変更分は下側プレート1個・左右レール各1個・前後アーム各1個。以下の3MFを各1回ずつ印刷します。カメラ・TD04A・QR等の未印刷部品はこの5ファイルには含みません。

X1 Carbon／0.4 mm／Bambu PETG Basic／Textured PEI Plate、0.20 mm層・8壁・100%充填。変更分合計 **772.1 g・17時間29分**。スライサー見積りで、実測ではありません。

| 3MF（各1個入り） | 見積り | 時間 | 支持材見積り |
|---|---:|---|---:|
| [下側プレート](parent_oneplate_frame/parent_oneplate_frame.3mf) | 695.2 g | 14時間52分 | 0.69 g |
| [左レール](parent_oneplate_box_locator_side_left/parent_oneplate_box_locator_side_left.3mf) | 12.2 g | 0時間31分 | 0.03 g |
| [右レール](parent_oneplate_box_locator_side_right/parent_oneplate_box_locator_side_right.3mf) | 10.5 g | 0時間38分 | 0.03 g |
| [固定側アーム](parent_oneplate_box_locator_end_fixed/parent_oneplate_box_locator_end_fixed.3mf) | 26.1 g | 0時間41分 | 0.35 g |
| [押し側アーム](parent_oneplate_box_locator_end_push/parent_oneplate_box_locator_end_push.3mf) | 28.1 g | 0時間47分 | 0.30 g |

支持材は5個の合計約1.41 gです。自動支持を45°・モデル上も許可したまま保存しています。支持材0の形状ではありません。平板下面のナット座天井、レールの縁、アームの補強部に少量残ります。支持材は六角穴・外側から除去でき、密閉された空洞へ閉じ込めていません。

![印刷姿勢と実支持材の位置](../../_work/images/removable_locators_20261022_supports.png)

## 印刷と組立

1. まず左右レールと前後アームを印刷し、支持材とブリムを取り除きます。ナット・ねじ頭・接触面に残さず、手持ちのM4金具が入ることを確認してください。
2. 下側プレートを下面を下に印刷。約696 g使うので残量750 g以上を目安にします。下面の六角穴内の支持材も除去してください。主プレートのブリム2 mm、他3 mmを保存済みです。
3. プレート下面から左右レール用のM4ナット4個を入れ、上からM4×20を4本でレールを固定します。ナット上面がポケット天井へ着座します。
4. プレート上面から前後アーム用のM4ナット4個を入れ、下からM4×25を4本でアームを固定します。指定のねじ先端は箱底より2.3 mm下です。
5. 既存の脚と上側押さえを取り付けます。箱を置く前に、ねじ先端と座面を確認してください。横押し調整ねじ・圧力パッドは既存方式です。

3MFはBambu Studioでプロジェクトとして開き、機種・ノズル・プレート・装填PETGの割当を確認します。保存した姿勢と設定を使い、支持材はOFFへ変更しないでください。実印刷・締結・強度・クリープは未確認です。

[元STLハッシュとスライス結果](validation.json)／[保存3MFと全層の経路検査](../../_work/analysis/removable_locators_20261022/slice_checks.json)／[組立とネジ指定](../../README.md)
