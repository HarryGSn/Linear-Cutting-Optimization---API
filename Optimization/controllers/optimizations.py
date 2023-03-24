from django.http import HttpResponse, JsonResponse
# from ..serializers.optimizations import OptimizationSerializer
# from Optimization.models import Optimizations 
from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from ..paginators.items import ItemsPaginator
# from django.db.models import Count
import json

# @api_view( [ 'GET' ] )
# def test(request):
#     return HttpResponse( 'test!' )

# @api_view( [ 'GET' ] )
# def get_all( request ):
#     count = Optimizations.objects.aggregate(count=Count('id'))['count']
#     paginator = ItemsPaginator( default_limit = 10, max_limit = 100, count = count)
#     offset = paginator.get_offset( request )
#     limit = paginator.get_limit( request )
#     optimizations = Optimizations.objects.all()[offset:offset+limit]
#     paginated_optimizations = paginator.paginate_queryset( optimizations, request )
#     serializer = OptimizationSerializer( paginated_optimizations, many = True )
#     return paginator.get_paginated_response( serializer.data )

@api_view( [ 'POST' ] )
def create( request ):
    #load the request data from the body
    json_object = json.loads( request.body )
    #get the required values / parameters
    left_trim = json_object.get( 'settings', { } ).get( 'trim', { } ).get( 'left', 0 )
    right_trim = json_object.get( 'settings', { } ).get( 'trim', { } ).get( 'right', 0 )
    kerf = json_object.get( 'settings', { } ).get( 'kerf', 0 )
    parts = json_object.get( 'parts', [ ] )
    bar_length = json_object.get( 'bar_length', 6000 )
    # subtract the kerf and the left, right trim, if any
    if left_trim:
        bar_length -= left_trim + kerf
    if right_trim:
        bar_length -= right_trim + kerf
    # use the optimize parts controller to return the number of bars and the cuts placed in each bar
    result = optimize_parts( bar_length=bar_length, kerf=kerf, parts=parts )
    # print( result )
    # respond with a json object
    return JsonResponse( { 'cuts': result } )


# optimization algorithm implementing first-fit method
def optimize_parts( bar_length, kerf, parts ):
    # Sort the required lengths in descending order
    parts.sort( reverse=True )

    # Initialize the list of bins with the first empty bin
    bars = [[bar_length, []]]

    # Iterate over the required lengths and pack them into the bins
    for length in parts:
        # Try to pack the length into the first available bin
        for bar in bars:
            if bar[0] >= length + kerf:
                bar[0] -= length + kerf
                bar[1].append(length)
                break
        else:
            # If no available bin can accommodate the length, create a new bin
            bars.append([bar_length - length - kerf, [length]])

    # Return the list of cuts for each bin
    return [bar[1] for bar in bars]
