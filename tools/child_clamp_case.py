"""Select an existing clamp analysis case without overwriting its history."""
import os
from pathlib import Path


def analysis_case(part: Path):
    name = os.environ.get('CHILD_CLAMP_CASE','connected_cage_rubber1_v065')
    if Path(name).name != name or name in ('.','..'):
        raise ValueError('CHILD_CLAMP_CASE must be a single case folder name')
    return part/'_work/analysis'/name
