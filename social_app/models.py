from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    date_of_birth = models.DateTimeField(blank=True, null=True)
    bio = models.CharField(max_length=500, blank=True, null=True)
    photo = models.ImageField(upload_to="users-photo/", blank=True, null=True)
    job = models.CharField(max_length=500, blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
