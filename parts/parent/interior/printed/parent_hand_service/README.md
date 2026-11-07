## 2026-10-29 電池蓋を上方取り外しへ変更

電池蓋はM3×12ねじ1本を外し、真上に持ち上げる方式へ変更。本体の固定ねじ4本は外さない。本体と蓋を各1個再印刷する。旧スライド手順は履歴。詳しくは [電池蓋の改訂報告](../../../../../assemblies/parent_hand_service/battery_top_lid_report.md)。

# 2026-10-29 床下面ナットへの貫通固定

現行は [改訂報告](../../../../../assemblies/parent_hand_service/unified_support_report.md)。床の下面開放六角くぼみへM3ナットを入れ、上からの貫通ねじで床板まで挟む。MAIN枠とSony/GNSS支持枠の対象穴は通し穴。足の一体化・50 mmは維持。以下は変更前の履歴。

# 2026-10-28 一体支持枠・埋め込みナット廃止

現行の説明は [改訂報告](../../../../../assemblies/parent_hand_service/unified_support_report.md)。Sonyの4本の足をsony_support_frameの1部品へ統合し、肩まで50.0 mm、キー0.8 mmを別に確保。床の内部ナット穴と電池蓋用ナット穴を廃止。床は通し穴、支持部品と電池蓋は内接径2.8 mmの樹脂下穴へ締結する。

設計正本は既存Python生成元。製造姿勢はmanufacturing.json、使用バリアントと数量はassemblyのplacement.json。印刷入口はassemblyのparts/PRINT.md。以下は旧版履歴。

# 2026-10-27 北側ペネトレータ対応

現行の説明・寸法・締結手順は [床板改訂報告](../../../../../assemblies/parent_hand_service/plate_access_report.md)。印刷入口は [PRINT.md](../../../../../assemblies/parent_hand_service/parts/PRINT.md)。この改訂ではfloor_plate、sony_mount_plate、sony_fixed_column_0、battery_baseを交換する。共有柱と同軸リングは各共通部品フォルダの同じ正本を更新する。

床の生成元はspec/build_parent_hand_service.py／spec/parent_switch_tx_body.py、局所形状はscad/lib/parent_floor_access.py。既存の同じ生成元から作り、出力SCADを手編集しない。床M3ナット11か所は対辺5.8 mmの横挿入穴、上の屋根で+Zの抜けを受ける。M4頭口10.8 mm、電池台は配線端へ開放した頭通路。床・固定板・柱は原姿勢の下面をベッドへ向ける。

以下の床板無加工再使用・床裏座金・旧取付軸は改訂履歴。実ねじ・工具・嵌合・印刷・強度は試作確認。

2026-10-24 MAIN下面・独立スペーサ改訂：格子下面の3.7 mmの浮きを解消。独立スペーサ12軸は対辺3.5 mmの通し穴と多角形外形。一体の基板ねじ座は2.8 mm下穴を維持。現行の金具・手順は assemblies/parent_hand_service/frame_spacer_printability_report.md を参照。床裏のナットを保持して締める構成に変更。以下の全スペーサ直接締結・整備用M3×8・最長30 mmの記述は変更前の履歴。

2026-10-24 SPRESENSE固定板増厚：ねじ止め時の割れに対応し、板厚1.6→3.2 mm。固定板1個を再印刷。基板とねじ座を1.6 mm上げ、支柱接合面は維持。現行手順は assemblies/parent_hand_service/sony_plate_thickening_report.md（リポジトリ基準）。下記の厚1.6 mm・Sony板再印刷不要の記述は変更前の履歴。

2026-10-24 現行：スペーサ・床側受け・棚接合柱の内部ナット穴27か所を廃止。内接径2.8 mmの縦下穴へ直接締結する。抜け止め4個は不要。印刷一式は16種類16個。以下のナット式の記述は変更履歴であり、現行の手順と数量は改良報告・parts/PRINT.mdを参照。

2026-10-24 基板直接固定：MAINはM3×8を4本、電源基板はM3×6を4本で樹脂下穴（内接径2.8 mm）へ直接固定。基板用ナット8個を廃止。MAIN枠と電源アダプタだけ変更し、床板・LiPo・整備ねじ4本の構造は維持。現行の数量と手順はretrofit_report.mdおよびparts/PRINT.mdを参照。

## 2026-10-24 内装改良バリアント

設計元は `scad/lib/parent_service_retrofit.py`、生成入口は `spec/build_parent_hand_service.py --service-retrofit`。旧部品は保持し、現行内装の選択は `assemblies/parent_hand_service/placement.json` に従う。新規バリアントの手順・再使用範囲・金具は [改良報告](../../../../../assemblies/parent_hand_service/retrofit_report.md)。STLの姿勢は manufacturing.json を使い、支持材禁止モディファイアは部品として印刷しない。実物検証前の試作。

