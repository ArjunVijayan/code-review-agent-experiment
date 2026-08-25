# Agent Skills Flow

```mermaid
flowchart TD
    H[Agent Skills-compatible host] --> CR[code-review skill]
    CR --> V[Validate repository and refs]
    V --> MB[Calculate merge base]
    MB --> C[Collect CodeReviewContext]
    C --> GM[Git metadata]
    C --> DF[Diff and changed files]
    C --> RH[Commit history]
    C --> RS[Repository structure]
    C --> IT[Instructions and tests]
    GM --> CT[Context JSON]
    DF --> CT
    RH --> CT
    RS --> CT
    IT --> CT
    CT --> MD[review/review-context.md]
    CT --> AC[Acceptance context facts]
    AC --> ACM[review/acceptance-criteria.md]
    CT --> TC[Test and coverage facts]
    TC --> TCM[review/code-coverage-report.md]
    MD --> RH[Review handoff]
    ACM --> RH
    TCM --> RH

    W[Merged PR webhook or scheduled job] --> RI[repo-intelligence]
    RI --> IG[Review comment extraction and cleansing]
    IG --> D[Deduplicate by PR ID + comment hash]
    D --> J[pr-insights.json]
    D --> I[.github/instructions/insights.instructions.md]
    I -. loaded by .-> CR
    J -. detailed provenance .-> CR

```

The portable package surface is `plugin.json` plus the immediate skill directories under `skills/`. The Git-only collector produces review context; hosts decide how to expose skills and deliver merged-PR events.