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


