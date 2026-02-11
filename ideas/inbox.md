# Idea Inbox

Rule: Inbox is for quick capture only. Grooming happens later by moving items to backlog.md or creating a module folder.

## Items

- [ ] MI-0001 | Workspace Contacts Directory (دفترچه مخاطبین ورک‌اسپیس)
  - candidate_module_code: core.contacts
  - proposed_category: core-platform
  - priority: P1
  - dependencies: []
  - platform_compatibility: unknown
  - target_persona: end_user
  - core_dependency_risk: yes
  - created_at: 2026-02-11
  - notes:

    EN: Workspace-scoped shared contacts directory for all users; acts as the canonical Contacts provider for other modules (no duplicate contact lists elsewhere).

    FA: دفترچه مخاطبین اشتراکی در سطح ورک‌اسپیس برای همه کاربران؛ مرجع واحد مخاطبین برای سرویس‌دهی به سایر ماژول‌ها (عدم تکرار لیست مخاطبین در ماژول‌های دیگر).

- [ ] MI-0002 | Workspace Business Profile (Dynamic Attributes by Business Type)
  - candidate_module_code: core.business_profile
  - proposed_category: core-platform
  - priority: P1
  - dependencies: []
  - platform_compatibility: unknown
  - target_persona: admin
  - core_dependency_risk: yes
  - created_at: 2026-02-11
  - notes:

    EN: Workspace-scoped “business profile” intake driven by the workspace business_segment (and the segment is changeable). Collects typed attributes/questions based on selected segment (e.g., restaurant: floors, table count, seats per table, delivery capability, etc.). When business_segment changes, the active questionnaire/attribute set switches accordingly; other modules query this as the canonical source of business attributes.

    FA: ماژول «مشخصات بیزینس» در سطح ورک‌اسپیس که بر اساس business_segment ورک‌اسپیس کار می‌کند (و این سگمنت قابل تغییر است). بر اساس سگمنت، سوالات/فیلدهای تایپ‌دار می‌گیرد (مثلاً رستوران: تعداد طبقات، تعداد میز، ظرفیت هر میز، امکان دلیوری و…). با تغییر business_segment، مجموعه سوالات/فیلدها هم تغییر می‌کند و سایر ماژول‌ها اینجا را به‌عنوان مرجع واحد مشخصات بیزینس مصرف می‌کنند.
