"""Open a verified template in the real FreeCAD GUI (explicit user action only)."""
import argparse
import json
from pathlib import Path

from cli import ROOT, digest, read_json
from service import CadService


def choose_template(service):
    for report_path in sorted(service.runs.glob("*/report.json"), reverse=True):
        try:
            report = read_json(report_path)
            model = report_path.parent / "model.FCStd"
            if report.get("kind") == "demo" and report.get("status") == "passed" and model.is_file() and digest(model) == report.get("model_sha256"):
                return model
        except (OSError, ValueError):
            continue
    return Path(service.create_demo()["model"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Print the selected file without opening the GUI")
    args = parser.parse_args()
    service = CadService(ROOT)
    path = choose_template(service)
    result = {"path": str(path)} if args.dry_run else service.open_document(str(path))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
