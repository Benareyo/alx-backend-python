from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Conversation, Message
from rest_framework.exceptions import PermissionDenied
from rest_framework.status import HTTP_403_FORBIDDEN

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']
EDIT_METHODS = ['PUT', 'PATCH', 'DELETE']

class IsAuthenticatedUser(BasePermission):
    """
    Allows access only to authenticated users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class IsParticipantOfConversation(BasePermission):
    """
    Allows only participants of the conversation to send, view, update, or delete messages.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow read-only access
        conversation = getattr(obj, 'conversation', None)
        if conversation:
            return request.user == conversation.sender or request.user == conversation.receiver
        return False
    
        if request.method in SAFE_METHODS:
            return True

        # Allow edit methods only if the user is the sender or receiver
        if request.method in EDIT_METHODS or request.method == "POST":
            if request.user != obj.sender and request.user != obj.receiver:
                raise PermissionDenied(
                    detail="You are not a participant in this conversation.",
                    code=HTTP_403_FORBIDDEN
                )

        # General object-level permission check
        return request.user == obj.sender or request.user == obj.receiver
class IsParticipant(BasePermission):
    """
    Custom permission to only allow participants of a conversation
    to view, send, update, or delete messages.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the request.user is in the conversation's participants
        return request.user in obj.conversation.participants.all()