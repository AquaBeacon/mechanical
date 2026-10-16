# 設計・印刷条件の控え（自動生成）

以下は設計元の文書を転記したものです。リンク先は元フォルダ基準です。印刷条件と未検証事項を確認してください。

## parent_service_review/README.md

**印刷一式:** [parts/PRINT.md](parts/PRINT.md)（STL・数量・モディファイア） · **確認画像:** [_work/images/](_work/images/)

> 旧案：USB・SDの小さい操作空間のみを確認した配置です。一般的な手の操作性は確認できておらず、アクセス可能という旧記述は撤回します。最新の引き上げ式案は ../parent_hand_service/README.md を参照してください。

## LiPo固定改訂（2026-09-26追記）

子機の着脱式電池箱を参考に、6面保持の親機用ケースを追加。M3×12ねじ4本で上蓋を固定し、端・側・上面フォームで遊びを埋める。詳細は [parent_lipo_retainer](../../parts/parent/interior/printed/parent_lipo_retainer/parent_lipo_retainer.md)。ベースと蓋を剛性支柱で位置決めするので、締め付けによる電池の圧迫を避ける。USB・SD全5か所の干渉ゼロを維持。6方向接触0 mm、箱蓋基準面までの高さ余裕5.5 mm。

# 親機内装・蓋開放サービス改訂（2026-09-26）

SONY Spresense拡張ボード + メインボード + マルチIMUを独立スタックとして搭載する。
ユーザー指定の「蓋を開ければ、基板を外さずUSB・SDを抜き差しできる」運用。
この改訂の確認用CADは `parent_service_review.step`、緑の操作空間は `service_volumes.step`。
`_work/images/service_paths.png` は同じ配置JSON・STEPから生成したSTLのプレビュー。

## Webから取得し、実際に使用したデータ

