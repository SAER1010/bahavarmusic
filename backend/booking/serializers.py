from rest_framework import serializers
from .models import Booking, BookingService, TimeSlot


class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['id', 'date', 'start_time', 'end_time', 'is_booked']


class BookingServiceSerializer(serializers.ModelSerializer):
    service_type_display = serializers.CharField(source='get_service_type_display', read_only=True)
    available_slots = serializers.SerializerMethodField()

    class Meta:
        model = BookingService
        fields = [
            'id',
            'title',
            'slug',
            'service_type',
            'service_type_display',
            'duration_minutes',
            'price',
            'description',
            'requirements',
            'icon',
            'cover_image',
            'is_active',
            'available_slots',
        ]

    def get_available_slots(self, obj):
        # Return next 10 unbooked slots
        slots = obj.time_slots.filter(is_booked=False)[:10]
        return TimeSlotSerializer(slots, many=True).data


class BookingSerializer(serializers.ModelSerializer):
    service_title = serializers.CharField(source='service.title', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id',
            'booking_code',
            'service',
            'service_title',
            'date',
            'start_time',
            'client_name',
            'client_phone',
            'client_email',
            'status',
            'status_display',
            'notes',
            'total_fee',
            'created_at',
        ]


class CreateBookingSerializer(serializers.Serializer):
    service_id = serializers.IntegerField()
    time_slot_id = serializers.IntegerField(required=False, allow_null=True)
    date = serializers.DateField()
    start_time = serializers.TimeField()
    client_name = serializers.CharField(max_length=120)
    client_phone = serializers.CharField(max_length=15)
    client_email = serializers.EmailField(required=False, allow_blank=True)
    notes = serializers.CharField(required=False, allow_blank=True)
