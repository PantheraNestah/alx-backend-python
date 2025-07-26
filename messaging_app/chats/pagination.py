# chats/pagination.py

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class MessagePagination(PageNumberPagination):
    page_size = 20 # Number of messages per page
    page_size_query_param = 'page_size' # Allows clients to override page size with ?page_size=X
    max_page_size = 100 # Maximum page size a client can request

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })