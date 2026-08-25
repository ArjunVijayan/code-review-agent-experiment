# Agent Skills Flow

```mermaid
flowchart TD
    H[Agent Skills-compatible host] --> PR[pr-quality-review]
    PR --> R[Requirements]
    R --> B[Change and blast radius]
    B --> G[Repository guidelines and coding standards]
    G --> T[Test and integration analysis]
    T --> S{Tests sufficient?}
    S -->|yes| Q[Quality report]
    S -->|no| TG[Test generation]
    TG --> M[Issue remediation]
    M --> Q

    W[Merged PR webhook or scheduled job] --> RI[repo-intelligence]
    RI --> IG[Review comment extraction and cleansing]
    IG --> D[Deduplicate by PR ID + comment hash]
    D --> J[pr-insights.json]
    D --> I[.github/instructions/insights.instructions.md]
    I -. loaded by .-> PR
    J -. detailed provenance .-> PR

```

The portable package surface is `plugin.json` plus the immediate skill directories under `skills/`. Hosts decide how skills are exposed and how merged-PR events invoke `repo-intelligence`.