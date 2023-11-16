from djoser.serializers import UserSerializer
from rest_framework import serializers

from social.private_message.models import PrivateMessage


class PrivateMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    receiver = UserSerializer()

    class Meta:
        model = PrivateMessage
        fields = ("id", "sender", "receiver", "body", "timestamp")


class PrivateMessageSerializerCreate(serializers.ModelSerializer):
    sender = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PrivateMessage
        fields = ("id", "sender", "receiver", "body", "timestamp")
