#!/usr/bin/env python3
"""
Defines the API views for the chats application.
"""
from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for conversations with filtering, searching, and ordering.
    """
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Use DRF's filter backends for powerful query capabilities.
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    # Define the fields that can be searched.
    # This allows searching by participant username or email.
    search_fields = ['participants__username', 'participants__email']

    # Define the fields that the results can be ordered by.
    ordering_fields = ['created_at']

    def get_queryset(self):
        """
        Ensures users only see conversations they are a part of.
        The filtering backends will act on this base queryset.
        """
        return self.request.user.conversations.all()


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for messages within a conversation.
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filters messages based on the `conversation_pk` from the URL.
        """
        conversation_pk = self.kwargs.get('conversation_pk')
        return Message.objects.filter(conversation_id=conversation_pk)

    def perform_create(self, serializer):
        """
        Associates the message with the sender and conversation.
        """
        conversation_pk = self.kwargs.get('conversation_pk')
        conversation = get_object_or_404(Conversation, pk=conversation_pk)

        if self.request.user not in conversation.participants.all():
            raise permissions.PermissionDenied(
                "You are not a participant in this conversation."
            )

        serializer.save(sender=self.request.user, conversation=conversation)