# Backlog

Triaged ideas moved from inbox.md.

## 2026-02-20 ? Captured ideas for release 0.0.0

Moved from ideas/inbox.md (initial capture).

- [ ] MI-0001 | Workspace Contacts Directory (دفترچه مخاطبین ورک‌اسپیس)
  - candidate_module_code: core.contacts
  - proposed_category: core-platform
  - priority: P1
  - dependencies: []
  - platform_compatibility: unknown
  - target_persona: end_user
  - applicable_business_segments: all
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
  - applicable_business_segments: all
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
  - applicable_business_segments: [restaurant, catering, bakery_patisserie, retail, ecommerce_b2c, ecommerce_marketplace_seller, hospitality]
  - core_dependency_risk: no
  - created_at: 2026-02-11
  - notes:

    - EN: Digital Catalog/Menu Builder is a presentation & curation layer only (themes, responsive layouts, channels like QR/table, public URL, embed). It does NOT own item creation. All products/services must come from the canonical registry core.products, and catalogs only select/organize/display those items.

    - FA: دیجیتال کاتالوگ/منوساز فقط لایه‌ی نمایش و چیدمان است (قالب‌ها، ریسپانسیو، کانال‌ها مثل QR/میز، لینک عمومی، Embed) و محل ثبت کالا نیست. تمام کالا/خدمت باید از بانک مرجع core.products تامین شود و کاتالوگ فقط انتخاب/گروه‌بندی/نمایش آیتم‌ها را انجام می‌دهد.

- [ ] MI-0004 | Ordering & Checkout (Context-aware)
  - candidate_module_code: commerce.ordering
  - proposed_category: commerce
  - priority: P1
  - dependencies: [commerce.catalog]
  - platform_compatibility: unknown
  - target_persona: end_user
  - applicable_business_segments: [restaurant, catering, retail, ecommerce_b2c, ecommerce_marketplace_seller, hospitality]
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
  - applicable_business_segments: [restaurant, catering, retail, ecommerce_b2c, ecommerce_marketplace_seller, hospitality]
  - core_dependency_risk: no
  - created_at: 2026-02-11
  - notes:

    - EN: Introduce a lightweight, workspace-scoped Customer entity for ordering/checkout without polluting Contacts. Supports minimal registration (phone/email, OTP verification), guest vs registered modes (per workspace/channel setting), and maintains order history linkage. Store low-trust user-entered name as display_name (not a canonical contact). Optionally link a customer to a curated Contact via nullable contact_id when admin confirms/matches. Enforce uniqueness per workspace (workspace_id+phone/email).

    - FA: تعریف موجودیت/ماژول «مشتری» سبک و در سطح ورک‌اسپیس برای سفارش‌گیری/پرداخت بدون آلوده‌کردن Contacts. ثبت‌نام حداقلی (موبایل/ایمیل + OTP)، حالت مهمان یا ثبت‌نام (قابل تنظیم per workspace/channel)، و اتصال تاریخچه سفارش‌ها. نام واردشده توسط کاربر به‌صورت display_name ذخیره شود (نه کانتکت مرجع). امکان لینک اختیاری به Contact تمیز از طریق contact_id (nullable) فقط پس از تأیید/Match توسط ادمین. یکتایی بر اساس workspace_id + phone/email.
  
- [ ] MI-0006 | Product/Service Registry (Workspace Item Bank)
  - candidate_module_code: core.products
  - proposed_category: core-platform
  - priority: P1
  - dependencies: []
  - platform_compatibility: unknown
  - target_persona: admin
  - applicable_business_segments: all
  - core_dependency_risk: yes
  - created_at: 2026-02-11
  - notes:

    - EN: Workspace-scoped canonical registry (“bank”) of products and services (items) to be reused across modules. Acts as SSoT for CRM, Accounting, Catalog/Menu design, Ordering, and future inventory/quotes. Other modules must reference items from this registry instead of defining their own product lists.

    - FA: بانک/رجیستری مرجع کالا و خدمت در سطح ورک‌اسپیس برای استفاده’ی مشترک بین ماژول‌ها. مرجع واحد (SSoT) برای CRM، حسابداری، طراحی کاتالوگ/منو، سفارش’گیری و توسعه’های آینده مثل انبار/پیش’فاکتور. سایر ماژول‌ها باید به آیتم‌های این بانک ارجاع بدهند و لیست مستقل کالا نسازند.
  
- [ ] MI-0007 | Digital Signage (Multi-Screen Promo Presentation)
  - candidate_module_code: commerce.signage
  - proposed_category: commerce
  - priority: P2
  - dependencies: [core.products]
  - platform_compatibility: unknown
  - target_persona: admin
  - applicable_business_segments: [restaurant, retail, events_exhibitions, fitness_gym]
  - core_dependency_risk: no
  - created_at: 2026-02-11
  - notes:

    - EN: Digital signage/promo presentation module for non-interactive, slideshow-style display (powerpoint-like). Supports playlists of slides containing static images, designed visuals, and animations. Must support multiple screens per workspace, with screen groups that run synchronized and scheduled playback (time-based campaigns, rotation, start/stop windows). Content references products/services from core.products (and optionally curated collections), but does not own item creation. Designed for cashier-area menu boards and promotional monitors.

    - FA: ماژول دیجیتال ساینیج/پرزنتیشن تبلیغاتی برای نمایش غیرتعاملی و اسلایدشو‌وار (شبیه پاورپوینت). پشتیبانی از پلی‌لیست اسلایدها شامل تصاویر ثابت، طرح‌های گرافیکی، و انیمیشن. پشتیبانی از چندین مانیتور در هر ورک‌اسپیس با مفهوم گروه مانیتور (screen groups) که هماهنگ و زمان‌بندی‌شده اجرا شوند (کمپین‌های زمان‌دار، چرخش، پنجره‌های شروع/پایان). محتوا به کالا/خدمت‌های core.products (و در صورت نیاز کالکشن‌ها) ارجاع می‌دهد و مالک ایجاد آیتم نیست. مناسب مانیتورهای بالای صندوق و نمایش‌های تبلیغاتی.

