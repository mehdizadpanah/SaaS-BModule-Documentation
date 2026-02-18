# Idea Item Template

- [ ] MI-0000 | [short title]
  - candidate_module_code: `placeholder`
  - proposed_category: <category_key>
  - priority: P1|P2|P3
  - dependencies: []
  - platform_compatibility: unknown
  - target_persona: admin|end_user|...
  - applicable_business_segments: all|[restaurant, retail, manufacturing]
  - core_dependency_risk: yes|no
  - created_at: YYYY-MM-DD
  - notes:
    - EN: ...
    - FA: ...

Rule:

- `applicable_business_segments` must be either `all` or a non-empty list.
- List items must be `lowercase_snake_case`.
- List items must exist in the official registry at `catalogs/business_segments.yaml`.
- Use `all` only when the idea is genuinely segment-agnostic.
