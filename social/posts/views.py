from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, PostHashtag
from .serializers import PostHashtagSerializer, PostSerializer
from ..users.models import User


class PostListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    @staticmethod
    def get(request, *args, **kwargs):
        queryset = Post.objects.all().order_by("-timestamp")
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)


class PostListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, format=None):
        # Get the queryset of posts and serialize them
        queryset = Post.objects.order_by("-timestamp")
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request, format=None):
        # Create a new post using the request data
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=User.objects.get(pk=1))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostHashtagListAPIView(ListAPIView):
    # queryset = PostHashtag.objects.all()
    # serializer_class = PostHashtagSerializer

    serializer_class = PostHashtagSerializer

    @staticmethod
    def get(request, *args, **kwargs):
        queryset = PostHashtag.objects.all().order_by("-hashtag_time")
        serializer = PostHashtagSerializer(queryset, many=True)
        return Response(serializer.data)
