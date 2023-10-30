from rest_framework.generics import ListAPIView, ListCreateAPIView

from .models import Post, PostHashtag
from .serializers import PostHashtagSerializer, PostSerializer
from ..users.models import User


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all().order_by("-timestamp")
    serializer_class = PostSerializer


class PostListCreateView(ListCreateAPIView):
    queryset = Post.objects.order_by("-timestamp")
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=User.objects.get(pk=1))


class PostHashtagListAPIView(ListAPIView):
    queryset = PostHashtag.objects.all()
    serializer_class = PostHashtagSerializer
