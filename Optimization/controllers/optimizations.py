from django.http import HttpResponse, JsonResponse
# from ..serializers.optimizations import OptimizationSerializer
# from Optimization.models import Optimizations 
from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from ..paginators.items import ItemsPaginator
# from django.db.models import Count
import json
from itertools import combinations, count

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
    bar_length = json_object.get( 'settings', { } ).get( 'bar_length', 0 )
    left_trim = json_object.get( 'settings', { } ).get( 'trim', { } ).get( 'left', 0 )
    right_trim = json_object.get( 'settings', { } ).get( 'trim', { } ).get( 'right', 0 )
    kerf = json_object.get( 'settings', { } ).get( 'kerf', 0 )
    parts = json_object.get( 'parts', [ ] )
    
    # check if bar length is a valid value
    if bar_length <= .0:
        return JsonResponse( { 'result': 'error', 'message': 'missing bar length' } )
    # check if parts are present
    if len( parts ) < 1.0:
        return JsonResponse( { 'result': 'error', 'message': 'missing parts!' } )
    
    serialized_parts = [ ]
    # we shall keep it simple,
    # if a user wants to provide a serialized row, we will accept it.
    for part in parts:
        if isinstance( part, dict ) and 'quantity' in part and 'length' in part:
            for i in range( part['quantity']):
                if isinstance( part[ 'length' ], ( int, float ) ):
                    serialized_parts.append( part[ 'length' ] )
                else:
                    return JsonResponse( { 'result': 'error', 'message': 'invalid part length!' } )
        elif isinstance( part, ( int, float ) ):
            serialized_parts.append( part )
        else:
            return JsonResponse( { 'result': 'error', 'message': 'invalid part!' } )

    # check configuration regarding right and left trim
    if left_trim > bar_length or right_trim > bar_length:
        return JsonResponse( { 'result': 'error', 'message': 'invalid configuration, trim cannot exceed bar length!' } )
    
    # subtract the kerf and the left, right trim, if any, in order to get the usable bar length
    # usable bar length is the initial (total) bar lenght minus the left and right trim + kerf
    if left_trim and left_trim > 0:
        bar_length -= ( left_trim + kerf )
    if right_trim and right_trim > 0:
        bar_length -= ( right_trim + kerf )
    
    # usable bar length cannot be a negative number!
    if bar_length < .0:
        return JsonResponse( { 'result': 'error', 'message': 'invalid configuration, usable bar length cannot be less than 0!' } )
    
    # check if any part is longer than usable bar length
    for part in serialized_parts:
        if part > bar_length:
            return JsonResponse( { 'result': 'error', 'message': 'cannot optimize part longer than usable bar length!' } )

    parts = sorted( serialized_parts, reverse=True )
    remaining_parts = parts.copy( )
    bars = [ ]
    while remaining_parts:
        bar = [ ]
        length = 0
        while remaining_parts:
            part = max( [ p for p in remaining_parts if p + kerf <= bar_length - length ] + [ 0 ] )
            if part == 0:
                break
            bar.append( part )
            length += part + kerf
            remaining_parts.remove( part )
        bars.append( bar )

    # Optimize the part positions within each bar to minimize wastage
    for i in range( len( bars ) ):
        bar = bars[ i ]
        # Generate all possible combinations of part positions within the bar
        part_combinations = list( combinations( range( len( bar ) ), len( bar ) ) )
        # first o f all, I will set the best wastage to be a maximum number, in order to check the 
        # minumum available for the calculated
        best_wastage = float( 'inf' )
        best_part_order = [ ]
        # Find the combination with the least wastage
        for part_order in part_combinations:
            wastage = bar_length - sum( [ bar[ j ] for j in part_order ] )
            if wastage < best_wastage:
                best_wastage = wastage
                best_part_order = part_order
        # Rearrange the parts in the bar according to the best part order
        new_bar = [ ]
        for j in best_part_order:
            new_bar.append( bar[ j ] )
        bars[ i ] = new_bar
    
    # Calculate remaining space in each bar
    for i, bar in enumerate(bars):
        length = sum( bar )  # Total length of parts in current bar
        num_parts = len( bar )  # Number of parts in current bar
        remnant = bar_length - ( length + num_parts * kerf )  # Remaining material "remnant" in current bar
        bars[ i ] = {
            # keep these here for testing, if needed
            # 'bar_length': bar_length,
            # 'length': length,
            # 'num_parts': num_parts,
            # 'kerf': kerf,
            # to evaluate and see if we need it: add quantity here, in order to group them by parts!
            'index': i,
            'parts': sorted( bar, reverse=True ),
            'remnant': remnant
        }

    return JsonResponse( { 'result': 'ok', 'solution': bars } )