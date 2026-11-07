from django.contrib import admin
from .models import Booking, BookingService, TimeSlot


class TimeSlotInline(admin.TabularInline):
    model = TimeSlot
    extra = 3
    verbose_name = 'سانس زمانی'
    verbose_name_plural = 'سانس‌های زمانی این خدمت'


@admin.register(BookingService)
class BookingServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'service_type', 'duration_minutes', 'price', 'is_active', 'order_index')
    list_filter = ('service_type', 'is_active')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [TimeSlotInline]


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('service', 'date', 'start_time', 'end_time', 'is_booked')
    list_filter = ('service', 'date', 'is_booked')
    search_fields = ('service__title',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_code', 'client_name', 'client_phone', 'service', 'date', 'start_time', 'status', 'total_fee')
    list_filter = ('status', 'service', 'date', 'created_at')
    search_fields = ('booking_code', 'client_name', 'client_phone', 'client_email')
    readonly_fields = ('booking_code', 'created_at')
