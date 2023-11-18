from rest_framework import serializers

from social.private_message.models import PrivateMessage
from social.users.models import User


class PrivateMessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    receiver = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)

    class Meta:
        model = PrivateMessage
        fields = ("sender", "receiver", "body", "timestamp")

    def create(self, validated_data):
        # Create a new PrivateMessage instance
        private_message = PrivateMessage.objects.create(**validated_data)
        return private_message


class PrivateMessageSerializerCreate(serializers.ModelSerializer):
    sender = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PrivateMessage
        fields = ("id", "sender", "receiver", "body", "timestamp")
