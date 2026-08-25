# Agent Skills Flow

```mermaid
flowchart TD
    H[Agent Skills-compatible host] --> CR[pr-code-review skill]
    CR --> V[Validate repository and refs]
    V --> MB[Calculate merge base]
    MB --> C[Collect CodeReviewContext]
    C --> GM[Git metadata]
    C --> DF[Diff and changed files]
    C --> CH[Commit history]
    C --> RS[Repository structure]
    C --> IT[Instructions and tests]
    GM --> CT[Context JSON]
    DF --> CT
    CH --> CT
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
    RH --> FR[Final five-gate review]
    FR --> RR[review/review-result.json]
    RR --> HTML[review/review-report.html]

    RR --> MR[pr-code-merger skill]
    MR --> BR[Six-dimension blast-radius assessment]
    BR --> BRM[review/blast-radius-report.md]
    BR --> MP[Merge policy]
    MP --> DEC{Low risk and all gates pass?}
    DEC -->|yes| AM[auto_merge decision]
    DEC -->|no| HR[human_review decision]
    AM --> MERGE[Optional host merge tool]
    MERGE --> VERIFY[Verify merged state]
    VERIFY --> MJSON[review/merge-result.json]
    HR --> MJSON

    W[Merged PR webhook or scheduled job] --> RI[Historical intelligence phase]
    RI --> IG[Review comment extraction and cleansing]
    IG --> D[Deduplicate by PR ID + comment hash]
    D --> J[pr-insights.json]
    D --> I[.github/instructions/insights.instructions.md]
    I -. loaded by .-> CR
    J -. detailed provenance .-> CR

```

The portable package surface is `plugin.json` plus the immediate skill directories under `skills/`. The Git-only collector produces review context; hosts decide how to expose skills and deliver merged-PR events.