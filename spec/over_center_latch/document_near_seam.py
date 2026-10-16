"""Document the near-seam revision without reusing old structural results."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'parts/common/jigs/over_center_latch';ASM=ROOT/'assemblies/over_center_latch'
v=json.loads((P/'parameters.json').read_text());v['closed_angle_deg']=150
(P/'parameters.json').write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
for path in [P/'README.md',ASM/'README.md']:
    s=path.read_text(encoding='utf-8')
    s=s.replace('閉リンク角170°','閉リンク角150°').replace('受けの局所穴X=8','受けの局所穴X=18.6').replace('X=23 mm','X=12.4 mm')
    s=s.replace('構造解析のメッシュ収束が未確認で、固定部の局所応力も残っています。','爪・受けを継ぎ目へ寄せた今回の形状は構造解析を再実行していません。以前の解析は旧形状の記録です。')
    s=s.replace('構造解析の収束FAILと固定部の局所応力が残っています。','今回の爪位置と閉じ角では構造解析を再実行していません。以前の解析は旧形状の記録です。')
    s=s.replace('構造解析は部品内','旧形状の構造解析は部品内')
    line='\n継ぎ目X=2.1から爪の80°接触面中心X=9.6まで7.5 mm（実際の分布反力中心は約7.47 mm）。保持段の接触点は約7.81 mm。B軸から接触面までの水平距離は約16.53 mmです。台の外形・取付穴の世界座標は維持し、受けの局所取付穴X=18.6へ補正しました。閉じ角150°に合わせ、死点付近の過大なゴム圧縮を抑えています。\n'
    s=s.replace('\n## 必要な購入品',line+'\n## 必要な購入品') if path==P/'README.md' else s+line
    path.write_text(s,encoding='utf-8')
calc=ROOT/'spec/over_center_latch/HOLDING_CALCULATION.md'
s=calc.read_text(encoding='utf-8'); start=s.index('## 材料と構造解析の前提')
history=s[start:].replace('## 検証結果','## 旧形状の検証結果（現在の形状の強度根拠には使用しない）')
history=history.replace('今回の最終STL','爪位置変更前のSTL').replace('最終STL','変更前STL').replace('最終STEP','変更前STEP')
calc.write_text('# 継ぎ目から7.5 mmへ寄せたDJI式ラッチ（2026-10-10）\n\n爪・受けを継ぎ目へ移動。接触面中心X=9.6、継ぎ目X=2.1で7.5 mm。受け基準X=12.4、閉角150°。台の外形と世界座標の6取付穴、80°面、台厚6/8 mm、後端操作部を維持。閉時40 Nはゴム概算による目標で、実測校正が必要です。\n\n機構とCADの最新結果は下記の生成記録を参照。構造解析は位置変更前の記録を保存し、今回の強度評価として使用しません。\n\n- 機構：assemblies/over_center_latch/_work/analysis/kinematics/report.json\n- CAD：同_work/analysis/verification/transverse_sweep.json、step_report.json\n- 変更前一式：parts/common/jigs/over_center_latch/_work/analysis/dji_groove40N_near_seam_20261010/before\n\n'+history,encoding='utf-8')
strength=ASM/'_work/analysis/verification/strength_report.json'
if strength.exists():
    strength.write_text(json.dumps(dict(status='NOT_RUN_FOR_REVISED_GEOMETRY',reason='Contact moved near seam and closed angle changed. Previous FEA retained in revision snapshot; not applicable to current geometry.'),indent=2)+'\n',encoding='utf-8')
