from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
import random
import string

class UserProfileManager( BaseUserManager ):
	"""Manager for User Profiles"""

	def create_user( self, email, name, password = None ):
		"""Create a new User Profile"""
		if not email:
			raise ValueError( 'Email address is required!' )
		# normalize email
		email = self.normalize_email( email )
		token = self.create_token( 64 )
		user = self.model( email = email, name = name, token = token )
		# encrypt user password
		user.set_password( password )
		user.save( using=self._db )
		return user

	def create_superuser( self, email, name, password ):
		"""Create a Super User Profile"""
		user = self.create_user( email, name, password )
		user.is_superuser = True
		user.save( using=self._db )
		return user

	def create_token( self, len ):
		return ''.join( random.choices( string.ascii_letters + string.digits, k = len ) )


class UserProfile( AbstractBaseUser, PermissionsMixin ):
	"""Database Model for Users"""
	id = models.AutoField( primary_key=True, help_text="ID -> PK, Auto Increment" )
	email = models.EmailField( max_length=255, unique = True )
	name = models.CharField( max_length=255 )
	token = models.CharField( max_length=64 )

	objects = UserProfileManager( )

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = [ 'name' ]
 
	def get_id( self ):
		"""Retrieve ID of the User"""
		return self.id

	def get_name( self ):
		"""Retrieve Full name of the User"""
		return self.name
	
	def get_email( self ):
		"""Retrieve email of the User"""
		return self.email

	def __str__( self ):
		"""Retrieve string representation of the User"""
		return self.email