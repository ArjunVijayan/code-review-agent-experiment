#!/usr/bin/env python3
"""Resolve a supported PR/MR URL into normalized change-request metadata."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from provider_adapters import ProviderError, fetch_change_request


class ChangeRequestError(RuntimeError):
    """Raised when a change-request URL cannot be resolved."""


def resolve(url: str, remote: str) -> dict:
    try:
        return fetch_change_request(remote, url)
    except ProviderError as error:
        raise ChangeRequestError(str(error)) from error


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url")
    parser.add_argument("--remote", default="")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        metadata = resolve(args.url, args.remote)
    except ChangeRequestError as error:
        print(f"Change-request resolution failed: {error}", file=sys.stderr)
        return 1
    rendered = json.dumps(metadata, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())