from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.status import HTTP_403_FORBIDDEN

class IsAuthenticatedUser(permissions.BasePermission):
    """
    Allows access only to authenticated users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission: Only participants of a conversation can view, update, delete, or send messages.
    """

    def has_object_permission(self, request, view, obj):
        if request.user == obj.sender or request.user == obj.receiver:
            return True
        raise PermissionDenied(
            detail="You are not a participant in this conversation.",
            code=HTTP_403_FORBIDDEN
        )
