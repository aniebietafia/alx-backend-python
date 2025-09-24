from rest_framework import permissions


class IsOwnerOrParticipant(permissions.BasePermission):
    """
    Custom permission to ensure users can only access their own conversations and messages.
    """

    def has_object_permission(self, request, view, obj):
        # For Conversation objects
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        # For Message objects
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()

        return False


class IsConversationParticipant(permissions.BasePermission):
    """
    Permission to check if user is a participant in the conversation.
    """

    def has_permission(self, request, view):
        if hasattr(view, 'kwargs') and 'conversation_pk' in view.kwargs:
            from .models import Conversation
            try:
                conversation = Conversation.objects.get(
                    conversation_id=view.kwargs['conversation_pk']
                )
                return request.user in conversation.participants.all()
            except Conversation.DoesNotExist:
                return False
        return True
