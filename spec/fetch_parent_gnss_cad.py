"""Fetch official model/source inventory, saving originals and evidence in ref."""
from pathlib import Path
import urllib.request, json
R=Path(__file__).resolve().parents[1]
P=R/'parts/parent/interior/cots/sparkfun_neo_f9p/ref'
for repo,branch in [('sparkfun/3D_Models','master'),('u-blox/3D-Step-Models-Library','master')]:
    try:
        tree=json.load(urllib.request.urlopen(f'https://api.github.com/repos/{repo}/git/trees/{branch}?recursive=1'))
    except Exception as e:
        print(repo,e);continue
    matches=[x['path'] for x in tree['tree'] if any(k in x['path'].lower() for k in ['23288','f9p','neo-f9'])]
    print(repo,matches,flush=True)
    for path in matches:
        if not path.lower().endswith(('.step','.stp')):continue
        url=f'https://raw.githubusercontent.com/{repo}/{branch}/{urllib.parse.quote(path)}'
        target=P/Path(path).name
        urllib.request.urlretrieve(url,target)
        print('Saved',target,flush=True)
