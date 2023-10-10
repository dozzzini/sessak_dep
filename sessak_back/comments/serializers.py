from rest_framework.serializers import ModelSerializer
from .models import Comment
from rest_framework import serializers
from users.serializers import UserSerializer

# from posts.serializers import PostSerializer


class CommentSerializer(ModelSerializer):
    author = UserSerializer(read_only=True)
    # post = PostSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "comment", "author"]


class UpdatedCommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ["comment"]
