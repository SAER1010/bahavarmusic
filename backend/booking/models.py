import uuid
from django.conf import settings
from django.db import models


class BookingService(models.Model):
    class ServiceType(models.TextChoices):
        GUITAR_CLASS = 'guitar_class', 'کلاس آموزش تخصصی گیتار (حضوری / آنلاین)'
        STUDIO_RECORDING = 'studio_recording', 'ضبط آکوستیک استودیو (وکال و ساز)'
        MIX_MASTER = 'mix_master', 'میکس، مسترینگ و پالایش صدا'
        VIDEO_EDIT = 'video_edit', 'تولید و تدوین موزیک‌ویدیو و تیزر'
        CONSULTATION = 'consultation', 'مشاوره، استعدادیابی و تعیین سطح'

    title = models.CharField(max_length=150, verbose_name='عنوان خدمت')
    slug = models.SlugField(max_length=160, unique=True, allow_unicode=True, verbose_name='اسلاگ URL')
    service_type = models.CharField(
        max_length=30,
        choices=ServiceType.choices,
        default=ServiceType.GUITAR_CLASS,
        verbose_name='نوع سرویس'
    )
    duration_minutes = models.PositiveIntegerField(default=60, verbose_name='مدت زمان هر جلسه (دقیقه)')
    price = models.PositiveBigIntegerField(verbose_name='هزینه سرویس (تومان)')
    description = models.TextField(verbose_name='توضیحات و شرایط رزرو')
    requirements = models.TextField(blank=True, verbose_name='پیش‌نیازها و تجهیزات لازم')
    icon = models.CharField(max_length=50, default='Mic', verbose_name='نام آیکون')
    cover_image = models.ImageField(upload_to='booking/services/', blank=True, null=True, verbose_name='تصویر کاور')
    is_active = models.BooleanField(default=True, verbose_name='فعال برای رزرو')
    order_index = models.PositiveIntegerField(default=0, verbose_name='ترتیب نمایش')

    class Meta:
        verbose_name = 'سرویس رزرو'
        verbose_name_plural = 'سرویس‌های رزرو و استودیو'
        ordering = ['order_index', 'title']

    def __str__(self):
        return f"{self.title} ({self.get_service_type_display()})"


class TimeSlot(models.Model):
    service = models.ForeignKey(
        BookingService,
        on_delete=models.CASCADE,
        related_name='time_slots',
        verbose_name='سرویس مربوطه'
    )
    date = models.DateField(verbose_name='تاریخ نوبت')
    start_time = models.TimeField(verbose_name='ساعت شروع')
    end_time = models.TimeField(verbose_name='ساعت پایان')
    is_booked = models.BooleanField(default=False, verbose_name='رزرو شده')

    class Meta:
        verbose_name = 'سانس زمانی'
        verbose_name_plural = 'سانس‌های زمانی'
        ordering = ['date', 'start_time']
        unique_together = ('service', 'date', 'start_time')

    def __str__(self):
        return f"{self.service.title} - {self.date} ({self.start_time.strftime('%H:%M')} تا {self.end_time.strftime('%H:%M')})"


class Booking(models.Model):
    class BookingStatus(models.TextChoices):
        PENDING = 'pending', 'در انتظار تایید'
        CONFIRMED = 'confirmed', 'تایید شده و قطعی'
        COMPLETED = 'completed', 'برگزار شده'
        CANCELLED = 'cancelled', 'لغو شده'

    booking_code = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        verbose_name='کد رهگیری نوبت'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bookings',
        verbose_name='کاربر ثبت‌کننده'
    )
    service = models.ForeignKey(
        BookingService,
        on_delete=models.CASCADE,
        related_name='bookings',
        verbose_name='سرویس انتخابی'
    )
    time_slot = models.ForeignKey(
        TimeSlot,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='booking_records',
        verbose_name='سانس رزرو'
    )
    date = models.DateField(verbose_name='تاریخ رزرو')
    start_time = models.TimeField(verbose_name='ساعت شروع')
    client_name = models.CharField(max_length=120, verbose_name='نام متقاضی')
    client_phone = models.CharField(max_length=15, verbose_name='شماره تماس متقاضی')
    client_email = models.EmailField(blank=True, null=True, verbose_name='ایمیل متقاضی')
    status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING,
        verbose_name='وضعیت نوبت'
    )
    notes = models.TextField(blank=True, verbose_name='توضیحات و اهداف جلسه / پروژه')
    total_fee = models.PositiveBigIntegerField(default=0, verbose_name='مبلغ پرداختی / بیعانه (تومان)')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')

    class Meta:
        verbose_name = 'رزرو نوبت'
        verbose_name_plural = 'رزروهای نوبت و استودیو'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.booking_code:
            self.booking_code = f"BK-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"رزرو {self.booking_code} - {self.client_name} ({self.service.title})"
