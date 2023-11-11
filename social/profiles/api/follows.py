from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from social.profiles.api.exeptions import CannotFollowYourSelf
from social.profiles.api.serializers import FollowersSerializer
from social.profiles.models import Profile


class FollowersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, format=None, *args, **kwargs):
        try:
            profile = Profile.objects.get(user__id=request.user.id)
            followers_profile = profile.followers.all()
            serializer = FollowersSerializer(followers_profile, many=True)
            formatted_response = {
                "status_code": status.HTTP_200_OK,
                "followers_count": followers_profile.count(),
                "followers": serializer.data,
            }
            return Response(formatted_response, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response(status=404)


class FollowingAPIView(APIView):
    @staticmethod
    def get(self, request, user_id, *args, **kwargs):
        try:
            profile = Profile.objects.get(user__id=user_id)
            following_profile = profile.following.all()
            user = [p.user for p in following_profile]
            serializer = FollowersSerializer(user, many=True)
            formatted_response = {
                "status_code": status.HTTP_200_OK,
                "following_count": following_profile.count(),
                "user_I_follow": serializer.data,
            }
            return Response(formatted_response, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response(status=404)


class FollowAPIView(APIView):
    def post(self, request, user_id, format=None):
        try:
            follower = Profile.objects.get(user=self.request.user)
            user_profile = request.user.profile
            profile = Profile.objects.get(user__id=user_id)
            if profile == follower:
                raise CannotFollowYourSelf()

            if user_profile.check_following(profile):
                formatted_response = {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": f"You are already following {profile.user.first_name} {profile.user.last_name}",
                }
                return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)

            user_profile.follow(profile)
            return Response(
                {
                    "status_code": status.HTTP_200_OK,
                    "message": f"You are now following {profile.user.first_name} {profile.user.last_name}",
                },
            )
        except Profile.DoesNotExist:
            raise NotFound("You can't follow a profile that does not exist.")


class UnfollowAPIView(APIView):
    @staticmethod
    def post(request, user_id, *args, **kwargs):
        user_profile = request.user.profile
        profile = Profile.objects.get(user__id=user_id)

        if not user_profile.check_following(profile):
            formatted_response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": f"You can't unfollow {profile.user.first_name} {profile.user.last_name}, "
                           f"since you were not following them in the first place ",
            }
            return Response(formatted_response, status.HTTP_400_BAD_REQUEST)

        user_profile.unfollow(profile)
        formatted_response = {
            "status_code": status.HTTP_200_OK,
            "message": f"You have unfollowed {profile.user.first_name} {profile.user.last_name}",
        }
        return Response(formatted_response, status.HTTP_200_OK)
