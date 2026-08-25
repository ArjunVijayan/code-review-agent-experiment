# Code Review Context

## 1. Review Scope

- Base: `main`
- Source: `dev/open-skills-plugin`
- Merge Base: `a1c05c26d5d4d0af513cb7d5dea7f399eb4eabf0`

## 2. Repository

- Root: `/Users/arjunv/Downloads/review-agents`
- Files discovered: 29
- Manifests: None found

## 3. Change Statistics

- Files changed: 45
- Insertions: 2759
- Deletions: 723

## 4. Changed Files

- `.gitignore` (modified)
- `pr-quality-assistant/.code-review/insights-state.json` (added)
- `pr-quality-assistant/AGENTS.md` (deleted)
- `pr-quality-assistant/FLOW.md` (modified)
- `pr-quality-assistant/README.md` (modified)
- `pr-quality-assistant/agents/developer-code-review.agent.md` (deleted)
- `pr-quality-assistant/agents/pr-quality-report.agent.md` (deleted)
- `pr-quality-assistant/agents/pr-quality.agent.md` (deleted)
- `pr-quality-assistant/agents/repo-intelligence.agent.md` (deleted)
- `pr-quality-assistant/data/insights.instructions.md` (deleted)
- `pr-quality-assistant/data/pr-insights.json` (deleted)
- `pr-quality-assistant/hooks.json` (deleted)
- `pr-quality-assistant/plugin.json` (modified)
- `pr-quality-assistant/pr-insights.json` (added)
- `pr-quality-assistant/skills/_shared/agent-skills-compatibility.md` (deleted)
- `pr-quality-assistant/skills/_shared/analysis-phase.md` (deleted)
- `pr-quality-assistant/skills/change-blast-radius/SKILL.md` (deleted)
- `pr-quality-assistant/skills/change-blast-radius/references/blast-radius-methodology.md` (deleted)
- `pr-quality-assistant/skills/insights-generator/SKILL.md` (deleted)
- `pr-quality-assistant/skills/pr-code-review/SKILL.md` (added)
- `pr-quality-assistant/skills/pr-code-review/references/acceptance-criteria.md` (added)
- `pr-quality-assistant/skills/pr-code-review/references/coverage-analysis.md` (added)
- `pr-quality-assistant/skills/pr-code-review/references/data-collection-guidelines.md` (added)
- `pr-quality-assistant/skills/pr-code-review/references/final-review.md` (added)
- `pr-quality-assistant/skills/pr-code-review/references/insight-generation.md` (added)
- `pr-quality-assistant/skills/pr-code-review/references/insight-schema.md` (added)
- `pr-quality-assistant/skills/pr-code-review/references/review-context-schema.md` (added)
- `pr-quality-assistant/skills/pr-code-review/references/review-policy.json` (added)
- `pr-quality-assistant/skills/pr-code-review/scripts/analyze-test-coverage.py` (added)
- `pr-quality-assistant/skills/pr-code-review/scripts/collect_context.py` (added)
- `pr-quality-assistant/skills/pr-code-review/scripts/discover-historical-prs.py` (added)
- `pr-quality-assistant/skills/pr-code-review/scripts/evaluate-review.py` (added)
- `pr-quality-assistant/skills/pr-code-review/scripts/extract-acceptance-context.py` (added)
- `pr-quality-assistant/skills/pr-code-review/scripts/generate_context.py` (added)
- `pr-quality-assistant/skills/pr-code-review/scripts/git_context.py` (added)
- `pr-quality-assistant/skills/pr-code-review/scripts/manage-insights-state.py` (added)
- `pr-quality-assistant/skills/pr-code-review/scripts/render-review-report.py` (added)
- `pr-quality-assistant/skills/quality-report/SKILL.md` (deleted)
- `pr-quality-assistant/skills/quality-report/references/report-format.md` (deleted)
- `pr-quality-assistant/skills/requirement-analysis/SKILL.md` (deleted)
- `pr-quality-assistant/skills/test-analysis/SKILL.md` (deleted)
- `pr-quality-assistant/skills/test-analysis/references/test-coverage-methodology.md` (deleted)
- `pr-quality-assistant/skills/test-generation/SKILL.md` (deleted)
- `pr-quality-assistant/skills/test-sufficiency/SKILL.md` (deleted)
- `review/review-context.md` (added)

## 5. Commit History

- `cc1d4f00046b` Add deterministic final review evaluation (Arjun V, 2026-08-26T01:35:39+05:30)
- `8467e72aa962` Add evidence-driven acceptance and coverage analysis (Arjun V, 2026-08-26T01:25:27+05:30)
- `ce9e0edbd709` added additional insights (Arjun V, 2026-08-26T01:23:41+05:30)
- `2c97955da96b` Add incremental historical review intelligence (Arjun V, 2026-08-26T01:06:43+05:30)
- `3825d22cf467` Add Git review context collection skill (Arjun V, 2026-08-26T00:36:26+05:30)
- `008927553af9` insights removed (Arjun V, 2026-08-25T22:47:29+05:30)
- `f76a46282e3f` Adopt open Agent Plugins skill standard (Arjun V, 2026-08-25T22:44:47+05:30)

## 6. Repository Instructions

- `pr-quality-assistant/README.md` (scope `/pr-quality-assistant`)

## 7. Tests

- Test files: 0

## 8. Diff

