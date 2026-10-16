"""Current 40 N operating loads; rubber is a provisional estimate."""
from pathlib import Path
import json
import numpy as np
from geometry import load_at,closed_angle,dead_angle
ROOT=Path(__file__).resolve().parents[2]
def evaluate(v):
    rows=[load_at(v,a) for a in np.linspace(v['open_angle'],closed_angle(v),601)]
    return dict(target_closed_clamp_N=v['design_clamp_force_N'],closed=load_at(v,closed_angle(v)),dead=load_at(v,dead_angle(v)),peak_link=max(rows,key=lambda q:q['link_N']),peak_hand=max(rows,key=lambda q:abs(q['hand_vertical_N'])),peak_clamp=max(rows,key=lambda q:q['clamp_horizontal_N']),limitations=['Assumed rubber hardness and simple contact; not measured force'])
if __name__=='__main__':
    v=json.loads((ROOT/'parts/common/jigs/over_center_latch/parameters.json').read_text())
    out=ROOT/'assemblies/over_center_latch/_work/analysis/holding';out.mkdir(parents=True,exist_ok=True)
    report=evaluate(v);(out/'clamp_40N.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('Nominal closed horizontal clamp:',report['closed']['clamp_horizontal_N'])
