# chats/permissions.py

from rest_framework import permissions
from .models import Conversation, Message

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Assumes the model instance has an 'owner' or 'user' attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        # This assumes your model has a field named 'owner' that links to the User model.
        # If your model links to 'user' or 'creator', adjust 'obj.owner' accordingly.
        return obj.owner == request.user

class IsMessageSender(permissions.BasePermission):
    """
    Custom permission to only allow the sender of a message to view/edit it.
    Assumes the Message model has a 'sender' field.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.sender == request.user or obj.receiver == request.user
        
        return obj.sender == request.user

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow access only to authenticated users who are
    participants of the relevant conversation.

    This permission works for both Conversation and Message viewsets.
    - For Conversation objects: checks if the user is a participant of the conversation.
    - For Message objects: checks if the user is a participant of the message's conversation.
    - For list/create operations (where no object exists yet):
      - For Conversations: allows creating a new conversation (assuming it will be populated with participants).
      - For Messages: checks if the user is a participant of the conversation specified in the URL kwargs.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        # For list/create actions on ConversationViewSet (e.g., POST /api/conversations/)
        # A user should be able to create a conversation.
        if view.basename == 'conversation' and request.method == 'POST':
            return True

        # For list/create actions on MessageViewSet (e.g., POST /api/conversations/{pk}/messages/)
        # We need to check if the user is a participant of the conversation from the URL.
        if view.basename == 'conversation-messages':
            conversation_pk = view.kwargs.get('conversation_pk')
            if not conversation_pk:
                return False

            conversation = get_object_or_404(Conversation, pk=conversation_pk)
            return request.user in conversation.participants.all()

        return True

    def has_object_permission(self, request, view, obj):

        if not request.user or not request.user.is_authenticated:
            return False

        # If the object is a Conversation
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()

        if isinstance(obj, Message): 
             return request.user in obj.conversation.participants.all()

        # Fallback for any other unexpected object types
        return False