- [Sony公式HW CAD](https://github.com/sonydevworld/spresense-hw-design-files)：CXD5602PWBMAIN1.stp / CXD5602PWBEXT1.stpを取得し、基板・コネクタ・穴の実ソリッドを配置した。
- [Sony公式IMU仕様](https://developer.spresense.sony-semicon.com/ja/buy-spresense/spresense-imu-add-on-board/)：50.0 × 20.6 × 9.1 mm。取得したHTMLは `parts/parent/interior/cots/spresense_logger/ref/sony_imu_product.html`。
- IMU詳細STEPは取得したSony公式設計資料リポジトリに掲載されていなかった。IMUは**公式寸法による包絡**であり、詳細CADとして扱わない。
- 取得原本とSHA256は `parts/parent/interior/cots/spresense_service_stack/sources.json`。Sony原本は `spresense_logger/ref/` に保存。

## 最終配置

座標は箱外面の南西底を原点、X東・Y北・Z上。単位mm。

| 部品 | XY範囲（基板外形） | 基板下面Z |
|---|---|---:|
| 自作P-MAIN | (15.5,40.5)–(127.5,128.5) | 24.8 |
| P-PWR | (19.5,133.5)–(119.5,217.5) | 28.3 |
| TX（90°） | (134.5,140.5)–(184.5,214.5) | 24.8 |
| Sony拡張 | (134.5,41)–(187.84,109.58) | 24.8 |
| Sonyメイン | (145.79,41)–(166.39,91) | 29.4（積層仮値） |

P-MAINとP-PWRは北へ25、P-PWRはさらに東へ4、TXは北へ50移動。
PWR裏リードの逃げは9.5 mm支持を継承。LiPo、トレイ、MAINの4本のスペーサも北へ25移動。
PWRはプレート北端を1 mm越えるが、箱との体積交差はゼロで取付穴はプレート内にある。
TXの部品突出を含む実モデル北端は215.94 mm。箱との体積交差はゼロ。

Sony拡張のØ3取付穴は、不等配置の実CAD座標
(2.54,54.61)、(50.8,53.34)、(7.62,2.54)、(35.56,2.54)を使う。
旧四隅inset=3.5のボスは使わない。自作基板の穴は `.kicad_pcb` から生成し `hole_sources.json` に保存。
箱固定ねじは**南側のM4インサート2点**へ変更。中央の南側位置決めピン2点は継承。
北側はPWR/TXに近いため固定工具の通路に使わない。

## USBとSDの確認

| 操作対象 | 挿抜方向 | 予約奥行 | 指・プラグの予約幅 | 結果 |
|---|---|---:|---:|---|
| P-MAINのPico USB | 南 | 30 | 14 | 交差0 |
| P-MAIN microSD | 南 | 25 | 20 | 交差0 |
| SonyメインUSB | 南 | 30 | 14 | 交差0 |
| Sony拡張USB | 南 | 30 | 14 | 交差0 |
| Sony拡張microSD | 北 | 25 | 22 | 交差0 |

USBは幅14 × 高さ8 mmのプラグ包絡、USB口から30 mmの通路を予約。
想定はコネクタ外側の樹脂ボディ20 mm以下 + 上方へのケーブル曲げ10 mm。
製品固有のケーブルが未指定なので、これを越える樹脂ボディや曲げ半径の適合は未確認。
USBの金属嵌合部は意図して口に入るため、樹脂ボディの検査は口の3 mm外側から行う。
SDはカードの幅12 × 厚さ1 mmの移動包絡と、スロットより上の指の通路を別々に検査。
いずれも蓋側から指を下ろせる。電池・トレイ・基板を外す操作を検査条件に含めていない。
USBを同時に給電する電気的な可否は、この機械検証の対象ではない。

## 検証と残る確認

- `verification.json`：5つの操作空間を全28部品のSTEPに対して検査。プラグの嵌合域、ねじ／ボスは除外条件をスクリプトに明記。干渉0。
- Sony–箱、Sony–プレート、PWR–箱、TX–箱、電池トレイ–南側引込2個の体積交差はいずれも0。
- アセンブリSTEPの読み戻し：28部品、位置不一致0（既存検査許容0.5 mm）。
- 印刷プレート：STEP 1有効ソリッド、STL閉メッシュ、STEP/STL外形差ほぼ0、体積差0.007%未満。
- Sonyスタックは重なりを持つ実部品のcompoundであり、単一の印刷用閉メッシュではない。

**実機で確定すべき項目**：Sonyメインの嵌合後の高さ、IMUの挿入深さ・上面高さ・向き、使用USBケーブルのボディと曲げ半径、箱ボス高さ、蓋裏形状。
メイン上面を拡張上面+4.6 mmとして仮配置し、IMU包絡は箱Z34.7..43.8 mm。
その上にさらに5 mmの積層余裕を予約しても箱Z48.8 mmまで（蓋パッキン面90.9 mm）。
ただし積層高さが変わった場合、USBのZも動くので再検査する。
詳細CADがないIMUのピン・下面部品・固定具は、包絡だけでは接触成立を確認できない。

Sony取付穴はØ3のため、固定にはM2.5通しねじ・ナットを想定し、プレート穴は現物に合わせØ2.9へリーマ仕上げする。
LiPo固定用ねじ・ナット12点を追加済み。他の固定ねじの全数実体、配線、LCDブラケットは未追加。LCDは旧モデルでも未設計だった。
この配置では北側ストリップをPWR/TXが使用するため、LCDは蓋側支持に再設計する必要がある。
現時点の成果物は**内装の機械レビュー改訂**であり、配線・LCDを含む完成機の印刷承認モデルではない。

## 再生成

ワークスペース直下から `python mechanical/spec/prepare_parent_service.py`。
OpenSCADで `parent_plate_service.scad` をSTLへ出力。
FreeCAD同梱Pythonで `mechanical/spec/build_parent_service_cad.py` を実行し、
`verify_parent_service_cad.py`、`check_parent_service_pairs.py` で検査。
`preview_parent_service.py` は平面配置図、`scad/lib/asm_gen.py` はアセンブリ表示ソースを生成する。




## parts/parent/interior/printed/parent_lipo_retainer/parent_lipo_retainer.md

# parent_lipo_retainer — 親機LiPoの6面保持

2026-10-02：親機引上げ内装では`parent_lipo_retainer_lid_narrow`を使用。元のlidに`west_trim=0.6`を適用し、西縁だけ0.6 mm狭めてガイドと離す。元のボルト穴・フォーム接触・厚み3 mmは保持。`spec/prepare_parent_lipo_retainer.py`と`export_parent_lipo_retainer.py`で再生成。旧構成の標準lidは変更しない。現行配置は`assemblies/parent_hand_service/placement.json`を参照。

子機の `child_vtray_batt_box` と `child_vtray_batt_floor` の「端壁・側壁・着脱板＋フォーム」を参考にした。
親機のZeee 102×34×23 mmを、床・両端・両側・ねじ止め上蓋で保持する。
ベルクロによる固定から、**M3×12ねじ4本で閉じる剛性上蓋**へ変更。
ねじは側面から挿入するM3ナット4個で受ける。上蓋は支柱上端に当たって止まり、締め付け量で電池厚を決めない。

| 部位 | 公称パックに対する設計 |
|---|---|
| 前後（X） | 片側2 mmの端フォーム。西端はリード開口を避けて2分割 |
| 左右（Y） | 片側3 mm、長さ63 mmの側フォーム |
| 上下（Z） | 床で下面を支持、上面3 mmフォーム＋3 mm厚の固定蓋 |
| トレイ固定 | 従来のMAIN穴103×75.5 mmとM3 MF25×4。M3×8×4で支持スペーサへ固定 |
| 蓋固定 | M3×12なべねじ×4、M3ナット（対辺5.5、厚2.4）×4 |
| 外形 | ベイ111×45 mm、蓋111×53×3 mm。ベースは従来の支持レールを含む |
| 高さ | トレイ下面51.4、蓋下面80.4、蓋上面83.4、ねじ頭上85.4 mm（箱座標） |
| 箱蓋まで | パッキン面90.9を基準として5.5 mm |

原点とMAIN取付穴は旧 `parent_lipo_tray` と同じ。現行のサービス改訂では箱(20,48.5,51.4)へ配置。
ベースのMAIN固定穴は全高さの工具逃げを設け、ねじの頭は床厚3 mmの座に載る。
上蓋のナットは上下2.5 mmの横穴へ挿入。上蓋を締めるとナット上面が横穴の屋根に当たる。
ねじを電池へ向ける部品はない。工具は全て蓋開放後に上から入れられる。

## 電池交換

1. 電源コネクタを外す。
2. 上蓋のM3×12ねじ4本を外し、蓋（上面フォーム付き）を真上へ持ち上げる。
3. 電池を真上へ引き出す。トレイ、MAIN、Sony基板は外さない。
4. 電池とリードを収め、上蓋を支柱に当たるまで締める。

フォームは剛性部品側へ薄いテープで固定し、電池には貼り付けない。
上記フォーム厚は**装着時の厚み**。公称寸法に対する自由厚の例は上3.5、側3.5、端2.5 mmで、0.5 mmの軽い圧縮を想定。
実購入パックの寸法は未実測・商品値±2 mmなので、実寸に合わせフォームと薄いシムを選ぶ。
厚い個体へ同じフォームを無理に押し込まない。上蓋の高さは `lipo_h` と `top_gap` で調整する。
リード出口の現物位置も未確定。西端16 mmの開口は旧トレイのリード逃げを継承した位置。

## 検証

`verification.json`：公称パックの6方向すべてで床／フォームとの距離0、剛性ベースへの食い込み0。
上面フォームと上蓋、上蓋と支柱は接触。ベース／蓋は各STEP 1有効ソリッド、STL閉メッシュ。
STEP/STLの外形差ほぼ0、体積差0.013%未満。
詳細な振動・落下・フォーム保持力の実測は未実施。6面保持を検証した機械レビュー形状である。

## 出力と印刷

`parent_lipo_retainer.scad` の `part` を base / lid / pads / assembly で切り替える。
ベースと蓋をPETGで別々に平置き印刷。padsはフォームの裁断・配置用モデルで、印刷しない。
ベースのナット横穴は2.5 mm高の短いブリッジ。必要なら糸引きを除去してナットを挿す。
寸法データは `dimensions.json`、生成元は `spec/prepare_parent_lipo_retainer.py` と `spec/export_parent_lipo_retainer.py`。

組立状態の追加検査：`assemblies/parent_service_review/battery_retention_checks.json`。
新ベース／上蓋と既存部品の18組、直径8 mmのドライバー4経路、上蓋30 mm／電池35 mmの上抜き経路はすべて干渉0。
`support_checks.json` でM3ナット4個と屋根、ベースとMAIN支持スペーサ4個の接触も確認した。
アセンブリSTEPは28部品で読み戻し、配置不一致0。


## parts/parent/interior/printed/parent_plate_service/parent_plate_service.md

# parent_plate_service

親機の蓋開放USB/SDサービス配置に合わせた183×203×5 mmの改訂プレート。
設計詳細・配置・未確定項目は `assemblies/parent_service_review/README.md`。
OpenSCADソース、STL、編集可能なソリッドSTEPを同梱。
PETG、プレート面を下に印刷。下面の位置決めピンがあるため、ピンの局所サポートまたはピン別印刷が必要。
基板穴はPCBソース、Sony穴は取得した公式STEPから生成。箱固定は南側M4×2。
SonyはM2.5通し固定のためボス穴をØ2.9に仕上げてナットを使用する。その他はM3セルフタップ下穴Ø2.6。
機構荷重・落下強度は今回未解析。印刷前に箱ボス高さと実機の積層高さを合わせる。

