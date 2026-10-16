"""Print the bounds of real STEP intersections without changing pass limits."""
from pathlib import Path
path=Path(__file__).with_name('verify_step.py')
code=path.read_text(encoding='utf-8').replace('assert volume<.005,(theta,lift,a,b,volume)',"if volume>=.005: print('INTERSECTION',theta,lift,a,b,volume,common.BoundBox)")
# Stop before writing a verification report: this is diagnostic only.
code=code[:code.index('assembly=Part.Shape()')]
exec(compile(code,str(path),'exec'),dict(__file__=str(path)))
