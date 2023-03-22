from rest_framework import serializers
from Optimization.models.optimizations import Optimizations

class OptimizationSerializer( serializers.ModelSerializer ):
    class Meta:
        model = Optimizations
        fields = [ 'id', 'kerf', 'left_deduction', 'right_deduction' ]