#!/usr/bin/env python3
"""Run native compiler probes; a failed probe always fails this command.

This records evidence only. It never compiles, rewrites, or interprets Transit
source, and a successful build is not reported as runtime qualification.
"""

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run_probe(entry, root=ROOT):
    command = [
        "transit", "build", "-f", str(entry.relative_to(root)),
        "--check", "--format", "json", "--color", "off",
    ]
    record = {
        "entry": str(entry.relative_to(root)),
        "sources": {
            str(source.relative_to(entry.parent)): hashlib.sha256(source.read_bytes()).hexdigest()
            for source in sorted(entry.parent.rglob("*.transit"))
            if ".transit" not in source.relative_to(entry.parent).parts
        },
        "command": command,
        "runtime_tests": "not_run",
        "provider_verification": "not_run",
    }
    try:
        result = subprocess.run(command, cwd=root, capture_output=True, text=True, timeout=60)
        record.update(
            status="compiled" if result.returncode == 0 else "build_failed",
            exit_code=result.returncode, stdout=result.stdout, stderr=result.stderr,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        record.update(status="tool_failed", exit_code=None, stdout="", stderr=str(error))
    return record


def collect(entries, root=ROOT):
    records = [run_probe(entry, root) for entry in entries]
    return records, 0 if records and all(r["status"] == "compiled" for r in records) else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / ".transit/reports/compiler-probes.json")
    args = parser.parse_args()
    lock = json.loads((ROOT / "flake.lock").read_text())
    entries = sorted((ROOT / "tests/compiler").glob("*/build.transit"))
    records, status = collect(entries)
    report = {
        "schema_version": 1,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "executable": shutil.which("transit"),
        "declared_pins": {
            name: lock["nodes"][name]["locked"]["rev"]
            for name in ("transit-upstream", "transitc-upstream")
        },
        "recommended_invocation": "nix develop --no-update-lock-file -c python3 tooling/probe.py",
        "scope": "Compiler acceptance only; no installation, recovery, or provider tests.",
        "probes": records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    for record in records:
        print(f"{record['status'].upper()}: {record['entry']}")
    print(f"Report: {args.output}")
    print("No integration is qualified by these probes.")
    return status


if __name__ == "__main__":
    sys.exit(main())
