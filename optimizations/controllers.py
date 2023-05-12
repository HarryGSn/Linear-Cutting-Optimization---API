from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import AccessToken
from itertools import combinations, count
import jwt
import json
from django.shortcuts import get_object_or_404
from .serializers import OptimizationsSerializer, OptimizationSerializer
from .models import Optimization, OptimizationBar, OptimizationBarPart
from django.contrib.auth.models import User
from app.views import NotFound

@api_view( [ 'POST', 'GET' ] )
def optimizations( request ):
    if request.method == 'POST':
        # handle POST request
        return create( request )
    elif request.method == 'GET':
        # handle GET request
        return get( request )
    else:
        return NotFound( request )

def create( request ):
    #check for authorization if exists
    # Get the token from the request headers
    user_id = 0
    auth_header = request.headers.get('Authorization')
    if auth_header:
        # Extract the token from the Authorization header
        token = auth_header.split(' ')[1]
        try:
            # Decode the token to get the payload
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            # Now you can use the user_id variable as needed in your code
            print(f"The user ID is: {user_id}")
        except Exception as e:
            # Handle any errors that might occur
            return JsonResponse( { 'result': 'error', 'message': 'invalid token' }, status=401 )
    
    #load the request data from the body
    json_object = json.loads( request.body )
    #get the required values / parameters
    try:
        bar_length = float( json_object.get( 'settings', { } ).get( 'bar_length', 0 ) )
        left_trim = float( json_object.get( 'settings', { } ).get( 'trim', { } ).get( 'left', 0 ) )
        right_trim = float( json_object.get( 'settings', { } ).get( 'trim', { } ).get( 'right', 0 ) )
        kerf = float( json_object.get( 'settings', { } ).get( 'kerf', 0 ) )
    except:
        return JsonResponse( { 'result': 'error', 'message': 'invalid paramters' } )
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
    if user_id > 0:
        stored = store_optimization( bar_length, left_trim, right_trim, kerf, bars, user_id )
        return JsonResponse( { 'result': 'ok', 'solution': bars, 'stored':stored } )
    return JsonResponse( { 'result': 'ok', 'solution': bars } )

def get( request ):
    #check for authorization if exists
    # Get the token from the request headers
    user_id = 0
    auth_header = request.headers.get('Authorization')
    if auth_header:
        # Extract the token from the Authorization header
        token = auth_header.split(' ')[1]
        try:
            # Decode the token to get the payload
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            # Now you can use the user_id variable as needed in your code
            print(f"The user ID is: {user_id}")
        except Exception as e:
            # Handle any errors that might occur
            return JsonResponse( { 'result': 'error', 'message': 'invalid token' }, status=401 )
    if( user_id > 0 ):
        user = User.objects.get(id=user_id)
        optimizations = Optimization.objects.filter( created_by=user ).all( )
        serializer = OptimizationsSerializer(optimizations, many=True)
        return JsonResponse( { 'result': 'ok', 'optimizations': serializer.data } )
    else:
        return JsonResponse( { 'result': 'error', 'message': 'unauthorized' }, status=401 )

def store_optimization( bar_length, left_trim, right_trim, kerf, bars, user_id ):
    try:
        # Create an instance of Optimization
        user = User.objects.get(id=user_id)

        optimization = Optimization.objects.create(
            kerf=kerf,
            deduct_left=left_trim,
            deduct_right=right_trim,
            bar_length=bar_length,
            created_by=user,  # assuming you are using Django's authentication framework
        )

        # Loop through the bars list and create an instance of OptimizationBar and OptimizationPart for each bar
        for bar in bars:
            optimization_bar = OptimizationBar.objects.create(
                optimization=optimization,
                remnant=bar[ 'remnant' ],
            )

            for length in bar["parts"]:

                optimization_bar_part = OptimizationBarPart.objects.create(
                    optimization_bar=optimization_bar,
                    length=length,
                )
        return True
    except Exception as e:
        print( str( e ) )
        return False
    
def get_single( request, id ):
    user_id = 0
    auth_header = request.headers.get('Authorization')
    if auth_header:
        # Extract the token from the Authorization header
        token = auth_header.split(' ')[1]
        try:
            # Decode the token to get the payload
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            # Now you can use the user_id variable as needed in your code
            print(f"The user ID is: {user_id}")
        except Exception as e:
            # Handle any errors that might occur
            return JsonResponse( { 'result': 'error', 'message': 'invalid token' }, status=401 )
    user = User.objects.get(id=user_id)
    optimization = Optimization.objects.filter(id=id, created_by=user).first()
    serializer = OptimizationSerializer(optimization)
    res = None
    try:
        res = JsonResponse( serializer.data )
    except Exception as e:
        res = JsonResponse( { 'error' } )
    return res