# PR Quality Assistant

This file is the host-neutral entrypoint for agents that support the Agent Skills specification. Discover the skills under `skills/` by reading each directory's `SKILL.md`; do not require `plugin.json`, `agents/*.agent.md`, or `hooks.json`.

## Persona Flow

For a pre-PR review or an at-PR quality report:

1. Load `data/insights.instructions.md` when present.
2. Invoke `requirement-analysis` with the PR description, linked work item, and commits.
3. Invoke `change-blast-radius` with the diff and requirement output.
4. Invoke `test-analysis` with the change analysis output.
5. Invoke `test-sufficiency` with the test-analysis gap output.
6. If `sufficient` is false, invoke `test-generation`.
7. Invoke `quality-report` with all accumulated outputs.

Keep the skill output contracts intact and surface open questions instead of guessing.

## Repository Intelligence Flow

When the host reports a merged PR, invoke `repo-intelligence`. It must verify the PR is merged, fetch and cleanse review comments, and invoke `insights-generator`. The generator deduplicates by PR ID and comment hash, then updates `data/pr-insights.json` and `data/insights.instructions.md` only when needed.

Hosts without lifecycle hooks should connect their own merged-PR webhook or scheduled automation to `repo-intelligence`. Never treat a session-start prompt as a universal merge event.

## Host Adapters

The `skills/` directory and this file are the portable integration surface. `plugin.json`, `agents/*.agent.md`, and `hooks.json` are optional Copilot-style adapters and may be ignored by other hosts.