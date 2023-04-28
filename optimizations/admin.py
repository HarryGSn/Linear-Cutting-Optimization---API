from django.contrib import admin
from .models import Optimization, OptimizationPart, OptimizationBar, OptimizationBarPart

admin.site.register(Optimization)
admin.site.register(OptimizationPart)
admin.site.register(OptimizationBar)
admin.site.register(OptimizationBarPart)
