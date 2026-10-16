"""Slice a candidate with the assembly's X1C/PETG Basic process settings."""
from pathlib import Path
import argparse, hashlib, json
from topopt import slicer
from topopt.cli import slice as native

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--supports',choices=['auto','tree'],default='auto')
    args=ap.parse_args()
    args.out.mkdir(parents=True,exist_ok=False)
    slicer.FILAMENT_FAMILY['PETG']='Bambu PETG Basic'
    original=native._write_presets
    overrides=dict(wall_loops='8',sparse_infill_density='100%',
        sparse_infill_pattern='alignedrectilinear',infill_direction='0',
        brim_width='5',brim_type='outer_only',support_threshold_angle='45',
        curr_bed_type='Textured PEI Plate')
    def presets(*a,**kw):
        files=original(*a,**kw);p=Path(files['process'])
        data=json.loads(p.read_text());data.update(overrides)
        p.write_text(json.dumps(data,indent=1)+'\n',encoding='utf-8')
        return files
    native._write_presets=presets
    code=native.main([str(args.source),'--out',str(args.out),'--printer','X1C',
        '--material','PETG','--layer-mm','0.2','--supports',args.supports,
        '--orient','keep','--bed-type','Textured PEI Plate','--timeout','240','--quiet'])
    report=json.loads((args.out/'slice.json').read_text())
    report['candidate_sha256']=hashlib.sha256(args.source.read_bytes()).hexdigest()
    report['process_overrides']=overrides
    (args.out/'candidate_slice.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:report.get(k) for k in ['pass','bed_fits','filament_g',
        'support_filament_g','print_time_s','error','warnings']}),flush=True)
    raise SystemExit(code)

if __name__=='__main__':main()