電源基板は元の向きで南11 mm・上5.5 mm。MAIN枠の後端中央に逃げを追加し、電源アダプタの床固定はM3×8を4本、頭を1 mm沈める。Pico 2 Wの基板上17 mm包絡からアンテナ棚まで3.8 mmを確認。床板とLiPo固定具は変更しない。

# 親機：固定板とねじ座

2026-10-13 全長側溝改訂：蓋を端から全長107.4 mmの両側溝へ差し込み、M3×12ねじ1本で固定。開く際は台の固定ねじ4本を外して閉じた電池ボックスを上へ約90 mm持ち上げ、蓋を南108 mm引き抜く。基板・最下段・同軸巻き部は変更なし。電池台と蓋を各1個再印刷。現行手順はbattery_side_grooves_report.md。

2026-10-13：電池下の工具穴を8 mmへ拡大。蓋は2 mmスライド＋M3×12ねじ1本。ナット差込み口を50°の斜め天井にし、局所サポート禁止設定を同梱。電池台の設定済み3MFと詳しい手順はbattery_tool_nut_access_report.md。最下段とコード巻き部の形状は変更なし。

2026-10-12 子機参照改訂：現行child_vtray_batt_floorの2本の端フック（厚1.3・高さ3・差込2・根元4 mm）と片側0.3 mmのすきまを親機へ反映。蓋を南2 mmの位置から下ろし、北へ2 mm差し込んでM3×12ねじ1本を締める。外すときはねじを外し南2 mm戻して上へ抜く。電池台と蓋だけ再印刷。床板・MAIN固定板・子機部品は変更なし。 共通生成元scad/lib/parent_battery_slide.pyが子機の現行SCADを直接読み、フック寸法を引き継ぐ。

2026-10-12：容器固定ねじは南西・南東・北西のM4×12を各1本、計3本。最下段floor_plateはSCAD/STEP/STLすべて変更前と同一。再印刷はmain_mount_plate、battery_base、ann_mb1_coax_ring各1個だけ。長軸2.5 mmボールポイント六角レンチを使い、南西は南西方向へ10°、北西は西方向へ10°傾ける。南東は電池蓋とねじ1本、LiPo、上面フォームを外して電池台のØ4.2穴から操作する。北東ねじは使用しない。工具穴へコードを通さず、同軸束は新しい囲いの外へ収める。リング下面の局所支持を除去し工具穴を確認。実工具の嵌合、5 m巻き容量・R20曲げと3点固定の強度は未認定。 設計条件はscad/lib/parent_case_access.py、生成は既存spec/build_parent_hand_service.pyとspec/build_parent_gnss.pyを継続。

2026-10-11。MAIN/Sonyの両方に固定板を設ける。大きな矩形肉抜きで材料を減らし、ねじ座4点で基板を浮かせる。ピンごとの切欠きは使わない。板下面を平らにし、下の柱を分離して印刷支持を減らす。

MAIN板はmain_mount_plate、厚2.4・下面33.1・座上面41.95。main_corner_columnは高さ14.3を4本。Sony板はsony_mount_plate、厚1.6・下面60.5・座上面65.55。Sony柱4本は41.7＋キー0.8。Sony床ねじはM3×50を4本、頭座62.1。基板高さ42/65.6とMAIN/PCBねじは維持。

正本はspec/build_parent_hand_service.py、spec/parent_switch_tx_body.py、共通形状はscad/lib/parent_corner_mounts.py、共通寸法はscad/lib/parent_gnss.py。配置はassemblyのplacement.json。旧支持板・独立支持腕は履歴で現行の非印刷ファイル。旧解析を現行剛性の認定に使わない。

両板と柱は下面をベッドへ向ける。扱い稜と穴入口は0.15 mm面取り、座面・キー・パイロットは機能寸法を保持。GNSSを含む12本の柱をランナー1枚へまとめる。印刷入口はassemblies/parent_hand_service/parts/PRINT.md、最新検証はfixed_plate_report.md。実締付け・嵌合・波浪・クリープは未認定。

## 過去の説明（履歴）

# 親機：ねじ穴付近だけの基板支持

2026-10-11。MAINは直立スペーサ3本と前左支持腕1個、SPRESENSEは床からの柱4本に載る独立支持腕4個へ変更。PCB高さ42/65.6 mmを維持し、広い支持板と部品・ピンごとの逃げ加工を撤去。MAIN前左は同軸リングを避け、Sonyの柱はTX予約外に置き、腕下面をZ60.5へ置く。基板下に全体を覆う板はない。

