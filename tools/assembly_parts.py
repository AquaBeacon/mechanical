"""Generate portable print sets from shared CAD and assembly placements.

Only STL deliverables are copied; CAD definitions remain in their source folders.
Run `python tools/assembly_parts.py sync` or `check` from any working directory.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def within(path, base=None):
    base = ROOT if base is None else base
    path = path.resolve()
    if not path.is_relative_to(base.resolve()):
        raise ValueError(f"path escapes {base}: {path}")
    return path


def source_path(part, stem):
    if Path(stem).name != stem or not re.fullmatch(r"[A-Za-z0-9_.-]+", stem):
        raise ValueError(f"invalid file stem: {stem}")
    return within(ROOT / part / (stem + ".stl"))


def is_printed(item):
    if "print" in item:
        return bool(item["print"])
    folder = within(ROOT / item["part"])
    metadata = folder / "manufacturing.json"
    stem = item.get("file") or folder.name
    if metadata.exists() and stem in read(metadata).get("non_print_files", []):
        return False
    segments = Path(item["part"]).parts
    return "printed" in segments or "jigs" in segments


def linear_matrix(ops):
    """Full linear transform, retaining rotations around scales/reflections."""
    import numpy as np
    matrix = np.eye(3)
    for op in ops:
        for kind, value in op.items():
            if kind == "translate":
                continue
            if kind == "rotate":
                x, y, z = np.radians(value)
                cx, cy, cz, sx, sy, sz = math.cos(x), math.cos(y), math.cos(z), math.sin(x), math.sin(y), math.sin(z)
                transform = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]]) @ np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]]) @ np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
            elif kind == "scale":
                transform = np.diag(value)
            elif kind == "mirror":
                n = np.asarray(value, dtype=float)
                transform = np.eye(3) if n @ n == 0 else np.eye(3) - 2 * np.outer(n, n) / (n @ n)
            else:
                raise ValueError(f"unknown placement operation: {kind}")
            matrix = matrix @ transform
    # Polar decomposition removes rigid rotation, while preserving chirality.
    u, s, vt = np.linalg.svd(matrix)
    if min(s) < 1e-9:
        raise ValueError("zero scale cannot be printed")
    stretch = vt.T @ np.diag(s) @ vt
    reflection = np.diag([-1, 1, 1]) if np.linalg.det(matrix) < 0 else np.eye(3)
    return np.round(reflection @ stretch, 9)


def definitions(assembly):
    config_path = assembly / "print_config.json"
    config = read(config_path) if config_path.exists() else {}
    placement = assembly / "placement.json"
    data = read(placement) if placement.exists() else {}
    rows = data.get("items", data.get("parts", []))
    entries = {}
    for item in rows:
        if not is_printed(item):
            continue
        stem = item.get("file") or Path(item["part"]).name
        shape = linear_matrix(item.get("ops", []))
        key = (item["part"], stem, tuple(shape.flatten()))
        if key not in entries:
            entries[key] = {"part": item["part"], "stem": stem, "shape": shape.tolist(), "quantity": 0, "labels": []}
        entries[key]["quantity"] += 1
        entries[key]["labels"].append(item.get("label", stem))
    for item in config.get("extra_parts", []):
        stem = item["file"]
        key = (item["part"], stem, "extra")
        if any(e["part"] == item["part"] and e["stem"] == stem for e in entries.values()):
            raise ValueError(f"duplicate extra part: {stem}")
        if not isinstance(item.get("quantity", 1), int) or item.get("quantity", 1) < 1:
            raise ValueError(f"invalid extra part quantity: {stem}")
        entries[key] = {"part": item["part"], "stem": stem, "shape": [[1, 0, 0], [0, 1, 0], [0, 0, 1]], "quantity": item.get("quantity", 1), "labels": item.get("labels", [stem])}
    used = set()
    for entry in entries.values():
        import numpy as np
        shape = np.asarray(entry["shape"])
        base = entry["stem"]
        if not np.allclose(shape, np.eye(3)):
            if np.allclose(shape, np.diag([-1, 1, 1])):
                base += "_mirrored"
            else:
                base += "_shape_" + hashlib.sha256(json.dumps(entry["shape"]).encode()).hexdigest()[:8]
        if base in used:
            base += "_" + hashlib.sha256(entry["part"].encode()).hexdigest()[:8]
        used.add(base)
        entry["file"] = base + ".stl"
        metadata_path = ROOT / entry["part"] / "manufacturing.json"
        metadata = read(metadata_path) if metadata_path.exists() else {}
        entry["rotation_deg"] = config.get("orientations", {}).get(entry["stem"], metadata.get("print_rotations_deg", {}).get(entry["stem"], [0, 0, 0]))
    return list(entries.values()), config


def part_sources(part):
    folder = ROOT / part
    paths = set()
    for pattern in ("*.scad", "variants.txt", "manufacturing.json", "*.md", "*.py"):
        paths.update(folder.glob(pattern))
    metadata = folder / "manufacturing.json"
    if metadata.exists():
        for relative in read(metadata).get("source_dependencies", []):
            dependency = within(folder / relative)
            if not dependency.is_file():
                raise ValueError(f"missing CAD source dependency: {dependency}")
            paths.add(dependency)
    for doc in folder.glob("*.md"):
        content = doc.read_text(encoding="utf-8-sig", errors="replace").replace("\\", "/")
        for ref in re.findall(r"spec/[A-Za-z0-9_/.-]+\.py", content):
            generator = within(ROOT / ref)
            if generator.is_file():
                paths.add(generator)
    # Shared dimensional modules also trigger staleness, including nested includes.
    pending = list(paths)
    while pending:
        path = pending.pop()
        if path.suffix != ".scad":
            continue
        for ref in re.findall(r"(?:include|use)\s*<([^>]+)>", path.read_text(encoding="utf-8-sig")):
            dependency = (path.parent / ref).resolve()
            if dependency.is_relative_to(ROOT) and dependency.is_file() and dependency not in paths:
                paths.add(dependency)
                pending.append(dependency)
    return paths


def supporting_sources(assembly, entries):
    paths = set()
    for part in {entry["part"] for entry in entries}:
        paths.update(part_sources(part))
    for name in ("placement.json", "print_config.json", "manufacturing_parts.json", "README.md"):
        if (assembly / name).exists():
            paths.add(assembly / name)
    config_path = assembly / "print_config.json"
    if config_path.exists():
        paths.update(within(ROOT / ref) for ref in read(config_path).get("notes", []))
    return {p.relative_to(ROOT).as_posix(): digest(p) for p in sorted(paths)}


def build(assembly):
    import numpy as np
    import trimesh
    entries, config = definitions(assembly)
    dest = assembly / "parts"
    dest.mkdir(exist_ok=True)
    old_path = dest / "manifest.json"
    old = read(old_path) if old_path.exists() else {}
    source_hashes = supporting_sources(assembly, entries)
    # Repackaging must not silently accept a changed CAD with an old STL.
    changed_cad = [ROOT / name for name, sha in source_hashes.items()
                   if name.endswith((".scad", ".py", ".stl", ".npy")) and name in old.get("source_hashes", {})
                   and old["source_hashes"][name] != sha]
    if changed_cad:
        for entry in entries:
            affected = set(changed_cad) & part_sources(entry["part"])
            if not affected:
                continue
            latest_change = max(path.stat().st_mtime_ns for path in affected)
            src = source_path(entry["part"], entry["stem"])
            if src.stat().st_mtime_ns < latest_change:
                raise ValueError(f"CAD changed; rebuild STL before sync: {src.relative_to(ROOT)}")
    generated = []
    for entry in entries:
        src = source_path(entry["part"], entry["stem"])
        if not src.is_file():
            raise ValueError(f"missing print source: {src}")
        mesh = trimesh.load(src, force="mesh")
        metadata_path = src.parent / "manufacturing.json"
        metadata = read(metadata_path) if metadata_path.exists() else {}
        known_issue = metadata.get("known_mesh_issues", {}).get(entry["stem"])
        if (not mesh.is_watertight or not mesh.is_winding_consistent) and not known_issue:
            raise ValueError(f"invalid print mesh: {src}")
        entry["mesh_warning"] = known_issue
        transform = trimesh.transformations.euler_matrix(*np.radians(entry["rotation_deg"]))
        shape = np.eye(4)
        shape[:3, :3] = entry["shape"]
        transform = transform @ shape
        mesh.apply_transform(transform)
        transform[:3, 3] = -mesh.bounds[0]
        mesh.apply_translation(transform[:3, 3])
        target = within(dest / entry["file"], dest)
        export_format = metadata.get("portable_stl_export_format", "stl")
        if export_format not in ("stl", "stl_ascii"):
            raise ValueError(f"invalid portable STL format: {export_format}")
        mesh.export(target, file_type=export_format)
        # Bed translation can move distinct float32 coordinates into the same
        # rounding bin. Validate the saved copy, not just its in-memory source.
        packed = trimesh.load(target, force="mesh")
        if not known_issue and (not packed.is_watertight or not packed.is_winding_consistent
                or (mesh.is_volume and not packed.is_volume)
                or packed.euler_number != mesh.euler_number
                or np.count_nonzero(packed.area_faces == 0) > np.count_nonzero(mesh.area_faces == 0)):
            raise ValueError(f"invalid exported print mesh: {target}; preserve precision with portable_stl_export_format=stl_ascii")
        entry.update(source=src.relative_to(ROOT).as_posix(), source_sha256=digest(src), sha256=digest(target), extents_mm=packed.extents.round(4).tolist(), model_to_print=transform.tolist(), watertight=bool(packed.is_watertight), stl_format=export_format, fits_x1c_250=bool(max(packed.extents) <= 250.01))
        generated.append(entry["file"])
    modifiers = []
    for modifier in config.get("modifiers", []):
        host = next(e for e in entries if e["stem"] == modifier["host"])
        src = within(ROOT / modifier["source"])
        mesh = trimesh.load(src, force="mesh")
        mesh.apply_transform(np.asarray(host["model_to_print"]))
        filename = "modifiers/" + Path(modifier["source"]).name
        target = within(dest / filename, dest)
        target.parent.mkdir(exist_ok=True)
        mesh.export(target)
        generated.append(filename)
        modifiers.append({**modifier, "file": filename, "host_file": host["file"], "source_sha256": digest(src), "sha256": digest(target)})
    notes = []
    assembly_readme = assembly / "README.md"
    if assembly_readme.exists():
        notes.append(f"## {assembly.name}/README.md\n\n{assembly_readme.read_text(encoding='utf-8-sig')}\n")
    for part in sorted({e["part"] for e in entries}):
        for doc in sorted((ROOT / part).glob("*.md")):
            content = doc.read_text(encoding="utf-8-sig", errors="replace")
            notes.append(f"## {part}/{doc.name}\n\n{content}\n")
    for reference in config.get("notes", []):
        doc = within(ROOT / reference)
        if doc != assembly_readme:
            notes.append(f"## {reference}\n\n{doc.read_text(encoding='utf-8-sig')}\n")
    # Embedded text keeps material/orientation cautions available when copied out.
    note_path = dest / "DESIGN_NOTES.md"
    note_path.write_text("# 設計・印刷条件の控え（自動生成）\n\n以下は設計元の文書を転記したものです。リンク先は元フォルダ基準です。印刷条件と未検証事項を確認してください。\n\n" + "\n".join(notes), encoding="utf-8")
    generated.append("DESIGN_NOTES.md")
    result = {"schema_version": 1, "assembly": assembly.name, "release_status": config.get("status", "existing_prototype"), "note": config.get("note", "既存構成の印刷データを整理。強度・造形性の新規認証ではない。"), "source_hashes": source_hashes, "parts": entries, "modifiers": modifiers}
    rows = ["# 印刷一式\n", f"対象: `{assembly.name}`。同じ部品は表の数量だけ複製してください。\n", result["note"] + "\n", "STLは全てこのフォルダ内の実ファイルです。このフォルダをコピーして印刷できます。組立配置は除き、最小XYZを0へ移動済み。鏡像・スケールは反映済みです。CAD原本は編集せず、設計元を更新して再生成します。\n", "| STL | 個数 | 外形 mm | 設計元からの回転 X/Y/Z ° | X1C 250³ |", "|---|---:|---|---|---|"]
    for entry in entries:
        dims = " × ".join(f"{x:g}" for x in entry["extents_mm"])
        rows.append(f"| [{entry['file']}]({entry['file']}) | {entry['quantity']} | {dims} | {entry['rotation_deg']} | {'枠内' if entry['fits_x1c_250'] else '**枠外・分割等が必要**'} |")
    for entry in entries:
        if entry.get("mesh_warning"):
            rows.append(f"\n**{entry['file']} の既存不具合:** {entry['mesh_warning']}\n")
    if not entries:
        rows.append("\nこの構成は探索記録のみで、確定した印刷用部品はありません。")
    rows += ["\n回転0°のものは設計元の姿勢を保っています。枠内の判定は外形だけです。サポート・積層方向・材料・強度の条件は [設計元の説明](DESIGN_NOTES.md) と上のassemblyの説明を確認してください。", "\n`manifest.json` は出所、個数、鏡像変換、元STLとコピーのSHA-256を記録します。コピーを編集すると検査で不一致になります。"]
    if modifiers:
        rows.append("\n## モディファイア（印刷部品ではない）\n")
        for modifier in modifiers:
            rows.append(f"- [{modifier['file']}]({modifier['file']}) を `{modifier['host_file']}` と同じオブジェクトに読み込み、モディファイアとして局所100%に設定。両方の相対座標を保持し、個別の自動整列をしない。")
    (dest / "PRINT.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    generated.append("PRINT.md")
    result["generated_files"] = generated
    result["document_hashes"] = {name: digest(dest / name) for name in ("DESIGN_NOTES.md", "PRINT.md")}
    # Remove only files previously owned by this generator, never user files.
    for filename in set(old.get("generated_files", [])) - set(generated):
        stale = within(dest / filename, dest)
        if stale.is_file():
            stale.unlink()
    write_json(old_path, result)
    return len(entries), sum(e["quantity"] for e in entries)


def check(assembly):
    dest = assembly / "parts"
    manifest_path = dest / "manifest.json"
    if not manifest_path.is_file():
        return ["missing parts/manifest.json"]
    manifest = read(manifest_path)
    expected, config = definitions(assembly)
    errors = []
    fields = ("part", "stem", "shape", "quantity", "labels", "file", "rotation_deg")
    simplify = lambda rows: [{k: row[k] for k in fields} for row in rows]
    if simplify(expected) != simplify(manifest["parts"]):
        errors.append("placement/config differs from print set")
    if supporting_sources(assembly, expected) != manifest.get("source_hashes"):
        errors.append("CAD/config sources changed; rebuild parts then sync")
    for entry in manifest["parts"]:
        src = within(ROOT / entry["source"])
        if not src.is_file() or digest(src) != entry["source_sha256"]:
            errors.append("source changed/missing: " + entry["source"])
        target = within(dest / entry["file"], dest)
        if not target.is_file() or digest(target) != entry["sha256"]:
            errors.append("copy changed/missing: " + entry["file"])
    if config.get("modifiers", []) != [{k: m[k] for k in ("host", "source")} for m in manifest.get("modifiers", [])]:
        errors.append("modifier configuration changed")
    for modifier in manifest.get("modifiers", []):
        src = within(ROOT / modifier["source"])
        target = within(dest / modifier["file"], dest)
        if not src.is_file() or digest(src) != modifier["source_sha256"]:
            errors.append("modifier source changed: " + modifier["source"])
        if not target.is_file() or digest(target) != modifier["sha256"]:
            errors.append("modifier copy changed: " + modifier["file"])
    for name, sha in manifest.get("document_hashes", {}).items():
        target = within(dest / name, dest)
        if not target.is_file() or digest(target) != sha:
            errors.append("generated document changed: " + name)
    expected_files = set(manifest.get("generated_files", [])) | {"manifest.json"}
    unknown = [p.relative_to(dest).as_posix() for p in dest.rglob("*") if p.is_file() and p.relative_to(dest).as_posix() not in expected_files]
    if unknown:
        errors.append("unmanaged print files: " + ", ".join(unknown))
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("sync", "check"))
    parser.add_argument("assemblies", nargs="*", help="assembly names or folders; default all")
    args = parser.parse_args()
    targets = [within(ROOT / "assemblies" / Path(a.replace('\\', '/')).name) for a in args.assemblies] if args.assemblies else sorted(p for p in (ROOT / "assemblies").iterdir() if p.is_dir() and p.name != "_work")
    failed = 0
    for assembly in targets:
        try:
            if not assembly.is_dir():
                raise ValueError(f"assembly not found: {assembly.name}")
            if args.command == "sync":
                kinds, count = build(assembly)
                print(f"SYNC {assembly.name}: {kinds} STL, {count} pieces")
            else:
                errors = check(assembly)
                if errors:
                    raise ValueError("; ".join(errors))
                print(f"PASS {assembly.name}")
        except (ValueError, OSError, KeyError) as error:
            failed += 1
            print(f"FAIL {assembly.name}: {error}")
    if args.command == "sync" and not failed:
        update_index()
    raise SystemExit(1 if failed else 0)


def update_index():
    """Keep the human-facing assembly and print-set entry points together."""
    descriptions = {
        "child_assembly": "子機・横置き旧構成", "child_frame2_assembly": "子機・旧フレーム2",
        "child_interior": "子機内装・200 mm・PLA Matte根元補強", "child_vertical_assembly": "子機・縦置き全体（内装を共有）",
        "child_simple_assembly": "子機・シンプル筐体", "child_simple_light_mount": "子機・シンプル筐体＋ライト",
        "child_petg100_design": "子機・PETG100%の試作6部品", "child_single_camera_topopt": "子機・単眼topopt探索記録",
        "child_clamp_suspension": "子機・3段連結M3/PETGクランプと吊り穴（試作）",
        "child_exterior_concept": "子機外装・Blenderイメージ（寸法未確定）",
        "child_exterior_horizontal": "子機外装・横置きクランプ穴固定（試作）",
        "child_horizontal_plate_frame": "子機・横置き4枚フレーム（X1C PETG嵌合試作）",
        "child_exterior_structure": "子機・フレームA（試作）",
        "parent_hand_service": "親機・電源操作対応内装", "parent_service_review": "親機・操作空間の内装レビュー",
        "parent_integrated": "親機・内外装統合", "parent_interior_p1": "親機・P1内装", "parent_interior_p2": "親機・P2内装",
        "parent_oneplate": "親機外装・小型1プレート版", "parent_assembly": "親機・従来全体",
        "parent_spar_concept": "親機・旧縦長外装の配置検討", "tether_open_reel": "テザーリール・開放状態",
        "tether_open_reel_closed": "テザーリール・カバー装着状態",
    }
    rows = ["# assemblyと印刷一式\n", "全体モデル・組立説明と、その構成の印刷用partsを同じフォルダにまとめています。`parts/` 内のSTLを、PRINT.mdの個数だけ印刷します。各構成の試作・未検証事項は説明を確認してください。\n", "子機内装は [child_interior](child_interior/README.md)、親機の現行内装は [parent_hand_service](parent_hand_service/README.md)。全体表示は [child_vertical_assembly](child_vertical_assembly/README.md) と [parent_integrated](parent_integrated/README.md) を参照できます。構成ごとに部品の組合せが異なります。\n", "| 構成・説明 | 全体／確認モデル | 印刷一式 | STL種類 / 個数 |", "|---|---|---|---|"]
    for assembly in sorted((ROOT / "assemblies").iterdir()):
        if not assembly.is_dir() or assembly.name == "_work":
            continue
        manifest = assembly / "parts/manifest.json"
        if not manifest.exists():
            continue
        data = read(manifest)
        models = []
        preferred = [assembly.name + ".step", "closed.step", assembly.name + "_structure.step", assembly.name + ".stl", assembly.name + ".blend", assembly.name + "_view.scad", assembly.name + ".scad", "topology_result.scad"]
        for name in preferred:
            if (assembly / name).exists():
                models.append(f"[{name}]({assembly.name}/{name})")
                if len(models) == 1:
                    break
        label = descriptions.get(assembly.name, assembly.name)
        count = sum(e["quantity"] for e in data["parts"])
        state = "探索のみ" if data["release_status"] == "exploration_only" else f"{len(data['parts'])} / {count}"
        rows.append(f"| [{label}]({assembly.name}/README.md) | {' '.join(models) or '説明内のビュー'} | [parts/PRINT.md]({assembly.name}/parts/PRINT.md) | {state} |")
    rows.append("\n印刷セットの原本は共通の `../parts/` 等にあります。設計のコピーは増やさず、STLだけを同期しています。基板・購入品・金属部品・フォーム・配線モデルは印刷セットから除外しています。")
    (ROOT / "assemblies/README.md").write_text("\n".join(rows) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
