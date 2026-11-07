from django.urls import path
from .views import (
    CategoryListView,
    CreateOrderView,
    CreateReviewView,
    PaymentInitiateView,
    PaymentVerifyView,
    ProductDetailView,
    ProductListView,
    UserOrdersListView,
)

app_name = 'shop'

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/<slug:slug>/reviews/', CreateReviewView.as_view(), name='product-reviews'),
    path('orders/', UserOrdersListView.as_view(), name='user-orders'),
    path('orders/create/', CreateOrderView.as_view(), name='order-create'),
    path('orders/<int:order_id>/pay/', PaymentInitiateView.as_view(), name='payment-initiate'),
    path('payment/verify/', PaymentVerifyView.as_view(), name='payment-verify'),
]
