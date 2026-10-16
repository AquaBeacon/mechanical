"""Print geometry guard must distinguish a short bridge from a wide roof."""
import sys,unittest
from pathlib import Path
import trimesh

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from check_child_horizontal_support_free import bridge_regions


class SupportFreeGeometryTests(unittest.TestCase):
    def roof(self,width):
        outer=trimesh.creation.box([20,20,12]);outer.apply_translation([0,0,6])
        opening=trimesh.creation.box([width,11,8]);opening.apply_translation([0,0,2])
        return trimesh.boolean.difference([outer,opening],engine='manifold')

    def test_short_opening_is_identified_as_an_eight_mm_bridge(self):
        regions=bridge_regions(self.roof(8))
        self.assertEqual(len(regions),1)
        self.assertAlmostEqual(regions[0]['local_width_mm'],8,places=2)

    def test_wide_ceiling_exceeds_the_ten_mm_guard(self):
        regions=bridge_regions(self.roof(14))
        self.assertGreater(max(r['local_width_mm'] for r in regions),10)


if __name__=='__main__':unittest.main()
