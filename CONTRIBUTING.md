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

## Quality Gates (SSoT)

See the QC standard in [standards/QC.md](standards/QC.md).
