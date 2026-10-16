"""Persist run results and execute one reviewed refinement after the initial GPU queue.

No FEA implementation here: all solving is delegated to the installed topopt CLI.
Run detached with --follow; without arguments only writes the current snapshot.
"""
from pathlib import Path
import datetime, html, json, os, subprocess, sys, time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assemblies/child_single_camera_topopt'
NAMES = {'child_cam_bridge':'カメラ取付部', 'child_jaw_gate':'可動ゲート', 'child_core_frame':'コアフレーム'}
STATE = OUT / 'refinement_status.json'

def read(path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def write_state(state):
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')

def snapshot():
    queue = read(OUT / 'exploration_status.json')
    refinement = read(STATE)
    status = {r['part']:r['status'] for r in queue.get('runs',[])}
    rows = []
    sections = []
    records = []
    runs = [(n,'exploration','study',status.get(n,'waiting')) for n in NAMES]
    runs.append(('child_cam_bridge','refined','study_refined',refinement.get('status','prepared')))
    for name,phase,stem,current in runs:
        folder = OUT / name / phase / '03_optimization'
        result = read(folder / f'{stem}.json')
        title = NAMES[name] + ('（2 mm再計算）' if phase=='refined' else '（初回3 mm）')
        record = {'part':name,'phase':phase,'status':current}
        if result:
            cases = result.get('final_fea',[])
            sf = min((c['min_safety_factor'] for c in cases),default=float('nan'))
            p99 = min((c['safety_factor_p99_5'] for c in cases),default=float('nan'))
            disp = max((c['max_displacement_mm'] for c in cases),default=float('nan'))
            reason = result.get('termination_reason','unknown')
            passed = result.get('pass') is True and sf >= 3 and reason != 'max_iterations'
            judgement = '探索チェック通過／製造未検証' if passed else '未合格'
            rows.append(f'| {title} | {judgement} | {sf:.2f} / {p99:.2f} | {disp:.3f} | {reason} |')
            record.update(min_safety_factor=sf,safety_factor_p99_5=p99,max_displacement_mm=disp,
                          termination_reason=reason,tool_pass=result.get('pass'),judgement=judgement)
            prefix = f'{name}/{phase}/03_optimization'
            image = folder / f'{stem}_topo.png'
            pic = f'<img src="{prefix}/{image.name}">' if image.exists() else ''
            sections.append(f'<section><h2>{html.escape(title)}：{judgement}</h2><p>最低安全率 {sf:.2f} / p99.5 {p99:.2f}、最大変位 {disp:.3f} mm、{reason}</p>{pic}<p><a href="{prefix}/report.md">詳細レポート</a> · <a href="{prefix}/{stem}.json">解析結果JSON</a> · <a href="{prefix}/{stem}_final.stl">材料配置STL（製造用ではありません）</a></p></section>')
        else:
            label = {'running':'実行中','waiting':'順番待ち','prepared':'setup済み','finished':'終了・結果なし','failed':'実行失敗'}.get(current,current)
            rows.append(f'| {title} | {label} | — | — | — |')
        records.append(record)
    now = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
    table = '\n'.join(['| 部品 | 状態 | 最低安全率 / p99.5 | 最大変位 mm | 終了理由 |','|---|---|---:|---:|---|'] + rows)
    text = f'''# 子機外装：単眼カメラ・縦向きライトのtopopt

更新：{now}

ユーザーの2026-09-10の指示で最適化実行を承認済み。カメラ1台、右側の縦向きライト1灯に変更。
これは設計候補の探索記録です。完成部品・製造承認ではありません。

追記：[自重の確認記録](gravity_audit.md)。図のG矢印位置は作用点ではありません。探索中に自重が密度変化に追従しない実装を確認しており、その影響は未検証です。

{table}

## 配置・除外領域・荷重

- [setupの3D図と全17荷重ケース](review.html) / [最適化結果の画像](results.html)
- カメラは中央前方に1台。取付柱との干渉を避けて従来より前へ9 mm。レンズ中心 (0,129,125) mm。
- ライトは右側、長軸をZ方向。仮寸法 Ø40 × 100 mm、中心軸 (80,-75)、高さ50〜150 mm。実物の光の出射方向は未確認。
- 配線はØ6 mm＋周囲1 mmの予約空間。耐圧容器、カメラ・視野、ライト、TD04A・取付部、配線、手の進入空間を除外。設計空間外の機器も配置図に表示。
- 持ち手の握り部を保持し、持上げ+200 Nのケースを追加。ライトの自重9 Nと偏心モーメント324 Nmm、TD04Aの取付部荷重9.4 Nを考慮。これらは仮の質量・3g条件。
- 荷重図は36本の入力荷重矢印と3本の自重矢印。別々の荷重ケースであり、全矢印を同時に適用しません。
- 手と配線の重なりは1 mmボクセルで0。詳細は [幾何・矢印チェック](review_checks.json)。実物のケーブル曲げ半径と組立・工具の確認は残っています。

## 実行条件と判定の範囲

初回はPETG、要求安全率3、3 mmボクセル、80反復、quick探索。ゲート・コアの薄い6 mm部分は2要素しかなく、メッシュ精度の合格条件を満たしません。
カメラ取付部の再計算は同じ荷重・要求安全率で2 mm、フィルタ6 mm、自由領域の体積率0.30、160反復。setupの実測見積りは約39分（19〜58分）。初回3部品の後に順次実行します。

最低安全率とp99.5の両方を記録します。p99.5だけで合格としません。最大反復到達は収束ではありません。
今回のquick出力は材料配置であり、ねじ穴等を持つ最終パラメトリックCADではありません。CalculiX独立再解析、メッシュ収束、実際の造形・締結・引抜き検証は未実施です。
取付位置・保持領域の多くは既存CADから与えた入力であり、全形状を最適化が自動決定したわけではありません。

実行状態： [初回キュー](exploration_status.json) / [再計算](refinement_status.json)。結果ページはローカル集計プログラムが更新します。既存の製造用部品は置き換えていません。
'''
    (OUT/'README.md').write_text(text,encoding='utf-8')
    head = f'<!doctype html><html lang="ja"><meta charset="utf-8"><meta http-equiv="refresh" content="60"><title>子機外装 topopt結果</title><style>body{{font-family:system-ui;max-width:1400px;margin:32px auto;background:#edf1f5;color:#203040}}section{{background:white;padding:20px;margin:24px 0}}img{{width:100%}}p{{line-height:1.8}}</style><h1>単眼カメラ・縦向きライト：最適化結果</h1><p>更新 {now}。未完成の材料配置です。製造用モデルではありません。<a href="README.md">状態と数値の一覧</a> · <a href="review.html">配置・全荷重図</a></p>'
    (OUT/'results.html').write_text(head+''.join(sections)+'</html>',encoding='utf-8')
    (OUT/'results_summary.json').write_text(json.dumps({'updated':now,'runs':records},ensure_ascii=False,indent=2),encoding='utf-8')

if __name__ == '__main__':
    if '--follow' not in sys.argv:
        snapshot()
        sys.exit(0)
    if STATE.exists():
        raise SystemExit('Refinement state already exists; refusing a duplicate run.')
    state = {'status':'waiting','supervisor_pid':os.getpid(),'created':time.time()}
    write_state(state)
    while not read(OUT/'exploration_status.json').get('finished'):
        snapshot()
        time.sleep(30)
    folder = OUT/'child_cam_bridge'
    setup = read(folder/'setup_refined/study_refined_setup.json')
    if setup.get('ok') is not True:
        state.update(status='failed',reason='Refined setup is not valid');write_state(state);snapshot()
        raise SystemExit(1)
    dest = folder/'refined';dest.mkdir(exist_ok=True)
    args = [sys.executable,'-m','topopt','run',str(folder/'study_refined.json'),'--model',str(dest),'--iters','160','--quick']
    env = os.environ.copy();env['PYTHONIOENCODING']='utf-8'
    env['TOPOPT_FREECAD']='C:/Users/ryupc/AppData/Local/Programs/FreeCAD 1.0/bin/freecadcmd.exe'
    with (dest/'run.log').open('w',encoding='utf-8') as log:
        p = subprocess.Popen(args,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT)
        state.update(status='running',pid=p.pid,started=time.time(),command=args);write_state(state)
        while p.poll() is None:
            snapshot();time.sleep(30)
        state.update(status='finished',exit_code=p.returncode,finished=time.time());write_state(state)
    snapshot()