- [ ] MI-0008 | Queue Management (Ticket + Pickup, Multi-Counter, Real-time)
  - candidate_module_code: commerce.queue
  - proposed_category: commerce
  - priority: P1
  - dependencies: [commerce.ordering]
  - platform_compatibility: unknown
  - target_persona: admin
  - applicable_business_segments: [medical_clinic, dental, lab_imaging, government, retail, restaurant, insurance_brokerage]
  - core_dependency_risk: no
  - created_at: 2026-02-11
  - notes:

    - EN: Workspace queue/turn management system supporting multiple independent queues per workspace (units/branches) with independent numbering. Supports two main modes: (A) Ticket Queue (bank-like: customer takes a number via QR/link/kiosk) and (B) Pickup Number (restaurant-like: number exists on receipt/order and is called when ready). Per-queue configuration supports Standalone numbering, Ordering-fed numbers (from commerce.ordering), or Hybrid. Each queue supports multiple counters/desks with an operator console (Call Next/Recall/Skip/Hold/Transfer/No-show) and announces “number X → counter Y”. Provide web-based counter display (tablet/monitor) and a public waiting display with last-called history. Real-time sync via WebSockets/SignalR-like so all displays update instantly. Audio announcements must support pre-recorded audio assets (mandatory) and optionally TTS later. Queue reset policy must be configurable by workspace (daily reset vs manual/continuous).

    - FA: سیستم نوبت‌دهی/صف در سطح ورک‌اسپیس با امکان چند صف مستقل برای واحدها/شعبه‌ها و شماره‌گذاری مستقل. دو حالت اصلی: (A) نوبت‌گیری واقعی مثل بانک (QR/لینک/کیوسک) و (B) شماره فیش/سفارش مثل رستوران (بدون نوبت‌گیری، اعلام هنگام آماده‌شدن). برای هر صف امکان تنظیم وجود دارد: مستقل (Standalone)، تغذیه از سفارش‌ها (Ordering-fed از commerce.ordering)، یا Hybrid. پشتیبانی از چند کانتر/باجه با پنل اپراتور (Call Next/Recall/Skip/Hold/Transfer/No-show) و اعلام «شماره X به کانتر Y». نمایشگر اختصاصی هر کانتر (تبلت/مانیتور) و نمایشگر عمومی سالن با تاریخچه شماره‌های اخیر. همگام‌سازی لحظه‌ای با WebSocket/SignalR-like برای آپدیت فوری همه نمایشگرها. اعلان صوتی با فایل‌های صوتی آماده (اجباری) و امکان TTS در آینده. سیاست ریست شماره‌ها قابل تنظیم توسط ورک‌اسپیس (روزانه یا دستی/پیوسته).

- [ ] MI-0009 | Service Requests (Staff Assist / Call for Help)
  - candidate_module_code: commerce.service_requests
  - proposed_category: commerce
  - priority: P2
  - dependencies: [commerce.catalog]
  - platform_compatibility: unknown
  - target_persona: end_user
  - applicable_business_segments: [restaurant, hospitality, medical_clinic, dental, retail, fitness_gym]
  - core_dependency_risk: no
  - created_at: 2026-02-12
  - notes:

    - EN: Context-aware “staff assist” requests triggered by customers/visitors via QR/link (e.g., table/room/counter/fitting-room). A workspace can define request types (Help, Bill, Assistance, etc.) and route them to internal staff users (all staff are active workspace users) by role/team/group. Provide staff dashboard with real-time updates (new/accepted/resolved), assignment/accept workflow, and history/metrics (response time). Reuses existing channel/token context from commerce.catalog; does not require ordering.

    - FA: ماژول «درخواست سرویس/فراخوان پرسنل» مبتنی بر کانتکست که توسط مشتری/مراجع از طریق QR/لینک (میز/اتاق/کانتر/اتاق پرو و…) ثبت می‌شود. ورک‌اسپیس می‌تواند نوع درخواست‌ها را تعریف کند (کمک، صورت‌حساب، رسیدگی، …) و آن را به Staffهای داخلی (همه Staffها کاربر فعال workspace هستند) بر اساس Role/Team/Group روت کند. داشبورد پرسنل با آپدیت لحظه‌ای (جدید/پذیرفته‌شده/حل‌شده)، جریان کاری assignment/accept و تاریخچه/متریک‌ها (زمان پاسخ) ارائه شود. از کانتکست/توکن‌های کانال در commerce.catalog استفاده می‌کند و الزاماً به سفارش‌گیری وابسته نیست.

- [ ] MI-0010 | Appointments/Booking (Time Slots + Check-in Integration)
  - candidate_module_code: commerce.appointments
  - proposed_category: commerce
  - priority: P1
  - dependencies: [commerce.queue, commerce.customers]
  - platform_compatibility: unknown
  - target_persona: admin
  - core_dependency_risk: no
  - applicable_business_segments: [medical_clinic, dental, beauty_wellness, school, training_institute, legal_services, accounting_tax, engineering_consulting, government]
  - created_at: 2026-02-12
  - notes:

    - EN: Appointment scheduling module for businesses that require booking time slots (e.g., clinics/doctors, professional services, branches). Supports services + schedules + slot templates (availability rules), resource allocation (staff/provider/room), capacity per slot, and customer self-service (book/reschedule/cancel) with automated confirmations/reminders to reduce no-shows. Include waitlist/backfill (fill cancelled slots) and configurable policies (lead time, cancellation window, deposits optional later). Integrates with commerce.queue via check-in: scheduled customers can arrive and “check in” to the appropriate queue/counter; supports mixed walk-ins + appointments in the same flow.

    - FA: ماژول رزرو وقت/Appointment برای بیزینس‌هایی که نیاز به ثبت تایم دارند (کلینیک/پزشک، خدمات حرفه‌ای، شعب). پشتیبانی از تعریف سرویس‌ها + زمان‌بندی + قالب اسلات‌ها (قوانین دسترسی)، تخصیص منابع (پرسنل/پرووایدر/اتاق)، ظرفیت هر اسلات، و سلف‌سرویس مشتری (رزرو/جابجایی/کنسلی) همراه با تاییدیه و Reminder خودکار برای کاهش no-show. دارای waitlist/backfill جهت پرکردن اسلات‌های خالی‌شده و سیاست‌های قابل تنظیم (حداقل زمان تا نوبت، پنجره کنسلی؛ ودیعه/Deposit در آینده اختیاری). یکپارچه با commerce.queue از طریق Check-in: مراجعه‌کننده وقت‌دار هنگام حضور وارد صف/کانتر مربوط می‌شود و امکان ترکیب Walk-in و Appointment در یک جریان فراهم می‌شود.

