from django.http import FileResponse
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from social.profiles.api.paginations import ProfileSetPagination
from social.profiles.api.serializers import ProfileSerializer, UpdateProfileSerializer
from social.profiles.models import Profile
from social.users.authentications import CustomJWTAuthentication


class ProfileListAPIView(generics.ListAPIView):
    queryset = Profile.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer
    renderer_classes = (JSONRenderer,)
    pagination_class = ProfileSetPagination


class ProfileRetrieveAPIView(generics.RetrieveAPIView):
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer
    renderer_classes = (JSONRenderer,)

    def get_queryset(self):
        queryset = Profile.objects.select_related("user")
        return queryset

    def get_object(self):
        user = self.request.user
        profile = self.get_queryset().get(user=user)
        return profile


class ProfileUpdateAPIView(generics.RetrieveAPIView):
    # authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateProfileSerializer
    parser_classes = [MultiPartParser]
    renderer_classes = [JSONRenderer]

    def get_object(self):
        profile = self.request.user.userprofiles
        return profile

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfilePhotoAPIView(generics.RetrieveAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Profile.objects.all()
    authentication_classes = (CustomJWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    renderer_classes = (JSONRenderer,)
    parser_classes = (MultiPartParser, FormParser)  # Support file uploads
    serializer_class = UpdateProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check if the user has a profile photo
        if instance.profile_photo:
            # Return the profile photo as a FileResponse
            photo_file = instance.profile_photo.open()
            response = FileResponse(photo_file)
            return response
        # If no profile photo is found, you can return a default image or 404,
        # For example, you can create a "no image available" default image
        # and serve it here as a response, or return a 404 response
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check if the user wants to update the profile photo
        profile_photo = request.FILES.get("profile_photo")
        if profile_photo:
            # Handle the file update logic here
            # You can save the new photo, delete the old one, etc.
            # For example, update the profile photo and save the instance
            instance.profile_photo = profile_photo
            instance.save()
            # Serialize the updated instance and return it in the response
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return Response({"message": "No file provided for update"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Check if the user wants to delete the profile photo
        if instance.profile_photo:
            # Handle the file deletion logic here,
            # For example, delete the profile photo file
            # and set the profile_photo field to None
            instance.profile_photo.delete(save=False)
            instance.profile_photo = None
            instance.save()
            return Response({"message": "Profile photo deleted"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "No profile photo to delete"}, status=status.HTTP_400_BAD_REQUEST)
