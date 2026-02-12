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
  - applicable_business_segments: all
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
  - applicable_business_segments: [restaurant, hospitality, retail, ecommerce_b2c, b2b_commerce]
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
  - applicable_business_segments: [restaurant, hospitality, retail, ecommerce_b2c, b2b_commerce]
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
  - applicable_business_segments: [restaurant, hospitality, retail]
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
  - applicable_business_segments: [banking_finance, healthcare, government, retail, restaurant]
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
  - applicable_business_segments: [restaurant, hospitality, retail, healthcare]
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
  - applicable_business_segments: [healthcare, professional_services, government, banking_finance, retail]
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
  - applicable_business_segments: all
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
