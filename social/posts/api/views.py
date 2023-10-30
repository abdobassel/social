from django.db.models import Q
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from social.posts.models import Post, PostHashtag
from .serializers import PostHashtagSerializer, PostSerializer


class PostListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    @staticmethod
    def get(request, *args, **kwargs):
        paginator = PageNumberPagination()
        paginator.page_size = 2

        queryset = Post.objects.all().order_by("-timestamp")
        # Filter the queryset based on query parameters
        user_id = request.query_params.get("user_id")
        if user_id is not None:
            try:
                user_id = int(user_id)
                queryset = queryset.filter(user=user_id)
            except ValueError:
                return Response(
                    {"error": "Invalid user ID provided in query parameters."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        # Search and Filtering
        search_query = request.query_params.get("search", None)
        if search_query:
            # Create a Q object to perform an OR operation (e.g., keywords in content or username)
            search_condition = (
                    Q(content__icontains=search_query)
                    | Q(user__username__icontains=search_query)
                    | Q(hashtags__name__icontains=search_query)
            )
            queryset = queryset.filter(search_condition)

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
