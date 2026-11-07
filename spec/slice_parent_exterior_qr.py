"""Slice Rev.2 portable meshes using the installed X1C/PETG Basic profiles."""
from pathlib import Path
import json,hashlib,sys
from topopt import slicer
from topopt.cli import slice as native
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'assemblies/parent_exterior'

def main(job_name='qr_standing',detect_supports=False,output_root=None,qualified_no_support=()):
    slicer.FILAMENT_FAMILY['PETG']='Bambu PETG Basic'
    original=native._write_presets;pick=slicer.pick_process
    slicer.pick_process=lambda presets,machine,layer:pick(presets,machine,0.12 if abs(float(layer)-0.1)<1e-8 else layer)
    overrides={}
    def inputs(*args,**kwargs):
        files=original(*args,**kwargs);p=Path(files['process']);d=json.loads(p.read_text());d.update(overrides)
        p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');return files
    native._write_presets=inputs
    rows=[];selected=sys.argv[1:]
    job_root=A/'print_jobs'/job_name if output_root is None else Path(output_root)
    for e in json.loads((A/'parts/manifest.json').read_text(encoding='utf-8'))['parts']:
        stem=e['stem']
        if selected and stem not in selected:continue
        if not stem.startswith('parent_oneplate_') and not detect_supports:continue
        layer=0.1 if 'camera_qr' in stem else 0.2
        supports='auto' if stem in ['parent_oneplate_frame','parent_oneplate_camera_stop','parent_oneplate_td_support','parent_oneplate_box_locator_end_fixed','parent_oneplate_box_locator_end_push'] else 'none'
        if detect_supports:supports='auto'
        if stem in qualified_no_support:supports='none'
        overrides.update(layer_height=str(layer),wall_loops='8',sparse_infill_density='100%',sparse_infill_pattern='alignedrectilinear',top_shell_layers='6',bottom_shell_layers='6',brim_width='3',brim_type='outer_only',support_threshold_angle='45',support_on_build_plate_only='1',curr_bed_type='Textured PEI Plate')
        overrides['support_style']='snug' if stem=='parent_oneplate_frame' else 'default'
        if detect_supports:overrides['support_on_build_plate_only']='0'
        if detect_supports:
            overrides['brim_width']='6' if stem=='parent_oneplate_td_support' else '2' if stem=='parent_oneplate_frame' else '3'
            camera=stem=='camera_mount'
            slicer.FILAMENT_FAMILY['PETG']='Generic PETG' if camera else 'Bambu PETG Basic'
            overrides.update(wall_loops='6' if camera else '8',sparse_infill_density='15%' if camera else '100%',sparse_infill_pattern='gyroid' if camera else 'alignedrectilinear')
        overrides['raft_first_layer_expansion']='0' if stem=='parent_oneplate_frame' else '-1'
        source=A/'parts'/e['file'];job=job_root/stem;job.mkdir(parents=True,exist_ok=True)
        code=native.main([str(source),'--out',str(job),'--printer','X1C','--material','PETG','--layer-mm',str(layer),'--supports',supports,'--orient','keep','--bed-type','Textured PEI Plate','--timeout','240','--quiet'])
        report=json.loads((job/'slice.json').read_text())
        row=dict(file=e['file'],quantity=e['quantity'],source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),layer_mm=layer,supports=supports,exit_code=code,bed_fits=report.get('bed_fits'),passed=report.get('pass'),warnings=report.get('warnings'),error=report.get('error'),grams=report.get('filament_g'),seconds=report.get('print_time_s'),support_filament_mm=slicer.support_mm(report.get('filament_by_feature_mm',{})),limits='Slicer result only; inspect supports and physically verify printing/fit/strength.')
        rows.append(row);(job/'source_manifest.json').write_text(json.dumps(row,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(row),flush=True)
    summary=job_root/'validation.json';summary.parent.mkdir(parents=True,exist_ok=True)
    if selected and summary.exists():
        old=json.loads(summary.read_text());rows=[x for x in old if x['file'] not in {r['file'] for r in rows}]+rows
    summary.write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
    return 0 if all(r['exit_code']==0 and r['passed'] and r['bed_fits'] for r in rows) else 1
if __name__=='__main__':sys.exit(main())
