from django.db.models import Q
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from social.private_message.api.serializers import PrivateMessageSerializer, PrivateMessageSerializerCreate
from social.private_message.models import PrivateMessage


class PrivateMessageListApiView(APIView):
    """List all private messages"""

    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def get(request, *args, **kwargs):
        private_messages = PrivateMessage.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
        return Response(PrivateMessageSerializer(private_messages, many=True).data)

    @staticmethod
    def post(request, *args, **kwargs):
        """Create a new private message"""
        serializer = PrivateMessageSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(PrivateMessageSerializerCreate(serializer.instance).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PrivateMessageDetailApiView(APIView):
    """Private message details"""

    permission_classes = (permissions.IsAuthenticated,)

    @staticmethod
    def get(request, private_message_id, *args, **kwargs):
        private_messages = PrivateMessage.objects.filter(
            Q(sender=request.user) | Q(receiver=request.user),
            pk=private_message_id,
        ).first()
        if not private_messages:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(PrivateMessageSerializer(private_messages).data)
