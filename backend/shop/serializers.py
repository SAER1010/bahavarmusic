from rest_framework import serializers
from .models import Category, Order, OrderItem, Product, ProductImage, Review


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(source='products.count', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon', 'image', 'order_index', 'products_count']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'order']


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'user_name', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_user_name(self, obj):
        return obj.user.get_full_name() or obj.user.username


class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    product_type_display = serializers.CharField(source='get_product_type_display', read_only=True)
    current_price = serializers.IntegerField(read_only=True)
    discount_percent = serializers.IntegerField(read_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'slug',
            'category',
            'category_name',
            'product_type',
            'product_type_display',
            'price',
            'discount_price',
            'current_price',
            'discount_percent',
            'is_in_stock',
            'cover_image',
            'short_description',
            'is_featured',
            'created_at',
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    product_type_display = serializers.CharField(source='get_product_type_display', read_only=True)
    gallery_images = ProductImageSerializer(many=True, read_only=True)
    reviews = serializers.SerializerMethodField()
    current_price = serializers.IntegerField(read_only=True)
    discount_percent = serializers.IntegerField(read_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'slug',
            'category',
            'category_name',
            'product_type',
            'product_type_display',
            'price',
            'discount_price',
            'current_price',
            'discount_percent',
            'stock_quantity',
            'is_in_stock',
            'cover_image',
            'short_description',
            'description',
            'features',
            'gallery_images',
            'reviews',
            'is_featured',
            'created_at',
        ]

    def get_reviews(self, obj):
        approved = obj.reviews.filter(is_approved=True)
        return ReviewSerializer(approved, many=True).data


class OrderItemSerializer(serializers.ModelSerializer):
    total_price = serializers.IntegerField(read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'product',
            'product_title',
            'quantity',
            'unit_price',
            'total_price',
            'digital_access_granted',
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'order_number',
            'status',
            'status_display',
            'total_amount',
            'shipping_full_name',
            'shipping_phone',
            'shipping_address',
            'shipping_postal_code',
            'payment_ref_id',
            'tracking_code',
            'paid_at',
            'created_at',
            'items',
        ]


class CreateOrderItemInputSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1, min_value=1)


class CreateOrderSerializer(serializers.Serializer):
    shipping_full_name = serializers.CharField(max_length=120)
    shipping_phone = serializers.CharField(max_length=15)
    shipping_address = serializers.CharField(required=False, allow_blank=True)
    shipping_postal_code = serializers.CharField(required=False, allow_blank=True)
    items = CreateOrderItemInputSerializer(many=True)

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError('سبد خرید نمی‌تواند خالی باشد.')
        return value
