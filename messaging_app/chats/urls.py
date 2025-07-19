#!/usr/bin/env python3
"""
URL routing for the chats application.
"""
from django.urls import path, include
from rest_framework_nested import routers
from .views import ConversationViewSet, MessageViewSet

# The main router generates URLs for /conversations/
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# The nested router generates URLs like /conversations/{pk}/messages/
conversations_router = routers.NestedDefaultRouter(
    router,
    r'conversations',
    lookup='conversation'
)
conversations_router.register(
    r'messages',
    MessageViewSet,
    basename='conversation-messages'
)

# The urlpatterns list defines the final URL structure for the app
urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversations_router.urls)),
]