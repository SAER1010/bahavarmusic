from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import OTPVerification, StudentProfile, User


class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False
    verbose_name = 'پروفایل هنرجویی'
    verbose_name_plural = 'پروفایل‌های هنرجویی'
    extra = 0


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'phone_number', 'email', 'first_name', 'last_name', 'is_verified', 'is_staff')
    list_filter = ('is_verified', 'is_staff', 'is_superuser', 'created_at')
    search_fields = ('username', 'phone_number', 'email', 'first_name', 'last_name')
    ordering = ('-created_at',)
    inlines = [StudentProfileInline]

    fieldsets = (
        ('اطلاعات ورود و پایه', {'fields': ('username', 'password', 'phone_number', 'email')}),
        ('اطلاعات فردی', {'fields': ('first_name', 'last_name', 'avatar', 'bio', 'national_id')}),
        ('وضعیت و دسترسی‌ها', {'fields': ('is_active', 'is_verified', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('تاریخ‌ها', {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created_at', 'expires_at', 'is_used', 'is_valid')
    list_filter = ('is_used', 'created_at')
    search_fields = ('phone_number', 'code')
    readonly_fields = ('created_at',)


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'instrument', 'skill_level', 'attended_sessions_count', 'updated_at')
    list_filter = ('instrument', 'skill_level')
    search_fields = ('user__username', 'user__phone_number', 'user__first_name', 'user__last_name')
