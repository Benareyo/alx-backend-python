<<<<<<< HEAD
from rest_framework.permissions import BasePermission
=======
from rest_framework import permissions
>>>>>>> 304ced478da411f5219fe2b9bd843517e7e0dce4
from .models import Conversation
from rest_framework.exceptions import PermissionDenied
from rest_framework.status import HTTP_403_FORBIDDEN

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']
EDIT_METHODS = ['PUT', 'PATCH', 'DELETE']

<<<<<<< HEAD
class IsAuthenticatedUser(BasePermission):
=======
class IsAuthenticatedUser(permissions.BasePermission):
>>>>>>> 304ced478da411f5219fe2b9bd843517e7e0dce4
    """
    Allows access only to authenticated users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


<<<<<<< HEAD
class IsParticipantOfConversation(BasePermission):
=======
class IsParticipantOfConversation(permissions.BasePermission):
>>>>>>> 304ced478da411f5219fe2b9bd843517e7e0dce4
    """
    Allows only participants of the conversation to send, view, update, or delete messages.
    """

    def has_object_permission(self, request, view, obj):
        # Allow read-only access
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
<<<<<<< HEAD
class IsParticipant(BasePermission):
=======
class IsParticipant(permissions.BasePermission):
>>>>>>> 304ced478da411f5219fe2b9bd843517e7e0dce4
    """
    Custom permission to only allow participants of a conversation
    to view, send, update, or delete messages.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the request.user is in the conversation's participants
        return request.user in obj.conversation.participants.all()