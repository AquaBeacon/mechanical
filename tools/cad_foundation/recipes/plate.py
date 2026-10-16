"""Editable integration sample, NOT a production print-ready part.

Use the project-native generator contract: build(doc, parameters) -> final objects.
No GUI, file writes, custom proxies or mandatory installed Python modules.
Sharp sample edges and circular holes are illustrative; apply manufacturing
finishes/profiles in an actual part's canonical source before manufacturing.
"""
import sys
from pathlib import Path

# native_template.py is passed as a declared dependency by the caller.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from native_template import build as build_template


def build(doc, parameters):
    allowed = {"length", "width", "thickness", "hole_diameter", "hole_spacing"}
    unknown = set(parameters) - allowed
    if unknown:
        raise ValueError("unknown plate parameters: " + str(sorted(unknown)))
    values = dict(length=80, width=30, thickness=6, hole_diameter=6, hole_spacing=50)
    values.update(parameters)
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) or v <= 0 for v in values.values()):
        raise ValueError("plate dimensions must be positive numbers in mm")
    if values["hole_spacing"] + values["hole_diameter"] >= values["length"] or values["hole_diameter"] >= values["width"]:
        raise ValueError("holes must remain inside the plate")
    pocket = build_template(doc)
    sheet = doc.getObject("Parameters")
    for alias, value in values.items():
        sheet.set(sheet.getCellFromAlias(alias), str(value) + " mm")
    doc.recompute()
    return [pocket]