- [ ] MI-0011 | Guest Wi-Fi (Captive Portal + OTP/Voucher + Policy + Audit)
  - candidate_module_code: core.guest_wifi
  - proposed_category: core-platform
  - priority: P2
  - dependencies: []
  - platform_compatibility: unknown
  - target_persona: admin
  - core_dependency_risk: no
  - applicable_business_segments: [restaurant, hospitality, retail, medical_clinic, dental, lab_imaging, school, training_institute, fitness_gym, events_exhibitions, government]
  - created_at: 2026-02-12
  - notes:

    - EN: Guest Wi-Fi module providing controlled internet access for visitors via captive portal. Supports login methods per workspace/location: SMS/OTP, voucher/username+password, or simple form + ToS acceptance. Enforce policies: temporary validity (time-based), bandwidth limits, data quotas, device limits, schedules, and optional walled-garden. Must keep audit/reporting to answer “which phone/device was connected at date/time”, including timestamps, device MAC, assigned IP, SSID/location, and session status; retention policy configurable. Integration options: RADIUS-based auth (e.g., MikroTik User Manager / UniFi hotspot captive portal) and/or gateway API adapters. Security baseline: guest network segmentation/isolation from internal LAN. ('Aislelabs'[1])

    - FA: ماژول وای‌فای مهمان برای ارائه اینترنت کنترل‌شده به مراجعین از طریق Captive Portal. روش‌های ورود قابل تنظیم per workspace/location: پیامک/OTP، ووچر/یوزرنیم+پسورد، یا فرم ساده + پذیرش قوانین. اعمال Policy: اعتبار زمان‌دار، محدودیت سرعت، سقف مصرف دیتا، محدودیت تعداد دستگاه، زمان‌بندی و در صورت نیاز walled-garden. ثبت لاگ و گزارش‌گیری برای پاسخ به «در تاریخ/ساعت مشخص چه شماره/دستگاهی وصل بوده» شامل زمان‌ها، MAC، IP، SSID/لوکیشن و وضعیت سشن؛ مدت نگهداری لاگ قابل تنظیم. گزینه‌های اتصال: RADIUS (مثل MikroTik User Manager / UniFi Hotspot) و/یا آداپترهای API. خط پایه امنیتی: جداسازی شبکه مهمان از LAN داخلی. ('Aislelabs'[1])

- [ ] MI-0012 | Feedback & Complaints (Intake + Optional Reply)
  - candidate_module_code: commerce.feedback
  - proposed_category: commerce
  - priority: P2
  - dependencies: [commerce.catalog]
  - platform_compatibility: unknown
  - target_persona: end_user
  - core_dependency_risk: no
  - applicable_business_segments: all
  - created_at: 2026-02-12
  - notes:

    - EN: Simple customer feedback/complaints intake module with omni-channel entry points (QR from catalog/menu, public website link). Collects feedback type (suggestion/complaint/praise), message, optional attachments, and optional contact info (phone/email) with consent. Workspace can choose one-way (intake only) or two-way (reply to customer) mode; replies are sent via SaaS Channels. This module intentionally avoids workflow/SLA/assignment complexity; instead it should be able to integrate/forward records into a future CRM module for case management.

    - FA: ماژول ساده دریافت پیشنهادات/انتقادات/شکایات با ورودی چندکاناله (QR از کاتالوگ/منو، لینک عمومی وب‌سایت). نوع پیام (پیشنهاد/شکایت/تقدیر)، متن، فایل/عکس اختیاری و اطلاعات تماس اختیاری (موبایل/ایمیل) همراه با رضایت را ثبت می‌کند. ورک‌اسپیس می‌تواند حالت یک‌طرفه (فقط دریافت) یا دوطرفه (ارسال پاسخ) را انتخاب کند؛ پاسخ از طریق Channelهای SaaS ارسال می‌شود. این ماژول عمداً وارد SLA/Assign/Workflow نمی‌شود و باید امکان اتصال/ارسال رکوردها به ماژول CRM آینده برای مدیریت کیس را داشته باشد.

- [ ] MI-0013 | Audience/Subscribers (Opt-in Club List)
  - candidate_module_code: commerce.audience
  - proposed_category: commerce
  - priority: P2
  - dependencies: [commerce.customers]
  - platform_compatibility: unknown
  - target_persona: admin
  - core_dependency_risk: no
  - applicable_business_segments: [restaurant, retail, ecommerce_b2c, ecommerce_marketplace_seller, beauty_wellness, fitness_gym, events_exhibitions, travel_agency]
  - created_at: 2026-02-12
  - notes:

    - EN: Lightweight “club/audience” module to collect opt-in phone/email subscribers per workspace for announcements and marketing updates. Supports consent tracking (SMS/email), unsubscribe handling, basic segmentation/tags, and export/targeting via existing SaaS Channels (this module provides the audience; sending is handled by the platform channels). Designed to stay simple (not full CRM).

    - FA: ماژول سبک «باشگاه مشتریان/مخاطبان» برای جمع‌آوری لیست افرادِ رضایت‌داده (موبایل/ایمیل) در سطح ورک‌اسپیس جهت اطلاع‌رسانی و اخبار. شامل ثبت رضایت (SMS/Email)، امکان لغو عضویت، سگمنت/تگ ساده، و استفاده از Channelهای SaaS برای ارسال (این ماژول فقط Audience می‌دهد؛ ارسال توسط پلتفرم انجام می‌شود). طراحی‌شده برای ساده‌ماندن و جایگزین CRM کامل نیست.

- [ ] MI-0014 | Basic Accounting (Standard COA, Locked by User)
  - candidate_module_code: finance.accounting_basic
  - proposed_category: finance
  - priority: P1
  - dependencies: []
  - platform_compatibility: unknown
  - target_persona: admin
  - core_dependency_risk: no
  - applicable_business_segments: all
  - created_at: 2026-02-12
  - notes:

    - EN: Lightweight accounting module based on General Ledger + double-entry journal posting. Uses a standard, system-provided Chart of Accounts (COA) that is NOT editable by the workspace (locked). Must still expose stable account identifiers so other modules can post accounting entries via SaaS Channels/Integration mechanisms. Sales/Inventory/Fixed Assets/Budgeting are explicitly out of scope and handled by separate modules; this module only records GL postings and provides basic financial reports. Data model must be upgrade-safe so a workspace can later enable Advanced Accounting without losing historical entries (journal lines reference account IDs, not mutable codes/names).

    - FA: ماژول حسابداری سبک مبتنی بر دفترکل (GL) و ثبت‌های دوطرفه. از چارت حساب‌های استاندارد و از پیش‌تعریف‌شده استفاده می‌کند که توسط ورک‌اسپیس قابل ویرایش نیست (Locked). با این حال باید شناسه‌های پایدار حساب‌ها را ارائه دهد تا سایر ماژول‌ها بتوانند از طریق مکانیزم Channel/Integration پلتفرم، سند/آرتیکل مالی ثبت کنند. فروش/انبار/دارایی ثابت/بودجه خارج از دامنه این ماژول هستند و ماژول جدا دارند؛ این ماژول فقط ثبت‌های GL و گزارش‌های پایه مالی را پوشش می‌دهد. دیتامدل باید طوری باشد که ارتقاء به حسابداری پیشرفته بدون از دست رفتن سوابق ممکن باشد (ارجاع آرتیکل‌ها به account_id پایدار).

- [ ] MI-0015 | Advanced Accounting (Configurable Account Levels/Hierarchy)
  - candidate_module_code: finance.accounting_advanced
  - proposed_category: finance
  - priority: P1
  - dependencies: [finance.accounting_basic]
  - platform_compatibility: unknown
  - target_persona: admin
  - core_dependency_risk: no
  - applicable_business_segments: [mid_market, enterprise, manufacturing, food_manufacturing, textile_apparel, printing_packaging, machining_workshop, distribution, wholesale, construction_contracting, accounting_tax, corporate_financial_services]
  - created_at: 2026-02-12
  - notes:

    - EN: Advanced accounting module that extends Basic Accounting by enabling workspace-managed Chart of Accounts with hierarchical levels (e.g., parent/child rollups; equivalent to “Kol/Moein/…”) and user-defined account structures for reporting. Core GL posting remains the same (double-entry, journal lines posting to account IDs), but COA becomes configurable by the workspace. Must provide an upgrade path from Basic: retain all historical journal entries; either unlock/extend the existing standard COA or introduce a mapping layer from standard accounts to the customized hierarchy for reporting continuity. Sales/Inventory/Fixed Assets/Budgeting remain separate modules; this module’s key differentiator is editable account hierarchy/levels + reporting rollups.

    - FA: ماژول حسابداری پیشرفته که تفاوت اصلی‌اش با نسخه ساده، امکان تعریف و مدیریت چارت حساب‌ها با ساختار سلسله‌مراتبی و طبقات حساب (معادل کل/معین/…) توسط ورک‌اسپیس است. ماهیت ثبت‌ها همان GL دوطرفه می‌ماند (آرتیکل‌ها به account_id ارجاع می‌دهند)، اما COA قابل پیکربندی می‌شود و رول‌آپ‌های گزارش‌گیری از طریق parent/child امکان‌پذیر است. باید مسیر ارتقاء از Basic داشته باشد: هیچ سندی از بین نرود؛ یا COA استاندارد را unlock/extend کند یا یک mapping برای نگهداری تداوم گزارش‌گیری بین حساب‌های استاندارد و ساختار جدید فراهم کند. فروش/انبار/دارایی ثابت/بودجه همچنان ماژول‌های جدا هستند؛ مزیت کلیدی این ماژول فقط طبقات/سلسله‌مراتب حساب و رول‌آپ گزارش‌هاست.

- [ ] MI-0016 | Integration & API Gateway / Webhooks (هاب یکپارچه‌سازی)
  - candidate_module_code: core.integration_gateway
  - proposed_category: core-platform
  - priority: P1
  - dependencies: []
  - platform_compatibility: unknown
  - target_persona: admin
  - core_dependency_risk: yes
  - applicable_business_segments: all
  - created_at: 2026-02-20
  - notes:

    - EN: Central integration hub for inbound/outbound APIs, webhooks, and event delivery; manages credentials, rate limits, retries, and tenant-scoped connectors/adapters.

    - FA: هاب مرکزی یکپارچه‌سازی برای API و Webhook و انتشار/تحویل رویدادها؛ مدیریت Credential، Rate limit، Retry و کانکتورها/آداپترهای tenant-scoped.

- [ ] MI-0017 | Role-based Access + Audit Log (کنترل دسترسی و لاگ)
  - candidate_module_code: core.rbac_audit
  - proposed_category: core-platform
  - priority: P1
  - dependencies: []
  - platform_compatibility: unknown
  - target_persona: admin
  - core_dependency_risk: yes
  - applicable_business_segments: all
  - created_at: 2026-02-20
  - notes:

    - EN: Workspace RBAC (roles/permissions) plus immutable audit log for security and compliance; supports actor, action, target, timestamp, and retention policy.

    - FA: RBAC در سطح ورک‌اسپیس (نقش/دسترسی) به‌همراه Audit Log غیرقابل‌دستکاری برای امنیت و انطباق؛ شامل actor/action/target/time و سیاست نگهداشت.

- [ ] MI-0018 | Company AI Assistant (دستیار هوش مصنوعی ورک‌اسپیس)
  - candidate_module_code: core.ai_assistant
  - proposed_category: core-platform
  - priority: P2
  - dependencies: [core.integration_gateway]
  - platform_compatibility: unknown
  - target_persona: end_user
  - core_dependency_risk: yes
  - applicable_business_segments: all
  - created_at: 2026-02-20
  - notes:

    - EN: Workspace AI assistant that answers questions over workspace data and suggests actions/automations; must respect RBAC and provide citations/traceability for outputs.

    - FA: دستیار AI برای پرسش‌وپاسخ روی دیتای ورک‌اسپیس و پیشنهاد اقدام/اتوماسیون؛ الزام رعایت RBAC و ارائه ردپا/استناد برای خروجی‌ها.

- [ ] MI-0019 | CRM (Services/Ticketing) (CRM خدمات/تیکتینگ)
  - candidate_module_code: service.crm
  - proposed_category: process
  - priority: P1
  - dependencies: [core.contacts, core.products, core.rbac_audit]
  - platform_compatibility: unknown
  - target_persona: admin
  - core_dependency_risk: no
  - applicable_business_segments: [it_msp, field_service, security_safety_systems, construction_contracting, mep_services, automotive_services, accounting_tax, legal_services, medical_clinic, dental, lab_imaging, property_management, government]
  - created_at: 2026-02-20
  - notes:

    - EN: Service CRM/ticketing with intake, assignment, SLA, statuses, internal notes, and reporting; links tickets to contacts, assets/items, and optional appointments/queue.

    - FA: CRM خدمات/تیکتینگ با ثبت درخواست، تخصیص، SLA، وضعیت‌ها، نوت داخلی و گزارش‌گیری؛ اتصال تیکت به مخاطب، دارایی/آیتم و در صورت نیاز رزرو/صف.

- [ ] MI-0020 | Contracts (in/out) (قراردادهای ورودی/خروجی)
  - candidate_module_code: process.contracts
  - proposed_category: process
  - priority: P1
  - dependencies: [core.contacts, process.workflow_approvals]
  - platform_compatibility: unknown
  - target_persona: admin
  - core_dependency_risk: no
  - applicable_business_segments: all
  - created_at: 2026-02-20
  - notes:

    - EN: Contract lifecycle management for inbound/outbound agreements: templates, versions, approval flow, obligations, renewal alerts, and attachments.

    - FA: مدیریت چرخه عمر قراردادهای ورودی/خروجی: قالب‌ها، نسخه‌ها، گردش تایید، تعهدات، هشدار تمدید و پیوست‌ها.

- [ ] MI-0021 | Workflow & Approvals (گردش‌کار و تاییدیه‌ها)
  - candidate_module_code: process.workflow_approvals
  - proposed_category: process
  - priority: P1
  - dependencies: [core.rbac_audit]
  - platform_compatibility: unknown
  - target_persona: admin
  - core_dependency_risk: yes
  - applicable_business_segments: all
  - created_at: 2026-02-20
  - notes:

    - EN: Configurable workflows and approval chains (rules/conditions/routing) reusable across modules (expenses, procurement, contracts, HR, etc.).

    - FA: موتور گردش‌کار و تاییدیه قابل پیکربندی (قواعد/شرایط/مسیر‌دهی) قابل استفاده مجدد بین ماژول‌ها (هزینه‌ها، خرید، قرارداد، منابع انسانی و…).

- [ ] MI-0022 | Project & Task Management (مدیریت پروژه‌ها و تسک‌ها)
  - candidate_module_code: process.projects_tasks
  - proposed_category: process
  - priority: P2
  - dependencies: [core.contacts, core.rbac_audit]
  - platform_compatibility: unknown
  - target_persona: end_user
  - core_dependency_risk: no
  - applicable_business_segments: [it_msp, construction_contracting, engineering_consulting, marketing_agency, management_consulting]
  - created_at: 2026-02-20
  - notes:

    - EN: Projects, tasks, assignments, statuses, and basic planning views; supports team collaboration and optional workflow approvals for changes.

    - FA: مدیریت پروژه/تسک با تخصیص، وضعیت‌ها و نماهای پایه برنامه‌ریزی؛ همکاری تیمی و در صورت نیاز تاییدیه تغییرات.

- [ ] MI-0023 | Reports / Dashboards / KPI Builder (گزارشات و شاخص‌ها)
  - candidate_module_code: analytics.reports_kpi
  - proposed_category: analytics
  - priority: P1
  - dependencies: []
  - platform_compatibility: unknown
  - target_persona: admin
  - core_dependency_risk: no
  - applicable_business_segments: all
  - created_at: 2026-02-20
  - notes:

    - EN: Self-serve dashboards and KPI builder across modules with scheduling/export and RBAC-aware data access.

    - FA: داشبورد و KPI ساز سلف‌سرویس بین ماژول‌ها با زمان‌بندی/خروجی و رعایت دسترسی‌ها.

- [ ] MI-0024 | Document Management + OCR (مدیریت اسناد + OCR)
  - candidate_module_code: documents.dms_ocr
  - proposed_category: documents
  - priority: P1
  - dependencies: [core.rbac_audit]
  - platform_compatibility: unknown
  - target_persona: admin
  - core_dependency_risk: no
  - applicable_business_segments: all
  - created_at: 2026-02-20
  - notes:

    - EN: Document repository with tagging, versioning, full-text search, and OCR extraction for scans; supports retention and access policies.

    - FA: مخزن اسناد با تگ/نسخه‌بندی/جستجوی متنی و استخراج OCR از اسکن‌ها؛ دارای سیاست نگهداشت و دسترسی.

- [ ] MI-0025 | Treasury / Cash Management (خزانه)
  - candidate_module_code: finance.treasury
  - proposed_category: finance
  - priority: P1
  - dependencies: [finance.accounting_basic]
  - platform_compatibility: unknown
  - target_persona: admin
  - core_dependency_risk: no
  - applicable_business_segments: all
  - created_at: 2026-02-20
  - notes:

    - EN: Cash/bank accounts, cashboxes, transfers, reconciliations, and payment instruments; integrates with accounting postings.

    - FA: مدیریت حساب‌های بانکی/صندوق، انتقال‌ها، مغایرت‌گیری و ابزار پرداخت؛ یکپارچه با ثبت‌های حسابداری.

- [ ] MI-0026 | Cashflow & Liquidity (مدیریت نقدینگی)
  - candidate_module_code: finance.cashflow_liquidity
  - proposed_category: finance
  - priority: P1
  - dependencies: [finance.treasury, finance.ar_ap]
  - platform_compatibility: unknown
  - target_persona: admin
  - core_dependency_risk: no
  - applicable_business_segments: all
  - created_at: 2026-02-20
  - notes:

    - EN: Cashflow forecasting, liquidity snapshots, scenarios, and alerts based on receivables/payables and planned payments.

    - FA: پیش‌بینی جریان نقدی، نمای نقدینگی، سناریوها و هشدارها بر اساس دریافتنی/پرداختنی و پرداخت‌های برنامه‌ریزی‌شده.

- [ ] MI-0027 | Receivables/Payables (AR/AP) (حساب‌های دریافتنی/پرداختنی)
  - candidate_module_code: finance.ar_ap
  - proposed_category: finance
  - priority: P1
  - dependencies: [finance.accounting_basic, core.contacts]
  - platform_compatibility: unknown
  - target_persona: admin
  - core_dependency_risk: no
  - applicable_business_segments: all
  - created_at: 2026-02-20
  - notes:

    - EN: Open-item tracking for invoices/bills, aging, reminders, settlement status; posts summarized entries to GL.

    - FA: مدیریت آیتم‌های باز دریافتنی/پرداختنی، سررسیدها، پیگیری و وضعیت تسویه؛ ارسال ثبت‌های خلاصه به GL.

- [ ] MI-0028 | Credit & Installment Management (مدیریت اعتبارات و اقساط)
  - candidate_module_code: finance.credit_installments
  - proposed_category: finance
  - priority: P2
  - dependencies: [finance.ar_ap, core.contacts]
  - platform_compatibility: unknown
  - target_persona: admin
  - core_dependency_risk: no
  - applicable_business_segments: [retail, dental, automotive_services, beauty_wellness]
  - created_at: 2026-02-20
  - notes:

    - EN: Credit limits, installment plans, schedules, penalties, and delinquency tracking; integrates with AR collection workflow.

    - FA: سقف اعتبار، پلن اقساط، زمان‌بندی، جریمه و مدیریت معوقه؛ یکپارچه با وصول دریافتنی‌ها.

- [ ] MI-0029 | Expense & Reimbursement (هزینه‌ها/ماموریت/صورت‌هزینه)
  - candidate_module_code: finance.expense_reimbursement
  - proposed_category: finance
  - priority: P1
  - dependencies: [process.workflow_approvals, finance.accounting_basic]
  - platform_compatibility: unknown
  - target_persona: end_user
  - core_dependency_risk: no
  - applicable_business_segments: all
  - created_at: 2026-02-20
  - notes:

    - EN: Expense claims with receipt capture, policies, approvals, and reimbursement; posts to treasury/accounting.

    - FA: مدیریت صورت‌هزینه با ثبت رسید، قوانین، تاییدیه و بازپرداخت؛ ارسال به خزانه/حسابداری.

