# Acceptance Criteria

Produce `acceptance-criteria.md` from the facts emitted by `extract-acceptance-context.py`.

- Prefer explicit PR requirements and discussion over inferred behavior.
- Use implementation and tests to clarify observable behavior, not to turn implementation details into requirements.
- Never create a criterion solely because it sounds like good engineering practice.
- Every criterion must be independently meaningful and verifiable.
- Merge semantic duplicates while preserving distinct observable behaviors.
- Include `Requirement`, `Evidence`, `Confidence`, and `Verification` for every criterion.
- Mark unsupported intent as `Unknown / cannot determine` instead of inventing a criterion.

Include a source-of-criteria section and cite paths, PR/change-request IDs, comments, or test names for every claim.