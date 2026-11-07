from django.db.models import F
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import BlogCategory, BlogComment, BlogPost, Tag
from .serializers import (
    BlogCategorySerializer,
    BlogPostDetailSerializer,
    BlogPostListSerializer,
    CreateBlogCommentSerializer,
    TagSerializer,
)


class BlogCategoryListView(generics.ListAPIView):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    permission_classes = [permissions.AllowAny]


class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]


class BlogPostListView(generics.ListAPIView):
    serializer_class = BlogPostListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = BlogPost.objects.filter(is_published=True).select_related('category', 'author')
        category_slug = self.request.query_params.get('category')
        tag_slug = self.request.query_params.get('tag')
        search = self.request.query_params.get('search')

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)
        if search:
            queryset = queryset.filter(title__icontains=search)

        return queryset.order_by('-published_at')


class BlogPostDetailView(generics.RetrieveAPIView):
    queryset = BlogPost.objects.filter(is_published=True).select_related('category', 'author').prefetch_related('tags')
    serializer_class = BlogPostDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        BlogPost.objects.filter(pk=instance.pk).update(view_count=F('view_count') + 1)
        instance.refresh_from_db(fields=['view_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class AddCommentView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CreateBlogCommentSerializer

    def perform_create(self, serializer):
        slug = self.kwargs.get('slug')
        post = generics.get_object_or_404(BlogPost, slug=slug, is_published=True)
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(post=post, user=user)
