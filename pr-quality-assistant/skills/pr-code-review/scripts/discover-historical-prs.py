#!/usr/bin/env python3
"""Select merged change requests from provider-supplied JSON without API logic."""

from __future__ import annotations

import argparse
import json
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--input", type=Path, required=True, help="Provider-neutral JSON input")
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit must be at least 1")
    try:
        state = json.loads(args.state.read_text(encoding="utf-8"))
        payload = json.loads(args.input.read_text(encoding="utf-8"))
        analyzed = set()
        if state.get("base_ref") in {"", args.base}:
            analyzed = {str(value) for value in state.get("analyzed_change_requests", [])}
        result = discover(payload, args.base, analyzed, args.limit)
    except (OSError, json.JSONDecodeError) as error:
        print(f"Historical discovery failed: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())