#!/usr/bin/env python3
"""Render review-result.json as a self-contained HTML report."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from urllib.parse import quote


def render(result: dict) -> str:
    status = html.escape(result.get("status", "FAILED"))
    pull_request = result.get("pull_request", {})
    request_url = str(pull_request.get("url", ""))
    request_link = (
        f'<a href="{html.escape(request_url, quote=True)}">{html.escape(request_url)}</a>'
        if request_url.startswith(("https://", "http://"))
        else html.escape(request_url or "Not supplied")
    )
    gates = result.get("gates", {})
    findings = result.get("findings", [])
    blocking_findings = result.get("blocking_findings", [])

    def text(value: object, fallback: str = "Not supplied") -> str:
        return html.escape(str(value)) if value not in (None, "", []) else fallback

    def gate_score(gate: dict) -> str:
        if str(gate.get("status", "")).upper() == "UNAVAILABLE":
            return str(gate.get("unavailable_reason", "Required evidence unavailable"))
        if gate.get("score") is not None:
            return str(gate["score"])
        passed = gate.get("passed")
        total = sum(int(gate.get(key, 0)) for key in ("passed", "failed", "uncertain"))
        if passed is not None and total:
            return f"{passed}/{total}"
        return "Not measured"

    gate_rows = "".join(
        f"<tr id=\"gate-{html.escape(name)}\"><td>{html.escape(name.replace('_', ' ').title())}</td><td class=\"status-cell status-{html.escape(str(gate.get('status', 'UNAVAILABLE')).lower())}\">{text(gate.get('status', 'UNAVAILABLE'))}</td><td>{text(gate_score(gate))}</td><td>{text(gate.get('unavailable_reason', gate.get('summary', '')))}</td></tr>"
        for name, gate in gates.items()
    )

    def reference_cell(item: dict) -> str:
        reference = str(item.get("reference", ""))
        if not reference:
            return "Not supplied"
        if reference.startswith(("https://", "http://")):
            href = reference
        elif reference.startswith("review/"):
            href = "../" + quote(reference, safe="/._-#")
        else:
            href = "../" + quote(reference, safe="/._-#")
        return f'<a href="{html.escape(href, quote=True)}">{html.escape(reference)}</a>'

    def issue_row(item: dict) -> str:
        gates_text = ", ".join(item.get("gates", [item.get("gate", "")]))
        issue_id = item.get("id", item.get("fingerprint", "issue"))
        return (
            f"<tr id=\"finding-{html.escape(str(issue_id))}\"><td><a href=\"#finding-{html.escape(str(issue_id))}\">{text(issue_id)}</a></td>"
            f"<td>{text(item.get('severity', 'INFO'))}</td>"
            f"<td>{text(item.get('gate', gates_text))}</td>"
            f"<td>{text(item.get('issue'))}</td>"
            f"<td>{text(item.get('impact'))}<br><strong>Evidence:</strong> {text(item.get('evidence'))}</td>"
            f"<td>{text(item.get('recommendation'))}</td>"
            f"<td>{reference_cell(item)}</td></tr>"
        )

    issues = "".join(
        issue_row(item) for item in result.get("findings", [])
    ) or '<tr><td colspan="7">No issues reported.</td></tr>'

    recommendations = "".join(
        f"<li><strong>{text(item.get('priority', 'ACTION'))}</strong>: {text(item.get('description', item.get('recommendation', '')))} {reference_cell(item)}</li>"
        for item in result.get("recommendations", [])
        if isinstance(item, dict)
    ) or "<li>No recommendations supplied.</li>"

    evidence_links = "".join(
        f'<li><a href="../{path}">{path}</a></li>'
        for path in (
            "review/review-context.md",
            "review/acceptance-criteria.md",
            "review/code-coverage-report.md",
            "pr-insights.json",
            ".github/instructions/insights.instructions.md",
        )
    )

    metrics = result.get("metrics", {})
    metric_rows = "".join(
        f"<tr><td>{html.escape(str(key).replace('_', ' ').title())}</td><td>{text(value)}</td></tr>"
        for key, value in metrics.items()
    ) or "<tr><td colspan=\"2\">No additional metrics supplied.</td></tr>"

    change_summary = result.get("change_summary", [])
    summary_rows = "".join(
        f"<tr><td>{text(item.get('requirement'))}</td><td>{text(', '.join(item.get('files', [])))}</td><td>{text(item.get('behavior'))}</td><td>{text(', '.join(item.get('tests', [])))}</td></tr>"
        for item in change_summary if isinstance(item, dict)
    ) or "<tr><td colspan=\"4\">No change summary supplied.</td></tr>"

    primary_reason = (
        f"{len(blocking_findings)} blocking issue(s) require resolution."
        if blocking_findings
        else "No blocking findings were supplied; gate status determines readiness."
    )
    toc = "".join(
        f'<li><a href="#{anchor}">{label}</a></li>'
        for anchor, label in (("gates", "Quality Gates"), ("evidence", "Evidence Packages"), ("issues", "Issues and Evidence"), ("recommendations", "Recommended Changes"))
    )

    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>PR Merge Readiness</title>
<style>body{{font:16px system-ui,sans-serif;max-width:1180px;margin:2rem auto;padding:0 1rem;color:#202124;line-height:1.45}}h1{{border-bottom:2px solid #202124;padding-bottom:.5rem}}h2{{margin-top:2rem}}table{{border-collapse:collapse;width:100%;margin:1rem 0}}th,td{{border:1px solid #c8c8c8;padding:.6rem;text-align:left;vertical-align:top}}th{{background:#f2f2f2}}.status{{font-size:1.4rem;font-weight:700}}.APPROVED,.status-pass{{color:#176b36}}.FAILED,.status-fail,.status-unavailable,.status-uncertain{{color:#a12622}}.status-cell{{font-weight:700}}.meta{{background:#f7f7f7;padding:1rem;border-left:4px solid #666}}.summary{{background:#fff8e1;border:1px solid #e0c36e;padding:1rem}}li{{margin:.45rem 0}}a{{color:#0645ad}}.muted{{color:#666}}</style></head>
<body><h1>PR Merge Readiness</h1><div class="meta"><p>PR/MR: {request_link}</p><p>Base: {text(pull_request.get('base'))} | Source: {text(pull_request.get('source'))}</p><p class="status {status}">FINAL DECISION: {status}</p><p class="summary"><strong>What this means:</strong> {html.escape(primary_reason)}<br><strong>Issues:</strong> {len(findings)} total, {len(blocking_findings)} blocking, {len(findings) - len(blocking_findings)} non-blocking.</p></div>
<nav aria-label="Table of contents"><strong>Review navigation</strong><ul>{toc}</ul></nav>
<h2 id="gates">Quality Gates</h2><table><thead><tr><th>Gate</th><th>Status</th><th>Score / Ratio</th><th>Evidence or unavailable reason</th></tr></thead><tbody>{gate_rows}</tbody></table>
<h2 id="evidence">Review Evidence</h2><p class="muted">Open these artifacts to verify the decision, requirement coverage, tests, and historical guidance.</p><ul>{evidence_links}</ul>
<h2>Change Summary</h2><table><thead><tr><th>Requirement</th><th>Files</th><th>Observable behavior</th><th>Tests</th></tr></thead><tbody>{summary_rows}</tbody></table>
<h2>Metrics</h2><table><thead><tr><th>Metric</th><th>Value</th></tr></thead><tbody>{metric_rows}</tbody></table>
<h2 id="issues">Issues and Evidence</h2><p class="muted">Each issue connects its gate to impact, evidence, remediation, and a source reference.</p><table><thead><tr><th>ID</th><th>Severity</th><th>Gate(s)</th><th>What is wrong</th><th>Why it matters / evidence</th><th>Recommended change</th><th>Reference</th></tr></thead><tbody>{issues}</tbody></table>
<h2 id="recommendations">What To Change Next</h2><ul>{recommendations}</ul>
<h2>Merge Decision</h2><p>Merge only when every blocking gate passes and no blocking-severity finding remains. Missing or unavailable evidence cannot be treated as a pass.</p></body></html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("result", type=Path)
    parser.add_argument("--output", type=Path, default=Path("review/review-report.html"))
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(json.loads(args.result.read_text(encoding="utf-8"))), encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())