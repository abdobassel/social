from rest_framework import serializers

from social.posts.models import Post, PostHashtag
from social.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class PostHashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostHashtag
        fields = ["id", "name", "slug", "is_active"]


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    hashtags = PostHashtagSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "likes",
            "views",
            "visibility",
            "timestamp",
            "hashtags",
            "content",
            "image",
        ]

    def create(self, validated_data):
        # Extract mentioned users and hashtag data
        hashtags_data = validated_data.pop("hashtags", [])
        # Create the Post instance
        post = Post.objects.create(**validated_data)
        # Call custom methods to handle mentions and hashtags
        self.handle_hashtags(post, hashtags_data)

        return post

    @staticmethod
    def handle_hashtags(post, hashtags_data):
        # Create and associate hashtags with the post
        for hashtag_data in hashtags_data:
            hashtag, created = PostHashtag.objects.get_or_create(**hashtag_data)
            post.hashtags.add(hashtag)

    @staticmethod
    def get_image(obj):
        return obj.image.url
