from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Post
from rest_framework import serializers
from users.serializers import UserSerializer
from categories.serializers import CategorySerializer
from comments.serializers import CommentSerializer


class PostSerializer(ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    post_comments = CommentSerializer(read_only=True, many=True)
    like_nums = SerializerMethodField()
    comment_nums = SerializerMethodField()

    # methodfield로 선언한 애들은 무조건 field에 추가해줘야함
    class Meta:
        model = Post
        fields = "__all__"

    def get_like_nums(self, post):
        return post.like_users.all().count()

    def get_comment_nums(self, post):
        return post.post_comments.all().count()


class PopularPostSerializer(ModelSerializer):
    total_nums = serializers.IntegerField()

    class Meta:
        model = Post
        fields = "__all__"

    def get_total_nums(self, post):
        return post.total_nums


class PostListSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "content", "id")
