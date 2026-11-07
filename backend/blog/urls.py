from django.urls import path
from .views import (
    AddCommentView,
    BlogCategoryListView,
    BlogPostDetailView,
    BlogPostListView,
    TagListView,
)

app_name = 'blog'

urlpatterns = [
    path('categories/', BlogCategoryListView.as_view(), name='category-list'),
    path('tags/', TagListView.as_view(), name='tag-list'),
    path('posts/', BlogPostListView.as_view(), name='post-list'),
    path('posts/<slug:slug>/', BlogPostDetailView.as_view(), name='post-detail'),
    path('posts/<slug:slug>/comment/', AddCommentView.as_view(), name='post-comment'),
]
