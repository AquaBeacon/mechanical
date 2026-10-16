"""Register this FreeCAD stdio server for future Codex sessions, preserving settings."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import tempfile
import tomllib

from cli import ROOT


def register(dry_run=False):
    here = Path(__file__).resolve().parent
    python = here / ".venv/Scripts/python.exe"
    if os.name != "nt":
        python = here / ".venv/bin/python"
    if not python.is_file():
        raise RuntimeError("Create the local .venv and install requirements.txt before registering")
    config = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))) / "config.toml"
    before = config.read_bytes() if config.exists() else b""
    parsed = tomllib.loads(before.decode("utf-8-sig"))
    settings = {"command": str(python), "args": ["-X", "utf8", str(here / "mcp_server.py"), "--workspace", str(ROOT)],
                "startup_timeout_sec": 30, "tool_timeout_sec": 300, "enabled": True}
    existing = parsed.get("mcp_servers", {}).get("freecad")
    if existing is not None:
        if all(existing.get(key) == value for key, value in settings.items()):
            return {"status": "already_registered", "config": str(config), "settings": settings}
        raise RuntimeError("A different freecad MCP registration already exists; inspect it before replacing")
    block = "\n\n# Body_Models FreeCAD foundation\n[mcp_servers.freecad]\n" + "\n".join(
        key + " = " + json.dumps(value, ensure_ascii=False) for key, value in settings.items()) + "\n"
    text = before.decode("utf-8-sig") + block
    verified = tomllib.loads(text)
    without_new = dict(verified)
    without_new["mcp_servers"] = dict(verified["mcp_servers"])
    del without_new["mcp_servers"]["freecad"]
    if "mcp_servers" not in parsed:
        del without_new["mcp_servers"]
    if without_new != parsed:
        raise RuntimeError("unrelated configuration would change")
    if dry_run:
        return {"status": "dry_run", "config": str(config), "settings": settings}
    config.parent.mkdir(parents=True, exist_ok=True)
    backup_dir = config.parent / "backups/cad-foundation"
    backup_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    backup = backup_dir / ("config-" + stamp + ".toml")
    backup.write_bytes(before)
    descriptor, temporary = tempfile.mkstemp(prefix="freecad-config-", suffix=".toml", dir=config.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(text)
        current = config.read_bytes() if config.exists() else b""
        if current != before:
            raise RuntimeError("Codex settings changed concurrently; registration was not applied")
        os.replace(temporary, config)
    finally:
        if Path(temporary).exists():
            Path(temporary).unlink()
    return {"status": "registered", "config": str(config), "backup": str(backup), "settings": settings}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    print(json.dumps(register(parser.parse_args().dry_run), ensure_ascii=False, indent=2))
