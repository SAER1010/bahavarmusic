from django.urls import path
from .views import (
    AvailableSlotsView,
    BookingServiceListView,
    CreateBookingView,
    UserBookingsListView,
)

app_name = 'booking'

urlpatterns = [
    path('services/', BookingServiceListView.as_view(), name='service-list'),
    path('slots/', AvailableSlotsView.as_view(), name='available-slots'),
    path('reserve/', CreateBookingView.as_view(), name='reserve-slot'),
    path('my-bookings/', UserBookingsListView.as_view(), name='user-bookings'),
]
