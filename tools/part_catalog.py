"""Search reusable source parts and show which assemblies use them."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("keywords", nargs="*", help="case-insensitive source name/path keywords")
    args = parser.parse_args()
    uses = {}
    for assembly in sorted((ROOT / "assemblies").iterdir()):
        if not assembly.is_dir():
            continue
        placement = assembly / "placement.json"
        if placement.exists():
            data = json.loads(placement.read_text(encoding="utf-8-sig"))
            for item in data.get("items", data.get("parts", [])):
                uses.setdefault(item["part"], set()).add(assembly.name)
        config = assembly / "print_config.json"
        if config.exists():
            for item in json.loads(config.read_text(encoding="utf-8-sig")).get("extra_parts", []):
                uses.setdefault(item["part"], set()).add(assembly.name)
    candidates = set()
    for category in ("printed", "cots", "pcb", "jigs", "cabling"):
        for folder in (ROOT / "parts").rglob(category):
            if folder.is_dir():
                candidates.update(p.relative_to(ROOT).as_posix() for p in folder.iterdir() if p.is_dir() and p.name != "_work")
    candidates.update(uses)
    for part in sorted(candidates):
        if not all(keyword.casefold() in part.casefold() for keyword in args.keywords):
            continue
        folder = ROOT / part
        definitions = sorted(p.name for p in folder.glob("*.scad"))
        print(part)
        print("  CAD:", ", ".join(definitions) or "reference / generated CAD")
        print("  assemblies:", ", ".join(sorted(uses.get(part, []))) or "not in current placements (standalone / history)")


if __name__ == "__main__":
    main()
