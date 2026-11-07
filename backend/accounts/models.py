from datetime import timedelta
import random
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """
    Custom user model supporting authentication via either Phone Number or Email/Username.
    """
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        blank=True,
        db_index=True,
        verbose_name='شماره موبایل'
    )
    email = models.EmailField(
        unique=True,
        null=True,
        blank=True,
        verbose_name='ایمیل'
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='تصویر پروفایل'
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='بیوگرافی یا توضیحات'
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name='احراز هویت شده'
    )
    national_id = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name='کد ملی'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ عضویت'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='آخرین بروزرسانی'
    )

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'
        ordering = ['-created_at']

    def __str__(self):
        if self.get_full_name():
            return f"{self.get_full_name()} ({self.phone_number or self.username})"
        return self.phone_number or self.username or self.email or f"User #{self.id}"


class OTPVerification(models.Model):
    """
    One-Time Password model for passwordless login and mobile verification.
    """
    phone_number = models.CharField(
        max_length=15,
        db_index=True,
        verbose_name='شماره موبایل'
    )
    code = models.CharField(
        max_length=6,
        verbose_name='کد یکبار مصرف'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )
    expires_at = models.DateTimeField(
        verbose_name='تاریخ انقضا'
    )
    is_used = models.BooleanField(
        default=False,
        verbose_name='استفاده شده'
    )

    class Meta:
        verbose_name = 'کد تایید OTP'
        verbose_name_plural = 'کدهای تایید OTP'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=2)
        if not self.code:
            self.code = f"{random.randint(100000, 999999)}"
        super().save(*args, **kwargs)

    @property
    def is_valid(self):
        return not self.is_used and timezone.now() <= self.expires_at

    def __str__(self):
        return f"OTP for {self.phone_number} - Code: {self.code}"


class StudentProfile(models.Model):
    """
    Detailed profile for music students enrolled in Bahavar's courses or masterclasses.
    """
    class SkillLevel(models.TextChoices):
        BEGINNER = 'beginner', 'مقدماتی (صفر تا صد)'
        INTERMEDIATE = 'intermediate', 'متوسط (تکنیک و قطعه‌نوازی)'
        ADVANCED = 'advanced', 'پیشرفته (بداهه‌نوازی و تحلیل هارمونی)'
        PROFESSIONAL = 'professional', 'حرفه‌ای و کنسرت‌نوازی'

    class PreferredInstrument(models.TextChoices):
        CLASSICAL_GUITAR = 'classical', 'گیتار کلاسیک'
        FLAMENCO_GUITAR = 'flamenco', 'گیتار فلامنکو'
        ACOUSTIC_GUITAR = 'acoustic', 'گیتار آکوستیک'
        ELECTRIC_GUITAR = 'electric', 'گیتار الکتریک'
        COMPOSITION = 'composition', 'آهنگسازی و تنظیم'
        MUSIC_PRODUCTION = 'production', 'تولید موسیقی و استودیو'

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile',
        verbose_name='کاربر'
    )
    instrument = models.CharField(
        max_length=30,
        choices=PreferredInstrument.choices,
        default=PreferredInstrument.CLASSICAL_GUITAR,
        verbose_name='ساز تخصصی / شاخه'
    )
    skill_level = models.CharField(
        max_length=20,
        choices=SkillLevel.choices,
        default=SkillLevel.BEGINNER,
        verbose_name='سطح نوازندگی'
    )
    learning_goals = models.TextField(
        blank=True,
        null=True,
        verbose_name='اهداف یادگیری و یادداشت استاد'
    )
    attended_sessions_count = models.PositiveIntegerField(
        default=0,
        verbose_name='تعداد جلسات برگزار شده'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='بروزرسانی')

    class Meta:
        verbose_name = 'پروفایل هنرجو'
        verbose_name_plural = 'پروفایل‌های هنرجویان'

    def __str__(self):
        return f"پروفایل {self.user} - {self.get_instrument_display()}"
