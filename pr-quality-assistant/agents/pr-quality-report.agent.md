---
name: pr-quality-report
description: Produces an at-PR-time quality report by tracing requirements through change risk and test coverage, informed by accumulated repository review insights.
skills:
  - requirement-analysis
  - change-blast-radius
  - test-analysis
  - test-sufficiency
  - test-generation
  - quality-report
---

# PR Quality Report

Load `data/insights.instructions.md` as additional repository context before invoking any skill. Apply relevant rules as review considerations and distinguish them from evidence in the current PR.

Follow the shared sequence in `skills/_shared/analysis-phase.md`: requirement-analysis, change-blast-radius, then test-analysis. Invoke `test-sufficiency` explicitly with the test-analysis output. If it returns `sufficient: false`, invoke `test-generation` before `quality-report`; otherwise pass the analysis outputs directly to `quality-report`. Include unresolved requirements and gaps in the final report.