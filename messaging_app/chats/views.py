from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsOwner

class MessageViewSet(viewsets.ModelViewSet):
    ...
    permission_classes = [IsAuthenticated, IsOwner]

class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, creating, retrieving, updating, and deleting conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']  # or any field you want to allow searching on

  

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, creating, retrieving, updating, and deleting messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        """
        Optionally restrict messages to a given conversation,
        by filtering against a `conversation_pk` URL parameter.
        """
        conversation_pk = self.kwargs.get('conversation_pk')
        if conversation_pk:
            return self.queryset.filter(conversation_id=conversation_pk)
        return self.queryset.all()
