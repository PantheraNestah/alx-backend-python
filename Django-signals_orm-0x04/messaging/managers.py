from django.db import models


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
            'sender__username'  # Also fetch the sender's username efficiently
        ).order_by('-timestamp')

    def unread_count_for_user(self, user):
        """
        Returns the count of unread messages for a specific user.
        Optimized to only count without fetching data.
        """
        return self.get_queryset().filter(
            receiver=user,
            is_read=False
        ).count()

    def mark_as_read_for_user(self, user, message_ids=None):
        """
        Mark messages as read for a specific user.
        If message_ids is provided, only mark those specific messages.
        """
        queryset = self.get_queryset().filter(
            receiver=user,
            is_read=False
        )
        
        if message_ids:
            queryset = queryset.filter(id__in=message_ids)
        
        return queryset.update(is_read=True)
