#!/usr/bin/env python3
"""Select merged change requests from provider-supplied JSON without API logic."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from pathlib import Path


GITHUB_REMOTE = re.compile(r"(?:github\.com[/:])([^/ :]+)/([^/]+?)(?:\.git)?$")


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


def github_repository(root: Path) -> tuple[str, str] | None:
    match = GITHUB_REMOTE.search(remote_url(root))
    return match.groups() if match else None


def github_get(url: str) -> object:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "pr-code-review"}
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        with urlopen(Request(url, headers=headers), timeout=20) as response:
            return json.load(response)
    except HTTPError as error:
        if error.code in {401, 403}:
            raise OSError("GitHub rejected the request; set GITHUB_TOKEN or GH_TOKEN") from error
        raise OSError(f"GitHub API request failed with HTTP {error.code}") from error
    except URLError as error:
        raise OSError(f"unable to reach GitHub: {error.reason}") from error
    except json.JSONDecodeError as error:
        raise OSError(f"GitHub returned invalid JSON for {url}") from error


def fetch_github_change_requests(root: Path, base_ref: str, limit: int) -> dict:
    repository = github_repository(root)
    if not repository:
        raise OSError("origin remote is not a GitHub repository")
    owner, name = repository
    requests = []
    page = 1
    while len(requests) < limit:
        query = urlencode({"state": "closed", "base": base_ref, "per_page": min(100, limit), "page": page})
        pulls = github_get(f"https://api.github.com/repos/{owner}/{name}/pulls?{query}")
        if not isinstance(pulls, list) or not pulls:
            break
        for pull in pulls:
            if not isinstance(pull, dict) or not pull.get("merged_at"):
                continue
            number = pull.get("number")
            if number is None:
                continue
            comments = github_get(f"https://api.github.com/repos/{owner}/{name}/pulls/{number}/comments")
            reviews = github_get(f"https://api.github.com/repos/{owner}/{name}/pulls/{number}/reviews")
            discussion = github_get(f"https://api.github.com/repos/{owner}/{name}/issues/{number}/comments")
            requests.append(
                {
                    "id": str(number),
                    "provider": "github",
                    "base_ref": pull.get("base", {}).get("ref", base_ref),
                    "source_ref": pull.get("head", {}).get("ref", ""),
                    "merged": True,
                    "title": pull.get("title", ""),
                    "description": pull.get("body") or "",
                    "url": pull.get("html_url", ""),
                    "comments": comments if isinstance(comments, list) else [],
                    "reviews": reviews if isinstance(reviews, list) else [],
                    "discussion_comments": discussion if isinstance(discussion, list) else [],
                }
            )
            if len(requests) >= limit:
                break
        if len(pulls) < min(100, limit):
            break
        page += 1
    return {"change_requests": requests, "provider": "github", "repository": f"{owner}/{name}"}


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
            payload = fetch_github_change_requests(root, args.base, args.limit) if github_repository(root) else {}
            provider_available = bool(payload)
        analyzed = set()
        if state.get("base_ref") in {"", args.base}:
            analyzed = {str(value) for value in state.get("analyzed_change_requests", [])}
        result = discover(payload, args.base, analyzed, args.limit)
        result["provider_data_available"] = provider_available
        result["provider"] = payload.get("provider", "unknown")
        if not result["provider_data_available"]:
            result["note"] = f"No provider input found at {input_path}, and no supported provider was detected; no historical change requests were selected."
    except (OSError, json.JSONDecodeError) as error:
        print(f"Historical discovery failed: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())