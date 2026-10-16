"""Summarize recorded solver results without recomputing any FEM result."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1];O=R/'assemblies/parent_hand_service';D=O/'rigidity'
current=hashlib.sha256((R/'parts/parent/interior/printed/parent_hand_service/lift_carrier.stl').read_bytes()).hexdigest()
rows=[]
for f in sorted(D.glob('iteration_*')):
 inputs=json.loads((f/'inputs.json').read_text())
 entry=dict(attempt=f.name,current_carrier_stl_matches=inputs['sha256']['carrier.stl']==current,scope=inputs['scope'])
 execution=f/'execution.json';summary=f/'ccx/ccx_summary.json'
 override=f/'ccx/mesher_override.json'
 entry['mesher_override']=json.loads(override.read_text()) if override.exists() else None
 entry['execution']=json.loads(execution.read_text()) if execution.exists() else {'completed':False}
 if summary.exists():
  s=json.loads(summary.read_text());entry['mesh_convergence']=s.get('mesh_convergence')
  entry['assembly_guarantee']=False
  entry['warning']='Ideal clamps, carrier only; connector/PCB, joints, floor, props and case not represented. A numerical PASS is not assembly approval.'
  entry['runs']=[dict(mesh_target_mm=r.get('mesh_target_mm'),tool_pass=r.get('pass'),mesh_quality=r.get('mesh_quality'),cases=[dict(name=c.get('case'),safety_factor_p99_5=c.get('safety_factor_p99_5'),worst_element_safety_factor=c.get('worst_element_safety_factor'),max_disp_mm=c.get('max_disp_mm'),tool_pass=c.get('pass')) for c in r.get('cases',[])]) for r in s['runs']]
  entry['displacement_gate_all_recorded_cases']=all(c.get('max_disp_mm') is not None and c['max_disp_mm']<=.2 for r in s['runs'] for c in r.get('cases',[])) and any(r.get('cases') for r in s['runs'])
 else:
  entry['analysis_status']='NO_COMPLETE_SUMMARY; no stiffness approval'
 rows.append(entry)
(O/'rigidity_analysis_status.json').write_text(json.dumps(dict(current_carrier_stl_sha256=current,attempts=rows,assembly_guarantee=False,physical_test_records_complete=0),indent=2),encoding='utf-8')
print([(r['attempt'],r['execution']) for r in rows])
