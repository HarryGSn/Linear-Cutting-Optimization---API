from django.http import HttpResponse, JsonResponse
from ..serializers.optimizations import OptimizationSerializer
from Optimization.models import Optimizations 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..paginators.items import ItemsPaginator
from django.db.models import Count

@api_view( [ 'GET' ] )
def test(request):
    return HttpResponse( 'test!' )

@api_view( [ 'GET' ] )
def get_all( request ):
    count = Optimizations.objects.aggregate(count=Count('id'))['count']
    paginator = ItemsPaginator( default_limit = 10, max_limit = 100, count = count)
    offset = paginator.get_offset( request )
    limit = paginator.get_limit( request )
    optimizations = Optimizations.objects.all()[offset:offset+limit]
    paginated_optimizations = paginator.paginate_queryset( optimizations, request )
    serializer = OptimizationSerializer( paginated_optimizations, many = True )
    return paginator.get_paginated_response( serializer.data )