#!/usr/bin/env python3
"""Provider adapters for normalized merged change-request history."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode, urlparse
from urllib.request import Request, urlopen

from dotenv import load_dotenv
load_dotenv()


@dataclass(frozen=True)
class ProviderRepository:
    provider: str
    namespace: str
    name: str


class ProviderError(RuntimeError):
    """Raised when a provider cannot be detected or queried."""


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

    print(f"Fetching JSON from URL: {url} with provider: {provider}, token available: {token is not None}")
    if token:
        headers["Authorization"] = f"Bearer {token}"
        if provider == "gitlab":
            headers["PRIVATE-TOKEN"] = token
    try:
        with urlopen(Request(url, headers=headers), timeout=20) as response:
            return json.load(response)
    except HTTPError as error:
        if error.code in {401, 403}:
            print(f"{provider} rejected the request with HTTP {error.code}")
            raise ProviderError(f"{provider} rejected the request; set {token_name} or VCS_TOKEN") from error
        if error.code == 404:
            print(f"{provider} repository or change-request data not found (HTTP 404)")
            raise ProviderError(f"{provider} repository or change-request data was not found or is not accessible") from error
        raise ProviderError(f"{provider} API request failed with HTTP {error.code}") from error
    except URLError as error:
        print(f"Failed to reach {provider}: {error.reason}")
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


def fetch_merged_change_requests(remote: str, base_ref: str, limit: int) -> dict:
    repository = detect_provider(remote)
    if repository is None:
        raise ProviderError("unsupported VCS provider; add an adapter for this remote host")
    if repository.provider == "github":
        print(f"Fetching GitHub requests for repository: {repository.namespace}/{repository.name}, base_ref: {base_ref}, limit: {limit}")
        requests = _github_requests(repository, base_ref, limit)
    elif repository.provider == "gitlab":
        print(f"Fetching GitLab requests for repository: {repository.namespace}/{repository.name}, base_ref: {base_ref}, limit: {limit}")
        requests = _gitlab_requests(repository, base_ref, limit)
    else:
        raise ProviderError(f"no adapter registered for provider {repository.provider}")
    return {"provider": repository.provider, "repository": f"{repository.namespace}/{repository.name}", "change_requests": requests}
