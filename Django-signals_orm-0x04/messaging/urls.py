
from django.urls import path
from .views import message_detail, delete_user_account, inbox_view, edit_message, conversation_thread_view

urlpatterns = [
    path('message/<int:message_id>/', message_detail, name='message_detail'),
    path('message/<int:message_id>/edit/', edit_message, name='edit_message'),
    path('thread/<int:message_id>/', conversation_thread_view, name='conversation_thread'),
    path('account/delete/', delete_user_account, name='delete_account'),
    path('inbox/', inbox_view, name='inbox'),
]
