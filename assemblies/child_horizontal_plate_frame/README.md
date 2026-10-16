# 子機・横向き耐圧容器の4枚フレーム

2026-10-12更新、Rev.4。左右側板2枚＋底板1枚＋上部1枚。前後の追加フレーム4枚は側板内側、ライトの一体型twist台座は段差なし。ライトを60°回して停止した位置で上向き、その横の水平ノブを締めて固定する。X1 Carbon / Bambu PETG Basicの嵌合・荷重試験用（fit_prototype）。

- [印刷入口・STLと数量](parts/PRINT.md)
- [配置・購入品の正本](placement.json)
- [組立表示用STL](child_horizontal_plate_frame.stl) / [全体SCAD](child_horizontal_plate_frame_view.scad) / [ライトSCAD](child_horizontal_plate_frame_light_view.scad)
- [基本フレーム設計元](../../parts/child/exterior/printed/child_horizontal_plate_frame/README.md)
- [取付規格 CHILD-HORIZONTAL-TWIST-C-R4](../../docs/child_horizontal_twist_interface.md)

SCADはOpenSCADで開きF5で確認する。全体ビューは `show_accessories=true` を生成時に定義。ライトビューは `pose="locked"` で固定位置、`pose="entry"` で横ボルトを抜いた差し込み位置、`show_frame=false` で治具だけを表示する。どちらも配置JSONから生成される。

![差し込み位置から上向きに回して固定](_work/images/side_twist_locked_entry.png)

固定時の照射軸は機体+Z、ノブ軸は水平+Y。ノブ中心(136,105.5,130)はライト軸(161,80)の横に来る。右外側から側板を見る向きで、差し込み位置から反時計回り60°で停止してからノブを締める。解除はノブ付き横ボルトを+Yへ45 mm抜き、時計回り60°で差し込み位置へ戻して外側へ抜く。

## 内側の追加フレームと段差のない台座

![内側の追加フレームと上向きライト](_work/images/side_twist_complete.png)

側板は左X−122〜−110、右X110〜122。厚8の前後延長は左X−110〜−102、右X102〜110へ置く。主フレーム244×230×230、保護延長込み244×350×230。上部フレームの接合座と後部回転止めの取付足には1 mmの設計逃げを設けた。guard_front_inner / guard_rear_innerを使い、旧外側延長は履歴用バリアントへ残す。

延長固定は既存Y±98・Z100/176穴、外側からM3×25、内側から普通ナットを工具で保持し、両側に0.5 mmワッシャ。側板の旧ナット受けは延長で覆われる。ねじ先端、ナット挿入、薄口スパナ、上部と回転止めの工具通路を実メッシュで検査する。

![内側取付の断面](_work/images/inner_side_extensions.png)

フレーム台座＋Cメス、ライト保持半割＋Cオスは各1個の一体部品。平坦な台座足24×84×4は側板外面X122に直接接し、twist中心はX122/Y80/Z130。固定は既存Y60/Z100・160の2穴にM3×18。ライト軸はX161/Y80、保持区間Z89.5〜170.5、既存内径33・保持長81のホルダーと押さえを流用し上向き照射。ホルダー突出は **68.5→59.5 mm**、最初のRev.1の123.5 mmから64 mm減る。

![中央の手の通路と突出の比較](_work/images/side_twist_comparison.png)

側面中央Y−45〜45、Z40〜210の外側の通路を空け、既存90×34の指通し穴と内側の手の予約領域を保つ。実ライトの頭部・操作部・ケーブル、手袋サイズは未モデル化。カメラとTD04AはCオスを機器治具へ直接組み込む規格を定め、機器側の寸法確定後に設計する。

## 印刷済みとこれから印刷するもの

トップフレームは2026-10-12に改良し、下にあるクランプの締付ねじ6本の真上へ工具穴を追加した。内接円径φ10、正12角形、両入口0.4 mm面取り。φ8×軸長70 mmの工具を想定し、トップフレームを取り外さず上から締められる。縁に近い2穴の周囲は少し広げ、既存の取付穴と接合座を保持する。工具の実寸は確認する。

![クランプ締付ねじ用の上側工具穴6か所](_work/images/top_clamp_access.png)

[工具穴・全長の進入・座面と肉厚の検査](_work/analysis/top_clamp_access/validation.json)。変更前の上部、組立と印刷データは[before_top_clamp_access履歴](_work/intermediate/history/before_top_clamp_access/)に保存した。トップフレームは従来と同じ向きで1個印刷する。

6本のφ8×70工具通路は全装着状態で合格。穴入口直近と中央の断面では最小肉厚約3.3 mm、既存8か所のクランプ取付ねじの座面材料は一致。トップは閉メッシュ・単一連結、実スライスのサポート押出0、PETG Basicで約291.77 g・6時間の見積り。変更していない9バリアントの頂点・外形・体積は[変更前との照合](_work/analysis/top_clamp_access/unchanged_parts.json)で一致し、全品の位置とねじ配置は保持した。

