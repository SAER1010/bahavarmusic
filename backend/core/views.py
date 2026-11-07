from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PopupAdvertisement, SiteSetting, StudioMetric
from .serializers import (
    PopupAdvertisementSerializer,
    SiteSettingSerializer,
    StudioMetricSerializer,
)


class SiteSettingView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        setting = SiteSetting.objects.first()
        if not setting:
            setting = SiteSetting.objects.create(
                about_bahavar="بهاور، موزیسین، آهنگساز، خواننده، مدرس گیتار کلاسیک و فلامنکو و مدیر استودیو ضبط موسیقی با بیش از ۱۵ سال سابقه فعالیت حرفه‌ای و پرورش صدها هنرجو در ایران و خارج از کشور است."
            )
        serializer = SiteSettingSerializer(setting)
        return Response(serializer.data)


class ActivePopupView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        active_popup = PopupAdvertisement.objects.filter(is_active=True).first()
        if active_popup:
            serializer = PopupAdvertisementSerializer(active_popup)
            return Response(serializer.data)
        return Response(None)


class StudioMetricListView(generics.ListAPIView):
    queryset = StudioMetric.objects.all()
    serializer_class = StudioMetricSerializer
    permission_classes = [permissions.AllowAny]
