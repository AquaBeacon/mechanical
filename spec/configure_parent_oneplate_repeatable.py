"""One-time, idempotent placement migration for the retained locating hardware."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assemblies/parent_oneplate"

def main():
    path = OUT / "placement.json"
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    history = OUT / "_work/analysis/repeatable_mount/history"
    history.mkdir(parents=True, exist_ok=True)
    if not (history / "placement_before_locators.json").exists():
        (history / "placement_before_locators.json").write_bytes(path.read_bytes())
        (history / "README_before_locators.md").write_bytes((OUT / "README.md").read_bytes())
    data["items"] = [i for i in data["items"] if not i["label"].startswith("locating_")]
    data["note"] = "Repeatable box locating: three bottom datums, left two-point datum, end datum, retained keyed stops. Sensor support and camera mount register to the same open frame."
    data["coordinate_system"] = "Box bottom Z=0; datum seats Z=0, main deck top Z=-0.8, underside Z=-12."
    for i in data["items"]:
        if i["label"] == "camera_mount":
            i["note"] = "Existing mount remains installed; seat its rear-plate end and right edge against the frame guides before tightening M3."
    def item(label, folder, file, ops=None, group="exterior", color="MediumSeaGreen", note=None):
        row = dict(label="locating_" + label, part=folder, file=file, ops=ops or [], group=group, color=color)
        if note:
            row["note"] = note
        data["items"].append(row)
    folder="parts/parent/exterior/printed/parent_oneplate_box_locator"
    for variant in ("side_left", "side_right", "end_fixed", "end_push"):
        item(variant, folder, "parent_oneplate_box_locator_" + variant)
    for y in (-38, 38):
        item("pressure_pad_" + str(y), folder, "parent_oneplate_box_locator_pressure_pad", [{"translate": [105,y,12]}, {"rotate": [0,90,0]}])
    item("pressure_pad_end", folder, "parent_oneplate_box_locator_pressure_pad", [{"translate": [-94,-115,9]}, {"rotate": [90,0,0]}])
    item("camera_stop", "parts/parent/exterior/printed/parent_oneplate_camera_stop", "parent_oneplate_camera_stop", [{"translate": [-40,-40,-55.45]}, {"rotate": [-90,0,0]}], note="Fit adjustable contact tips to real case once; retain settings. Remove bridge before accessing rear M3 bolts.")
    screws="parts/common/interior/cots/screw"
    def fast(label,file,xyz,rot=None):
        ops=[{"translate": xyz}]
        if rot:
            ops.append({"rotate": rot})
        item(label,screws,"screw_"+file,ops,"hardware","Silver")
    for x in (-110,110):
        for y in (-8,8):
            fast(f"side_bolt_{x}_{y}","m4x16_socket",[x,y,1.4])
            fast(f"side_nut_{x}_{y}","nut_m4",[x,y,-12])
    for s in (-1,1):
        for y in (52,62):
            fast(f"end_bolt_{s}_{y}","m4x14_socket",[s*94,s*y,-14.4],[180,0,0])
            fast(f"end_nut_{s}_{y}","nut_m4",[s*94,s*y,-4.2])
    for y in (-38,38):
        fast(f"press_bolt_{y}","m4x25_socket",[110.2,y,12],[0,-90,0])
        fast(f"press_nut_{y}","nut_m4",[112.6,y,12],[0,90,0])
        fast(f"press_locknut_{y}","nut_m4",[116,y,12],[0,90,0])
    fast("press_bolt_end","m4x25_socket",[-94,-120.2,9],[-90,0,0])
    fast("press_nut_end","nut_m4",[-94,-127,9],[-90,0,0])
    fast("press_locknut_end","nut_m4",[-94,-130.2,9],[-90,0,0])
    # Camera local Y maps to assembly Z; contact screws run along local Z.
    for x in (-20,20):
        item(f"camera_bridge_bolt_{x}",screws,"screw_m4x20_socket",[{"translate":[-40,-40,-55.45]},{"rotate":[-90,0,0]},{"translate":[x,35,20]},{"rotate":[-90,0,0]}],"hardware","Silver")
        item(f"camera_bridge_nut_{x}",screws,"screw_nut_m4",[{"translate":[-40,-40,-55.45]},{"rotate":[-90,0,0]},{"translate":[x,19.8,20]},{"rotate":[-90,0,0]}],"hardware","Silver")
        item(f"camera_adjust_bolt_{x}",screws,"screw_m4x12_socket",[{"translate":[-40,-40,-55.45]},{"rotate":[-90,0,0]},{"translate":[x,20,24.5]},{"rotate":[180,0,0]}],"hardware","Silver")
        item(f"camera_adjust_nut_{x}",screws,"screw_nut_m4",[{"translate":[-40,-40,-55.45]},{"rotate":[-90,0,0]},{"translate":[x,20,32.2]}],"hardware","Silver")
        item(f"camera_adjust_locknut_{x}",screws,"screw_nut_m4",[{"translate":[-40,-40,-55.45]},{"rotate":[-90,0,0]},{"translate":[x,20,29.0]}],"hardware","Silver")
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+"\n",encoding="utf-8")
    (OUT / "print_config.json").write_text(json.dumps({"status":"prototype_repeatable_locating", "note":"位置決め追加の試作。PETG・0.20 mm・壁6周・上下6層・40%・ブリム5 mm・通常サポートON。camera_mount.stlは既存品を再利用できる。初回の実物合わせと反復着脱試験は未実施。現行3MFはprint_jobs/repeatable_mount/。"},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    variants=ROOT / screws / "variants.txt"
    old=variants.read_text(encoding="utf-8-sig")
    additions=[]
    for length in (12,14,16,20,25):
        name=f"m4x{length}_socket"
        if not any(line.startswith(name+" ") for line in old.splitlines()):
            additions.append(f"{name} d=4 l={length} head_d=7 head_h=4")
    if additions:
        variants.write_text(old.rstrip()+"\n\n# Repeatable parent locator hardware: M4 socket-head envelope, purchased metal\n"+"\n".join(additions)+"\n",encoding="utf-8")
    print("Configured retained box locators, pressure shoes, camera stop and M4 hardware.")

if __name__ == "__main__":
    main()
