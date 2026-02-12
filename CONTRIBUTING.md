# Contributing

Thanks for helping improve this repo. This guide provides a clear path for local setup, common commands, and the end-to-end workflow.

## Prerequisites

- Python 3.x
- pip

## Install

```bash
pip install -r requirements.txt
```

## Common Commands

```bash
bash scripts/build_docs.sh
python3 scripts/validate_docs.py
python3 scripts/doctor.py
python3 scripts/package_artifacts.py
python3 scripts/package_output.py --mode changed
```

## Workflow

Idea -> Inbox -> Triage (Approval) -> Definition (MDS fit + Core risk) -> Scaffolding -> Documentation (MDS) -> Release

## Idea field: applicable_business_segments

Use this field to specify which business segments an idea applies to so we can correctly align with workspace `business_segment` segmentation.
This field is required and impacts module decisions, pricing strategy, and feature activation logic.

Allowed formats:

- `all`
- A non-empty list like `[restaurant, retail, b2b_manufacturing]`

Rules:

- List values must be `lowercase_snake_case`.
- Use `all` only if the idea is truly general.
- For `proposed_category: commerce`, avoid defaulting to `all`; prefer an explicit segment list unless the idea is truly universal.
- For older ideas where applicability is still unknown, temporarily set `all` and refine later.

Examples:

- General idea: `applicable_business_segments: all`
- Segment-specific idea: `applicable_business_segments: [restaurant, retail]`

## Quality Gates (SSoT)

See the QC standard in [standards/QC.md](standards/QC.md).
