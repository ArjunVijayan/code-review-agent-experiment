---
name: code-review
description: Collect Git repository context for code review.
---

# Code Review

When invoked with the logical request `{ "base": "main", "source": "dev/bug_fix" }`:

1. Validate the repository.
2. Validate the supplied refs.
3. Determine the merge base.
4. Collect Git metadata, including the merge base and introduced commit history.
5. Collect changed files.
6. Collect the complete diff.
7. Collect repository structure, relevant instructions, and test information.
8. Collect repository instructions.
9. Collect relevant test information.
10. Generate `review/review-context.md` from the canonical `CodeReviewContext` object.

Do not perform code review at this stage.

Do not make approval decisions.

## Implementation

The client or launcher maps its command syntax to the logical request; the skill does not depend on a specific CLI. Run `scripts/collect_context.py` to produce the structured context JSON, then run `scripts/generate_context.py` with that JSON to render the Markdown artifact.

The scripts require Python 3.9 or newer and a Git repository. They use Git only for repository facts and do not call GitHub, GitLab, or any remote API.