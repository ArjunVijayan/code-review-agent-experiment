#!/usr/bin/env python3
"""Render review-result.json as a self-contained HTML report."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


def render(result: dict) -> str:
    status = html.escape(result.get("status", "FAILED"))
    gates = result.get("gates", {})
    gate_rows = "".join(
        f"<tr><td>{html.escape(name.replace('_', ' ').title())}</td><td>{html.escape(str(gate.get('status', 'UNCERTAIN')))}</td></tr>"
        for name, gate in gates.items()
    )
    issues = "".join(
        f"<tr><td>{html.escape(item.get('id', item.get('fingerprint', '')))}</td><td>{html.escape(str(item.get('severity', 'INFO')))}</td><td>{html.escape(item.get('issue', ''))}</td><td>{html.escape(str(item.get('evidence', '')))}</td></tr>"
        for item in result.get("findings", [])
    ) or '<tr><td colspan="4">None</td></tr>'
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>PR Code Review</title>
<style>body{{font:16px system-ui,sans-serif;max-width:960px;margin:2rem auto;padding:0 1rem;color:#202124}}h1{{border-bottom:2px solid #202124;padding-bottom:.5rem}}table{{border-collapse:collapse;width:100%;margin:1rem 0}}th,td{{border:1px solid #c8c8c8;padding:.6rem;text-align:left}}th{{background:#f2f2f2}}.status{{font-size:1.4rem;font-weight:700}}.APPROVED{{color:#176b36}}.FAILED{{color:#a12622}}</style></head>
<body><h1>PR Code Review</h1><p class="status {status}">FINAL RESULT: {status}</p>
<h2>Review Gates</h2><table><thead><tr><th>Gate</th><th>Status</th></tr></thead><tbody>{gate_rows}</tbody></table>
<h2>Issues</h2><table><thead><tr><th>ID</th><th>Severity</th><th>Issue</th><th>Evidence</th></tr></thead><tbody>{issues}</tbody></table>
<h2>Decision</h2><p>Approval requires every blocking gate to pass and no blocking-severity finding.</p></body></html>
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