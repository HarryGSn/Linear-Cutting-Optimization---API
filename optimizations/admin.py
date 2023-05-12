from django.contrib import admin
from .models import Optimization, OptimizationBar, OptimizationBarPart

admin.site.register(Optimization)
admin.site.register(OptimizationBar)
admin.site.register(OptimizationBarPart)
