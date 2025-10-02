from django.db import models


class UnreadMessagesManager(models.Manager):
    """
    Custom manager to filter unread messages for a specific user.
    """

    def unread_for_user(self, user):
        """
        Get all unread messages for a specific user where they are the receiver.
        Uses .only() to retrieve only necessary fields for optimization.
        """
        return self.get_queryset().filter(
            receiver=user,
            read=False
        ).select_related('sender', 'conversation').only(
            'message_id',
            'message_body',
            'sent_at',
            'sender__email',
            'sender__first_name',
            'sender__last_name',
            'conversation__conversation_id'
        )

    def unread_count_for_user(self, user):
        """
        Get the count of unread messages for a user.
        """
        return self.get_queryset().filter(receiver=user, read=False).count()

    def mark_as_read(self, user, message_ids=None):
        """
        Mark messages as read for a user.
        If message_ids is provided, mark only those messages.
        Otherwise, mark all unread messages for the user.
        """
        queryset = self.get_queryset().filter(receiver=user, read=False)
        if message_ids:
            queryset = queryset.filter(message_id__in=message_ids)
        return queryset.update(read=True)
