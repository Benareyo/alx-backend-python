from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.status import HTTP_403_FORBIDDEN

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsAuthenticatedUser, IsParticipantOfConversation

from django_filters.rest_framework import DjangoFilterBackend
from .filters import MessageFilter  
from .pagination import MessagePagination  
from rest_framework import generics

from rest_framework.permissions import IsAuthenticated


from rest_framework import viewsets
from .models import Message
from .serializers import MessageSerializer
from .permissions import IsParticipant
class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, creating, retrieving, updating, and deleting conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    permission_classes = [IsAuthenticatedUser]

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, creating, retrieving, updating, and deleting messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticatedUser, IsParticipantOfConversation]
    #permission_classes = [IsParticipant]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter
    pagination_class = MessagePagination
    
    def get_queryset(self):
        """
        Restrict messages to a given conversation and check if user is a participant.
        """
        conversation_pk = self.kwargs.get('conversation_pk')
        if conversation_pk:
            # Filter messages for the conversation
            messages = Message.objects.filter(conversation_id=conversation_pk)

            # Check if the user is a participant in the conversation
            try:
                conversation = Conversation.objects.get(pk=conversation_pk)
            except Conversation.DoesNotExist:
                raise PermissionDenied(detail="Conversation not found.", code=HTTP_403_FORBIDDEN)

            if self.request.user not in [conversation.sender, conversation.receiver]:
                raise PermissionDenied(
                    detail="You are not a participant in this conversation.",
                    code=HTTP_403_FORBIDDEN
                )

            return messages

        return self.queryset.none()  # Return no messages if no conversation_pk provided
class MessageListAPIView(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter