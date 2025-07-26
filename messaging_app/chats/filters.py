# chats/filters.py

import django_filters
from .models import Message, Conversation # Import your models here
from django.contrib.auth import get_user_model

User = get_user_model() # Get the currently active User model

class MessageFilter(django_filters.FilterSet):
    """
    Filter class for Message objects.
    Allows filtering by:
    - sender (username or ID)
    - sent_at (date range: greater than or equal, less than or equal)
    """
    # Filter by sender's username (case-insensitive contains)
    sender_username = django_filters.CharFilter(
        field_name='sender__username', lookup_expr='icontains',
        help_text="Filter messages by sender's username (case-insensitive partial match)."
    )
    # Filter by sender's ID
    sender_id = django_filters.CharFilter(
        field_name='sender__id', lookup_expr='exact',
        help_text="Filter messages by sender's user ID."
    )

    # Filter by sent_at greater than or equal to a date/datetime
    sent_after = django_filters.DateTimeFilter(
        field_name='sent_at', lookup_expr='gte',
        help_text="Filter messages sent on or after this date/time (e.g., YYYY-MM-DDTHH:MM:SSZ)."
    )
    # Filter by sent_at less than or equal to a date/datetime
    sent_before = django_filters.DateTimeFilter(
        field_name='sent_at', lookup_expr='lte',
        help_text="Filter messages sent on or before this date/time (e.g., YYYY-MM-DDTHH:MM:SSZ)."
    )

    class Meta:
        model = Message
        fields = ['sender', 'sent_at'] # You can list specific fields for exact matches here
                                        # Or let the above custom filters handle it.
                                        # 'sender' here would allow filtering by sender ID directly: ?sender=1