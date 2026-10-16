"""Register a project-local Bambu PETG Basic card, then run unmodified topopt FEA.

No solver or acceptance logic is replaced. Compression/shear/Poisson data are
explicit estimates because the manufacturer's TDS does not provide them.
"""
import json
import sys
from pathlib import Path
from topopt import materials

NAME = 'BAMBU-PETG-BASIC-V3'
SOURCE = 'https://store.bblcdn.com/s1/default/cb94589bf7994fdcbfa833badefae9cd/Bambu_PETG_Basic_Technical_Data_Sheet.pdf'
fields = dict(Ex=2715., Ey=2715., Ez=2450., Gxy=1005.56, Gyz=907.41,
              Gzx=907.41, nu_xy=.35, nu_yz=.35, nu_zx=.35,
              Xt=50., Yt=50., Zt=29., Xc=50., Yc=50., Zc=29.,
              Sxy=28.86, Syz=16.74, Szx=16.74, density_kg_m3=1250.)
provenance = {k: 'estimated' for k in fields}
for k in ['Ex', 'Ey', 'Ez', 'Xt', 'Yt', 'Zt', 'density_kg_m3']:
    provenance[k] = 'literature_anchor'
card = materials.Orthotropic(card_id='bambu_petg_basic_v3_tds_minus_reported_spread',
    **fields, classification='manufacturer_tds_with_estimated_missing_constants',
    measured_for_specific_printer=False, source=SOURCE,
    conditions=dict(printer='Manufacturer X1 Carbon specimens; not this machine',
        nozzle_C=255, bed_C=70, speed_mm_s=150, infill=1.,
        values='TDS mean minus reported spread; NOT a statistical lower tolerance bound',
        missing='Poisson .35; shear modulus E/(2*(1+nu)); compression=tension; shear strength=tension/sqrt(3), unmeasured estimates',
        use='Dry room-temperature short-term prototype only; no creep/wet qualification'),
    provenance=provenance)
errors, warnings = card.check()
if errors:
    raise ValueError(errors)
materials.ORTHOTROPIC[NAME] = card
materials.MATERIALS[NAME] = materials.Material(NAME,2715,2450,.35,50,29,1.25,50,
    'Manufacturer V3 TDS with explicitly estimated missing properties; max_service_c50 is a provisional cap, not a tested rating.')

if __name__ == '__main__':
    from dataclasses import asdict
    if '--out' in sys.argv:
        out = Path(sys.argv[sys.argv.index('--out')+1]); out.mkdir(parents=True,exist_ok=True)
        (out/'material_card.json').write_text(json.dumps(asdict(card),indent=2)+'\n',encoding='utf-8')
    from topopt.cli.fea import main
    sys.exit(main(sys.argv[1:]))
