from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from messaging_app.chats.models import User, Conversation, Message
from messaging_app.chats.serializers import ConversationSerializer, MessageSerializer


# Create your views here.

class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating conversations.
    """

    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the conversations
        for the currently authenticated user.
        """
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with a list of participant emails.
        Expects `participants` in request data, a list of emails.
        """
        participant_emails = request.data.get('participants', [])
        if not isinstance(participant_emails, list):
            return Response(
                {"error": "Participants must be a list of emails."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Add the current user's email to the set to ensure they are included
        all_emails = set(participant_emails)
        all_emails.add(request.user.email)

        participants = User.objects.filter(email__in=all_emails)

        # Optional: Check if all provided emails were found
        if len(participants) != len(all_emails):
            found_emails = {p.email for p in participants}
            missing_emails = all_emails - found_emails
            return Response(
                {"error": f"Users not found: {', '.join(missing_emails)}"},
                status=status.HTTP_404_NOT_FOUND
            )

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating messages within a conversation.
    """

    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filter messages by a `conversation_id` from the URL.
        Ensures user is a participant of the conversation.
        """
        conversation_id = self.kwargs.get('conversation_id')
        if conversation_id:
            return Message.objects.filter(
                conversation_id=conversation_id,
                conversation__participants=self.request.user
            )
        return Message.objects.none()

    def perform_create(self, serializer):
        """
        Set the sender of the message to the current authenticated user.
        """
        conversation_id = self.kwargs.get('conversation_id')
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            raise ValidationError("Conversation does not exist.")

        if self.request.user not in conversation.participants.all():
            raise ValidationError("You are not a participant of this conversation.")

        serializer.save(sender=self.request.user, conversation=conversation)
