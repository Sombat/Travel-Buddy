from __future__ import unicode_literals
from django.db import models
import re, bcrypt
from datetime import date, datetime, timedelta

class UserManager(models.Manager):
	def register_validator(self, postData):
		userinDB_filter = User.objects.filter(username=postData['username'])
		errors = {}
		# print(len(User.objects.filter(username="postData['username']")))
		if len(postData['name']) < 3 or str.isalpha(postData['name']) == False:
			errors["name"] = "Name should be at least 3 characters, and contain only letters."
		if len(postData['username']) < 3 or str.isalpha(postData['username']) == False:
			errors["username"] = "Username should be at least 3 characters, and contain only letters."
		if len(userinDB_filter) != 0:
			errors["username_2"] = "Username already taken."
		if len(postData['password']) < 8:
			errors["last_name"] = "Password should be at least 8 characters."
		if postData['password'] != postData['confirm_password']:
			errors["password"] = "Password and confirmation does not match."
		return errors

	def login_validator(self, postData):
		userinDB_filter = User.objects.filter(username=postData['username'])
		errors = {}
		if len(userinDB_filter) == 0:
			errors['username'] = "User does not exist."
		else:
			userinDB_get = User.objects.get(username=postData['username'])
			if not bcrypt.checkpw(postData['password'].encode(), userinDB_get.password.encode()): 
				errors['password'] = "Password does not match."
		print(errors)
		return errors

class TripManager(models.Manager):
	def trip_validator(self, postData):
		errors = {}
		if len(postData['destination']) < 1:
			errors["destination"] = "Destination cannot be empty."
		if len(postData['description']) < 1:
			errors["description"] = "Description cannot be empty."
		# if datetime.strptime(postData['travel_start'], "%Y-%m-%d" ) < datetime.today():
		if postData['travel_start'] < str(datetime.today()):
			errors["travel_start"] = "Travel start date should not be before today."
		if postData['travel_end'] < postData['travel_start']:
			errors["travel_end"] = "Travel end date should not be before travel start date."
		return errors

class User(models.Model):
	name = models.CharField(max_length=255)
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

class Trip(models.Model):
	destination = models.CharField(max_length=50)
	description = models.CharField(max_length=255)
	travel_start = models.DateField()
	travel_end = models.DateField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	creator = models.ForeignKey(User, related_name="trips_created", on_delete=models.CASCADE)
	guest = models.ManyToManyField(User, related_name="trips_guest_of")
	objects = TripManager()