正本は既存spec/build_parent_hand_service.pyとspec/parent_switch_tx_body.py、支持形状の共通関数はscad/lib/parent_corner_mounts.py。配置・数量はassemblies/parent_hand_service/placement.json。main_corner_columnを3個、main_offset_cornerを1個、sony_corner_0..3を各1個使う。これらはGNSS/Sony柱とともに16個のランナー1枚へ組み込む。個別STLを追加印刷しない。

扱い稜と穴入口は0.15 mm面取り。座面・パイロット・キーの機能寸法は保持。MAIN直立柱はZ上向き、支持腕はX180度、Sony角3だけさらにZ90度。印刷・サポートは同assemblyのparts/PRINT.mdとcorner_mount_report.mdを参照。旧main_lower_carrier/sony_upper_carrierは履歴の非印刷ファイルで、現行配置に含めない。

実嵌合、締付け、波浪、樹脂クリープと現行剛性は未認定。

## 過去の説明（履歴）

# parent_hand_service：容器図面の訂正に対応

2026-10-11。メーカーPDF/DXF由来のBCAS本体・ふたに合わせ、床四隅の成形壁と全16ボスを逃がし、M4接触座をZ10まで延長した。M4×12ボタン4本で固定する。LiPo北3.6 mm、TX南4 mm、GNSS後左脚東2.6 mmの移動とSony後梁の短縮を生成元へ反映。PCB高さ、床M3ナット座下面の連結、開放積み上げを維持。印刷入口はassemblies/parent_hand_service/parts/PRINT.md、現行検証は同assemblyのcase_fit_report.md。過去の剛性解析は変更形状には適用できず、実物公差と剛性は未認定。

## スペーサ積み上げ改訂の履歴

2026-10-10。Sony囲い壁を撤去して、上台と独立した印刷スペーサ4本で積み上げる。床ナット座は格子下面Z8.84までつなぎ、ケースボスとの重なりだけを逃がす。床上18.8、PCB高さ・ねじ頭座・ナット高さは維持。MAIN・PWR・TX・電池の一体支持は印刷部品のまま。スペーサセットは parts/common/interior/printed/stack_spacers に一か所だけ定義し、GNSS既存支柱も再利用して8本を切離しランナーへまとめる。

生成元はspec/build_parent_hand_service.py、spec/parent_switch_tx_body.py、共通寸法はscad/lib/parent_gnss.py。印刷入口と今回の条件はassemblies/parent_hand_service/parts/PRINT.md。実印刷と実波浪での保持は未認定。

## 以前の説明（履歴）

# parent_hand_service：現行の印刷削減改訂

2026-10-09。現行床は幅7.5・高さ9.96 mmの開放格子。PWR/TX/LiPo支持座とM4座・M3ナット座を維持。MAIN/Sonyは支持面を下にするX180°で印刷。Sony配線窓は幅24・最大高さ13、印刷時45°の屋根。MAINのSD/USB領域は支持板を残す。

生成元、共通寸法、配置は既存の一か所を継続。印刷姿勢の正本はmanufacturing.json、印刷入口はassemblies/parent_hand_service/parts/PRINT.md。PETG0.2 mm・4周壁・100%インフィル、局所自動支持。操作／同軸包絡／工具経路は再検査。解析・実締結の適用限界は同assemblyのwave_rigidity_report.mdとprint_economy_report.md。新しいキーの嵌合と揺動・緩みを実物で確認する。

## 改訂前の説明（履歴、現行印刷には上記を適用）

# 親機内装の共通設計元

`spec/build_parent_hand_service.py`と`spec/parent_switch_tx_body.py`が同じパラメータからSTEP/STL/SCADを生成。寸法の正本は`scad/lib/parent_gnss.py`、配置は`assemblies/parent_hand_service/placement.json`。

現行は`floor_plate`、`battery_base`、`main_lower_carrier`、`sony_upper_carrier`。MAINをアンテナ下へ移し、電源2スイッチの上方を空ける。Sony棚下面Z61.5で、TX実装上端Z40.195から20 mmの予約領域を避ける。MAIN USBは箱外、両SDとLiPoは箱内で操作する。

2026-10-09：LIS3MDL磁気センサをX62.78/Y195/Z76・Z回転90°へ追加。固定棚は[既存GNSS台](../gnss_universal_carrier/README.md)の一体バリアントとして生成し、このフォルダに重複定義しない。公式完成基板STEP、ナイロンM2×8／M2ナット各4個を組立へ追加した。磁気精度・実プラグは実機確認。

旧`lift_carrier`、`guide_*`、`service_prop_*`は履歴。現行構成へ混ぜない。金属ピン・長ねじ・ストラップ・蓋予約・`tx_top_keepout`は印刷しない。LiPoフォームと捕捉ナット、`lid_narrow`は既存設計を再利用。

