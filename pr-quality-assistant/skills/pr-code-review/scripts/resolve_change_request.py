#!/usr/bin/env python3
"""Resolve a supported PR/MR URL into normalized change-request metadata."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


GITHUB_PATTERN = re.compile(r"^https?://github\.com/([^/]+)/([^/]+)/pull/(\d+)(?:/.*)?$")


class ChangeRequestError(RuntimeError):
    """Raised when a change-request URL cannot be resolved."""


def resolve_github(url: str, match: re.Match[str]) -> dict:
    owner, repository, number = match.groups()
    api_url = f"https://api.github.com/repos/{owner}/{repository}/pulls/{number}"
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "pr-code-review"}
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(api_url, headers=headers)
    try:
        with urlopen(request, timeout=15) as response:
            payload = json.load(response)
    except HTTPError as error:
        if error.code in {401, 403}:
            raise ChangeRequestError("GitHub rejected the request; set GITHUB_TOKEN for private or rate-limited repositories") from error
        if error.code == 404:
            raise ChangeRequestError("GitHub PR was not found or is not accessible") from error
        raise ChangeRequestError(f"GitHub API request failed with HTTP {error.code}") from error
    except URLError as error:
        raise ChangeRequestError(f"unable to reach GitHub: {error.reason}") from error
    try:
        return {
            "provider": "github",
            "id": str(payload["number"]),
            "url": url,
            "base_ref": payload["base"]["ref"],
            "source_ref": payload["head"]["ref"],
            "base_sha": payload["base"]["sha"],
            "source_sha": payload["head"]["sha"],
            "title": payload.get("title", ""),
            "description": payload.get("body") or "",
            "merged": payload.get("merged_at") is not None,
        }
    except (KeyError, TypeError) as error:
        raise ChangeRequestError("GitHub response is missing required PR metadata") from error


def resolve(url: str) -> dict:
    match = GITHUB_PATTERN.match(url)
    if match:
        return resolve_github(url, match)
    raise ChangeRequestError("unsupported PR/MR URL; currently supported provider: GitHub")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        metadata = resolve(args.url)
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