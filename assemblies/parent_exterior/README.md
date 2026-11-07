## 2026-10-29 素手で着脱するカメラ接続（試作・現行）

カメラ1台分の新しい印刷品は、共通カメラ本体1個、その機体用の受け1個、指掛け付きUスペーサ2個、手回しノブ2個、ノブ蓋2個。前側押さえは後続の右5 mm追加移動で更新。フレーム・ガード・ライトは維持。変更した本体と押さえは `print_jobs/camera_clamp_right5_20261029/`、受けと手回し部品は `print_jobs/camera_hand_release_20261029/` を参照する。購入金具は各機に六角頭M3×30 2本（頭部二面幅5.5 mm・厚さ2 mmを仮定）とM3普通ナット2個。従来のソケットねじ・ワッシャはこの接続に使わない。部品の入手状態と現物寸法は未確認。

初回のみ受けを既存フレームに固定し、各ねじをノブ上側から通して蓋を押し込み、六角頭を囲む。蓋の突起は保持用で、締付力はねじ頭→ノブの厚1 mmの印刷床→カメラ耳→Uスペーサ→受け→ナット屋根で受ける。初回の受け固定には工具が必要。ノブ床の強度、クリープ、蓋の弾性と繰り返し保持は未検証。蓋は中央円盤に4本の弧状アームを持つ。アームを長さ約6.8 mm・幅1.75 mmの直線片とみなし、先端を0.15 mm曲げた簡易見積りは表面ひずみ約0.9%であり、曲がった実形状や積層を含む強度解析ではない。

通常の取外しはカメラを支え、各ノブをねじ山が外れるまで緩める。必要に応じてノブを約0.5 mm持ち上げ、頭の座面が約3.8 mm上がった状態にする。先にUスペーサの指掛けをつまんで接続座標の−Xへ抜き、次に各ねじ・ノブを受けの外側へ横に滑らせて外す。その後カメラを60°回して軸方向に引き抜く。取付は逆順で、カメラを回してからねじを横から入れ、スペーサを入れてノブを手で締める。落下防止コードを別に取り付ける。

親子の実メッシュで、接触・ナット反力・ノブの六角回り止め・蓋の引抜き障害と、上記の離散位置を検査した。指先φ9 mmからφ16 mmへ広がる長さ25 mmの指2本を同時に仮定した進入・引抜きも検査した。手全体、連続掃引、実物寸法、濡れた手での操作、締付力、振動・強度・爪の耐久は未認定。ケース幅95 mmは仮値、厚さ41 mmは既存実測値。特に解除途中のノブと仮ケースのZ方向すきまは約0.4 mmのため、現物の形状と寸法で確認する。詳しい結果は `_work/analysis/clamp_right5_20261029/geometry_hand_checks.json`。既存節の数値・94項目等は旧版の履歴であり今回に流用しない。

## 履歴：2026-10-29 工具締付け版（上記の素手着脱版に置換）

**履歴：この節は前側押さえの追加移動前の工具締付け版。** 各機で共通カメラ本体1個、専用受け1個、Uスペーサ2個を交換する。旧カメラの3MFを使わない。全機体のSTL一覧と今回の交換分を混同しない。

親機外装の40×40 mm取付穴、受け背面、カメラの配置は維持する。外装プレートの加工・再印刷は不要。既存受けを新しい受けへ交換する。

回転後、Uスペーサ2個を差し込み、M3×30ソケット2本・外径7×厚0.5 mmワッシャ2枚・M3普通ナット2個で接合面を締め付ける。旧横ロックねじ・ノブ・ゴム2枚は廃止。解除はカメラを支え、両ねじとワッシャを外し、スペーサを接続座標−Xへ14 mm以上抜いてから60°回して引き抜く。独立落下防止コードを使用する。

[設計寸法・締結経路・組立手順](../../parts/child/exterior/printed/dji_osmo_action6_mount_m3/README.md)。ケース厚さ41 mmのみ実測、幅95 mm・高さ75 mmなどは既存仮値。仮ケースと直径8 mm工具の横方向余裕は0.5 mm。実物で工具が通ることと接触位置を確認する。

### 検証状況

最終R1の正式STLで、閉メッシュ・単一連結、両機の静止干渉、接触座面、ナットの回り止めと引抜き反力、横挿入の掃引包絡、ねじのかかりと底付き、子機4点の締結経路、工具通路、スペーサ抜去と回転解除を検査し94項目PASS。非カメラSTL90件は作業前SHA-256と一致。回転は5°刻み、スペーサ抜去は0.5 mm刻みのサンプル検査であり、連続すきまの保証ではない。実物の締結力・濡れた状態の保持・クリープ・疲労・強度は未認定。

