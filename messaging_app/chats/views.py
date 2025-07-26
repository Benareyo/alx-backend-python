from rest_framework import viewsets, status, filters
from rest_framework.response import Response
<<<<<<< HEAD
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.status import HTTP_403_FORBIDDEN

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsAuthenticatedUser, IsParticipantOfConversation

from django_filters.rest_framework import DjangoFilterBackend
from .filters import MessageFilter  # Make sure you have this file
from .pagination import MessagePagination  # If you created custom pagination
from rest_framework import generics


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


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, creating, retrieving, updating, and deleting messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticatedUser, IsParticipantOfConversation]
    permission_classes = [IsParticipant]
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
=======
from rest_framework.decorators import action
from django.contrib.auth.models import User
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__username']

    def create(self, request, *args, **kwargs):
        participants = request.data.get("participants")
        if not participants or len(participants) < 2:
            return Response({"error": "At least two participants are required."},
                            status=status.HTTP_400_BAD_REQUEST)
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['sender__username', 'conversation__id']

    def create(self, request, *args, **kwargs):
        data = request.data
        conversation_id = data.get("conversation")
        sender = request.user
        content = data.get("content")

        if not (conversation_id and content):
            return Response({"error": "Conversation and content are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            conversation = Conversation.objects.get(pk=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found."}, status=status.HTTP_404_NOT_FOUND)

        message = Message.objects.create(conversation=conversation, sender=sender, content=content)
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
>>>>>>> 304ced478da411f5219fe2b9bd843517e7e0dce4
