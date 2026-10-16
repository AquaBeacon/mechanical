"""Generate blank real-test records and keep untested hardware out of release."""
import csv,json
from pathlib import Path
O=Path(__file__).resolve().parents[1]/'assemblies/parent_hand_service'
fields=['case_id','pose','port','axis','force_N','peak_displacement_mm','displacement_uncertainty_mm','residual_displacement_mm','damage_or_slip','instrument_calibration_record','operator','test_date','actual_material_and_print_settings','actual_connector_load_rating_confirmed']
file=O/'rigidity_physical_tests.csv'
if not file.exists():
 with file.open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
  for pose in ['closed','service']:
   for port in ['MAIN_USB','MAIN_SD','SONY_MAIN_USB','SONY_EXT_USB','SONY_SD']:
    for axis in ['X+','X-','Y+','Y-','Z+','Z-']:
     w.writerow(dict(case_id=pose+'_'+port+'_'+axis,pose=pose,port=port,axis=axis))
rows=list(csv.DictReader(file.open(encoding='utf-8-sig')))
required=[x for x in fields if x not in ['case_id','pose','port','axis']]
complete=[r for r in rows if all(r.get(k,'').strip() for k in required)]
status='NOT_TESTED' if not complete else 'INCOMPLETE'
# This script records completeness, not certification: complete measurements
# still require technical review, fixture validity and traceable calibrated data.
report=dict(guarantee_status='NOT_ESTABLISHED',manufacturing_release=False,
 design_target=dict(force_N=20,case_relative_displacement_mm=.2),
 geometry_evidence='verification.json; no structural implication',
 analysis_evidence='rigidity/iteration_*/inputs.json, execution.json, ccx/ccx_summary.json; scope must include case, connections, all PCBs and all directions before approval',
 physical_tests=dict(status=status,required_cases=60,recorded_rows=len(rows),complete_rows=len(complete),file=file.name,acceptance='For each real test: abs(peak displacement) + calibrated displacement uncertainty <=0.2 mm at20 N; no damage or slip; unloading residual <=0.02 mm. Confirm connector allowable load before applying20 N.'),
 unresolved=['Full assembly mechanics including floor, service sleeves, threaded ties, guide lock and case flexibility','Sony MAIN/EXT/IMU internal attachment and connector solder/housing loading','PCB local bending and uplift restraints','Manufactured material properties, print settings and joint preload/creep','Actual enclosure/lid and battery dimensions','Calibrated physical force/displacement tests for all60 cases'],
 principle='Do not convert geometric PASS, component-only FEA, or incomplete measurements into an assembly guarantee.')
(O/'rigidity_acceptance.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('Guarantee NOT_ESTABLISHED; actual physical test records:',len(complete),'/60')
