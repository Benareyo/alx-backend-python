from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.status import HTTP_403_FORBIDDEN
from django.http import JsonResponse, HttpResponse

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsAuthenticatedUser, IsParticipant, IsParticipantOfConversation
from .filters import MessageFilter
from .pagination import MessagePagination

# Basic API landing views

def index(request):
    return JsonResponse({"message": "Welcome to Chats API!"})

def chat_home(request):
    return HttpResponse("Hello! This is the Chats page.")



class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
    permission_classes = [IsAuthenticated]


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Messages within a Conversation.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipant]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter
    pagination_class = MessagePagination

    def get_queryset(self):
        conversation_pk = self.kwargs.get('conversation_pk')

        if conversation_pk:
            try:
                conversation = Conversation.objects.get(pk=conversation_pk)
            except Conversation.DoesNotExist:
                raise PermissionDenied(detail="Conversation not found.", code=HTTP_403_FORBIDDEN)

            # Only allow participants to access messages
            if self.request.user not in [conversation.sender, conversation.receiver]:
                raise PermissionDenied(
                    detail="You are not a participant in this conversation.",
                    code=HTTP_403_FORBIDDEN
                )

            return Message.objects.filter(conversation=conversation)

        return Message.objects.none()


# Optional: Generic List API View (not used in router)
class MessageListAPIView(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter
