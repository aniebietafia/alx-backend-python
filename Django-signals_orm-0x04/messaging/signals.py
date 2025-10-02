from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Message, Notification


@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    """
    Signal to automatically create notifications when a new message is sent.
    Creates a notification for the message receiver.
    """
    if created:  # Only act on newly created messages
        # Create notification for the receiver
        Notification.objects.create(
            user=instance.receiver,
            receiver=instance.receiver,
            message=instance,
            content=f"New message from {instance.sender.first_name} {instance.sender.last_name}: {instance.message_body[:100]}{'...' if len(instance.message_body) > 100 else ''}"
        )
