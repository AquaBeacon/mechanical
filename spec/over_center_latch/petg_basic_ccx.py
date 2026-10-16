"""Run the existing CalculiX CLI with the same project PETG material card."""
from pathlib import Path
from dataclasses import asdict
import json,sys
from petg_basic_fea import card
from topopt.cli.ccx import main

if __name__=='__main__':
    if '--out' in sys.argv:
        out=Path(sys.argv[sys.argv.index('--out')+1]);out.mkdir(parents=True,exist_ok=True)
        (out/'material_card.json').write_text(json.dumps(asdict(card),indent=2)+'\n',encoding='utf-8')
    sys.exit(main(sys.argv[1:]))
