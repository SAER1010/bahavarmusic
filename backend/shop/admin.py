from django.contrib import admin
from .models import Category, Order, OrderItem, Product, ProductImage, Review


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    verbose_name = 'تصویر گالری'
    verbose_name_plural = 'گالری تصاویر'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_title', 'quantity', 'unit_price', 'total_price', 'digital_access_granted')
    can_delete = False


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon', 'order_index')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'product_type', 'price', 'discount_price', 'stock_quantity', 'is_featured', 'is_active')
    list_filter = ('category', 'product_type', 'is_featured', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductImageInline]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'status', 'total_amount', 'shipping_phone', 'payment_ref_id', 'created_at')
    list_filter = ('status', 'payment_gateway', 'created_at')
    search_fields = ('order_number', 'user__username', 'shipping_full_name', 'shipping_phone', 'payment_ref_id')
    inlines = [OrderItemInline]
    readonly_fields = ('created_at', 'order_number')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'rating', 'created_at')
    search_fields = ('product__title', 'user__username', 'comment')
