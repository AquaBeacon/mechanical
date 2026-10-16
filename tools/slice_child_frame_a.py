"""Native topopt/Bambu slice with the frame's declared manufacturing inputs.

Only the prepared process JSON is overridden; slicing and result parsing are
the installed native pipeline. No printer, installed preset or solver changes.
"""
from pathlib import Path
import hashlib,json,sys
from clamp_bambu_material import register

ROOT=Path(__file__).resolve().parents[1]
PART=ROOT/'parts/child/exterior/printed/child_exterior_structural_frame'
CASE=PART/'_work/analysis/frame_a_rim_thickness'


def main():
    register()
    from topopt import slicer
    from topopt.cli import slice as native
    slicer.FILAMENT_FAMILY['BAMBU-PETG-BASIC']='Bambu PETG Basic'
    original=native._write_presets
    overrides=dict(wall_loops='8',sparse_infill_density='100%',sparse_infill_pattern='alignedrectilinear',
                   infill_direction='0',brim_width='5',brim_type='outer_only',support_threshold_angle='45',curr_bed_type='Textured PEI Plate')
    def inputs(*args,**kwargs):
        files=original(*args,**kwargs)
        p=Path(files['process']);data=json.loads(p.read_text());data.update(overrides)
        p.write_text(json.dumps(data,indent=1)+'\n',encoding='utf-8')
        return files
    native._write_presets=inputs
    rows={}
    for name in (sys.argv[1:] or ['lower_minus','lower_plus','upper_minus','upper_plus','splice']):
        source=PART/f'child_exterior_structural_frame_{name}.stl'
        out=CASE/'slice'/name;out.mkdir(parents=True,exist_ok=True)
        code=native.main([str(source),'--out',str(out),'--printer','X1C','--material','BAMBU-PETG-BASIC',
                          '--layer-mm','0.2','--supports','auto','--orient','keep','--timeout','180','--quiet'])
        rows[name]=dict(exit_code=code,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),process_overrides=overrides,
                        note='Slicer raster alternates by layer; provisional material card is not calibrated to this toolpath. Slicing does not certify structural strength.')
        print(name,'slice exit',code,flush=True)
    (CASE/'slice/manufacturing_inputs.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
