from django.contrib import admin
from django.urls import path, re_path, include
from . import views

# custom routes
from Optimization.routes.optimizations import urlpatterns as optimizations_urlpatterns

urlpatterns = [
    # admin is handle in admin site
	path( 'admin/', admin.site.urls ),
    
    # custom routes handling below
	path( 'optimizations', include( optimizations_urlpatterns ) ),
    
    # everything else returns 404 not found status, including a message
    re_path( r'^.*$', views.NotFound, name="not-found" ),
]
