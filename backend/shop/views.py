import uuid
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Order, OrderItem, Product, Review
from .serializers import (
    CategorySerializer,
    CreateOrderSerializer,
    OrderSerializer,
    ProductDetailSerializer,
    ProductListSerializer,
    ReviewSerializer,
)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class ProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related('category')
        category_slug = self.request.query_params.get('category')
        product_type = self.request.query_params.get('type')
        is_featured = self.request.query_params.get('featured')
        search = self.request.query_params.get('search')
        ordering = self.request.query_params.get('ordering', '-created_at')

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        if product_type:
            queryset = queryset.filter(product_type=product_type)
        if is_featured in ['true', '1', 'True']:
            queryset = queryset.filter(is_featured=True)
        if search:
            queryset = queryset.filter(title__icontains=search)

        if ordering in ['price', '-price', 'created_at', '-created_at', '-is_featured']:
            queryset = queryset.order_by(ordering)

        return queryset


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True).prefetch_related('gallery_images', 'reviews__user')
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'


class CreateOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        total_amount = 0
        order_items_data = []

        for item_data in data['items']:
            try:
                product = Product.objects.select_for_update().get(id=item_data['product_id'], is_active=True)
            except Product.DoesNotExist:
                return Response(
                    {'detail': f"محصول با شناسه {item_data['product_id']} یافت نشد."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            quantity = item_data['quantity']
            unit_price = product.current_price
            line_total = unit_price * quantity
            total_amount += line_total

            order_items_data.append({
                'product': product,
                'product_title': product.title,
                'quantity': quantity,
                'unit_price': unit_price,
            })

        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            shipping_full_name=data['shipping_full_name'],
            shipping_phone=data['shipping_phone'],
            shipping_address=data.get('shipping_address', ''),
            shipping_postal_code=data.get('shipping_postal_code', ''),
            status=Order.OrderStatus.PENDING,
        )

        for item in order_items_data:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                product_title=item['product_title'],
                quantity=item['quantity'],
                unit_price=item['unit_price'],
            )

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class UserOrdersListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items').order_by('-created_at')


class PaymentInitiateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({'detail': 'سفارش یافت نشد.'}, status=status.HTTP_404_NOT_FOUND)

        if order.status == Order.OrderStatus.PAID:
            return Response({'detail': 'این سفارش قبلاً پرداخت شده است.'}, status=status.HTTP_400_BAD_REQUEST)

        # Payment abstraction: simulated mock gateway or Zarinpal
        authority = f"A0000000000000000000000{uuid.uuid4().hex[:10]}"
        payment_url = f"{settings.PAYMENT_CALLBACK_URL}?Authority={authority}&Status=OK&order_id={order.id}"

        return Response({
            'status': 'success',
            'order_id': order.id,
            'order_number': order.order_number,
            'amount': order.total_amount,
            'authority': authority,
            'payment_url': payment_url,
        })


class PaymentVerifyView(APIView):
    permission_classes = [permissions.AllowAny]

    @transaction.atomic
    def post(self, request):
        order_id = request.data.get('order_id')
        authority = request.data.get('authority', 'MOCK-AUTH-1234')
        payment_status = request.data.get('status', 'OK')

        try:
            order = Order.objects.select_for_update().get(id=order_id)
        except Order.DoesNotExist:
            return Response({'detail': 'سفارش یافت نشد.'}, status=status.HTTP_404_NOT_FOUND)

        if order.status == Order.OrderStatus.PAID:
            return Response({
                'status': 'already_paid',
                'message': 'این سفارش قبلاً پرداخت شده است.',
                'order': OrderSerializer(order).data,
            })

        if payment_status == 'OK':
            ref_id = f"REF-{uuid.uuid4().hex[:10].upper()}"
            order.status = Order.OrderStatus.PAID
            order.payment_ref_id = ref_id
            order.paid_at = timezone.now()
            order.save()

            # Decrement stock and grant digital access
            for item in order.items.all():
                if item.product:
                    if item.product.product_type in [Product.ProductType.PHYSICAL, Product.ProductType.ACCESSORY]:
                        item.product.stock_quantity = max(0, item.product.stock_quantity - item.quantity)
                        item.product.save(update_fields=['stock_quantity'])
                    elif item.product.product_type in [Product.ProductType.DIGITAL_COURSE, Product.ProductType.SHEET_MUSIC]:
                        item.digital_access_granted = True
                        item.save(update_fields=['digital_access_granted'])

            return Response({
                'status': 'success',
                'message': 'پرداخت با موفقیت انجام شد.',
                'ref_id': ref_id,
                'order': OrderSerializer(order).data,
            })
        else:
            order.status = Order.OrderStatus.CANCELLED
            order.save()
            return Response({
                'status': 'failed',
                'message': 'پرداخت توسط کاربر لغو شد یا ناموفق بود.',
            }, status=status.HTTP_400_BAD_REQUEST)


class CreateReviewView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        product_slug = self.kwargs.get('slug')
        product = generics.get_object_or_404(Product, slug=product_slug)
        serializer.save(user=self.request.user, product=product)
