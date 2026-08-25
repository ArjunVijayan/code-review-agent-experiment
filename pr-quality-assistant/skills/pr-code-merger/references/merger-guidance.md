# Merger Guidance

The merger consumes `review/review-result.json`, not HTML, as its authoritative review result. It must fail closed when the review result is absent, invalid, failed, uncertain, missing a gate, or contains a blocking finding.

Assess blast radius using these dimensions:

1. Change size: deterministic files, lines, commits, and modified symbols.
2. Dependency reach: direct and transitive consumers.
3. Architectural criticality: low, medium, high, or critical.
4. Data impact: schema, persistence, deletion, PII, financial data, or credentials.
5. Contract impact: APIs, public methods, events, schemas, interfaces, or configuration contracts.
6. Runtime/deployment impact: configuration, environment, flags, infrastructure, dependencies, startup, or shutdown.

The LLM interprets these facts and must cite evidence. Blast-radius level is explainable and primary; a numeric score is secondary. Low risk plus all review gates passing is the only default auto-merge path. Medium, high, and critical levels require human review.

Always distinguish:

- `decision`: what policy recommends.
- `action`: what the host attempted or may attempt.
- `status`: whether the PR/MR is actually merged and verified.

When no merge capability is available, use `decision: auto_merge`, `action: merge_not_executed`, and `status: not_merged` for an otherwise eligible low-risk change.