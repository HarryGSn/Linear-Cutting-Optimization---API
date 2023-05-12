from rest_framework import serializers
from .models import Optimization, OptimizationBar, OptimizationBarPart

class OptimizationsSerializer( serializers.ModelSerializer ):
    class Meta:
        model = Optimization
        fields = ( 'id', 'kerf', 'bar_length', 'deduct_left', 'deduct_right', 'created_at' )


class OptimizationBarPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptimizationBarPart
        fields = ('id', 'length')

class OptimizationBarSerializer(serializers.ModelSerializer):
    optimization_bar_parts = OptimizationBarPartSerializer(many=True, read_only=True)
    class Meta:
        model = OptimizationBar
        fields = ('id', 'optimization_bar_parts')

class OptimizationSerializer(serializers.ModelSerializer):
    optimization_bar_parts = serializers.SerializerMethodField()
    optimization_bars = OptimizationBarSerializer(many=True, read_only=True)

    class Meta:
        model = Optimization
        fields = ('id', 'kerf', 'bar_length', 'deduct_left', 'deduct_right', 'created_at', 'created_by', 'optimization_bar_parts', 'optimization_bars')

    def get_optimization_bar_parts(self, optimization):
        optimization_bars = optimization.optimizationbar_set.all()
        parts = []
        for optimization_bar in optimization_bars:
            optimization_bar_parts = optimization_bar.optimizationbarpart_set.all()
            parts.append({
                # 'optimization_bar_id': optimization_bar.id,
                'remnant': optimization_bar.remnant,
                'parts': OptimizationBarPartSerializer(optimization_bar_parts, many=True).data
            })
        return parts
