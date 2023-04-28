from django.http import JsonResponse

def NotFound( request ):
    return JsonResponse( { "message": "NOT_FOUND" } )