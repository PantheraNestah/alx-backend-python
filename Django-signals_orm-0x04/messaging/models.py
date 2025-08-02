from django.db import models

# Create your models here.
# notifications/models.py

from django.db import models
from django.contrib.auth.models import User


class UnreadMessagesManager(models.Manager):
    def get_queryset(self):
        # Start with the base queryset from the default manager
        return super().get_queryset()

    def unread_for_user(self, user):
        """
        Returns a queryset of unread messages for a given user.
        Optimized with .only() to fetch only essential fields for an inbox list.
        """
        # Filter for messages where the user is the receiver and the message is unread
        return self.get_queryset().filter(
            receiver=user, 
            is_read=False
        ).select_related('sender').only(
            'id', 
            'content', 
            'timestamp', 
            'sender__username' # Also fetch the sender's username efficiently
        ).order_by('-timestamp')


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    parent_message = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='replies'
    )
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)

    objects = models.Manager()
    unread = UnreadMessagesManager()

    def __str__(self):
        read_status = "Read" if self.is_read else "Unread"
        base_str = f"From {self.sender.username} to {self.receiver.username} ({read_status})"
        if self.parent_message:
            return f"{base_str} (in reply to {self.parent_message.id})"
        return base_str

class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} regarding message from {self.message.sender.username}"

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, related_name='history', on_delete=models.CASCADE)
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-edited_at'] # Show the most recent edit first

    def __str__(self):
        editor = self.edited_by.username if self.edited_by else 'Unknown'
        return f"Edit for message {self.message.id} at {self.edited_at:%Y-%m-%d %H:%M} (Edited by {editor})"
