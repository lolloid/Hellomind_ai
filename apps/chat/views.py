from django.db.models import Count
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Chat
from .serializers import (
    ChatCreateSerializer,
    ChatRenameSerializer,
    ChatRequestSerializer,
    ChatSerializer,
    MessageSerializer,
)
from .services import process_chat_message


class ChatListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        chats = Chat.objects.filter(user=request.user).annotate(message_count=Count("messages"))
        return Response(ChatSerializer(chats, many=True).data)

    def post(self, request):
        serializer = ChatCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        title = serializer.validated_data.get("title") or "Obrolan Baru"
        chat = Chat.objects.create(user=request.user, title=title)
        return Response(ChatSerializer(chat).data, status=status.HTTP_201_CREATED)


class ChatDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, chat_id: int):
        serializer = ChatRenameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        chat = Chat.objects.filter(id=chat_id, user=request.user).first()
        if not chat:
            return Response({"detail": "Chat tidak ditemukan."}, status=status.HTTP_404_NOT_FOUND)
        chat.title = serializer.validated_data["title"]
        chat.save(update_fields=["title", "updated_at"])
        return Response({"message": "Chat renamed.", "title": chat.title})

    def delete(self, request, chat_id: int):
        chat = Chat.objects.filter(id=chat_id, user=request.user).first()
        if not chat:
            return Response({"detail": "Chat tidak ditemukan."}, status=status.HTTP_404_NOT_FOUND)
        chat.delete()
        return Response({"message": "Chat dihapus."})


class ChatMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, chat_id: int):
        chat = Chat.objects.filter(id=chat_id, user=request.user).first()
        if not chat:
            return Response({"detail": "Chat tidak ditemukan."}, status=status.HTTP_404_NOT_FOUND)
        return Response(MessageSerializer(chat.messages.all(), many=True).data)


class ChatEndpointView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChatRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(process_chat_message(request.user, serializer.validated_data))
