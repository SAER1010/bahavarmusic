from django.contrib import admin
from .models import PopupAdvertisement, SiteSetting, StudioMetric


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('site_title', 'phone_number', 'email', 'updated_at')

    def has_add_permission(self, request):
        # Only allow 1 site setting record
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(PopupAdvertisement)
class PopupAdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'badge_text', 'is_active', 'cookie_dismiss_hours', 'show_delay_seconds', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'subtitle', 'description')


@admin.register(StudioMetric)
class StudioMetricAdmin(admin.ModelAdmin):
    list_display = ('label', 'value_number', 'suffix', 'icon', 'order_index')
    list_editable = ('order_index',)
