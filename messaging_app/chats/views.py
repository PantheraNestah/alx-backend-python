#!/usr/bin/env python3
"""
Defines the API views for the chats application.
"""
from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listing, retrieving, and creating conversations.

    - list: Returns all conversations the current user is a participant in.
    - retrieve: Returns a specific conversation if the user is a participant.
    - create: Creates a new conversation with the specified participants.
    """
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Overrides the default queryset to filter conversations.

        This ensures that users can only see conversations they are
        a part of.
        """
        # The 'related_name' on the Conversation model's participants field
        # allows this reverse lookup.
        return self.request.user.conversations.all()


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listing and creating messages within a conversation.

    This ViewSet is designed to be nested under the ConversationViewSet.
    - list: Returns all messages in a specific conversation.
    - create: Sends a new message to a specific conversation.
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Overrides the queryset to filter messages by conversation.

        Filters messages based on the `conversation_pk` provided in the URL.
        """
        conversation_pk = self.kwargs.get('conversation_pk')
        return Message.objects.filter(conversation_id=conversation_pk)

    def perform_create(self, serializer):
        """
        Overrides the default creation behavior to set the sender and conversation.

        This method ensures the new message is correctly associated with the
        current user and the conversation from the URL.
        """
        conversation_pk = self.kwargs.get('conversation_pk')
        conversation = get_object_or_404(Conversation, pk=conversation_pk)

        # Check if the sender is a participant in the conversation
        if self.request.user not in conversation.participants.all():
            # You might want a more specific exception or response here
            raise permissions.PermissionDenied(
                "You are not a participant in this conversation."
            )

        # Set the sender to the current user and save the message
        serializer.save(sender=self.request.user, conversation=conversation)
