from rest_framework.generics import ListAPIView

from .models import Post, PostHashtag
from .serializers import PostHashtagSerializer, PostSerializer


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostHashtagListAPIView(ListAPIView):
    queryset = PostHashtag.objects.all()
    serializer_class = PostHashtagSerializer