[機械可読検査結果](../child_horizontal_plate_frame/_work/analysis/camera_fixture_20261029/fixture_checks.json) / [設計条件](../child_horizontal_plate_frame/_work/analysis/camera_fixture_20261029/design_contract.json)。STEP・スライス・印刷セットの最終検査状況はこの節末の納品記録を参照。

### 再生成

共通治具：`python spec/build_camera_mount_m3.py --twist-only`。子機受けは既存SCADの`part="camera_receiver"`をレンダー、親機受けは既存`qr_source()`から生成してfemaleをレンダーする。旧`spec/configure_camera_twist.py`は廃止。配置は`python spec/configure_camera_fixture_clamp.py`、検査は`python spec/verify_camera_fixture_clamp.py`、STEPと組立は`python spec/export_camera_fixture_clamp.py`。変更しない既存バリアントは同値再レンダーで元のSTLバイト列を維持する。最後に対象assemblyの`tools/assembly_parts.py sync`と`check`を行う。

印刷入口：[parts/PRINT.md](parts/PRINT.md)。カメラ本体は底板下、受けは取付面下、スペーサは平面下。Generic PETG・0.1 mm・6壁・15% Gyroidを検証条件とする。カメラ裏側・C爪の支持材、受けナット溝屋根のブリッジを確認し、機能面を傷つけず支持材を除去する。

### 納品検査（2026-10-29）

変更4形状のSTEPは保存後に再読込し、全て有効な1ソリッド、STLとの外形差0.01 mm未満・体積差0.0025未満を確認。[STEP照合](../child_horizontal_plate_frame/_work/analysis/camera_fixture_20261029/step_checks.json)。親機全体STEPは107配置・0 NG、両機の組立STLと確認SCADを更新済み。

X1C／0.4 mm／Generic PETG／0.1 mm／6壁／15% Gyroid／自動支持（ベッドのみ）で4形状をスライスし、警告なし・造形域内。壁・支持・ナット溝屋根前後の層を確認した。スペーサは支持検出を有効にして支持0。これは実印刷の成功保証ではない。親受けの張り出し下面とカメラ裏側の支持材を除去し、ナット挿入溝と締結面を確認する。

[今回のスライス記録](print_jobs/camera_fixture_clamp_20261029/README.md)。3MFは1形状1個ずつ。スペーサは各機2個、両機で計4個必要。共通カメラ本体は両機で計2個必要。旧3MFは履歴として保持する。

対象2構成の印刷一式の出所・個数・更新状態はPASS。workspace整理検査もPASS。全体チェックには今回触れていない親機内装系6構成の既存未同期が残る。tools/testsは42件中41件PASS、既存材料カード`child_wte4_suspension_clamp/spec/bambu_petg_basic_material.json`欠落による1件ERROR。今回の治具検査とは分けて扱う。

![治具の取付状態](_work/images/camera_fixture_20261029_installed.png)

---

## 2026-10-29 カメラ前側押さえの追加移動

前側L字押さえと本体取付床・M4穴を正面から右へさらに5 mm移動。局所座標の接触帯 X=5.5..30.5、M4軸 X=11.5, 24.5。M5爪への干渉を避けるため足に局所逃げを設ける。カメラ姿勢と素手で着脱する回転接続は維持。変更した本体・押さえの3MFは print_jobs/camera_clamp_right5_20261029/、それ以外は従来の手操作版を使う。実物での締付け・保持・干渉は未確認。

## 2026-10-26 カメラ押さえ（履歴：下記の右5 mm追加移動で置換）

現行の印刷一式は13種類16個。

背板に追加していた四角い突出パッドを撤去。元の背板を後側の当たり面とし、前側押さえも位置を合わせて41 mmの間隔を維持する。実物のM5軸からケース背面までの距離は未測定。実測厚さ41 mmに合わせ、幅25 mmの前側押さえと取付穴・ねじを正面から見て右へ12 mm移動。左端から12〜37 mmの範囲を前後で挟む。中央M5固定爪と横方向に2.85 mm離し、20 mm移動版の足の切欠きは廃止。camera_mount_twist本体1個とcamera_front_clamp前側押さえ1個へ更新。追加はM4×16ソケット2本、M4ナット2個、外径9×厚0.8 mmワッシャ2枚。前側のL字足をカメラ下側へ反転し、元の左右底面受けを撤去。前方への張り出しは16 mm短縮。前側は0..3 mm開けて位置合わせし、下面からM4ねじを締める。ねじ頭とワッシャは底面に埋め込み、ナットは足の上側へ入れる。R1外縁・R3根元フィレット付き。背面下側20 mmの逃げを維持する。

