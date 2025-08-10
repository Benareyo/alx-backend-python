from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows only authenticated users who are participants in the conversation
    to send, view, update, or delete messages.
    """

    def has_permission(self, request, view):
        # All users must be authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Handles object-level permission:
        - For Conversations: check if user is a participant
        - For Messages: check if user is in the conversation participants
        - For update/delete (PUT, PATCH, DELETE): enforce participant check too
        """

        if request.method in SAFE_METHODS or request.method in ["PUT", "PATCH", "DELETE", "POST"]:
            # If the object is a Conversation
            if hasattr(obj, 'participants'):
                return request.user in obj.participants.all()

            # If the object is a Message
            if hasattr(obj, 'conversation'):
                return request.user in obj.conversation.participants.all()

        return False
