#!/usr/bin/env python3
"""
Defines the serializers for the chats application models.
"""
from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the custom User model.

    This serializer exposes essential user information. The password
    field is write-only to prevent it from ever being exposed in an API
    response.
    """
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name',
            'email', 'password', 'phone_number', 'role'
        ]
        # Ensure password is not readable
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """
        Overrides the default create method to handle password hashing.
        Uses Django's `create_user` helper function.
        """
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.
    """
    sender = serializers.ReadOnlyField(source='sender.username')

    class Meta:
        model = Message
        fields = ['id', 'sender', 'message_body', 'sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Conversation model.

    This serializer provides a detailed view of a conversation, nesting
    the full details of its participants and all associated messages.
    """
    # Use the UserSerializer to nest participant details in the response
    participants = UserSerializer(many=True, read_only=True)
    # Nest all messages within the conversation using the MessageSerializer
    messages = MessageSerializer(many=True, read_only=True)

    # This field is used only for creating a conversation
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True
    )

    class Meta:
        model = Conversation
        fields = [
            'id', 'participants', 'participant_ids', 'messages', 'created_at'
        ]

    def create(self, validated_data):
        """
        Overrides create to handle adding participants from a list of IDs.
        """
        # Extract the list of participant UUIDs
        participant_ids = validated_data.pop('participant_ids')
        participants = User.objects.filter(id__in=participant_ids)

        # Validate that all provided UUIDs correspond to existing users
        if len(participant_ids) != participants.count():
            raise serializers.ValidationError(
                "One or more participant IDs are invalid."
            )

        # Create the conversation and set its participants
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        return conversation
