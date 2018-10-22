from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self,postData):
        errors={}
        if User.objects.filter(email=postData['email']):
            errors['email'] = "The user exist, please log in."
        else:    
            if len(postData['first_name']) < 1:
                errors['first_name'] = "First Name cannot be blank."
            elif str.isalpha(postData['first_name'])==False and len(postData['first_name']) >1:
                errors['first_name'] = "First Name cannot contain numbers."
            if len(postData['last_name']) < 1:
                errors['last_name'] = "Last Name cannot be blank."
            elif str.isalpha(postData['last_name'])==False and len(postData['last_name']) >1:
                errors['last_name'] = "Last Name cannot contain numbers."
            if len(postData['email']) < 1:
                errors['email'] = "Email cannot be blank."
            elif not EMAIL_REGEX.match(postData['email']):
                errors['email'] = "Invalid Email Address."
            if len(postData['code']) < 8 and len(postData['code']) >1:
                errors['code'] = "Password should be more than 8 characters."
            elif len(postData['code']) < 1:
                errors['code'] = "Password cannot be blank."
            if len(postData['confirm']) < 1:
                errors['confirm'] = "Password Confirmation cannot be blank."
            if postData['code'] != postData['confirm']:
                errors['code'] = "Password doesn't match with confirmation."
        
            
        return errors



class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

    def __str__(self):
        return self.first_name

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title

class Review(models.Model):
    content = models.CharField(max_length=255)
    rating = models.IntegerField()
    review_poster = models.ForeignKey(User,related_name="reviews")
    book_reviewed = models.ForeignKey(Book, related_name="reviews")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.book_reviewed.title


    