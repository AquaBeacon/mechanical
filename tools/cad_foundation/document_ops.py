"""Native document operations executed only inside the isolated FreeCAD worker."""
import importlib.util
import math
import os
from pathlib import Path
import re
import sys

import FreeCAD as App
import Part
import Mesh
import MeshPart


def check_document(doc):
    doc.recompute()
    bad = [(o.Name, list(o.State)) for o in doc.Objects if any(s in ("Invalid", "Error") for s in o.State)]
    if bad:
        raise ValueError("document recompute failed: " + str(bad))
    for obj in doc.Objects:
        if any(p.Document != doc for p in obj.OutList):
            raise ValueError("external document links are not self-contained; embed dependencies before processing")


def outputs(doc, names):
    if not names:
        info = doc.getObject("CADFoundationInfo")
        names = list(info.OutputNames) if info and "OutputNames" in info.PropertiesList else []
    if not names or len(names) != len(set(names)):
        raise ValueError("explicit unique output object names are required; inspect the document first")
    objects = []
    for name in names:
        obj = doc.getObject(name)
        if obj is None or not hasattr(obj, "Shape") or obj.Shape.isNull() or not obj.Shape.isValid() or not obj.Shape.Solids:
            raise ValueError("output must be a valid solid object: " + name)
        objects.append(obj)
    for obj in objects:
        if any(other in obj.OutListRecursive for other in objects if other != obj):
            raise ValueError("do not select both a final body and its intermediate features")
    return objects


def remember_outputs(doc, objects):
    info = doc.getObject("CADFoundationInfo")
    if info is None:
        info = doc.addObject("App::FeaturePython", "CADFoundationInfo")
        info.addProperty("App::PropertyStringList", "OutputNames", "CAD foundation")
        info.addProperty("App::PropertyString", "Notice", "CAD foundation")
    info.OutputNames = [o.Name for o in objects]
    info.Notice = "Review copy. Geometry checks do not certify fit, printing or strength."
    info.setEditorMode("OutputNames", 1)


def load_document(job):
    path = Path(job["snapshots"][job["source"]]["path"])
    if path.suffix.lower() == ".fcstd":
        doc = App.openDocument(str(path))
    else:
        doc = App.newDocument("Imported")
        if path.suffix.lower() == ".stl":
            obj = doc.addObject("Mesh::Feature", "ImportedMesh")
            obj.Mesh = Mesh.Mesh(str(path))
        else:
            obj = doc.addObject("Part::Feature", "ImportedSolid")
            obj.Shape = Part.read(str(path))
    check_document(doc)
    return doc


