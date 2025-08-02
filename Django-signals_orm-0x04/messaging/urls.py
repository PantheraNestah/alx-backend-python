
from django.urls import path
from .views import (
    message_detail, delete_user_account, inbox_view, edit_message, 
    conversation_thread_view, sent_messages_view, user_conversations_view,
    unread_messages_dashboard
)

urlpatterns = [
    path('message/<int:message_id>/', message_detail, name='message_detail'),
    path('message/<int:message_id>/edit/', edit_message, name='edit_message'),
    path('thread/<int:message_id>/', conversation_thread_view, name='conversation_thread'),
    path('sent/', sent_messages_view, name='sent_messages'),
    path('conversations/', user_conversations_view, name='conversations'),
    path('unread-dashboard/', unread_messages_dashboard, name='unread_dashboard'),
    path('account/delete/', delete_user_account, name='delete_account'),
    path('inbox/', inbox_view, name='inbox'),
]
