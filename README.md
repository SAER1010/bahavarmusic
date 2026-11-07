# 🎸 پلتفرم جامع موسیقی «بهاور» (Bahavar Music Platform)

وب‌سایت و سامانه یکپارچه آکادمی موسیقی، استودیو صدابرداری آکوستیک، آرشیو رپرتوار و فروشگاه تخصصی گیتار بهاور (`bahavarmusic`).

---

## 🏗 معماری و فناوری‌ها (Tech Stack)

### بک‌اند (Backend)
- **Django 5.1 & Django REST Framework (DRF)**
- **احراز هویت:** SimpleJWT + پشتیبانی دوگانه از لاگین با کد یکبار مصرف پیامکی (OTP) و نام کاربری/رمز عبور
- **پایگاه‌داده:** PostgreSQL 16 با فال‌بک اتوماتیک به SQLite جهت تست‌های سریع محلی
- **مدیریت فایل و مدیا:** ادغام با `django-storages` سازگار با فضای ذخیره‌سازی ابری ArvanCloud / S3 / MinIO
- **پنل مدیریت:** Django Admin بومی‌سازی شده به زبان فارسی با راست‌چین کامل (RTL)

### فرانت‌اند (Frontend)
- **Nuxt 3 با SSR فعال (Server-Side Rendering)** جهت رتبه‌گیری عالی در موتورهای جستجو (Deep SEO)
- **طراحی و استایل:** Tailwind CSS با پالت رنگی گرم و ملهم از چوب گیتارهای اسپانیایی (Amber / Cedar / Spruce)
- **حالت‌های رنگی:** Nuxt ColorMode (تاریک / روشن)
- **مدیریت وضعیت:** Pinia Store (سبد خرید و مدیریت توکن‌های کاربر)
- **آیکون‌ها:** Lucide Icons (`lucide-vue-next`)
- **سئو ساخت‌یافته:** تزریق خودکار متادیتا و اسکیماهای استاندارد Schema.org (`Person`, `MusicComposition`, `Product`, `Course`, `Article`)

### زیرساخت و دوآپس (DevOps & Containerization)
- **Docker & Docker Compose:** راه‌اندازی چهار سرویس مستقل `db`، `web`، `frontend` و `nginx`
- **Nginx Reverse Proxy:** توزیع بار، کش استاتیک‌ها، لود بالانسینگ و فشرده‌سازی Gzip

---

## 📁 ساختار پوشه‌ها و ماژول‌ها

```
Bahavar-Music/
├── backend/
│   ├── config/              # تنظیمات اصلی جنگو، روت‌ها و ASGI/WSGI
│   ├── accounts/            # احراز هویت، کاربر سفارشی، OTP و پروفایل هنرجویان
│   ├── shop/                # محصولات، سازها، سفارشات، سبد خرید و درگاه پرداخت
│   ├── booking/             # سیستم رزرو نوبت کلاس، استودیو آکوستیک و مشاوره
│   ├── blog/                # مقالات سئو شده، دسته‌بندی‌ها و دیدگاه‌ها
│   ├── repertoire/          # رپرتوار آثار، دانلود رایگان نت/تبلچر و آموزش‌های گیتد شده
│   ├── core/                # تنظیمات کلی، پاپ‌آپ تبلیغاتی، شاخص‌ها و بذر داده‌ها
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── assets/css/          # استایل‌های سراسری، انیمیشن امواج صوتی
│   ├── components/          # کامپوننت‌های ماژولار (پلیر صوتی، پلیر ویدیوی گیتد، هدر شیشه‌ای و ...)
│   ├── composables/         # هوک‌های سراسری (useApi, useSeoSchema)
│   ├── layouts/             # لایه اصلی سایت (default.vue)
│   ├── pages/               # صفحات Nuxt 3 (صفحه نخست، فروشگاه، رپرتوار، رزرو، وبلاگ، پرتال)
│   ├── server/routes/       # تولید خودکار robots.txt و sitemap.xml
│   ├── stores/              # استورهای Pinia (احراز هویت و سبد خرید)
│   ├── nuxt.config.ts
│   ├── tailwind.config.ts
│   └── package.json
├── docker/
│   ├── Dockerfile.backend   # ایمیج بهینه پایتون ۳.۱۲
│   ├── Dockerfile.frontend  # ایمیج چندمرحله‌ای نود ۲۲ و خروجی نیترو
│   ├── entrypoint.backend.sh# اسکریپت مایگریشن، جمع‌آوری استاتیک و لود داده‌ها
│   └── nginx.conf           # پیکربندی ریورس پروکسی و کش
├── docker-compose.yml       # استقرار یکپارچه کانتینرها
├── .env.example             # نمونه متغیرهای محیطی
└── .gitignore
```

---

## 🚀 راه‌اندازی با داکر (Production-Ready)

جهت اجرای کامل پروژه با تمام کانتینرها:

```bash
# ۱. کپی کردن متغیرهای محیطی
cp .env.example .env

# ۲. بیلد و اجرای کانتینرها
docker compose up -d --build

# ۳. بررسی وضعیت سرویس‌ها
docker compose ps
```

پس از بالا آمدن کانتینرها:
- **پلتفرم اصلی و وب‌سایت:** `http://localhost`
- **پنل مدیریت جنگو:** `http://localhost/admin/`
- **مستندات و روت‌های API:** `http://localhost/api/`

---

## 🔑 اطلاعات ورود پیش‌فرض (مدیر و هنرجوی نمونه)

هنگام اولین راه‌اندازی با دستور `seed_bahavar_data`، کاربر مدیر و اطلاعات زیر به طور خودکار بارگذاری می‌شوند:

- **نام کاربری ادمین:** `bahavar`
- **رمز عبور ادمین:** `Bahavar@2026`
- **ورود سریع آزمایشی با OTP:** وارد کردن شماره `09121234567` با کد آزمایشی نمایش داده شده

---

## 🛠 راه‌اندازی محلی جهت توسعه (Local Dev)

### اجرای بک‌اند جنگو:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_bahavar_data
python manage.py runserver 0.0.0.0:8000
```

### اجرای فرانت‌اند ناکست:
```bash
cd frontend
npm install
npm run dev
```
سایت در آدرس `http://localhost:3000` در دسترس خواهد بود.

---

## 🌿 ساختار شاخه‌های گیت (Git Workflow)
- شاخه `main`: کد پایدار، تست شده و آماده استقرار پروداکشن
- شاخه `saer`: شاخه فعال توسعه و ویژگی‌های جدید