[寸法・締結経路・印刷・検証](../../parts/child/exterior/printed/dji_osmo_action6_mount_m3/README.md)。ケースの幅・高さ・M5軸からの位置は既存仮値で、実物の新方式の保持力は未認定。親子共通2部品の印刷ジョブはparent_exterior/print_jobs/camera_clamp_clearance_20261026/。印刷入口はparts/PRINT.md。旧カメラ用3MFは使わない。

## 2026-10-25 カメラ旧版の実物評価（履歴）

2026-10-24版は実物で十分に回転を止められなかった。旧版の再印刷指示は取り消し、上記の前後押さえ方式へ更新した。

## 2026-10-25 TD04A固定治具 Rev.6（現行）

TD04A改訂時点の印刷一式は12種類15個。共通治具をM4・12 mmピッチ（実測前）、穴列基準でケーブル逃げ60 mmへ更新。親機は送受信面下向き、子機は上向き。旧TD04Aモデルは使用しない。[設計・ねじ・未確認事項](../../parts/common/exterior/printed/td04a_bracket_mount/README.md)。現行データはparts/PRINT.md。下記の旧TD04A支持・押さえ金具の記述と古い全体個数は今回の配置に適用しない。実物の耳厚・正確なピッチ・本体・配線根元・締結・強度は未検証。

# 親機外装・後付け位置決めプレート Rev.7

## 2026-10-24 カメラ底面受けの更新（旧版）

カメラ背面下側の突起に対し、左右受けを背面から20.5 mm前方へ退避した共通camera_mount_twistへ更新。背板・C接続・M5軸・配置は維持。カメラ治具1個を再印刷する。左右受けの範囲で床上Z=8..36.5の背面20 mm空間を確保し、中央M5爪と床は残す。実ケースの突起高さ・幅、接触と締結・回転保持力・強度は未検証。

[寸法と検証の詳細](../../parts/child/exterior/printed/dji_osmo_action6_mount_m3/README.md)。2026-10-21のカメラ3MFは旧形状の履歴。現行STLはparts/内を使い、新しい共通カメラ3MFは親機のprint_jobs/camera_bottom_clearance_20261024/に保存する。下記の旧カメラの支持位置・スライス時間・質量は今回の結果に適用しない。


2026-10-22。防水容器の下側プレートから位置決め部を分離し、左右レール2個・前後アーム2個を後からねじ止めする方式へ変更。配置の正本は[placement.json](placement.json)、印刷入口は[parts/PRINT.md](parts/PRINT.md)。全体は13種類16個。

**上側押さえ1個と脚2個は印刷済み。形状と配置を維持し、旧印刷データとの形状差0を確認した。再印刷は不要。今回変更した印刷物は下側プレート1個と位置決め部4個の計5個。** カメラは2026-10-21の小型・Cオス一体型を継続し、別体オス・旧角度ストップを追加しない。

parts/に保存されていた上側押さえと脚の3MFは、3部品とも回転・平行移動を除いて現行STLと一致することを照合し、[印刷済みジョブの履歴](print_jobs/printed_upper_and_skids_20261021/README.md)へ原本のまま移動した。元の保存層厚0.28 mmは保持する。

## 下側プレートと後付け位置決め部

主プレートはタブ込み240×134×20 mmの平板。三点支持Z=0、主面Z=-0.8、下面Z=-20、既存のM5全ねじ穴・カメラCメス・TD04A・ロープ穴と予備M4穴15箇所は維持する。元の一体アームや柱はプレートに残さない。

![下側プレート単体](_work/images/removable_locators_plate.png)

| 別体部品 | 個数 | プレートへの固定 | ナットの装着 |
|---|---:|---|---|
| 左右レール | 各1 | M4×20ソケット 各2本・上から | プレート下面の六角ポケット、脚より先に挿入 |
| 前後アーム | 各1 | M4×25ソケット 各2本・下から | プレート上面の六角ポケット、箱を載せる前に挿入 |

取付用は合計M4×20が4本、M4×25が4本、M4普通ナット（二面幅7・厚3.2 mm）が8個。左右のねじ座面Z=1.3、ナット上面Z=-12.3、ねじ先端Z=-18.7で、脚上面Z=-20に対し1.3 mmの隙間。下面から入れたナットを六角穴の天井で受けるため、締付時に上へ抜けない。

