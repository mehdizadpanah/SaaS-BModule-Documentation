# Module Docs Standard (MDS) v1

Version: 1.0.0

## Canonical docs list (Module /docs/)

00_overview.md  
01_scope_personas_usecases.md  
02_domain_model.md  
03_business_logic_and_rules.md  
04_ui_specifications.md  
05_api_contracts.md  
06_events_and_realtime.md  
07_data_model_and_migrations.md  
08_integrations.md  
09_operations_observability.md  
10_qc_and_acceptance.md  

## Legacy to MDS Mapping (Mental Model)

This standard is the target architecture for ALL system documentation.
For developers migrating from the legacy `v2.25` structure:

| Legacy Folder/Context | Target MDS File (Module-based) |
| :--- | :--- |
| `logic/` (Business Rules) | `03_business_logic_and_rules.md` |
| `ui/` (Specs & Wireframes) | `04_ui_specifications.md` |
| `db/` (Schema & Models) | `07_data_model_and_migrations.md` |
| `docs/` (General Overview) | `00_overview.md` & `01_scope_personas_usecases.md` |

> **Note:** New modules MUST follow MDS v1. Legacy Core docs will be migrated to this structure incrementally.

## Changelog

- 1.0.0: Initial skeleton + canonical docs list + legacy mapping.

## Appendix: Definition of Done (DoD) — MDS v1

A repo is considered MDS-compliant when:

- catalogs/categories.yaml + catalogs/modules_registry.yaml exist (SSoT)
- standards/MDS_v1.md is present and guarded (version bump + changelog on change)
- scripts/validate_docs.py passes locally and in CI
- scripts/build_docs.sh produces mkdocs site successfully
- A sample module exists and passes doctor + link checks
- package_artifacts.py produces a zip containing site + exports
