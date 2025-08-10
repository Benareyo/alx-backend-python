from rest_framework import serializers
from .models import User,Conversation,Message

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model=User
        fields=['user_id', 'first_name', 'last_name', 'email', 'password','phone_number', 'role', 'created_at']
        read_only_fields = ['user_id', 'created_at']
class MessageSerializer(serializers.ModelSerializer):
    sender=UserSerializer(read_only=True)
    class Meta:
        model=Message
        fields=['message_id', 'sender', 'conversation', 'message_body', 'sent_at']
        read_only_fields=['message_id', 'sent_at', 'sender']
    
    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty or whitespace only.")
        return value
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()
    class Meta:
        model=Conversation
        fields=['conversation_id', 'participants', 'created_at', 'messages','message_count']
        read_only_fields=['conversation_id', 'created_at']
    def get_message_count(self, obj):
        return obj.messages.count()