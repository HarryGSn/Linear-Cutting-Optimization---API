from django.shortcuts import render        
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.http import JsonResponse
# import json

def test(request):
    value = {
        "language": 1,
        "company": 2,
        "Itemid": 3,
        "price": 4
    }
    return JsonResponse( value )

def NotFound( request ):
    return JsonResponse( { "message": "NOT_FOUND" } )