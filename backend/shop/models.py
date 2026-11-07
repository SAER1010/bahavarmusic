import uuid
from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام دسته‌بندی')
    slug = models.SlugField(max_length=120, unique=True, allow_unicode=True, verbose_name='اسلاگ URL')
    description = models.TextField(blank=True, verbose_name='توضیحات دسته‌بندی')
    icon = models.CharField(max_length=50, blank=True, default='Music', verbose_name='نام آیکون')
    image = models.ImageField(upload_to='shop/categories/', blank=True, null=True, verbose_name='تصویر کاور')
    order_index = models.PositiveIntegerField(default=0, verbose_name='ترتیب نمایش')

    class Meta:
        verbose_name = 'دسته‌بندی فروشگاه'
        verbose_name_plural = 'دسته‌بندی‌های فروشگاه'
        ordering = ['order_index', 'name']

    def __str__(self):
        return self.name


class Product(models.Model):
    class ProductType(models.TextChoices):
        PHYSICAL = 'physical', 'ساز و ابزار فیزیکی'
        ACCESSORY = 'accessory', 'اکسسوری و لوازم جانبی'
        DIGITAL_COURSE = 'digital_course', 'دوره ویدیویی / مسترکلاس'
        SHEET_MUSIC = 'sheet_music', 'کتاب نت و پارتیتور دیجیتال'

    title = models.CharField(max_length=200, verbose_name='عنوان محصول')
    slug = models.SlugField(max_length=220, unique=True, allow_unicode=True, verbose_name='اسلاگ URL')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products',
        verbose_name='دسته‌بندی'
    )
    product_type = models.CharField(
        max_length=20,
        choices=ProductType.choices,
        default=ProductType.PHYSICAL,
        verbose_name='نوع محصول'
    )
    price = models.PositiveBigIntegerField(verbose_name='قیمت اصلی (تومان)')
    discount_price = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        verbose_name='قیمت با تخفیف (تومان)'
    )
    stock_quantity = models.IntegerField(default=1, verbose_name='موجودی انبار')
    cover_image = models.ImageField(upload_to='shop/products/', blank=True, null=True, verbose_name='تصویر اصلی')
    short_description = models.CharField(max_length=300, blank=True, verbose_name='توضیح کوتاه')
    description = models.TextField(verbose_name='توضیحات و مشخصات جامع')
    features = models.JSONField(
        default=list,
        blank=True,
        verbose_name='ویژگی‌های کلیدی (لیست JSON)'
    )
    digital_file = models.FileField(
        upload_to='shop/digital/',
        blank=True,
        null=True,
        verbose_name='فایل دانلودی (مخصوص محصولات دیجیتال)'
    )
    is_featured = models.BooleanField(default=False, verbose_name='محصول منتخب صفحه اصلی')
    is_active = models.BooleanField(default=True, verbose_name='فعال / قابل سفارش')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درج')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_product_type_display()})"

    @property
    def current_price(self):
        if self.discount_price and self.discount_price < self.price:
            return self.discount_price
        return self.price

    @property
    def discount_percent(self):
        if self.discount_price and self.discount_price < self.price:
            diff = self.price - self.discount_price
            return int((diff / self.price) * 100)
        return 0

    @property
    def is_in_stock(self):
        if self.product_type in [self.ProductType.DIGITAL_COURSE, self.ProductType.SHEET_MUSIC]:
            return True
        return self.stock_quantity > 0


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='gallery_images',
        verbose_name='محصول'
    )
    image = models.ImageField(upload_to='shop/gallery/', verbose_name='تصویر گالری')
    alt_text = models.CharField(max_length=150, blank=True, verbose_name='متن جایگزین (ALT)')
    order = models.PositiveIntegerField(default=0, verbose_name='ترتیب')

    class Meta:
        verbose_name = 'تصویر گالری'
        verbose_name_plural = 'گالری تصاویر محصول'
        ordering = ['order', 'id']


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'pending', 'در انتظار پرداخت'
        PAID = 'paid', 'پرداخت شده / تایید شده'
        PROCESSING = 'processing', 'در حال آماده‌سازی'
        SHIPPED = 'shipped', 'ارسال شده'
        COMPLETED = 'completed', 'تکمیل شده'
        CANCELLED = 'cancelled', 'لغو شده'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='کاربر خریدار'
    )
    order_number = models.CharField(
        max_length=32,
        unique=True,
        db_index=True,
        verbose_name='شماره پیگیری سفارش'
    )
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
        verbose_name='وضعیت سفارش'
    )
    total_amount = models.PositiveBigIntegerField(verbose_name='مبلغ نهایی (تومان)')
    shipping_full_name = models.CharField(max_length=120, verbose_name='نام گیرنده')
    shipping_phone = models.CharField(max_length=15, verbose_name='شماره تماس گیرنده')
    shipping_address = models.TextField(blank=True, verbose_name='آدرس پستی')
    shipping_postal_code = models.CharField(max_length=10, blank=True, verbose_name='کد پستی')
    payment_gateway = models.CharField(max_length=30, default='zarinpal', verbose_name='درگاه پرداخت')
    payment_ref_id = models.CharField(max_length=100, blank=True, verbose_name='شماره ارجاع بانکی (RefID)')
    tracking_code = models.CharField(max_length=100, blank=True, verbose_name='کد رهگیری پست')
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name='زمان پرداخت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"BHV-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"سفارش {self.order_number} - {self.user.get_full_name() or self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='سفارش'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        related_name='order_items',
        verbose_name='محصول'
    )
    product_title = models.CharField(max_length=200, verbose_name='عنوان محصول در زمان خرید')
    quantity = models.PositiveIntegerField(default=1, verbose_name='تعداد')
    unit_price = models.PositiveBigIntegerField(verbose_name='قیمت واحد (تومان)')
    digital_access_granted = models.BooleanField(default=False, verbose_name='دسترسی دیجیتال فعال شد')

    class Meta:
        verbose_name = 'آیتم سفارش'
        verbose_name_plural = 'آیتم‌های سفارش'

    @property
    def total_price(self):
        return self.quantity * self.unit_price


class Review(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='محصول'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='کاربر نظر دهنده'
    )
    rating = models.PositiveSmallIntegerField(default=5, verbose_name='امتیاز (۱ تا ۵)')
    comment = models.TextField(verbose_name='متن دیدگاه')
    is_approved = models.BooleanField(default=True, verbose_name='تایید شده برای نمایش')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ دیدگاه')

    class Meta:
        verbose_name = 'دیدگاه محصول'
        verbose_name_plural = 'دیدگاه‌های محصولات'
        ordering = ['-created_at']

    def __str__(self):
        return f"دیدگاه {self.user} برای {self.product.title}"
