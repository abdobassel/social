from rest_framework import serializers

from .models import Post, PostHashtag
from ..users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class PostHashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostHashtag
        fields = ["id", "name"]


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    hashtags = PostHashtagSerializer(many=True, read_only=True)
    mentions = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "slug",
            "likes",
            "reposted",
            "replies",
            "mentions",
            "hashtags",
            "views",
            "visibility",
            "timestamp",
            "content",
            "image",
        ]
