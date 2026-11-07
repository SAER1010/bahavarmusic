from rest_framework import serializers
from .models import BlogCategory, BlogComment, BlogPost, Tag


class BlogCategorySerializer(serializers.ModelSerializer):
    posts_count = serializers.IntegerField(source='posts.count', read_only=True)

    class Meta:
        model = BlogCategory
        fields = ['id', 'name', 'slug', 'description', 'posts_count']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class BlogCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogComment
        fields = ['id', 'user_name', 'comment', 'created_at']


class BlogPostListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    author_name = serializers.CharField(read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            'id',
            'title',
            'slug',
            'category',
            'category_name',
            'author_name',
            'excerpt',
            'featured_image',
            'reading_time_minutes',
            'view_count',
            'published_at',
        ]


class BlogPostDetailSerializer(serializers.ModelSerializer):
    category = BlogCategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    author_name = serializers.CharField(read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = BlogPost
        fields = [
            'id',
            'title',
            'slug',
            'category',
            'tags',
            'author_name',
            'excerpt',
            'content',
            'featured_image',
            'reading_time_minutes',
            'view_count',
            'meta_title',
            'meta_description',
            'comments',
            'published_at',
            'updated_at',
        ]

    def get_comments(self, obj):
        approved = obj.comments.filter(is_approved=True)
        return BlogCommentSerializer(approved, many=True).data


class CreateBlogCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogComment
        fields = ['user_name', 'user_email', 'comment']
