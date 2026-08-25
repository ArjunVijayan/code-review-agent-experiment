# Review Context Schema

The canonical internal object is `CodeReviewContext`; `review/review-context.md` is its human-readable rendering. The collector must preserve source facts and keep the raw diff last in the Markdown output.

```json
{
  "repository": { "root": "...", "files": [], "manifests": [] },
  "change": {
    "base": "main",
    "source": "dev/bug_fix",
    "base_commit": "...",
    "source_commit": "...",
    "merge_base": "...",
    "files": [],
    "statistics": { "files_changed": 0, "insertions": 0, "deletions": 0 },
    "diff": "..."
  },
  "history": { "commits": [] },
  "instructions": { "files": [] },
  "tests": { "manifests": [], "test_files": [], "changed_tests": [] }
}
```