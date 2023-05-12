from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponseForbidden

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.rate_limit_requests = getattr(settings, 'RATE_LIMIT_REQUESTS', 100)
        self.rate_limit_timeout = getattr(settings, 'RATE_LIMIT_TIMEOUT', 3600)

    def __call__(self, request):
        client_ip = request.META.get('REMOTE_ADDR')
        cache_key = f"ratelimit:{client_ip}"
        request_count = cache.get(cache_key, 0)
        request_count += 1
        cache.set(cache_key, request_count, timeout=self.rate_limit_timeout)

        if request_count > self.rate_limit_requests:
            return HttpResponseForbidden( b'Too many requests' )

        response = self.get_response(request)
        return response
