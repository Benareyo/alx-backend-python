from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return only conversations the current user is part of
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        participants = request.data.get('participants')
        
        if not participants or not isinstance(participants, list):
            return Response({'error': 'Participants must be a list of user IDs.'},
                            status=status.HTTP_400_BAD_REQUEST)

        users = User.objects.filter(id__in=participants)
        if users.count() != len(participants):
            return Response({'error': 'Some participants not found.'},
                            status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        conversation.participants.set(users)
        conversation.participants.add(request.user)  # Ensure the creator is added
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return messages only from conversations the user is part of
        return Message.objects.filter(conversation__participants=self.request.user)

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get('conversation')
        content = request.data.get('content')

        if not conversation_id or not content:
            return Response({'error': 'Conversation and content are required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({'error': 'Conversation not found.'}, status=status.HTTP_404_NOT_FOUND)

        if request.user not in conversation.participants.all():
            return Response({'error': 'You are not a participant of this conversation.'},
                            status=status.HTTP_403_FORBIDDEN)

        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=content
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
