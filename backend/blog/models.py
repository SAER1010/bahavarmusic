from django.conf import settings
from django.db import models
from django.utils import timezone


class BlogCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام دسته')
    slug = models.SlugField(max_length=120, unique=True, allow_unicode=True, verbose_name='اسلاگ URL')
    description = models.TextField(blank=True, verbose_name='توضیح دسته')

    class Meta:
        verbose_name = 'دسته‌بندی مقاله'
        verbose_name_plural = 'دسته‌بندی‌های مقالات'
        ordering = ['name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='نام برچسب')
    slug = models.SlugField(max_length=60, unique=True, allow_unicode=True, verbose_name='اسلاگ URL')

    class Meta:
        verbose_name = 'برچسب'
        verbose_name_plural = 'برچسب‌ها'

    def __str__(self):
        return f"#{self.name}"


class BlogPost(models.Model):
    title = models.CharField(max_length=250, verbose_name='عنوان مقاله')
    slug = models.SlugField(max_length=270, unique=True, allow_unicode=True, verbose_name='اسلاگ URL')
    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts',
        verbose_name='دسته‌بندی'
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts', verbose_name='برچسب‌ها')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='blog_posts',
        verbose_name='نویسنده'
    )
    excerpt = models.CharField(max_length=350, verbose_name='چکیده مقاله (برای پیش‌نمایش و سئو)')
    content = models.TextField(verbose_name='متن کامل مقاله (فرمت Markdown یا HTML)')
    featured_image = models.ImageField(upload_to='blog/covers/', blank=True, null=True, verbose_name='تصویر شاخص')
    reading_time_minutes = models.PositiveSmallIntegerField(default=5, verbose_name='زمان تخمینی مطالعه (دقیقه)')
    is_published = models.BooleanField(default=True, verbose_name='منتشر شده')
    published_at = models.DateTimeField(default=timezone.now, verbose_name='تاریخ انتشار')
    view_count = models.PositiveIntegerField(default=0, verbose_name='تعداد بازدید')
    
    # Deep SEO fields
    meta_title = models.CharField(max_length=70, blank=True, verbose_name='عنوان سئو (Title Tag)')
    meta_description = models.CharField(max_length=160, blank=True, verbose_name='توضیحات متا سئو')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ نگارش')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات وبلاگ'
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    @property
    def author_name(self):
        if self.author:
            return self.author.get_full_name() or self.author.username
        return 'بهاور'


class BlogComment(models.Model):
    post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='مقاله'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='blog_comments',
        verbose_name='کاربر سایت'
    )
    user_name = models.CharField(max_length=100, verbose_name='نام کاربر')
    user_email = models.EmailField(blank=True, null=True, verbose_name='ایمیل کاربر')
    comment = models.TextField(verbose_name='متن نظر')
    is_approved = models.BooleanField(default=True, verbose_name='تایید شده')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')

    class Meta:
        verbose_name = 'دیدگاه مقاله'
        verbose_name_plural = 'دیدگاه‌های مقالات'
        ordering = ['-created_at']

    def __str__(self):
        return f"دیدگاه {self.user_name} برای {self.post.title}"
