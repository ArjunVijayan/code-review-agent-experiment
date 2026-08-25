#!/usr/bin/env python3
"""Read or atomically update analyzed change-request state after successful generation."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--successful-ids", nargs="*", default=[])
    parser.add_argument("--mark-success", action="store_true", help="Required to persist state")
    args = parser.parse_args()
    try:
        current = json.loads(args.state.read_text(encoding="utf-8")) if args.state.exists() else {}
        analyzed = set()
        if current.get("base_ref") in {None, "", args.base}:
            analyzed = {str(value) for value in current.get("analyzed_change_requests", [])}
        requested = {str(value) for value in args.successful_ids if str(value)}
        result = {
            "base_ref": args.base,
            "last_analyzed_at": current.get("last_analyzed_at", ""),
            "analyzed_change_requests": sorted(analyzed),
        }
        if args.mark_success:
            result["analyzed_change_requests"] = sorted(analyzed | requested)
            result["last_analyzed_at"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
            args.state.parent.mkdir(parents=True, exist_ok=True)
            temporary = args.state.with_suffix(args.state.suffix + ".tmp")
            temporary.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
            temporary.replace(args.state)
    except (OSError, json.JSONDecodeError) as error:
        print(f"Insights state update failed: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())