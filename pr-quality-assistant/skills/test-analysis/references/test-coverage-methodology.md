# Test Coverage Methodology

## Goal
Evaluate test adequacy in a way that is proportional to risk, rather than chasing raw coverage percentage.

## Coverage Dimensions
1. **Code coverage** — is the changed code path exercised by at least one test?
2. **Behavioral coverage** — does a test assert on the *behavior* implied by the change, not just execute the line?
3. **Acceptance criteria coverage** — does every AC from `requirement-analysis` map to at least one test that would fail if the AC were violated?
4. **Edge case coverage** — for the change type identified in blast-radius analysis:
   - Interface changes → contract/boundary tests (null, empty, type mismatches)
   - Schema changes → migration/backward-compatibility tests
   - Logic changes → happy path + at least one failure/error path
   - Concurrency-sensitive code → race condition or idempotency checks where applicable

## Mapping Tests to Changes
- Prefer explicit traceability (test file naming conventions, `@covers`/`@requirement` style annotations, or coverage tool output) over inference.
- When inferring, match by: same module/class under test, shared imports, or test descriptions referencing the changed behavior.
- A test "covers" an AC only if its assertions would fail when that specific AC is violated — merely calling the function is not sufficient.

## Gap Severity Rules
| Condition | Severity |
|---|---|
| Changed logic file with zero associated tests, `riskTier: high` | blocking |
| Acceptance criterion with no mapped test | blocking |
| Changed logic file with zero associated tests, `riskTier: low/medium` | warning |
| Missing edge case test (e.g., no error-path test) | warning |
| Config/styling-only change with no tests | informational (not a gap) |

## Reporting Gaps
Each gap must include:
- `target`: the file, module, or AC id affected
- `reason`: plain-language explanation of what's missing
- `severity`: `blocking` | `warning` | `informational`
- `suggestedAction`: e.g., "add unit test for null input on `parseInvoice()`"

This structured output feeds directly into `test-generation` (for blocking/warning gaps) and into the traceability matrix in `quality-report`.
