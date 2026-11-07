from datetime import date, time, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from accounts.models import StudentProfile
from shop.models import Category, Product, ProductImage
from booking.models import BookingService, TimeSlot
from blog.models import BlogCategory, Tag, BlogPost
from repertoire.models import Composition, GatedTutorial
from core.models import SiteSetting, PopupAdvertisement, StudioMetric

User = get_user_model()


class Command(BaseCommand):
    help = 'بذردهی اطلاعات اولیه و واقعی پلتفرم بهاور موزیک (Seed Initial Bahavar Data)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('در حال آغاز بارگذاری داده‌های اولیه...'))

        # 1. Superuser / Bahavar Profile
        bahavar_user, created = User.objects.get_or_create(
            username='bahavar',
            defaults={
                'email': 'bahavar@bahavarmusic.com',
                'phone_number': '09121234567',
                'first_name': 'بهاور',
                'last_name': 'موزیسین',
                'is_staff': True,
                'is_superuser': True,
                'is_verified': True,
                'bio': 'موزیسین، آهنگساز، مدرس ارشد گیتار کلاسیک و فلامنکو و مدیر استودیو ضبط صدا',
            }
        )
        if created:
            bahavar_user.set_password('Bahavar@2026')
            bahavar_user.save()
            self.stdout.write(self.style.SUCCESS('کاربر مدیر بهاور با رمز Bahavar@2026 ایجاد شد.'))

        # 2. Site Settings
        SiteSetting.objects.get_or_create(
            id=1,
            defaults={
                'site_title': 'وب‌سایت رسمی بهاور | موزیسین، آهنگساز و مدرس گیتار',
                'brand_tagline': 'آکادمی تخصصی گیتار، استودیو حرفه‌ای ضبط و تولید موسیقی و فروشگاه تخصصی',
                'about_bahavar': (
                    'بهاور، نوازنده گیتار کلاسیک و فلامنکو، آهنگساز و تولیدکننده موسیقی با بیش از ۱۵ سال تجربه '
                    'در اجرای زنده، تدریس دانشگاهی و آموزشگاهی، و سرپرستی پروژه‌های صوتی در استودیو آکوستیک است.'
                ),
                'phone_number': '02188776655',
                'support_mobile': '09121234567',
                'email': 'info@bahavarmusic.com',
                'studio_address': 'تهران، خیابان ولیعصر، برج نگار، طبقه ۶، استودیو موسیقی بهاور',
                'instagram_handle': 'bahavarmusic',
                'telegram_channel': 'bahavarmusic',
                'youtube_channel': '@BahavarMusicOfficial',
                'soundcloud_url': 'https://soundcloud.com/bahavarmusic',
                'enamad_html_code': '<div class="enamad-badge"><img src="/enamad-badge.png" alt="نماد اعتماد الکترونیکی" /></div>',
            }
        )

        # 3. Popup Ad
        PopupAdvertisement.objects.get_or_create(
            id=1,
            defaults={
                'title': 'ثبت‌نام ترم جدید مسترکلاس فلامنکو و آکوستیک',
                'badge_text': 'ظرفیت محدود - ۳۰٪ تخفیف',
                'subtitle': 'دوره جامع تکنیک‌های دست راست (راسگوادو، آلزاپوا، پیکادو) با استاد بهاور',
                'description': 'با ثبت‌نام آنلاین در این دوره، پکیج نت‌ها و تبلچرهای رسمی اختصاصی قطعات را نیز به رایگان دریافت خواهید کرد.',
                'cta_text': 'مشاهده سرفصل‌ها و رزرو صندلی',
                'cta_link': '/booking',
                'is_active': True,
                'cookie_dismiss_hours': 24,
                'show_delay_seconds': 3,
            }
        )

        # 4. Metrics
        metrics_data = [
            {'label': 'هنرجوی فارغ‌التحصیل', 'value_number': 680, 'suffix': '+', 'icon': 'Users', 'order_index': 1},
            {'label': 'ساعت رکورد در استودیو', 'value_number': 3400, 'suffix': ' ساعت', 'icon': 'Mic', 'order_index': 2},
            {'label': 'قطعه و پارت نت منتشر شده', 'value_number': 120, 'suffix': ' اثر', 'icon': 'Music', 'order_index': 3},
            {'label': 'رضایت هنرجویان و مراجعین', 'value_number': 99, 'suffix': '٪', 'icon': 'Award', 'order_index': 4},
        ]
        for m in metrics_data:
            StudioMetric.objects.get_or_create(label=m['label'], defaults=m)

        # 5. Shop Categories & Products
        cat_guitars, _ = Category.objects.get_or_create(
            slug='guitars',
            defaults={'name': 'ساز و گیتارهای دست‌ساز', 'icon': 'Guitar', 'order_index': 1}
        )
        cat_acc, _ = Category.objects.get_or_create(
            slug='accessories',
            defaults={'name': 'سیم و اکسسوری نوازندگی', 'icon': 'Sliders', 'order_index': 2}
        )
        cat_courses, _ = Category.objects.get_or_create(
            slug='courses',
            defaults={'name': 'دوره‌ها و مسترکلاس‌های دیجیتال', 'icon': 'Video', 'order_index': 3}
        )
        cat_sheets, _ = Category.objects.get_or_create(
            slug='sheet-music',
            defaults={'name': 'کتاب‌های نت و متدهای تخصصی', 'icon': 'BookOpen', 'order_index': 4}
        )

        products_data = [
            {
                'title': 'گیتار فلامنکو دست‌ساز الحمبرا مدل 7FP Flamenco Negra',
                'slug': 'alhambra-7fp-flamenco-negra',
                'category': cat_guitars,
                'product_type': Product.ProductType.PHYSICAL,
                'price': 68500000,
                'discount_price': 64000000,
                'stock_quantity': 3,
                'short_description': 'صفحه رویی صنوبر ماسیو آلمانی، پشت و بغل رزوود هندی با پاسخ‌دهی صدایی رسا و کوبنده.',
                'description': 'این ساز یکی از شاهکارهای کارگاه الحمبرا در اسپانیاست. رگه‌های چوب طبیعی، رزونانس فوق‌العاده در ضربه‌های گلپ و راسگوادو، و اکشن استاندارد زیر ۳ میلی‌متر.',
                'features': ['صفحه تاپ: سالید اسپروس آلمان', 'صفحه بک و ساید: رزوود هندی', 'فینگربرد: آبنوس آفریقایی', 'همراه با هاردکیس اورجینال اسپانیایی'],
                'is_featured': True,
            },
            {
                'title': 'سیم گیتار کلاسیک و فلامنکو ساوارز مدل 500ARJ Corum Alliance',
                'slug': 'savarez-500arj-corum-alliance',
                'category': cat_acc,
                'product_type': Product.ProductType.ACCESSORY,
                'price': 1850000,
                'discount_price': 1650000,
                'stock_quantity': 25,
                'short_description': 'ترکیب تریبل‌های آلیانس کربن با تنشن بالا و بیس‌های کروم نرم و منعطف با دوام صدای طولانی.',
                'description': 'انتخاب همیشگی استاد بهاور برای اجراهای زنده و ضبط استودیویی. تفکیک نت‌های بی‌نقص و پایداری کوک در رطوبت.',
                'features': ['ساخت فرانسه', 'جنس تریبل: کربن کریستال', 'کشش: High / Mixed Tension', 'پوشش ضد اکسیداسیون'],
                'is_featured': True,
            },
            {
                'title': 'دوره جامع ویدئویی تکنیک‌های دست راست در گیتار فلامنکو و آکوستیک',
                'slug': 'masterclass-right-hand-flamenco-acoustic',
                'category': cat_courses,
                'product_type': Product.ProductType.DIGITAL_COURSE,
                'price': 1450000,
                'discount_price': 980000,
                'stock_quantity': 999,
                'short_description': '۱۲ ساعت آموزش ویدیویی با فیلمبرداری ۴ زاویه‌ای فول‌اچ‌دی، بررسی آناتومی دست و سرعت‌بخشی به ضربات.',
                'description': 'در این دوره صفر تا صد آلزاپوا، راسگوادوهای ۴ و ۵ ضربه‌ای، پیکادو با سرعت بالا و طنین تمیز، تریوله و گلپ با تحلیل ریتمیک آموزش داده می‌شود.',
                'features': ['۱۲ فصل ویدیویی با دسترسی مادام‌العمر', 'فایل‌های PDF تبلچر و تمرینات روزانه', 'پشتیبانی و رفع اشکال آنلاین توسط استاد بهاور'],
                'is_featured': True,
            },
            {
                'title': 'کتاب پارتیتور و تبلچر آثار برگزیده موسیقی فلامنکو و اسپانیایی',
                'slug': 'selected-flamenco-masterpieces-book',
                'category': cat_sheets,
                'product_type': Product.ProductType.SHEET_MUSIC,
                'price': 420000,
                'discount_price': 350000,
                'stock_quantity': 15,
                'short_description': 'گردآوری و انگشت‌گذاری شده توسط بهاور همراه با توضیحات تحلیل هارمونی دستگاه‌ها.',
                'description': 'شامل ۲۰ قطعه ماندگار از پاکو دلوسیا، توماتیتو، سابیکاس و تارگا به همراه فایل صوتی نمونه اجرا با تمپوی تمرینی.',
                'features': ['چاپ نفیس با فنربندی سیمی برای قرارگیری آسان روی پوپیتر', 'انگشت‌گذاری دقیق دو دست (P-I-M-A)', 'شامل بارکد صوتی جهت گوش دادن در تلفن همراه'],
                'is_featured': False,
            },
        ]
        for p in products_data:
            Product.objects.get_or_create(slug=p['slug'], defaults=p)

        # 6. Booking Services & Time Slots
        services_data = [
            {
                'title': 'کلاس خصوصی گیتار کلاسیک و فلامنکو',
                'slug': 'private-guitar-lesson',
                'service_type': BookingService.ServiceType.GUITAR_CLASS,
                'duration_minutes': 60,
                'price': 750000,
                'icon': 'Guitar',
                'description': 'آموزش تک‌نفره حضوری در استودیو یا آنلاین با تمرکز بر سونوریته، ریتم‌شناسی، تکنیک‌های پیشرفته و رپرتوار جهانی.',
                'requirements': 'به همراه داشتن ساز شخصی (برای جلسات حضوری) یا وب‌کم و میکروفون باکیفیت (برای آنلاین).',
                'order_index': 1,
            },
            {
                'title': 'ضبط آکوستیک استودیو (وکال و سازهای زهی)',
                'slug': 'studio-acoustic-recording',
                'service_type': BookingService.ServiceType.STUDIO_RECORDING,
                'duration_minutes': 120,
                'price': 1800000,
                'icon': 'Mic',
                'description': 'رکورد در اتاق آکوستیک استاندارد استودیو بهاور مجهز به میکروفون‌های لامپی نویمن (Neumann) و پری‌امپ‌های یونیورسال آئودیو.',
                'requirements': 'آماده بودن اتود و لاین ریتم / بکینگ‌ترک پیش از ورود به استودیو.',
                'order_index': 2,
            },
            {
                'title': 'میکس و مسترینگ تک‌آهنگ یا آلبوم',
                'slug': 'mixing-mastering-services',
                'service_type': BookingService.ServiceType.MIX_MASTER,
                'duration_minutes': 90,
                'price': 3500000,
                'icon': 'Sliders',
                'description': 'پالایش فرکانسی، داینامیک، استریو ایمیجینگ و مسترینگ مطابق استانداردهای روز اسپاتیفای و اپل‌موزیک.',
                'requirements': 'ارسال لاین‌های استم به صورت WAV با سمپل‌ریت 48kHz/24bit بدون کلیپینگ.',
                'order_index': 3,
            },
            {
                'title': 'مشاوره تخصصی، استعدادیابی و خرید ساز',
                'slug': 'consultation-and-assessment',
                'service_type': BookingService.ServiceType.CONSULTATION,
                'duration_minutes': 45,
                'price': 300000,
                'icon': 'MessageCircle',
                'description': 'جلسه تحلیل سطح نوازندگی هنرجو، ارزیابی نقاط قوت و ضعف، برنامه‌ریزی آموزشی و تست ساز پیش از خرید.',
                'requirements': 'اجرای یک اتود یا قطعه دلخواه در ابتدای جلسه.',
                'order_index': 4,
            },
        ]
        today = date.today()
        for s in services_data:
            svc, _ = BookingService.objects.get_or_create(slug=s['slug'], defaults=s)
            # Create slots for the next 7 days
            for day_offset in range(1, 8):
                slot_date = today + timedelta(days=day_offset)
                for start_h, end_h in [(14, 15), (16, 17), (18, 19)]:
                    TimeSlot.objects.get_or_create(
                        service=svc,
                        date=slot_date,
                        start_time=time(start_h, 0),
                        defaults={'end_time': time(end_h, 0), 'is_booked': False}
                    )

        # 7. Blog Categories, Tags & Posts
        bcat_tech, _ = BlogCategory.objects.get_or_create(slug='technique', defaults={'name': 'تکنیک و نوازندگی'})
        bcat_gear, _ = BlogCategory.objects.get_or_create(slug='gear', defaults={'name': 'تجهیزات، سازشناسی و آکوستیک'})
        bcat_theory, _ = BlogCategory.objects.get_or_create(slug='theory', defaults={'name': 'هارمونی و تئوری موسیقی'})

        tag_guitar, _ = Tag.objects.get_or_create(slug='guitar', defaults={'name': 'گیتار'})
        tag_flamenco, _ = Tag.objects.get_or_create(slug='flamenco', defaults={'name': 'فلامنکو'})
        tag_studio, _ = Tag.objects.get_or_create(slug='studio', defaults={'name': 'استودیو'})

        posts_data = [
            {
                'title': 'رازهای دست‌یابی به راسگوادوی روان و قدرتمند در گیتار فلامنکو',
                'slug': 'secrets-of-flamenco-rasgueado',
                'category': bcat_tech,
                'author': bahavar_user,
                'reading_time_minutes': 7,
                'excerpt': 'بررسی ارگونومی دست راست، نحوه رهاسازی انگشتان و تمرینات مرحله‌ای برای دستیابی به راسگوادوی متقارن و بدون کوفتگی عضله.',
                'content': (
                    '### مقدمه\n\n'
                    'تکنیک راسگوادو (Rasgueado) یکی از متمایزترین و هیجان‌انگیزترین مؤلفه‌های صدای گیتار فلامنکو است. '
                    'بسیاری از هنرجویان به دلیل انقباض بیش از حد تاندون‌های اکستنسور ساعد، پس از چند دقیقه احساس خستگی می‌کنند.\n\n'
                    '### ۱. موقعیت مچ و تکیه‌گاه شست\n\n'
                    'شست دست راست باید به عنوان لنگر پایدار روی سیم ششم قرار گیرد تا مچ دست آزادی چرخش حول محور استخوان اولنا را حفظ کند.\n\n'
                    '### ۲. رهاسازی انگشتان به صورت بادبزنی (Abanico)\n\n'
                    'پرتاب انگشتان نباید با زور عضلانی بلکه با رهاسازی سریع تنش ارتجاعی بند اول انگشتان انجام شود.'
                ),
                'meta_title': 'آموزش راسگوادو در گیتار فلامنکو | بهاور موزیک',
                'meta_description': 'تکنیک‌های کلیدی و تمرینات روزانه برای تسلط بر انواع راسگوادو در گیتار فلامنکو به همراه نکات اصلاح ارگونومی دست.',
            },
            {
                'title': 'راهنمای جامع تفاوت چوب صنوبر (Spruce) و سرو (Cedar) در صفحه رویی گیتار',
                'slug': 'spruce-vs-cedar-soundboard-guide',
                'category': bcat_gear,
                'author': bahavar_user,
                'reading_time_minutes': 6,
                'excerpt': 'کدام تاپ‌وود برای سبک نوازندگی شما مناسب‌تر است؟ تحلیل رزونانس، رنگ صوتی و سرعت باز شدن صدای ساز در گذر زمان.',
                'content': (
                    '### انتخاب تاپ‌وود؛ مهم‌ترین تصمیم در خرید ساز\n\n'
                    'بیش از ۷۰ درصد کاراکتر صوتی یک ساز زهی ناشی از ارتعاشات ساندبورد (صفحه رویی) آن است.\n\n'
                    '#### ۱. چوب صنوبر اروپایی (European Spruce)\n'
                    '- صدایی درخشان، شفاف با تفکیک نت‌های بی‌نظیر\n'
                    '- نیاز به نوازندگی مداوم طی ۱ تا ۲ سال جهت رسیدن به اوج پختگی صوتی\n\n'
                    '#### ۲. چوب سدر سرخ کانادایی (Western Red Cedar)\n'
                    '- صدایی گرم، مخملی، با حجم اولیه بسیار بالا حتی از روز اول ساخت ساز'
                ),
                'meta_title': 'مقایسه چوب صنوبر و سدر در گیتار کلاسیک | وبلاگ بهاور',
                'meta_description': 'تحلیل تخصصی تفاوت چوب اسپرووس و سیدر در صفحه رویی گیتار و تأثیر آن بر شفافیت، داینامیک و رنگ صدایی.',
            },
        ]
        for p in posts_data:
            post, _ = BlogPost.objects.get_or_create(slug=p['slug'], defaults=p)
            post.tags.add(tag_guitar, tag_flamenco)

        # 8. Repertoire & Gated Tutorials
        repertoire_data = [
            {
                'title': 'Asturias (Leyenda)',
                'persian_title': 'آستوریاس (افسانه) - تنظیم اختصاصی بهاور',
                'slug': 'asturias-leyenda-bahavar-arrangement',
                'composer': 'Isaac Albéniz',
                'arranger': 'بهاور',
                'genre': Composition.Genre.FLAMENCO,
                'key_signature': 'G minor / D Phrygian',
                'tempo_bpm': 132,
                'duration_display': '06:15',
                'description': 'شاهکار ایساک آلبنیس بازآفرینی شده با حس و حال فلامنکو مدرن، استفاده از تکنیک‌های راسگوادو و ترملوی اصیل.',
                'audio_mp3_url': 'https://cdn.freesound.org/previews/612/612610_5674468-lq.mp3',
                'sheet_music_url': 'https://bahavarmusic.com/sheets/asturias-bahavar-tab.pdf',
                'is_free_sheet_music': True,
                'is_featured': True,
                'play_count': 1420,
                'download_count': 560,
            },
            {
                'title': 'Romance Anónimo',
                'persian_title': 'رومانس گمنام (عشق اسپانیایی)',
                'slug': 'romance-anonimo-spanish-romance',
                'composer': 'Spanish Traditional',
                'arranger': 'بهاور',
                'genre': Composition.Genre.CLASSICAL,
                'key_signature': 'E minor / E major',
                'tempo_bpm': 92,
                'duration_display': '03:40',
                'description': 'یکی از معروف‌ترین و عاشقانه‌ترین قطعات رپرتوار گیتار کلاسیک جهان با ملودی شناور روی آرپژ سیم‌های آزاد.',
                'audio_mp3_url': 'https://cdn.freesound.org/previews/612/612610_5674468-lq.mp3',
                'sheet_music_url': 'https://bahavarmusic.com/sheets/romance-anonimo-tab.pdf',
                'is_free_sheet_music': True,
                'is_featured': True,
                'play_count': 2890,
                'download_count': 1120,
            },
            {
                'title': 'Caravan Melodies',
                'persian_title': 'نوای کاروان (تنظیم آکوستیک بهاور)',
                'slug': 'navaye-karevan-acoustic-arrangement',
                'composer': 'مرتضی محجوبی / تنظیم بهاور',
                'arranger': 'بهاور',
                'genre': Composition.Genre.FOLK_PERSIAN,
                'key_signature': 'شور / دشتی',
                'tempo_bpm': 88,
                'duration_display': '04:55',
                'description': 'تنظیم پلی‌فونیک قطعه ماندگار نوای کاروان برای گیتار نایلون، ترکیب هارمونی‌های غنی اسپانیایی با فواصل ربع‌پرده‌ای دستگاه شور.',
                'audio_mp3_url': 'https://cdn.freesound.org/previews/612/612610_5674468-lq.mp3',
                'sheet_music_url': 'https://bahavarmusic.com/sheets/navaye-karevan-guitar.pdf',
                'is_free_sheet_music': True,
                'is_featured': True,
                'play_count': 1950,
                'download_count': 830,
            },
        ]

        for rep in repertoire_data:
            comp, _ = Composition.objects.get_or_create(slug=rep['slug'], defaults=rep)
            
            # Create Gated Tutorial for Asturias
            if comp.slug == 'asturias-leyenda-bahavar-arrangement':
                GatedTutorial.objects.get_or_create(
                    composition=comp,
                    defaults={
                        'title': 'مسترکلاس ویدیویی گام‌به‌گام اجرای قطعه آستوریاس',
                        'description': 'تحلیل انگشت‌گذاری دقیق میزان به میزان، رفع نقاط عطف ریتمیک در تمپوهای بالا و تنظیم داینامیک ضربات.',
                        'preview_video_url': 'https://www.aparat.com/video/video/embed/videohash/sample/vt/frame',
                        'full_video_url': 'https://stream.bahavarmusic.com/tutorials/asturias-masterclass-full.mp4',
                        'download_video_url': 'https://dl.bahavarmusic.com/tutorials/asturias-masterclass-1080p.zip',
                        'duration_minutes': 55,
                        'price': 240000,
                        'is_free_for_active_students': True,
                    }
                )

        self.stdout.write(self.style.SUCCESS('بارگذاری داده‌های اولیه پلتفرم بهاور با موفقیت به پایان رسید!'))
