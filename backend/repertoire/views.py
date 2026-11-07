from django.db.models import F
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Composition, GatedTutorial, TutorialAccess
from .serializers import (
    CompositionDetailSerializer,
    CompositionListSerializer,
    GatedTutorialSerializer,
)


class CompositionListView(generics.ListAPIView):
    serializer_class = CompositionListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Composition.objects.all()
        genre = self.request.query_params.get('genre')
        featured = self.request.query_params.get('featured')
        search = self.request.query_params.get('search')

        if genre:
            queryset = queryset.filter(genre=genre)
        if featured in ['true', '1', 'True']:
            queryset = queryset.filter(is_featured=True)
        if search:
            queryset = queryset.filter(persian_title__icontains=search) | queryset.filter(title__icontains=search)

        return queryset.order_by('-is_featured', '-created_at')


class CompositionDetailView(generics.RetrieveAPIView):
    queryset = Composition.objects.all().select_related('gated_tutorial')
    serializer_class = CompositionDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'


class TrackPlayView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, slug):
        composition = generics.get_object_or_404(Composition, slug=slug)
        Composition.objects.filter(pk=composition.pk).update(play_count=F('play_count') + 1)
        return Response({'status': 'success', 'play_count': composition.play_count + 1})


class DownloadSheetMusicView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, slug):
        composition = generics.get_object_or_404(Composition, slug=slug)
        Composition.objects.filter(pk=composition.pk).update(download_count=F('download_count') + 1)
        download_url = composition.sheet_music_pdf.url if composition.sheet_music_pdf else composition.sheet_music_url

        return Response({
            'status': 'success',
            'download_url': download_url or 'https://bahavarmusic.com/sheets/sample-sheet.pdf',
            'download_count': composition.download_count + 1,
        })


class UnlockTutorialView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, tutorial_id):
        tutorial = generics.get_object_or_404(GatedTutorial, id=tutorial_id)
        access, created = TutorialAccess.objects.get_or_create(
            user=request.user,
            tutorial=tutorial,
            defaults={'order_reference': f"TUT-ACQ-{request.user.id}-{tutorial.id}"}
        )
        return Response({
            'status': 'success',
            'message': 'دسترسی به آموزش ویدیویی و فایل‌های تکمیلی با موفقیت فعال شد.',
            'created': created,
            'tutorial': GatedTutorialSerializer(tutorial, context={'request': request}).data,
        })


class UserPurchasedTutorialsView(generics.ListAPIView):
    serializer_class = GatedTutorialSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_tutorial_ids = TutorialAccess.objects.filter(user=self.request.user).values_list('tutorial_id', flat=True)
        return GatedTutorial.objects.filter(id__in=user_tutorial_ids)
