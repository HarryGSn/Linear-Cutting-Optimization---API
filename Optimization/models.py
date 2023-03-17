from django.db import models
# from django.contrib.auth.models import AbstractBaseUser
# from django.contrib.auth.models import PermissionsMixin
# from django.contrib.auth.models import BaseUserManager

# class UserProfileManager( BaseUserManager ):
#     """Manager for User Profiles"""

# 	def create_user( self, email, name, password = None ):
# 		"""Create a new User Profile"""
# 		if not email:
# 			raise ValueError( 'Email address is required!' )
# 		# normalize email
#   		email = self.normalize_email( email )
# 		user = self.model( email = email, name = name )
# 		# encrypt user password
# 		user.set_password( password )
# 		user.save( using=self._db )
# 		return user

# 	def create_superuser( self, email, name, password ):
# 		"""Create a Super User Profile"""
# 		user = self.create_user( email, name, password )
# 		user.is_superuser = True
# 		user.save( using=self._db )
# 		return user


# class UserProfile( AbstractBaseUser, PermissionsMixin ):
#     """Database Model for Users"""
#     id = models.AutoField( primary_key=True, help_text="ID -> PK, Auto Increment" )
# 	email = models.EmailField( max_length=255, unique=true )
# 	name = models.CharField( max_length=255 )

# 	objects = UserProfileManager( )

# 	USERNAME_FIELD = 'email'
# 	REQUIRED_FIELDS = [ 'name' ]
 
# 	def get_name( self ):
# 		"""Retrieve ID of the User"""
# 		return self.id

# 	def get_name( self ):
# 		"""Retrieve Full name of the User"""
# 		return self.name
	
#  	def get_email( self ):
# 		"""Retrieve email of the User"""
# 		return self.email

# 	def __str__( self ):
# 		"""Retrieve string representation of the User"""
# 		return self.email


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

    # def get_absolute_url(self):
    #     return reverse("Optimization_detail", kwargs={"pk": self.pk})
