from django.urls import re_path

from social.private_message.api.views import PrivateMessageListApiView, PrivateMessageDetailApiView

urlpatterns = [
    re_path(r"^private_messages$", PrivateMessageListApiView.as_view()),
    re_path(r"^private_messages/(?P<private_message_id>'\d'+)$", PrivateMessageDetailApiView.as_view()),
]