側板2枚・底板1枚・クランプ上下各1個、4種類5個は印刷済み。形状・配置・設計元STLのSHAを保持する。共通SCAD更新後は別出力の全頂点・外形・体積を照合して元のバイト列を保つ。

現構成17種類24個、未印刷13種類19個。基本フレームの未印刷15個は上部1、前後延長左右各1（計4）、回転止め左右各1（計2）、支持治具4、C押さえ4。追加ライトは一体メス・一体オス・既存押さえ・ノブの4種類各1個。鏡像STLは左右を区別する。

0.4 mmノズル、8壁、100%充填、5 mmブリム、Textured PEI。一体メス・オスは0.1 mm層、他は0.2 mm層。一体ライトオスだけベッドからの外部サポートを使用し、上下離隔0.2 mm、筒内に入れない。平坦なメスと基本フレーム・押さえ・ノブはサポート無効。製造姿勢は配布STLへ反映済みで、スライサ上で寝かせ直さない。

[現行スライス](print_jobs/x1c_petg_basic/validation.json)、[ライト部品の支持位置と積層](_work/analysis/side_twist_mount/slicing.json)、[全印刷条件検査](_work/analysis/print_verification/validation.json)。実スライスの設定・G-code・STLハッシュを照合する。初回印刷でブリッジ、サポート除去後の爪・カム・嵌合、ライト保持を確認する。

## 金具と組立

| 用途 | ねじ | 本数 | ナット |
|---|---|---:|---|
| 上クランプ→上部 | M3×18 | 8 | 印刷済み受け |
| 下クランプ→支持治具 | M3×25 | 8 | 印刷済み受け |
| クランプ上下締結 | M3×30 | 6 | 印刷済み受け |
| 底板→側板 | M3×25 | 4 | 印刷済み受け |
| 上部→側板 | M3×30 | 4 | 開放座、上から工具 |
| 支持治具→側板 | M3×25 | 16 | 開放座、側端から工具 |
| 回転止め→側板 | M3×25 | 4 | 開放座、+Yから工具 |
| 保護延長→側板 | M3×25 | 8 | 内向き面、前後端から工具 |
| C押さえ | M3×30 | 8 | 印刷済み底板の受け |
| Bプレート→底板 | M5×12 | 16 | 既存M5受け |
| 一体メス→側板 | M3×18 | 2 | 既存側板の受け |
| ライト半割 | M3×20 | 4 | 普通ナット、両側ワッシャ |
| twistロック | 六角頭M3×40 | 1 | 既存ノブとCの手順 |

現構成のねじ購入数量は下記の6種類・計89本（予備を含まない）。長さは首下寸法。通常固定はモデル上のなべ頭、twistロックだけ六角頭を指定する。カメラとTD04Aの未設計治具は含まない。

| ねじ | 合計本数 |
|---|---:|
| M3×18 | 10 |
| M3×20 | 4 |
| M3×25 | 40 |
| M3×30 | 18 |
| 六角頭M3×40 | 1 |
| M5×12 | 16 |
| 合計 | 89 |

2026-10-12集計：配置正本の88締結組と別モデルのtwistロック1本を照合した。C押さえのM3×25という旧説明は誤記で、配置と共通寸法の正しい値M3×30へ修正した。

基本フレームのM3ナット66個・φ7×0.5ワッシャ98枚、M5ナット16個・φ10×1ワッシャ16枚。追加ライト分はM3ナット7個・φ7×0.5ワッシャ11枚、5×8×1ゴム2枚。保護材はクランプEPDM厚1とC受け厚0.8が仮条件。

支持治具は厚8足、既存20×24穴配置・支持面Z75.2を保持。回転止めは厚8足・Y−98/Z122・142、公式蓋輪郭の隙間0.55と受け奥行7.1を保持する。上部接合座は厚12。未印刷部品のM3穴は内接円径3.5の八角形・入口0.3面取り、外形R2・縁0.6面取り。印刷済み部品の丸穴と既存ナット受けは保持する。

1. 底板のC2個とB4個を固定する。申告質量2.24 kgは在庫正本による。
2. 支持治具と回転止めを側板内面へ固定し、普通ナットを開放部から工具で押さえる。下クランプと底板を接合する。
3. 前後延長を側板内側へ固定する。上部と後部回転止めは延長の逃げへ収まる。
4. 蓋のM10穴の1つを真下へ向け、容器を上から載せ、上クランプと上部を固定する。既存蓋突起は180°対称で逆向きも入るため穴配列を合わせる。
5. 一体メスを固定してから、ライトを60°傾いた差し込み位置へ入れる。右外側から見て反時計回り60°で上向きに整列し、横の水平ノブを締める。解除は横ボルト全体を+Yへ45 mm抜き、時計回り60°で解除し外側へ抜く。独立した落下防止コードを機体へ掛ける。

下クランプの締め直しはBを外し底板φ9穴からφ8以下の工具を通す。C押さえは容器を外す。代替長M3×30（支持・回転止め・延長）、M3×40（上部）は検査対象とし、無制限の長ねじ使用は許容しない。

