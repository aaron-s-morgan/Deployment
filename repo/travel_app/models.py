from django.db import models
import re
from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters"
        if str.isalpha(postData['first_name']) == False:
            errors['first_name'] = "First name must be alpha only"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters"
        if str.isalpha(postData['last_name']) == False:
            errors['last_name'] = "Last name must be alpha only"
        if not EMAIL_REGEX.match(postData['email']):   
            errors['email'] = "Invalid email address!"
        users_with_email = User.objects.filter(email = postData['email'])
        if len(users_with_email) >= 1:
            errors['duplicate'] = "Email already exists."
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        if postData['password'] != postData['confirm_password']:
            errors['pw_match'] = "Password must match!"
        return errors

class TripManager(models.Manager):
    def trip_validator(self, postData):
        errors = {}

        if len(postData['destination']) < 3:
            errors['destination'] = "Destination must have 3 characaters or more"
        if len(postData['plan']) < 1:
            errors["plan"] = "Must have plan"
        if datetime.strptime(postData['start_date'], '%Y-%m-%d') < datetime.now():
                errors['start_date'] = 'Start date must be in the past'
        if datetime.strptime(postData['end_date'], '%Y-%m-%d') < datetime.strptime(postData['start_date'], '%Y-%m-%d'):
                errors['end_date'] = 'End date must be after start date'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length=75)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    plan = models.CharField(max_length=75)
    travelers = models.ManyToManyField(User, related_name="trips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()
    creator = models.ForeignKey(User, related_name="creations", on_delete=models.CASCADE)