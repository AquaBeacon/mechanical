# parent_interior_p1 — 親機内装 パターン1 (Osmo Action 6 外付け) 組立モデル

タカチ BCAS212310G (選定案・人間確認待ち) に `parent_plate_p1` (183×203) を載せ、
P-MAIN / P-PWR / TX_improved / SPRESENSE / LiPo を実配置したモデル。
**2026-08-28 改訂:** LiPo は `parent_lipo_tray` (MAIN 穴の M3 MF25 スペーサ ×4 に架ける
ブリッジトレイ) で最上段に固定。箱モデルはタカチ図面 DXF 実座標。宙に浮いた部品は LCD (未設計) のみ。
配置根拠: [docs/親機内装_収まり検討.md](../../docs/親機内装_収まり検討.md) §4、
検証: `spec/parent_interior_layout.py` (assert 済み。2026-08-29 に南壁ペネトレータの `check_penetrators()` を追加)。

## 座標系

箱外形の左下手前が原点。X=210 / Y=230 / Z=上。
箱底外面 z=0 / 内床 z=3.8 (図面 3.84) / プレート下面 z=13.8 (ボス高さ 10 仮値)。

## z スタック

| z | 内容 |
|---|---|
| 3.8 | 箱内床 (中央 193.2×173.2 にリブ台 +3) |
| 13.8–18.8 | parent_plate (t5)。北 M4 皿 ×2 + 南ピン ×2 → 箱タッピングボス (65,25)/(105,25) |
| 24.8 | 基板下面 (M3 ボス 6)。MAIN 基板上面 26.4 = M3 MF25 スペーサ ×4 の下端 |
| 51.4 | `parent_lipo_tray` 下面 (MAIN 最高部品 44.9 と 6.5) |
| 54.4 | LiPo 下面 (トレイ床 3) |
| 77.4 | LiPo 上面 (最高点。蓋パッキン面まで 13.5) |
| **65** | **南壁ペネトレータ ×2 の軸** (WetLink M10。箱内へ y=14.5 まで突出) |
| 90.9 | 蓋パッキン面 (内高 87.1 + 床 3.8) |

## 貫通部 (南壁 WetLink M10 ×2) — 2026-08-29 追加

| ラベル | 箱座標 | ケーブル | 落とし先 |
|---|---|---|---|
| `pen_tether` | 南壁 (Y=0) x=120, 軸 z=65 | C1 テザー (電源 + RS485) | P-MAIN `J_TETH1` (箱 x≈123) |
| `pen_td04a` | 南壁 (Y=0) x=85, 軸 z=65 | C3 TD04A | TX (右列) |

- 箱側の追加工は `bcas212310g.scad` の `pen_x` / `pen_z` / `pen_d`(10.2)。
  座面・カバービス柱・トルクレンチのピッチを同 `.scad` が assert する。
- 部品は `wetlink_penetrator_m10_ref` の **`bcas` バリアント** (`wall_t 6.1`
  = このモデルの側壁厚)。実壁 3.08 ではナットが 3 mm 外側に来る = 保守側。
- y の占有: 箱外 −22…0 / 壁 0…6.1 / 箱内 6.1…14.5 (ナット上端)。
- **箱内に出るのは素の導体** (WetLink は濡れ側だけをシールする)。
  → 箱内に端子台が要る。**TD04A の 3P プラグは通らないのでケーブルを切る**。
- **検査コマンドに注意**: ペネトレータと箱は `group: "vessel"` なので、
  CLAUDE.md の既定 (`--groups interior`) では**見られない**。この 2 本を含めるには
  `--groups all` を付けること:

  ```powershell
  python scad\lib\check_asm_contacts.py assemblies\parent_interior_p1\placement.json --root . --ignore-threads --groups all
  ```

  (2026-08-29 現在: ペネトレータ ↔ 箱 は 貫通 0 / FLOATING 0。
  残る `plate ↔ p_pwr` `plate ↔ spresense` はペネトレータ以前からの既知の指摘)
- 内装との当たりは `spec/parent_interior_layout.py` の `check_penetrators()` が
  平面/高さの両方で見る。**`bcas212310g.scad` の `pen_*` と三重定義**なので
  位置を動かすときは両方直して、このアセンブリを再ビルドすること。

## 未反映 (モデルに入っていないもの) — 揃うまで干渉確認は完了していない

- LCD NHD-C0216CiZ + `parent_lcd_bracket` (北縁ストリップ予約済み・未設計)
- 発泡パッド、ベルクロ帯 ×2、M4 皿ねじ ×2 / 基板 M3 ねじ / トレイ M3×6 ×4
- 箱の 3D STEP (会員 DL 待ち。現在は図面 DXF からの自作モデル)
- ~~ケーブルグランド (南壁2)~~ → ✅ **ペネトレータ ×2 をモデル化 (2026-08-29)**。
  北壁 GPS 引込み ×1 と、**全配線 (C1/C3/C7)・箱内の端子台・ストレインリリーフ**は未反映
- 南壁**外側**: 未設計の防水ボックスマウント／浮子との干渉 (ペネトレータは壁外へ 22 mm 出る)
- SPRESENSE 給電線 (USB)、LiPo リード / XT30
- 箱の蓋・カバービス、蓋裏パッキン
- マストクランプ M5×4 ボルト頭 (箱底内側 ±28、プレート下 z<13.8 に収まる想定)

## 更新手順

配置を変えるときは `spec/parent_interior_layout.py` を先に直して assert を通し、
`parent_plate.scad` の対応変数と本 `placement.json` を追従させること (三重定義)。
南壁ペネトレータも同じく三重定義: `bcas212310g.scad` の `pen_x` / `pen_z` /
`spec/parent_interior_layout.py` の `PEN_*` / 本 `placement.json` の `ops`。
スペーサ長 (`LIPO_SPACER`) を変えたら `parent_lipo_tray.scad` の `spacer_l` と `hex_spacer` も直す。
