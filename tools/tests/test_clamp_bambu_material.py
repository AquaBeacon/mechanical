"""The manufacturer input must not silently strengthen unrelated PETG runs."""
import dataclasses
import importlib.util
from pathlib import Path
import unittest


class BambuMaterialTests(unittest.TestCase):
    def test_card_registration_and_missing_property_policy(self):
        from topopt.materials import MATERIALS, ORTHOTROPIC, material_model
        baseline=dataclasses.asdict(ORTHOTROPIC['PETG'])
        generic=MATERIALS['PETG']
        module_path=Path(__file__).resolve().parents[1]/'clamp_bambu_material.py'
        spec=importlib.util.spec_from_file_location('clamp_bambu_material_test',module_path)
        module=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.register()
        _,card,_=material_model('BAMBU-PETG-BASIC',infill=1,walls=8)
        self.assertEqual([],card.check()[0])
        self.assertEqual((2715,2715,2450),(card.Ex,card.Ey,card.Ez))
        self.assertEqual((50,29),(card.Xt,card.Zt))
        self.assertEqual(1250,card.density_kg_m3)
        self.assertFalse(card.measured_for_specific_printer)
        for name in ['Yt','Xc','Yc','Zc','Sxy','Syz','Szx','Gxy','Gyz','Gzx','nu_xy','nu_yz','nu_zx']:
            self.assertEqual(baseline[name],getattr(card,name),name)
        self.assertEqual(baseline,dataclasses.asdict(ORTHOTROPIC['PETG']))
        self.assertEqual(generic,MATERIALS['PETG'])


if __name__=='__main__':
    unittest.main()
