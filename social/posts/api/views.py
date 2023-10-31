from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as rest_filters
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from social.posts.models import Post, PostHashtag
from .serializers import PostHashtagSerializer, PostSerializer
from ..filters import PostFilter
from ...users.models import User


class PostListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, rest_filters.SearchFilter]
    filterset_class = PostFilter

    @staticmethod
    def get(request, *args, **kwargs):
        paginator = PageNumberPagination()
        paginator.page_size = 5

        likes_prefetch = Prefetch("likes", queryset=User.objects.only("id"))
        queryset = Post.objects.select_related().prefetch_related("hashtags", likes_prefetch).all().order_by(
            "-timestamp")

        # Paginate the queryset
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = PostSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
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
            serializer.save(user=request.user)
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
