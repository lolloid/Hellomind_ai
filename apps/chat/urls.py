from django.urls import path

from .views import ChatDetailView, ChatEndpointView, ChatListCreateView, ChatMessagesView


urlpatterns = [
    path("chats", ChatListCreateView.as_view(), name="chat-list-create"),
    path("chats/", ChatListCreateView.as_view(), name="chat-list-create-slash"),
    path("chats/<int:chat_id>", ChatDetailView.as_view(), name="chat-detail"),
    path("chats/<int:chat_id>/", ChatDetailView.as_view(), name="chat-detail-slash"),
    path("chats/<int:chat_id>/messages", ChatMessagesView.as_view(), name="chat-messages"),
    path("chats/<int:chat_id>/messages/", ChatMessagesView.as_view(), name="chat-messages-slash"),
    path("chat", ChatEndpointView.as_view(), name="chat-endpoint"),
    path("chat/", ChatEndpointView.as_view(), name="chat-endpoint-slash"),
]
