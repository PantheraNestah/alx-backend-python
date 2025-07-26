#!/usr/bin/env python3
"""
Defines the API views for the chats application.
"""
from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework.status import HTTP_403_FORBIDDEN


from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsOwnerOrReadOnly, IsMessageSender, IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter


class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for conversations with filtering, searching, and ordering.
    """
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]

    # Use DRF's filter backends for powerful query capabilities.
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    
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

    def perform_create(self, serializer):
        """
        When creating a conversation, the creator is automatically added as a participant.
        """
        # Save the conversation first
        conversation = serializer.save()
        # Add the creator as a participant
        conversation.participants.add(self.request.user)
        conversation.save()


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for messages within a conversation.
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]

    pagination_class = MessagePagination

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MessageFilter

    ordering_fields = ['sent_at']

    def get_queryset(self):
        """
        Filters messages based on the `conversation_pk` from the URL.
        """
        conversation_pk = self.kwargs.get('conversation_pk')
        conversation = get_object_or_404(Conversation, pk=conversation_pk)

        if self.request.user not in conversation.participants.all():
            raise HTTP_403_FORBIDDEN("You are not a participant in this conversation.")

        return Message.objects.filter(conversation_id=conversation_pk).order_by('sent_at')

    def perform_create(self, serializer):
        """
        Associates the message with the sender and conversation.
        """
        conversation_pk = self.kwargs.get('conversation_pk')
        conversation = get_object_or_404(Conversation, pk=conversation_pk)
        if self.request.user not in conversation.participants.all():
            raise HTTP_403_FORBIDDEN("You are not a participant in this conversation.")

        serializer.save(sender=self.request.user, conversation=conversation)