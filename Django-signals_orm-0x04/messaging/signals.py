from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Message, Notification


@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    """
    Signal to automatically create notifications when a new message is sent.
    Notifies all conversation participants except the sender.
    """
    if created: # Only act on newly created messages
        # Get all participants in the conversation except the sender
        participants = instance.conversation.participants.exclude(user_id=instance.sender.user_id)

        notifications = []
        for participant in participants:
            notification = Notification(
                user=participant,
                message=instance,
                content=f"New message from {instance.sender.first_name} {instance.sender.last_name}: {instance.message_body[:100]}{'...' if len(instance.message_body) > 100 else ''}"
            )
            notifications.append(notification)

        # Bulk create notifications for efficiency
        if notifications:
            Notification.objects.bulk_create(notifications)