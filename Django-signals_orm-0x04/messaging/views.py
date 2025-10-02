from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import User, Conversation, Message, build_message_tree
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import (
    IsParticipantOfConversation,
    IsMessageSenderOrParticipant
)
from .filters import MessageFilter, ConversationFilter
from .pagination import MessagePagination, ConversationPagination


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating conversations.
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ConversationFilter
    search_fields = ['participants__email', 'participants__first_name', 'participants__last_name']
    ordering_fields = ['created_at', 'participants__email']
    ordering = ['-created_at']
    pagination_class = ConversationPagination

    def get_queryset(self):
        """
        This view should return a list of all the conversations
        for the currently authenticated user.
        """
        return Conversation.objects.filter(participants=self.request.user).distinct()

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

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            # Only authenticated users can create conversations
            permission_classes = [IsAuthenticated]
        else:
            # For other actions, check if user is participant
            permission_classes = [IsAuthenticated, IsParticipantOfConversation]

        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['delete'], url_path='delete-account')
    def delete_user_account(self, request):
        """
        Allow a user to delete their own account.
        This will trigger the post_delete signal to clean up related data.
        """
        user = request.user

        # Optional: Add confirmation check
        confirmation = request.data.get('confirm_deletion', False)
        if not confirmation:
            return Response(
                {"error": "Please confirm deletion by setting 'confirm_deletion' to true"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user_email = user.email
            user.delete()  # This will trigger the post_delete signal
            return Response(
                {"message": f"User account {user_email} has been successfully deleted"},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to delete account: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MessageViewSet(viewsets.ModelViewSet):
    # ... existing code ...

    def get_queryset(self):
        """
        Filter messages by conversation_id with optimized threading queries.
        """
        conversation_pk = self.kwargs.get('conversation_pk')
        if conversation_pk:
            return Message.threaded.get_threaded_messages(
                Conversation.objects.get(conversation_id=conversation_pk)
            ).filter(conversation__participants=self.request.user)
        return Message.objects.none()

    @action(detail=False, methods=['get'], url_path='threaded')
    def get_threaded_view(self, request, conversation_pk=None):
        """
        Get messages in threaded format with optimized queries.
        """
        try:
            conversation = Conversation.objects.get(
                conversation_id=conversation_pk,
                participants=request.user
            )
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Get all messages with optimized queries
        messages = Message.threaded.get_threaded_messages(conversation)

        # Build threaded structure
        threaded_messages = build_message_tree(messages)

        # Serialize the threaded data
        def serialize_thread(thread_node):
            message = thread_node['message']
            return {
                'message_id': str(message.message_id),
                'sender': {
                    'email': message.sender.email,
                    'first_name': message.sender.first_name,
                    'last_name': message.sender.last_name
                },
                'message_body': message.message_body,
                'sent_at': message.sent_at,
                'edited': message.edited,
                'parent_message_id': str(message.parent_message.message_id) if message.parent_message else None,
                'depth': message.get_thread_depth(),
                'replies': [serialize_thread(reply) for reply in thread_node['replies']]
            }

        serialized_data = [serialize_thread(thread) for thread in threaded_messages]

        return Response({
            'conversation_id': str(conversation.conversation_id),
            'threaded_messages': serialized_data
        })

    @action(detail=True, methods=['get'], url_path='thread')
    def get_message_thread(self, request, pk=None, conversation_pk=None):
        """
        Get a specific message and all its replies recursively.
        """
        try:
            # Verify conversation access
            conversation = Conversation.objects.get(
                conversation_id=conversation_pk,
                participants=request.user
            )

            # Get the message thread
            thread_messages = Message.threaded.get_message_with_replies(pk)

            if not thread_messages:
                return Response(
                    {"error": "Message not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Serialize the thread
            serialized_messages = []
            for message in thread_messages:
                serialized_messages.append({
                    'message_id': str(message.message_id),
                    'sender': {
                        'email': message.sender.email,
                        'first_name': message.sender.first_name,
                        'last_name': message.sender.last_name
                    },
                    'message_body': message.message_body,
                    'sent_at': message.sent_at,
                    'edited': message.edited,
                    'parent_message_id': str(message.parent_message.message_id) if message.parent_message else None,
                    'depth': getattr(message, 'depth', message.get_thread_depth())
                })

            return Response({
                'thread_messages': serialized_messages
            })

        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    def perform_create(self, serializer):
        """
        Enhanced create method to handle reply creation.
        """
        conversation_pk = self.kwargs.get('conversation_pk')
        parent_message_id = self.request.data.get('parent_message_id')

        try:
            conversation = Conversation.objects.get(conversation_id=conversation_pk)
        except Conversation.DoesNotExist:
            raise ValidationError("Conversation does not exist.")

        if self.request.user not in conversation.participants.all():
            raise ValidationError("You are not a participant of this conversation.")

        # Handle parent message if this is a reply
        parent_message = None
        if parent_message_id:
            try:
                parent_message = Message.objects.get(
                    message_id=parent_message_id,
                    conversation=conversation
                )
            except Message.DoesNotExist:
                raise ValidationError("Parent message not found in this conversation.")

        serializer.save(
            sender=self.request.user,
            conversation=conversation,
            parent_message=parent_message
        )
