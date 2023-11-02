from django.db.models import Prefetch
from django.http import Http404, FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters as rest_filters, generics
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from social.posts.models import Post, PostHashtag, Like
from .serializers import PostHashtagSerializer, PostSerializer, PostFileMediaSerializer, UserSerializer
from ..filters import PostFilter
from ...users.models import User


class LikePostAPIView(APIView):

    @staticmethod
    def post(request, post_id):
        post = Post.objects.get(pk=post_id)
        user = request.user

        # Check if the user has already liked the post
        existing_like = Like.objects.filter(user=user, post=post).first()
        if existing_like:
            # User has already liked the post, so remove the like
            existing_like.delete()
            message = "You've unliked the post."
        else:
            # User hasn't liked the post, so add the like
            Like.objects.create(user=user, post=post)
            message = "You've liked the post."
        # Calculate the like's count
        likes_count = Like.objects.filter(post=post).count()
        # Update the likes_count field in the Post model
        post.likes_count = likes_count
        post.save()
        # Serialize the post
        serializer = PostSerializer(post)

        return Response(
            {"message": message, "post": serializer.data, "likes_count": likes_count},
            status=status.HTTP_200_OK,
        )


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


class PostPhotoRetrieveUpdateDestroyAPIView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    queryset = Post.objects.all()
    parser_classes = (MultiPartParser, FormParser)  # Support file uploads
    serializer_class = PostSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check if the user has a profile photo
        if instance.post_photo:
            # Return the profile photo as a FileResponse
            photo_file = instance.post_photo.open()
            response = FileResponse(photo_file)
            return response
        # If no photo is found, you can return a default image or 404,
        # For example, you can create a "no image available" default image
        # and serve it here as a response, or return a 404 response
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check if the user wants to update the photo
        post_photo = request.FILES.get("post_photo")
        if post_photo:
            # Handle the file update logic here
            # You can save the new photo, delete the old one, etc.
            # For example, update the photo and save the instance
            instance.post_photo = post_photo
            instance.save()
            # Serialize the updated instance and return it in the response
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return Response({"message": "No file provided for update"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check if the user wants to delete the photo
        if instance.post_photo:
            # Handle the file deletion logic here,
            # For example, delete the photo file
            # and set the post_photo field to None
            instance.post_photo.delete(save=False)
            instance.post_photo = None
            instance.save()
            return Response({"message": "Post photo deleted"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "No photo to delete"}, status=status.HTTP_400_BAD_REQUEST)


class PostCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        try:
            post_data = request.data.copy()
            if not ("content" in post_data):
                return Response(
                    {"error": "You must provide 'content' data"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if "content" in post_data:
                post_data["content"] = post_data.pop("content")  # Move content to the right field name
            else:
                return Response(post_data.errors, status=status.HTTP_400_BAD_REQUEST)
            # Include the request in the context when initializing the serializer
            post_serializer = PostSerializer(data=post_data, context={"request": request})
            if post_serializer.is_valid():
                post_serializer.validated_data["user"] = request.user
                post_serializer.save(user=request.user)
                return Response(post_serializer.data, status=status.HTTP_201_CREATED)
            return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostPhotoCreateAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        try:
            if "post_photo" not in request.data:
                return Response(
                    {"error": "You must provide a 'photo' to create a post with a photo."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # Include the user in the request data based on the current user
            post_data = {"user": request.user.id, "post_photo": request.data["post_photo"]}
            post_serializer = PostFileMediaSerializer(data=post_data)
            if post_serializer.is_valid():
                post_serializer.save()
                return Response(post_serializer.data, status=status.HTTP_201_CREATED)
            return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def put(request, post_id):
        try:
            post = Post.objects.get(id=post_id, user=request.user)
            # Check if at least one of the two fields (content or image) is provided
            if "content" not in request.data and "image" is None:
                return Response(
                    {"error": "You must provide either content or an image."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # Use partial=True to allow partial updates
            serializer = PostSerializer(post, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found or you don't have permission to update it."},
                status=status.HTTP_404_NOT_FOUND,
            )

    @staticmethod
    def patch(request, post_id):
        try:
            post = Post.objects.get(id=post_id, user=request.user)
            # Check if at least one of the two fields (content or image) is provided
            if "content" not in request.data and "image" is None:
                return Response(
                    {"error": "You must provide either content or an image."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # Use partial=True to allow partial updates
            serializer = PostSerializer(post, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found or you don't have permission to update it."},
                status=status.HTTP_404_NOT_FOUND,
            )


class PostDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def delete(request, post_id):
        try:
            post = Post.objects.get(pk=post_id)
            # Ensure the user has permission to delete the post (e.g., ownership check)
            if post.user == request.user:
                post.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {"error": "You do not have permission to delete this post."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostHashtagResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


class PostHashtagListCreateAPIView(generics.ListCreateAPIView):
    queryset = PostHashtag.objects.all().order_by("-hashtag_time")
    serializer_class = PostHashtagSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, rest_filters.SearchFilter]
    filterset_fields = ["name"]
    search_fields = ["name"]
    ordering_fields = ["hashtag_time"]
    pagination_class = PostHashtagResultsSetPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Http404:
            return Response({"error": "Hashtag not found"}, status=status.HTTP_404_NOT_FOUND)


class UserListByHashtagAPIView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        hashtag_name = self.kwargs["hashtag_name"]  # Extract the hashtag name from the URL parameter
        hashtag_name = hashtag_name if hashtag_name.startswith("#") else f"#{hashtag_name}"
        try:
            # # Retrieve posts that contain the specified hashtag
            posts_with_hashtag = Post.objects.filter(hashtags__name=hashtag_name)
            # Extract the users from those posts
            print(hashtag_name)
            print(hashtag_name)
            users = User.objects.filter(post__in=posts_with_hashtag).distinct()
            return users
        except PostHashtag.DoesNotExist:
            return User.objects.none()  # Return an empty queryset if the hashtag doesn't exist

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        count = queryset.count()  # Calculate the count of users
        serializer = self.get_serializer(queryset, many=True)
        response_data = {"count": count, "users": serializer.data}
        return Response(response_data)
