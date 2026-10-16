"""Add physical load increments to a not-yet-run native study, retaining combined loads."""
import json
from copy import deepcopy
from pathlib import Path
from child_clamp_case import analysis_case

ROOT=Path(__file__).resolve().parents[1]
CASE=analysis_case(ROOT/'parts/child/exterior/printed/child_wte4_suspension_clamp')

if __name__=='__main__':
    if (CASE/'setup').exists() or (CASE/'opt').exists():
        raise RuntimeError('Do not change a study after setup or optimisation')
    for filename in ['study_cage.json','study_solid_bound.json']:
        path=CASE/filename
        data=json.loads(path.read_text(encoding='utf-8'))
        if any(c['name'].startswith('increment_') for c in data['cases']):
            raise RuntimeError('Already augmented')
        (CASE/(path.stem+'_before_increment.json')).write_bytes(path.read_bytes())
        preload={x['region']:x['force'] for x in data['cases'][0]['loads']}
        additions=[]
        for case in data['cases']:
            if case['load_class']!='abnormal': continue
            incremental=deepcopy(case)
            incremental['name']='increment_'+case['name']
            incremental['loads']=[dict(region=x['region'],force=[a-b for a,b in zip(x['force'],preload[x['region']])])
                                  for x in case['loads'] if x['region'].startswith('contact_')]
            additions.append(incremental)
        data['cases']+=additions
        data['required_cases']=[c['name'] for c in data['cases']]
        data['_incremental_compliance']='Seven additional handling increments balance global bending against the repeated clamping preload in the normalised native compliance objective. All original eleven combined cases and their force vectors remain unchanged. This is not a claim of frictional grip without preload.'
        path.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    print('Retained 11 combined cases; added 7 handling increments.')
