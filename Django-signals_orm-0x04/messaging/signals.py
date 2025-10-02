from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver

from .models import Message, Notification, MessageHistory, User


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
                    old_content=old_message.message_body,
                    edited_by=instance.sender  # Track who edited the message
                )

                # Mark the message as edited
                instance.edited = True

        except Message.DoesNotExist:
            # Handle case where message doesn't exist yet
            pass


@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """
    Signal to clean up all user-related data when a user account is deleted.
    This handles data cleanup that isn't automatically handled by CASCADE.
    """
    # Delete MessageHistory entries where the user was the editor
    # (these might not be automatically deleted if the message still exists)
    MessageHistory.objects.filter(edited_by=instance).delete()

    # Note: Messages, Notifications, and other related data with CASCADE foreign keys
    # will be automatically deleted by Django when the user is deleted
    # This signal handles any additional cleanup needed
