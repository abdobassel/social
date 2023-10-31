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
        queryset = (
            Post.objects.select_related()
            .prefetch_related("hashtags", likes_prefetch)
            .all()
            .order_by(
                "-timestamp",
            )
        )
        # Paginate the queryset
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = PostSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)


class PostCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    # parser_classes = (MultiPartParser, FormParser)

    @staticmethod
    def post(request):
        try:
            # Check if at least one of the two fields (content or image) is provided
            if "content" not in request.data and "image" is None:
                return Response(
                    {"error": "You must provide either content or an image."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = PostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.validated_data["user"] = request.user
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostHashtagListAPIView(ListAPIView):
    serializer_class = PostHashtagSerializer

    @staticmethod
    def get(request, *args, **kwargs):
        queryset = PostHashtag.objects.all().order_by("-hashtag_time")
        serializer = PostHashtagSerializer(queryset, many=True)
        return Response(serializer.data)
