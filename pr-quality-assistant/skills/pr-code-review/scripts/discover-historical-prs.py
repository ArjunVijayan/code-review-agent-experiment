#!/usr/bin/env python3
"""Select merged change requests from provider-supplied JSON without API logic."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from provider_adapters import ProviderError, detect_provider, fetch_merged_change_requests


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


def remote_url(root: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), "remote", "get-url", "origin"],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else ""


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
        state_text = state_path.read_text(encoding="utf-8").strip() if state_path.is_file() else ""
        state = json.loads(state_text) if state_text else {}
        input_text = input_path.read_text(encoding="utf-8").strip() if input_path.is_file() else ""
        if input_text:
            payload = json.loads(input_text)
            provider_available = True
        else:
            remote = remote_url(root)
            provider = detect_provider(remote) if remote else None

            print(f"Detected provider: {provider}")
            print(f"Remote URL: {remote}")

            if provider is None:
                payload = {}
                provider_available = False
            else:
                payload = fetch_merged_change_requests(remote, args.base, args.limit)
                provider_available = True
        analyzed = set()
        if state.get("base_ref") in {"", args.base}:
            analyzed = {str(value) for value in state.get("analyzed_change_requests", [])}
        result = discover(payload, args.base, analyzed, args.limit)
        result["provider_data_available"] = provider_available
        result["provider"] = payload.get("provider", "unknown")
        if not result["provider_data_available"]:
            result["note"] = f"No provider input found at {input_path}, and no supported provider was detected; no historical change requests were selected."
    except (OSError, ProviderError, json.JSONDecodeError) as error:
        print(f"Historical discovery failed: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())