#!/usr/bin/env python3
"""Provider adapters for normalized merged change-request history."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode, urlparse
from urllib.request import Request, urlopen

def load_local_environment() -> None:
    """Load simple KEY=value entries without overriding exported variables."""
    script_path = Path(__file__).resolve()
    candidates = [Path.cwd() / ".env", *(parent / ".env" for parent in script_path.parents)]
    git_root = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=False,
    )
    if git_root.returncode == 0 and git_root.stdout.strip():
        candidates.insert(0, Path(git_root.stdout.strip()) / ".env")
    for path in candidates:
        if not path.is_file():
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value
        return


load_local_environment()


@dataclass(frozen=True)
class ProviderRepository:
    provider: str
    namespace: str
    name: str


class ProviderError(RuntimeError):
    """Raised when a provider cannot be detected or queried."""


def _github_identity(url: str) -> tuple[str, str, str] | None:
    parts = urlparse(url).path.strip("/").split("/")
    if len(parts) >= 4 and parts[2] == "pull" and parts[3].isdigit():
        return parts[0], parts[1], parts[3]
    return None


def _gitlab_identity(url: str) -> tuple[str, str, str] | None:
    parsed = urlparse(url)
    parts = [part for part in parsed.path.strip("/").split("/") if part]
    if "-" in parts and "merge_requests" in parts and parts[-1].isdigit():
        marker = parts.index("-")
        project_path = "/".join(parts[:marker])
        return project_path, project_path, parts[-1]
    return None


def detect_provider(remote: str) -> ProviderRepository | None:
    parsed = urlparse(remote if "://" in remote else f"ssh://{remote.replace(':', '/', 1)}")
    host = parsed.hostname or ""
    path = parsed.path.strip("/")
    if path.endswith(".git"):
        path = path[:-4]
    parts = [part for part in path.split("/") if part]
    if host == "github.com" and len(parts) >= 2:
        return ProviderRepository("github", parts[0], parts[1])
    if "gitlab" in host and len(parts) >= 2:
        return ProviderRepository("gitlab", "/".join(parts[:-1]), parts[-1])
    return None


def _get_json(url: str, provider: str) -> object:
    headers = {"Accept": "application/json", "User-Agent": "pr-code-review"}
    token_name = "GITHUB_TOKEN" if provider == "github" else "GITLAB_TOKEN"
    token = os.environ.get(token_name) or os.environ.get("VCS_TOKEN")

    print(f"Fetching JSON from URL: {url} with provider: {provider}, token available: {token is not None}", file=sys.stderr)
    if token:
        headers["Authorization"] = f"Bearer {token}"
        if provider == "gitlab":
            headers["PRIVATE-TOKEN"] = token
    try:
        with urlopen(Request(url, headers=headers), timeout=20) as response:
            return json.load(response)
    except HTTPError as error:
        if error.code in {401, 403}:
            print(f"{provider} rejected the request with HTTP {error.code}", file=sys.stderr)
            raise ProviderError(f"{provider} rejected the request; set {token_name} or VCS_TOKEN") from error
        if error.code == 404:
            print(f"{provider} repository or change-request data not found (HTTP 404)", file=sys.stderr)
            raise ProviderError(f"{provider} repository or change-request data was not found or is not accessible") from error
        raise ProviderError(f"{provider} API request failed with HTTP {error.code}") from error
    except URLError as error:
        print(f"Failed to reach {provider}: {error.reason}", file=sys.stderr)
        raise ProviderError(f"unable to reach {provider}: {error.reason}") from error
    except json.JSONDecodeError as error:
        raise ProviderError(f"{provider} returned invalid JSON") from error


def _github_requests(repository: ProviderRepository, base_ref: str, limit: int) -> list[dict]:
    requests = []
    page = 1
    while len(requests) < limit:
        query = urlencode({"state": "closed", "base": base_ref, "per_page": min(100, limit), "page": page})
        pulls = _get_json(f"https://api.github.com/repos/{repository.namespace}/{repository.name}/pulls?{query}", "github")
        if not isinstance(pulls, list) or not pulls:
            break
        for pull in pulls:
            if not isinstance(pull, dict) or not pull.get("merged_at"):
                continue

            number = pull.get("number")
            if number is None:
                continue
            root = f"https://api.github.com/repos/{repository.namespace}/{repository.name}"
            comments = _get_json(f"{root}/pulls/{number}/comments", "github")
            reviews = _get_json(f"{root}/pulls/{number}/reviews", "github")
            discussion = _get_json(f"{root}/issues/{number}/comments", "github")
            requests.append({
                "id": str(number), "provider": "github", "base_ref": pull.get("base", {}).get("ref", base_ref),
                "source_ref": pull.get("head", {}).get("ref", ""), "merged": True,
                "title": pull.get("title", ""), "description": pull.get("body") or "",
                "url": pull.get("html_url", ""), "comments": comments if isinstance(comments, list) else [],
                "reviews": reviews if isinstance(reviews, list) else [],
                "discussion_comments": discussion if isinstance(discussion, list) else [],
            })
            if len(requests) >= limit:
                break
        if len(pulls) < min(100, limit):
            break
        page += 1
    return requests


def _gitlab_requests(repository: ProviderRepository, base_ref: str, limit: int) -> list[dict]:
    project = quote(f"{repository.namespace}/{repository.name}", safe="")
    requests = []
    page = 1
    while len(requests) < limit:
        query = urlencode({"state": "merged", "target_branch": base_ref, "per_page": min(100, limit), "page": page})
        merge_requests = _get_json(f"https://gitlab.com/api/v4/projects/{project}/merge_requests?{query}", "gitlab")
        if not isinstance(merge_requests, list) or not merge_requests:
            break
        for merge_request in merge_requests:
            if not isinstance(merge_request, dict):
                continue
            iid = merge_request.get("iid")
            if iid is None:
                continue
            root = f"https://gitlab.com/api/v4/projects/{project}/merge_requests/{iid}"
            notes = _get_json(f"{root}/notes?per_page=100", "gitlab")
            requests.append({
                "id": str(iid), "provider": "gitlab", "base_ref": merge_request.get("target_branch", base_ref),
                "source_ref": merge_request.get("source_branch", ""), "merged": True,
                "title": merge_request.get("title", ""), "description": merge_request.get("description") or "",
                "url": merge_request.get("web_url", ""), "comments": notes if isinstance(notes, list) else [],
                "reviews": [], "discussion_comments": [],
            })
            if len(requests) >= limit:
                break
        if len(merge_requests) < min(100, limit):
            break
        page += 1
    return requests


def fetch_change_request(remote: str, url: str) -> dict:
    """Fetch one PR/MR and all evidence needed for current acceptance analysis."""
    repository = detect_provider(remote)
    if repository is None:
        raise ProviderError("unsupported VCS provider; add an adapter for this remote host")
    if repository.provider == "github":
        identity = _github_identity(url)
        if identity is None:
            raise ProviderError("invalid GitHub pull-request URL")
        owner, name, number = identity
        root = f"https://api.github.com/repos/{owner}/{name}"
        pull = _get_json(f"{root}/pulls/{number}", "github")
        commits = _get_json(f"{root}/pulls/{number}/commits?per_page=100", "github")
        files = _get_json(f"{root}/pulls/{number}/files?per_page=100", "github")
        comments = _get_json(f"{root}/pulls/{number}/comments?per_page=100", "github")
        reviews = _get_json(f"{root}/pulls/{number}/reviews?per_page=100", "github")
        discussion = _get_json(f"{root.replace('/repos/', '/repos/')}/issues/{number}/comments?per_page=100", "github")
        return {
            "provider": "github", "id": number, "url": url,
            "base_ref": pull["base"]["ref"], "source_ref": pull["head"]["ref"],
            "base_sha": pull["base"]["sha"], "source_sha": pull["head"]["sha"],
            "merged": pull.get("merged_at") is not None, "title": pull.get("title", ""),
            "description": pull.get("body") or "", "comments": comments if isinstance(comments, list) else [],
            "reviews": reviews if isinstance(reviews, list) else [],
            "discussion_comments": discussion if isinstance(discussion, list) else [],
            "commits": commits if isinstance(commits, list) else [],
            "changed_files": files if isinstance(files, list) else [],
        }
    if repository.provider == "gitlab":
        identity = _gitlab_identity(url)
        if identity is None:
            raise ProviderError("invalid GitLab merge-request URL")
        project_path, _, iid = identity
        project = quote(project_path, safe="")
        root = f"https://gitlab.com/api/v4/projects/{project}/merge_requests/{iid}"
        merge_request = _get_json(root, "gitlab")
        notes = _get_json(f"{root}/notes?per_page=100", "gitlab")
        commits = _get_json(f"{root}/commits?per_page=100", "gitlab")
        changes = _get_json(f"{root}/changes", "gitlab")
        return {
            "provider": "gitlab", "id": iid, "url": url,
            "base_ref": merge_request["target_branch"], "source_ref": merge_request["source_branch"],
            "base_sha": merge_request.get("diff_refs", {}).get("base_sha", ""),
            "source_sha": merge_request.get("sha", ""), "merged": merge_request.get("state") == "merged",
            "title": merge_request.get("title", ""), "description": merge_request.get("description") or "",
            "comments": notes if isinstance(notes, list) else [], "reviews": [], "discussion_comments": [],
            "commits": commits if isinstance(commits, list) else [],
            "changed_files": changes.get("changes", []) if isinstance(changes, dict) else [],
        }
    raise ProviderError(f"no adapter registered for provider {repository.provider}")


def fetch_merged_change_requests(remote: str, base_ref: str, limit: int) -> dict:
    repository = detect_provider(remote)
    if repository is None:
        raise ProviderError("unsupported VCS provider; add an adapter for this remote host")
    if repository.provider == "github":
        print(f"Fetching GitHub requests for repository: {repository.namespace}/{repository.name}, base_ref: {base_ref}, limit: {limit}", file=sys.stderr)
        requests = _github_requests(repository, base_ref, limit)
    elif repository.provider == "gitlab":
        print(f"Fetching GitLab requests for repository: {repository.namespace}/{repository.name}, base_ref: {base_ref}, limit: {limit}", file=sys.stderr)
        requests = _gitlab_requests(repository, base_ref, limit)
    else:
        raise ProviderError(f"no adapter registered for provider {repository.provider}")
    return {"provider": repository.provider, "repository": f"{repository.namespace}/{repository.name}", "change_requests": requests}
