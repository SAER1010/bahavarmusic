from django.urls import path
from .views import (
    ActivePopupView,
    SiteSettingView,
    StudioMetricListView,
)

app_name = 'core'

urlpatterns = [
    path('settings/', SiteSettingView.as_view(), name='site-settings'),
    path('popup/', ActivePopupView.as_view(), name='active-popup'),
    path('metrics/', StudioMetricListView.as_view(), name='metrics-list'),
]
