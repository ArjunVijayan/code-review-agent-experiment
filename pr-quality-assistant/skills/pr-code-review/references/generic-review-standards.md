# Generic Review Standards

Apply these standards to the existing review gates. They are quality rules for the review output, not additional agent personas.

## Scope and State

- Review only behavior introduced or changed by the current PR/MR. Do not report pre-existing issues as findings.
- Before reviewing, inspect PR/MR state when provider data is available; skip closed or draft requests unless explicitly requested.
- Treat repository instructions (`AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `.github/instructions/`, and equivalent files) as applicable standards. Cite the specific rule when reporting a violation.
- Historical insights provide context and recurring patterns; they are not proof without current evidence.

## Structured Findings

Every finding must include category, severity, status, blocking flag, title or summary, evidence, expected behavior, actual behavior, impact, recommendation, confidence, and references. Evidence should identify the exact source file and line/range, test, artifact section, provider record, or build result where available.

Use `BLOCKER`, `CRITICAL`, `MAJOR`, `MINOR`, or `INFO` severities in the final result. Use `HIGH`, `MEDIUM`, or `LOW` confidence for AI-derived judgments. A finding without evidence, a violated expectation, demonstrable impact, and sufficient confidence cannot block approval; mark it `WARNING` or `NOT_VERIFIABLE`.

## Gate Coverage

The existing five gates must collectively cover acceptance criteria, test sufficiency/coverage, coding and architecture standards, security, historical compliance, regression/blast radius, and build/test status when evidence is available. Do not infer a gate status from prose; provide structured gate status and evidence.

## False-Positive Controls

- Do not flag code merely because it looks AI-generated.
- Do not flag issues that a configured linter or formatter already reports unless the finding explains additional impact.
- Do not recommend tests solely to increase line coverage.
- Do not fabricate test runs, coverage values, source locations, requirements, historical PRs, or references.
- Consolidate findings with the same root cause and link all affected gates and requirements.

## Decision States

Use `READY_TO_MERGE`, `READY_WITH_WARNINGS`, `NOT_READY_TO_MERGE`, or `CANNOT_DETERMINE`. Missing required evidence produces `CANNOT_DETERMINE`; it must not become approval. The policy engine, not the LLM, determines the final decision.
