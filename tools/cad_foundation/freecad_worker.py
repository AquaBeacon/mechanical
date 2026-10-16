"""Private FreeCADCmd worker. Paths arrive via CAD_FOUNDATION_JOB/ASM_ROOT."""
import json
import os
from pathlib import Path
import sys
import traceback

import FreeCAD as App
import Part
import Mesh

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cli import read_json, write_json, digest, validate_ops


def matrix_for(ops):
    """Same outer-to-inner order as placement.json / OpenSCAD: M0*M1*..."""
    validate_ops(ops)
    result = App.Matrix()
    for op in ops:
        kind, v = next(iter(op.items()))
        matrix = App.Matrix()
        if kind == "translate":
            matrix.move(App.Vector(*v))
        elif kind == "rotate":
            matrix = App.Rotation(v[2], v[1], v[0]).toMatrix()
        elif kind == "scale":
            matrix.A11, matrix.A22, matrix.A33 = v
        else:
            d = sum(x * x for x in v)
            for i in range(3):
                for j in range(3):
                    setattr(matrix, "A%d%d" % (i + 1, j + 1), (1 if i == j else 0) - 2 * v[i] * v[j] / d)
        result = result.multiply(matrix)
    return result


def rigid(matrix):
    a = [[getattr(matrix, "A%d%d" % (i + 1, j + 1)) for j in range(3)] for i in range(3)]
    return abs(matrix.determinant() - 1) < 1e-8 and all(
        abs(sum(a[k][i] * a[k][j] for k in range(3)) - (1 if i == j else 0)) < 1e-8
        for i in range(3) for j in range(3))


def bbox(shape):
    b = shape.BoundBox
    return [b.XMin, b.YMin, b.ZMin, b.XMax, b.YMax, b.ZMax]


def metrics(obj):
    if obj.TypeId == "Mesh::Feature":
        return {"bbox_mm": bbox(obj.Mesh), "facets": obj.Mesh.CountFacets,
                "closed": obj.Mesh.isSolid(), "volume_mm3": abs(obj.Mesh.Volume), "type": "mesh_reference"}
    shape = obj.Shape
    return {"bbox_mm": bbox(shape), "volume_mm3": abs(shape.Volume), "solids": len(shape.Solids),
            "valid": shape.isValid(), "type": "brep"}


def metadata(obj, row, snapshot):
    for key, value in {"SourcePath": row["source"], "SourceSHA256": snapshot["sha256"],
                       "SourceOps": json.dumps(row["ops"]), "Editability": row["editability"]}.items():
        obj.addProperty("App::PropertyString", key, "Provenance")
        setattr(obj, key, value)
        obj.setEditorMode(key, 1)


def import_assembly(doc, job):
    cache, groups, objects, checks = {}, {}, [], []
    for row in job["entries"]:
        source = row["source"]
        snap = job["snapshots"][source]
        if digest(snap["path"]) != snap["sha256"]:
            raise ValueError("snapshot changed: " + source)
        is_mesh = Path(source).suffix.lower() == ".stl"
        if source not in cache:
            geometry = Mesh.Mesh(snap["path"]) if is_mesh else Part.read(snap["path"])
            if is_mesh:
                if not geometry.CountFacets:
                    raise ValueError("empty mesh: " + source)
            elif geometry.isNull() or not geometry.isValid() or not geometry.Solids or geometry.Volume <= 0:
                raise ValueError("invalid or non-solid STEP: " + source)
            check = {"source": source, "type": "mesh_reference" if is_mesh else "brep"}
            ref = row.get("stl_reference")
            if not is_mesh and ref:
                mesh = Mesh.Mesh(job["snapshots"][ref]["path"])
                if not mesh.CountFacets:
                    raise ValueError("empty STL reference: " + ref)
                delta = max(abs(a - b) for a, b in zip(bbox(geometry), bbox(mesh)))
                volume_delta = abs(abs(geometry.Volume) - abs(mesh.Volume)) / max(abs(mesh.Volume), 1e-9)
                check.update(bbox_difference_mm=delta, reference_closed=mesh.isSolid(), volume_relative_difference=volume_delta)
                # Historical importer checks: 0.5 mm / 2%. Not a surface-equivalence proof.
                if delta > 0.5 or (mesh.isSolid() and volume_delta > 0.02):
                    raise ValueError("STEP/STL mismatch: " + source + " " + str(check))
                if not mesh.isSolid():
                    check["warning"] = "Open STL reference: volume comparison is not certified."
            elif not is_mesh:
                check["warning"] = "No STL reference: cross-format consistency was not checked."
            cache[source] = geometry
            checks.append(check)
        matrix = matrix_for(row["ops"])
        obj = doc.addObject("Mesh::Feature" if is_mesh else "Part::Feature", "Component%04d" % row["index"])
        obj.Label = row["label"]
        geometry = cache[source].copy()
        if rigid(matrix):
            if is_mesh:
                obj.Mesh = geometry
            else:
                obj.Shape = geometry
            obj.Placement = App.Placement(matrix).multiply(obj.Placement)
        else:
            # Reflections and scale cannot be represented by a Placement.
            if is_mesh:
                geometry.transform(matrix)
                obj.Mesh = geometry
            else:
                obj.Shape = geometry.transformGeometry(matrix)
            obj.addProperty("App::PropertyString", "TransformMode", "Provenance")
            obj.TransformMode = "mirror/scale baked into review geometry; edit source ops to regenerate"
            obj.setEditorMode("TransformMode", 1)
        metadata(obj, row, snap)
        group = row["group"]
        if group not in groups:
            groups[group] = doc.addObject("App::DocumentObjectGroup", "Group%03d" % len(groups))
            groups[group].Label = group
        groups[group].addObject(obj)
        objects.append(obj)
    doc.recompute()
    for obj in objects:
        m = metrics(obj)
        if m["type"] == "brep" and (not m["valid"] or not m["solids"]):
            raise ValueError("invalid transformed solid: " + obj.Label)
    return objects, checks