- [ ] MI-0030 | Advance / Petty Cash (تن‌خواه)
  - candidate_module_code: finance.petty_cash
  - proposed_category: finance
  - priority: P2
  - dependencies: [process.workflow_approvals, finance.treasury]
  - platform_compatibility: unknown
  - target_persona: admin
  - core_dependency_risk: no
  - applicable_business_segments: all
  - created_at: 2026-02-20
  - notes:

    - EN: Manage advances/petty cash balances, allocations, settlements, and reconciliations per employee/unit.

    - FA: مدیریت تن‌خواه/علی‌الحساب، تخصیص، تسویه و مغایرت‌گیری به تفکیک فرد/واحد.

- [ ] MI-0031 | Receipts / Vouchers (رسید/سند)
  - candidate_module_code: finance.vouchers
  - proposed_category: finance
  - priority: P2
  - dependencies: [finance.accounting_basic, documents.dms_ocr]
  - platform_compatibility: unknown
  - target_persona: admin
  - core_dependency_risk: no
  - applicable_business_segments: all
  - created_at: 2026-02-20
  - notes:

    - EN: Voucher/receipt entry layer with numbering, attachments, and audit trail; bridges operational docs to accounting entries.

    - FA: لایه ثبت سند/رسید با شماره‌گذاری، پیوست و ردپا؛ پل بین مستندات عملیاتی و ثبت‌های حسابداری.

- [ ] MI-0032 | Asset Register (ثبت دارایی‌ها)
  - candidate_module_code: finance.asset_register
  - proposed_category: finance
  - priority: P2
  - dependencies: [finance.accounting_basic]
  - platform_compatibility: unknown
  - target_persona: admin
  - core_dependency_risk: no
  - applicable_business_segments: all
  - created_at: 2026-02-20
  - notes:

    - EN: Fixed asset registry with lifecycle (acquire/assign/transfer/dispose) and basic depreciation hooks (rules may be extended later).

    - FA: رجیستری دارایی ثابت با چرخه عمر (خرید/تخصیص/انتقال/اسقاط) و قلاب‌های استهلاک پایه (قابل توسعه در آینده).

- [ ] MI-0033 | Time & Attendance (ثبت ورود/خروج)
  - candidate_module_code: people.time_attendance
  - proposed_category: people-ops
  - priority: P1
  - dependencies: [core.contacts, core.rbac_audit]
  - platform_compatibility: unknown
  - target_persona: end_user
  - core_dependency_risk: no
  - applicable_business_segments: all
  - created_at: 2026-02-20
  - notes:

    - EN: Attendance, shifts, clock-in/out, exceptions, and export; supports device integrations later (biometric/mobile/kiosk).

    - FA: حضور و غیاب، شیفت‌ها، ورود/خروج، استثناها و خروجی؛ با قابلیت اتصال به دستگاه‌ها در آینده.

- [ ] MI-0034 | Payroll (Simple) (حقوق و دستمزد ساده)
  - candidate_module_code: people.payroll_basic
  - proposed_category: people-ops
  - priority: P2
  - dependencies: [people.time_attendance, finance.accounting_basic]
  - platform_compatibility: unknown
  - target_persona: admin
  - core_dependency_risk: no
  - applicable_business_segments: all
  - created_at: 2026-02-20
  - notes:

    - EN: Basic payroll calculation and payslips with configurable earnings/deductions; posts aggregated payroll entries to accounting.

    - FA: محاسبه حقوق پایه و فیش حقوقی با آیتم‌های قابل تنظیم؛ ارسال ثبت‌های تجمیعی حقوق به حسابداری.

- [ ] MI-0035 | Payroll (Professional) (حقوق و دستمزد حرفه‌ای)
  - candidate_module_code: people.payroll_pro
  - proposed_category: people-ops
  - priority: P2
  - dependencies: [people.payroll_basic]
  - platform_compatibility: unknown
  - target_persona: admin
  - core_dependency_risk: no
  - applicable_business_segments: [manufacturing, distribution, retail, hospitality, medical_clinic, lab_imaging, government]
  - created_at: 2026-02-20
  - notes:

    - EN: Advanced payroll for complex organizations (multi-branch rules, shift differentials, overtime policies, richer reporting).

    - FA: حقوق و دستمزد پیشرفته برای سازمان‌های پیچیده (قوانین چندشعبه، تفاوت شیفت، اضافه‌کاری، گزارش‌گیری غنی‌تر).

- [ ] MI-0036 | Simple Stock (انبار ساده)
  - candidate_module_code: inventory.stock_simple
  - proposed_category: inventory
  - priority: P1
  - dependencies: [core.products]
  - platform_compatibility: unknown
  - target_persona: admin
  - core_dependency_risk: no
  - applicable_business_segments: [retail, wholesale, distribution, bakery_patisserie, restaurant, agriculture, greenhouse_hydroponics]
  - created_at: 2026-02-20
  - notes:

    - EN: Simple inventory with on-hand quantities, basic in/out movements, and stock count adjustments.

    - FA: انبارداری ساده با موجودی لحظه‌ای، ورود/خروج پایه و اصلاحات انبارگردانی.

- [ ] MI-0037 | Advanced Stock (Multi-warehouse, Lot/Serial, Min/Max) (انبار پیشرفته)
  - candidate_module_code: inventory.stock_advanced
  - proposed_category: inventory
  - priority: P1
  - dependencies: [inventory.stock_simple]
  - platform_compatibility: unknown
  - target_persona: admin
  - core_dependency_risk: no
  - applicable_business_segments: [manufacturing, food_manufacturing, cosmetics_pharma, distribution, logistics_warehousing, import_export]
  - created_at: 2026-02-20
  - notes:

    - EN: Advanced inventory features: multi-warehouse, bins, lot/serial, expiry, min/max, and richer costing hooks.

    - FA: قابلیت‌های انبار پیشرفته: چندانبار، باین، سریال/لات، تاریخ انقضا، حداقل/حداکثر و قلاب‌های بهای تمام‌شده.

- [ ] MI-0038 | Purchasing / Procurement (خرید و تامین‌کننده)
  - candidate_module_code: inventory.procurement
  - proposed_category: inventory
  - priority: P1
  - dependencies: [inventory.stock_advanced, process.workflow_approvals, core.contacts]
  - platform_compatibility: unknown
  - target_persona: admin
  - core_dependency_risk: no
  - applicable_business_segments: [manufacturing, distribution, retail, construction_contracting, mep_services, hospitality, restaurant, cosmetics_pharma]
  - created_at: 2026-02-20
  - notes:

    - EN: Procurement workflow: requisitions, approvals, RFQ/quotes, purchase orders, receiving, and supplier performance notes.

    - FA: فرایند خرید: درخواست خرید، تاییدیه، استعلام/پیشنهاد، سفارش خرید، رسید انبار و ارزیابی تامین‌کننده.

