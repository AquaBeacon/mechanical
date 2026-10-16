"""OpenSCAD previews from authoritative placement.json and source STL."""
from pathlib import Path
import json
import subprocess
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASM = ROOT / "assemblies/quick_release_trials"
OSC = r"C:\Program Files\OpenSCAD\openscad.exe"
items = json.loads((ASM / "placement.json").read_text(encoding="utf-8"))["items"]
work = ASM / "_work/intermediate"
images = ASM / "_work/images"
logs = ASM / "_work/logs"
for folder in [work, images, logs]:
    folder.mkdir(parents=True, exist_ok=True)
canvas = Image.new("RGB", (1620, 970), "#fafafa")
draw = ImageDraw.Draw(canvas)
font = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 23)
small = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 18)
draw.text((60, 15), "Revised trials | Orange: male, Gray: female, Blue: pressure gib, Green: thumb bolt", font=font, fill="#26333d")
for row in range(2):
    for col, prefix in enumerate(["A", "B", "C"]):
        cad = (ROOT / "parts/common/jigs/quick_release_prototypes/quick_release_prototypes.scad").as_posix()
        lines = [f'use <{cad}>']
        for item in items:
            if not item["label"].startswith(prefix):
                continue
            ops = " ".join(f"{kind}({json.dumps(value)})" for op in item["ops"] for kind, value in op.items())
            shift = [55 if col==0 else (-55 if col==2 else 0), 0, 0]
            if row:
                if "male" in item["label"] and "female" not in item["label"]:
                    shift[1] -= 40 if prefix=="B" else 0
                    shift[2] += 22 if prefix!="B" else 0
                if "knob" in item["label"]:
                    if prefix=="A": shift[0] += 16
                    if prefix=="C": shift[0] += 16
                if "gib" in item["label"]: shift[0] += 10
            source = (ROOT / item["part"] / (item["file"]+".stl")).as_posix()
            lines.append(f'color("{item["color"]}") translate({json.dumps(shift)}) {ops} import("{source}");')
        if prefix in ["A","C"]:
            kind = "slide" if prefix=="A" else "twist"
            if row:
                lines.append(f'color("Silver") fixed_nut("{kind}");')
                lines.append(f'color("Silver") translate([16,0,0]) through_bolt("{kind}");')
            else:
                lines.append(f'color("Silver") metal_stack("{kind}");')
        if prefix=="C":
            lines.append(f'color("Tomato") twist_pad_reference(compressed={"false" if row else "true"},travel={22 if row else 0});')
        scad = work / f"preview_{prefix}_{row}.scad"
        png = images / f"preview_{prefix}_{row}.png"
        scad.write_text("\n".join(lines), encoding="utf-8")
        result = subprocess.run([OSC, "-o", str(png), "--imgsize=540,400", "--autocenter", "--viewall",
                                 "--camera=0,0,0,58,0,25,145", "--colorscheme=Tomorrow", str(scad)],
                                capture_output=True, text=True,
                                creationflags=subprocess.CREATE_NO_WINDOW if os.name=="nt" else 0)
        (logs / f"preview_{prefix}_{row}.log").write_text(result.stdout+result.stderr, encoding="utf-8")
        if result.returncode or "ERROR:" in result.stderr or "WARNING:" in result.stderr:
            raise RuntimeError(str(scad))
        canvas.paste(Image.open(png).convert("RGB"), (540*col, 80+row*430))
        label = ["A  Slide + through-bolt clamp", "B  Hooks protrude 1.5 mm", "C  1 mm rubber bonded under lid + cam lock"][col]
        draw.text((540*col+30, 55+row*430), label+(" (closed)" if not row else " (separated)"), font=small, fill="#26333d")
draw.text((60, 940), "Silver: metal hardware. Physical fit/retention tests pending. C: withdraw thumb bolt before turning.", font=small, fill="#26333d")
canvas.save(images / "comparison.png")
cad = (ROOT / "parts/common/jigs/quick_release_prototypes/quick_release_prototypes.scad").as_posix()
lid = next(item for item in items if item["label"] == "C twist male")
lid_stl = (ROOT / lid["part"] / (lid["file"]+".stl")).as_posix()
lid_z = lid["ops"][0]["translate"][2]
bond_scad = work / "preview_C_rubber_bond.scad"
bond_png = images / "preview_C_rubber_bond.png"
bond_scad.write_text(f'use <{cad}>\ncolor("Orange") import("{lid_stl}");\n'
                     f'color("Tomato") rotate([180,0,0]) translate([0,0,-{lid_z}]) twist_pad_reference(compressed=false);\n',
                     encoding="utf-8")
result = subprocess.run([OSC, "-o", str(bond_png), "--imgsize=700,520", "--autocenter", "--viewall",
                         "--camera=0,0,0,50,0,25,125", "--colorscheme=Tomorrow", str(bond_scad)],
                        capture_output=True, text=True,
                        creationflags=subprocess.CREATE_NO_WINDOW if os.name=="nt" else 0)
(logs / "preview_C_rubber_bond.log").write_text(result.stdout+result.stderr, encoding="utf-8")
if result.returncode or "ERROR:" in result.stderr or "WARNING:" in result.stderr:
    raise RuntimeError(str(bond_scad))
empty_scad = work / "preview_C_pocket_empty.scad"
empty_png = images / "preview_C_pocket_empty.png"
empty_scad.write_text(f'color("Orange") import("{lid_stl}");\n', encoding="utf-8")
result = subprocess.run([OSC, "-o", str(empty_png), "--imgsize=700,520", "--autocenter", "--viewall",
                         "--camera=0,0,0,50,0,25,125", "--colorscheme=Tomorrow", str(empty_scad)],
                        capture_output=True, text=True,
                        creationflags=subprocess.CREATE_NO_WINDOW if os.name=="nt" else 0)
(logs / "preview_C_pocket_empty.log").write_text(result.stdout+result.stderr, encoding="utf-8")
if result.returncode or "ERROR:" in result.stderr or "WARNING:" in result.stderr:
    raise RuntimeError(str(empty_scad))
print(images / "comparison.png")
