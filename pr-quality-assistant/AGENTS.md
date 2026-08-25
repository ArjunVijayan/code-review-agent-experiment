# PR Quality Assistant

This repository contains an Agent Plugins v1.0 package. Load `skills/pr-quality-review/SKILL.md` for the complete pull-request workflow or `skills/repo-intelligence/SKILL.md` after a merged PR. No custom orchestration agent is required.

The host supplies a merged-PR webhook, scheduled job, or native lifecycle event to `skills/repo-intelligence/SKILL.md`. No custom orchestration agent or client-specific hook is required.