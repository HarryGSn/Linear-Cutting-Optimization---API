from django.urls import re_path, path
from .controllers import optimizations, get_single

urlpatterns = [
    # create an optimization request to retrieve optimized data
    re_path( r'^$', optimizations, name='optimizations' ),
    re_path(r'^(?P<id>\d+)/?$', get_single, name='get_single_optimization')
]