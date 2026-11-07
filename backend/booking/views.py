from datetime import date
from django.db import transaction
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Booking, BookingService, TimeSlot
from .serializers import (
    BookingSerializer,
    BookingServiceSerializer,
    CreateBookingSerializer,
    TimeSlotSerializer,
)


class BookingServiceListView(generics.ListAPIView):
    queryset = BookingService.objects.filter(is_active=True)
    serializer_class = BookingServiceSerializer
    permission_classes = [permissions.AllowAny]


class AvailableSlotsView(generics.ListAPIView):
    serializer_class = TimeSlotSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        service_id = self.request.query_params.get('service_id')
        selected_date = self.request.query_params.get('date')

        queryset = TimeSlot.objects.filter(is_booked=False)
        if service_id:
            queryset = queryset.filter(service_id=service_id)
        if selected_date:
            queryset = queryset.filter(date=selected_date)
        else:
            queryset = queryset.filter(date__gte=date.today())

        return queryset.order_by('date', 'start_time')


class CreateBookingView(APIView):
    permission_classes = [permissions.AllowAny]

    @transaction.atomic
    def post(self, request):
        serializer = CreateBookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            service = BookingService.objects.get(id=data['service_id'], is_active=True)
        except BookingService.DoesNotExist:
            return Response({'detail': 'سرویس انتخاب شده معتبر نمی‌باشد.'}, status=status.HTTP_400_BAD_REQUEST)

        slot = None
        if data.get('time_slot_id'):
            try:
                slot = TimeSlot.objects.select_for_update().get(
                    id=data['time_slot_id'],
                    service=service,
                    is_booked=False
                )
                slot.is_booked = True
                slot.save(update_fields=['is_booked'])
            except TimeSlot.DoesNotExist:
                return Response({'detail': 'سانس انتخاب شده دیگر موجود نیست.'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user if request.user.is_authenticated else None

        booking = Booking.objects.create(
            user=user,
            service=service,
            time_slot=slot,
            date=data['date'],
            start_time=data['start_time'],
            client_name=data['client_name'],
            client_phone=data['client_phone'],
            client_email=data.get('client_email'),
            notes=data.get('notes', ''),
            total_fee=service.price,
            status=Booking.BookingStatus.PENDING,
        )

        return Response({
            'status': 'success',
            'message': 'درخواست رزرو شما با موفقیت ثبت شد و به زودی تایید خواهد شد.',
            'booking': BookingSerializer(booking).data,
        }, status=status.HTTP_201_CREATED)


class UserBookingsListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).select_related('service').order_by('-date', '-start_time')