## 検証・再生成・履歴

[組立干渉・工具・ナット・手・配線](_work/analysis/layout/validation.json)、[開放ナット・八角穴・印刷済み形状](_work/analysis/open_nut_fastening/validation.json)、[容器挿入・回転止め・内側延長](_work/analysis/guards/functional_validation.json)、[ライトの金具・参考ゲージ・着脱](_work/analysis/side_twist_mount/validation.json)。開放ナットは基本フレーム32組、薄口スパナ包絡は頭幅10・厚2.6・到達35を仮定する。CAD検査は実荷重・層間強度・クリープ・実配線や工具の認証ではない。前端Y174は仮ドームから12.775 mm、後端Y−176は蓋外面Y−114から配線予約50＋余裕12。実ドーム、ケーブル曲げ半径、内装保持・浮力・重心は未確定。

`python tools/build_child_horizontal_accessories.py --rebuild-frame` で既存生成系から再ビルドする。メーカーCAD入力が同じ場合だけ `--reuse-interfaces` で計測結果を再使用できる（CADレンダリングは実行する）。ソース変更後の基本ビルダの `--reuse` は使用しない。`check_child_horizontal_open_nuts.py`、`check_child_horizontal_clamp_supports.py`、`check_child_horizontal_side_attachments.py`、`check_child_horizontal_ballast_mounts.py`、`check_child_horizontal_clamp_links.py`、`check_child_horizontal_guards.py`、`check_child_horizontal_accessories.py` を実行する。

続けて `python tools/check_child_horizontal_top_access.py` → `python tools/review_child_horizontal_accessories.py` → `python tools/assembly_parts.py sync child_horizontal_plate_frame` → `python tools/check_child_horizontal_clamp_links.py --portable-only` → `python tools/assembly_parts.py check child_horizontal_plate_frame`。スライスは `python tools/slice_child_horizontal_plate_frame.py`、その後 `check_child_horizontal_accessory_slices.py` と `check_child_horizontal_support_free.py`。STLは印刷用を納品し、全種類のSTEP読戻しは未完了。旧/未完了STEPは `_work/intermediate/step_export_incomplete/` に保持する。

Rev.2の生成元・配置・STL・文書・検査を[_work/intermediate/history/side_twist_r2/](_work/intermediate/history/side_twist_r2/)、3MFを[print_jobs/history/side_twist_r2/](print_jobs/history/side_twist_r2/)へ保存した。Rev.1と開放ナット・サポート変更前の履歴も保持する。

Rev.3の生成元・配置・STL・文書・検査は[_work/intermediate/history/side_twist_r3/](_work/intermediate/history/side_twist_r3/)、3MFは[print_jobs/history/side_twist_r3/](print_jobs/history/side_twist_r3/)へ保持する。Rev.4では全体SCADの未定義表示スイッチを生成元で修正し、固定・差込の2姿勢ビューを追加した。Cの面内角を30°から0°へ変更し、足とC底板の入り隅をR2に仕上げた。固定穴、嵌合機構、ライト保持形状を検査する。

今回の構成は印刷一式の出所検査に合格。全体検査には別構成child_interiorの未管理3MF、parent_oneplateとparent_service_reviewの出所変更が残る。[全体検査ログ](_work/logs/side_twist_r4_global_check.log)。共通テスト42件中1件はchild_wte4_suspension_clampの材料JSON欠落による既存エラー。今回の構成の検査記録は上記リンクを参照する。

Rev.3までの検証値は履歴へ保持する。既存ライト押さえの印刷コピーはASCII STLで精度を保持し、設計元STLは変更していない。Rev.4の現行STL・配置・スライスについては上記検査記録を参照する。

Rev.4検証結果：固定後の照射軸+Z・ノブ軸+Y、ノブ全周と半径3 mmの局所余裕、参考ゲージ、着脱回転・抜去、中央の手の通路は合格。C嵌合域の元メッシュとの体積差分はメス0.0307 mm³、オス0.00082 mm³以下。基本フレームの工具・ナット・延長・容器挿入も合格。全17種類24個の印刷コピーは閉メッシュ・単一連結、設計元との全頂点誤差最大1.33e−14 mm。未印刷13種類19個の現行スライスを照合し、一体メスのサポート押出0・橋の局所幅最大3.99 mm、一体ライトオスだけ外部サポートを使用する。追加ライト4個の見積りは82.80 g・約6時間13分（各1個の合計）。全体SCAD・ライトSCADの両姿勢を警告なしで表示した。

parts直下へ保存されていた `child_horizontal_plate_frame_guard_front.3mf` は [print_jobs/history/imported_20261012/](print_jobs/history/imported_20261012/) へ元のバイト列を保持して移動し、出所・設定・ハッシュを記録した。内容は支持治具4個と回転止め左右で、現行CADとの一致は未認定。この履歴を現行STLの代わりに使用しない。
