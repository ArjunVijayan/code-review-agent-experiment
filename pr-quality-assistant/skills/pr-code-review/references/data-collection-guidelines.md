# Data Collection Guidelines

The context collector records facts that can be traced to Git or the repository filesystem.

- Use `base...source` for the change-focused comparison and record the merge base.
- Keep raw diff text unchanged and place it last in the rendered artifact.
- Record paths relative to the repository root where possible.
- Treat instruction files as metadata; do not interpret or rewrite their rules during collection.
- Identify tests without running them; execution belongs to a later review stage.
- Fail before rendering when the repository, refs, or merge base cannot be resolved.
