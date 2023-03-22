from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

class ItemsPaginator( LimitOffsetPagination ):
    def __init__( self, default_limit = 10, max_limit = 100, count = None ):
        self.default_limit = default_limit
        self.max_limit = max_limit
        self.count = count
        super( ).__init__( )
    
    def get_paginated_response(self, data):
        print( self.limit, self.offset )
        return Response( {
            'items': data,
            'links': {
                'next': self.get_next_link( ),
                'previous': self.get_previous_link( ),
                'limit': self.limit
            },
            'count': self.count
        } )
