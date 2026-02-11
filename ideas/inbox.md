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

    - EN: Workspace-scoped shared contacts directory for all users; acts as the canonical Contacts provider for other modules (no duplicate contact lists elsewhere).

    - FA: دفترچه مخاطبین اشتراکی در سطح ورک‌اسپیس برای همه کاربران؛ مرجع واحد مخاطبین برای سرویس‌دهی به سایر ماژول‌ها (عدم تکرار لیست مخاطبین در ماژول‌های دیگر).

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

    - EN: Workspace-scoped “business profile” intake driven by the workspace business_segment (and the segment is changeable). Collects typed attributes/questions based on selected segment (e.g., restaurant: floors, table count, seats per table, delivery capability, etc.). When business_segment changes, the active questionnaire/attribute set switches accordingly; other modules query this as the canonical source of business attributes.

    - FA: ماژول «مشخصات بیزینس» در سطح ورک‌اسپیس که بر اساس business_segment ورک‌اسپیس کار می‌کند (و این سگمنت قابل تغییر است). بر اساس سگمنت، سوالات/فیلدهای تایپ‌دار می‌گیرد (مثلاً رستوران: تعداد طبقات، تعداد میز، ظرفیت هر میز، امکان دلیوری و…). با تغییر business_segment، مجموعه سوالات/فیلدها هم تغییر می‌کند و سایر ماژول‌ها اینجا را به‌عنوان مرجع واحد مشخصات بیزینس مصرف می‌کنند.

- [ ] MI-0003 | Digital Catalog (Menu/Catalog) + Channels
  - candidate_module_code: commerce.catalog
  - proposed_category: commerce
  - priority: P1
  - dependencies: []
  - platform_compatibility: unknown
  - target_persona: admin
  - core_dependency_risk: no
  - created_at: 2026-02-11
  - notes:

    - EN: Business-agnostic digital catalog (products/services) with categories, pricing, media, and availability. Includes “Channel/Presentation” configuration to control how the catalog is exposed: QR/table link, public URL for website, embedded widget, kiosk, etc. Channel settings include access mode (public/login/approved customers), template/theme (restaurant vs industrial/B2B), and link/token generation. Acts as the canonical catalog provider for Ordering and other modules.

    - FA: کاتالوگ دیجیتال عمومی برای محصولات/خدمات (دسته‌بندی، قیمت، تصاویر/مدیا، در دسترس بودن). شامل مفهوم «کانال/Presentation» برای تعیین نحوه ارائه: QR روی میز، لینک عمومی برای وبسایت، ویجت قابل Embed، کیوسک و… با تنظیمات دسترسی (عمومی/لاگین/مشتری تأیید‌شده)، قالب/تم (رستورانی یا صنعتی/B2B) و تولید لینک/توکن. مرجع اصلی کاتالوگ برای ماژول سفارش و سایر ماژول‌ها.

- [ ] MI-0004 | Ordering & Checkout (Context-aware)
  - candidate_module_code: commerce.ordering
  - proposed_category: commerce
  - priority: P1
  - dependencies: [commerce.catalog]
  - platform_compatibility: unknown
  - target_persona: end_user
  - core_dependency_risk: no
  - created_at: 2026-02-11
  - notes:

    - EN: Optional ordering layer on top of the Digital Catalog: cart, order submission, order tracking, and optional online payment (admin-controlled). Supports context-aware ordering via Channel tokens: table-specific QR (table_id), counter/cashier (pickup), takeaway, delivery, or no-context web storefront (B2B). Uses signed/unique links/tokens to bind an order to its context and prevent guessing. Payment can be enabled/disabled per workspace/channel.

    - FA: لایه سفارش‌گیری اختیاری روی کاتالوگ: سبد خرید، ثبت سفارش، پیگیری وضعیت، و پرداخت آنلاین (اختیاری و قابل فعال/غیرفعال توسط مدیر). پشتیبانی از سفارش کانتکست‌دار از طریق توکن کانال: QR اختصاصی هر میز (table_id)، سفارش از صندوق/پیکاپ، بیرون‌بر، دلیوری، یا حالت فروشگاه وب بدون کانتکست (B2B). لینک/توکن یکتا و امضاشده برای اتصال سفارش به کانتکست و جلوگیری از حدس‌زدن. پرداخت به‌صورت per workspace/channel قابل کنترل است.

- [ ] MI-0005 | Customers (Lightweight Order Accounts, Workspace-Scoped)
  - candidate_module_code: commerce.customers
  - proposed_category: commerce
  - priority: P1
  - dependencies: [commerce.ordering, core.contacts]
  - platform_compatibility: unknown
  - target_persona: end_user
  - core_dependency_risk: no
  - created_at: 2026-02-11
  - notes:

    - EN: Introduce a lightweight, workspace-scoped Customer entity for ordering/checkout without polluting Contacts. Supports minimal registration (phone/email, OTP verification), guest vs registered modes (per workspace/channel setting), and maintains order history linkage. Store low-trust user-entered name as display_name (not a canonical contact). Optionally link a customer to a curated Contact via nullable contact_id when admin confirms/matches. Enforce uniqueness per workspace (workspace_id+phone/email).

    - FA: تعریف موجودیت/ماژول «مشتری» سبک و در سطح ورک‌اسپیس برای سفارش‌گیری/پرداخت بدون آلوده‌کردن Contacts. ثبت‌نام حداقلی (موبایل/ایمیل + OTP)، حالت مهمان یا ثبت‌نام (قابل تنظیم per workspace/channel)، و اتصال تاریخچه سفارش‌ها. نام واردشده توسط کاربر به‌صورت display_name ذخیره شود (نه کانتکت مرجع). امکان لینک اختیاری به Contact تمیز از طریق contact_id (nullable) فقط پس از تأیید/Match توسط ادمین. یکتایی بر اساس workspace_id + phone/email.
