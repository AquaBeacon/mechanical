"""Read-only Windows USB/COM inventory for GNSS commissioning; no device writes."""
from __future__ import annotations

import argparse
import csv
import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from serial.tools import list_ports

ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ROOT / "parts/parent/interior/cots/sparkfun_neo_f9p/_work/analysis/rtk_gnss_20261008"


def inventory():
    command = (
        "@(Get-PnpDevice -PresentOnly | Where-Object { "
        "$_.Class -in @('Ports','USB','USBDevice','Sensor') -or "
        "$_.FriendlyName -match 'u-blox|GNSS|Unknown' } | "
        "Select-Object Status,Class,FriendlyName,InstanceId) | ConvertTo-Json -Depth 3 -Compress"
    )
    result = subprocess.run(
        ["powershell.exe", "-NoProfile", "-Command",
         "[Console]::OutputEncoding=[System.Text.Encoding]::UTF8; " + command],
        capture_output=True, encoding="utf-8", errors="replace", timeout=30,
    )
    return {"utc": datetime.now(timezone.utc).isoformat(), "returncode": result.returncode,
            "devices": json.loads(result.stdout) if result.stdout.strip() else [],
            "stderr": result.stderr}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seconds", type=float, default=60)
    parser.add_argument("--interval", type=float, default=5)
    parser.add_argument("--output", type=Path, default=DEFAULT)
    args = parser.parse_args()
    if args.seconds < 0 or args.interval <= 0:
        parser.error("seconds must be >= 0 and interval > 0")
    # Each run has a unique directory; earlier evidence is preserved.
    folder = args.output / "01_basic" / "data" / datetime.now(timezone.utc).strftime("probe_%Y%m%dT%H%M%S_%fZ")
    folder.mkdir(parents=True, exist_ok=False)
    samples = []
    started = time.monotonic()
    with (folder / "ports.jsonl").open("w", encoding="utf-8") as raw:
        while True:
            ports = [{"device": p.device, "description": p.description, "hwid": p.hwid,
                      "vid": p.vid, "pid": p.pid} for p in list_ports.comports()]
            sample = {"utc": datetime.now(timezone.utc).isoformat(),
                      "elapsed_s": time.monotonic() - started, "port_count": len(ports), "ports": ports}
            raw.write(json.dumps(sample, ensure_ascii=False) + "\n")
            raw.flush()
            samples.append(sample)
            print(json.dumps(sample, ensure_ascii=False), flush=True)
            if time.monotonic() - started >= args.seconds:
                break
            time.sleep(min(args.interval, max(0, args.seconds - (time.monotonic() - started))))
    pnp = inventory()
    (folder / "windows_pnp.json").write_text(json.dumps(pnp, ensure_ascii=False, indent=2), encoding="utf-8")
    with (folder / "port_counts.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["utc", "elapsed_s", "port_count"])
        writer.writeheader()
        writer.writerows({k: row[k] for k in writer.fieldnames} for row in samples)
    fig, ax = plt.subplots(figsize=(8, 3.6), layout="constrained")
    ax.step([r["elapsed_s"] for r in samples], [r["port_count"] for r in samples], where="post", marker="o")
    ax.set(xlabel="Elapsed time (s)", ylabel="Detected COM ports (all devices)",
           title="Windows COM-port enumeration (not GNSS observation data)", ylim=(-0.1, max(1, max(r["port_count"] for r in samples)) + .2))
    ax.set_yticks(range(max(1, max(r["port_count"] for r in samples)) + 1))
    ax.grid(alpha=.25)
    fig.savefig(folder / "usb_port_detection.png", dpi=160)
    plt.close(fig)
    print("Saved:", folder, flush=True)


if __name__ == "__main__":
    main()