前後アームは厚12 mm、下面Z=-32・プレートとの接触面Z=-20。ねじ頭座面Z=-27.3、ナット底Z=-7.3、先端Z=-2.3で箱底へ出ない。固定端Y=115、左側基準X=-105、押しねじの位置と既存圧力パッド3個は維持する。横方向の押しねじは位置調整用で、上記8本の取付ねじとは別。

左右レールは長さ98 mmの一体部品。ロープ穴の外周を回る約3.2 mm以上の背骨を設け、小さな分断片を作らない。前後アームも小片へ分割せず、根元の丸め・補強を維持する。箱・カメラ・TD04Aを外し、ナット・位置決め部を締結してから脚と箱を装着する。既存の脚を加工する必要はない。

今回の5個の3MF・材料・設定・STLハッシュは[変更分の印刷ジョブ](print_jobs/removable_locators_20261022/README.md)。旧Rev.6主プレートの3MFを新しい平板として使わない。

![位置決め部をねじ止めした状態](_work/images/removable_locators_20261022_assembled.png)

今回の5個はX1C・0.4 mm・PETG Basic・0.2 mm層・8壁・100%充填。前後アームはY=90°で側面を下、左右レールと平板は底面を下。45°の自動支持を有効・モデル上も許可した検査では、ナット穴・通し穴と縁/補強部に少量の支持材が残る。印刷ジョブに実経路の図と見積りを記載する。箱・脚を付ける前に穴内と座面から除去する。全品支持材0という条件ではない。

![下面のカメラ接続](_work/images/camera_twist_underside.png)

## カメラの接続とネジ

- 印刷するカメラ部品はcamera_mount_twist.stl。60×60×厚6 mmの接続板とCオスを一体化し、旧別体QRオス、M3×14ねじ4本・ナット4個を省く。左右受けは上記の前方位置へ更新し、M5軸とC接続位置は保持する。元の背面M3穴には取付ねじを追加しない。
- Cメスは現行主プレートの40×40 mm穴へM3×25・M3ナット各4個で固定。頭座面Z=-27.4、ナット底Z=-6.5、先端Z=-2.4で箱底Z=0へ出ない。箱を載せる前にナットを入れる。
- 六角頭M3×40、既存φ16ノブ、M3ナット、φ7×厚0.5ワッシャ、5×8×厚1 mmゴム2枚を流用。カメラを支え、横ボルト・ワッシャ・ノブを機体+Yへ45 mm以上抜き、下から見て時計回り60°回して下へ抜く。独立落下防止コードを使う。
- 接続板だけに深さ1.2 mm・入口0.3 mmの開放逃げを追加し、ノブ周囲の操作余地を作る。C爪・カム・ゴム座の機能形状は変更しない。
- 外側の「○△○」前壁と不要な底板延長を廃止。親機の別体角度ストップ、左右の橋固定ねじ・調整M4ねじ・ナット類も取り外す。M5固定とZ=36.5の左右底面受けは維持する。

## その他の外装と取付

Rev.7平板の主面232×134 mm、公称厚20 mm、Z=-20..-0.8。三点基準のみZ=0。予備M4穴15個は[穴配置JSON](../../spec/parent_oneplate_mounting_pattern.json)が正本。厚7 mm・径12 mmの参考治具とM4×25の例のみ検証済み。未知の治具全体の干渉・荷重まで保証しない。予備穴のナットは箱を載せる前に入れる。

TD04A支持はXY=(65,-55),(85,-55)、上面Z=-20へM5×40皿ねじ2本・ワッシャ・ナット各2個で固定。頭上面Z=-0.8、ワッシャZ=-29、ナット底Z=-33。M4クランプ中心Z=-35、金属ブラケット基準X=43・Z=-27を維持。M5全ねじ180 mmを4本、下側ワッシャZ=-31・ナットZ=-35、上側ワッシャZ=122.3・ナットZ=123.3。地上自立時はカメラユニットとTD04A本体・押さえ板・M4押さえねじを外す。接地面Z=-72より上へ配線を保持する。

## 印刷・検証・再生成

