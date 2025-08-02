# notifications/signals.py

from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    """
    Creates a notification when a new message is created.
    """
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Before a message is saved, check if its content has changed.
    If it has, log the old content to MessageHistory.
    """
    # We only care about updates, not new message creations
    if instance.pk: # pk will be None if the object is new
        try:
            # Get the current version of the message from the database. [1, 4]
            old_instance = Message.objects.get(pk=instance.pk)
        except Message.DoesNotExist:
            return # Should not happen if instance.pk exists, but good practice

        # Compare the old content with the new content
        if old_instance.content != instance.content:
            # Create a history record with the old content
            MessageHistory.objects.create(
                message=instance,
                old_content=old_instance.content
            )
            # Mark the message as edited
            instance.edited = True

@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """
    This signal is for demonstration.
    Cleans up any remaining data after a User is deleted.
    NOTE: on_delete=models.CASCADE handles this automatically in our models.
    This signal is useful for more complex logic or when CASCADE is not used.
    """
    print(f"User {instance.username} deleted. Triggering cleanup signal.")
    
    # Example: If on_delete=models.SET_NULL was used on Message.sender,
    # you might want to delete messages that now have no sender.
    #
    # Message.objects.filter(sender__isnull=True).delete()
    #
    # Our models use CASCADE, so the related objects are already deleted by the DB.
    # This signal would run *after* the database cascade.
    # We can add a log here to confirm it runs.
    
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"User account {instance.username} (ID: {instance.id}) was deleted and associated data was cleaned up.")
