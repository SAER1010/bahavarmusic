from django.contrib import admin
from .models import Composition, GatedTutorial, TutorialAccess


class GatedTutorialInline(admin.StackedInline):
    model = GatedTutorial
    extra = 0
    verbose_name = 'آموزش ویدیویی قفل‌دار (Gated)'
    verbose_name_plural = 'آموزش ویدیویی پیوست شده به این قطعه'


@admin.register(Composition)
class CompositionAdmin(admin.ModelAdmin):
    list_display = ('persian_title', 'title', 'genre', 'composer', 'is_free_sheet_music', 'play_count', 'download_count', 'is_featured')
    list_filter = ('genre', 'is_free_sheet_music', 'is_featured', 'created_at')
    search_fields = ('persian_title', 'title', 'composer', 'arranger', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [GatedTutorialInline]


@admin.register(GatedTutorial)
class GatedTutorialAdmin(admin.ModelAdmin):
    list_display = ('title', 'composition', 'duration_minutes', 'price', 'is_free_for_active_students')
    search_fields = ('title', 'composition__persian_title')


@admin.register(TutorialAccess)
class TutorialAccessAdmin(admin.ModelAdmin):
    list_display = ('user', 'tutorial', 'order_reference', 'granted_at')
    list_filter = ('granted_at',)
    search_fields = ('user__username', 'tutorial__title', 'order_reference')
