# Acceptance Criteria

Produce `acceptance-criteria.md` from the facts emitted by `extract-acceptance-context.py`.

- Prefer explicit PR requirements and discussion over inferred behavior.
- If PR comments or requirements cannot be resolved, identify the repository's role from README/manifests and derive only observable behavior directly evidenced by the changed files, tests, and repository instructions.
- Make each derived criterion clear, concrete, and independently checkable by naming the actor/input, observable result, and relevant evidence.
- Use implementation and tests to clarify observable behavior, not to turn implementation details into requirements.
- Never create a criterion solely because it sounds like good engineering practice.
- Every criterion must be independently meaningful and verifiable.
- Merge semantic duplicates while preserving distinct observable behaviors.
- Include `Requirement`, `Evidence`, `Confidence`, and `Verification` for every criterion.
- Mark unsupported intent as `Unknown / cannot determine` instead of inventing a criterion.
- After extraction, evaluate every criterion as `PASS`, `FAIL`, `UNCERTAIN`, or `NOT_APPLICABLE`; uncertainty is never a pass.

Include a source-of-criteria section and cite paths, PR/change-request IDs, comments, or test names for every claim.