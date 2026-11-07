from django.urls import path
from .views import (
    CompositionDetailView,
    CompositionListView,
    DownloadSheetMusicView,
    TrackPlayView,
    UnlockTutorialView,
    UserPurchasedTutorialsView,
)

app_name = 'repertoire'

urlpatterns = [
    path('compositions/', CompositionListView.as_view(), name='composition-list'),
    path('compositions/<slug:slug>/', CompositionDetailView.as_view(), name='composition-detail'),
    path('compositions/<slug:slug>/play/', TrackPlayView.as_view(), name='track-play'),
    path('compositions/<slug:slug>/download-sheet/', DownloadSheetMusicView.as_view(), name='download-sheet'),
    path('tutorials/<int:tutorial_id>/unlock/', UnlockTutorialView.as_view(), name='unlock-tutorial'),
    path('my-tutorials/', UserPurchasedTutorialsView.as_view(), name='user-tutorials'),
]
