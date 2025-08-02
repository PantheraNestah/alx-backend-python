
from django.urls import path
from .views import message_detail, delete_user_account, inbox_view

urlpatterns = [
    path('message/<int:message_id>/', message_detail, name='message_detail'),
    path('account/delete/', delete_user_account, name='delete_account'),
    path('inbox/', inbox_view, name='inbox'),
]