def build_native(doc, job):
    path = Path(job["snapshots"][job["generator"]]["path"])
    # Review this project script before invoking. This is executable code, not a sandbox.
    workspace = Path(os.environ["ASM_ROOT"]).resolve()
    # Do not accidentally satisfy an undeclared import from live project sources.
    # Standard libraries and FreeCAD modules stay available. This is not a sandbox.
    sys.path[:] = [p for p in sys.path if p and not Path(p).resolve().is_relative_to(workspace)]
    sys.path.insert(0, str(Path(job["run_dir"]) / "intermediate/sources"))
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location("cad_native_generator", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.build(doc, job.get("parameters", {}))
    if not isinstance(result, (list, tuple)) or not result or any(o.Document != doc for o in result):
        raise ValueError("build(doc, parameters) must return a nonempty list of final objects in doc")
    check_document(doc)
    return outputs(doc, [o.Name for o in result])


def edit_parameters(doc, job):
    sheet = doc.getObject(job["sheet"])
    if sheet is None or sheet.TypeId != "Spreadsheet::Sheet":
        raise ValueError("named Spreadsheet object does not exist")
    changes = {}
    for alias, value in job["updates"].items():
        cell = sheet.getCellFromAlias(alias)
        if not cell:
            raise ValueError("unknown spreadsheet alias: " + alias)
        old = sheet.get(cell)
        if not isinstance(old, (float, int)) and not hasattr(old, "Value"):
            raise ValueError("spreadsheet alias is not numeric: " + alias)
        before = sheet.getContents(cell)
        literal = re.fullmatch(r"\s*=?\s*[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?\s*([A-Za-z][A-Za-z0-9 /^*-]*)?\s*", before)
        if not literal:
            raise ValueError("derived formula cannot be replaced as an input parameter: " + alias)
        unit = (literal.group(1) or "").strip()
        if unit and App.Units.Quantity("1 " + unit).Unit != old.Unit:
            raise ValueError("cannot preserve spreadsheet unit: " + alias)
        new = format(value, ".15g") + (" " + unit if unit else "")
        sheet.set(cell, new)
        changes[alias] = {"cell": cell, "before": before, "after": new}
    check_document(doc)
    return changes


def inspect_document(doc):
    info = doc.getObject("CADFoundationInfo")
    result = []
    for obj in doc.Objects:
        row = {"name": obj.Name, "label": obj.Label, "type": obj.TypeId, "state": list(obj.State)}
        if hasattr(obj, "Shape") and not obj.Shape.isNull():
            shape = obj.Shape
            box = shape.BoundBox
            row["geometry"] = {"valid": shape.isValid(), "solids": len(shape.Solids), "volume_mm3": abs(shape.Volume),
                               "bbox_mm": [box.XMin, box.YMin, box.ZMin, box.XMax, box.YMax, box.ZMax]}
        if obj.TypeId == "Mesh::Feature":
            row["geometry"] = {"facets": obj.Mesh.CountFacets, "closed": obj.Mesh.isSolid()}
        if obj.TypeId == "Spreadsheet::Sheet":
            aliases = {}
            for cell in obj.getNonEmptyCells():
                alias = obj.getAlias(cell)
                if alias:
                    aliases[alias] = {"cell": cell, "content": obj.getContents(cell)}
            row["parameters"] = aliases
        if hasattr(obj, "ExpressionEngine"):
            row["expressions"] = [[str(a), str(b)] for a, b in obj.ExpressionEngine]
        result.append(row)
    return {"label": doc.Label, "output_names": list(info.OutputNames) if info and hasattr(info, "OutputNames") else [],
            "object_count": len(result)}, result


def export_solids(objects, run_dir):
    import Import
    from cli import digest
    target = Path(run_dir)
    result = {}
    for obj in objects:
        shape = obj.Shape
        step, stl = target / (obj.Name + ".step"), target / (obj.Name + ".stl")
        if step.exists() or stl.exists():
            raise ValueError("refusing to overwrite exported geometry")
        Import.export([obj], str(step))
        readback = Part.read(str(step))
        if not readback.isValid() or len(readback.Solids) != len(shape.Solids):
            raise ValueError("STEP readback topology mismatch")
        expected_volume = abs(shape.Volume)
        if abs(abs(readback.Volume) - expected_volume) > max(1e-6, expected_volume * 1e-7):
            raise ValueError("STEP readback volume mismatch")
        mesh = MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.05, AngularDeflection=0.2, Relative=False)
        mesh.write(str(stl))
        saved_mesh = Mesh.Mesh(str(stl))
        if not saved_mesh.isSolid() or not saved_mesh.CountFacets:
            raise ValueError("STL readback is not closed")
        if abs(abs(saved_mesh.Volume) - expected_volume) / max(expected_volume, 1e-9) > 0.02:
            raise ValueError("STL tessellation differs from B-Rep volume by more than 2%")
        expected_box = shape.BoundBox
        for loaded, tolerance in ((readback, 1e-5), (saved_mesh, 0.1)):
            box = loaded.BoundBox
            if any(abs(getattr(box, p) - getattr(expected_box, p)) > tolerance for p in ("XMin", "YMin", "ZMin", "XMax", "YMax", "ZMax")):
                raise ValueError("exported bounding box mismatch")
        result[obj.Name] = {"step": str(step), "stl": str(stl), "step_sha256": digest(step), "stl_sha256": digest(stl),
                            "stl_closed": True, "volume_mm3": expected_volume}
    return result
