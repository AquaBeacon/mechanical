"""Refresh revision notes from generated mechanism/CAD results."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2];P=ROOT/'parts/common/jigs/over_center_latch';ASM=ROOT/'assemblies/over_center_latch'
r=json.loads((ASM/'_work/analysis/kinematics/report.json').read_text())
table='\n## 今回の機構概算\n\n| 項目 | 値 |\n|---|---:|\n'
for key,value in [('閉時水平締付力',f"{r['closed']['clamp_horizontal_N']:.2f} N"),('死点角',f"{r['dead_angle_deg']:.3f}°"),('死点から閉位置まで',f"{r['snap_travel_deg']:.3f}°"),('途中最大水平締付力',f"{r['peak_clamp']['clamp_horizontal_N']:.2f} N"),('最大リンク合計圧縮力',f"{r['peak_link']['link_N']:.2f} N"),('最大鉛直操作力',f"{r['peak_hand']['hand_vertical_N']:.2f} N"),('閉時の台着座反力',f"{-r['closed']['hand_vertical_N']:.2f} N"),('閉時ゴム圧縮',f"{r['closed']['compression_mm']:.4f} mm"),('最大局所ゴム圧縮',f"{r['max_compression_mm']:.4f} mm")]:table+=f'| {key} | {value} |\n'
table+='\n摩擦・PETGの変形・ゴム積層の接着と横膨れ・軸のガタを含まない公称概算です。実測校正と今回の形状に対する強度検証が必要です。短くした水平距離だけで力倍率を求めず、80°面と保持段の反力を含むB回りのモーメントを解いています。\n\n'
path=ROOT/'spec/over_center_latch/HOLDING_CALCULATION.md';s=path.read_text(encoding='utf-8');s=s.replace('## 材料と構造解析の前提',table+'## 材料と構造解析の前提');path.write_text(s,encoding='utf-8')
for path in [P/'README.md',ASM/'README.md']:
    s=path.read_text(encoding='utf-8').replace('約42.1 mm','約43.1 mm').replace('約42 mm','約43 mm')
    path.write_text(s,encoding='utf-8')
