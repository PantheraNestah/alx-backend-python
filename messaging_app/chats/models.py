#!/usr/bin/env python3

from django.db import models


"""
Defines the database models for the chats application.
"""
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom User model that extends Django's AbstractUser.

    Uses a UUID for the primary key and adds fields for phone number
    and user role.
    """
    class Role(models.TextChoices):
        """Enumeration for the user roles."""
        GUEST = 'guest', 'Guest'
        HOST = 'host', 'Host'
        ADMIN = 'admin', 'Admin'

    # Override the default ID to use UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.GUEST,
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # Make email unique and required
    email = models.EmailField(unique=True, blank=False, null=False)

    def __str__(self):
        """String representation of the User model."""
        return self.username


class Conversation(models.Model):
    """
    Represents a conversation between two or more users.

    Uses a ManyToManyField to link participants, which is the standard
    Django way to handle this relationship.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String representation of the Conversation model."""
        return f"Conversation {self.id}"


class Message(models.Model):
    """
    Represents a single message within a conversation.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta options for the Message model."""
        ordering = ['sent_at']

    def __str__(self):
        """String representation of the Message model."""
        return f"Message from {self.sender} at {self.sent_at}"
