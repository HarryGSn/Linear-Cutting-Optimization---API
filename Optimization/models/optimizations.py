from django.db import models

class Optimizations(models.Model):
    """Database Model for Optimizations"""
    # ID -> PK, Auto Increment
    id = models.AutoField(primary_key=True, help_text="ID -> PK, Auto Increment")
    # Kerf is the Saw Blade "Width", also known as saw cut deduction
    kerf = models.FloatField(default=0, help_text="Saw Cut Deduction")
    # Left bar deduction, which will be removed (trimmed) upon request
    left_deduction = models.FloatField(default=0, help_text="Left bar deduction")
    # Right bar deduction, which will be removed (trimmed) upon request
    right_deduction = models.FloatField(default=0, help_text="Right bar deduction")
    # Date of the Request
    created_at = models.DateField(auto_now_add=True, help_text="Request date")
    # User who called the API, if NULL, user is not logged-in
    # I will enable this in the future
    # created_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, help_text="API User, if NULL => unregisted user")

    class Meta:
        db_table = "optimizations"
        verbose_name = "Optimization"
        verbose_name_plural = "Optimizations"

    def __str__(self):
        # this is what we see on the database model;
        return f"{self.id} :: {self.created_at}"
