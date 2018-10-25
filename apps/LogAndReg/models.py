from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        email=User.objects.all().values().filter(email=postData['email'])
        if len(postData['First_Name']) < 3:
            errors["First_Name"] = "First_Name should be at least 3 characters"
        if postData['First_Name'].isalpha() is False:
            errors["First_Name"] = "Your first name can't have numbers"
        if len(postData['Last_Name']) < 3:
            errors["Last_Name"] = "Last_Name should be at least 3 characters"
        if postData['Last_Name'].isalpha() is False:
            errors["Last_Name"] = "Your Last name can't have numbers"
        if len(postData['email']) < 5:
            errors["email"] = "email should be at least 5 characters"
        if len(postData['password']) < 5:
            errors["password"] = "password should be at least 5 characters"
        if postData['password'] != postData['confirm_password']:
            errors["confirm_password"] = "password should match confirm password"
        if email:
            errors["email"] = "This email already exist. Please use a different email or log into your account"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "email is invalid"     
        return errors
    def login_validator(self, postData):
        errors = {}
        if len(postData['password']) < 1 :
            errors["password"] = "Password cannot be blank"
        try:
            user=User.objects.all().values().get(email=postData['email'])
            if user:
                if bcrypt.checkpw(postData['password'].encode(), user['password'].encode()):
                    print("Login Successful")
                else:
                    errors["password"] = "Incorrect Password"
                return errors
        except:
            errors['login'] = "Incorrect Email"
            return errors
class JobManager(models.Manager):
    def job_validator(self, postData):
        errors = {}
        if len(postData['Job_Title']) < 1 :
            errors["Job_Title"] = "Title cannot be blank"
        if len(postData['Job_Desc']) < 1 :
            errors["Job_Desc"] = "Description cannot be blank"
        if len(postData['Job_Loc']) < 1 :
            errors["Job_Loc"] = "Location cannot be blank"
        if len(postData['Job_Title']) < 3 :
            errors["Job_Title"] = "Title must be more than 3 characters"
        if len(postData['Job_Desc']) < 3 :
            errors["Job_Desc"] = "Description must be more than 3 characters"
        if len(postData['Job_Loc']) < 3 :
            errors["Job_Loc"] = "Location must be more than 3 characters"
        return errors
class User(models.Model):
    First_Name = models.CharField(max_length=255)
    Last_Name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
class Job(models.Model):
    Title = models.CharField(max_length=255)
    Desc = models.CharField(max_length=255)
    Location = models.CharField(max_length=255)
    Completed = models.BooleanField()
    Catagory = models.CharField(max_length=255)
    Creator = models.ForeignKey(User, related_name="jobs")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    OwnedBy =  models.IntegerField(null=True)
    objects = JobManager()