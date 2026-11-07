"""Generate canonical SCAD sources for the repeatable open parent mount."""
from pathlib import Path
import json
from parent_oneplate_frame_sources import frame_source, box_locator_source
from parent_exterior_revision_sources import bar_source, stand_source, qr_source
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
        "spec/parent_oneplate_sensor_sources.py", "spec/parent_exterior_revision_sources.py",
        "parts/common/jigs/quick_release_prototypes/quick_release_prototypes.scad", "scad/lib/parent_oneplate_interfaces.scad",
        "scad/lib/edge_finished_profiles.scad", "scad/lib/util.scad",
    )]
    config["stl_export_format"] = "asciistl"
    config["portable_stl_export_format"] = "stl_ascii"
    config["step_coplanar_merge"] = True
    if name == "parent_oneplate_frame":
        config["degenerate_edge_flip_files"] = [name]
        config["degenerate_precision_weld_files"] = [name]
        config["source_dependencies"].append("../../../exterior/cots/bcas212310g/dimensions.json")
        config["source_dependencies"].append("../../../../../spec/parent_oneplate_mounting_pattern.json")
        # Keep the verified exported surface; broad planar welding on the large
        # solid plate exceeds the compactor's absolute volume-change tolerance.
        config["step_coplanar_merge"] = False
    elif name == "parent_oneplate_td_support":
        config["degenerate_edge_flip_files"] = [name]
        config["degenerate_precision_weld_files"] = [name]
    elif name == "parent_oneplate_box_locator":
        config["degenerate_edge_flip_files"] = [name + "_" + v for v in ("end_fixed", "end_push", "pressure_pad")]
        config["degenerate_precision_weld_files"] = [name + "_pressure_pad"]
    elif name == "parent_oneplate_stand":
        config["degenerate_edge_flip_files"] = [name]
    elif name == "parent_oneplate_camera_qr":
        config["degenerate_edge_flip_files"] = [name + "_female", name + "_male"]
        config["layer_heights_mm"] = {name + "_female": 0.1, name + "_male": 0.1}
    (dest / "manufacturing.json").write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if variants:
        (dest / "variants.txt").write_text(variants, encoding="utf-8")

def main():
    save("parent_oneplate_bar", bar_source(), {"print_rotations_deg": {"parent_oneplate_bar": [0,0,0]}})
    save("parent_oneplate_stand", stand_source(), {"print_rotations_deg": {"parent_oneplate_stand": [0,90,0]}})
    save("parent_oneplate_camera_qr", qr_source(), {"print_rotations_deg": {"parent_oneplate_camera_qr_female": [0,0,0], "parent_oneplate_camera_qr_male": [0,0,0]}}, 'female part="female"\nmale part="male"\n')
    save("parent_oneplate_frame", frame_source(), {"print_rotations_deg": {"parent_oneplate_frame": [0, 0, 0]}})
    save("parent_oneplate_td_support", td_support_source(), {"print_rotations_deg": {"parent_oneplate_td_support": [0, -90, 0]}})
    variants = "\n".join(f'{s} part="{s}"' for s in ("side_left", "side_right", "end_fixed", "end_push", "pressure_pad")) + "\n"
    save("parent_oneplate_box_locator", box_locator_source(), {"print_rotations_deg": {
        "parent_oneplate_box_locator_side_left": [0, 0, 0],
        "parent_oneplate_box_locator_side_right": [0, 0, 0],
        "parent_oneplate_box_locator_end_fixed": [0, 90, 0],
        "parent_oneplate_box_locator_end_push": [0, 90, 0],
        "parent_oneplate_box_locator_pressure_pad": [0, 0, 0],
    }}, variants)
    save("parent_oneplate_camera_stop", camera_stop_source(), {"print_rotations_deg": {"parent_oneplate_camera_stop": [-90, 0, 0]}})
    print("Generated flat plate with removable locators, flat-seat TD support, C adapters and retained accessories.")

if __name__ == "__main__":
    main()
