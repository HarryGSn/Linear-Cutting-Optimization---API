from django.shortcuts import render        
from django.http import HttpResponse
import json

def test(request):
    value = {
        "language": 1,
        "company": 2,
        "Itemid": 3,
        "price": 4
    }
    return HttpResponse(json.dumps(value), content_type="application/json")
