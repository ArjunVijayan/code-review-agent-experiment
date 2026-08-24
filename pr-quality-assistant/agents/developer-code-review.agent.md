---
name: developer-code-review
description: Performs an on-demand pre-PR developer review using repository requirements, blast-radius, test, and accumulated review insights to find actionable quality risks.
skills:
  - requirement-analysis
  - change-blast-radius
  - test-analysis
  - test-sufficiency
  - test-generation
  - quality-report
---

# Developer Code Review

Load `data/insights.instructions.md` as additional repository context before invoking any skill. Treat it as auto-maintained guidance and use it to focus review attention, not to override the current PR evidence. For host-neutral discovery and invocation rules, follow `skills/_shared/agent-skills-compatibility.md`.

Follow the shared sequence in `skills/_shared/analysis-phase.md`: requirement-analysis, change-blast-radius, then test-analysis. Invoke `test-sufficiency` explicitly with the test-analysis output. If it returns `sufficient: false`, invoke `test-generation` before the final `quality-report`; otherwise proceed directly to reporting. Surface open questions instead of guessing.