PETG 0.2 mm・4周壁の取合い試作。床下面とキャリア棚／段差にサポート。新キャリア外周・支柱0.15 mm、床外周0.25、穴入口0.4 mm逃げ。実部品の逃げ、基板接触・ねじ座・パイロット・フォーム／ナット保持の機能稜は寸法を維持。強度・熱・反復操作は未認定。詳しくはassembly READMEとparts/PRINT.mdを参照。


2026-10-09 波揺れ改訂：現行assemblyのREADMEとwave_rigidity_report.mdを参照。床下面に高さ5 mmの格子・外周リブ、ケースM4×8ボタンねじ4点固定、MAINの支持面をZ41.95へ変更、Sony台に3面の壁と実部品逃げ付きベッドを追加。アンテナ台は左Ø7.8／右Ø6.8支柱・側梁・厚5 mm天板、南西ケースねじ頭の下面逃げØ8.4貫通、外壁4か所の編糸窓を持つ。主要扱い稜は結合前0.2 mm面取り、後加工の部品逃げ・座面・留め穴は機能寸法を保持しバリを除く。巻き束は糸込みでOD100/ID75/H10に保持。PETG 0.2 mm・4周壁・100%インフィル、積層Z。取付ねじの締付け・緩み・実寸・樹脂クリープは実物で確認する。

上締め改訂：床側16個のM3六角ナットへ長ねじで締結。MAINは台前左M3×25＋基板共締めM3×30×3、SonyはM3×45×4、GNSSはM3×40×4、アンテナはM3×50×4。床下面から締める旧M3×8×16は現行に使用しない。組立は現行assemblyのREADMEの順序を守る。


## 2026-10-11 LiPo配線端の全面開放

変更はLiPoボックスだけ。子機の着脱板と端面リード逃げを参考に、親機の配線側（ボックス局所−X、箱座標では南側）を内幅40 mm、床上26 mmの全域で開放した。従来の中央16 mm窓とその屋根を廃止し、左右端から出るコードを塞がない。開口縁は0.2 mm面取り。床厚3 mm、箱外形、4取付穴、蓋、ねじ・ナット、電池位置は維持した。基板・容器・アンテナ・スペーサは変更していない。

配線側の端フォーム2枚を省いた非印刷バリアント `battery_pads_open_end` を使用する。上面・側面・反対端の4枚は従来形状のまま。蓋の4本を外して電池と左右の線を一緒に上へ出し入れできる。開放端に剛性ストッパはなく、残したフォームを実物に合わせて軽く圧縮し保持する。

収納は公称102×34×23 mm、商品公差上限104×36×25 mmの剛体包絡を確認する。最大個体では端/側/上フォームを公称の2/3/3 mmのまま使えないので現物に合わせて薄くする。線径・端子外形・外部への曲げ経路は未実測。組立や強度の実物検証を済ませた扱いにはしない。

設計元は `spec/build_parent_hand_service.py --battery-only`。既存の全体ビルドもこの同じボックスとフォームを生成する。検証と印刷入口は assemblies/parent_hand_service/battery_box_report.md と同assemblyのparts/PRINT.md。
# MAINスペーサ4本の多角形STL（2026-10-22追加依頼）

`main_corner_column_polygon_4.stl` はMAIN用4本だけを並べた印刷バリアント。外側は六角形（元のØ7 mm包絡内、頂点と上下縁は0.1 mm面取り）、高さ14.3 mm、穴は内接径／対辺3.45 mmの補正八角形、穴口0.15 mm面取り。穴の縦8稜は指定の機能形状として保持する。元のM3通しねじとMAIN固定板を使い、柱にタップしない。

生成元は `spec/build_parent_main_polygon.py`。既存 `main_corner_column.step` から高さ・外形・穴径を取得する。単体の `main_corner_column_polygon` と4本入りの同名 `_4` は同じ生成元の出力で、4本のピッチ12 mm、2×2配置、つなぎなし、平らな下面Z0・穴は上向き。配布STLは `assemblies/parent_hand_service/print_jobs/main_polygon_4/MAIN_spacers_polygon_4.stl`。SHAと検証結果は隣のmanifest.json。PETG・0.4 mmノズル・0.2 mm積層・壁4周・100%充填を想定し、小さい接地面には3 mmブリムを推奨。実物の嵌合・締付けは未検証。

今回の依頼用の4本だけを印刷する場合に、このSTLを1個読み込む。従来の単体丸柱4本や12本入り3MFと重複印刷しない。既存の全体組立・13種類20個の一式は丸柱の参照構成を保持する。4か所すべてで床への着座・上側の接触・干渉を検証した多角形の印刷バリアントであり、全体の再配置は行っていない。
