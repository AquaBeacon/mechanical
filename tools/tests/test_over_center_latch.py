"""Check force/moment and virtual-work consistency of the current mechanism."""
import json,sys,unittest
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'spec/over_center_latch'))
import dji_geometry as g

class LatchMechanicsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.v=json.loads((ROOT/'parts/common/jigs/over_center_latch/parameters.json').read_text(encoding='utf-8'))

    def test_contact_is_unilateral_and_closure_restores(self):
        v=self.v
        for theta in np.linspace(v['open_angle'],g.closed_angle(v),101):
            q=g.load_at(v,theta)
            if not q['normal_rubber_N']:continue
            self.assertGreaterEqual(q['lip_N'],0)
            self.assertAlmostEqual(q['K'][2],v['catch_height']+v['toe_half_height'],places=8)
        q=g.load_at(v,g.closed_angle(v))
        self.assertAlmostEqual(q['clamp_horizontal_N'],v['design_clamp_force_N'],places=5)
        self.assertLess(q['hand_vertical_N'],0)
        self.assertGreater(g.closed_angle(v)-g.dead_angle(v),5)

    def test_force_moment_balance_and_virtual_work(self):
        v=self.v
        for theta in np.linspace(v['open_angle']+1,g.closed_angle(v)-1,4):
            q=g.load_at(v,theta);B=np.array(q['B'])[[0,2]]
            force_points=[(q['link_force_on_hood'],q['B']),
                (q['rubber_force_on_hook'],q['rubber_point']),
                (q['lip_force_on_hook'],q['K']),([0,0,-q['hand_vertical_N']],q['hand_point'])]
            total=np.zeros(2);moment=0.;power=0.
            h=1e-4;lo=g.pose(v,theta-h);hi=g.pose(v,theta+h)
            velocityB=(np.array(hi['B'])[[0,2]]-np.array(lo['B'])[[0,2]])/(2*h)
            omega=np.radians(hi['delta_deg']-lo['delta_deg'])/(2*h)
            for f,p in force_points:
                f=np.array(f)[[0,2]];r=np.array(p)[[0,2]]-B
                total+=f;moment+=r[0]*f[1]-r[1]*f[0]
                velocity=velocityB+omega*np.array([-r[1],r[0]])
                power+=float(f@velocity)
            self.assertLess(np.linalg.norm(total),1e-8)
            self.assertLess(abs(moment),1e-7)
            self.assertLess(abs(power),1e-6)

if __name__=='__main__':unittest.main()
