#!/usr/bin/env python3
"""Select merged change requests from provider-supplied JSON without API logic."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def discover(payload: dict, base_ref: str, analyzed: set[str], limit: int) -> dict:
    requests = []
    for item in payload.get("change_requests", []):
        identifier = str(item.get("id", ""))
        if not identifier or item.get("base_ref") != base_ref or item.get("merged") is not True:
            continue
        if identifier in analyzed:
            continue
        requests.append(item)
    return {"base_ref": base_ref, "change_requests": requests[:limit]}


def repository_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise OSError("current directory is not inside a Git repository")
    return Path(result.stdout.strip())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True)
    parser.add_argument("--state", type=Path, help="Path to the insights state JSON")
    parser.add_argument("--input", type=Path, help="Provider-neutral JSON input")
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit must be at least 1")
    try:
        root = repository_root()
        state_path = args.state or root / ".code-review" / "insights-state.json"
        input_path = args.input or root / "review" / "change-requests.json"
        state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.is_file() else {}
        payload = json.loads(input_path.read_text(encoding="utf-8")) if input_path.is_file() else {}
        analyzed = set()
        if state.get("base_ref") in {"", args.base}:
            analyzed = {str(value) for value in state.get("analyzed_change_requests", [])}
        result = discover(payload, args.base, analyzed, args.limit)
        result["provider_data_available"] = input_path.is_file()
        if not result["provider_data_available"]:
            result["note"] = f"No provider input found at {input_path}; no historical change requests were selected."
    except (OSError, json.JSONDecodeError) as error:
        print(f"Historical discovery failed: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())