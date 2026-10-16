"""Collect review images and loose build files in each component's _work/.

`plan` is read-only, `apply` moves files and updates existing document links,
`check` fails on loose files. Historical generators may be followed by `apply`.
The move journal stores hashes and old/new locations; no model is deleted.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMAGES = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}
LOOSE = {".log": "logs", ".err": "logs", ".csg": "intermediate", ".tmp": "intermediate"}
TEXT = {".md", ".html", ".json", ".txt", ".scad", ".py", ".ps1", ".sh"}


def owners():
    result = []
    for category in ("printed", "cots", "pcb", "jigs", "cabling"):
        for directory in (ROOT / "parts").rglob(category):
            if directory.is_dir():
                result.extend(p for p in directory.iterdir() if p.is_dir() and p.name != "_work")
    for root_name in ("assemblies", "print_jobs", "outputs"):
        directory = ROOT / root_name
        if not directory.is_dir():
            continue
        result.extend(p for p in directory.iterdir() if p.is_dir() and p.name != "_work")
        result.append(directory)
    result.append(ROOT / "spec")
    return sorted(set(result), key=lambda p: len(p.parts), reverse=True)


def plan():
    moves = []
    seen = set()
    for owner in owners():
        for path in sorted(owner.rglob("*")):
            if not path.is_file() or path in seen:
                continue
            rel = path.relative_to(owner)
            if "_work" in rel.parts:
                seen.add(path)
                continue
            # Images at any depth; loose logs/intermediates only at component root.
            if path.suffix.lower() in IMAGES:
                target = owner / "_work" / "images" / rel
            elif len(rel.parts) == 1 and path.suffix.lower() in LOOSE:
                target = owner / "_work" / LOOSE[path.suffix.lower()] / rel
            else:
                seen.add(path)
                continue
            if not target.resolve().is_relative_to(owner.resolve()) or not path.resolve().is_relative_to(ROOT):
                raise ValueError(f"unsafe move: {path}")
            moves.append((path, target))
            seen.add(path)
    return moves


def relink(moves):
    """Resolve document/data references against their actual former locations.

    Python output expressions are left intact: they must be followed by tidy.
    Plain full workspace paths in code/docs are rewritten as well.
    """
    mapping = {a.resolve(): b.resolve() for a, b in moves}
    updated = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT or path.name in ("tidy_workspace.py", "tidy_journal.json"):
            continue
        raw = path.read_bytes()
        encoding = "utf-8-sig" if raw.startswith(b"\xef\xbb\xbf") else "utf-8"
        try:
            content = raw.decode(encoding)
        except UnicodeDecodeError:
            # Several legacy docs were written as CP932; preserve that encoding.
            encoding = "cp932"
            try:
                content = raw.decode(encoding)
            except UnicodeDecodeError:
                continue
        old = content
        # Root-relative paths occur in model notes and generator source strings.
        for source, target in moves:
            before = source.relative_to(ROOT).as_posix()
            after = target.relative_to(ROOT).as_posix()
            content = content.replace(before, after)
            content = content.replace(before.replace("/", "\\"), after.replace("/", "\\"))
        if path.suffix.lower() in (".md", ".html", ".json", ".txt"):
            # Paths in Markdown, HTML attributes, quoted JSON data, or backticks.
            pattern = r"(?<![A-Za-z0-9_./\\-])(?P<path>(?:[A-Za-z]:[/\\]|\.{1,2}[/\\])?[^\s\"'`<>()[\]{}]{1,768}\.(?:png|jpe?g|webp|gif|svg|log|err|csg|tmp))"
            def replace(match):
                ref = match.group("path")
                normalized = ref.replace("\\", "/")
                candidates = [(path.parent / normalized).resolve(), (ROOT / normalized).resolve()]
                for candidate in candidates:
                    if candidate in mapping:
                        new = mapping[candidate]
                        return os.path.relpath(new, path.parent).replace("\\", "/") if candidate == candidates[0] else new.relative_to(ROOT).as_posix()
                return ref
            content = re.sub(pattern, replace, content, flags=re.IGNORECASE)
        if content != old:
            path.write_bytes(content.encode(encoding))
            updated.append(path.relative_to(ROOT).as_posix())
    return updated


def apply(moves):
    if not moves:
        print("PASS: workspace already tidy; no files moved")
        return
    updated = relink(moves)
    journal = ROOT / "tools" / "_work" / "tidy_journal.json"
    history = json.loads(journal.read_text(encoding="utf-8")) if journal.exists() else []
    for source, target in moves:
        sha = hashlib.sha256(source.read_bytes()).hexdigest()
        target.parent.mkdir(parents=True, exist_ok=True)
        # Preserve an older preview before promoting a newly rebuilt one.
        if target.exists() and source.read_bytes() != target.read_bytes():
            previous_sha = hashlib.sha256(target.read_bytes()).hexdigest()
            archive = target.parent / "history" / (target.stem + "_" + previous_sha[:12] + target.suffix)
            if not archive.resolve().is_relative_to(target.parent.resolve()):
                raise ValueError(f"unsafe archive path: {archive}")
            archive.parent.mkdir(exist_ok=True)
            if archive.exists():
                if hashlib.sha256(archive.read_bytes()).hexdigest() != previous_sha:
                    raise ValueError(f"archive collision: {archive}")
                target.unlink()
            else:
                target.rename(archive)
            history.append({"from": target.relative_to(ROOT).as_posix(), "to": archive.relative_to(ROOT).as_posix(), "sha256": previous_sha, "reason": "replaced by newer build"})
        # An identical older copy may already be there after a legacy rebuild.
        if target.exists():
            source.unlink()
        else:
            source.rename(target)
        history.append({"from": source.relative_to(ROOT).as_posix(), "to": target.relative_to(ROOT).as_posix(), "sha256": sha})
    journal.parent.mkdir(parents=True, exist_ok=True)
    journal.write_text(json.dumps(history, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"MOVED {len(moves)} files; updated {len(updated)} text files; journal: tools/_work/tidy_journal.json")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("plan", "apply", "check"))
    args = parser.parse_args()
    moves = plan()
    if args.command == "apply":
        apply(moves)
    elif moves:
        for source, target in moves[:30]:
            print(source.relative_to(ROOT).as_posix(), "->", target.relative_to(ROOT).as_posix())
        print(f"LOOSE {len(moves)} files")
        if args.command == "check":
            raise SystemExit(1)
    else:
        print("PASS: all review images and loose build files are under _work/")


if __name__ == "__main__":
    main()
