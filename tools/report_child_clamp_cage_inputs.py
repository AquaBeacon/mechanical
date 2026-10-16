"""Explain the frozen optimisation inputs; never launch optimisation or analysis."""
from pathlib import Path
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp'
CASE = PART/'_work/analysis/connected_cage_rubber1_v065'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    study = read(CASE/'study_cage.json')
    native = read(CASE/'opt/study_cage.json')
    material = read(PART/'spec/bambu_petg_basic_material.json')
    fea = read(CASE/'fea/finished_cage_fea.json')
    lines = ['# 今回のトポロジー最適化の全入力と近似','',
        '記録日: 2026-10-02。これは2026-10-01に実行した0.65版の入力説明であり、再最適化ではありません。空洞を埋める変更は別のCAD後処理です。', '',
        '入力の全項目・全荷重ベクトルは [study_cage.json](_work/analysis/connected_cage_rubber1_v065/study_cage.json)、実行設定・100反復履歴は [native最適化結果](_work/analysis/connected_cage_rubber1_v065/opt/study_cage.json)。', '',
        '## 初期モデルと座標','',
        '解析対象は後側の半割りケージ1個です。組立は同一部品をZ軸回り180°回転した2個ですが、FEAで2個を同時に接触解析していません。容器の下端をZ=0、管軸をZ、上向きを+Z、固定4穴の面側を-Yとしました。', '',
        '| 項目 | 実際の設定 |','|---|---|',
        '| WTE4 | 外径114.3 mm、管長200 mm。容器本体はFEA要素に含めない |',
        '| ゴム | 自由厚1 mm。0.2 mm圧縮、圧縮後0.8 mmは仮定。ゴムの材質・硬度・摩擦係数・弾性体はモデル化していない |',
        '| クランプ内半径 / 外半径 | 57.95 / 77.95 mm。接触内径115.9 mm、径方向厚20 mm |',
        '| 3段の中心 / 幅 | Z=40、100、160 mm / 各32 mm |',
        '| 連結設計領域 | Z=24～176 mmの連続半円筒。段間の自由領域は内半径58.45、外半径77.95 mm。3本の完全な半割りクランプと合成 |',
        '| 吊り耳までの領域 | 上端リングと吊り耳を包むhullを追加。特定の細い接続リブを事前指定していない |',
        '| 初期設計領域の外形 | X=-94.95～94.95、Y=-85.0～-0.799988、Z=24～210 mm。約189.90 ×84.20 ×186 mm |',
        '| 分割面 | Y=-0.8 mm。対向半体との隙間は1.6 mm |',
        '| M3締付け穴 | Ø3.5、X=±85.95、各段の中心Z±8。外部ワッシャØ12、締付けM3×60を12本 |',
        '| 固定4穴 | X=±18、各段の中心Z±8。36×16 mmピッチは既存の仮フレーム取合い。吊り解析の支持には使わない |',
        '| 固定面 / 工具座 | Y=-84.95 / -69.95。工具穴Ø9.4、OD8工具・OD9ワッシャを想定 |',
        '| 吊り穴 | 中心[0,-73,194]、軸X、Ø10.5 mm、幅24 mm |',
        '| 吊り耳の外形 | Y方向半径12、Z方向半径16 mm。穴口1.2 mm面取り |',
        '| 端部処理 | 外形/ゴム面0.6 mm面取り、既存根元R3、完成CADのM3入口0.3 mm面取り。機能座の段差は維持 |', '',
        '![初期設計領域](_work/images/cage_initial_model.png)', '',
        '上図は実際に入力した [design_space.stl](_work/analysis/connected_cage_rubber1_v065/design_space.stl)。CAD体積774060.424 mm³。初期密度は自由セル0.65、保持セル1、領域外/障害物0。初期モデルの全領域が最適化開始時から中実だったという意味ではありません。', '',
        '## 残す領域と材料を置かない領域','',
        '保持領域は各リングのゴム接触面から径方向4 mmの層、締付け穴・固定穴周辺の半径8.5 mmボス、正確な吊り耳です。CAD [preserve.stl](_work/analysis/connected_cage_rubber1_v065/preserve.stl) の体積182909.307 mm³。native格子では16保持ボディを全て接続する条件を指定しました。', '',
        '![保持領域](_work/images/cage_preserve_regions.png)', '',
        '障害物 [cuts.stl](_work/analysis/connected_cage_rubber1_v065/cuts.stl) は容器の連続収納空間、M3穴、工具/ワッシャ通路、吊り穴です。宣言CAD体積1624605.120 mm³で、設計領域外も含むため初期材料体積からこの全量を引く値ではありません。追加の障害物クリアランスは0 mmです。', '',
        '**密閉空洞禁止・サポート不要の制約は入れていませんでした。** フィルタ6 mmは密度の平滑化長さであり、全ての壁厚が6 mm以上になる保証ではありません。対称制約も指定していません。', '',
        '## 支持条件','',
        '唯一の支持は `rope_pin`。中心[0,-73,194]、軸X、半径7.25 mm、X範囲[-12.1,12.1]の円筒に入るPETG節点を、全てXYZ変位固定しました。穴半径5.25 mmなので、実質的には穴周囲約2 mmの材料を全周・全幅で固定する強い支持近似です。', '',
        '実ロープの接触面、ピン回転、ロープ角度、滑りを解く接触解析ではありません。固定4穴、蓋ねじ、容器底面、床面は解析支持にしていません。native出力のground_contactは印刷姿勢の床面情報で、吊り解析の固定条件ではありません。', '',
        '## 荷重と11ケース','',
        '完成機質量4 kgは既存案から引き継いだ仮定です。実測値ではありません。印刷部品を含む全質量として扱い、片側半体と吊り穴1個が全荷重を負担します。g=9.80665 m/s²、W=39.2266 N。CAD体積から別の自重を追加せず、4 kg分の重量を接触パッチへ分配しました。', '',
        '以下の合力は締付け予荷重を除いた追加荷重です。全ケースに同じ締付け予荷重を重畳します。段の分担は下/中/上の順で、各段6パッチに均等配分します。', '',
        '| ケース | 追加合力 [Fx,Fy,Fz] N | 下/中/上の分担 | 荷重区分 / 要求SF |',
        '|---|---|---|---|']
    for case in study['cases']:
        name = case['name']
        force = [0.,0.,0.]
        if 'static' in name: force[2]=-39.2266
        elif '2g' in name: force[2]=-78.4532
        if 'skew_x_' in name: force[0]=(-1 if '-1' in name else 1)*39.2266
        if 'skew_y_' in name: force[1]=(-1 if '-1' in name else 1)*39.2266
        share = [1/3]*3 if name=='preload_only' else [.5,.25,.25]
        if 'band' in name:
            share=[.25]*3; share[int(name[-1])-1]=.5
        sf=1.5 if case['load_class']=='abnormal' else 3
        lines.append(f'| `{name}` | {force} | '+('/'.join(f'{v*100:.1f}%' for v in share))+f' | {case["load_class"]} / {sf:g} |')
    radial = 600/-sum(math.sin(math.radians(-15-30*i)) for i in range(6))
    lines += ['',
        '2gは鉛直2倍荷重の静的近似です。偏荷重ケースは鉛直2gと横1gを同時に与えています。落下衝撃・時間応答・疲労・流体力・浮力・外水圧は解析していません。','',
        '締付け予荷重は12か所の外側ワッシャパッチへ各[0,+150,0] N。1段4か所で+600 NのY合力です。対応する6接触パッチに径方向外向きの反力を与え、1段のY合力を-600 Nにして釣り合わせます。実ボルトの締付けトルク、鋼の弾性、ナット/ワッシャ/ゴムの接触は解いていません。','',
        f'各接触パッチの径方向予荷重の大きさは `{radial:.9f} N`。θ=-15,-45,-75,-105,-135,-165°として `[R cosθ,R sinθ,0]`。ここへ段の分担率sを掛けた追加合力の1/6、`s·[Fx,Fy,Fz]/6`を足しています。','',
        '接触パッチは軸Z・半径9 mmの円筒、中心半径50.95 mm、Z範囲は各段中心±12 mm。円筒が実際のPETG要素と交わる部分へ荷重を配ります。ワッシャパッチは軸Y・半径6 mm、X=±85.95、Z=各段中心±8、Y範囲[-24.85,-23.75] mmです。','',
        '**この接触パッチへの指定力は摩擦保持を仮定した近似です。** ゴムの摩擦係数や締付け圧縮から引抜き限界を求めてはいません。11ケース全てに予荷重を含めるため、目的関数には締付け変形も含まれます。','',
        '全31領域を以下に転記します。軸方向範囲と円筒の材料との交差で節点を選択します。','',
        '| 領域 | 軸 | 中心 [X,Y,Z] mm | 半径 mm | 軸方向範囲 mm |','|---|---|---|---:|---|']
    for name,r in study['regions'].items():
        lines.append(f'| `{name}` | {r["axis"]} | '+str([round(v,9) for v in r['centre']])+f' | {r["r"]} | {r["range"]} |')
    card = material['orthotropic']
    lines += ['', '## 材料・積層方向','',
        '材料は `BAMBU-PETG-BASIC`、Bambu PETG Basicアップグレード版TDS V3.0に一部を合わせた**暫定異方性等価ソリッド**。材料原本は [bambu_petg_basic_material.json](spec/bambu_petg_basic_material.json)。メーカーの材料試験値は [BAMBU_PETG_BASIC.md](BAMBU_PETG_BASIC.md) に保存した資料を参照しています。', '',
        '材料座標のxはラスタ方向（設計Z）、zは積層方向（設計Y）、yは残りの層内方向です。materialのEx等の添字は設計座標のXYZと同一ではありません。印刷姿勢はX+90°回転、100%インフィル、外周8、0.20 mm、0.4 mmノズル。荷重軸Zを層内に置きます。', '',
        '| 定数 | 数値 MPa（νは無次元） | 根拠 |','|---|---:|---|']
    for key in ['Ex','Ey','Ez','Gxy','Gyz','Gzx','nu_xy','nu_yz','nu_zx','Xt','Xc','Yt','Yc','Zt','Zc','Sxy','Syz','Szx']:
        lines.append(f'| {key} | {card[key]} | {card["provenance"][key]} |')
    lines += ['',
        '密度1250 kg/m³（1.25 g/cm³）。乾燥・23°C・浸水0時間の短期値です。Ex=2780−65、Ez=2550−100、Xt=51−1、Zt=35−6を採用しましたが、「平均−公表ばらつき」は統計的な設計許容値ではありません。Ey、横ラスタ引張、せん断、圧縮、ポアソン比は実フィラメント/プリンタで実測していない仮値です。曲げ強度・Charpy値を静的引張強度に置き換えていません。', '',
        '実スライサの100% zig-zagラスタは層ごとに交互方向です。材料カードの単一ラスタZは近似で、その交互積層を忠実に再現していません。濡れ、温度変化、クリープ、実機の層間強度は未校正です。', '',
        '## 最適化設定','',
        '目的は11ケースのコンプライアンス（荷重による柔らかさ）を各ケース初期値で正規化し、等重みで合計した値の最小化です。体積上限と材料軸での応力制約を課しています。1 mmの最大変位は後段FEAの合否基準で、MMA問題に直接最大変位制約を追加してはいません。','',
        '| 設定 | 使用値 |','|---|---|',
        '| nativeツール | topopt 1.0.0、MMA |',
        '| 最適化格子 | 2 mm、99×76×98、原点[-98.95,-89,19.95] mm |',
        '| 格子の設計領域 / 保持 / 自由体積 | 775824 / 190512 / 585312 mm³。材料域96978セル、自由域73164セル |',
        '| 自由領域体積率 | 0.65。保持材料を除いた部分の値で、部品全体を65%にする指定ではない |',
        '| 密度フィルタ | 6 mm |',
        '| 投影閾値η / β | 0.5 / 1から最終16 |',
        '| SIMPペナルティ | 1から最終3 |',
        '| 応力判定 | 材料軸の最大応力、引張/圧縮/せん断を個別判定 |',
        '| 応力集約 / 緩和 | p-norm=8、ρ^0.5、全サンプル、adaptive scale damping=0.5 |',
        '| 要求安全率 | normal=3、abnormal=1.5 |',
        '| 更新move limit | 0.2、move_taper=true、volume_exact=false |',
        '| 対称 / オーバーハング | 未指定 / 無効 |',
        '| 反復 | 100回。収束連続回数要件5。最大反復で終了、完全収束していない |',
        '| 線形ソルバ | CUDA、RTX 4060 Ti、multigrid、mixed32 |', '',
        '実際のnative設定を省略せず掲載します。材料・荷重の全生値は冒頭のstudy JSONにあります。', '',
        '```json',json.dumps(native['settings'],ensure_ascii=False,indent=2),'```','',
        '## 抽出・完成形状の解析・印刷条件','',
        '抽出閾値0.4/0.5/0.6を比較し0.4を選択しました。nativeの理由は「全検査を通る候補はなく、連結候補の中で最も強い」であり、合格候補の選択ではありません。2 mm格子では最細部4 mmを2要素で表現し、3要素以上という解像度基準を満たしませんでした。', '',
        '仕上げは1 mmの再サンプル格子、1 mmの平滑化。保持形状を追加、障害物を除去し、元のSCADで正確な穴・座面・ゴム面・外形を復元しました。完成STLの再解析は1 mm格子の単一メッシュ。メッシュ収束の確認ではありません。', '',
        '| 元の完成STLケース | 最大変位 mm | 最悪局所SF | p99.5 SF | native判定 |','|---|---:|---:|---:|---|']
    for row in fea['cases']:
        lines.append(f'| {row["case"]} | {row["max_displacement_mm"]:.6f} | {row["min_safety_factor"]:.4f} | {row["safety_factor_p99_5"]:.4f} | {row["pass"]} |')
    lines += ['',
        '原形状の最適化native判定はFAIL（最終FEAの格子解像度）。完成STLの1 mm再解析も、X負方向の偏荷重で1.079 mm > 1 mmとなりFAIL。応力制約の満足やCGの1111/1111収束は、形状/メッシュの完全収束や使用合格ではありません。', '',
        '独立解析は元の完成STL、同じ材料・荷重・支持、`--map volume`、表面細分化あり、HXT Gmsh、目標10/5/2.5 mmの3段収束を要求しましたが、最初の四面体生成で停止しました。CalculiXの解析と収束判定は実施できていません。study説明欄のsurface mapping表記より実行記録のvolume指定を優先します。', '',
        '印刷はX1 Carbon、Bambu PETG Basic、Textured PEI、255°C/70°C、0.4 mmノズル、0.20 mm、100% zig-zag、外周8、上下8層、ラスタ基準90°、5 mm外ブリム、normal(auto)サポート、ベッドからのみ。1個/プレート、同一半体を2個。自動姿勢変更は使用していません。', '',
        '## 先行探索と今回の変更','',
        '先行0.50版は [別study](_work/analysis/connected_cage_rubber1/study_cage.json) に保持。100反復、同じ主要寸法・初期モデル外形/体積で、10ケース（Y偏荷重は+方向のみ `skew_y_2g`）。採用候補の0.65版は上記11ケースです。体積率以外に荷重ケースも変更しているため、体積率だけの純粋な比較ではありません。', '',
        '2026-10-02は再最適化しません。既存密度面にあった約355 mm³の密閉空洞を内側境界の除去で埋め、同じSCADで完成形状を再生成しています。外表面・穴・座面を維持し、外形と内部シェル数を検査します。今回の中実化後にFEA/CalculiXは実行していないため、上表は変更前の結果です。', '',
        '新しい印刷入口は既存assemblyの [PRINT.md](../../../../../assemblies/child_clamp_suspension/parts/PRINT.md)。変更記録は `_work/analysis/connected_cage_rubber1_solid/void_free_revision.json`。変更前の原本は旧caseの `before_closed_void_fill/` に保持。', '',
        '元入力のSHA-256: `'+hashlib.sha256((CASE/'study_cage.json').read_bytes()).hexdigest()+'`。新たな取付相手、質量、ゴム特性の確認を済ませたという意味ではありません。']
    (PART/'OPTIMIZATION_INPUTS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(PART/'OPTIMIZATION_INPUTS.md')


if __name__=='__main__':
    main()
