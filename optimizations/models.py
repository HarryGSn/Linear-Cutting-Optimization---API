from django.db import models
from django.contrib.auth.models import User


class Optimization(models.Model):
	id = models.AutoField(primary_key=True, help_text="ID -> PK, Auto Increment")
	kerf = models.FloatField(default=0, null=False)
	bar_length = models.FloatField(default=0, null=False)
	deduct_left = models.FloatField(default=0, null=False)
	deduct_right = models.FloatField(default=0, null=False)
	created_at = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

	class Meta:
		db_table = "optimizations"
		verbose_name = "Optimization"
		verbose_name_plural = "Optimizations"
		
	def __str__(self):
		return f"Optimization {self.id} :: {self.created_at}"

class OptimizationBar(models.Model):
	id = models.AutoField(primary_key=True, help_text="ID -> PK, Auto Increment")
	optimization = models.ForeignKey(Optimization, on_delete=models.CASCADE)
	remnant = models.FloatField(default=0, null=False)
	class Meta:
		db_table = "optimization_bars"
		verbose_name = "OptimizationBar"
		verbose_name_plural = "OptimizationBars"

	def __str__(self):
		return f"{self.id} :: Optimization -> {self.optimization}"


class OptimizationBarPart(models.Model):
	id = models.AutoField(primary_key=True, help_text="ID -> PK, Auto Increment")
	optimization_bar = models.ForeignKey(OptimizationBar, on_delete=models.CASCADE)
	length = models.FloatField()
 
	class Meta:
		db_table = "optimization_bar_parts"
		verbose_name = "OptimizationBarPart"
		verbose_name_plural = "OptimizationBarParts"

	def __str__(self):
		return f"{self.id} :: Optimization Bar -> {self.optimization_bar}"

