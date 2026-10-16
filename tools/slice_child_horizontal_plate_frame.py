"""Slice the canonical portable STL set with installed Bambu X1C/PETG presets.

No installed preset is changed. One validated copy per STL type; quantities
remain in placement/print manifest. Jobs stay inside this assembly.
"""
from pathlib import Path
import hashlib,json,sys
from topopt import slicer
from topopt.cli import slice as native

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assemblies/child_horizontal_plate_frame'

def main():
    # The registry key selects a preset family only; no FE material card used.
    slicer.FILAMENT_FAMILY['PETG']='Bambu PETG Basic'
    original=native._write_presets
    original_pick=slicer.pick_process
    def pick_process(presets,machine,layer):
        # X1C ships 0.12 mm Fine, not 0.10 mm. Resolve its installed vendor
        # profile, then override only the saved per-job copy to the C fit layer.
        return original_pick(presets,machine,0.12 if abs(float(layer)-0.1)<1e-9 else layer)
    slicer.pick_process=pick_process
    overrides=dict(enable_support='0',wall_loops='8',sparse_infill_density='100%',sparse_infill_pattern='alignedrectilinear',
        infill_direction='0',brim_width='5',brim_type='outer_only',support_threshold_angle='45',
        curr_bed_type='Textured PEI Plate')
    def inputs(*args,**kwargs):
        files=original(*args,**kwargs)
        p=Path(files['process']);data=json.loads(p.read_text());data.update(overrides)
        p.write_text(json.dumps(data,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
        return files
    native._write_presets=inputs
    manifest=json.loads((OUT/'parts/manifest.json').read_text(encoding='utf-8'))
    placement=json.loads((OUT/'placement.json').read_text(encoding='utf-8'))
    printed_labels=set()
    locked=set(placement['print_progress']['source_mesh_sha256'])
    for entry in manifest['parts']:
        if entry['source'] in locked: printed_labels.update(entry['labels'])
    rows=[]
    selected=sys.argv[1:]
    for entry in manifest['parts']:
        if set(entry['labels'])<=printed_labels: continue
        # Mirrored physical parts have the same source stem but distinct jobs.
        job_stem=Path(entry['file']).stem
        if selected and job_stem not in selected and entry['stem'] not in selected: continue
        source=OUT/'parts'/entry['file'];job=OUT/'print_jobs/x1c_petg_basic'/job_stem
        metadata_path=ROOT/entry['part']/'manufacturing.json'
        metadata=json.loads(metadata_path.read_text(encoding='utf-8')) if metadata_path.exists() else {}
        layer=metadata.get('layer_heights_mm',{}).get(entry['stem'],0.2)
        support_mode=metadata.get('support_modes',{}).get(entry['stem'],'none')
        overrides['enable_support']='1' if support_mode!='none' else '0'
        overrides['support_on_build_plate_only']='1'
        if support_mode!='none':overrides.update(metadata.get('support_process_overrides',{}))
        overrides['layer_height']=str(layer)
        job.mkdir(parents=True,exist_ok=True)
        code=native.main([str(source),'--out',str(job),'--printer','X1C','--material','PETG',
            '--layer-mm',str(layer),'--supports',support_mode,'--orient','keep','--bed-type','Textured PEI Plate',
            '--timeout','240','--quiet'])
        report=json.loads((job/'slice.json').read_text())
        support_length=slicer.support_mm(report.get('filament_by_feature_mm',{}))
        process=json.loads((job/'preset_process.json').read_text(encoding='utf-8'))
        support_free=(bool(report.get('filament_by_feature_mm')) and report.get('supports')=='none' and str(process.get('enable_support'))=='0'
                      and report.get('support_used') is False and support_length==0)
        record=dict(file=entry['file'],quantity=entry['quantity'],exit_code=code,
            source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),process_overrides=overrides.copy(),
            bed_fits=report.get('bed_fits'),pass_=report.get('pass'),error=report.get('error'),
            filament_g_per_part=report.get('filament_g'),print_time_s_per_part=report.get('print_time_s'),
            warnings=report.get('warnings'),supports=support_mode,material='Bambu PETG Basic',layer_height_mm=layer,
            support_free_verified=support_free,support_filament_mm=support_length,
            note='One copy sliced; duplicate according to quantity. Slicing is not strength qualification.')
        rows.append(record);print(job_stem,json.dumps(record,ensure_ascii=False),flush=True)
        (job/'source_manifest.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        if code or not report.get('pass') or not report.get('bed_fits') or report.get('warnings') or (support_mode=='none' and not support_free):
            raise RuntimeError(f'Slice verification failed: {source}')
    summary=OUT/'print_jobs/x1c_petg_basic/validation.json'
    previous=json.loads(summary.read_text(encoding='utf-8')) if selected and summary.exists() else []
    current={entry['file']:entry for entry in manifest['parts'] if not set(entry['labels'])<=printed_labels}
    retained=[r for r in previous if r['file'] in current and r['file'] not in {r['file'] for r in rows}]
    for index,row in enumerate(retained):
        source=OUT/'parts'/row['file']
        # A previous selected run may have sliced its jobs successfully, then
        # rejected a stale retained job before updating the aggregate summary.
        # Recover the per-job evidence; its hash must still match this STL.
        job_record=OUT/'print_jobs/x1c_petg_basic'/Path(row['file']).stem/'source_manifest.json'
        if job_record.exists():
            recovered=json.loads(job_record.read_text(encoding='utf-8'))
            if recovered.get('file')==row['file'] and recovered.get('pass_') and recovered.get('exit_code')==0:
                row=recovered;retained[index]=row
        if row['source_sha256']!=hashlib.sha256(source.read_bytes()).hexdigest():
            raise RuntimeError(f'Previous slice is stale; reslice {row["file"]}')
        if row.get('supports')=='none' and (not row.get('support_free_verified') or row.get('support_filament_mm')!=0):
            raise RuntimeError(f'Reslice with supports disabled: {row["file"]}')
        row['quantity']=current[row['file']]['quantity']
    rows=retained+rows
    summary.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__': main()
