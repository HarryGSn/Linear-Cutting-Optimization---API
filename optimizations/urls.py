from django.urls import path, re_path
from .controllers import create

urlpatterns = [
    # create an optimization request to retrieve optimized data
    re_path( r'^$', create, name='optimizations-create' ),
]