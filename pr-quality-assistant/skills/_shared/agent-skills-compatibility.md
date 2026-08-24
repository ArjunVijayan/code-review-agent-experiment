# Agent Skills Compatibility

The directories under `skills/` are the portable integration surface. Any agent host that supports the Agent Skills format can discover a skill by its directory and `SKILL.md` file, then invoke it by the frontmatter `name`.

Hosts should provide these inputs and preserve the documented output contracts. The shared workflow is:

1. Load `data/insights.instructions.md` when it exists.
2. Run `requirement-analysis`, `change-blast-radius`, and `test-analysis` in that order.
3. Run `test-sufficiency` with the test-analysis output.
4. Run `test-generation` only when sufficiency is false, then run `quality-report`.

The `agents/*.agent.md`, `plugin.json`, and `hooks.json` files are optional host adapters. A host without Copilot plugin or hook support can use the skills directly and invoke `repo-intelligence` from its own merged-PR webhook or scheduled automation. The intelligence agent must still verify merge status and write the same two data files.