```diff
diff --git a/.gitignore b/.gitignore
index 00fcae4..130e123 100644
--- a/.gitignore
+++ b/.gitignore
@@ -3,3 +3,4 @@
 .slingshot
 .vscode
 .agent
+.pyc
\ No newline at end of file
diff --git a/pr-quality-assistant/.code-review/insights-state.json b/pr-quality-assistant/.code-review/insights-state.json
new file mode 100644
index 0000000..8d2dd23
--- /dev/null
+++ b/pr-quality-assistant/.code-review/insights-state.json
@@ -0,0 +1,5 @@
+{
+  "base_ref": "",
+  "last_analyzed_at": "",
+  "analyzed_change_requests": []
+}
\ No newline at end of file
diff --git a/pr-quality-assistant/AGENTS.md b/pr-quality-assistant/AGENTS.md
deleted file mode 100644
index 36248be..0000000
--- a/pr-quality-assistant/AGENTS.md
+++ /dev/null
@@ -1,27 +0,0 @@
-# PR Quality Assistant
-
-This file is the host-neutral entrypoint for agents that support the Agent Skills specification. Discover the skills under `skills/` by reading each directory's `SKILL.md`; do not require `plugin.json`, `agents/*.agent.md`, or `hooks.json`.
-
-## Persona Flow
-
-For a pre-PR review or an at-PR quality report:
-
-1. Load `data/insights.instructions.md` when present.
-2. Invoke `requirement-analysis` with the PR description, linked work item, and commits.
-3. Invoke `change-blast-radius` with the diff and requirement output.
-4. Invoke `test-analysis` with the change analysis output.
-5. Invoke `test-sufficiency` with the test-analysis gap output.
-6. If `sufficient` is false, invoke `test-generation`.
-7. Invoke `quality-report` with all accumulated outputs.
-
-Keep the skill output contracts intact and surface open questions instead of guessing.
-
-## Repository Intelligence Flow
-
-When the host reports a merged PR, invoke `repo-intelligence`. It must verify the PR is merged, fetch and cleanse review comments, and invoke `insights-generator`. The generator deduplicates by PR ID and comment hash, then updates `data/pr-insights.json` and `data/insights.instructions.md` only when needed.
-
-Hosts without lifecycle hooks should connect their own merged-PR webhook or scheduled automation to `repo-intelligence`. Never treat a session-start prompt as a universal merge event.
-
-## Host Adapters
-
-The `skills/` directory and this file are the portable integration surface. `plugin.json`, `agents/*.agent.md`, and `hooks.json` are optional Copilot-style adapters and may be ignored by other hosts.
\ No newline at end of file
diff --git a/pr-quality-assistant/FLOW.md b/pr-quality-assistant/FLOW.md
index dcd4d28..72d13b4 100644
--- a/pr-quality-assistant/FLOW.md
+++ b/pr-quality-assistant/FLOW.md
@@ -1,58 +1,41 @@
-# Agent and Skill Flow
+# Agent Skills Flow
 
 ```mermaid
 flowchart TD
-    subgraph Personas[On-demand persona agents]
-        D[developer-code-review.agent.md]
-        R[pr-quality-report.agent.md]
-        P[pr-quality.agent.md\nCopilot orchestration adapter]
-    end
+    H[Agent Skills-compatible host] --> CR[pr-code-review skill]
+    CR --> V[Validate repository and refs]
+    V --> MB[Calculate merge base]
+    MB --> C[Collect CodeReviewContext]
+    C --> GM[Git metadata]
+    C --> DF[Diff and changed files]
+    C --> CH[Commit history]
+    C --> RS[Repository structure]
+    C --> IT[Instructions and tests]
+    GM --> CT[Context JSON]
+    DF --> CT
+    CH --> CT
+    RS --> CT
+    IT --> CT
+    CT --> MD[review/review-context.md]
+    CT --> AC[Acceptance context facts]
+    AC --> ACM[review/acceptance-criteria.md]
+    CT --> TC[Test and coverage facts]
+    TC --> TCM[review/code-coverage-report.md]
+    MD --> RH[Review handoff]
+    ACM --> RH
+    TCM --> RH
+    RH --> FR[Final five-gate review]
+    FR --> RR[review/review-result.json]
+    RR --> HTML[review/review-report.html]
+
+    W[Merged PR webhook or scheduled job] --> RI[repo-intelligence]
+    RI --> IG[Review comment extraction and cleansing]
+    IG --> D[Deduplicate by PR ID + comment hash]
+    D --> J[pr-insights.json]
+    D --> I[.github/instructions/insights.instructions.md]
+    I -. loaded by .-> CR
+    J -. detailed provenance .-> CR
 
-    I[data/insights.instructions.md]
-    Q[requirement-analysis]
-    B[change-blast-radius]
-    T[test-analysis]
-    S[test-sufficiency]
-    G{Tests sufficient?}
-    TG[test-generation]
-    QR[quality-report]
-
-    D --> I
-    R --> I
-    P --> I
-    D --> Q
-    R --> Q
-    P --> Q
-    Q --> B --> T --> S --> G
-    G -->|yes| QR
-    G -->|no| TG --> QR
-
-    subgraph Intelligence[Merge-triggered repo intelligence]
-        H[Host webhook, scheduled job, or Copilot session-start adapter]
-        RI[repo-intelligence.agent.md]
-        IG[insights-generator]
-        JSON[data/pr-insights.json]
-        INST[data/insights.instructions.md]
-    end
-
-    H -->|merged PR only| RI --> IG
-    IG -->|deduplicate by PR ID + comment hash| JSON
-    IG -->|regenerate shared guidance| INST
-    INST -. loaded by .-> D
-    INST -. loaded by .-> R
-    INST -. loaded by .-> P
-
-    subgraph Shared[Shared workflow references]
-        AP[skills/_shared/analysis-phase.md]
-        AC[skills/_shared/agent-skills-compatibility.md]
-    end
-
-    AP -. defines order .-> Q
-    AP -. defines order .-> B
-    AP -. defines order .-> T
-    AC -. host contract .-> D
-    AC -. host contract .-> R
-    AC -. host contract .-> RI
 ```
 
-The `skills/` directories and `AGENTS.md` are the portable Agent Skills integration surface. `plugin.json`, `agents/*.agent.md`, and `hooks.json` are optional host adapters.
\ No newline at end of file
+The portable package surface is `plugin.json` plus the immediate skill directories under `skills/`. The Git-only collector produces review context; hosts decide how to expose skills and deliver merged-PR events.
\ No newline at end of file
diff --git a/pr-quality-assistant/README.md b/pr-quality-assistant/README.md
index d1cb9f7..caec581 100644
--- a/pr-quality-assistant/README.md
+++ b/pr-quality-assistant/README.md
@@ -1,29 +1,29 @@
 # PR Quality Assistant
 
-This package exposes two reusable Agent Skills flows. Start with [AGENTS.md](AGENTS.md); it is the host-neutral entrypoint. The Copilot files provide one optional host adapter; other Agent Skills-compatible agents can discover and invoke the skills directly.
+This package is an Agent Plugins v1.0 package containing one primary portable Agent Skill. Clients discover it from the fixed `skills/` directory; no custom agent or orchestration layer is required.
 
-See [FLOW.md](FLOW.md) for the complete agent and skill flowchart.
+The `pr-code-review` skill first refreshes incremental historical intelligence, then collects Git-only context for a logical request such as `{ "base": "main", "source": "dev/bug_fix" }`. It creates a structured `CodeReviewContext`, renders evidence packages, evaluates five review gates, and produces `review/review-result.json` plus `review/review-report.html` without calling a hosting API.
 
-## On-demand persona flow
+See [FLOW.md](FLOW.md) for the complete skill flowchart.
 
-The developer review and PR quality report personas load repository insights, then share one analysis sequence:
+## On-demand review flow
 
-`requirements -> change and blast-radius -> test-analysis -> test-sufficiency`
+The `pr-code-review` skill provides the context handoff for developer-facing pre-PR review and PR-facing quality reporting:
+
+`historical intelligence -> current context -> acceptance + coverage evidence -> five-gate evaluation -> JSON result + HTML report`
 
 When tests are insufficient, test generation runs before acceptance-criteria traceability and the final quality report.
 
 ## Merge-triggered intelligence flow
 
-On a merged PR event, the host invokes `repo-intelligence`. That agent fetches and cleanses review comments, then calls `insights-generator`, which deduplicates evidence by PR ID and comment hash and updates `data/pr-insights.json` plus `data/insights.instructions.md` when a new reusable rule is found.
+During the historical phase, the host supplies merged change requests and review feedback to the `repo-intelligence` workflow described in `skills/pr-code-review/references/insight-generation.md`. It deduplicates evidence by change-request ID and comment hash, and updates `pr-insights.json` plus `.github/instructions/insights.instructions.md` when a new reusable rule is found.
 
-For Copilot, the valid session-start hook prompts `repo-intelligence` to check for newly merged PRs because the current Copilot hooks reference has no PR-merged event. Other compatible hosts should connect their native PR webhook or scheduled automation to the same agent. The agent's merge-status check keeps any adapter from recording unmerged PR feedback.
+The host supplies the change-request provider data through its webhook, scheduled job, or native lifecycle event. Hosts without lifecycle events may invoke discovery manually, but the workflow must verify merge status before writing either output.
 
 ## Compatibility
 
-Any host implementing the Agent Skills specification can use `AGENTS.md` and the directories under `skills/`; see `skills/_shared/agent-skills-compatibility.md` for the host contract. The Markdown persona agents, `plugin.json`, and `hooks.json` are optional adapters, while `data/` is the shared persistence format.
+Any Agent Plugins-compatible client can load this package. An Agent Skills-compatible client can consume the `pr-code-review/SKILL.md` file directly; the historical workflow is an internal phase, not a second exposed skill. The open standard controls package and skill discovery; each host controls user experience and event delivery.
 
-## Documentation consulted
+## Standard
 
-- [GitHub Copilot plugins](https://docs.github.com/en/copilot/concepts/agents/plugins) for the requested plugin conventions (the page was unavailable during validation).
-- [GitHub Copilot hooks reference](https://docs.github.com/en/copilot/reference/hooks-configuration), especially **Hook configuration format** and **Hook events**.
-- [Using hooks with GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/use-hooks) for the `version: 1` and `sessionStart` configuration examples.
\ No newline at end of file
+This package follows [Agent Plugins Specification 1.0.0](https://github.com/agentplugins/agent-plugins-spec/blob/main/spec/1.0.0.md) and [Agent Skills Specification](https://agentskills.io/specification). The plugin manifest uses the canonical Agent Plugins schema; skills are discovered from `skills/<name>/SKILL.md`.
\ No newline at end of file
diff --git a/pr-quality-assistant/agents/developer-code-review.agent.md b/pr-quality-assistant/agents/developer-code-review.agent.md
deleted file mode 100644
index 8216d76..0000000
--- a/pr-quality-assistant/agents/developer-code-review.agent.md
+++ /dev/null
@@ -1,17 +0,0 @@
----
-name: developer-code-review
-description: Performs an on-demand pre-PR developer review using repository requirements, blast-radius, test, and accumulated review insights to find actionable quality risks.
-skills:
-  - requirement-analysis
-  - change-blast-radius
-  - test-analysis
-  - test-sufficiency
-  - test-generation
-  - quality-report
----
-
-# Developer Code Review
-
-Load `data/insights.instructions.md` as additional repository context before invoking any skill. Treat it as auto-maintained guidance and use it to focus review attention, not to override the current PR evidence. For host-neutral discovery and invocation rules, follow `skills/_shared/agent-skills-compatibility.md`.
-
-Follow the shared sequence in `skills/_shared/analysis-phase.md`: requirement-analysis, change-blast-radius, then test-analysis. Invoke `test-sufficiency` explicitly with the test-analysis output. If it returns `sufficient: false`, invoke `test-generation` before the final `quality-report`; otherwise proceed directly to reporting. Surface open questions instead of guessing.
\ No newline at end of file
diff --git a/pr-quality-assistant/agents/pr-quality-report.agent.md b/pr-quality-assistant/agents/pr-quality-report.agent.md
deleted file mode 100644
index c5308d0..0000000
--- a/pr-quality-assistant/agents/pr-quality-report.agent.md
+++ /dev/null
@@ -1,17 +0,0 @@
----
-name: pr-quality-report
-description: Produces an at-PR-time quality report by tracing requirements through change risk and test coverage, informed by accumulated repository review insights.
-skills:
-  - requirement-analysis
-  - change-blast-radius
-  - test-analysis
-  - test-sufficiency
-  - test-generation
-  - quality-report
----
-
-# PR Quality Report
-
-Load `data/insights.instructions.md` as additional repository context before invoking any skill. Apply relevant rules as review considerations and distinguish them from evidence in the current PR. For host-neutral discovery and invocation rules, follow `skills/_shared/agent-skills-compatibility.md`.
-
-Follow the shared sequence in `skills/_shared/analysis-phase.md`: requirement-analysis, change-blast-radius, then test-analysis. Invoke `test-sufficiency` explicitly with the test-analysis output. If it returns `sufficient: false`, invoke `test-generation` before `quality-report`; otherwise pass the analysis outputs directly to `quality-report`. Include unresolved requirements and gaps in the final report.
\ No newline at end of file
diff --git a/pr-quality-assistant/agents/pr-quality.agent.md b/pr-quality-assistant/agents/pr-quality.agent.md
deleted file mode 100644
index 7ff16c9..0000000
--- a/pr-quality-assistant/agents/pr-quality.agent.md
+++ /dev/null
@@ -1,58 +0,0 @@
----
-name: pr-quality-agent
-description: Orchestrates end-to-end PR quality assessment by sequencing requirement analysis, change/blast-radius analysis, test analysis, conditional test generation, and final quality reporting.
-skills:
-  - requirement-analysis
-  - change-blast-radius
-  - test-analysis
-  - test-generation
-  - quality-report
----
-
-# PR Quality Agent
-
-## Role
-You are the orchestrator for PR Quality Assistance. You do not perform deep analysis yourself — you invoke the appropriate skill at each stage, pass structured context between them, and make sequencing/branching decisions based on their outputs.
-
-## Workflow
-
-```
-Requirements → Change Analysis → Blast Radius → Test Analysis →
-  Test Generation (conditional) → Acceptance Criteria / Test Traceability →
-  Quality Assessment → Final Report
-```
-
-### Stage 1 — Requirement Analysis
-Invoke `requirement-analysis` with the PR description and any linked ticket/story context.
-**Output contract:** `{ requirements[], acceptanceCriteria[], openQuestions[] }`
-
-### Stage 2 — Change & Blast Radius Analysis
-Invoke `change-blast-radius` with the PR diff and Stage 1 output.
-**Output contract:** `{ changedFiles[], affectedModules[], riskTier, blastRadiusSummary }`
-
-### Stage 3 — Test Analysis
-Invoke `test-analysis` with Stage 2 output (changed files/modules) plus repository test suite location.
-**Output contract:** `{ coverageGaps[], existingTestsMapped[], acceptanceCriteriaCoverage[] }`
-
-### Stage 4 — Test Generation (Conditional)
-Invoke `test-generation` **only if** `coverageGaps` from Stage 3 is non-empty.
-**Output contract:** `{ generatedTests[], skippedGaps[] (with reason) }`
-
-### Stage 5 — Acceptance Criteria / Test Traceability
-Built into `quality-report`. Combine Stage 1 `acceptanceCriteria[]` with Stage 3/4 test mappings to produce a traceability matrix (AC → test(s) → pass/fail/untested).
-
-### Stage 6 — Quality Assessment & Reporting
-Invoke `quality-report` with the aggregated outputs of all prior stages.
-**Output contract:** final markdown report (see `quality-report/references/report-format.md`) including quality score, risk tier, traceability matrix, and actionable recommendations.
-
-## Branching Rules
-- If `requirement-analysis` returns `openQuestions[]`, surface them to the user before proceeding — do not guess intent.
-- If `riskTier` from Stage 2 is `high`, ensure `test-analysis` runs in strict mode (fail on any gap rather than warn).
-- Skip Stage 4 only when Stage 3 reports zero gaps; otherwise always attempt generation before reporting.
-
-## Extension Points (future)
-- **Hook — pre-report**: reserved for future MCP/hook integration to post the final report as an inline PR comment automatically. Not implemented in this version; `quality-report` currently returns markdown only.
-- **Hook — post-test-generation**: reserved for future auto-commit of generated tests to a review branch.
-
-## Non-Goals
-- This agent does not merge PRs, approve/reject them, or modify source code outside of generated test files.
diff --git a/pr-quality-assistant/agents/repo-intelligence.agent.md b/pr-quality-assistant/agents/repo-intelligence.agent.md
deleted file mode 100644
index 061e207..0000000
--- a/pr-quality-assistant/agents/repo-intelligence.agent.md
+++ /dev/null
@@ -1,46 +0,0 @@
----
-name: repo-intelligence
-description: Maintains repository review intelligence after a pull request is merged by extracting deduplicated patterns from its review comments and updating shared agent guidance.
-skills:
-  - insights-generator
----
-
-# Repository Intelligence
-
-## Trigger
-Run for a merged pull request. The host may invoke this agent from a webhook, scheduled job, native lifecycle event, or Copilot hook. Regardless of host, the agent must verify merge status before changing repository intelligence.
-
-## Workflow
-1. Fetch the merged PR's review comments and metadata.
-2. Cleanse secrets, personal data, and irrelevant conversational content.
-3. Compare the normalized comments with `data/pr-insights.json` using PR ID plus comment hash as the idempotency key.
-4. Invoke `insights-generator` with the historical PRs, comments, and existing insight files.
-5. If feedback reveals a new reusable pattern, add or update its rule and regenerate `data/insights.instructions.md`.
-6. If the pattern is already documented, record no duplicate rule or evidence and skip the update.
-
-Do not infer a rule from a one-off comment without actionable repository-wide guidance. Never store secrets or sensitive comment text in either data file.
-
-## Review-Comment Extraction Contract
-
-Ask the repository integration available in the host to fetch all review comments for the target repository. Extract only generalizable coding rules and pass them to `insights-generator` as structured data:
-
-```json
-{
-  "insights": [
-    {
-      "pattern": "...",
-      "category": "suggestion|defect_pattern|performance|security|testing|code_quality|database",
-      "language": "...",
-      "description": "...",
-      "module": "...",
-      "shared": false
-    }
-  ]
-}
-```
-
-Ignore questions, clarification requests, one-off line-level nitpicks, and PR-specific observations. Merge comments expressing the same rule and keep the clearest wording. Mark rules affecting shared or common modules with `shared: true` and record the module. Use `database` for schema, query, migration, transaction, or connection-handling feedback.
-
-Inspect available manifests (`pom.xml`, `build.gradle`, `pyproject.toml`, `requirements.txt`, `Pipfile`, `package.json`, `go.mod`, `Cargo.toml`, and `*.csproj`) and pass detected language, framework, and package context to `insights-generator`. The generated guidance must also tell reviewers to check manifest dependencies for known CVEs and approaching end-of-life.
-
-The generated instructions must put shared-module rules first, then language/package guidance, dependency health, database rules, remaining category-grouped rules, and regression guidance. Regression guidance must require reviewing changed or added tests, preserving existing coverage, and protecting existing behavior and public contracts. Deduplicate against any `AGENTS.md` and existing instruction files before updating `data/insights.instructions.md`.
\ No newline at end of file
diff --git a/pr-quality-assistant/data/insights.instructions.md b/pr-quality-assistant/data/insights.instructions.md
deleted file mode 100644
index e7ed04f..0000000
--- a/pr-quality-assistant/data/insights.instructions.md
+++ /dev/null
@@ -1,19 +0,0 @@
-# Repository Review Insights
-
-<!-- Auto-maintained by the repo-intelligence agent. Do not hand-edit below this marker. -->
-
-<!-- BEGIN GENERATED INSIGHTS -->
-## Source
-
-Detailed rules live in `data/pr-insights.json`; this file summarizes them for review agents.
-
-## Dependency Health
-
-Check manifest dependencies for known CVEs and approaching end-of-life, and flag findings in review.
-
-## Regression
-
-Verify that changes add or update tests, preserve existing test coverage, and do not break existing behavior or public contracts.
-
-No repository-specific review rules have been recorded yet.
-<!-- END GENERATED INSIGHTS -->
\ No newline at end of file
diff --git a/pr-quality-assistant/data/pr-insights.json b/pr-quality-assistant/data/pr-insights.json
deleted file mode 100644
index 7d00d1f..0000000
--- a/pr-quality-assistant/data/pr-insights.json
+++ /dev/null
@@ -1,3 +0,0 @@
-{
-  "rules": []
-}
\ No newline at end of file
diff --git a/pr-quality-assistant/hooks.json b/pr-quality-assistant/hooks.json
deleted file mode 100644
index e6f652d..0000000
--- a/pr-quality-assistant/hooks.json
+++ /dev/null
@@ -1,12 +0,0 @@
-{
-  "version": 1,
-  "_comment": "Optional Copilot adapter only. The current GitHub Copilot hooks reference, Hook events section, does not define a PR-merged event. This valid sessionStart prompt asks repo-intelligence to process newly merged PRs and verify merge status.",
-  "hooks": {
-    "sessionStart": [
-      {
-        "type": "prompt",
-        "prompt": "Check whether any new pull requests have merged since the last repository-intelligence run. If so, invoke the repo-intelligence agent for each merged PR; otherwise take no action. Verify merge status before updating data files."
-      }
-    ]
-  }
-}
\ No newline at end of file
diff --git a/pr-quality-assistant/plugin.json b/pr-quality-assistant/plugin.json
index aa26091..9812e8c 100644
--- a/pr-quality-assistant/plugin.json
+++ b/pr-quality-assistant/plugin.json
@@ -1,29 +1,12 @@
 {
+  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
   "name": "pr-quality-assistant",
-  "version": "0.1.0",
-  "description": "Agent Skills-compatible PR quality workflow with reusable review analysis, test sufficiency, quality reporting, and repository intelligence.",
-  "publisher": "ps-health",
-  "license": "UNLICENSED",
-  "entry": {
-    "agents": [
-      "./agents/pr-quality.agent.md",
-      "./agents/developer-code-review.agent.md",
-      "./agents/pr-quality-report.agent.md",
-      "./agents/repo-intelligence.agent.md"
-    ],
-    "skills": [
-      "./skills/requirement-analysis",
-      "./skills/change-blast-radius",
-      "./skills/test-analysis",
-      "./skills/test-generation",
-      "./skills/quality-report",
-      "./skills/test-sufficiency",
-      "./skills/insights-generator"
-    ],
-    "hooks": [
-      "./hooks.json"
-    ]
+  "version": "0.2.0",
+  "description": "Portable Agent Skills for pull-request review, test sufficiency, quality reporting, and repository intelligence.",
+  "author": {
+    "name": "ps-health"
   },
+  "license": "UNLICENSED",
   "keywords": [
     "pull-request",
     "code-review",
diff --git a/pr-quality-assistant/pr-insights.json b/pr-quality-assistant/pr-insights.json
new file mode 100644
index 0000000..79174e4
--- /dev/null
+++ b/pr-quality-assistant/pr-insights.json
@@ -0,0 +1,3 @@
+{
+  "insights": []
+}
\ No newline at end of file
diff --git a/pr-quality-assistant/skills/_shared/agent-skills-compatibility.md b/pr-quality-assistant/skills/_shared/agent-skills-compatibility.md
deleted file mode 100644
index bfc7d1d..0000000
--- a/pr-quality-assistant/skills/_shared/agent-skills-compatibility.md
+++ /dev/null
@@ -1,12 +0,0 @@
-# Agent Skills Compatibility
-
-The directories under `skills/` are the portable integration surface. Any agent host that supports the Agent Skills format can discover a skill by its directory and `SKILL.md` file, then invoke it by the frontmatter `name`.
-
-Hosts should provide these inputs and preserve the documented output contracts. The shared workflow is:
-
-1. Load `data/insights.instructions.md` when it exists.
-2. Run `requirement-analysis`, `change-blast-radius`, and `test-analysis` in that order.
-3. Run `test-sufficiency` with the test-analysis output.
-4. Run `test-generation` only when sufficiency is false, then run `quality-report`.
-
-The `agents/*.agent.md`, `plugin.json`, and `hooks.json` files are optional host adapters. A host without Copilot plugin or hook support can use the skills directly and invoke `repo-intelligence` from its own merged-PR webhook or scheduled automation. The intelligence agent must still verify merge status and write the same two data files.
\ No newline at end of file
diff --git a/pr-quality-assistant/skills/_shared/analysis-phase.md b/pr-quality-assistant/skills/_shared/analysis-phase.md
deleted file mode 100644
index 0af638d..0000000
--- a/pr-quality-assistant/skills/_shared/analysis-phase.md
+++ /dev/null
@@ -1,9 +0,0 @@
-# Shared Analysis Phase
-
-Both PR-quality personas use this order and pass each output to the next skill:
-
-1. `requirement-analysis`: extract requirements, acceptance criteria, and open questions.
-2. `change-blast-radius`: map changed and affected modules and assign a risk tier.
-3. `test-analysis`: map tests to the requirements and report coverage gaps.
-
-Do not reorder or skip these stages. The `test-sufficiency` skill consumes the `test-analysis` gap output before any conditional test generation or reporting.
\ No newline at end of file
diff --git a/pr-quality-assistant/skills/change-blast-radius/SKILL.md b/pr-quality-assistant/skills/change-blast-radius/SKILL.md
deleted file mode 100644
index 6221eae..0000000
--- a/pr-quality-assistant/skills/change-blast-radius/SKILL.md
+++ /dev/null
@@ -1,38 +0,0 @@
----
-name: change-blast-radius
-description: Analyzes the PR diff to identify changed files, dependent/affected modules, and an overall risk tier (blast radius). Use after requirement-analysis and before test-analysis.
----
-
-# Change & Blast Radius Analysis
-
-## Purpose
-Determine the full scope of impact of the code changes in the PR — not just the files touched, but everything that depends on them — and assign a risk tier to guide how strict downstream test analysis should be.
-
-## Inputs
-- PR diff (changed files, added/removed/modified lines)
-- Repository dependency graph (imports, module references, shared config)
-- `requirements[]` from `requirement-analysis`
-
-## Steps
-1. List all changed files and classify the type of change (logic, config, schema, styling, test-only).
-2. Traverse direct and transitive dependents of changed files/modules.
-3. Classify affected modules as `direct` or `indirect` impact.
-4. Assign a `riskTier` (`low` | `medium` | `high`) per the methodology in `references/blast-radius-methodology.md`.
-5. Summarize the blast radius in plain language for the final report.
-
-See `references/blast-radius-methodology.md` for detailed scoring rules and dependency traversal approach.
-
-## Output Contract
-```json
-{
-  "changedFiles": ["path/to/file.ts"],
-  "affectedModules": [
-    { "module": "...", "impact": "direct|indirect" }
-  ],
-  "riskTier": "low|medium|high",
-  "blastRadiusSummary": "..."
-}
-```
-
-## Handoff
-Pass `changedFiles[]`, `affectedModules[]`, and `riskTier` to `test-analysis`. A `high` risk tier should cause the orchestrator to run test-analysis in strict mode.
diff --git a/pr-quality-assistant/skills/change-blast-radius/references/blast-radius-methodology.md b/pr-quality-assistant/skills/change-blast-radius/references/blast-radius-methodology.md
deleted file mode 100644
index a314da1..0000000
--- a/pr-quality-assistant/skills/change-blast-radius/references/blast-radius-methodology.md
+++ /dev/null
@@ -1,42 +0,0 @@
-# Blast Radius Methodology
-
-## Goal
-Provide a repeatable, explainable method for quantifying how far the impact of a change can propagate through a codebase, so risk can be assessed objectively rather than by intuition.
-
-## Step 1 — Classify Changed Files
-For each file in the diff, classify the change type:
-| Change Type | Examples |
-|---|---|
-| Logic | function/method body changes |
-| Interface | function signature, exported type, API contract changes |
-| Schema | DB schema, GraphQL schema, config schema |
-| Config | env vars, feature flags, build config |
-| Styling | CSS/UI-only changes with no logic impact |
-| Test-only | changes confined to test files |
-
-## Step 2 — Dependency Traversal
-1. Build (or reuse) a dependency graph from static imports/references.
-2. **Direct impact**: modules that directly import/reference a changed file or symbol.
-3. **Indirect impact**: modules that depend on a direct-impact module (traverse up to 2 levels by default; deeper only if the change is an `Interface` or `Schema` type).
-4. Stop traversal at natural boundaries (e.g., published package boundaries, microservice boundaries) but flag cross-boundary impacts as high-attention items.
-
-## Step 3 — Risk Tier Scoring
-Score = weighted sum of:
-- Change type weight: Interface/Schema = 3, Logic = 2, Config = 2, Styling = 1, Test-only = 0
-- Number of direct-impact modules (capped contribution)
-- Number of indirect-impact modules (capped contribution, lower weight than direct)
-- Whether changed code sits on a critical path (auth, payments, data integrity) — apply a multiplier if so
-
-| Score Range | Risk Tier |
-|---|---|
-| 0–3 | low |
-| 4–8 | medium |
-| 9+ | high |
-
-## Step 4 — Summarize
-Produce a human-readable summary, e.g.:
-> "3 files changed (2 logic, 1 interface). 4 direct-impact modules, 7 indirect-impact modules across the `billing` domain. Risk tier: **high** due to interface change on a critical payment path."
-
-## Notes for Implementers
-- Prefer static analysis tools available in-repo (e.g., `madge`, language-server references) over manual heuristics when possible.
-- If no dependency graph tooling is available, fall back to grep-based reference search and clearly flag reduced confidence in the summary.
diff --git a/pr-quality-assistant/skills/insights-generator/SKILL.md b/pr-quality-assistant/skills/insights-generator/SKILL.md
deleted file mode 100644
index 57a0364..0000000
--- a/pr-quality-assistant/skills/insights-generator/SKILL.md
+++ /dev/null
@@ -1,50 +0,0 @@
----
-name: insights-generator
-description: Extracts reusable review patterns and rules from historical PR review comments, deduplicates them by PR ID and comment hash, and maintains the repository intelligence files.
----
-
-# Insights Generator
-
-## Purpose
-Turn review feedback into durable repository-specific guidance for the PR-quality personas. Treat review comments as input evidence, not as instructions to blindly copy.
-
-## Inputs
-- Historical PR metadata, including a stable PR ID and merge status
-- Review comments, including author, body, file/line location when available, and comment ID
-- Existing `data/pr-insights.json` and `data/insights.instructions.md`
-
-## Process
-1. Consider merged PRs and their review comments; cleanse secrets, credentials, personal data, and irrelevant conversational text.
-2. Normalize each remaining comment and compute a stable hash from its PR ID, comment ID when available, location, and normalized body.
-3. Compare `(prId, commentHash)` with recorded evidence. Re-running on the same PR must not add duplicate evidence or rules.
-4. Group new comments into actionable recurring patterns. Add a rule only when the feedback identifies a reusable repository practice; otherwise retain the evidence without inventing a rule.
-5. Write the updated structured result to `data/pr-insights.json`, preserving existing entries and provenance.
-6. Inspect repository manifests for language, frameworks, and packages. Check `AGENTS.md` and existing instruction files before writing, and omit rules already covered there.
-7. Regenerate `data/insights.instructions.md` from the current rules. Keep the generated file concise, actionable, and safe to load as agent context. Put shared-module rules first, followed by language/package guidance, dependency health, database rules, category-grouped general rules, and regression guidance.
-
-## Output Contract
-`data/pr-insights.json` contains this shape:
-
-```json
-{
-  "rules": [
-    {
-      "id": "rule-...",
-      "pattern": "...",
-      "guidance": "...",
-      "evidence": [{ "prId": 123, "commentHash": "..." }]
-    }
-  ]
-}
-```
-
-The skill reports changed rule IDs, skipped duplicate evidence, and any comments withheld during cleansing. It must be safe to run repeatedly and must not edit source code.
-
-## Rule Classification
-
-- Keep only generalizable, actionable rules; ignore questions, clarification requests, and one-off line-level nitpicks.
-- Use categories `suggestion`, `defect_pattern`, `performance`, `security`, `testing`, `code_quality`, and `database`.
-- Set `shared: true` and record `module` for shared or common modules.
-- Use `database` for schema, queries, migrations, transactions, and connection handling.
-- Include a dependency-health instruction to check known CVEs and approaching end-of-life dependencies.
-- Include regression guidance to update or add tests, preserve existing coverage, and protect behavior and public contracts.
\ No newline at end of file
diff --git a/pr-quality-assistant/skills/pr-code-review/SKILL.md b/pr-quality-assistant/skills/pr-code-review/SKILL.md
new file mode 100644
index 0000000..8aeaaa0
--- /dev/null
+++ b/pr-quality-assistant/skills/pr-code-review/SKILL.md
@@ -0,0 +1,63 @@
+---
+name: pr-code-review
+description: Builds incremental historical review intelligence, collects Git repository context for a base/source comparison, and produces a traceable review-context.md artifact for later code review. Use with logical base and source refs for pre-PR or pull-request review.
+---
+
+# PR Code Review
+
+When invoked with the logical request `{ "base": "main", "source": "dev/bug_fix" }`, execute the phases below in order. Current-change context and historical knowledge are separate artifacts and must not be conflated.
+
+## Phase 1: Historical Intelligence
+
+1. Validate the repository and base ref before attempting discovery.
+2. Read `.code-review/insights-state.json`; if absent, treat historical knowledge as empty and bootstrap.
+3. Ask the host's change-request provider for merged change requests targeting the base ref. Git alone cannot supply PR/MR IDs, comments, reviewers, or approval history; do not add provider API logic to the scripts.
+4. Pass normalized provider JSON to `scripts/discover-historical-prs.py` with the state file and `--limit 100`. It returns only newly discovered, merged requests for the selected base. On a changed base ref, start a fresh analyzed set.
+5. For each returned request, provide its description, review comments, threads, and reviews to the model using `references/insight-generation.md`. Extract only generalizable, actionable rules; ignore questions and one-off or PR-specific feedback.
+6. Semantically deduplicate the extracted rules against the existing root `pr-insights.json`. Write knowledge to `pr-insights.json` and concise reviewer guidance to `.github/instructions/insights.instructions.md` in the required section order.
+7. Only after both outputs are successfully written, run `scripts/manage-insights-state.py --mark-success --base <base> --state .code-review/insights-state.json --successful-ids ...`. Never mark requests before successful generation.
+
+If no new requests are returned, preserve the existing insight files and state. Do not generate a historical raw-comments document.
+
+## Phase 2: Current Change Context
+
+1. Validate the repository, base ref, source ref, distinct commits, and merge base.
+2. Collect Git metadata, changed files, numeric diff statistics, complete raw diff, and introduced commit history.
+3. Collect repository structure, manifests, applicable instruction files, and test information.
+4. Build the canonical `CodeReviewContext` object with `scripts/collect_context.py`.
+5. Render `review/review-context.md` with `scripts/generate_context.py`. Keep the raw diff last.
+
+## Phase 3: Evidence Analysis
+
+1. Run `scripts/extract-acceptance-context.py` with the current context and any provider-supplied PR description, comments, threads, reviews, and issue references.
+2. Synthesize `review/acceptance-criteria.md` from that evidence using `references/acceptance-criteria.md`. Include source, evidence, confidence, and verification for every criterion. Merge semantic duplicates but preserve distinct observable behaviors. If intent is not supported, write `Unknown / cannot determine`; never invent a criterion from engineering convention or implementation detail alone.
+3. Run `scripts/analyze-test-coverage.py` with the current context. It inventories changed behavior candidates, tests, manifests, test commands, and measured coverage files.
+4. Synthesize `review/code-coverage-report.md` from those facts using `references/coverage-analysis.md`. Analyze behavioral execution paths and meaningful success, boundary, and error scenarios. Distinguish measured coverage from change-based test sufficiency, and never fabricate a percentage or claim a test passed without evidence.
+
+The two Markdown files are evidence packages for a later reviewer, not generic prose. Preserve links to changed paths, test names, manifests, coverage reports, PR IDs, and comments wherever available.
+
+## Phase 4: Final Review Assessment
+
+The final reviewer consumes `.github/instructions/insights.instructions.md`, `pr-insights.json`, `review/review-context.md`, `review/acceptance-criteria.md`, `review/code-coverage-report.md`, and the relevant source code. Evaluate exactly five gates: coverage, acceptance criteria, coding guidelines, historical compliance, and AI-slop. Use `references/final-review.md` to produce `review/review-assessment.json`.
+
+Every gate must be `PASS`, `FAIL`, `UNCERTAIN`, or `NOT_APPLICABLE`. Do not convert missing evidence or uncertainty into a pass. Findings must include severity from `BLOCKER`, `CRITICAL`, `MAJOR`, `MINOR`, or `INFO`, plus issue, impact, evidence, reference, recommendation, and a stable fingerprint when the same underlying issue appears in multiple gates.
+
+Run `scripts/evaluate-review.py review/review-assessment.json --policy references/review-policy.json` to produce the canonical `review/review-result.json`. The evaluator applies the configurable coverage threshold (default 95), mandatory gate rules, blocking severities, and AI-slop limits. It consolidates duplicate findings across gates. Approval requires all blocking gates to pass and no blocking-severity finding.
+
+Run `scripts/render-review-report.py review/review-result.json` to produce the human-facing `review/review-report.html`. HTML is presentation only; downstream automation must consume `review/review-result.json`.
+
+The AI-slop gate reports only unnecessary complexity, risk, duplication, maintenance burden, or repository-convention violations. Do not flag code merely because it appears AI-generated.
+
+## Phase 5: Review Handoff
+
+The skill stops after producing the structured result and HTML report. A merger or other downstream agent should consume `review/review-result.json`, not parse HTML or reinterpret an LLM response. This skill does not approve or reject changes on behalf of a host; it records the policy evaluation and decision.
+
+Do not perform code review at this stage.
+
+Do not make approval decisions.
+
+## Logical Request and Implementation
+
+The client or launcher maps its command syntax to the logical request; the skill does not depend on a specific CLI. The provider maps its API response to the normalized input expected by `scripts/discover-historical-prs.py`. Run `scripts/collect_context.py` to produce the current-change context JSON, then run `scripts/generate_context.py` with that JSON to render the Markdown artifact. Run `scripts/extract-acceptance-context.py` and `scripts/analyze-test-coverage.py` to produce the evidence inputs for the two additional artifacts.
+
+The scripts require Python 3.9 or newer and a Git repository. They use Git only for repository facts and do not call GitHub, GitLab, or any remote API. Historical extraction and semantic deduplication remain model-driven; Python only validates, selects, and persists state.
\ No newline at end of file
diff --git a/pr-quality-assistant/skills/pr-code-review/references/acceptance-criteria.md b/pr-quality-assistant/skills/pr-code-review/references/acceptance-criteria.md
new file mode 100644
index 0000000..2abeef9
--- /dev/null
+++ b/pr-quality-assistant/skills/pr-code-review/references/acceptance-criteria.md
@@ -0,0 +1,13 @@
+# Acceptance Criteria
+
+Produce `acceptance-criteria.md` from the facts emitted by `extract-acceptance-context.py`.
+
+- Prefer explicit PR requirements and discussion over inferred behavior.
+- Use implementation and tests to clarify observable behavior, not to turn implementation details into requirements.
+- Never create a criterion solely because it sounds like good engineering practice.
+- Every criterion must be independently meaningful and verifiable.
+- Merge semantic duplicates while preserving distinct observable behaviors.
+- Include `Requirement`, `Evidence`, `Confidence`, and `Verification` for every criterion.
+- Mark unsupported intent as `Unknown / cannot determine` instead of inventing a criterion.
+
+Include a source-of-criteria section and cite paths, PR/change-request IDs, comments, or test names for every claim.
\ No newline at end of file
diff --git a/pr-quality-assistant/skills/pr-code-review/references/coverage-analysis.md b/pr-quality-assistant/skills/pr-code-review/references/coverage-analysis.md
new file mode 100644
index 0000000..9533495
--- /dev/null
+++ b/pr-quality-assistant/skills/pr-code-review/references/coverage-analysis.md
@@ -0,0 +1,14 @@
+# Coverage Analysis
+
+Produce `code-coverage-report.md` from the facts emitted by `analyze-test-coverage.py`.
+
+- Analyze changed behavior and execution paths, not changed lines alone.
+- Inspect existing tests before declaring coverage missing.
+- Identify meaningful success, boundary, and error scenarios for each behavioral area.
+- Use measured coverage files when available and label their evidence as measured.
+- Without measured data, label conclusions as change-based test sufficiency.
+- Never fabricate a global percentage or claim a test passed unless it was inspected or run.
+- Do not require tests for mechanical changes unless they affect behavior.
+- Do not recommend tests merely to increase line coverage.
+
+For each behavioral area, include the changed code, required scenarios, test evidence, status, finding, and recommendation. If intended behavior cannot be established from evidence, say `Unknown / cannot determine`.
\ No newline at end of file
diff --git a/pr-quality-assistant/skills/pr-code-review/references/data-collection-guidelines.md b/pr-quality-assistant/skills/pr-code-review/references/data-collection-guidelines.md
new file mode 100644
index 0000000..101de71
--- /dev/null
+++ b/pr-quality-assistant/skills/pr-code-review/references/data-collection-guidelines.md
@@ -0,0 +1,10 @@
+# Data Collection Guidelines
+
+The context collector records facts that can be traced to Git or the repository filesystem.
+
+- Use `base...source` for the change-focused comparison and record the merge base.
+- Keep raw diff text unchanged and place it last in the rendered artifact.
+- Record paths relative to the repository root where possible.
+- Treat instruction files as metadata; do not interpret or rewrite their rules during collection.
+- Identify tests without running them; execution belongs to a later review stage.
+- Fail before rendering when the repository, refs, or merge base cannot be resolved.
diff --git a/pr-quality-assistant/skills/pr-code-review/references/final-review.md b/pr-quality-assistant/skills/pr-code-review/references/final-review.md
new file mode 100644
index 0000000..a588089
--- /dev/null
+++ b/pr-quality-assistant/skills/pr-code-review/references/final-review.md
@@ -0,0 +1,39 @@
+# Final Review
+
+The final review is a deterministic evaluation over these evidence packages and the inspected source code:
+
+- `review/review-context.md`
+- `review/acceptance-criteria.md`
+- `review/code-coverage-report.md`
+- `pr-insights.json`
+- `.github/instructions/insights.instructions.md`
+- repository `AGENTS.md` and `.github/instructions/*`
+
+The reviewer first produces `review/review-assessment.json` using the contract below. `scripts/evaluate-review.py` applies `references/review-policy.json` without reinterpretation and writes `review/review-result.json`. `scripts/render-review-report.py` renders that result as `review/review-report.html`.
+
+## Five Gates
+
+1. **Coverage**: evaluate meaningful behavioral scenarios, using measured coverage only when available. A missing score is `UNCERTAIN`, never a pass. The default blocking threshold is 95 and is configurable.
+2. **Acceptance criteria**: evaluate every criterion independently as `PASS`, `FAIL`, `UNCERTAIN`, or `NOT_APPLICABLE`. Mandatory or high-confidence criteria must all pass.
+3. **Coding guidelines**: check repository, language, framework, dependency, database, security, testing, and shared-module rules.
+4. **Historical compliance**: identify whether the current change reintroduces a historical defect pattern, with explicit historical and current evidence.
+5. **AI-slop**: report only unnecessary complexity, risk, duplication, maintenance burden, or convention violations. Never flag code merely because it appears AI-generated.
+
+Any gate finding must include `id`, `gate`, `severity`, `issue`, `impact`, `evidence`, `reference`, and `recommendation`. A finding may be referenced by multiple gates, but duplicate underlying issues must share one `fingerprint` and be consolidated by the evaluator.
+
+## Assessment Input
+
+```json
+{
+  "pull_request": { "base": "main", "source": "dev/bug_fix" },
+  "gates": {
+    "coverage": { "status": "PASS", "score": 98, "covered": 20, "required": 20, "findings": [] },
+    "acceptance_criteria": { "status": "PASS", "passed": 2, "failed": 0, "uncertain": 0, "criteria": [], "findings": [] },
+    "coding_guidelines": { "status": "PASS", "passed": 10, "failed": 0, "findings": [] },
+    "historical_review": { "status": "PASS", "passed": 4, "failed": 0, "findings": [] },
+    "ai_slop": { "status": "PASS", "blocking_findings": 0, "major_findings": 0, "findings": [] }
+  }
+}
+```
+
+Statuses supplied by the reviewer are validated against the policy. `FAIL` and `UNCERTAIN` never become `PASS`. Overall approval requires every blocking gate to pass and no blocking-severity finding. The final result is structured first; HTML is presentation only.
\ No newline at end of file
diff --git a/pr-quality-assistant/skills/pr-code-review/references/insight-generation.md b/pr-quality-assistant/skills/pr-code-review/references/insight-generation.md
new file mode 100644
index 0000000..07c0e72
--- /dev/null
+++ b/pr-quality-assistant/skills/pr-code-review/references/insight-generation.md
@@ -0,0 +1,42 @@
+# Historical Insight Generation
+
+You are a senior engineer producing repository-specific code-review guidance from historical merged change requests. The context collector supplies the change requests and their review feedback; do not fetch from a provider yourself.
+
+Extract only generalizable, actionable coding rules. Ignore questions, clarification requests, one-off line-level nitpicks, and anything specific to one change request. Deduplicate comments that express the same underlying rule and keep the clearest wording. Never copy secrets, credentials, personal data, or irrelevant conversation into either output.
+
+For each rule, return this shape:
+
+```json
+{
+  "insights": [
+    {
+      "pattern": "...",
+      "category": "suggestion|defect_pattern|performance|security|testing|code_quality|database",
+      "language": "...",
+      "description": "...",
+      "module": "...",
+      "shared": false
+    }
+  ]
+}
+```
+
+Set `shared` to `true` and record `module` when the rule affects a shared or common module. Use `database` for schema, queries, migrations, transactions, or connection handling.
+
+Inspect the supplied repository manifests (`pom.xml`, `build.gradle`, `pyproject.toml`, `requirements.txt`, `Pipfile`, `package.json`, `go.mod`, `Cargo.toml`, and `*.csproj`) and enrich rules with detected language, framework, and package context. Check `AGENTS.md` and `.github/instructions/`; do not repeat guidance already covered there.
+
+Update `pr-insights.json` by semantically deduplicating new rules against existing insights. This file contains knowledge, not processing state. Update `.github/instructions/insights.instructions.md` with the following frontmatter and section order:
+
+```yaml
+---
+description: >
+  Code-review guidelines for this repository, derived from PR review history
+  and the detected language/tech stack. The review agent must follow these when
+  reviewing pull requests. Source rules: pr-insights.json.
+applyTo: "**"
+---
+```
+
+Sections, omitting empty rule sections: Source; Shared / Common Module Rules; Language & Package Guidelines; Dependency Health; Database; General Rules grouped by category; Regression. Dependency Health must require checking manifest dependencies for known CVEs and approaching end of life. Regression must require updated tests, preserved existing coverage, and intact behavior and public contracts.
+
+Only after both insight outputs are successfully written may the state manager mark the supplied change-request IDs as analyzed.
\ No newline at end of file
diff --git a/pr-quality-assistant/skills/pr-code-review/references/insight-schema.md b/pr-quality-assistant/skills/pr-code-review/references/insight-schema.md
new file mode 100644
index 0000000..90615f2
--- /dev/null
+++ b/pr-quality-assistant/skills/pr-code-review/references/insight-schema.md
@@ -0,0 +1,31 @@
+# Insight State and Data Schemas
+
+`pr-insights.json` stores distilled knowledge:
+
+```json
+{
+  "insights": [
+    {
+      "pattern": "...",
+      "category": "security",
+      "language": "python",
+      "description": "...",
+      "module": "...",
+      "shared": true,
+      "evidence": [{ "change_request_id": "101", "comment_hash": "..." }]
+    }
+  ]
+}
+```
+
+`.code-review/insights-state.json` stores processing state only:
+
+```json
+{
+  "base_ref": "main",
+  "last_analyzed_at": "2026-08-26T00:30:00Z",
+  "analyzed_change_requests": ["101", "102"]
+}
+```
+
+State is updated only after insight generation succeeds. Change-request IDs are strings so providers can use numeric PRs, GitLab MRs, or other stable identifiers consistently.
\ No newline at end of file
diff --git a/pr-quality-assistant/skills/pr-code-review/references/review-context-schema.md b/pr-quality-assistant/skills/pr-code-review/references/review-context-schema.md
new file mode 100644
index 0000000..70e802a
--- /dev/null
+++ b/pr-quality-assistant/skills/pr-code-review/references/review-context-schema.md
@@ -0,0 +1,22 @@
+# Review Context Schema
+
+The canonical internal object is `CodeReviewContext`; `review/review-context.md` is its human-readable rendering. The collector must preserve source facts and keep the raw diff last in the Markdown output.
+
+```json
+{
+  "repository": { "root": "...", "files": [], "manifests": [] },
+  "change": {
+    "base": "main",
+    "source": "dev/bug_fix",
+    "base_commit": "...",
+    "source_commit": "...",
+    "merge_base": "...",
+    "files": [],
+    "statistics": { "files_changed": 0, "insertions": 0, "deletions": 0 },
+    "diff": "..."
+  },
+  "history": { "commits": [] },
+  "instructions": { "files": [] },
+  "tests": { "manifests": [], "test_files": [], "changed_tests": [] }
+}
+```
\ No newline at end of file
diff --git a/pr-quality-assistant/skills/pr-code-review/references/review-policy.json b/pr-quality-assistant/skills/pr-code-review/references/review-policy.json
new file mode 100644
index 0000000..ac8c720
--- /dev/null
+++ b/pr-quality-assistant/skills/pr-code-review/references/review-policy.json
@@ -0,0 +1,28 @@
+{
+  "coverage": {
+    "threshold": 95,
+    "blocking": true
+  },
+  "acceptance_criteria": {
+    "required_pass_rate": 100,
+    "blocking": true
+  },
+  "coding_guidelines": {
+    "required_pass_rate": 100,
+    "blocking": true
+  },
+  "historical_review": {
+    "required_pass_rate": 100,
+    "blocking": true
+  },
+  "ai_slop": {
+    "max_blocking_findings": 0,
+    "max_major_findings": 0,
+    "blocking": true
+  },
+  "blocking_severities": [
+    "BLOCKER",
+    "CRITICAL",
+    "MAJOR"
+  ]
+}
\ No newline at end of file
diff --git a/pr-quality-assistant/skills/pr-code-review/scripts/analyze-test-coverage.py b/pr-quality-assistant/skills/pr-code-review/scripts/analyze-test-coverage.py
new file mode 100644
index 0000000..2368671
--- /dev/null
+++ b/pr-quality-assistant/skills/pr-code-review/scripts/analyze-test-coverage.py
@@ -0,0 +1,80 @@
+#!/usr/bin/env python3
+"""Collect deterministic, change-focused test and coverage facts."""
+
+from __future__ import annotations
+
+import argparse
+import json
+from pathlib import Path
+
+
+COVERAGE_FILES = {"coverage.xml", "coverage.json", "lcov.info", "jacoco.xml"}
+TEST_COMMAND_KEYS = {"pytest", "jest", "nyc", "test", "coverage", "go test", "dotnet test"}
+
+
+def discover_coverage_files(repository: Path) -> list[str]:
+    return sorted(
+        path.relative_to(repository).as_posix()
+        for path in repository.rglob("*")
+        if path.is_file() and (path.name in COVERAGE_FILES or path.name.endswith(".lcov"))
+    )
+
+
+def discover_test_commands(repository: Path, manifests: list[str]) -> list[dict]:
+    commands = []
+    for manifest in manifests:
+        path = repository / manifest
+        try:
+            text = path.read_text(encoding="utf-8", errors="replace")
+        except OSError:
+            continue
+        for line_number, line in enumerate(text.splitlines(), 1):
+            if any(key in line.lower() for key in TEST_COMMAND_KEYS):
+                commands.append({"manifest": manifest, "line": line_number, "text": line.strip()})
+    return commands
+
+
+def analyze(context: dict, repository: Path) -> dict:
+    changed_files = context["change"]["files"]
+    source_files = [item["path"] for item in changed_files if item["status"] not in {"added", "deleted"}]
+    changed_tests = context.get("tests", {}).get("changed_tests", [])
+    test_files = context.get("tests", {}).get("test_files", [])
+    coverage_files = discover_coverage_files(repository)
+    manifests = context.get("repository", {}).get("manifests", [])
+    return {
+        "scope": {
+            "base": context["change"]["base"],
+            "source": context["change"]["source"],
+            "changed_files": [item["path"] for item in changed_files],
+            "behavioral_candidates": source_files,
+        },
+        "tests": {
+            "all_test_files": test_files,
+            "changed_test_files": changed_tests,
+            "potentially_relevant_tests": [path for path in test_files if any(Path(source).stem in path for source in source_files)],
+        },
+        "coverage": {
+            "measured_report_files": coverage_files,
+            "measured_data_available": bool(coverage_files),
+            "note": "No numeric coverage claim is made by this collector.",
+        },
+        "test_commands": discover_test_commands(repository, manifests),
+    }
+
+
+def main() -> int:
+    parser = argparse.ArgumentParser(description=__doc__)
+    parser.add_argument("context", type=Path)
+    parser.add_argument("--repository", type=Path, default=Path("."))
+    parser.add_argument("--output", type=Path, required=True)
+    args = parser.parse_args()
+    context = json.loads(args.context.read_text(encoding="utf-8"))
+    repository = args.repository.resolve()
+    args.output.parent.mkdir(parents=True, exist_ok=True)
+    args.output.write_text(json.dumps(analyze(context, repository), indent=2) + "\n", encoding="utf-8")
+    print(args.output)
+    return 0
+
+
+if __name__ == "__main__":
+    raise SystemExit(main())
\ No newline at end of file
diff --git a/pr-quality-assistant/skills/pr-code-review/scripts/collect_context.py b/pr-quality-assistant/skills/pr-code-review/scripts/collect_context.py
new file mode 100644
index 0000000..4c78e31
--- /dev/null
+++ b/pr-quality-assistant/skills/pr-code-review/scripts/collect_context.py
@@ -0,0 +1,95 @@
+#!/usr/bin/env python3
+"""Build the complete CodeReviewContext from Git data and repository files."""
+
+from __future__ import annotations
+
+import argparse
+import json
+import sys
+from pathlib import Path
+
+from git_context import GitContextError, collect_context, resolve_repository
+
+
+INSTRUCTION_NAMES = {"AGENTS.md", "CONTRIBUTING.md", "README.md", "copilot-instructions.md"}
+MANIFEST_NAMES = {"pom.xml", "build.gradle", "pyproject.toml", "requirements.txt", "Pipfile", "package.json", "go.mod", "Cargo.toml"}
+TEST_DIRECTORY_NAMES = {"tests", "test", "__tests__"}
+TEST_SUFFIXES = ("_test.py", ".spec.ts", ".test.ts", ".spec.js", ".test.js")
+
+
+def relative_files(repository: Path) -> list[str]:
+    ignored = {".git", ".venv", "node_modules", "__pycache__"}
+    files = []
+    for path in repository.rglob("*"):
+        if path.is_file() and not ignored.intersection(path.parts):
+            files.append(path.relative_to(repository).as_posix())
+    return sorted(files)
+
+
+def collect_instructions(repository: Path) -> list[dict]:
+    instructions = []
+    for path in repository.rglob("*"):
+        if path.is_file() and path.name in INSTRUCTION_NAMES and ".git" not in path.parts:
+            relative = path.relative_to(repository).as_posix()
+            scope = "/" + str(path.parent.relative_to(repository)).replace(".", "")
+            instructions.append({"path": relative, "scope": scope or "/"})
+    for path in repository.glob(".github/instructions/*.instructions.md"):
+        instructions.append({"path": path.relative_to(repository).as_posix(), "scope": "/"})
+    return sorted({item["path"]: item for item in instructions}.values(), key=lambda item: item["path"])
+
+
+def collect_tests(repository: Path, changed_files: list[dict]) -> dict:
+    all_files = relative_files(repository)
+    test_files = [
+        path
+        for path in all_files
+        if any(part in TEST_DIRECTORY_NAMES for part in Path(path).parts)
+        or path.endswith(TEST_SUFFIXES)
+        or Path(path).name.startswith("test_")
+    ]
+    manifests = [path for path in all_files if Path(path).name in MANIFEST_NAMES or Path(path).suffix == ".csproj"]
+    changed_tests = [item["path"] for item in changed_files if item["path"] in test_files]
+    return {"manifests": manifests, "test_files": test_files, "changed_tests": changed_tests}
+
+
+def collect_full_context(repository: Path, base: str, source: str) -> dict:
+    context = collect_context(repository, base, source)
+    files = relative_files(repository)
+    context["repository"].update(
+        {
+            "files": files,
+            "manifests": [
+                path
+                for path in files
+                if Path(path).name in MANIFEST_NAMES or Path(path).suffix == ".csproj"
+            ],
+        }
+    )
+    context["instructions"] = {"files": collect_instructions(repository)}
+    context["tests"] = collect_tests(repository, context["change"]["files"])
+    return context
+
+
+def main() -> int:
+    parser = argparse.ArgumentParser(description=__doc__)
+    parser.add_argument("--base", required=True)
+    parser.add_argument("--source", required=True)
+    parser.add_argument("--repository", default=".")
+    parser.add_argument("--output", type=Path)
+    args = parser.parse_args()
+    try:
+        repository = resolve_repository(args.repository)
+        context = collect_full_context(repository, args.base, args.source)
+    except GitContextError as error:
+        print(f"Context collection failed.\n\nReason:\n{error}", file=sys.stderr)
+        return 1
+    rendered = json.dumps(context, indent=2)
+    if args.output:
+        args.output.write_text(rendered + "\n", encoding="utf-8")
+    else:
+        print(rendered)
+    return 0
+
+
+if __name__ == "__main__":
+    raise SystemExit(main())
\ No newline at end of file
diff --git a/pr-quality-assistant/skills/pr-code-review/scripts/discover-historical-prs.py b/pr-quality-assistant/skills/pr-code-review/scripts/discover-historical-prs.py
new file mode 100644
index 0000000..f9655e6
--- /dev/null
+++ b/pr-quality-assistant/skills/pr-code-review/scripts/discover-historical-prs.py
@@ -0,0 +1,48 @@
+#!/usr/bin/env python3
+"""Select merged change requests from provider-supplied JSON without API logic."""
+
+from __future__ import annotations
+
+import argparse
+import json
+import sys
+from pathlib import Path
+
+
+def discover(payload: dict, base_ref: str, analyzed: set[str], limit: int) -> dict:
+    requests = []
+    for item in payload.get("change_requests", []):
+        identifier = str(item.get("id", ""))
+        if not identifier or item.get("base_ref") != base_ref or item.get("merged") is not True:
+            continue
+        if identifier in analyzed:
+            continue
+        requests.append(item)
+    return {"base_ref": base_ref, "change_requests": requests[:limit]}
+
+
+def main() -> int:
+    parser = argparse.ArgumentParser(description=__doc__)
+    parser.add_argument("--base", required=True)
+    parser.add_argument("--state", type=Path, required=True)
+    parser.add_argument("--input", type=Path, required=True, help="Provider-neutral JSON input")
+    parser.add_argument("--limit", type=int, default=100)
+    args = parser.parse_args()
+    if args.limit < 1:
+        parser.error("--limit must be at least 1")
+    try:
+        state = json.loads(args.state.read_text(encoding="utf-8"))
+        payload = json.loads(args.input.read_text(encoding="utf-8"))
+        analyzed = set()
+        if state.get("base_ref") in {"", args.base}:
+            analyzed = {str(value) for value in state.get("analyzed_change_requests", [])}
+        result = discover(payload, args.base, analyzed, args.limit)
+    except (OSError, json.JSONDecodeError) as error:
+        print(f"Historical discovery failed: {error}", file=sys.stderr)
+        return 1
+    print(json.dumps(result, indent=2))
+    return 0
+
+
+if __name__ == "__main__":
+    raise SystemExit(main())
\ No newline at end of file
diff --git a/pr-quality-assistant/skills/pr-code-review/scripts/evaluate-review.py b/pr-quality-assistant/skills/pr-code-review/scripts/evaluate-review.py
new file mode 100644
index 0000000..a60af3d
--- /dev/null
+++ b/pr-quality-assistant/skills/pr-code-review/scripts/evaluate-review.py
@@ -0,0 +1,99 @@
+#!/usr/bin/env python3
+"""Apply deterministic approval gates to a structured review assessment."""
+
+from __future__ import annotations
+
+import argparse
+import hashlib
+import json
+from pathlib import Path
+
+
+GATES = ("coverage", "acceptance_criteria", "coding_guidelines", "historical_review", "ai_slop")
+VALID_STATUSES = {"PASS", "FAIL", "UNCERTAIN", "NOT_APPLICABLE"}
+
+
+def fingerprint(finding: dict) -> str:
+    value = finding.get("fingerprint") or "|".join(
+        str(finding.get(key, "")).strip().lower()
+        for key in ("issue", "impact", "evidence", "reference")
+    )
+    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]
+
+
+def consolidate_findings(gates: dict) -> list[dict]:
+    merged: dict[str, dict] = {}
+    for gate_name in GATES:
+        for finding in gates.get(gate_name, {}).get("findings", []):
+            item = dict(finding)
+            item["gate"] = item.get("gate", gate_name)
+            item["fingerprint"] = fingerprint(item)
+            if item["fingerprint"] in merged:
+                existing = merged[item["fingerprint"]]
+                existing["gates"] = sorted(set(existing.get("gates", [existing["gate"]]) + [item["gate"]]))
+                existing["references"] = sorted(set(existing.get("references", [existing.get("reference", "")]) + [item.get("reference", "")]))
+            else:
+                item["gates"] = [item["gate"]]
+                item["references"] = [item.get("reference", "")]
+                merged[item["fingerprint"]] = item
+    return sorted(merged.values(), key=lambda item: (item.get("severity", "INFO"), item["fingerprint"]))
+
+
+def gate_status(name: str, gate: dict, policy: dict) -> str:
+    status = str(gate.get("status", "UNCERTAIN")).upper()
+    if status not in VALID_STATUSES:
+        return "UNCERTAIN"
+    if name == "coverage" and status == "PASS" and gate.get("score") is None:
+        return "UNCERTAIN"
+    if name == "coverage" and policy[name].get("blocking") and gate.get("score") is not None:
+        if float(gate["score"]) < float(policy[name]["threshold"]):
+            return "FAIL"
+    if name == "acceptance_criteria" and policy[name].get("blocking"):
+        total = int(gate.get("passed", 0)) + int(gate.get("failed", 0)) + int(gate.get("uncertain", 0))
+        if total and (int(gate.get("failed", 0)) > 0 or int(gate.get("uncertain", 0)) > 0):
+            return "FAIL" if int(gate.get("failed", 0)) else "UNCERTAIN"
+    if name in {"coding_guidelines", "historical_review"} and policy[name].get("blocking"):
+        if int(gate.get("failed", 0)) > 0:
+            return "FAIL"
+    if name == "ai_slop" and policy[name].get("blocking"):
+        if int(gate.get("blocking_findings", 0)) > policy[name]["max_blocking_findings"] or int(gate.get("major_findings", 0)) > policy[name]["max_major_findings"]:
+            return "FAIL"
+    return status
+
+
+def evaluate(assessment: dict, policy: dict) -> dict:
+    gates = assessment.get("gates", {})
+    evaluated_gates = {}
+    for name in GATES:
+        source = dict(gates.get(name, {}))
+        source["status"] = gate_status(name, source, policy)
+        evaluated_gates[name] = source
+    findings = consolidate_findings(evaluated_gates)
+    blocking_severities = set(policy.get("blocking_severities", []))
+    blocking_findings = [item for item in findings if str(item.get("severity", "INFO")).upper() in blocking_severities]
+    gate_failure = any(gate["status"] in {"FAIL", "UNCERTAIN"} and policy[name].get("blocking", False) for name, gate in evaluated_gates.items())
+    return {
+        "status": "FAILED" if gate_failure or blocking_findings else "APPROVED",
+        "pull_request": assessment.get("pull_request", {}),
+        "gates": evaluated_gates,
+        "blocking_findings": blocking_findings,
+        "findings": findings,
+        "approval_policy": policy,
+    }
+
+
+def main() -> int:
+    parser = argparse.ArgumentParser(description=__doc__)
+    parser.add_argument("assessment", type=Path)
+    parser.add_argument("--policy", type=Path, required=True)
+    parser.add_argument("--output", type=Path, default=Path("review/review-result.json"))
+    args = parser.parse_args()
+    result = evaluate(json.loads(args.assessment.read_text(encoding="utf-8")), json.loads(args.policy.read_text(encoding="utf-8")))
+    args.output.parent.mkdir(parents=True, exist_ok=True)
+    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
+    print(args.output)
+    return 0
+
+
+if __name__ == "__main__":
+    raise SystemExit(main())
\ No newline at end of file
diff --git a/pr-quality-assistant/skills/pr-code-review/scripts/extract-acceptance-context.py b/pr-quality-assistant/skills/pr-code-review/scripts/extract-acceptance-context.py
new file mode 100644
index 0000000..8ee9c3a
--- /dev/null
+++ b/pr-quality-assistant/skills/pr-code-review/scripts/extract-acceptance-context.py
@@ -0,0 +1,80 @@
+#!/usr/bin/env python3
+"""Collect evidence sources for model-driven acceptance-criteria synthesis."""
+
+from __future__ import annotations
+
+import argparse
+import json
+from pathlib import Path
+
+
+def read_text(repository: Path, relative_path: str, limit: int = 12000) -> str:
+    try:
+        return (repository / relative_path).read_text(encoding="utf-8", errors="replace")[:limit]
+    except OSError:
+        return ""
+
+
+def extract(context: dict, repository: Path, provider_payload: dict | None) -> dict:
+    change = context["change"]
+    provider_requests = (provider_payload or {}).get("change_requests", [])
+    request_evidence = []
+    for request in provider_requests:
+        request_evidence.append(
+            {
+                "id": str(request.get("id", "")),
+                "title": request.get("title", ""),
+                "description": request.get("description", ""),
+                "comments": request.get("comments", []),
+                "reviews": request.get("reviews", []),
+            }
+        )
+    instruction_evidence = []
+    for item in context.get("instructions", {}).get("files", []):
+        content = read_text(repository, item["path"])
+        if content:
+            instruction_evidence.append({"path": item["path"], "scope": item["scope"], "content": content})
+    return {
+        "principle": "Do not create an acceptance criterion without evidence; mark insufficiently supported behavior as unknown.",
+        "source_priority": [
+            "PR description and discussion",
+            "linked issue or task",
+            "historical reviewer discussion",
+            "implementation and diff",
+            "existing tests",
+            "repository conventions",
+        ],
+        "change": {
+            "base": change["base"],
+            "source": change["source"],
+            "changed_files": change["files"],
+            "diff": change["diff"],
+        },
+        "provider_evidence": request_evidence,
+        "repository_instruction_evidence": instruction_evidence,
+        "existing_tests": context.get("tests", {}),
+        "synthesis_rules": {
+            "merge_semantic_duplicates": True,
+            "preserve_distinct_observable_behaviors": True,
+            "required_fields": ["requirement", "evidence", "verification", "confidence"],
+        },
+    }
+
+
+def main() -> int:
+    parser = argparse.ArgumentParser(description=__doc__)
+    parser.add_argument("context", type=Path)
+    parser.add_argument("--repository", type=Path, default=Path("."))
+    parser.add_argument("--provider-input", type=Path)
+    parser.add_argument("--output", type=Path, required=True)
+    args = parser.parse_args()
+    context = json.loads(args.context.read_text(encoding="utf-8"))
+    provider = json.loads(args.provider_input.read_text(encoding="utf-8")) if args.provider_input else None
+    args.output.parent.mkdir(parents=True, exist_ok=True)
+    args.output.write_text(json.dumps(extract(context, args.repository.resolve(), provider), indent=2) + "\n", encoding="utf-8")
+    print(args.output)
+    return 0
+
+
+if __name__ == "__main__":
+    raise SystemExit(main())
\ No newline at end of file
diff --git a/pr-quality-assistant/skills/pr-code-review/scripts/generate_context.py b/pr-quality-assistant/skills/pr-code-review/scripts/generate_context.py
new file mode 100644
index 0000000..0b016ef
--- /dev/null
+++ b/pr-quality-assistant/skills/pr-code-review/scripts/generate_context.py
@@ -0,0 +1,75 @@
+#!/usr/bin/env python3
+"""Render a CodeReviewContext JSON document as review/review-context.md."""
+
+from __future__ import annotations
+
+import argparse
+import json
+from pathlib import Path
+
+
+def inline(value: object) -> str:
+    return str(value).replace("`", "' ")
+
+
+def render(context: dict) -> str:
+    repository = context["repository"]
+    change = context["change"]
+    lines = [
+        "# Code Review Context",
+        "",
+        "## 1. Review Scope",
+        "",
+        f"- Base: `{inline(change['base'])}`",
+        f"- Source: `{inline(change['source'])}`",
+        f"- Merge Base: `{inline(change['merge_base'])}`",
+        "",
+        "## 2. Repository",
+        "",
+        f"- Root: `{inline(repository['root'])}`",
+        f"- Files discovered: {len(repository.get('files', []))}",
+        f"- Manifests: {', '.join(f'`{inline(path)}`' for path in repository.get('manifests', [])) or 'None found'}",
+        "",
+        "## 3. Change Statistics",
+        "",
+        f"- Files changed: {change.get('statistics', {}).get('files_changed', 0)}",
+        f"- Insertions: {change.get('statistics', {}).get('insertions', 0)}",
+        f"- Deletions: {change.get('statistics', {}).get('deletions', 0)}",
+        "",
+        "## 4. Changed Files",
+        "",
+    ]
+    lines.extend(f"- `{inline(item['path'])}` ({item['status']})" for item in change["files"])
+    if not change["files"]:
+        lines.append("- No changed files")
+    lines.extend(["", "## 5. Commit History", ""])
+    for commit in context.get("history", {}).get("commits", []):
+        lines.append(f"- `{commit['sha'][:12]}` {commit['subject']} ({commit['author']}, {commit['date']})")
+    if not context.get("history", {}).get("commits"):
+        lines.append("- No commits introduced by the source ref")
+    lines.extend(["", "## 6. Repository Instructions", ""])
+    for item in context.get("instructions", {}).get("files", []):
+        lines.append(f"- `{item['path']}` (scope `{item['scope']}`)")
+    if not context.get("instructions", {}).get("files"):
+        lines.append("- No instruction files found")
+    tests = context.get("tests", {})
+    lines.extend(["", "## 7. Tests", "", f"- Test files: {len(tests.get('test_files', []))}"])
+    lines.extend(f"- Changed test: `{path}`" for path in tests.get("changed_tests", []))
+    lines.extend(["", "## 8. Diff", "", "```diff", change.get("diff", ""), "```", ""])
+    return "\n".join(lines)
+
+
+def main() -> int:
+    parser = argparse.ArgumentParser(description=__doc__)
+    parser.add_argument("context", type=Path)
+    parser.add_argument("--output", type=Path, default=Path("review/review-context.md"))
+    args = parser.parse_args()
+    context = json.loads(args.context.read_text(encoding="utf-8"))
+    args.output.parent.mkdir(parents=True, exist_ok=True)
+    args.output.write_text(render(context), encoding="utf-8")
+    print(args.output)
+    return 0
+
+
+if __name__ == "__main__":
+    raise SystemExit(main())
\ No newline at end of file
diff --git a/pr-quality-assistant/skills/pr-code-review/scripts/git_context.py b/pr-quality-assistant/skills/pr-code-review/scripts/git_context.py
new file mode 100644
index 0000000..c02733a
--- /dev/null
+++ b/pr-quality-assistant/skills/pr-code-review/scripts/git_context.py
@@ -0,0 +1,143 @@
+#!/usr/bin/env python3
+"""Collect validated Git metadata for a base/source comparison."""
+
+from __future__ import annotations
+
+import argparse
+import json
+import re
+import subprocess
+import sys
+from pathlib import Path
+
+
+class GitContextError(RuntimeError):
+    """Raised when the repository or comparison cannot be resolved."""
+
+
+def run_git(repository: Path, *arguments: str) -> str:
+    result = subprocess.run(
+        ["git", "-C", str(repository), *arguments],
+        capture_output=True,
+        text=True,
+        check=False,
+    )
+    if result.returncode != 0:
+        detail = result.stderr.strip() or "git command failed"
+        raise GitContextError(detail)
+    return result.stdout
+
+
+def resolve_repository(path: str) -> Path:
+    candidate = Path(path).expanduser().resolve()
+    if not candidate.is_dir():
+        raise GitContextError(f"repository '{path}' does not exist")
+    try:
+        root = run_git(candidate, "rev-parse", "--show-toplevel").strip()
+    except GitContextError as error:
+        raise GitContextError(f"'{path}' is not a Git repository: {error}") from error
+    return Path(root).resolve()
+
+
+def collect_context(repository: Path, base: str, source: str) -> dict:
+    base_commit = run_git(repository, "rev-parse", "--verify", f"{base}^{{commit}}").strip()
+    source_commit = run_git(repository, "rev-parse", "--verify", f"{source}^{{commit}}").strip()
+    if base_commit == source_commit:
+        raise GitContextError("base and source refs resolve to the same commit")
+
+    merge_base = run_git(repository, "merge-base", base, source).strip()
+    if not merge_base:
+        raise GitContextError(f"unable to determine merge base between '{base}' and '{source}'")
+
+    name_status = run_git(repository, "diff", "--name-status", "-z", f"{base}...{source}")
+    files = []
+    entries = name_status.split("\0")
+    index = 0
+    while index < len(entries) - 1:
+        status = entries[index]
+        index += 1
+        if not status:
+            continue
+        paths_needed = 2 if status[0] in {"R", "C"} else 1
+        paths = entries[index : index + paths_needed]
+        index += paths_needed
+        if len(paths) == paths_needed and all(paths):
+            item = {"path": paths[-1], "status": status_name(status)}
+            if paths_needed == 2:
+                item["previous_path"] = paths[0]
+            files.append(item)
+
+    stat = run_git(repository, "diff", "--shortstat", f"{base}...{source}").strip()
+    statistics = parse_shortstat(stat)
+    commits = run_git(
+        repository,
+        "log",
+        "--format=%H%x1f%an%x1f%aI%x1f%s%x1f%b%x1e",
+        f"{base}..{source}",
+    )
+    history = []
+    for record in commits.split("\x1e"):
+        fields = record.strip("\n").split("\x1f")
+        if len(fields) >= 5 and fields[0]:
+            history.append(
+                {
+                    "sha": fields[0],
+                    "author": fields[1],
+                    "date": fields[2],
+                    "subject": fields[3],
+                    "body": fields[4].strip(),
+                }
+            )
+
+    return {
+        "repository": {"root": str(repository)},
+        "change": {
+            "base": base,
+            "source": source,
+            "base_commit": base_commit,
+            "source_commit": source_commit,
+            "merge_base": merge_base,
+            "files": files,
+            "statistics": statistics,
+            "diff": run_git(repository, "diff", f"{base}...{source}"),
+        },
+        "history": {"commits": history},
+    }
+
+
+def status_name(status: str) -> str:
+    mapping = {"A": "added", "D": "deleted", "M": "modified", "R": "renamed", "C": "copied"}
+    return mapping.get(status[0], status.lower())
+
+
+def parse_shortstat(stat: str) -> dict:
+    values = {"files_changed": 0, "insertions": 0, "deletions": 0}
+    patterns = {
+        "files_changed": r"(\d+) file(?:s)? changed",
+        "insertions": r"(\d+) insertion(?:s)?\(\+\)",
+        "deletions": r"(\d+) deletion(?:s)?\(-\)",
+    }
+    for key, pattern in patterns.items():
+        match = re.search(pattern, stat)
+        if match:
+            values[key] = int(match.group(1))
+    return values
+
+
+def main() -> int:
+    parser = argparse.ArgumentParser(description=__doc__)
+    parser.add_argument("--base", required=True)
+    parser.add_argument("--source", required=True)
+    parser.add_argument("--repository", default=".")
+    args = parser.parse_args()
+    try:
+        repository = resolve_repository(args.repository)
+        print(json.dumps(collect_context(repository, args.base, args.source), indent=2))
+    except GitContextError as error:
+        print(f"Context collection failed.\n\nReason:\n{error}", file=sys.stderr)
+        return 1
+    return 0
+
+
+if __name__ == "__main__":
+    raise SystemExit(main())
\ No newline at end of file
diff --git a/pr-quality-assistant/skills/pr-code-review/scripts/manage-insights-state.py b/pr-quality-assistant/skills/pr-code-review/scripts/manage-insights-state.py
new file mode 100644
index 0000000..c1aba82
--- /dev/null
+++ b/pr-quality-assistant/skills/pr-code-review/scripts/manage-insights-state.py
@@ -0,0 +1,46 @@
+#!/usr/bin/env python3
+"""Read or atomically update analyzed change-request state after successful generation."""
+
+from __future__ import annotations
+
+import argparse
+import json
+import sys
+from datetime import datetime, timezone
+from pathlib import Path
+
+
+def main() -> int:
+    parser = argparse.ArgumentParser(description=__doc__)
+    parser.add_argument("--state", type=Path, required=True)
+    parser.add_argument("--base", required=True)
+    parser.add_argument("--successful-ids", nargs="*", default=[])
+    parser.add_argument("--mark-success", action="store_true", help="Required to persist state")
+    args = parser.parse_args()
+    try:
+        current = json.loads(args.state.read_text(encoding="utf-8")) if args.state.exists() else {}
+        analyzed = set()
+        if current.get("base_ref") in {None, "", args.base}:
+            analyzed = {str(value) for value in current.get("analyzed_change_requests", [])}
+        requested = {str(value) for value in args.successful_ids if str(value)}
+        result = {
+            "base_ref": args.base,
+            "last_analyzed_at": current.get("last_analyzed_at", ""),
+            "analyzed_change_requests": sorted(analyzed),
+        }
+        if args.mark_success:
+            result["analyzed_change_requests"] = sorted(analyzed | requested)
+            result["last_analyzed_at"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
+            args.state.parent.mkdir(parents=True, exist_ok=True)
+            temporary = args.state.with_suffix(args.state.suffix + ".tmp")
+            temporary.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
+            temporary.replace(args.state)
+    except (OSError, json.JSONDecodeError) as error:
+        print(f"Insights state update failed: {error}", file=sys.stderr)
+        return 1
+    print(json.dumps(result, indent=2))
+    return 0
+
+
+if __name__ == "__main__":
+    raise SystemExit(main())
\ No newline at end of file
diff --git a/pr-quality-assistant/skills/pr-code-review/scripts/render-review-report.py b/pr-quality-assistant/skills/pr-code-review/scripts/render-review-report.py
new file mode 100644
index 0000000..356c77c
--- /dev/null
+++ b/pr-quality-assistant/skills/pr-code-review/scripts/render-review-report.py
@@ -0,0 +1,45 @@
+#!/usr/bin/env python3
+"""Render review-result.json as a self-contained HTML report."""
+
+from __future__ import annotations
+
+import argparse
+import html
+import json
+from pathlib import Path
+
+
+def render(result: dict) -> str:
+    status = html.escape(result.get("status", "FAILED"))
+    gates = result.get("gates", {})
+    gate_rows = "".join(
+        f"<tr><td>{html.escape(name.replace('_', ' ').title())}</td><td>{html.escape(str(gate.get('status', 'UNCERTAIN')))}</td></tr>"
+        for name, gate in gates.items()
+    )
+    issues = "".join(
+        f"<tr><td>{html.escape(item.get('id', item.get('fingerprint', '')))}</td><td>{html.escape(str(item.get('severity', 'INFO')))}</td><td>{html.escape(item.get('issue', ''))}</td><td>{html.escape(str(item.get('evidence', '')))}</td></tr>"
+        for item in result.get("findings", [])
+    ) or '<tr><td colspan="4">None</td></tr>'
+    return f"""<!doctype html>
+<html lang="en"><head><meta charset="utf-8"><title>PR Code Review</title>
+<style>body{{font:16px system-ui,sans-serif;max-width:960px;margin:2rem auto;padding:0 1rem;color:#202124}}h1{{border-bottom:2px solid #202124;padding-bottom:.5rem}}table{{border-collapse:collapse;width:100%;margin:1rem 0}}th,td{{border:1px solid #c8c8c8;padding:.6rem;text-align:left}}th{{background:#f2f2f2}}.status{{font-size:1.4rem;font-weight:700}}.APPROVED{{color:#176b36}}.FAILED{{color:#a12622}}</style></head>
+<body><h1>PR Code Review</h1><p class="status {status}">FINAL RESULT: {status}</p>
+<h2>Review Gates</h2><table><thead><tr><th>Gate</th><th>Status</th></tr></thead><tbody>{gate_rows}</tbody></table>
+<h2>Issues</h2><table><thead><tr><th>ID</th><th>Severity</th><th>Issue</th><th>Evidence</th></tr></thead><tbody>{issues}</tbody></table>
+<h2>Decision</h2><p>Approval requires every blocking gate to pass and no blocking-severity finding.</p></body></html>
+"""
+
+
+def main() -> int:
+    parser = argparse.ArgumentParser(description=__doc__)
+    parser.add_argument("result", type=Path)
+    parser.add_argument("--output", type=Path, default=Path("review/review-report.html"))
+    args = parser.parse_args()
+    args.output.parent.mkdir(parents=True, exist_ok=True)
+    args.output.write_text(render(json.loads(args.result.read_text(encoding="utf-8"))), encoding="utf-8")
+    print(args.output)
+    return 0
+
+
+if __name__ == "__main__":
+    raise SystemExit(main())
\ No newline at end of file
diff --git a/pr-quality-assistant/skills/quality-report/SKILL.md b/pr-quality-assistant/skills/quality-report/SKILL.md
deleted file mode 100644
index a02e363..0000000
--- a/pr-quality-assistant/skills/quality-report/SKILL.md
+++ /dev/null
@@ -1,40 +0,0 @@
----
-name: quality-report
-description: Aggregates outputs from requirement-analysis, change-blast-radius, test-analysis, and test-generation into an acceptance-criteria traceability matrix and a final PR quality report with a score and actionable recommendations. Use as the last step in the workflow.
----
-
-# Quality Assessment & Reporting
-
-## Purpose
-Synthesize every prior skill's output into a single, decision-ready report: did the PR meet its stated requirements, is the blast radius acceptable, is it adequately tested, and what should happen next.
-
-## Inputs
-- `requirements[]`, `acceptanceCriteria[]` from `requirement-analysis`
-- `affectedModules[]`, `riskTier`, `blastRadiusSummary` from `change-blast-radius`
-- `existingTestsMapped[]`, `acceptanceCriteriaCoverage[]`, `coverageGaps[]` from `test-analysis`
-- `generatedTests[]`, `skippedGaps[]` from `test-generation` (if invoked)
-
-## Steps
-1. **Build the traceability matrix**: for every `acceptanceCriteria` item, resolve final status as `passed` (test exists and covers it), `generated` (newly created test covers it), or `untested` (still a gap after generation, i.e., in `skippedGaps`).
-2. **Compute the quality score** using the rubric in `references/report-format.md` (weights: requirement clarity, blast radius risk, test coverage completeness, unresolved gaps).
-3. **Summarize risk**: restate `riskTier` and `blastRadiusSummary` in context of test coverage — e.g., high risk + full coverage is very different from high risk + gaps.
-4. **List actionable recommendations**, prioritized by severity (blocking gaps first, then warnings, then informational notes).
-5. **Render the final report** using the exact structure defined in `references/report-format.md` so output is consistent across PRs.
-
-## Output Contract
-A single markdown report (see `references/report-format.md` for required sections) plus a machine-readable summary:
-```json
-{
-  "qualityScore": 0,
-  "riskTier": "low|medium|high",
-  "traceabilityMatrix": [
-    { "acId": "AC-1", "status": "passed|generated|untested", "tests": ["..."] }
-  ],
-  "recommendations": [
-    { "priority": "blocking|warning|info", "description": "..." }
-  ]
-}
-```
-
-## Handoff
-This is the terminal skill in the workflow. The orchestrator returns this report to the user/PR. No further skill is invoked. (Reserved: a future hook could post this report as a PR comment automatically.)
diff --git a/pr-quality-assistant/skills/quality-report/references/report-format.md b/pr-quality-assistant/skills/quality-report/references/report-format.md
deleted file mode 100644
index 8276c66..0000000
--- a/pr-quality-assistant/skills/quality-report/references/report-format.md
+++ /dev/null
@@ -1,61 +0,0 @@
-# Quality Report Format
-
-## Required Report Structure
-
-```markdown
-# PR Quality Report — <PR title>
-
-## Summary
-<1-2 sentence overview: what the PR does, overall verdict>
-
-## Quality Score: <0-100> (<Tier: Excellent/Good/Needs Work/At Risk>)
-
-## Risk Assessment
-- **Blast Radius Risk Tier:** low | medium | high
-- **Blast Radius Summary:** <from change-blast-radius>
-- **Affected Modules:** <count, direct vs indirect>
-
-## Acceptance Criteria Traceability
-| AC ID | Description | Status | Test(s) |
-|---|---|---|---|
-| AC-1 | ... | ✅ Passed / 🆕 Generated / ⚠️ Untested | ... |
-
-## Test Coverage
-- Existing tests mapped: <count>
-- Gaps identified: <count> (blocking: <n>, warning: <n>)
-- Tests generated: <count>
-- Gaps still open (require human follow-up): <list with reasons>
-
-## Recommendations
-1. **[Blocking]** <description + suggested action>
-2. **[Warning]** <description + suggested action>
-3. **[Info]** <description>
-
-## Open Questions (from Requirement Analysis)
-- <any ambiguities flagged earlier that still need clarification>
-```
-
-## Quality Score Rubric
-Score starts at 100 and is reduced by weighted deductions:
-
-| Factor | Deduction |
-|---|---|
-| Each `blocking` coverage gap left open | -15 (max -45) |
-| Each `warning` coverage gap left open | -5 (max -20) |
-| Unresolved `openQuestions` from requirement-analysis | -10 each (max -20) |
-| `riskTier: high` with any open gap | additional -10 |
-| All acceptance criteria traced to passing/generated tests | +0 (baseline expectation, no bonus) |
-
-Floor the score at 0. Map to tiers:
-| Score | Tier |
-|---|---|
-| 90–100 | Excellent |
-| 75–89 | Good |
-| 50–74 | Needs Work |
-| 0–49 | At Risk |
-
-## Formatting Rules
-- Always use the exact section headers above so the report is diffable/parseable across PRs.
-- Use status emojis consistently (✅ / 🆕 / ⚠️) only in the traceability table, not elsewhere.
-- Keep the Summary to 1-2 sentences — details belong in their respective sections.
-- Never omit the Open Questions section, even if empty — write "None" explicitly.
diff --git a/pr-quality-assistant/skills/requirement-analysis/SKILL.md b/pr-quality-assistant/skills/requirement-analysis/SKILL.md
deleted file mode 100644
index 214fcdd..0000000
--- a/pr-quality-assistant/skills/requirement-analysis/SKILL.md
+++ /dev/null
@@ -1,37 +0,0 @@
----
-name: requirement-analysis
-description: Extracts structured requirements and acceptance criteria from a PR description, linked ticket, or user story. Use this skill first, before analyzing code changes, to establish what the PR is supposed to achieve.
----
-
-# Requirement Analysis
-
-## Purpose
-Parse the PR description, commit messages, and any linked issue/ticket to produce a structured, unambiguous set of requirements and acceptance criteria that later skills (blast radius, test analysis, quality report) can validate against.
-
-## Inputs
-- PR title and description
-- Linked ticket/story (if available) — id, description, acceptance criteria
-- Commit messages in the PR
-
-## Steps
-1. Read the PR description and linked ticket content.
-2. Identify explicit and implicit requirements (functional and non-functional).
-3. Extract or infer acceptance criteria. If the ticket already lists AC, normalize them into discrete, testable statements.
-4. Flag ambiguous or missing requirements as `openQuestions` rather than guessing.
-5. Classify each requirement as functional, non-functional (perf/security/a11y), or refactor/chore.
-
-## Output Contract
-```json
-{
-  "requirements": [
-    { "id": "REQ-1", "description": "...", "type": "functional|non-functional|chore" }
-  ],
-  "acceptanceCriteria": [
-    { "id": "AC-1", "description": "...", "linkedRequirement": "REQ-1" }
-  ],
-  "openQuestions": ["..."]
-}
-```
-
-## Handoff
-Pass `requirements[]` and `acceptanceCriteria[]` to `change-blast-radius` and later to `quality-report` for traceability. Surface `openQuestions[]` to the orchestrator immediately — do not proceed with assumptions.
diff --git a/pr-quality-assistant/skills/test-analysis/SKILL.md b/pr-quality-assistant/skills/test-analysis/SKILL.md
deleted file mode 100644
index a2f5046..0000000
--- a/pr-quality-assistant/skills/test-analysis/SKILL.md
+++ /dev/null
@@ -1,43 +0,0 @@
----
-name: test-analysis
-description: Evaluates existing test coverage against the changed code and acceptance criteria to identify coverage gaps. Use after change-blast-radius and before test-generation.
----
-
-# Test Analysis
-
-## Purpose
-Determine whether existing tests adequately cover the changed/affected code and the acceptance criteria established during requirement analysis, and produce a precise list of gaps.
-
-## Inputs
-- `changedFiles[]` and `affectedModules[]` from `change-blast-radius`
-- `riskTier` (determines strict vs. warn mode)
-- `acceptanceCriteria[]` from `requirement-analysis`
-- Existing test suite in the repository
-
-## Steps
-1. Locate existing tests associated with each changed file/module (by naming convention, imports, or coverage reports if available).
-2. Map each `acceptanceCriteria` item to zero or more existing tests.
-3. Identify gaps:
-   - Changed code with no associated test.
-   - Acceptance criteria with no test mapped to it.
-   - Edge cases implied by the change type (e.g., interface changes → contract tests) that aren't covered.
-4. In **strict mode** (`riskTier: high`), any gap is reported as blocking. In normal mode, gaps are reported as warnings.
-5. Do not modify or generate tests in this skill — only analyze and report. See `references/test-coverage-methodology.md` for detailed evaluation criteria.
-
-## Output Contract
-```json
-{
-  "existingTestsMapped": [
-    { "file": "...", "tests": ["..."] }
-  ],
-  "acceptanceCriteriaCoverage": [
-    { "acId": "AC-1", "covered": true, "tests": ["..."] }
-  ],
-  "coverageGaps": [
-    { "target": "file|AC-id", "reason": "...", "severity": "blocking|warning" }
-  ]
-}
-```
-
-## Handoff
-If `coverageGaps[]` is non-empty, the orchestrator invokes `test-generation`. Regardless, all outputs are passed to `quality-report` for the traceability matrix.
diff --git a/pr-quality-assistant/skills/test-analysis/references/test-coverage-methodology.md b/pr-quality-assistant/skills/test-analysis/references/test-coverage-methodology.md
deleted file mode 100644
index b61a104..0000000
--- a/pr-quality-assistant/skills/test-analysis/references/test-coverage-methodology.md
+++ /dev/null
@@ -1,37 +0,0 @@
-# Test Coverage Methodology
-
-## Goal
-Evaluate test adequacy in a way that is proportional to risk, rather than chasing raw coverage percentage.
-
-## Coverage Dimensions
-1. **Code coverage** — is the changed code path exercised by at least one test?
-2. **Behavioral coverage** — does a test assert on the *behavior* implied by the change, not just execute the line?
-3. **Acceptance criteria coverage** — does every AC from `requirement-analysis` map to at least one test that would fail if the AC were violated?
-4. **Edge case coverage** — for the change type identified in blast-radius analysis:
-   - Interface changes → contract/boundary tests (null, empty, type mismatches)
-   - Schema changes → migration/backward-compatibility tests
-   - Logic changes → happy path + at least one failure/error path
-   - Concurrency-sensitive code → race condition or idempotency checks where applicable
-
-## Mapping Tests to Changes
-- Prefer explicit traceability (test file naming conventions, `@covers`/`@requirement` style annotations, or coverage tool output) over inference.
-- When inferring, match by: same module/class under test, shared imports, or test descriptions referencing the changed behavior.
-- A test "covers" an AC only if its assertions would fail when that specific AC is violated — merely calling the function is not sufficient.
-
-## Gap Severity Rules
-| Condition | Severity |
-|---|---|
-| Changed logic file with zero associated tests, `riskTier: high` | blocking |
-| Acceptance criterion with no mapped test | blocking |
-| Changed logic file with zero associated tests, `riskTier: low/medium` | warning |
-| Missing edge case test (e.g., no error-path test) | warning |
-| Config/styling-only change with no tests | informational (not a gap) |
-
-## Reporting Gaps
-Each gap must include:
-- `target`: the file, module, or AC id affected
-- `reason`: plain-language explanation of what's missing
-- `severity`: `blocking` | `warning` | `informational`
-- `suggestedAction`: e.g., "add unit test for null input on `parseInvoice()`"
-
-This structured output feeds directly into `test-generation` (for blocking/warning gaps) and into the traceability matrix in `quality-report`.
diff --git a/pr-quality-assistant/skills/test-generation/SKILL.md b/pr-quality-assistant/skills/test-generation/SKILL.md
deleted file mode 100644
index 5ffb8a0..0000000
--- a/pr-quality-assistant/skills/test-generation/SKILL.md
+++ /dev/null
@@ -1,39 +0,0 @@
----
-name: test-generation
-description: Generates unit/integration test cases for identified coverage gaps, following the repository's existing testing framework and conventions. Invoked conditionally by the orchestrator only when test-analysis reports gaps.
----
-
-# Test Generation
-
-## Purpose
-Close the coverage gaps identified by `test-analysis` by generating well-formed, idiomatic tests that match the existing repository conventions — without inventing a new testing pattern for the project.
-
-## Inputs
-- `coverageGaps[]` from `test-analysis` (only `blocking` and `warning` severities are actioned by default)
-- Existing test files in the repository (for framework/style detection: e.g., Jest, PyTest, JUnit, Mocha)
-- Changed source files and their surrounding context
-
-## Steps
-1. Detect the testing framework and conventions already in use (assertion style, mocking library, file naming, folder structure, AAA/Given-When-Return pattern).
-2. For each actionable gap, generate a test that:
-   - Targets the specific `reason`/`suggestedAction` from the gap.
-   - Uses existing fixtures/mocks where available rather than duplicating setup.
-   - Follows the AAA (Arrange-Act-Assert) or repo's established pattern.
-3. For AC-level gaps, ensure the generated test explicitly ties back to the acceptance criterion (e.g., in the test description/name).
-4. If a gap cannot be safely closed without deeper domain knowledge (e.g., ambiguous business rule), do not fabricate assertions — mark it as `skipped` with a reason for human follow-up.
-5. Do not modify production/source code in this skill — tests only.
-
-## Output Contract
-```json
-{
-  "generatedTests": [
-    { "file": "...", "testName": "...", "targetGap": "...", "content": "..." }
-  ],
-  "skippedGaps": [
-    { "target": "...", "reason": "requires domain clarification" }
-  ]
-}
-```
-
-## Handoff
-Pass `generatedTests[]` and `skippedGaps[]` to `quality-report` for inclusion in the traceability matrix and final recommendations. `skippedGaps` should always surface as explicit action items in the report, never silently dropped.
diff --git a/pr-quality-assistant/skills/test-sufficiency/SKILL.md b/pr-quality-assistant/skills/test-sufficiency/SKILL.md
deleted file mode 100644
index afc3535..0000000
--- a/pr-quality-assistant/skills/test-sufficiency/SKILL.md
+++ /dev/null
@@ -1,29 +0,0 @@
----
-name: test-sufficiency
-description: Decides whether the test-analysis coverage gaps are acceptable, returning a boolean decision and rationale before test generation or final reporting.
----
-
-# Test Sufficiency
-
-## Purpose
-Make the workflow's "Tests sufficient?" decision explicit and repeatable. This skill evaluates the gap output from `test-analysis`; it does not generate tests or alter repository files.
-
-## Inputs
-- `coverageGaps[]` from `test-analysis`
-- `riskTier` and strictness from `change-blast-radius`
-- Repository testing conventions and any stated acceptance criteria
-
-## Steps
-1. Confirm that every reported gap has a target, reason, and severity.
-2. Return `sufficient: true` only when `coverageGaps[]` is empty.
-3. When gaps exist, return `sufficient: false` and explain whether they are blocking or warning-level, including the highest-priority gaps.
-
-## Output Contract
-```json
-{
-  "sufficient": true,
-  "rationale": "No coverage gaps were reported by test-analysis."
-}
-```
-
-When gaps exist, `sufficient` must be `false`; the rationale must identify the gaps and state whether `test-generation` should run.
\ No newline at end of file
diff --git a/review/review-context.md b/review/review-context.md
new file mode 100644
index 0000000..0c02d66
--- /dev/null
+++ b/review/review-context.md
@@ -0,0 +1,1724 @@
+# Code Review Context
+
+## 1. Review Scope
+
+- Base: `main`
+- Source: `dev/open-skills-plugin`
+- Merge Base: `a1c05c26d5d4d0af513cb7d5dea7f399eb4eabf0`
+
+## 2. Repository
+
+- Root: `/Users/arjunv/Downloads/review-agents`
+- Files discovered: 20
+- Manifests: None found
+
+## 3. Change Statistics
+
+- Files changed: 36
+- Insertions: 653
+- Deletions: 723
+
+## 4. Changed Files
+
+- `pr-quality-assistant/.code-review/insights-state.json` (added)
+- `pr-quality-assistant/AGENTS.md` (deleted)
+- `pr-quality-assistant/FLOW.md` (modified)
+- `pr-quality-assistant/README.md` (modified)
+- `pr-quality-assistant/agents/developer-code-review.agent.md` (deleted)
+- `pr-quality-assistant/agents/pr-quality-report.agent.md` (deleted)
+- `pr-quality-assistant/agents/pr-quality.agent.md` (deleted)
+- `pr-quality-assistant/agents/repo-intelligence.agent.md` (deleted)
+- `pr-quality-assistant/data/insights.instructions.md` (deleted)
+- `pr-quality-assistant/data/pr-insights.json` (deleted)
+- `pr-quality-assistant/hooks.json` (deleted)
+- `pr-quality-assistant/plugin.json` (modified)
+- `pr-quality-assistant/pr-insights.json` (added)
+- `pr-quality-assistant/skills/_shared/agent-skills-compatibility.md` (deleted)
+- `pr-quality-assistant/skills/_shared/analysis-phase.md` (deleted)
+- `pr-quality-assistant/skills/change-blast-radius/SKILL.md` (deleted)
+- `pr-quality-assistant/skills/change-blast-radius/references/blast-radius-methodology.md` (deleted)
+- `pr-quality-assistant/skills/insights-generator/SKILL.md` (deleted)
+- `pr-quality-assistant/skills/pr-code-review/SKILL.md` (added)
+- `pr-quality-assistant/skills/pr-code-review/references/data-collection-guidelines.md` (added)
+- `pr-quality-assistant/skills/pr-code-review/references/insight-generation.md` (added)
+- `pr-quality-assistant/skills/pr-code-review/references/insight-schema.md` (added)
+- `pr-quality-assistant/skills/pr-code-review/references/review-context-schema.md` (added)
+- `pr-quality-assistant/skills/pr-code-review/scripts/collect_context.py` (added)
+- `pr-quality-assistant/skills/pr-code-review/scripts/discover-historical-prs.py` (added)
+- `pr-quality-assistant/skills/pr-code-review/scripts/generate_context.py` (added)
+- `pr-quality-assistant/skills/pr-code-review/scripts/git_context.py` (added)
+- `pr-quality-assistant/skills/pr-code-review/scripts/manage-insights-state.py` (added)
+- `pr-quality-assistant/skills/quality-report/SKILL.md` (deleted)
+- `pr-quality-assistant/skills/quality-report/references/report-format.md` (deleted)
+- `pr-quality-assistant/skills/repo-intelligence/SKILL.md` (added)
+- `pr-quality-assistant/skills/requirement-analysis/SKILL.md` (deleted)
+- `pr-quality-assistant/skills/test-analysis/SKILL.md` (deleted)
+- `pr-quality-assistant/skills/test-analysis/references/test-coverage-methodology.md` (deleted)
+- `pr-quality-assistant/skills/test-generation/SKILL.md` (deleted)
+- `pr-quality-assistant/skills/test-sufficiency/SKILL.md` (deleted)
+
+## 5. Commit History
+
+- `2c97955da96b` Add incremental historical review intelligence (Arjun V, 2026-08-26T01:06:43+05:30)
+- `3825d22cf467` Add Git review context collection skill (Arjun V, 2026-08-26T00:36:26+05:30)
+- `008927553af9` insights removed (Arjun V, 2026-08-25T22:47:29+05:30)
+- `f76a46282e3f` Adopt open Agent Plugins skill standard (Arjun V, 2026-08-25T22:44:47+05:30)
+
+## 6. Repository Instructions
+
+- `pr-quality-assistant/README.md` (scope `/pr-quality-assistant`)
+
+## 7. Tests
+
+- Test files: 0
+
+## 8. Diff
+
+```diff
+diff --git a/pr-quality-assistant/.code-review/insights-state.json b/pr-quality-assistant/.code-review/insights-state.json
+new file mode 100644
+index 0000000..8d2dd23
+--- /dev/null
++++ b/pr-quality-assistant/.code-review/insights-state.json
+@@ -0,0 +1,5 @@
++{
++  "base_ref": "",
++  "last_analyzed_at": "",
++  "analyzed_change_requests": []
++}
+\ No newline at end of file
+diff --git a/pr-quality-assistant/AGENTS.md b/pr-quality-assistant/AGENTS.md
+deleted file mode 100644
+index 36248be..0000000
+--- a/pr-quality-assistant/AGENTS.md
++++ /dev/null
+@@ -1,27 +0,0 @@
+-# PR Quality Assistant
+-
+-This file is the host-neutral entrypoint for agents that support the Agent Skills specification. Discover the skills under `skills/` by reading each directory's `SKILL.md`; do not require `plugin.json`, `agents/*.agent.md`, or `hooks.json`.
+-
+-## Persona Flow
+-
+-For a pre-PR review or an at-PR quality report:
+-
+-1. Load `data/insights.instructions.md` when present.
+-2. Invoke `requirement-analysis` with the PR description, linked work item, and commits.
+-3. Invoke `change-blast-radius` with the diff and requirement output.
+-4. Invoke `test-analysis` with the change analysis output.
+-5. Invoke `test-sufficiency` with the test-analysis gap output.
+-6. If `sufficient` is false, invoke `test-generation`.
+-7. Invoke `quality-report` with all accumulated outputs.
+-
+-Keep the skill output contracts intact and surface open questions instead of guessing.
+-
+-## Repository Intelligence Flow
+-
+-When the host reports a merged PR, invoke `repo-intelligence`. It must verify the PR is merged, fetch and cleanse review comments, and invoke `insights-generator`. The generator deduplicates by PR ID and comment hash, then updates `data/pr-insights.json` and `data/insights.instructions.md` only when needed.
+-
+-Hosts without lifecycle hooks should connect their own merged-PR webhook or scheduled automation to `repo-intelligence`. Never treat a session-start prompt as a universal merge event.
+-
+-## Host Adapters
+-
+-The `skills/` directory and this file are the portable integration surface. `plugin.json`, `agents/*.agent.md`, and `hooks.json` are optional Copilot-style adapters and may be ignored by other hosts.
+\ No newline at end of file
+diff --git a/pr-quality-assistant/FLOW.md b/pr-quality-assistant/FLOW.md
+index dcd4d28..e306f52 100644
+--- a/pr-quality-assistant/FLOW.md
++++ b/pr-quality-assistant/FLOW.md
+@@ -1,58 +1,31 @@
+-# Agent and Skill Flow
++# Agent Skills Flow
+ 
+ ```mermaid
+ flowchart TD
+-    subgraph Personas[On-demand persona agents]
+-        D[developer-code-review.agent.md]
+-        R[pr-quality-report.agent.md]
+-        P[pr-quality.agent.md\nCopilot orchestration adapter]
+-    end
++    H[Agent Skills-compatible host] --> CR[code-review skill]
++    CR --> V[Validate repository and refs]
++    V --> MB[Calculate merge base]
++    MB --> C[Collect CodeReviewContext]
++    C --> GM[Git metadata]
++    C --> DF[Diff and changed files]
++    C --> RH[Commit history]
++    C --> RS[Repository structure]
++    C --> IT[Instructions and tests]
++    GM --> CT[Context JSON]
++    DF --> CT
++    RH --> CT
++    RS --> CT
++    IT --> CT
++    CT --> MD[review/review-context.md]
++
++    W[Merged PR webhook or scheduled job] --> RI[repo-intelligence]
++    RI --> IG[Review comment extraction and cleansing]
++    IG --> D[Deduplicate by PR ID + comment hash]
++    D --> J[pr-insights.json]
++    D --> I[.github/instructions/insights.instructions.md]
++    I -. loaded by .-> CR
++    J -. detailed provenance .-> CR
+ 
+-    I[data/insights.instructions.md]
+-    Q[requirement-analysis]
+-    B[change-blast-radius]
+-    T[test-analysis]
+-    S[test-sufficiency]
+-    G{Tests sufficient?}
+-    TG[test-generation]
+-    QR[quality-report]
+-
+-    D --> I
+-    R --> I
+-    P --> I
+-    D --> Q
+-    R --> Q
+-    P --> Q
+-    Q --> B --> T --> S --> G
+-    G -->|yes| QR
+-    G -->|no| TG --> QR
+-
+-    subgraph Intelligence[Merge-triggered repo intelligence]
+-        H[Host webhook, scheduled job, or Copilot session-start adapter]
+-        RI[repo-intelligence.agent.md]
+-        IG[insights-generator]
+-        JSON[data/pr-insights.json]
+-        INST[data/insights.instructions.md]
+-    end
+-
+-    H -->|merged PR only| RI --> IG
+-    IG -->|deduplicate by PR ID + comment hash| JSON
+-    IG -->|regenerate shared guidance| INST
+-    INST -. loaded by .-> D
+-    INST -. loaded by .-> R
+-    INST -. loaded by .-> P
+-
+-    subgraph Shared[Shared workflow references]
+-        AP[skills/_shared/analysis-phase.md]
+-        AC[skills/_shared/agent-skills-compatibility.md]
+-    end
+-
+-    AP -. defines order .-> Q
+-    AP -. defines order .-> B
+-    AP -. defines order .-> T
+-    AC -. host contract .-> D
+-    AC -. host contract .-> R
+-    AC -. host contract .-> RI
+ ```
+ 
+-The `skills/` directories and `AGENTS.md` are the portable Agent Skills integration surface. `plugin.json`, `agents/*.agent.md`, and `hooks.json` are optional host adapters.
+\ No newline at end of file
++The portable package surface is `plugin.json` plus the immediate skill directories under `skills/`. The Git-only collector produces review context; hosts decide how to expose skills and deliver merged-PR events.
+\ No newline at end of file
+diff --git a/pr-quality-assistant/README.md b/pr-quality-assistant/README.md
+index d1cb9f7..96d6506 100644
+--- a/pr-quality-assistant/README.md
++++ b/pr-quality-assistant/README.md
+@@ -1,29 +1,29 @@
+ # PR Quality Assistant
+ 
+-This package exposes two reusable Agent Skills flows. Start with [AGENTS.md](AGENTS.md); it is the host-neutral entrypoint. The Copilot files provide one optional host adapter; other Agent Skills-compatible agents can discover and invoke the skills directly.
++This package is an Agent Plugins v1.0 package containing one primary portable Agent Skill. Clients discover it from the fixed `skills/` directory; no custom agent or orchestration layer is required.
+ 
+-See [FLOW.md](FLOW.md) for the complete agent and skill flowchart.
++The `pr-code-review` skill first refreshes incremental historical intelligence, then collects Git-only context for a logical request such as `{ "base": "main", "source": "dev/bug_fix" }`. It creates a structured `CodeReviewContext` and renders `review/review-context.md` without reviewing code or calling a hosting API.
+ 
+-## On-demand persona flow
++See [FLOW.md](FLOW.md) for the complete skill flowchart.
+ 
+-The developer review and PR quality report personas load repository insights, then share one analysis sequence:
++## On-demand review flow
+ 
+-`requirements -> change and blast-radius -> test-analysis -> test-sufficiency`
++The `pr-code-review` skill provides the context handoff for developer-facing pre-PR review and PR-facing quality reporting:
++
++`historical intelligence -> validate refs -> collect current context -> review handoff`
+ 
+ When tests are insufficient, test generation runs before acceptance-criteria traceability and the final quality report.
+ 
+ ## Merge-triggered intelligence flow
+ 
+-On a merged PR event, the host invokes `repo-intelligence`. That agent fetches and cleanses review comments, then calls `insights-generator`, which deduplicates evidence by PR ID and comment hash and updates `data/pr-insights.json` plus `data/insights.instructions.md` when a new reusable rule is found.
++During the historical phase, the host supplies merged change requests and review feedback to the `repo-intelligence` workflow described in `skills/pr-code-review/references/insight-generation.md`. It deduplicates evidence by change-request ID and comment hash, and updates `pr-insights.json` plus `.github/instructions/insights.instructions.md` when a new reusable rule is found.
+ 
+-For Copilot, the valid session-start hook prompts `repo-intelligence` to check for newly merged PRs because the current Copilot hooks reference has no PR-merged event. Other compatible hosts should connect their native PR webhook or scheduled automation to the same agent. The agent's merge-status check keeps any adapter from recording unmerged PR feedback.
++The host supplies the change-request provider data through its webhook, scheduled job, or native lifecycle event. Hosts without lifecycle events may invoke discovery manually, but the workflow must verify merge status before writing either output.
+ 
+ ## Compatibility
+ 
+-Any host implementing the Agent Skills specification can use `AGENTS.md` and the directories under `skills/`; see `skills/_shared/agent-skills-compatibility.md` for the host contract. The Markdown persona agents, `plugin.json`, and `hooks.json` are optional adapters, while `data/` is the shared persistence format.
++Any Agent Plugins-compatible client can load this package. An Agent Skills-compatible client can consume the `pr-code-review/SKILL.md` file directly; the historical workflow is an internal phase, not a second exposed skill. The open standard controls package and skill discovery; each host controls user experience and event delivery.
+ 
+-## Documentation consulted
++## Standard
+ 
+-- [GitHub Copilot plugins](https://docs.github.com/en/copilot/concepts/agents/plugins) for the requested plugin conventions (the page was unavailable during validation).
+-- [GitHub Copilot hooks reference](https://docs.github.com/en/copilot/reference/hooks-configuration), especially **Hook configuration format** and **Hook events**.
+-- [Using hooks with GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/use-hooks) for the `version: 1` and `sessionStart` configuration examples.
+\ No newline at end of file
++This package follows [Agent Plugins Specification 1.0.0](https://github.com/agentplugins/agent-plugins-spec/blob/main/spec/1.0.0.md) and [Agent Skills Specification](https://agentskills.io/specification). The plugin manifest uses the canonical Agent Plugins schema; skills are discovered from `skills/<name>/SKILL.md`.
+\ No newline at end of file
+diff --git a/pr-quality-assistant/agents/developer-code-review.agent.md b/pr-quality-assistant/agents/developer-code-review.agent.md
+deleted file mode 100644
+index 8216d76..0000000
+--- a/pr-quality-assistant/agents/developer-code-review.agent.md
++++ /dev/null
+@@ -1,17 +0,0 @@
+----
+-name: developer-code-review
+-description: Performs an on-demand pre-PR developer review using repository requirements, blast-radius, test, and accumulated review insights to find actionable quality risks.
+-skills:
+-  - requirement-analysis
+-  - change-blast-radius
+-  - test-analysis
+-  - test-sufficiency
+-  - test-generation
+-  - quality-report
+----
+-
+-# Developer Code Review
+-
+-Load `data/insights.instructions.md` as additional repository context before invoking any skill. Treat it as auto-maintained guidance and use it to focus review attention, not to override the current PR evidence. For host-neutral discovery and invocation rules, follow `skills/_shared/agent-skills-compatibility.md`.
+-
+-Follow the shared sequence in `skills/_shared/analysis-phase.md`: requirement-analysis, change-blast-radius, then test-analysis. Invoke `test-sufficiency` explicitly with the test-analysis output. If it returns `sufficient: false`, invoke `test-generation` before the final `quality-report`; otherwise proceed directly to reporting. Surface open questions instead of guessing.
+\ No newline at end of file
+diff --git a/pr-quality-assistant/agents/pr-quality-report.agent.md b/pr-quality-assistant/agents/pr-quality-report.agent.md
+deleted file mode 100644
+index c5308d0..0000000
+--- a/pr-quality-assistant/agents/pr-quality-report.agent.md
++++ /dev/null
+@@ -1,17 +0,0 @@
+----
+-name: pr-quality-report
+-description: Produces an at-PR-time quality report by tracing requirements through change risk and test coverage, informed by accumulated repository review insights.
+-skills:
+-  - requirement-analysis
+-  - change-blast-radius
+-  - test-analysis
+-  - test-sufficiency
+-  - test-generation
+-  - quality-report
+----
+-
+-# PR Quality Report
+-
+-Load `data/insights.instructions.md` as additional repository context before invoking any skill. Apply relevant rules as review considerations and distinguish them from evidence in the current PR. For host-neutral discovery and invocation rules, follow `skills/_shared/agent-skills-compatibility.md`.
+-
+-Follow the shared sequence in `skills/_shared/analysis-phase.md`: requirement-analysis, change-blast-radius, then test-analysis. Invoke `test-sufficiency` explicitly with the test-analysis output. If it returns `sufficient: false`, invoke `test-generation` before `quality-report`; otherwise pass the analysis outputs directly to `quality-report`. Include unresolved requirements and gaps in the final report.
+\ No newline at end of file
+diff --git a/pr-quality-assistant/agents/pr-quality.agent.md b/pr-quality-assistant/agents/pr-quality.agent.md
+deleted file mode 100644
+index 7ff16c9..0000000
+--- a/pr-quality-assistant/agents/pr-quality.agent.md
++++ /dev/null
+@@ -1,58 +0,0 @@
+----
+-name: pr-quality-agent
+-description: Orchestrates end-to-end PR quality assessment by sequencing requirement analysis, change/blast-radius analysis, test analysis, conditional test generation, and final quality reporting.
+-skills:
+-  - requirement-analysis
+-  - change-blast-radius
+-  - test-analysis
+-  - test-generation
+-  - quality-report
+----
+-
+-# PR Quality Agent
+-
+-## Role
+-You are the orchestrator for PR Quality Assistance. You do not perform deep analysis yourself — you invoke the appropriate skill at each stage, pass structured context between them, and make sequencing/branching decisions based on their outputs.
+-
+-## Workflow
+-
+-```
+-Requirements → Change Analysis → Blast Radius → Test Analysis →
+-  Test Generation (conditional) → Acceptance Criteria / Test Traceability →
+-  Quality Assessment → Final Report
+-```
+-
+-### Stage 1 — Requirement Analysis
+-Invoke `requirement-analysis` with the PR description and any linked ticket/story context.
+-**Output contract:** `{ requirements[], acceptanceCriteria[], openQuestions[] }`
+-
+-### Stage 2 — Change & Blast Radius Analysis
+-Invoke `change-blast-radius` with the PR diff and Stage 1 output.
+-**Output contract:** `{ changedFiles[], affectedModules[], riskTier, blastRadiusSummary }`
+-
+-### Stage 3 — Test Analysis
+-Invoke `test-analysis` with Stage 2 output (changed files/modules) plus repository test suite location.
+-**Output contract:** `{ coverageGaps[], existingTestsMapped[], acceptanceCriteriaCoverage[] }`
+-
+-### Stage 4 — Test Generation (Conditional)
+-Invoke `test-generation` **only if** `coverageGaps` from Stage 3 is non-empty.
+-**Output contract:** `{ generatedTests[], skippedGaps[] (with reason) }`
+-
+-### Stage 5 — Acceptance Criteria / Test Traceability
+-Built into `quality-report`. Combine Stage 1 `acceptanceCriteria[]` with Stage 3/4 test mappings to produce a traceability matrix (AC → test(s) → pass/fail/untested).
+-
+-### Stage 6 — Quality Assessment & Reporting
+-Invoke `quality-report` with the aggregated outputs of all prior stages.
+-**Output contract:** final markdown report (see `quality-report/references/report-format.md`) including quality score, risk tier, traceability matrix, and actionable recommendations.
+-
+-## Branching Rules
+-- If `requirement-analysis` returns `openQuestions[]`, surface them to the user before proceeding — do not guess intent.
+-- If `riskTier` from Stage 2 is `high`, ensure `test-analysis` runs in strict mode (fail on any gap rather than warn).
+-- Skip Stage 4 only when Stage 3 reports zero gaps; otherwise always attempt generation before reporting.
+-
+-## Extension Points (future)
+-- **Hook — pre-report**: reserved for future MCP/hook integration to post the final report as an inline PR comment automatically. Not implemented in this version; `quality-report` currently returns markdown only.
+-- **Hook — post-test-generation**: reserved for future auto-commit of generated tests to a review branch.
+-
+-## Non-Goals
+-- This agent does not merge PRs, approve/reject them, or modify source code outside of generated test files.
+diff --git a/pr-quality-assistant/agents/repo-intelligence.agent.md b/pr-quality-assistant/agents/repo-intelligence.agent.md
+deleted file mode 100644
+index 061e207..0000000
+--- a/pr-quality-assistant/agents/repo-intelligence.agent.md
++++ /dev/null
+@@ -1,46 +0,0 @@
+----
+-name: repo-intelligence
+-description: Maintains repository review intelligence after a pull request is merged by extracting deduplicated patterns from its review comments and updating shared agent guidance.
+-skills:
+-  - insights-generator
+----
+-
+-# Repository Intelligence
+-
+-## Trigger
+-Run for a merged pull request. The host may invoke this agent from a webhook, scheduled job, native lifecycle event, or Copilot hook. Regardless of host, the agent must verify merge status before changing repository intelligence.
+-
+-## Workflow
+-1. Fetch the merged PR's review comments and metadata.
+-2. Cleanse secrets, personal data, and irrelevant conversational content.
+-3. Compare the normalized comments with `data/pr-insights.json` using PR ID plus comment hash as the idempotency key.
+-4. Invoke `insights-generator` with the historical PRs, comments, and existing insight files.
+-5. If feedback reveals a new reusable pattern, add or update its rule and regenerate `data/insights.instructions.md`.
+-6. If the pattern is already documented, record no duplicate rule or evidence and skip the update.
+-
+-Do not infer a rule from a one-off comment without actionable repository-wide guidance. Never store secrets or sensitive comment text in either data file.
+-
+-## Review-Comment Extraction Contract
+-
+-Ask the repository integration available in the host to fetch all review comments for the target repository. Extract only generalizable coding rules and pass them to `insights-generator` as structured data:
+-
+-```json
+-{
+-  "insights": [
+-    {
+-      "pattern": "...",
+-      "category": "suggestion|defect_pattern|performance|security|testing|code_quality|database",
+-      "language": "...",
+-      "description": "...",
+-      "module": "...",
+-      "shared": false
+-    }
+-  ]
+-}
+-```
+-
+-Ignore questions, clarification requests, one-off line-level nitpicks, and PR-specific observations. Merge comments expressing the same rule and keep the clearest wording. Mark rules affecting shared or common modules with `shared: true` and record the module. Use `database` for schema, query, migration, transaction, or connection-handling feedback.
+-
+-Inspect available manifests (`pom.xml`, `build.gradle`, `pyproject.toml`, `requirements.txt`, `Pipfile`, `package.json`, `go.mod`, `Cargo.toml`, and `*.csproj`) and pass detected language, framework, and package context to `insights-generator`. The generated guidance must also tell reviewers to check manifest dependencies for known CVEs and approaching end-of-life.
+-
+-The generated instructions must put shared-module rules first, then language/package guidance, dependency health, database rules, remaining category-grouped rules, and regression guidance. Regression guidance must require reviewing changed or added tests, preserving existing coverage, and protecting existing behavior and public contracts. Deduplicate against any `AGENTS.md` and existing instruction files before updating `data/insights.instructions.md`.
+\ No newline at end of file
+diff --git a/pr-quality-assistant/data/insights.instructions.md b/pr-quality-assistant/data/insights.instructions.md
+deleted file mode 100644
+index e7ed04f..0000000
+--- a/pr-quality-assistant/data/insights.instructions.md
++++ /dev/null
+@@ -1,19 +0,0 @@
+-# Repository Review Insights
+-
+-<!-- Auto-maintained by the repo-intelligence agent. Do not hand-edit below this marker. -->
+-
+-<!-- BEGIN GENERATED INSIGHTS -->
+-## Source
+-
+-Detailed rules live in `data/pr-insights.json`; this file summarizes them for review agents.
+-
+-## Dependency Health
+-
+-Check manifest dependencies for known CVEs and approaching end-of-life, and flag findings in review.
+-
+-## Regression
+-
+-Verify that changes add or update tests, preserve existing test coverage, and do not break existing behavior or public contracts.
+-
+-No repository-specific review rules have been recorded yet.
+-<!-- END GENERATED INSIGHTS -->
+\ No newline at end of file
+diff --git a/pr-quality-assistant/data/pr-insights.json b/pr-quality-assistant/data/pr-insights.json
+deleted file mode 100644
+index 7d00d1f..0000000
+--- a/pr-quality-assistant/data/pr-insights.json
++++ /dev/null
+@@ -1,3 +0,0 @@
+-{
+-  "rules": []
+-}
+\ No newline at end of file
+diff --git a/pr-quality-assistant/hooks.json b/pr-quality-assistant/hooks.json
+deleted file mode 100644
+index e6f652d..0000000
+--- a/pr-quality-assistant/hooks.json
++++ /dev/null
+@@ -1,12 +0,0 @@
+-{
+-  "version": 1,
+-  "_comment": "Optional Copilot adapter only. The current GitHub Copilot hooks reference, Hook events section, does not define a PR-merged event. This valid sessionStart prompt asks repo-intelligence to process newly merged PRs and verify merge status.",
+-  "hooks": {
+-    "sessionStart": [
+-      {
+-        "type": "prompt",
+-        "prompt": "Check whether any new pull requests have merged since the last repository-intelligence run. If so, invoke the repo-intelligence agent for each merged PR; otherwise take no action. Verify merge status before updating data files."
+-      }
+-    ]
+-  }
+-}
+\ No newline at end of file
+diff --git a/pr-quality-assistant/plugin.json b/pr-quality-assistant/plugin.json
+index aa26091..9812e8c 100644
+--- a/pr-quality-assistant/plugin.json
++++ b/pr-quality-assistant/plugin.json
+@@ -1,29 +1,12 @@
+ {
++  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
+   "name": "pr-quality-assistant",
+-  "version": "0.1.0",
+-  "description": "Agent Skills-compatible PR quality workflow with reusable review analysis, test sufficiency, quality reporting, and repository intelligence.",
+-  "publisher": "ps-health",
+-  "license": "UNLICENSED",
+-  "entry": {
+-    "agents": [
+-      "./agents/pr-quality.agent.md",
+-      "./agents/developer-code-review.agent.md",
+-      "./agents/pr-quality-report.agent.md",
+-      "./agents/repo-intelligence.agent.md"
+-    ],
+-    "skills": [
+-      "./skills/requirement-analysis",
+-      "./skills/change-blast-radius",
+-      "./skills/test-analysis",
+-      "./skills/test-generation",
+-      "./skills/quality-report",
+-      "./skills/test-sufficiency",
+-      "./skills/insights-generator"
+-    ],
+-    "hooks": [
+-      "./hooks.json"
+-    ]
++  "version": "0.2.0",
++  "description": "Portable Agent Skills for pull-request review, test sufficiency, quality reporting, and repository intelligence.",
++  "author": {
++    "name": "ps-health"
+   },
++  "license": "UNLICENSED",
+   "keywords": [
+     "pull-request",
+     "code-review",
+diff --git a/pr-quality-assistant/pr-insights.json b/pr-quality-assistant/pr-insights.json
+new file mode 100644
+index 0000000..79174e4
+--- /dev/null
++++ b/pr-quality-assistant/pr-insights.json
+@@ -0,0 +1,3 @@
++{
++  "insights": []
++}
+\ No newline at end of file
+diff --git a/pr-quality-assistant/skills/_shared/agent-skills-compatibility.md b/pr-quality-assistant/skills/_shared/agent-skills-compatibility.md
+deleted file mode 100644
+index bfc7d1d..0000000
+--- a/pr-quality-assistant/skills/_shared/agent-skills-compatibility.md
++++ /dev/null
+@@ -1,12 +0,0 @@
+-# Agent Skills Compatibility
+-
+-The directories under `skills/` are the portable integration surface. Any agent host that supports the Agent Skills format can discover a skill by its directory and `SKILL.md` file, then invoke it by the frontmatter `name`.
+-
+-Hosts should provide these inputs and preserve the documented output contracts. The shared workflow is:
+-
+-1. Load `data/insights.instructions.md` when it exists.
+-2. Run `requirement-analysis`, `change-blast-radius`, and `test-analysis` in that order.
+-3. Run `test-sufficiency` with the test-analysis output.
+-4. Run `test-generation` only when sufficiency is false, then run `quality-report`.
+-
+-The `agents/*.agent.md`, `plugin.json`, and `hooks.json` files are optional host adapters. A host without Copilot plugin or hook support can use the skills directly and invoke `repo-intelligence` from its own merged-PR webhook or scheduled automation. The intelligence agent must still verify merge status and write the same two data files.
+\ No newline at end of file
+diff --git a/pr-quality-assistant/skills/_shared/analysis-phase.md b/pr-quality-assistant/skills/_shared/analysis-phase.md
+deleted file mode 100644
+index 0af638d..0000000
+--- a/pr-quality-assistant/skills/_shared/analysis-phase.md
++++ /dev/null
+@@ -1,9 +0,0 @@
+-# Shared Analysis Phase
+-
+-Both PR-quality personas use this order and pass each output to the next skill:
+-
+-1. `requirement-analysis`: extract requirements, acceptance criteria, and open questions.
+-2. `change-blast-radius`: map changed and affected modules and assign a risk tier.
+-3. `test-analysis`: map tests to the requirements and report coverage gaps.
+-
+-Do not reorder or skip these stages. The `test-sufficiency` skill consumes the `test-analysis` gap output before any conditional test generation or reporting.
+\ No newline at end of file
+diff --git a/pr-quality-assistant/skills/change-blast-radius/SKILL.md b/pr-quality-assistant/skills/change-blast-radius/SKILL.md
+deleted file mode 100644
+index 6221eae..0000000
+--- a/pr-quality-assistant/skills/change-blast-radius/SKILL.md
++++ /dev/null
+@@ -1,38 +0,0 @@
+----
+-name: change-blast-radius
+-description: Analyzes the PR diff to identify changed files, dependent/affected modules, and an overall risk tier (blast radius). Use after requirement-analysis and before test-analysis.
+----
+-
+-# Change & Blast Radius Analysis
+-
+-## Purpose
+-Determine the full scope of impact of the code changes in the PR — not just the files touched, but everything that depends on them — and assign a risk tier to guide how strict downstream test analysis should be.
+-
+-## Inputs
+-- PR diff (changed files, added/removed/modified lines)
+-- Repository dependency graph (imports, module references, shared config)
+-- `requirements[]` from `requirement-analysis`
+-
+-## Steps
+-1. List all changed files and classify the type of change (logic, config, schema, styling, test-only).
+-2. Traverse direct and transitive dependents of changed files/modules.
+-3. Classify affected modules as `direct` or `indirect` impact.
+-4. Assign a `riskTier` (`low` | `medium` | `high`) per the methodology in `references/blast-radius-methodology.md`.
+-5. Summarize the blast radius in plain language for the final report.
+-
+-See `references/blast-radius-methodology.md` for detailed scoring rules and dependency traversal approach.
+-
+-## Output Contract
+-```json
+-{
+-  "changedFiles": ["path/to/file.ts"],
+-  "affectedModules": [
+-    { "module": "...", "impact": "direct|indirect" }
+-  ],
+-  "riskTier": "low|medium|high",
+-  "blastRadiusSummary": "..."
+-}
+-```
+-
+-## Handoff
+-Pass `changedFiles[]`, `affectedModules[]`, and `riskTier` to `test-analysis`. A `high` risk tier should cause the orchestrator to run test-analysis in strict mode.
+diff --git a/pr-quality-assistant/skills/change-blast-radius/references/blast-radius-methodology.md b/pr-quality-assistant/skills/change-blast-radius/references/blast-radius-methodology.md
+deleted file mode 100644
+index a314da1..0000000
+--- a/pr-quality-assistant/skills/change-blast-radius/references/blast-radius-methodology.md
++++ /dev/null
+@@ -1,42 +0,0 @@
+-# Blast Radius Methodology
+-
+-## Goal
+-Provide a repeatable, explainable method for quantifying how far the impact of a change can propagate through a codebase, so risk can be assessed objectively rather than by intuition.
+-
+-## Step 1 — Classify Changed Files
+-For each file in the diff, classify the change type:
+-| Change Type | Examples |
+-|---|---|
+-| Logic | function/method body changes |
+-| Interface | function signature, exported type, API contract changes |
+-| Schema | DB schema, GraphQL schema, config schema |
+-| Config | env vars, feature flags, build config |
+-| Styling | CSS/UI-only changes with no logic impact |
+-| Test-only | changes confined to test files |
+-
+-## Step 2 — Dependency Traversal
+-1. Build (or reuse) a dependency graph from static imports/references.
+-2. **Direct impact**: modules that directly import/reference a changed file or symbol.
+-3. **Indirect impact**: modules that depend on a direct-impact module (traverse up to 2 levels by default; deeper only if the change is an `Interface` or `Schema` type).
+-4. Stop traversal at natural boundaries (e.g., published package boundaries, microservice boundaries) but flag cross-boundary impacts as high-attention items.
+-
+-## Step 3 — Risk Tier Scoring
+-Score = weighted sum of:
+-- Change type weight: Interface/Schema = 3, Logic = 2, Config = 2, Styling = 1, Test-only = 0
+-- Number of direct-impact modules (capped contribution)
+-- Number of indirect-impact modules (capped contribution, lower weight than direct)
+-- Whether changed code sits on a critical path (auth, payments, data integrity) — apply a multiplier if so
+-
+-| Score Range | Risk Tier |
+-|---|---|
+-| 0–3 | low |
+-| 4–8 | medium |
+-| 9+ | high |
+-
+-## Step 4 — Summarize
+-Produce a human-readable summary, e.g.:
+-> "3 files changed (2 logic, 1 interface). 4 direct-impact modules, 7 indirect-impact modules across the `billing` domain. Risk tier: **high** due to interface change on a critical payment path."
+-
+-## Notes for Implementers
+-- Prefer static analysis tools available in-repo (e.g., `madge`, language-server references) over manual heuristics when possible.
+-- If no dependency graph tooling is available, fall back to grep-based reference search and clearly flag reduced confidence in the summary.
+diff --git a/pr-quality-assistant/skills/insights-generator/SKILL.md b/pr-quality-assistant/skills/insights-generator/SKILL.md
+deleted file mode 100644
+index 57a0364..0000000
+--- a/pr-quality-assistant/skills/insights-generator/SKILL.md
++++ /dev/null
+@@ -1,50 +0,0 @@
+----
+-name: insights-generator
+-description: Extracts reusable review patterns and rules from historical PR review comments, deduplicates them by PR ID and comment hash, and maintains the repository intelligence files.
+----
+-
+-# Insights Generator
+-
+-## Purpose
+-Turn review feedback into durable repository-specific guidance for the PR-quality personas. Treat review comments as input evidence, not as instructions to blindly copy.
+-
+-## Inputs
+-- Historical PR metadata, including a stable PR ID and merge status
+-- Review comments, including author, body, file/line location when available, and comment ID
+-- Existing `data/pr-insights.json` and `data/insights.instructions.md`
+-
+-## Process
+-1. Consider merged PRs and their review comments; cleanse secrets, credentials, personal data, and irrelevant conversational text.
+-2. Normalize each remaining comment and compute a stable hash from its PR ID, comment ID when available, location, and normalized body.
+-3. Compare `(prId, commentHash)` with recorded evidence. Re-running on the same PR must not add duplicate evidence or rules.
+-4. Group new comments into actionable recurring patterns. Add a rule only when the feedback identifies a reusable repository practice; otherwise retain the evidence without inventing a rule.
+-5. Write the updated structured result to `data/pr-insights.json`, preserving existing entries and provenance.
+-6. Inspect repository manifests for language, frameworks, and packages. Check `AGENTS.md` and existing instruction files before writing, and omit rules already covered there.
+-7. Regenerate `data/insights.instructions.md` from the current rules. Keep the generated file concise, actionable, and safe to load as agent context. Put shared-module rules first, followed by language/package guidance, dependency health, database rules, category-grouped general rules, and regression guidance.
+-
+-## Output Contract
+-`data/pr-insights.json` contains this shape:
+-
+-```json
+-{
+-  "rules": [
+-    {
+-      "id": "rule-...",
+-      "pattern": "...",
+-      "guidance": "...",
+-      "evidence": [{ "prId": 123, "commentHash": "..." }]
+-    }
+-  ]
+-}
+-```
+-
+-The skill reports changed rule IDs, skipped duplicate evidence, and any comments withheld during cleansing. It must be safe to run repeatedly and must not edit source code.
+-
+-## Rule Classification
+-
+-- Keep only generalizable, actionable rules; ignore questions, clarification requests, and one-off line-level nitpicks.
+-- Use categories `suggestion`, `defect_pattern`, `performance`, `security`, `testing`, `code_quality`, and `database`.
+-- Set `shared: true` and record `module` for shared or common modules.
+-- Use `database` for schema, queries, migrations, transactions, and connection handling.
+-- Include a dependency-health instruction to check known CVEs and approaching end-of-life dependencies.
+-- Include regression guidance to update or add tests, preserve existing coverage, and protect behavior and public contracts.
+\ No newline at end of file
+diff --git a/pr-quality-assistant/skills/pr-code-review/SKILL.md b/pr-quality-assistant/skills/pr-code-review/SKILL.md
+new file mode 100644
+index 0000000..c7536a9
+--- /dev/null
++++ b/pr-quality-assistant/skills/pr-code-review/SKILL.md
+@@ -0,0 +1,42 @@
++---
++name: pr-code-review
++description: Builds incremental historical review intelligence, collects Git repository context for a base/source comparison, and produces a traceable review-context.md artifact for later code review. Use with logical base and source refs for pre-PR or pull-request review.
++---
++
++# PR Code Review
++
++When invoked with the logical request `{ "base": "main", "source": "dev/bug_fix" }`, execute the phases below in order. Current-change context and historical knowledge are separate artifacts and must not be conflated.
++
++## Phase 1: Historical Intelligence
++
++1. Validate the repository and base ref before attempting discovery.
++2. Read `.code-review/insights-state.json`; if absent, treat historical knowledge as empty and bootstrap.
++3. Ask the host's change-request provider for merged change requests targeting the base ref. Git alone cannot supply PR/MR IDs, comments, reviewers, or approval history; do not add provider API logic to the scripts.
++4. Pass normalized provider JSON to `scripts/discover-historical-prs.py` with the state file and `--limit 100`. It returns only newly discovered, merged requests for the selected base. On a changed base ref, start a fresh analyzed set.
++5. For each returned request, provide its description, review comments, threads, and reviews to the model using `references/insight-generation.md`. Extract only generalizable, actionable rules; ignore questions and one-off or PR-specific feedback.
++6. Semantically deduplicate the extracted rules against the existing root `pr-insights.json`. Write knowledge to `pr-insights.json` and concise reviewer guidance to `.github/instructions/insights.instructions.md` in the required section order.
++7. Only after both outputs are successfully written, run `scripts/manage-insights-state.py --mark-success --base <base> --state .code-review/insights-state.json --successful-ids ...`. Never mark requests before successful generation.
++
++If no new requests are returned, preserve the existing insight files and state. Do not generate a historical raw-comments document.
++
++## Phase 2: Current Change Context
++
++1. Validate the repository, base ref, source ref, distinct commits, and merge base.
++2. Collect Git metadata, changed files, numeric diff statistics, complete raw diff, and introduced commit history.
++3. Collect repository structure, manifests, applicable instruction files, and test information.
++4. Build the canonical `CodeReviewContext` object with `scripts/collect_context.py`.
++5. Render `review/review-context.md` with `scripts/generate_context.py`. Keep the raw diff last.
++
++## Phase 3: Review Handoff
++
++The skill stops after context construction. A later review stage may read, in order, `.github/instructions/insights.instructions.md`, `pr-insights.json`, and `review/review-context.md`, then inspect source code and produce findings. This skill does not review code, generate findings, approve or reject changes, or call GitHub/GitLab APIs.
++
++Do not perform code review at this stage.
++
++Do not make approval decisions.
++
++## Logical Request and Implementation
++
++The client or launcher maps its command syntax to the logical request; the skill does not depend on a specific CLI. The provider maps its API response to the normalized input expected by `scripts/discover-historical-prs.py`. Run `scripts/collect_context.py` to produce the current-change context JSON, then run `scripts/generate_context.py` with that JSON to render the Markdown artifact.
++
++The scripts require Python 3.9 or newer and a Git repository. They use Git only for repository facts and do not call GitHub, GitLab, or any remote API. Historical extraction and semantic deduplication remain model-driven; Python only validates, selects, and persists state.
+\ No newline at end of file
+diff --git a/pr-quality-assistant/skills/pr-code-review/references/data-collection-guidelines.md b/pr-quality-assistant/skills/pr-code-review/references/data-collection-guidelines.md
+new file mode 100644
+index 0000000..101de71
+--- /dev/null
++++ b/pr-quality-assistant/skills/pr-code-review/references/data-collection-guidelines.md
+@@ -0,0 +1,10 @@
++# Data Collection Guidelines
++
++The context collector records facts that can be traced to Git or the repository filesystem.
++
++- Use `base...source` for the change-focused comparison and record the merge base.
++- Keep raw diff text unchanged and place it last in the rendered artifact.
++- Record paths relative to the repository root where possible.
++- Treat instruction files as metadata; do not interpret or rewrite their rules during collection.
++- Identify tests without running them; execution belongs to a later review stage.
++- Fail before rendering when the repository, refs, or merge base cannot be resolved.
+diff --git a/pr-quality-assistant/skills/pr-code-review/references/insight-generation.md b/pr-quality-assistant/skills/pr-code-review/references/insight-generation.md
+new file mode 100644
+index 0000000..07c0e72
+--- /dev/null
++++ b/pr-quality-assistant/skills/pr-code-review/references/insight-generation.md
+@@ -0,0 +1,42 @@
++# Historical Insight Generation
++
++You are a senior engineer producing repository-specific code-review guidance from historical merged change requests. The context collector supplies the change requests and their review feedback; do not fetch from a provider yourself.
++
++Extract only generalizable, actionable coding rules. Ignore questions, clarification requests, one-off line-level nitpicks, and anything specific to one change request. Deduplicate comments that express the same underlying rule and keep the clearest wording. Never copy secrets, credentials, personal data, or irrelevant conversation into either output.
++
++For each rule, return this shape:
++
++```json
++{
++  "insights": [
++    {
++      "pattern": "...",
++      "category": "suggestion|defect_pattern|performance|security|testing|code_quality|database",
++      "language": "...",
++      "description": "...",
++      "module": "...",
++      "shared": false
++    }
++  ]
++}
++```
++
++Set `shared` to `true` and record `module` when the rule affects a shared or common module. Use `database` for schema, queries, migrations, transactions, or connection handling.
++
++Inspect the supplied repository manifests (`pom.xml`, `build.gradle`, `pyproject.toml`, `requirements.txt`, `Pipfile`, `package.json`, `go.mod`, `Cargo.toml`, and `*.csproj`) and enrich rules with detected language, framework, and package context. Check `AGENTS.md` and `.github/instructions/`; do not repeat guidance already covered there.
++
++Update `pr-insights.json` by semantically deduplicating new rules against existing insights. This file contains knowledge, not processing state. Update `.github/instructions/insights.instructions.md` with the following frontmatter and section order:
++
++```yaml
++---
++description: >
++  Code-review guidelines for this repository, derived from PR review history
++  and the detected language/tech stack. The review agent must follow these when
++  reviewing pull requests. Source rules: pr-insights.json.
++applyTo: "**"
++---
++```
++
++Sections, omitting empty rule sections: Source; Shared / Common Module Rules; Language & Package Guidelines; Dependency Health; Database; General Rules grouped by category; Regression. Dependency Health must require checking manifest dependencies for known CVEs and approaching end of life. Regression must require updated tests, preserved existing coverage, and intact behavior and public contracts.
++
++Only after both insight outputs are successfully written may the state manager mark the supplied change-request IDs as analyzed.
+\ No newline at end of file
+diff --git a/pr-quality-assistant/skills/pr-code-review/references/insight-schema.md b/pr-quality-assistant/skills/pr-code-review/references/insight-schema.md
+new file mode 100644
+index 0000000..90615f2
+--- /dev/null
++++ b/pr-quality-assistant/skills/pr-code-review/references/insight-schema.md
+@@ -0,0 +1,31 @@
++# Insight State and Data Schemas
++
++`pr-insights.json` stores distilled knowledge:
++
++```json
++{
++  "insights": [
++    {
++      "pattern": "...",
++      "category": "security",
++      "language": "python",
++      "description": "...",
++      "module": "...",
++      "shared": true,
++      "evidence": [{ "change_request_id": "101", "comment_hash": "..." }]
++    }
++  ]
++}
++```
++
++`.code-review/insights-state.json` stores processing state only:
++
++```json
++{
++  "base_ref": "main",
++  "last_analyzed_at": "2026-08-26T00:30:00Z",
++  "analyzed_change_requests": ["101", "102"]
++}
++```
++
++State is updated only after insight generation succeeds. Change-request IDs are strings so providers can use numeric PRs, GitLab MRs, or other stable identifiers consistently.
+\ No newline at end of file
+diff --git a/pr-quality-assistant/skills/pr-code-review/references/review-context-schema.md b/pr-quality-assistant/skills/pr-code-review/references/review-context-schema.md
+new file mode 100644
+index 0000000..70e802a
+--- /dev/null
++++ b/pr-quality-assistant/skills/pr-code-review/references/review-context-schema.md
+@@ -0,0 +1,22 @@
++# Review Context Schema
++
++The canonical internal object is `CodeReviewContext`; `review/review-context.md` is its human-readable rendering. The collector must preserve source facts and keep the raw diff last in the Markdown output.
++
++```json
++{
++  "repository": { "root": "...", "files": [], "manifests": [] },
++  "change": {
++    "base": "main",
++    "source": "dev/bug_fix",
++    "base_commit": "...",
++    "source_commit": "...",
++    "merge_base": "...",
++    "files": [],
++    "statistics": { "files_changed": 0, "insertions": 0, "deletions": 0 },
++    "diff": "..."
++  },
++  "history": { "commits": [] },
++  "instructions": { "files": [] },
++  "tests": { "manifests": [], "test_files": [], "changed_tests": [] }
++}
++```
+\ No newline at end of file
+diff --git a/pr-quality-assistant/skills/pr-code-review/scripts/collect_context.py b/pr-quality-assistant/skills/pr-code-review/scripts/collect_context.py
+new file mode 100644
+index 0000000..4c78e31
+--- /dev/null
++++ b/pr-quality-assistant/skills/pr-code-review/scripts/collect_context.py
+@@ -0,0 +1,95 @@
++#!/usr/bin/env python3
++"""Build the complete CodeReviewContext from Git data and repository files."""
++
++from __future__ import annotations
++
++import argparse
++import json
++import sys
++from pathlib import Path
++
++from git_context import GitContextError, collect_context, resolve_repository
++
++
++INSTRUCTION_NAMES = {"AGENTS.md", "CONTRIBUTING.md", "README.md", "copilot-instructions.md"}
++MANIFEST_NAMES = {"pom.xml", "build.gradle", "pyproject.toml", "requirements.txt", "Pipfile", "package.json", "go.mod", "Cargo.toml"}
++TEST_DIRECTORY_NAMES = {"tests", "test", "__tests__"}
++TEST_SUFFIXES = ("_test.py", ".spec.ts", ".test.ts", ".spec.js", ".test.js")
++
++
++def relative_files(repository: Path) -> list[str]:
++    ignored = {".git", ".venv", "node_modules", "__pycache__"}
++    files = []
++    for path in repository.rglob("*"):
++        if path.is_file() and not ignored.intersection(path.parts):
++            files.append(path.relative_to(repository).as_posix())
++    return sorted(files)
++
++
++def collect_instructions(repository: Path) -> list[dict]:
++    instructions = []
++    for path in repository.rglob("*"):
++        if path.is_file() and path.name in INSTRUCTION_NAMES and ".git" not in path.parts:
++            relative = path.relative_to(repository).as_posix()
++            scope = "/" + str(path.parent.relative_to(repository)).replace(".", "")
++            instructions.append({"path": relative, "scope": scope or "/"})
++    for path in repository.glob(".github/instructions/*.instructions.md"):
++        instructions.append({"path": path.relative_to(repository).as_posix(), "scope": "/"})
++    return sorted({item["path"]: item for item in instructions}.values(), key=lambda item: item["path"])
++
++
++def collect_tests(repository: Path, changed_files: list[dict]) -> dict:
++    all_files = relative_files(repository)
++    test_files = [
++        path
++        for path in all_files
++        if any(part in TEST_DIRECTORY_NAMES for part in Path(path).parts)
++        or path.endswith(TEST_SUFFIXES)
++        or Path(path).name.startswith("test_")
++    ]
++    manifests = [path for path in all_files if Path(path).name in MANIFEST_NAMES or Path(path).suffix == ".csproj"]
++    changed_tests = [item["path"] for item in changed_files if item["path"] in test_files]
++    return {"manifests": manifests, "test_files": test_files, "changed_tests": changed_tests}
++
++
++def collect_full_context(repository: Path, base: str, source: str) -> dict:
++    context = collect_context(repository, base, source)
++    files = relative_files(repository)
++    context["repository"].update(
++        {
++            "files": files,
++            "manifests": [
++                path
++                for path in files
++                if Path(path).name in MANIFEST_NAMES or Path(path).suffix == ".csproj"
++            ],
++        }
++    )
++    context["instructions"] = {"files": collect_instructions(repository)}
++    context["tests"] = collect_tests(repository, context["change"]["files"])
++    return context
++
++
++def main() -> int:
++    parser = argparse.ArgumentParser(description=__doc__)
++    parser.add_argument("--base", required=True)
++    parser.add_argument("--source", required=True)
++    parser.add_argument("--repository", default=".")
++    parser.add_argument("--output", type=Path)
++    args = parser.parse_args()
++    try:
++        repository = resolve_repository(args.repository)
++        context = collect_full_context(repository, args.base, args.source)
++    except GitContextError as error:
++        print(f"Context collection failed.\n\nReason:\n{error}", file=sys.stderr)
++        return 1
++    rendered = json.dumps(context, indent=2)
++    if args.output:
++        args.output.write_text(rendered + "\n", encoding="utf-8")
++    else:
++        print(rendered)
++    return 0
++
++
++if __name__ == "__main__":
++    raise SystemExit(main())
+\ No newline at end of file
+diff --git a/pr-quality-assistant/skills/pr-code-review/scripts/discover-historical-prs.py b/pr-quality-assistant/skills/pr-code-review/scripts/discover-historical-prs.py
+new file mode 100644
+index 0000000..f9655e6
+--- /dev/null
++++ b/pr-quality-assistant/skills/pr-code-review/scripts/discover-historical-prs.py
+@@ -0,0 +1,48 @@
++#!/usr/bin/env python3
++"""Select merged change requests from provider-supplied JSON without API logic."""
++
++from __future__ import annotations
++
++import argparse
++import json
++import sys
++from pathlib import Path
++
++
++def discover(payload: dict, base_ref: str, analyzed: set[str], limit: int) -> dict:
++    requests = []
++    for item in payload.get("change_requests", []):
++        identifier = str(item.get("id", ""))
++        if not identifier or item.get("base_ref") != base_ref or item.get("merged") is not True:
++            continue
++        if identifier in analyzed:
++            continue
++        requests.append(item)
++    return {"base_ref": base_ref, "change_requests": requests[:limit]}
++
++
++def main() -> int:
++    parser = argparse.ArgumentParser(description=__doc__)
++    parser.add_argument("--base", required=True)
++    parser.add_argument("--state", type=Path, required=True)
++    parser.add_argument("--input", type=Path, required=True, help="Provider-neutral JSON input")
++    parser.add_argument("--limit", type=int, default=100)
++    args = parser.parse_args()
++    if args.limit < 1:
++        parser.error("--limit must be at least 1")
++    try:
++        state = json.loads(args.state.read_text(encoding="utf-8"))
++        payload = json.loads(args.input.read_text(encoding="utf-8"))
++        analyzed = set()
++        if state.get("base_ref") in {"", args.base}:
++            analyzed = {str(value) for value in state.get("analyzed_change_requests", [])}
++        result = discover(payload, args.base, analyzed, args.limit)
++    except (OSError, json.JSONDecodeError) as error:
++        print(f"Historical discovery failed: {error}", file=sys.stderr)
++        return 1
++    print(json.dumps(result, indent=2))
++    return 0
++
++
++if __name__ == "__main__":
++    raise SystemExit(main())
+\ No newline at end of file
+diff --git a/pr-quality-assistant/skills/pr-code-review/scripts/generate_context.py b/pr-quality-assistant/skills/pr-code-review/scripts/generate_context.py
+new file mode 100644
+index 0000000..0b016ef
+--- /dev/null
++++ b/pr-quality-assistant/skills/pr-code-review/scripts/generate_context.py
+@@ -0,0 +1,75 @@
++#!/usr/bin/env python3
++"""Render a CodeReviewContext JSON document as review/review-context.md."""
++
++from __future__ import annotations
++
++import argparse
++import json
++from pathlib import Path
++
++
++def inline(value: object) -> str:
++    return str(value).replace("`", "' ")
++
++
++def render(context: dict) -> str:
++    repository = context["repository"]
++    change = context["change"]
++    lines = [
++        "# Code Review Context",
++        "",
++        "## 1. Review Scope",
++        "",
++        f"- Base: `{inline(change['base'])}`",
++        f"- Source: `{inline(change['source'])}`",
++        f"- Merge Base: `{inline(change['merge_base'])}`",
++        "",
++        "## 2. Repository",
++        "",
++        f"- Root: `{inline(repository['root'])}`",
++        f"- Files discovered: {len(repository.get('files', []))}",
++        f"- Manifests: {', '.join(f'`{inline(path)}`' for path in repository.get('manifests', [])) or 'None found'}",
++        "",
++        "## 3. Change Statistics",
++        "",
++        f"- Files changed: {change.get('statistics', {}).get('files_changed', 0)}",
++        f"- Insertions: {change.get('statistics', {}).get('insertions', 0)}",
++        f"- Deletions: {change.get('statistics', {}).get('deletions', 0)}",
++        "",
++        "## 4. Changed Files",
++        "",
++    ]
++    lines.extend(f"- `{inline(item['path'])}` ({item['status']})" for item in change["files"])
++    if not change["files"]:
++        lines.append("- No changed files")
++    lines.extend(["", "## 5. Commit History", ""])
++    for commit in context.get("history", {}).get("commits", []):
++        lines.append(f"- `{commit['sha'][:12]}` {commit['subject']} ({commit['author']}, {commit['date']})")
++    if not context.get("history", {}).get("commits"):
++        lines.append("- No commits introduced by the source ref")
++    lines.extend(["", "## 6. Repository Instructions", ""])
++    for item in context.get("instructions", {}).get("files", []):
++        lines.append(f"- `{item['path']}` (scope `{item['scope']}`)")
++    if not context.get("instructions", {}).get("files"):
++        lines.append("- No instruction files found")
++    tests = context.get("tests", {})
++    lines.extend(["", "## 7. Tests", "", f"- Test files: {len(tests.get('test_files', []))}"])
++    lines.extend(f"- Changed test: `{path}`" for path in tests.get("changed_tests", []))
++    lines.extend(["", "## 8. Diff", "", "```diff", change.get("diff", ""), "```", ""])
++    return "\n".join(lines)
++
++
++def main() -> int:
++    parser = argparse.ArgumentParser(description=__doc__)
++    parser.add_argument("context", type=Path)
++    parser.add_argument("--output", type=Path, default=Path("review/review-context.md"))
++    args = parser.parse_args()
++    context = json.loads(args.context.read_text(encoding="utf-8"))
++    args.output.parent.mkdir(parents=True, exist_ok=True)
++    args.output.write_text(render(context), encoding="utf-8")
++    print(args.output)
++    return 0
++
++
++if __name__ == "__main__":
++    raise SystemExit(main())
+\ No newline at end of file
+diff --git a/pr-quality-assistant/skills/pr-code-review/scripts/git_context.py b/pr-quality-assistant/skills/pr-code-review/scripts/git_context.py
+new file mode 100644
+index 0000000..c02733a
+--- /dev/null
++++ b/pr-quality-assistant/skills/pr-code-review/scripts/git_context.py
+@@ -0,0 +1,143 @@
++#!/usr/bin/env python3
++"""Collect validated Git metadata for a base/source comparison."""
++
++from __future__ import annotations
++
++import argparse
++import json
++import re
++import subprocess
++import sys
++from pathlib import Path
++
++
++class GitContextError(RuntimeError):
++    """Raised when the repository or comparison cannot be resolved."""
++
++
++def run_git(repository: Path, *arguments: str) -> str:
++    result = subprocess.run(
++        ["git", "-C", str(repository), *arguments],
++        capture_output=True,
++        text=True,
++        check=False,
++    )
++    if result.returncode != 0:
++        detail = result.stderr.strip() or "git command failed"
++        raise GitContextError(detail)
++    return result.stdout
++
++
++def resolve_repository(path: str) -> Path:
++    candidate = Path(path).expanduser().resolve()
++    if not candidate.is_dir():
++        raise GitContextError(f"repository '{path}' does not exist")
++    try:
++        root = run_git(candidate, "rev-parse", "--show-toplevel").strip()
++    except GitContextError as error:
++        raise GitContextError(f"'{path}' is not a Git repository: {error}") from error
++    return Path(root).resolve()
++
++
++def collect_context(repository: Path, base: str, source: str) -> dict:
++    base_commit = run_git(repository, "rev-parse", "--verify", f"{base}^{{commit}}").strip()
++    source_commit = run_git(repository, "rev-parse", "--verify", f"{source}^{{commit}}").strip()
++    if base_commit == source_commit:
++        raise GitContextError("base and source refs resolve to the same commit")
++
++    merge_base = run_git(repository, "merge-base", base, source).strip()
++    if not merge_base:
++        raise GitContextError(f"unable to determine merge base between '{base}' and '{source}'")
++
++    name_status = run_git(repository, "diff", "--name-status", "-z", f"{base}...{source}")
++    files = []
++    entries = name_status.split("\0")
++    index = 0
++    while index < len(entries) - 1:
++        status = entries[index]
++        index += 1
++        if not status:
++            continue
++        paths_needed = 2 if status[0] in {"R", "C"} else 1
++        paths = entries[index : index + paths_needed]
++        index += paths_needed
++        if len(paths) == paths_needed and all(paths):
++            item = {"path": paths[-1], "status": status_name(status)}
++            if paths_needed == 2:
++                item["previous_path"] = paths[0]
++            files.append(item)
++
++    stat = run_git(repository, "diff", "--shortstat", f"{base}...{source}").strip()
++    statistics = parse_shortstat(stat)
++    commits = run_git(
++        repository,
++        "log",
++        "--format=%H%x1f%an%x1f%aI%x1f%s%x1f%b%x1e",
++        f"{base}..{source}",
++    )
++    history = []
++    for record in commits.split("\x1e"):
++        fields = record.strip("\n").split("\x1f")
++        if len(fields) >= 5 and fields[0]:
++            history.append(
++                {
++                    "sha": fields[0],
++                    "author": fields[1],
++                    "date": fields[2],
++                    "subject": fields[3],
++                    "body": fields[4].strip(),
++                }
++            )
++
++    return {
++        "repository": {"root": str(repository)},
++        "change": {
++            "base": base,
++            "source": source,
++            "base_commit": base_commit,
++            "source_commit": source_commit,
++            "merge_base": merge_base,
++            "files": files,
++            "statistics": statistics,
++            "diff": run_git(repository, "diff", f"{base}...{source}"),
++        },
++        "history": {"commits": history},
++    }
++
++
++def status_name(status: str) -> str:
++    mapping = {"A": "added", "D": "deleted", "M": "modified", "R": "renamed", "C": "copied"}
++    return mapping.get(status[0], status.lower())
++
++
++def parse_shortstat(stat: str) -> dict:
++    values = {"files_changed": 0, "insertions": 0, "deletions": 0}
++    patterns = {
++        "files_changed": r"(\d+) file(?:s)? changed",
++        "insertions": r"(\d+) insertion(?:s)?\(\+\)",
++        "deletions": r"(\d+) deletion(?:s)?\(-\)",
++    }
++    for key, pattern in patterns.items():
++        match = re.search(pattern, stat)
++        if match:
++            values[key] = int(match.group(1))
++    return values
++
++
++def main() -> int:
++    parser = argparse.ArgumentParser(description=__doc__)
++    parser.add_argument("--base", required=True)
++    parser.add_argument("--source", required=True)
++    parser.add_argument("--repository", default=".")
++    args = parser.parse_args()
++    try:
++        repository = resolve_repository(args.repository)
++        print(json.dumps(collect_context(repository, args.base, args.source), indent=2))
++    except GitContextError as error:
++        print(f"Context collection failed.\n\nReason:\n{error}", file=sys.stderr)
++        return 1
++    return 0
++
++
++if __name__ == "__main__":
++    raise SystemExit(main())
+\ No newline at end of file
+diff --git a/pr-quality-assistant/skills/pr-code-review/scripts/manage-insights-state.py b/pr-quality-assistant/skills/pr-code-review/scripts/manage-insights-state.py
+new file mode 100644
+index 0000000..c1aba82
+--- /dev/null
++++ b/pr-quality-assistant/skills/pr-code-review/scripts/manage-insights-state.py
+@@ -0,0 +1,46 @@
++#!/usr/bin/env python3
++"""Read or atomically update analyzed change-request state after successful generation."""
++
++from __future__ import annotations
++
++import argparse
++import json
++import sys
++from datetime import datetime, timezone
++from pathlib import Path
++
++
++def main() -> int:
++    parser = argparse.ArgumentParser(description=__doc__)
++    parser.add_argument("--state", type=Path, required=True)
++    parser.add_argument("--base", required=True)
++    parser.add_argument("--successful-ids", nargs="*", default=[])
++    parser.add_argument("--mark-success", action="store_true", help="Required to persist state")
++    args = parser.parse_args()
++    try:
++        current = json.loads(args.state.read_text(encoding="utf-8")) if args.state.exists() else {}
++        analyzed = set()
++        if current.get("base_ref") in {None, "", args.base}:
++            analyzed = {str(value) for value in current.get("analyzed_change_requests", [])}
++        requested = {str(value) for value in args.successful_ids if str(value)}
++        result = {
++            "base_ref": args.base,
++            "last_analyzed_at": current.get("last_analyzed_at", ""),
++            "analyzed_change_requests": sorted(analyzed),
++        }
++        if args.mark_success:
++            result["analyzed_change_requests"] = sorted(analyzed | requested)
++            result["last_analyzed_at"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
++            args.state.parent.mkdir(parents=True, exist_ok=True)
++            temporary = args.state.with_suffix(args.state.suffix + ".tmp")
++            temporary.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
++            temporary.replace(args.state)
++    except (OSError, json.JSONDecodeError) as error:
++        print(f"Insights state update failed: {error}", file=sys.stderr)
++        return 1
++    print(json.dumps(result, indent=2))
++    return 0
++
++
++if __name__ == "__main__":
++    raise SystemExit(main())
+\ No newline at end of file
+diff --git a/pr-quality-assistant/skills/quality-report/SKILL.md b/pr-quality-assistant/skills/quality-report/SKILL.md
+deleted file mode 100644
+index a02e363..0000000
+--- a/pr-quality-assistant/skills/quality-report/SKILL.md
++++ /dev/null
+@@ -1,40 +0,0 @@
+----
+-name: quality-report
+-description: Aggregates outputs from requirement-analysis, change-blast-radius, test-analysis, and test-generation into an acceptance-criteria traceability matrix and a final PR quality report with a score and actionable recommendations. Use as the last step in the workflow.
+----
+-
+-# Quality Assessment & Reporting
+-
+-## Purpose
+-Synthesize every prior skill's output into a single, decision-ready report: did the PR meet its stated requirements, is the blast radius acceptable, is it adequately tested, and what should happen next.
+-
+-## Inputs
+-- `requirements[]`, `acceptanceCriteria[]` from `requirement-analysis`
+-- `affectedModules[]`, `riskTier`, `blastRadiusSummary` from `change-blast-radius`
+-- `existingTestsMapped[]`, `acceptanceCriteriaCoverage[]`, `coverageGaps[]` from `test-analysis`
+-- `generatedTests[]`, `skippedGaps[]` from `test-generation` (if invoked)
+-
+-## Steps
+-1. **Build the traceability matrix**: for every `acceptanceCriteria` item, resolve final status as `passed` (test exists and covers it), `generated` (newly created test covers it), or `untested` (still a gap after generation, i.e., in `skippedGaps`).
+-2. **Compute the quality score** using the rubric in `references/report-format.md` (weights: requirement clarity, blast radius risk, test coverage completeness, unresolved gaps).
+-3. **Summarize risk**: restate `riskTier` and `blastRadiusSummary` in context of test coverage — e.g., high risk + full coverage is very different from high risk + gaps.
+-4. **List actionable recommendations**, prioritized by severity (blocking gaps first, then warnings, then informational notes).
+-5. **Render the final report** using the exact structure defined in `references/report-format.md` so output is consistent across PRs.
+-
+-## Output Contract
+-A single markdown report (see `references/report-format.md` for required sections) plus a machine-readable summary:
+-```json
+-{
+-  "qualityScore": 0,
+-  "riskTier": "low|medium|high",
+-  "traceabilityMatrix": [
+-    { "acId": "AC-1", "status": "passed|generated|untested", "tests": ["..."] }
+-  ],
+-  "recommendations": [
+-    { "priority": "blocking|warning|info", "description": "..." }
+-  ]
+-}
+-```
+-
+-## Handoff
+-This is the terminal skill in the workflow. The orchestrator returns this report to the user/PR. No further skill is invoked. (Reserved: a future hook could post this report as a PR comment automatically.)
+diff --git a/pr-quality-assistant/skills/quality-report/references/report-format.md b/pr-quality-assistant/skills/quality-report/references/report-format.md
+deleted file mode 100644
+index 8276c66..0000000
+--- a/pr-quality-assistant/skills/quality-report/references/report-format.md
++++ /dev/null
+@@ -1,61 +0,0 @@
+-# Quality Report Format
+-
+-## Required Report Structure
+-
+-```markdown
+-# PR Quality Report — <PR title>
+-
+-## Summary
+-<1-2 sentence overview: what the PR does, overall verdict>
+-
+-## Quality Score: <0-100> (<Tier: Excellent/Good/Needs Work/At Risk>)
+-
+-## Risk Assessment
+-- **Blast Radius Risk Tier:** low | medium | high
+-- **Blast Radius Summary:** <from change-blast-radius>
+-- **Affected Modules:** <count, direct vs indirect>
+-
+-## Acceptance Criteria Traceability
+-| AC ID | Description | Status | Test(s) |
+-|---|---|---|---|
+-| AC-1 | ... | ✅ Passed / 🆕 Generated / ⚠️ Untested | ... |
+-
+-## Test Coverage
+-- Existing tests mapped: <count>
+-- Gaps identified: <count> (blocking: <n>, warning: <n>)
+-- Tests generated: <count>
+-- Gaps still open (require human follow-up): <list with reasons>
+-
+-## Recommendations
+-1. **[Blocking]** <description + suggested action>
+-2. **[Warning]** <description + suggested action>
+-3. **[Info]** <description>
+-
+-## Open Questions (from Requirement Analysis)
+-- <any ambiguities flagged earlier that still need clarification>
+-```
+-
+-## Quality Score Rubric
+-Score starts at 100 and is reduced by weighted deductions:
+-
+-| Factor | Deduction |
+-|---|---|
+-| Each `blocking` coverage gap left open | -15 (max -45) |
+-| Each `warning` coverage gap left open | -5 (max -20) |
+-| Unresolved `openQuestions` from requirement-analysis | -10 each (max -20) |
+-| `riskTier: high` with any open gap | additional -10 |
+-| All acceptance criteria traced to passing/generated tests | +0 (baseline expectation, no bonus) |
+-
+-Floor the score at 0. Map to tiers:
+-| Score | Tier |
+-|---|---|
+-| 90–100 | Excellent |
+-| 75–89 | Good |
+-| 50–74 | Needs Work |
+-| 0–49 | At Risk |
+-
+-## Formatting Rules
+-- Always use the exact section headers above so the report is diffable/parseable across PRs.
+-- Use status emojis consistently (✅ / 🆕 / ⚠️) only in the traceability table, not elsewhere.
+-- Keep the Summary to 1-2 sentences — details belong in their respective sections.
+-- Never omit the Open Questions section, even if empty — write "None" explicitly.
+diff --git a/pr-quality-assistant/skills/repo-intelligence/SKILL.md b/pr-quality-assistant/skills/repo-intelligence/SKILL.md
+new file mode 100644
+index 0000000..aebdf73
+--- /dev/null
++++ b/pr-quality-assistant/skills/repo-intelligence/SKILL.md
+@@ -0,0 +1,48 @@
++---
++name: repo-intelligence
++description: Builds repository-specific code-review guidance from merged pull-request review comments, manifests, and existing instructions. Use after a PR merges or when refreshing historical review insights.
++---
++
++# Repository Intelligence
++
++Run this skill from a merged-PR webhook, scheduled job, or host-native event. A host without lifecycle events may invoke it manually, but the skill must verify the target PR is merged before writing either output.
++
++## Outputs
++
++1. `pr-insights.json`: raw, deduplicated, generalizable coding rules.
++2. `.github/instructions/insights.instructions.md`: short reviewer instructions that summarize and reference `pr-insights.json`.
++
++## Process
++
++1. Fetch all review comments through the host's repository integration. Do not assume a particular tool name or MCP server.
++2. Extract only actionable, generalizable rules. Ignore questions, clarification requests, one-off line-level nitpicks, and PR-specific observations.
++3. Cleanse secrets, credentials, personal data, and irrelevant conversational text.
++4. Detect language, frameworks, and packages from available manifests including `pom.xml`, `build.gradle`, `pyproject.toml`, `requirements.txt`, `Pipfile`, `package.json`, `go.mod`, `Cargo.toml`, and `*.csproj`.
++5. Normalize comments and deduplicate by stable PR ID plus comment hash. Merge comments expressing the same rule and retain the clearest wording.
++6. Mark shared or common-module rules with `shared: true` and record `module`. Use categories `suggestion`, `defect_pattern`, `performance`, `security`, `testing`, `code_quality`, and `database`.
++7. Check `AGENTS.md` and existing `.github/instructions/` files. Do not repeat guidance already covered there.
++8. Write only the two output files. Do not generate scripts, modify source code, or embed credentials.
++
++## JSON Contract
++
++```json
++{
++  "insights": [
++    {
++      "pattern": "...",
++      "category": "suggestion",
++      "language": "...",
++      "description": "...",
++      "module": "...",
++      "shared": false,
++      "evidence": [{ "prId": 123, "commentHash": "..." }]
++    }
++  ]
++}
++```
++
++Re-running the same PR must not duplicate evidence or rules.
++
++## Instructions File
++
++Write `.github/instructions/insights.instructions.md` with `description` and `applyTo: "**"` frontmatter. Keep it short and use these sections in order: Source; Shared / Common Module Rules; Language & Package Guidelines; Dependency Health; Database; General Rules; Regression. Dependency Health must require checking known CVEs and approaching end of life. Regression must require updated tests, preserved coverage, and intact behavior and public contracts.
+\ No newline at end of file
+diff --git a/pr-quality-assistant/skills/requirement-analysis/SKILL.md b/pr-quality-assistant/skills/requirement-analysis/SKILL.md
+deleted file mode 100644
+index 214fcdd..0000000
+--- a/pr-quality-assistant/skills/requirement-analysis/SKILL.md
++++ /dev/null
+@@ -1,37 +0,0 @@
+----
+-name: requirement-analysis
+-description: Extracts structured requirements and acceptance criteria from a PR description, linked ticket, or user story. Use this skill first, before analyzing code changes, to establish what the PR is supposed to achieve.
+----
+-
+-# Requirement Analysis
+-
+-## Purpose
+-Parse the PR description, commit messages, and any linked issue/ticket to produce a structured, unambiguous set of requirements and acceptance criteria that later skills (blast radius, test analysis, quality report) can validate against.
+-
+-## Inputs
+-- PR title and description
+-- Linked ticket/story (if available) — id, description, acceptance criteria
+-- Commit messages in the PR
+-
+-## Steps
+-1. Read the PR description and linked ticket content.
+-2. Identify explicit and implicit requirements (functional and non-functional).
+-3. Extract or infer acceptance criteria. If the ticket already lists AC, normalize them into discrete, testable statements.
+-4. Flag ambiguous or missing requirements as `openQuestions` rather than guessing.
+-5. Classify each requirement as functional, non-functional (perf/security/a11y), or refactor/chore.
+-
+-## Output Contract
+-```json
+-{
+-  "requirements": [
+-    { "id": "REQ-1", "description": "...", "type": "functional|non-functional|chore" }
+-  ],
+-  "acceptanceCriteria": [
+-    { "id": "AC-1", "description": "...", "linkedRequirement": "REQ-1" }
+-  ],
+-  "openQuestions": ["..."]
+-}
+-```
+-
+-## Handoff
+-Pass `requirements[]` and `acceptanceCriteria[]` to `change-blast-radius` and later to `quality-report` for traceability. Surface `openQuestions[]` to the orchestrator immediately — do not proceed with assumptions.
+diff --git a/pr-quality-assistant/skills/test-analysis/SKILL.md b/pr-quality-assistant/skills/test-analysis/SKILL.md
+deleted file mode 100644
+index a2f5046..0000000
+--- a/pr-quality-assistant/skills/test-analysis/SKILL.md
++++ /dev/null
+@@ -1,43 +0,0 @@
+----
+-name: test-analysis
+-description: Evaluates existing test coverage against the changed code and acceptance criteria to identify coverage gaps. Use after change-blast-radius and before test-generation.
+----
+-
+-# Test Analysis
+-
+-## Purpose
+-Determine whether existing tests adequately cover the changed/affected code and the acceptance criteria established during requirement analysis, and produce a precise list of gaps.
+-
+-## Inputs
+-- `changedFiles[]` and `affectedModules[]` from `change-blast-radius`
+-- `riskTier` (determines strict vs. warn mode)
+-- `acceptanceCriteria[]` from `requirement-analysis`
+-- Existing test suite in the repository
+-
+-## Steps
+-1. Locate existing tests associated with each changed file/module (by naming convention, imports, or coverage reports if available).
+-2. Map each `acceptanceCriteria` item to zero or more existing tests.
+-3. Identify gaps:
+-   - Changed code with no associated test.
+-   - Acceptance criteria with no test mapped to it.
+-   - Edge cases implied by the change type (e.g., interface changes → contract tests) that aren't covered.
+-4. In **strict mode** (`riskTier: high`), any gap is reported as blocking. In normal mode, gaps are reported as warnings.
+-5. Do not modify or generate tests in this skill — only analyze and report. See `references/test-coverage-methodology.md` for detailed evaluation criteria.
+-
+-## Output Contract
+-```json
+-{
+-  "existingTestsMapped": [
+-    { "file": "...", "tests": ["..."] }
+-  ],
+-  "acceptanceCriteriaCoverage": [
+-    { "acId": "AC-1", "covered": true, "tests": ["..."] }
+-  ],
+-  "coverageGaps": [
+-    { "target": "file|AC-id", "reason": "...", "severity": "blocking|warning" }
+-  ]
+-}
+-```
+-
+-## Handoff
+-If `coverageGaps[]` is non-empty, the orchestrator invokes `test-generation`. Regardless, all outputs are passed to `quality-report` for the traceability matrix.
+diff --git a/pr-quality-assistant/skills/test-analysis/references/test-coverage-methodology.md b/pr-quality-assistant/skills/test-analysis/references/test-coverage-methodology.md
+deleted file mode 100644
+index b61a104..0000000
+--- a/pr-quality-assistant/skills/test-analysis/references/test-coverage-methodology.md
++++ /dev/null
+@@ -1,37 +0,0 @@
+-# Test Coverage Methodology
+-
+-## Goal
+-Evaluate test adequacy in a way that is proportional to risk, rather than chasing raw coverage percentage.
+-
+-## Coverage Dimensions
+-1. **Code coverage** — is the changed code path exercised by at least one test?
+-2. **Behavioral coverage** — does a test assert on the *behavior* implied by the change, not just execute the line?
+-3. **Acceptance criteria coverage** — does every AC from `requirement-analysis` map to at least one test that would fail if the AC were violated?
+-4. **Edge case coverage** — for the change type identified in blast-radius analysis:
+-   - Interface changes → contract/boundary tests (null, empty, type mismatches)
+-   - Schema changes → migration/backward-compatibility tests
+-   - Logic changes → happy path + at least one failure/error path
+-   - Concurrency-sensitive code → race condition or idempotency checks where applicable
+-
+-## Mapping Tests to Changes
+-- Prefer explicit traceability (test file naming conventions, `@covers`/`@requirement` style annotations, or coverage tool output) over inference.
+-- When inferring, match by: same module/class under test, shared imports, or test descriptions referencing the changed behavior.
+-- A test "covers" an AC only if its assertions would fail when that specific AC is violated — merely calling the function is not sufficient.
+-
+-## Gap Severity Rules
+-| Condition | Severity |
+-|---|---|
+-| Changed logic file with zero associated tests, `riskTier: high` | blocking |
+-| Acceptance criterion with no mapped test | blocking |
+-| Changed logic file with zero associated tests, `riskTier: low/medium` | warning |
+-| Missing edge case test (e.g., no error-path test) | warning |
+-| Config/styling-only change with no tests | informational (not a gap) |
+-
+-## Reporting Gaps
+-Each gap must include:
+-- `target`: the file, module, or AC id affected
+-- `reason`: plain-language explanation of what's missing
+-- `severity`: `blocking` | `warning` | `informational`
+-- `suggestedAction`: e.g., "add unit test for null input on `parseInvoice()`"
+-
+-This structured output feeds directly into `test-generation` (for blocking/warning gaps) and into the traceability matrix in `quality-report`.
+diff --git a/pr-quality-assistant/skills/test-generation/SKILL.md b/pr-quality-assistant/skills/test-generation/SKILL.md
+deleted file mode 100644
+index 5ffb8a0..0000000
+--- a/pr-quality-assistant/skills/test-generation/SKILL.md
++++ /dev/null
+@@ -1,39 +0,0 @@
+----
+-name: test-generation
+-description: Generates unit/integration test cases for identified coverage gaps, following the repository's existing testing framework and conventions. Invoked conditionally by the orchestrator only when test-analysis reports gaps.
+----
+-
+-# Test Generation
+-
+-## Purpose
+-Close the coverage gaps identified by `test-analysis` by generating well-formed, idiomatic tests that match the existing repository conventions — without inventing a new testing pattern for the project.
+-
+-## Inputs
+-- `coverageGaps[]` from `test-analysis` (only `blocking` and `warning` severities are actioned by default)
+-- Existing test files in the repository (for framework/style detection: e.g., Jest, PyTest, JUnit, Mocha)
+-- Changed source files and their surrounding context
+-
+-## Steps
+-1. Detect the testing framework and conventions already in use (assertion style, mocking library, file naming, folder structure, AAA/Given-When-Return pattern).
+-2. For each actionable gap, generate a test that:
+-   - Targets the specific `reason`/`suggestedAction` from the gap.
+-   - Uses existing fixtures/mocks where available rather than duplicating setup.
+-   - Follows the AAA (Arrange-Act-Assert) or repo's established pattern.
+-3. For AC-level gaps, ensure the generated test explicitly ties back to the acceptance criterion (e.g., in the test description/name).
+-4. If a gap cannot be safely closed without deeper domain knowledge (e.g., ambiguous business rule), do not fabricate assertions — mark it as `skipped` with a reason for human follow-up.
+-5. Do not modify production/source code in this skill — tests only.
+-
+-## Output Contract
+-```json
+-{
+-  "generatedTests": [
+-    { "file": "...", "testName": "...", "targetGap": "...", "content": "..." }
+-  ],
+-  "skippedGaps": [
+-    { "target": "...", "reason": "requires domain clarification" }
+-  ]
+-}
+-```
+-
+-## Handoff
+-Pass `generatedTests[]` and `skippedGaps[]` to `quality-report` for inclusion in the traceability matrix and final recommendations. `skippedGaps` should always surface as explicit action items in the report, never silently dropped.
+diff --git a/pr-quality-assistant/skills/test-sufficiency/SKILL.md b/pr-quality-assistant/skills/test-sufficiency/SKILL.md
+deleted file mode 100644
+index afc3535..0000000
+--- a/pr-quality-assistant/skills/test-sufficiency/SKILL.md
++++ /dev/null
+@@ -1,29 +0,0 @@
+----
+-name: test-sufficiency
+-description: Decides whether the test-analysis coverage gaps are acceptable, returning a boolean decision and rationale before test generation or final reporting.
+----
+-
+-# Test Sufficiency
+-
+-## Purpose
+-Make the workflow's "Tests sufficient?" decision explicit and repeatable. This skill evaluates the gap output from `test-analysis`; it does not generate tests or alter repository files.
+-
+-## Inputs
+-- `coverageGaps[]` from `test-analysis`
+-- `riskTier` and strictness from `change-blast-radius`
+-- Repository testing conventions and any stated acceptance criteria
+-
+-## Steps
+-1. Confirm that every reported gap has a target, reason, and severity.
+-2. Return `sufficient: true` only when `coverageGaps[]` is empty.
+-3. When gaps exist, return `sufficient: false` and explain whether they are blocking or warning-level, including the highest-priority gaps.
+-
+-## Output Contract
+-```json
+-{
+-  "sufficient": true,
+-  "rationale": "No coverage gaps were reported by test-analysis."
+-}
+-```
+-
+-When gaps exist, `sufficient` must be `false`; the rationale must identify the gaps and state whether `test-generation` should run.
+\ No newline at end of file
+
+```

```
