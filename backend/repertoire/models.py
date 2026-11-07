from django.conf import settings
from django.db import models


class Composition(models.Model):
    class Genre(models.TextChoices):
        FLAMENCO = 'flamenco', 'فلامنکو (سولئا، بولریاس، تارانتا)'
        CLASSICAL = 'classical', 'کلاسیک و رنسانس'
        ACOUSTIC_FUSION = 'acoustic_fusion', 'آکوستیک و فیوژن معاصر'
        FOLK_PERSIAN = 'folk_persian', 'نواها و تنظیم‌های محلی و اصیل ایرانی'
        ORIGINAL = 'original', 'آهنگسازی اختصاصی بهاور'

    title = models.CharField(max_length=200, verbose_name='عنوان لاتین / بین‌المللی')
    persian_title = models.CharField(max_length=200, verbose_name='عنوان فارسی قطعه')
    slug = models.SlugField(max_length=220, unique=True, allow_unicode=True, verbose_name='اسلاگ URL')
    composer = models.CharField(max_length=150, default='بهاور', verbose_name='آهنگساز')
    arranger = models.CharField(max_length=150, default='بهاور', verbose_name='تنظیم‌کننده')
    genre = models.CharField(
        max_length=30,
        choices=Genre.choices,
        default=Genre.FLAMENCO,
        verbose_name='سبک / دستگاه'
    )
    key_signature = models.CharField(max_length=20, default='A minor', verbose_name='گام و تنالیته')
    tempo_bpm = models.PositiveSmallIntegerField(default=120, verbose_name='تمپو (BPM)')
    duration_display = models.CharField(max_length=10, default='03:45', verbose_name='طول قطعه (دقیقه:ثانیه)')
    description = models.TextField(verbose_name='داستان و توضیحات ساختاری قطعه')
    cover_image = models.ImageField(upload_to='repertoire/covers/', blank=True, null=True, verbose_name='تصویر کاور قطعه')
    
    # Audio previews
    audio_mp3_url = models.URLField(blank=True, verbose_name='لینک استریم صوتی MP3 (خارجی/CDN)')
    audio_file = models.FileField(upload_to='repertoire/audio/', blank=True, null=True, verbose_name='فایل صوتی MP3 آپلود شده')
    
    # Free or paid Sheet Music & Tabs
    sheet_music_pdf = models.FileField(upload_to='repertoire/sheets/', blank=True, null=True, verbose_name='فایل PDF نت (پارتیتور)')
    tabs_pdf = models.FileField(upload_to='repertoire/tabs/', blank=True, null=True, verbose_name='فایل PDF تبلچر و فینگرینگ')
    sheet_music_url = models.URLField(blank=True, verbose_name='لینک مستقیم دانلود نت PDF')
    
    is_free_sheet_music = models.BooleanField(default=True, verbose_name='دانلود نت رایگان است')
    sheet_price = models.PositiveBigIntegerField(default=0, verbose_name='قیمت نت در صورت غیررایگان بودن (تومان)')
    
    play_count = models.PositiveIntegerField(default=0, verbose_name='تعداد دفعات شنیده شده')
    download_count = models.PositiveIntegerField(default=0, verbose_name='تعداد دانلود نت')
    is_featured = models.BooleanField(default=False, verbose_name='قطعه منتخب صفحه نخست')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درج')

    class Meta:
        verbose_name = 'قطعه موسیقی'
        verbose_name_plural = 'رپرتوار و آثار موسیقی'
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return f"{self.persian_title} ({self.title}) - {self.composer}"

    @property
    def audio_stream_url(self):
        if self.audio_file:
            return self.audio_file.url
        return self.audio_mp3_url or 'https://cdn.freesound.org/previews/612/612610_5674468-lq.mp3'


class GatedTutorial(models.Model):
    composition = models.OneToOneField(
        Composition,
        on_delete=models.CASCADE,
        related_name='gated_tutorial',
        verbose_name='قطعه مربوطه'
    )
    title = models.CharField(max_length=200, verbose_name='عنوان آموزش ویدیویی')
    description = models.TextField(verbose_name='سرفصل‌ها و توضیحات آموزش')
    preview_video_url = models.URLField(verbose_name='لینک ویدیو تیزر رایگان (آپارات یا یوتیوب/CDN)')
    full_video_url = models.URLField(verbose_name='لینک جریان ویدیوی امن کامل (گیتد شده)')
    download_video_url = models.URLField(blank=True, verbose_name='لینک دانلود مستقیم ویدیوی باکیفیت')
    duration_minutes = models.PositiveIntegerField(default=45, verbose_name='مدت زمان آموزش (دقیقه)')
    price = models.PositiveBigIntegerField(default=180000, verbose_name='هزینه خرید آموزش (تومان)')
    is_free_for_active_students = models.BooleanField(default=True, verbose_name='رایگان برای هنرجویان فعال آکادمی')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'آموزش ویدیویی گیتد'
        verbose_name_plural = 'آموزش‌های ویدیویی قفل‌دار (Gated Tutorials)'

    def __str__(self):
        return f"مسترکلاس {self.title} - {self.composition.persian_title}"


class TutorialAccess(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tutorial_accesses',
        verbose_name='کاربر خریدار'
    )
    tutorial = models.ForeignKey(
        GatedTutorial,
        on_delete=models.CASCADE,
        related_name='access_grants',
        verbose_name='آموزش ویدیویی'
    )
    order_reference = models.CharField(max_length=100, blank=True, verbose_name='شماره سفارش یا ارجاع')
    granted_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ اعطا دسترسی')

    class Meta:
        verbose_name = 'مجوز دسترسی به آموزش'
        verbose_name_plural = 'مجوزهای دسترسی به آموزش‌ها'
        unique_together = ('user', 'tutorial')

    def __str__(self):
        return f"دسترسی {self.user.username} به {self.tutorial.title}"
