from rest_framework import serializers
from .models import PopupAdvertisement, SiteSetting, StudioMetric


class SiteSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSetting
        fields = '__all__'


class PopupAdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = PopupAdvertisement
        fields = [
            'id',
            'title',
            'badge_text',
            'subtitle',
            'description',
            'image',
            'cta_text',
            'cta_link',
            'cookie_dismiss_hours',
            'show_delay_seconds',
        ]


class StudioMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudioMetric
        fields = ['id', 'label', 'value_number', 'suffix', 'icon', 'order_index']