- [ ] MI-0039 | Supplier Portal (پورتال تامین‌کننده)
  - candidate_module_code: inventory.supplier_portal
  - proposed_category: inventory
  - priority: P2
  - dependencies: [inventory.procurement, core.integration_gateway]
  - platform_compatibility: unknown
  - target_persona: end_user
  - core_dependency_risk: no
  - applicable_business_segments: [manufacturing, distribution, wholesale, retail, construction_contracting]
  - created_at: 2026-02-20
  - notes:

    - EN: Supplier self-service portal for onboarding, quote submission, PO acknowledgment, shipment updates, and document exchange.

    - FA: پورتال سلف‌سرویس تامین‌کننده برای ثبت‌نام، ارسال پیشنهاد، تایید PO، آپدیت ارسال و تبادل اسناد.

- [ ] MI-0040 | Inventory Forecasting (پیش‌بینی مصرف/سفارش خرید)
  - candidate_module_code: inventory.forecasting
  - proposed_category: inventory
  - priority: P2
  - dependencies: [inventory.stock_simple, inventory.procurement]
  - platform_compatibility: unknown
  - target_persona: admin
  - core_dependency_risk: no
  - applicable_business_segments: [retail, distribution, manufacturing, food_manufacturing, restaurant, catering, greenhouse_hydroponics]
  - created_at: 2026-02-20
  - notes:

    - EN: Forecast consumption/demand and suggest replenishment; supports seasonality, lead time, and safety stock.

    - FA: پیش‌بینی مصرف/تقاضا و پیشنهاد تامین؛ پشتیبانی از فصلی‌بودن، زمان تامین و موجودی اطمینان.

- [ ] MI-0041 | Fleet & Delivery Management (مدیریت ناوگان و ارسال)
  - candidate_module_code: operations.fleet_delivery
  - proposed_category: operations
  - priority: P2
  - dependencies: [commerce.ordering, inventory.stock_simple]
  - platform_compatibility: unknown
  - target_persona: end_user
  - core_dependency_risk: no
  - applicable_business_segments: [distribution, logistics_warehousing, courier_last_mile, restaurant, field_service, equipment_rental]
  - created_at: 2026-02-20
  - notes:

    - EN: Dispatch, driver assignment, delivery statuses, route planning hooks, and proof-of-delivery; can consume order events.

    - FA: دیسپچ و تخصیص راننده، وضعیت ارسال، قلاب‌های مسیریابی و تایید تحویل؛ قابلیت مصرف رویدادهای سفارش.

- [ ] MI-0042 | Cloud POS (Offline/Online) (پایانه فروش ابری)
  - candidate_module_code: commerce.pos
  - proposed_category: commerce
  - priority: P1
  - dependencies: [core.products, finance.accounting_basic]
  - platform_compatibility: unknown
  - target_persona: end_user
  - core_dependency_risk: no
  - applicable_business_segments: [restaurant, retail, bakery_patisserie]
  - created_at: 2026-02-20
  - notes:

    - EN: POS with offline/online modes, cashier operations, receipts, returns, and sync; integrates with inventory/accounting if enabled.

    - FA: POS با حالت آنلاین/آفلاین، عملیات صندوق، رسید، مرجوعی و همگام‌سازی؛ اتصال به انبار/حسابداری در صورت فعال بودن.

- [ ] MI-0043 | Kitchen Display System (KDS) (نمایشگر آشپزخانه)
  - candidate_module_code: commerce.kds
  - proposed_category: commerce
  - priority: P2
  - dependencies: [commerce.ordering]
  - platform_compatibility: unknown
  - target_persona: end_user
  - core_dependency_risk: no
  - applicable_business_segments: [restaurant, catering, bakery_patisserie]
  - created_at: 2026-02-20
  - notes:

    - EN: Kitchen screen for live orders, preparation stages, batching, and ready/serve signals; supports multiple stations.

    - FA: نمایش زنده سفارش‌ها در آشپزخانه با مراحل آماده‌سازی، دسته‌بندی و اعلام آماده/تحویل؛ پشتیبانی از چند ایستگاه.

- [ ] MI-0044 | Table Management (مدیریت میز/رزرو میز)
  - candidate_module_code: commerce.table_management
  - proposed_category: commerce
  - priority: P2
  - dependencies: [commerce.ordering]
  - platform_compatibility: unknown
  - target_persona: end_user
  - core_dependency_risk: no
  - applicable_business_segments: [restaurant, hospitality]
  - created_at: 2026-02-20
  - notes:

    - EN: Table map/status (free/occupied/reserved), basic reservations, and linkage to ordering contexts (table_id tokens).

    - FA: مدیریت وضعیت میز (خالی/اشغال/رزرو)، رزرو پایه و اتصال به کانتکست سفارش (توکن table_id).

- [ ] MI-0045 | Loyalty & Rewards Engine (وفاداری و پاداش)
  - candidate_module_code: cx.loyalty_rewards
  - proposed_category: cx-marketing
  - priority: P2
  - dependencies: [commerce.customers, commerce.audience]
  - platform_compatibility: unknown
  - target_persona: admin
  - core_dependency_risk: no
  - applicable_business_segments: [restaurant, retail, ecommerce_b2c, ecommerce_marketplace_seller, bakery_patisserie, beauty_wellness, fitness_gym]
  - created_at: 2026-02-20
  - notes:

    - EN: Points, tiers, rewards, coupons, and redemption rules; integrates with POS/ordering for earning and redemption events.

    - FA: امتیاز، سطوح، پاداش/کوپن و قواعد خرج‌کردن؛ اتصال به POS/Ordering برای رویدادهای کسب/مصرف.

- [ ] MI-0046 | Production Simple (تولید ساده)
  - candidate_module_code: production.simple
  - proposed_category: production
  - priority: P2
  - dependencies: [inventory.stock_advanced]
  - platform_compatibility: unknown
  - target_persona: admin
  - core_dependency_risk: no
  - applicable_business_segments: [manufacturing, food_manufacturing, textile_apparel, printing_packaging, machining_workshop]
  - created_at: 2026-02-20
  - notes:

    - EN: Simple work orders and basic material consumption/outputs; focuses on straightforward assembly/manufacturing flows.

    - FA: دستور تولید ساده و ثبت مصرف مواد/خروجی؛ مناسب جریان‌های تولید/مونتاژ ساده.

- [ ] MI-0047 | Production Custom (تولید سفارشی/اختصاصی)
  - candidate_module_code: production.custom
  - proposed_category: production
  - priority: P3
  - dependencies: [production.simple]
  - platform_compatibility: unknown
  - target_persona: admin
  - core_dependency_risk: no
  - applicable_business_segments: [printing_packaging, textile_apparel, machining_workshop, food_manufacturing]
  - created_at: 2026-02-20
  - notes:

    - EN: Make-to-order production with custom specs, job tracking, and tighter linkage to quotes/orders and job costing hooks.

    - FA: تولید سفارشی بر اساس مشخصات سفارش، رهگیری کار و اتصال قوی‌تر به سفارش/پیش‌فاکتور و قلاب‌های هزینه‌یابی.

