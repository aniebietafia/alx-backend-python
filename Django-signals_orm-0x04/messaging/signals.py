from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Message, Notification, MessageHistory


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


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Signal to log message edits by saving the old content before updating.
    Only triggers for existing messages that are being modified.
    """
    if instance.pk:  # Only for existing messages (not new ones)
        try:
            # Get the current version from database
            old_message = Message.objects.get(pk=instance.pk)

            # Check if the message body has changed
            if old_message.message_body != instance.message_body:
                # Save the old content to history
                MessageHistory.objects.create(
                    message=old_message,
                    old_content=old_message.message_body
                )

                # Mark the message as edited
                instance.edited = True

        except Message.DoesNotExist:
            # Handle case where message doesn't exist yet
            pass
