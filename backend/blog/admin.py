from django.contrib import admin
from .models import BlogCategory, BlogComment, BlogPost, Tag


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class BlogCommentInline(admin.TabularInline):
    model = BlogComment
    extra = 0
    readonly_fields = ('user_name', 'user_email', 'created_at')


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'reading_time_minutes', 'is_published', 'view_count', 'published_at')
    list_filter = ('is_published', 'category', 'published_at')
    search_fields = ('title', 'excerpt', 'content')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    inlines = [BlogCommentInline]

    fieldsets = (
        ('محتوای مقاله', {'fields': ('title', 'slug', 'category', 'tags', 'author', 'excerpt', 'content', 'featured_image')}),
        ('تنظیمات انتشار', {'fields': ('is_published', 'published_at', 'reading_time_minutes')}),
        ('سئو و متادیتا', {'fields': ('meta_title', 'meta_description')}),
    )


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'post', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('user_name', 'comment', 'post__title')
