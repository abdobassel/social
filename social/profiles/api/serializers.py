from phonenumber_field.formfields import PhoneNumberField
from rest_framework import serializers

from social.profiles.api.validations import is_valid_phone_number
from social.profiles.models import Profile
from social.users.models import User


class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    slug = serializers.CharField(source="user.slug")
    username = serializers.EmailField(source="user.username")
    email = serializers.EmailField(source="user.email")
    gender = serializers.CharField(source="user.gender")
    profile_photo = serializers.ImageField(max_length=None, allow_empty_file=False, use_url=True, required=False)
    country = serializers.CharField()
    phone_number = PhoneNumberField()
    is_active = serializers.BooleanField(source="user.is_active")

    class Meta:
        model = Profile
        fields = (
            "user",
            "first_name",
            "last_name",
            "slug",
            "email",
            "profile_photo",
            "username",
            "gender",
            "country",
            "city",
            "phone_number",
            "bio",
            "is_active",
        )

    def validate_user(self, value):
        # Ensure that the user being updated matches the request user
        request_user = self.context["request"].user
        if value != request_user:
            raise serializers.ValidationError("You can only update your own profile.")
        return value

    @staticmethod
    def validate_first_name(value):
        if not value:
            raise serializers.ValidationError("First name is required.")
        if len(value) > 10:  # Adjust the character limit as needed
            raise serializers.ValidationError("First name is too long.")
        return value

    @staticmethod
    def validate_last_name(value):
        if not value:
            raise serializers.ValidationError("Last name is required.")
        if len(value) > 10:  # Adjust the character limit as needed
            raise serializers.ValidationError("Last name is too long.")
        return value

    @staticmethod
    def validate_phone_number(value):
        # You can add custom phone number validation logic here,
        # For example, checking if the phone number is valid for the specified country
        if not is_valid_phone_number(value):
            raise serializers.ValidationError("Invalid phone number format or country.")
        return value

    @staticmethod
    def validate_gender(value):
        allowed_choices = [choice[0] for choice in User.Gender.choices]
        if value not in allowed_choices:
            raise serializers.ValidationError("Invalid gender value")
        return value

    @staticmethod
    def get_profile_photo(obj):
        return obj.profile_photo.url


class UpdateProfileSerializer(serializers.ModelSerializer):
    country = serializers.CharField()
    phone_number = PhoneNumberField()

    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")

    class Meta:
        model = Profile
        fields = (
            "first_name",
            "last_name",
            "phone_number",
            "profile_photo",
            "country",
            "city",
            "bio",
        )

    def update(self, instance, validated_data):
        if "first_name" in validated_data:
            instance.user.first_name = validated_data["first_name"]
        if "last_name" in validated_data:
            instance.user.last_name = validated_data["last_name"]
        if "phone_number" in validated_data:
            instance.phone_number = validated_data["phone_number"]
        if "profile_photo" in validated_data:
            instance.profile_photo = validated_data["profile_photo"]
        if "country" in validated_data:
            instance.country = validated_data["country"]
        if "city" in validated_data:
            instance.city = validated_data["city"]
        if "bio" in validated_data:
            instance.bio = validated_data["bio"]

        instance.save()
        instance.user.save()
        return instance


class FollowersSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")

    class Meta:
        model = Profile
        fields = ("first_name", "last_name")
