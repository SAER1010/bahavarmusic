from rest_framework import serializers
from .models import Composition, GatedTutorial, TutorialAccess


class GatedTutorialSerializer(serializers.ModelSerializer):
    has_access = serializers.SerializerMethodField()
    accessible_stream_url = serializers.SerializerMethodField()
    accessible_download_url = serializers.SerializerMethodField()

    class Meta:
        model = GatedTutorial
        fields = [
            'id',
            'title',
            'description',
            'preview_video_url',
            'duration_minutes',
            'price',
            'is_free_for_active_students',
            'has_access',
            'accessible_stream_url',
            'accessible_download_url',
        ]

    def get_has_access(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        # Check active student condition
        if obj.is_free_for_active_students and hasattr(request.user, 'student_profile'):
            if request.user.student_profile.attended_sessions_count > 0:
                return True
        return TutorialAccess.objects.filter(user=request.user, tutorial=obj).exists()

    def get_accessible_stream_url(self, obj):
        if self.get_has_access(obj):
            return obj.full_video_url
        return None

    def get_accessible_download_url(self, obj):
        if self.get_has_access(obj):
            return obj.download_video_url or obj.full_video_url
        return None


class CompositionListSerializer(serializers.ModelSerializer):
    genre_display = serializers.CharField(source='get_genre_display', read_only=True)
    audio_stream_url = serializers.CharField(read_only=True)
    has_tutorial = serializers.SerializerMethodField()

    class Meta:
        model = Composition
        fields = [
            'id',
            'title',
            'persian_title',
            'slug',
            'composer',
            'arranger',
            'genre',
            'genre_display',
            'key_signature',
            'tempo_bpm',
            'duration_display',
            'cover_image',
            'audio_stream_url',
            'is_free_sheet_music',
            'play_count',
            'download_count',
            'is_featured',
            'has_tutorial',
            'created_at',
        ]

    def get_has_tutorial(self, obj):
        return hasattr(obj, 'gated_tutorial')


class CompositionDetailSerializer(serializers.ModelSerializer):
    genre_display = serializers.CharField(source='get_genre_display', read_only=True)
    audio_stream_url = serializers.CharField(read_only=True)
    gated_tutorial = GatedTutorialSerializer(read_only=True)
    sheet_music_download_url = serializers.SerializerMethodField()

    class Meta:
        model = Composition
        fields = [
            'id',
            'title',
            'persian_title',
            'slug',
            'composer',
            'arranger',
            'genre',
            'genre_display',
            'key_signature',
            'tempo_bpm',
            'duration_display',
            'description',
            'cover_image',
            'audio_stream_url',
            'is_free_sheet_music',
            'sheet_price',
            'sheet_music_download_url',
            'play_count',
            'download_count',
            'is_featured',
            'gated_tutorial',
            'created_at',
        ]

    def get_sheet_music_download_url(self, obj):
        if obj.sheet_music_pdf:
            return obj.sheet_music_pdf.url
        return obj.sheet_music_url or None
