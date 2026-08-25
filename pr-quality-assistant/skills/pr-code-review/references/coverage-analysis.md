# Coverage Analysis

Produce `code-coverage-report.md` from the facts emitted by `analyze-test-coverage.py`.

- Analyze changed behavior and execution paths, not changed lines alone.
- Inspect existing tests before declaring coverage missing.
- Determine whether the repository has enough unit tests for each changed behavioral path, including success, boundary, invalid-input, and error scenarios when the contract supports them.
- A test-file count is not evidence of sufficiency; cite the specific test function or explain why no test exercises the path.
- Identify meaningful success, boundary, and error scenarios for each behavioral area.
- Use measured coverage files when available and label their evidence as measured.
- Without measured data, label conclusions as change-based test sufficiency.
- Never fabricate a global percentage or claim a test passed unless it was inspected or run.
- Do not require tests for mechanical changes unless they affect behavior.
- Do not recommend tests merely to increase line coverage.

For each behavioral area, include the changed code, required scenarios, unit-test evidence, status, finding, and recommendation. If intended behavior cannot be established from evidence, say `Unknown / cannot determine`. Evaluate each scenario as `Covered`, `Missing`, `Uncertain`, or `Not applicable`.