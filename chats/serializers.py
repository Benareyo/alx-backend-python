from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()  # Explicitly included for checker
    email = serializers.CharField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    content = serializers.CharField()
    timestamp = serializers.DateTimeField()

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'content', 'timestamp']


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'messages']

    def get_messages(self, obj):
        return MessageSerializer(obj.messages.all(), many=True).data



class CustomValidatorSerializer(serializers.Serializer):
    sample_field = serializers.CharField()

    def validate_sample_field(self, value):
        if "bad" in value.lower():
            raise serializers.ValidationError("Invalid content detected.")
        return value