def compare_readback(before, after):
    if before.keys() != after.keys():
        raise ValueError("component identity changed on reopening")
    for name, expected in before.items():
        actual = after[name]
        if expected["type"] != actual["type"]:
            raise ValueError("component representation changed")
        if max(abs(a - b) for a, b in zip(expected["bbox_mm"], actual["bbox_mm"])) > 1e-6:
            raise ValueError("bbox changed on reopening: " + name)
        if abs(expected["volume_mm3"] - actual["volume_mm3"]) > max(1e-6, expected["volume_mm3"] * 1e-8):
            raise ValueError("volume changed on reopening: " + name)
        for key in ("valid", "solids", "closed", "facets"):
            if expected.get(key) != actual.get(key):
                raise ValueError("topology changed on reopening: " + name)


def run(job):
    from document_ops import (build_native, check_document, edit_parameters, export_solids,
                              inspect_document, load_document, outputs, remember_outputs)
    run_dir = Path(job["run_dir"])
    model = run_dir / "model.FCStd"
    if model.exists():
        raise ValueError("refusing to overwrite a FreeCAD document")
    for source, snapshot in job.get("snapshots", {}).items():
        if digest(snapshot["path"]) != snapshot["sha256"]:
            raise ValueError("snapshot changed: " + source)
    doc = load_document(job) if job["kind"] in ("inspect", "edit", "export") else App.newDocument("CADFoundation")
    if job["kind"] == "inspect":
        summary, items = inspect_document(doc)
        App.closeDocument(doc.Name)
        return {"schema_version": 1, "run_id": job["run_id"], "status": "passed", "kind": "inspect",
                "freecad_version": list(App.Version()), "document": summary, "objects": items}
    doc.Label = job["name"] + " [review copy]"
    checks = []
    parameter_changes = None
    if job["kind"] == "demo":
        from native_template import build
        objects = [build(doc)]
    elif job["kind"] == "native":
        objects = build_native(doc, job)
    elif job["kind"] in ("edit", "export"):
        if job["kind"] == "edit":
            parameter_changes = edit_parameters(doc, job)
        objects = outputs(doc, job.get("object_names"))
    elif job["kind"] == "assembly":
        objects, checks = import_assembly(doc, job)
    else:
        raise ValueError("unknown job kind: " + job["kind"])
    if job["kind"] != "assembly":
        remember_outputs(doc, objects)
    check_document(doc)
    before = {o.Name: metrics(o) for o in objects}
    if any(m["type"] == "brep" and (not m["valid"] or not m["solids"]) for m in before.values()):
        raise ValueError("invalid output geometry")
    doc.saveAs(str(model))
    App.closeDocument(doc.Name)
    reopened = App.openDocument(str(model))
    reopened.recompute()
    after = {name: metrics(reopened.getObject(name)) for name in before}
    compare_readback(before, after)
    edit_check = None
    if job["kind"] == "demo":
        from native_template import verify_editability
        edit_check = verify_editability(reopened)
    exports = export_solids([reopened.getObject(name) for name in before], run_dir) if job["kind"] != "assembly" else {}
    # The editability check is intentionally not saved over the delivered baseline.
    App.closeDocument(reopened.Name)
    return {"schema_version": 1, "run_id": job["run_id"], "status": "passed",
            "freecad_version": list(App.Version()), "kind": job["kind"],
            "model_sha256": digest(model), "component_count": len(before), "components": after,
            "cross_format_checks": checks, "editability_check": edit_check,
            "parameter_changes": parameter_changes, "exports": exports,
            "limitations": ["Review copy, not a manufacturing release.",
                            "No collision, motion, strength, or source-freshness certification.",
                            "Imported STEP components have no recovered parametric history."]}


# FreeCADCmd executes Python files with its own module name, not __main__.
if os.environ.get("CAD_FOUNDATION_JOB"):
    job = read_json(os.environ["CAD_FOUNDATION_JOB"])
    try:
        result = run(job)
    except Exception as exc:
        traceback.print_exc()
        result = {"schema_version": 1, "run_id": job["run_id"], "status": "failed", "error": str(exc)}
    write_json(Path(job["run_dir"]) / "report.json", result)
    print("[cad-foundation]", result["status"], flush=True)
