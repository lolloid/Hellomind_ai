from rest_framework import serializers

from .models import Chat, Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("id", "role", "text", "face_emotion", "text_emotion", "mood_score", "created_at")


class ChatSerializer(serializers.ModelSerializer):
    message_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Chat
        fields = ("id", "title", "created_at", "updated_at", "message_count")


class ChatCreateSerializer(serializers.Serializer):
    title = serializers.CharField(required=False, allow_blank=True, default="Obrolan Baru", max_length=200)


class ChatRenameSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)


class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(allow_blank=False)
    history = serializers.ListField(required=False, default=list)
    face_emotion = serializers.CharField(required=False, allow_blank=True, default="")
    chat_id = serializers.IntegerField(required=False, allow_null=True)
    language = serializers.ChoiceField(choices=("id", "en"), required=False, default="id")
    is_voice = serializers.BooleanField(required=False, default=False)
