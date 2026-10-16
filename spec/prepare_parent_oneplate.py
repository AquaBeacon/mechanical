"""Generate canonical SCAD sources for the repeatable open parent mount."""
from pathlib import Path
import json
from parent_oneplate_frame_sources import frame_source, box_locator_source
from parent_oneplate_sensor_sources import td_support_source, camera_stop_source

ROOT = Path(__file__).resolve().parents[1]
PARTS = ROOT / "parts/parent/exterior/printed"

def save(name, source, manufacturing, variants=None):
    dest = PARTS / name
    dest.mkdir(parents=True, exist_ok=True)
    (dest / (name + ".scad")).write_text(source, encoding="utf-8")
    config = dict(manufacturing)
    config["source_dependencies"] = ["../../../../../" + p for p in (
        "spec/prepare_parent_oneplate.py", "spec/parent_oneplate_frame_sources.py",
        "spec/parent_oneplate_sensor_sources.py", "scad/lib/parent_oneplate_interfaces.scad",
        "scad/lib/edge_finished_profiles.scad", "scad/lib/util.scad",
    )]
    config["stl_export_format"] = "asciistl"
    config["portable_stl_export_format"] = "stl_ascii"
    config["step_coplanar_merge"] = True
    if name == "parent_oneplate_frame":
        config["degenerate_edge_flip_files"] = [name]
    elif name == "parent_oneplate_td_support":
        config["degenerate_edge_flip_files"] = [name]
    elif name == "parent_oneplate_box_locator":
        config["degenerate_edge_flip_files"] = [name + "_" + v for v in ("end_fixed", "end_push", "pressure_pad")]
    (dest / "manufacturing.json").write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if variants:
        (dest / "variants.txt").write_text(variants, encoding="utf-8")

def main():
    save("parent_oneplate_frame", frame_source(), {"print_rotations_deg": {"parent_oneplate_frame": [180, 0, 0]}})
    save("parent_oneplate_td_support", td_support_source(), {"print_rotations_deg": {"parent_oneplate_td_support": [-90, 0, 0]}})
    variants = "\n".join(f'{s} part="{s}"' for s in ("side_left", "side_right", "end_fixed", "end_push", "pressure_pad")) + "\n"
    save("parent_oneplate_box_locator", box_locator_source(), {"print_rotations_deg": {
        "parent_oneplate_box_locator_side_left": [0, 0, 0],
        "parent_oneplate_box_locator_side_right": [0, 0, 0],
        "parent_oneplate_box_locator_end_fixed": [0, 0, 0],
        "parent_oneplate_box_locator_end_push": [0, 0, 0],
        "parent_oneplate_box_locator_pressure_pad": [0, 0, 0],
    }}, variants)
    save("parent_oneplate_camera_stop", camera_stop_source(), {"print_rotations_deg": {"parent_oneplate_camera_stop": [0, 0, 0]}})
    print("Generated repeatable frame, keyed TD support, retained box locators, adjustable camera stops.")

if __name__ == "__main__":
    main()
