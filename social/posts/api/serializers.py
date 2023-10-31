from djoser.serializers import UserSerializer as PostUserSerializer
from rest_framework import serializers

from social.posts.models import Post, PostHashtag
from social.users.models import User


class UserSerializer(PostUserSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class PostHashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostHashtag
        fields = ["id", "name", "slug", "is_active"]


class PostFileMediaSerializer(serializers.ModelSerializer):
    # user = serializers.HyperlinkedRelatedField(view_name="user-detail", read_only=True)
    post_photo = serializers.ImageField(max_length=None, allow_empty_file=False, use_url=True, required=False)

    class Meta:
        model = Post
        fields = [
            "id",
            "post_photo",
            "user",
            "likes",
            "hashtags",
            "views",
        ]

    @staticmethod
    def get_file_post(self, obj):
        return obj.file_post.url


class PostSerializer(serializers.ModelSerializer):
    # user = serializers.HyperlinkedRelatedField(view_name="user-detail", read_only=True)
    # post_photo = serializers.HyperlinkedRelatedField(view_name="photo-detail", read_only=True)
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
            "post_photo",
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

    def __init__(self, *args, **kwargs):
        # Get the request from the serializer context
        request = kwargs.pop("context", {}).get("request", None)
        super(PostSerializer, self).__init__(*args, **kwargs, context={"request": request})
