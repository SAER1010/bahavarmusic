from django.db import models


class SiteSetting(models.Model):
    site_title = models.CharField(max_length=150, default='وب‌سایت رسمی بهاور | موزیسین، آهنگساز و مدرس گیتار', verbose_name='عنوان سایت')
    brand_tagline = models.CharField(max_length=250, default='پلتفرم جامع آموزش موسیقی، خدمات استودیو آکوستیک و فروشگاه ادوات نوازندگی', verbose_name='شعار برند')
    about_bahavar = models.TextField(verbose_name='درباره بهاور (بیوگرافی رسمی)')
    phone_number = models.CharField(max_length=20, default='02188001234', verbose_name='شماره تماس استودیو')
    support_mobile = models.CharField(max_length=15, default='09121234567', verbose_name='شماره واتساپ و پشتیبانی')
    email = models.EmailField(default='contact@bahavarmusic.com', verbose_name='ایمیل ارتباطی')
    studio_address = models.CharField(max_length=255, default='تهران، خیابان ولیعصر، نرسیده به میدان ونک، برج نگار، استودیو بهاور', verbose_name='نشانی استودیو')
    
    # Social links
    instagram_handle = models.CharField(max_length=100, default='bahavar_music', verbose_name='آیدی اینستاگرام')
    telegram_channel = models.CharField(max_length=100, default='bahavarmusic', verbose_name='کانال تلگرام')
    youtube_channel = models.CharField(max_length=100, default='@BahavarMusic', verbose_name='کانال یوتیوب')
    soundcloud_url = models.URLField(blank=True, default='https://soundcloud.com/bahavar', verbose_name='پروفایل ساندکلاد')

    # Legal & Trust Badges
    enamad_html_code = models.TextField(blank=True, default='<!-- نماد اعتماد الکترونیکی ای‌نماد -->', verbose_name='کد اسکریپت / آی‌فریم اینماد')
    samandehi_code = models.TextField(blank=True, verbose_name='کد ساماندهی')

    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')

    class Meta:
        verbose_name = 'تنظیمات کلی وب‌سایت'
        verbose_name_plural = 'تنظیمات کلی وب‌سایت'

    def __str__(self):
        return self.site_title


class PopupAdvertisement(models.Model):
    title = models.CharField(max_length=150, verbose_name='عنوان پاپ‌آپ تبلیغاتی')
    badge_text = models.CharField(max_length=50, default='تخفیف ویژه دوره جامع', verbose_name='بج / برچسب پاپ‌آپ')
    subtitle = models.CharField(max_length=200, blank=True, verbose_name='زیرعنوان')
    description = models.TextField(verbose_name='توضیحات و متن جذاب تبلیغاتی')
    image = models.ImageField(upload_to='core/popups/', blank=True, null=True, verbose_name='تصویر پاپ‌آپ')
    cta_text = models.CharField(max_length=60, default='مشاهده و ثبت‌نام با تخفیف', verbose_name='متن دکمه اکشن (CTA)')
    cta_link = models.CharField(max_length=255, default='/shop', verbose_name='لینک دکمه اکشن')
    is_active = models.BooleanField(default=True, verbose_name='فعال بودن پاپ‌آپ')
    cookie_dismiss_hours = models.PositiveIntegerField(default=24, verbose_name='مدت پنهان ماندن پس از بستن (ساعت)')
    show_delay_seconds = models.PositiveIntegerField(default=3, verbose_name='تاخیر نمایش پس از ورود به سایت (ثانیه)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'پاپ‌آپ تبلیغاتی'
        verbose_name_plural = 'پاپ‌آپ‌های تبلیغاتی و اطلاعیه‌ها'
        ordering = ['-is_active', '-created_at']

    def __str__(self):
        return f"{self.title} ({'فعال' if self.is_active else 'غیرفعال'})"


class StudioMetric(models.Model):
    label = models.CharField(max_length=100, verbose_name='عنوان شاخص (مثال: هنرجوی فارغ‌التحصیل)')
    value_number = models.PositiveIntegerField(verbose_name='عدد مقدار (مثال: 450)')
    suffix = models.CharField(max_length=20, default='+', verbose_name='پسوند (مثال: + یا ساعت)')
    icon = models.CharField(max_length=50, default='Award', verbose_name='نام آیکون')
    order_index = models.PositiveIntegerField(default=0, verbose_name='ترتیب')

    class Meta:
        verbose_name = 'شاخص و دستاورد'
        verbose_name_plural = 'شاخص‌ها و آمار موفقیت استودیو'
        ordering = ['order_index']

    def __str__(self):
        return f"{self.label}: {self.value_number}{self.suffix}"
