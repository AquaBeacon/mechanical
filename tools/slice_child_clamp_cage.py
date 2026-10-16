"""Slice the real cage in its analysed Y-build orientation on an X1 Carbon.

Uses native topopt preset resolution/parsing and Bambu Studio CLI. Overrides
the manufacturing input settings to 100% infill, eight walls and eight shells.
No FEM, slicing engine or toolpath parser is reimplemented.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import sys
import zipfile
from topopt import external, slicer
from topopt.cli import slice as native

ROOT = Path(__file__).resolve().parents[1]
PART = ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp'
from child_clamp_case import analysis_case
CASE = analysis_case(PART)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--support',choices=['normal','tree'],default='normal')
    args=parser.parse_args()
    part = CASE/'cage_print_orientation.stl'
    out = CASE/('slice' if args.support=='normal' else 'slice_tree')
    out.mkdir(parents=True, exist_ok=True)
    exe = external.require('slicer', 'X1C cage print verification')
    presets, profile_root = native._presets(exe)
    machine = slicer.pick_machine('X1C')
    process = slicer.pick_process(presets, machine, .2)
    filament = slicer.pick_filament(presets, machine, 'PETG')
    files = native._write_presets(presets, str(out), machine, process, filament, 'auto')
    machine_file = Path(files['machine'])
    data = json.loads(machine_file.read_text(encoding='utf-8'))
    # Studio 2.8 stores X1 G-code separately from the inherits chain. Native
    # Presets resolves the chain only; otherwise its generic 205C start remains.
    templates = []
    for template in sorted((Path(profile_root)/'BBL/machine').glob(machine+' template *.json')):
        value = json.loads(template.read_text(encoding='utf-8'))
        data.update({key:val for key,val in value.items() if key.endswith('_gcode')})
        templates.append(dict(path=str(template),sha256=hashlib.sha256(template.read_bytes()).hexdigest()))
    if not templates:
        raise RuntimeError('Installed X1 G-code templates missing; do not use a generic machine start')
    data['curr_bed_type'] = 'Textured PEI Plate'
    machine_file.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    process_file = Path(files['process'])
    data = json.loads(process_file.read_text(encoding='utf-8'))
    # Bambu Studio 2.8 names the rectilinear (ipRectilinear) enum "zig-zag".
    # The historic "rectilinear" token fails CLI configuration validation.
    settings = dict(sparse_infill_density='100%', sparse_infill_pattern='zig-zag', infill_direction='90',
        wall_loops='8', top_shell_layers='8', bottom_shell_layers='8', brim_width='5',
        brim_type='outer_only', support_on_build_plate_only='1', layer_height='0.2',
        support_type=args.support+'(auto)')
    data.update(settings)
    process_file.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    # Preserve the TDS V3 print-temperature anchors; all other material defaults
    # are recorded from the installed Bambu PETG Basic vendor profile.
    filament_file = Path(files['filament'])
    data = json.loads(filament_file.read_text(encoding='utf-8'))
    data.update(nozzle_temperature=['255'], nozzle_temperature_initial_layer=['255'],
        hot_plate_temp=['70'], hot_plate_temp_initial_layer=['70'],
        textured_plate_temp=['70'], textured_plate_temp_initial_layer=['70'])
    filament_file.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    project_name = 'cage_x1c_petg100.3mf'
    project = out/project_name
    code, output, seconds = native._run(exe, files, str(part), str(out), project_name, 'keep', 1200)
    (out/'slicer.log').write_text(output,encoding='utf-8')
    error = None
    quantities = {}
    temperatures = dict(nozzle_positive_targets_c=[], bed_positive_targets_c=[], pass_check=False)
    try:
        if code!=0:
            raise RuntimeError(f'Bambu Studio exit {code}')
        info, header, features = native._read_3mf(str(project))
        quantities = native._quantities(info,header,features,'PETG',.2)
        with zipfile.ZipFile(project) as archive:
            gcode = next(name for name in archive.namelist() if name.endswith('.gcode'))
            with archive.open(gcode) as stream:
                for raw in stream:
                    match = re.match(rb'^(M104|M109|M140|M190)\s+S([0-9.]+)',raw.strip())
                    if match and float(match[2])>0:
                        key = 'nozzle_positive_targets_c' if match[1] in [b'M104',b'M109'] else 'bed_positive_targets_c'
                        temperatures[key].append(float(match[2]))
        temperatures['pass_check'] = bool(temperatures['nozzle_positive_targets_c'] and temperatures['bed_positive_targets_c'] and
            temperatures['nozzle_positive_targets_c'][-1]==255 and temperatures['bed_positive_targets_c'][-1]==70)
    except Exception as exc:
        error = str(exc)
    ok, checks, note = slicer.judge(quantities,error)
    checks.append(dict(key='gcode_print_temperatures',state='PASS' if temperatures['pass_check'] else 'FAIL',
        condition='Last positive nozzle/bed targets in actual G-code are 255C / 70C',detail=temperatures))
    ok = ok and temperatures['pass_check']
    result = dict(schema=slicer.SCHEMA, part=str(part), part_sha256=hashlib.sha256(part.read_bytes()).hexdigest(),
        tool=dict(name='Bambu Studio',path=exe), printer='X1C', printer_name='Bambu Lab X1-Carbon',
        material='PETG', filament_preset=filament, layer_mm=.2, bed_type='Textured PEI Plate', supports='auto',
        support_type=args.support+'(auto)', orient='keep', rotation_from_design_deg=[90,0,0],
        process_overrides=settings, presets=dict(root=profile_root,machine=machine,process=process,filament=filament,files=files),
        vendor_gcode_templates=templates, gcode_temperature_checks=temperatures,
        project_3mf=str(project) if project.exists() else None, seconds=seconds, exit_code_slicer=code,
        plate_gcode=str(out/'plate_1.gcode') if (out/'plate_1.gcode').exists() else None,
        error=error, warnings=native._warnings(output), pass_check=bool(ok), checks=checks,note=note,
        internal_support_policy='Build plate only: do not trap generated support inside sealed density-field cavities. Internal bridges still require inspection and a physical print trial.')
    result['pass'] = bool(ok)
    result.update(quantities)
    (CASE/'slice_checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (out/'slice_checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
