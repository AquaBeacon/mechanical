# X1-Carbon 造形性監査

実施日: 2026-08-01 / 対象: `parts/` 以下の 3Dプリント部品 30 点 (購入品・基板は除外)

再実行:

```powershell
$env:PYTHONIOENCODING='utf-8'
$S = "C:\Users\ryupc\.claude\skills\3d-print-design\scripts"
python "$S\printability.py" parts --audit --json docs\x1c_audit.json
```

判定基準は **実用造形枠 250 × 250 × 250 mm**。
公称は 256³ だが、パージ/ワイプ領域とプレート端の定着不良を見込んで 250 で設計する。

## 1. 造形枠に入らない部品 (3 点) — 要分割

| 部品 | 外形 (モデル座標) | 分割案 | 備考 |
|---|---|---|---|
| `child_frame_plate` | 200 × **300** × 6 | Y を 150 × 2 | 構成 A のベースプレート |
| `child_tray_deck` | 75 × **281** × 24 | Y を 140.5 × 2 | 構成 A の内装トレイ。旧仮値のまま |
| `child_vtray_deck_t300` | 97 × 14 × **304** | Z を 152 × 2 | t300 バリアント。t200 (204mm) は収まる |

分割位置はモデル座標なので `.scad` にそのまま入れられる。
接合は `assets/scad_modules/joints.scad` を使う (ピン + ボルトフランジ)。
**分割後は接合部を弱点として `fea_check.py` をやり直すこと。**

- 3 点とも構成 A / t300 バリアントに属する。本線が構成 B (t200) のままなら
  `child_vtray_deck_t300` 以外は実害がない。構成の確定が先。

## 2. サポートが多い部品 (最良姿勢でもオーバーハング 15% 超)

| 部品 | 最良姿勢 | オーバーハング |
|---|---|---|
| `xdcr_clamp_body` | +Z up | 27.7% |
| `xdcr_poolside_jig_hook` | -Y up | 25.6% |
| `child_clamp_base` | +Z up | 25.5% |
| `child_tray_rib` | -Y up | 23.1% |
| `xdcr_socket_child` | +Z up | 22.7% |
| `child_bottom_guard` | +Z up | 22.1% |
| `test_bracket` | +Y up | 20.7% |
| `parent_mast_clamp` | +Z up | 18.1% |
| `child_light_clamp` | +X up | 16.5% |

クランプ類が並んでいるのは当然で、内側の円筒面が必ず天井を作るため。
45° 面取り (チャンファ) を入れるとサポートは大きく減る。フィレットでは減らない。

## 3. 最小肉厚

| 部品 | 最薄部 (p1) | 判定 |
|---|---|---|
| `child_tray_rib` | 0.73 mm | **0.4mm ノズルの 2 周 = 0.8mm を下回る** |

`child_tray_rib` の最薄部は 1 周ぶんしか出ず、実質ギャップフィルになる。
1.6 mm (= 0.4 × 4 周) 以上にすること。

## 4. 印刷姿勢と強度の関係 (重要)

FDM は**層間 (Z) の引張が面内 (XY) の 5〜7 割しかない**。
姿勢はスライサ設定ではなく**構造の決定事項**なので、部品の `.md` に必ず書く。

`child_shell_aft` は子機全体を吊り耳で吊る部品で、吊り下げ荷重はモデル Z 方向。
モデル姿勢のまま (+Z up) 印刷すると、その引張がすべての層界面に直交する。

```powershell
python "$S\printability.py" parts\child\exterior\printed\child_shell_aft\child_shell_aft.stl --load-axis 0,0,1
```

→ 最良姿勢は **+Y up** (荷重が層面内、cos = 0.00)。造形枠にも収まる (196 × 234 × 121)。

## 5. まだ見ていないこと

この監査は**幾何形状だけ**を見ている。荷重をかけた結果ではない。

- 各部品の荷重ケースが `.md` に書かれていないため、安全率・たわみは未評価。
- `fea_check.py` を回すには「何 N・どこから・どこで受ける」を先に決める必要がある。
- 吊り下げ・持ち運び・テザー引きの 3 ケースは全部品に効くので、まずそこから。
