# 設計・印刷条件の控え（自動生成）

以下は設計元の文書を転記したものです。リンク先は元フォルダ基準です。印刷条件と未検証事項を確認してください。

## parent_clamped/README.md

**印刷一式:** [parts/PRINT.md](parts/PRINT.md)（STL・数量・モディファイア） · **確認画像:** [_work/images/](_work/images/)

# 親機外装：上下クランプ案（2026-09-16）

「箱底の固定穴が使いにくい」という意味を仮定した改訂案。タカチBCAS212310Gを底板1枚と上部バー2本で挟み、箱の外側を通るM5全ねじ4本で締結する。箱底の既存穴は使わない。下方への揺れ止め支柱・フィン・錘は設けない。

## 構成

|部品|数量|仕様|
|---|---:|---|
|底板 `parent_clamped_deck`|1|236×236×12 mm、M5通し穴は224×110 mmピッチ|
|上部バー `parent_clamp_bar`|2|236×24×12 mm、穴ピッチ224 mm|
|浮子取付耳 `parent_float_lug`|4|24×32×44 mmのL字部品、横向きφ10.5通し穴1個／部品|
|取付耳用M5×30ボルト・座金・ナット|各8|各耳を2本で底板に固定|
|M5全ねじ|4|長さ150 mm、図ではZ=-20〜130。金属購入品|
|M5ナット|8|図は二面幅8、高さ5 mmの簡略形状。緩み止め方式は実物のナット仕様に合わせる|
|M5座金|8|図は外径10、内径5.5、厚さ1 mm。外径12以上は底板端に余裕がないため避ける|
|ゴムパッド|4|14×24×厚さ2 mmを仮置き。上部バーの下面両端に貼付|
|M5熱圧入インサート|8|カメラ・TD04Aマウント用。下穴径6.4、深さ8 mmは購入インサートに合わせて調整|

箱底をZ=0、箱中心をX=Y=0とする。全ねじはX=±112、Y=±55。上部バー下面Z=102.3、上面114.3。ゴムパッド中心X=±98、Y=±55、下面Z=100.3。箱の高さ100.3 mmは既存図面値。ゴム厚は締結前の名目値で、圧縮分はナット位置で調整する。

箱上面の外縁近くに荷重をかけ、中央をバーで直接押さない構造。箱の横ずれは締付けとパッドの摩擦で抑えるため、滑りの実物確認が必要。蓋形状・パッキンへの締付荷重の影響は未検証で、確定トルクは設定していない。実物の支持できる平面位置にパッドを合わせ、箱が変形するほど締め込まない。

## 組立と開閉

1. 底板の下面からカメラ・TD04A用インサートを取り付ける。
2. 底板に箱を置き、M5全ねじを外側の4穴に通して下面の座金・ナットで受ける。
3. 上部バーの両端下面へゴムパッドを貼り、全ねじへバー2本を通す。
4. 上側の座金・ナットを付け、4か所を交互に均等に締める。
5. 底板の左右に取付耳を各2個、M5×30の2本／個で固定する。ボルトは上から、座金とナットは下面。取付耳の横向きφ10.5穴へ浮子固定用の紐・金具を取り付ける。浮子側の接続具は今回含めない。

### 浮子固定用の追加部品

穴はM10用の**通し穴φ10.5 mm**で、ねじ山は設けない。穴中心は左右X=±122、前後Y=±85、高さZ=10 mm。穴軸はX方向。取付耳の板厚は8 mm、底板への固定穴は16 mmピッチのM5通し穴2個。左右は同じ印刷部品を180°回して使用できる。

底板の従来φ8紐穴4個は、取付耳用M5穴8個（X=±112、Y=±77／±93）に置き換えた。クランプ全ねじから取付耳までは11.5 mm、箱側面から耳までは13 mm離れる。浮子の仮包絡との最小隙間は2 mm。M10ボルト・アイボルトなど実際の固定具の長さは相手部品に合わせる（大きな金具は別途干渉確認）。

**蓋を開く際は上側ナット4個とバー2本を外す。** バーを付けたまま開閉する構造ではない。蓋のねじ位置Y=±106とバー端Y=±67は39 mm離れる。南側ペネトレータと中央のケーブル切欠きは従来位置を継承。

