from django.urls import path
from django.urls import re_path
from Optimization.controllers.optimizations import create #, get_all 

urlpatterns = [
    # re_path( r'^/?$', get_all, name='optimizations-get-all' ),
    re_path( r'^/?$', create, name='optimizations-create' ),
    # re_path( '/', get_all, name='optimizations-get-all' ),
    # re_path( r'^/test/?$', test ),
]