- [ ] MI-0048 | Quality Checklists (چک‌لیست کیفیت با QR/بارکد)
  - candidate_module_code: operations.quality_checklists
  - proposed_category: operations
  - priority: P2
  - dependencies: [production.simple, service.crm]
  - platform_compatibility: unknown
  - target_persona: end_user
  - core_dependency_risk: no
  - applicable_business_segments: [manufacturing, field_service, construction_contracting, mep_services, security_safety_systems, logistics_warehousing]
  - created_at: 2026-02-20
  - notes:

    - EN: QR/barcode-driven checklists for QA/QC and field inspections; supports evidence attachments and audit trail.

    - FA: چک‌لیست‌های QC با QR/بارکد برای کنترل کیفیت و بازرسی میدانی؛ پشتیبانی از پیوست شواهد و ردپا.

- [ ] MI-0049 | Maintenance / Preventive Maintenance (PM) (نت پیشگیرانه)
  - candidate_module_code: operations.maintenance_pm
  - proposed_category: operations
  - priority: P2
  - dependencies: [finance.asset_register, inventory.stock_simple]
  - platform_compatibility: unknown
  - target_persona: admin
  - core_dependency_risk: no
  - applicable_business_segments: [manufacturing, construction_contracting, mep_services, property_management, security_safety_systems, equipment_rental, automotive_services]
  - created_at: 2026-02-20
  - notes:

    - EN: Preventive maintenance schedules, work orders, parts consumption, and service history per asset; supports reminders and SLA hooks.

    - FA: زمان‌بندی PM، دستورکار، مصرف قطعات و تاریخچه سرویس برای هر دارایی؛ هشدارها و قلاب‌های SLA.

- [ ] MI-0050 | AI Cashflow Risk Watch (هشدار ریسک نقدینگی)
  - candidate_module_code: ai.cashflow_risk_watch
  - proposed_category: ai-addons
  - priority: P2
  - dependencies: [finance.cashflow_liquidity]
  - platform_compatibility: unknown
  - target_persona: admin
  - core_dependency_risk: no
  - applicable_business_segments: all
  - created_at: 2026-02-20
  - notes:

    - EN: AI alerts for abnormal cashflow patterns, missed payments, and risk signals; explains drivers and recommended actions.

    - FA: هشدارهای AI برای الگوهای غیرعادی نقدینگی، ریسک عدم پرداخت و سیگنال‌های خطر؛ همراه با توضیح علت و پیشنهاد اقدام.

- [ ] MI-0051 | AI Ticket Triage (تریاژ هوشمند تیکت)
  - candidate_module_code: ai.ticket_triage
  - proposed_category: ai-addons
  - priority: P2
  - dependencies: [service.crm]
  - platform_compatibility: unknown
  - target_persona: admin
  - core_dependency_risk: no
  - applicable_business_segments: [it_msp, field_service, medical_clinic, dental, beauty_wellness, government]
  - created_at: 2026-02-20
  - notes:

    - EN: Auto-classify tickets (topic/urgency/sentiment) and suggest responses; keeps human approval in the loop.

    - FA: دسته‌بندی خودکار تیکت (موضوع/فوریت/احساسات) و پیشنهاد پاسخ؛ با الزام تایید انسانی.

- [ ] MI-0052 | AI Workforce Scheduler (شیفت‌بندی نیمه‌خودکار)
  - candidate_module_code: ai.workforce_scheduler
  - proposed_category: ai-addons
  - priority: P3
  - dependencies: [people.time_attendance]
  - platform_compatibility: unknown
  - target_persona: admin
  - core_dependency_risk: no
  - applicable_business_segments: [restaurant, hospitality, retail, medical_clinic, lab_imaging, courier_last_mile, events_exhibitions]
  - created_at: 2026-02-20
  - notes:

    - EN: AI-assisted shift suggestions based on demand patterns, constraints, and staff availability; exports to attendance/payroll.

    - FA: پیشنهاد شیفت با کمک AI بر اساس الگوی تقاضا، محدودیت‌ها و دسترسی پرسنل؛ خروجی برای حضور و غیاب/حقوق.

- [ ] MI-0053 | AI Kitchen ETA (پیش‌بینی زمان آماده‌سازی)
  - candidate_module_code: ai.kitchen_eta
  - proposed_category: ai-addons
  - priority: P3
  - dependencies: [commerce.kds, commerce.ordering]
  - platform_compatibility: unknown
  - target_persona: end_user
  - core_dependency_risk: no
  - applicable_business_segments: [restaurant, catering, bakery_patisserie]
  - created_at: 2026-02-20
  - notes:

    - EN: Predict order preparation ETA and balance kitchen workload; updates customer-facing status if enabled.

    - FA: پیش‌بینی ETA آماده‌سازی و بالانس بار کاری آشپزخانه؛ در صورت فعال بودن، بروزرسانی وضعیت مشتری.

- [ ] MI-0054 | AI Inventory Optimizer (بهینه‌ساز هوشمند موجودی)
  - candidate_module_code: ai.inventory_optimizer
  - proposed_category: ai-addons
  - priority: P3
  - dependencies: [inventory.forecasting, inventory.procurement]
  - platform_compatibility: unknown
  - target_persona: admin
  - core_dependency_risk: no
  - applicable_business_segments: [restaurant, catering, retail, distribution, food_manufacturing, greenhouse_hydroponics]
  - created_at: 2026-02-20
  - notes:

    - EN: Optimize reorder points and supplier choices using forecast, lead time, and stockout risk; produces explainable recommendations.

    - FA: بهینه‌سازی نقطه سفارش و انتخاب تامین‌کننده بر اساس پیش‌بینی، زمان تامین و ریسک کمبود؛ پیشنهادهای قابل توضیح.

- [ ] MI-0055 | AI Review Sentiment & Auto-Responder (تحلیل احساسات بازخورد + پاسخ‌یار)
  - candidate_module_code: ai.review_sentiment_autoresponder
  - proposed_category: ai-addons
  - priority: P3
  - dependencies: [commerce.feedback, commerce.audience]
  - platform_compatibility: unknown
  - target_persona: admin
  - core_dependency_risk: no
  - applicable_business_segments: all
  - created_at: 2026-02-20
  - notes:

    - EN: Analyze feedback sentiment and draft response templates; supports routing high-risk complaints to CRM when enabled.

    - FA: تحلیل احساسات بازخورد و تولید پیش‌نویس پاسخ؛ امکان ارجاع شکایات پرریسک به CRM در صورت فعال بودن.
