# QC Standard (modules-docs / MDS v1)

Status: draft  
Introduced in: 0.0.0  
Last updated in: 0.0.0  

This document defines the official QC (Quality Control) gates for the **modules-docs** repository.

## 1) QC Gates (Pass/Fail)

### Gate 1: Guard Rules (Protected Standards)

Purpose: prevent unauthorized drift on protected files (e.g., MDS standard).

Command:

```bash
python3 scripts/guard_rules.py
```

PASS:

* Exit code = 0

FAIL:

* Any protected file changed without the required process/version bump.

---

### Gate: Release Meta Sync (README + CHANGELOG)

Command:

```bash
python3 scripts/validate_release_meta.py
```

PASS:

Exit code = 0

README version/date == SSoT version/date

CHANGELOG has a structured entry for the same version and date

FAIL:

Any mismatch between SSoT - README - CHANGELOG

Changelog entry missing Keep-a-Changelog structure: ### Added/Changed/Fixed + at least one bullet

---

### Gate 2: Doctor (MDS Compliance)

Purpose: enforce MDS v1 structural and schema rules across all modules.

Command:

```bash
python3 scripts/doctor.py
```

PASS:

* Exit code = 0
* All registered modules have valid `module.yaml` (schema valid)
* Required docs files exist
* `module_code` uniqueness passes
* Categories are valid

FAIL:

* Any L1/L2/L3/L4/L5 error from Doctor

---

### Gate 3: Catalog Exports

Purpose: ensure registry catalogs can be exported for CI/tools.

Command:

```bash
python3 scripts/export_catalogs.py
```

PASS:

* Exit code = 0
* `.build/exports/` generated successfully

---

### Gate 4: Index/Nav Generation

Purpose: rebuild `.build/docs` and generate `mkdocs_generated.yml`.

Command:

```bash
python3 scripts/generate_indexes.py
```

PASS:

* Exit code = 0
* `mkdocs_generated.yml` generated successfully

---

### Gate 5: Link Checks

Purpose: detect broken internal links in generated docs.

Command:

```bash
python3 scripts/check_links.py
```

PASS:

* Exit code = 0

---

### Gate 6: MkDocs Build

Purpose: build site output deterministically.

Command:

```bash
mkdocs build -f mkdocs_generated.yml
```

PASS:

* Exit code = 0
* `site/` created

---

### Gate 7: Artifacts Packaging

Purpose: generate a standard artifact for CI delivery.

Command:

```bash
python3 scripts/package_artifacts.py
```

PASS:

* Exit code = 0
* `dist/` contains artifacts zip

## 2) Default Local QC Run (Recommended)

Command:

```bash
chmod +x scripts/build_docs.sh
./scripts/build_docs.sh
python3 scripts/package_artifacts.py
```

## 3) CI Policy

CI must run the same gates on every Pull Request.