## マウント取付面

底面Z=-12にカメラ用22×32 mmピッチ（中心X=-48,Y=0）とTD04A用50×46 mmピッチ（中心X=55,Y=0）を各4穴。M5インサート用止まり下穴で、箱側に4 mmの肉が残る。マウント本体は今回含めない。既存の垂直面用マウントを水平底面で下向きに使うには向き変更／アダプターが必要。

## データ・検証

- 底板：[SCAD](../../parts/parent/exterior/printed/parent_clamped_deck/parent_clamped_deck.scad) / [STEP](../../parts/parent/exterior/printed/parent_clamped_deck/parent_clamped_deck.step) / [STL](../../parts/parent/exterior/printed/parent_clamped_deck/parent_clamped_deck.stl)
- 上部バー（同じ物を2個）：[SCAD](../../parts/parent/exterior/printed/parent_clamp_bar/parent_clamp_bar.scad) / [STEP](../../parts/parent/exterior/printed/parent_clamp_bar/parent_clamp_bar.step) / [STL](../../parts/parent/exterior/printed/parent_clamp_bar/parent_clamp_bar.stl)
- 浮子取付耳（同じ物を4個）：[SCAD](../../parts/parent/exterior/printed/parent_float_lug/parent_float_lug.scad) / [STEP](../../parts/parent/exterior/printed/parent_float_lug/parent_float_lug.step) / [STL](../../parts/parent/exterior/printed/parent_float_lug/parent_float_lug.stl)
- 組立表示：[parent_clamped_view.scad](parent_clamped_view.scad)。`placement.json`が配置の正。金具・蓋・ゴムは簡略参照モデルで、印刷しない。購入箱の既存モデルは蓋面を省略しているため、厚さ3 mmの蓋表示を追加している（製造形状ではない）。
- OpenSCAD出力、STEP単一ソリッド化、閉じた単一STLと寸法を3種類とも確認。STEP変換時にSTLとの外形・体積を照合。正面・斜視プレビューを目視確認。
- 名目隙間：全ねじと箱4.5 mm、座金と底板端1 mm。これらは仮包絡に対する寸法確認で実物適合や耐荷重を保証しない。
- 未検証：蓋の凹凸・パッドの当たり、締付力、濡れた状態の滑り、樹脂の長期変形、浮力・復原性、スライス。

PETG、0.4 mmノズル、0.2 mm層、壁6周、上下6層、40%インフィルを初期値とする。底板は箱側平面をベッドにして上下反転、バーは広い面を下にする。どちらもサポート不要の形状。236 mm辺は5 mmブリム込み246 mm。プリンタ禁止領域を含む配置はスライサで確認する。

浮子取付耳は足の下面をベッドに置く。M5穴は縦向き、φ10.5穴は横向きになるため、横穴の天井は必要に応じてサポートし、印刷後に通りを確認する。新規部品のスライス・耐荷重評価は未実施。

再生成：`python spec/prepare_parent_clamped.py` → `./build.ps1 -Paths parts/parent/exterior/printed/parent_clamped_deck,parts/parent/exterior/printed/parent_clamp_bar,parts/parent/exterior/printed/parent_float_lug` → `python spec/build_parent_clamped.py`。最初のスクリプトは旧底板から派生ソースを再生成するため、手修正した派生SCADは上書きされる。


## parts/parent/exterior/printed/parent_float_lug/parent_float_lug.md

# 浮子固定用取付耳

親機クランプ外装の左右に2個ずつ、同じ部品を計4個使用。

- 外形24×32×44 mm、L字の板厚8 mm。
- 浮子側：横向きφ10.5 mmのM10通し穴。ねじ山なし。
- 底板側：φ5.5 mmを16 mmピッチで2穴。M5×30の2本と下面の座金・ナットで固定。
- 右側はSCAD座標のままY=±85へ移動。左側はZ軸まわり180°回転して同位置へ配置。
- 印刷は足の下面をベッドへ。横穴天井のサポートと穴の通りを確認。
- STL閉メッシュ1個、STEPソリッド1個、寸法一致を確認済み。耐荷重・スライスは未検証。

組立詳細：`assemblies/parent_clamped/README.md`。