parts内の現行STLをPRINT.mdの数量だけ使う。一体カメラは底板下、X1C・0.4 mm・Generic PETG、0.1 mm層、6壁、15% Gyroid、ブリム5 mm、ベッドからの自動サポート。背面接続板・軸・爪の外部支持を除去できる姿勢で、実G-codeの支持はZ=0.2..34.7にある。C摺動面を傷つけずに取り除き、初回は実メスとの嵌合を確認する。[今回のカメラ3MF](print_jobs/camera_twist_20261021/camera_mount_twist/camera_mount_twist.3mf)は1個入り、約5時間18分・106.0 g。他部品は従来のPETG Basic・8壁・100%充填と製造メタデータの姿勢を継続する。

旧[x1c_petg_rev6](print_jobs/x1c_petg_rev6/README.md)の6プレートは変更前の履歴。旧カメラ・別体オス・旧一体位置決め主プレートを含むため、現行一式として印刷しない。camera_twist_20261021の3MFは現行カメラ1個用。Rev.7の5個の3MFは今回変更したプレートと位置決め部だけで、全13種類16個のジョブではない。

C一体化時点（2026-10-21）は全配置73部品のSTEP照合0 NG、当時9種類のSTEP有効性・外形・体積、ネジを含む干渉、Cの60°回転・80 mm抜去、ロック45 mm抜去を検査した。[当時の幾何検査](_work/analysis/support_reduction/geometry_checks.json)、[当時のSTEP検査](_work/analysis/support_reduction/step_checks.json)、[現行カメラのスライス](print_jobs/camera_twist_20261021/camera_mount_twist/validation.json)。実印刷・実ケース・ケーブル・画角・強度・クリープは未認定。

Rev.7では全配置93部品・現行13種類のSTEPとSTLを照合。実体の干渉0、取付8穴の通過・頭/ナット座・ねじ先端と工具、予備15穴・ロープ4箇所、Cの脱着経路を再検査した。印刷済み上側押さえ・脚の形状差は0。[今回の幾何検査](_work/analysis/removable_locators_20261022/geometry_checks.json)、[STEP検査](_work/analysis/removable_locators_20261022/step_checks.json)、[保存3MFと全層の経路検査](_work/analysis/removable_locators_20261022/slice_checks.json)。直前の73部品・9種類の記録はC一体化時点の履歴。

今回の再生成はspec/prepare_parent_oneplate.py、配置はspec/configure_parent_exterior_removable_locators.py。検査はspec/verify_parent_exterior_removable_locators.py、交換用STEP・組立はspec/export_parent_exterior_removable_locators.py、スライスはspec/slice_parent_exterior_removable_locators.py、印刷ジョブ説明はspec/finalize_parent_exterior_removable_locators.py。その後tools/assembly_parts.py sync parent_exteriorを実行する。[変更前の正本・印刷済み部品の参照](_work/analysis/removable_locators_20261022/history/snapshot.json)を保持する。

Rev.7の対象印刷一式はcheck合格、整理検査も合格。全体チェックでは対象外の既存構成に出所不整合・未管理3MFが残る。共通テスト42件は41件合格・既存child_wte4_suspension_clampの材料JSON欠落1件でエラー。今回のログは_work/logs/removable_locators_global_parts_check.log、removable_locators_tidy_check.log、removable_locators_unittest.log。

設計元はspec/build_camera_mount_m3.py --twist-only。既存camera_mount.scadを再利用する生成バリアントで、出力を手編集しない。配置はspec/configure_camera_twist.py、検査はspec/verify_camera_twist.pyとspec/verify_parent_exterior_support_reduction.py、交換用STEPと組立STLの更新はspec/export_camera_twist.py、スライスはspec/slice_camera_twist.py。その後tools/assembly_parts.py sync parent_exteriorとcheckを行う。主プレート等は既存spec/prepare_parent_oneplate.py系統が正本のまま。

[変更前の配置・説明・印刷一式](_work/analysis/camera_twist_20261021/history/snapshot.json)を保持。共通42テストは41件合格・既存の材料JSON欠落1件でエラー。対象外の印刷一式には既存の出所不整合があり、今回の検査と分けて記録する。

前壁付きの設計元・STL・STEPはカメラ部品の_work/analysis/compact_front_20261021/history/、親機の旧配置・説明は[_workの履歴](_work/analysis/compact_camera_20261021/history/)、旧カメラ3MFは[print_jobsの履歴](print_jobs/history/camera_with_front_stop_20261021/)へ保持する。別体角度ストップを現行印刷一式へ戻さない。


[TD04A改訂後の全体確認画像](_work/images/td04a_cable_r6.png)。幾何・STL/STEP・外装側ナット保持・スライス結果は[共通治具の検証](../td04a_fixture/_work/analysis/validation_summary.json)。センサー側の実締結成立・実物適合・強度は未検証。
