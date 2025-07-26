# chats/pagination.py

from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    page_size = 20 # Number of messages per page
    page_size_query_param = 'page_size' # Allows clients to override page size with ?page_size=X
    max_page_size = 100 # Maximum page size a client can request