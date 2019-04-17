from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.

class User(AbstractBaseUser):
    follow_users = models.ManyToManyField(settings.AUTH_USER_MODEL,
    related_name='following_users',blank=True)
    
    