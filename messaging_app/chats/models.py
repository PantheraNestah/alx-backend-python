#!/usr/bin/env python3
"""
Defines the database models for the chats application.
"""
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom User model that extends Django's AbstractUser.

    This model matches the database specification by explicitly defining the
    primary key's database column name. Other fields like first_name,
    last_name, and password are inherited from AbstractUser.
    """
    class Role(models.TextChoices):
        GUEST = 'guest', 'Guest'
        HOST = 'host', 'Host'
        ADMIN = 'admin', 'Admin'

    # The primary key field. In Django/Python, we access this as `user.id`.
    # In the database, the column will be named 'user_id'.
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='user_id'  # Explicitly name the DB column
    )
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.GUEST,
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # Ensure email is unique and required, inherited from AbstractUser
    email = models.EmailField(unique=True, blank=False, null=False)

    def __str__(self):
        return self.username


class Conversation(models.Model):
    """
    Represents a conversation between two or more users.
    """
    # The primary key field. In the DB, the column is 'conversation_id'.
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='conversation_id'  # Explicitly name the DB column
    )
    # This ManyToManyField will create a separate mapping table as is
    # standard for this relationship.
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"


class Message(models.Model):
    """
    Represents a single message within a conversation.
    """
    # The primary key field. In the DB, the column is 'message_id'.
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='message_id'  # Explicitly name the DB column
    )
    # This ForeignKey will create a 'conversation_id' column in the DB.
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    # This ForeignKey will create a 'sender_id' column in the DB.
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sent_at']

    def __str__(self):
        return f"Message from {self.sender} at {self.sent_at}"