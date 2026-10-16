"""Small, editable FreeCAD native-tree demonstration; dimensions are illustrative only."""

import FreeCAD as App
import Part
import Sketcher


def _must_recompute(doc, obj):
    doc.recompute()
    if getattr(obj, "State", None) and "Invalid" in obj.State:
        raise RuntimeError("FreeCAD object is invalid: %s (%s)" % (obj.Name, obj.State))
    shape = getattr(obj, "Shape", None)
    if shape is not None and shape.isNull():
        raise RuntimeError("FreeCAD object has a null shape: %s" % obj.Name)


def _expression(obj, prop, expression):
    obj.setExpression(prop, expression)


def build(doc):
    """Create a spreadsheet-driven two-hole plate and return its final Pocket."""
    params = doc.addObject("Spreadsheet::Sheet", "Parameters")
    params.Label = "Illustrative parameters (mm)"
    for cell, value in (("A1", "Parameter"), ("B1", "Value"),
                        ("A2", "length"), ("B2", "80 mm"),
                        ("A3", "width"), ("B3", "30 mm"),
                        ("A4", "thickness"), ("B4", "6 mm"),
                        ("A5", "hole_diameter"), ("B5", "6 mm"),
                        ("A6", "hole_spacing"), ("B6", "50 mm")):
        params.set(cell, value)
    for cell, alias in (("B2", "length"), ("B3", "width"),
                        ("B4", "thickness"), ("B5", "hole_diameter"),
                        ("B6", "hole_spacing")):
        params.setAlias(cell, alias)

    body = doc.addObject("PartDesign::Body", "Body")
    body.Label = "Editable plate demonstration — illustrative only"
    outline = doc.addObject("Sketcher::SketchObject", "Outline")
    body.addObject(outline)
    outline.Label = "Plate outline"
    pts = [App.Vector(-40, -15, 0), App.Vector(40, -15, 0),
           App.Vector(40, 15, 0), App.Vector(-40, 15, 0)]
    for i in range(4):
        outline.addGeometry(Part.LineSegment(pts[i], pts[(i + 1) % 4]), False)
    constraints = [Sketcher.Constraint("Coincident", 0, 2, 1, 1),
                   Sketcher.Constraint("Coincident", 1, 2, 2, 1),
                   Sketcher.Constraint("Coincident", 2, 2, 3, 1),
                   Sketcher.Constraint("Coincident", 3, 2, 0, 1),
                   Sketcher.Constraint("Horizontal", 0),
                   Sketcher.Constraint("Vertical", 1),
                   Sketcher.Constraint("Horizontal", 2),
                   Sketcher.Constraint("Vertical", 3),
                   Sketcher.Constraint("Distance", 0, 80.0),
                   Sketcher.Constraint("Distance", 1, 30.0),
                   Sketcher.Constraint("DistanceX", 0, 1, -40.0),
                   Sketcher.Constraint("DistanceY", 0, 1, -15.0)]
    outline.addConstraint(constraints)
    _expression(outline, "Constraints[8]", "Parameters.length")
    _expression(outline, "Constraints[9]", "Parameters.width")
    _expression(outline, "Constraints[10]", "-Parameters.length / 2")
    _expression(outline, "Constraints[11]", "-Parameters.width / 2")

    pad = body.newObject("PartDesign::Pad", "Pad")
    pad.Label = "Plate thickness"
    pad.Profile = outline
    pad.Length = 6
    _expression(pad, "Length", "Parameters.thickness")
    outline.Visibility = False
    _must_recompute(doc, pad)

    holes = doc.addObject("Sketcher::SketchObject", "Holes")
    body.addObject(holes)
    holes.Label = "Two hole centers"
    holes.Placement.Base = App.Vector(0, 0, 6)
    _expression(holes, "Placement.Base.z", "Parameters.thickness")
    holes.addGeometry(Part.Circle(App.Vector(-25, 0, 0), App.Vector(0, 0, 1), 3), False)
    holes.addGeometry(Part.Circle(App.Vector(25, 0, 0), App.Vector(0, 0, 1), 3), False)
    holes.addConstraint([Sketcher.Constraint("Diameter", 0, 6.0),
                         Sketcher.Constraint("Diameter", 1, 6.0),
                         Sketcher.Constraint("DistanceX", 0, 3, -25.0),
                         Sketcher.Constraint("DistanceY", 0, 3, 0.0),
                         Sketcher.Constraint("DistanceX", 1, 3, 25.0),
                         Sketcher.Constraint("DistanceY", 1, 3, 0.0)])
    _expression(holes, "Constraints[0]", "Parameters.hole_diameter")
    _expression(holes, "Constraints[1]", "Parameters.hole_diameter")
    _expression(holes, "Constraints[2]", "-Parameters.hole_spacing / 2")
    _expression(holes, "Constraints[4]", "Parameters.hole_spacing / 2")

    pocket = body.newObject("PartDesign::Pocket", "Pocket")
    pocket.Label = "Through holes"
    pocket.Profile = holes
    pocket.Type = 1
    _must_recompute(doc, pocket)
    pad.Visibility = False
    holes.Visibility = False
    outline.Visibility = False
    pocket.Visibility = True
    return pocket


def _metrics(obj):
    shape = obj.Shape
    if shape.isNull() or not shape.isValid() or len(shape.Solids) != 1:
        raise RuntimeError("Expected one valid solid in final feature")
    box = shape.BoundBox
    return {"bbox_mm": [box.XLength, box.YLength, box.ZLength],
            "volume_mm3": shape.Volume, "solid_count": len(shape.Solids)}


def verify_editability(doc):
    """Edit a named spreadsheet dimension, check propagated geometry, then restore it."""
    params = doc.getObject("Parameters")
    final = doc.getObject("Pocket")
    if params is None or final is None:
        raise RuntimeError("Expected build(doc) objects Parameters and Pocket")
    baseline = _metrics(final)
    original = params.getContents("B2")
    try:
        params.set("B2", "100 mm")
        _must_recompute(doc, final)
        changed = _metrics(final)
        if abs(changed["bbox_mm"][0] - baseline["bbox_mm"][0] - 20.0) > 1e-5:
            raise RuntimeError("Spreadsheet length edit did not propagate to bounding box")
        expected_delta = 20.0 * 30.0 * 6.0
        if abs(changed["volume_mm3"] - baseline["volume_mm3"] - expected_delta) > 1e-4:
            raise RuntimeError("Spreadsheet length edit produced an unexpected volume change")
    finally:
        params.set("B2", original)
        _must_recompute(doc, final)
    restored = _metrics(final)
    if abs(restored["bbox_mm"][0] - baseline["bbox_mm"][0]) > 1e-5:
        raise RuntimeError("Restoring spreadsheet parameter did not restore geometry")
    if abs(restored["volume_mm3"] - baseline["volume_mm3"]) > 1e-4:
        raise RuntimeError("Restoring spreadsheet parameter did not restore volume")
    return {"editable": True, "parameter_tested": "length", "baseline": baseline,
            "after_edit": changed, "after_restore": restored,
            "native_features": ["Spreadsheet::Sheet", "Sketcher::SketchObject",
                                "PartDesign::Pad", "PartDesign::Pocket"],
            "limitations": "Illustrative two-hole plate only; dimensions and hole pattern are not validated hardware."}
