"""Slice the parent/child bent straps with the installed X1C profiles.

Default: supports auto, all surfaces, 45 degrees, for detection. --production:
support disabled to inspect the actual short bridge paths. A successful slice
alone is never a support-free or physical printing certification.
"""
from pathlib import Path
import hashlib
import json
import sys
from topopt import slicer
from topopt.cli import slice as native

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'assemblies/td04a_fixture'

def main():
    production='--production' in sys.argv
    target=A/'print_jobs/cable_clearance_r6' if production else A/'_work/analysis/slicing/support_detection'
    slicer.FILAMENT_FAMILY['PETG']='Bambu PETG Basic'
    original=native._write_presets;pick=slicer.pick_process
    slicer.pick_process=lambda presets,machine,layer:pick(presets,machine,0.12 if abs(float(layer)-.1)<1e-8 else layer)
    overrides={}
    def presets(*args,**kwargs):
        files=original(*args,**kwargs)
        p=Path(files['process']);d=json.loads(p.read_text());d.update(overrides)
        p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');return files
    native._write_presets=presets
    rows=[]
    for e in json.loads((A/'parts/manifest.json').read_text(encoding='utf-8'))['parts']:
        stem=e['stem'];layer=.2
        overrides.update(layer_height=str(layer),wall_loops='8',sparse_infill_density='100%',
                         sparse_infill_pattern='alignedrectilinear',top_shell_layers='6',bottom_shell_layers='6',
                         brim_width='5',brim_type='outer_only',support_threshold_angle='45',
                         support_on_build_plate_only='0',curr_bed_type='Textured PEI Plate')
        source=A/'parts'/e['file'];job=target/stem;job.mkdir(parents=True,exist_ok=True)
        supports='none' if production else 'auto'
        code=native.main([str(source),'--out',str(job),'--printer','X1C','--material','PETG',
                          '--layer-mm',str(layer),'--supports',supports,'--orient','keep',
                          '--bed-type','Textured PEI Plate','--timeout','240','--quiet'])
        report=json.loads((job/'slice.json').read_text())
        row=dict(file=e['file'],source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                 layer_mm=layer,supports=supports,exit_code=code,bed_fits=report.get('bed_fits'),
                 passed=report.get('pass'),warnings=report.get('warnings'),error=report.get('error'),
                 grams=report.get('filament_g'),seconds=report.get('print_time_s'),
                 support_filament_mm=slicer.support_mm(report.get('filament_by_feature_mm',{})))
        rows.append(row)
        print(json.dumps(row),flush=True)
    (target/'validation.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
    return 0 if all(r['exit_code']==0 and r['passed'] and r['bed_fits'] for r in rows) else 1
if __name__=='__main__':sys.exit(main())
