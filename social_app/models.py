from django.db import models
from django.contrib.auth.models import AbstractUser
from taggit.managers import TaggableManager

# Create your models here.


class User(AbstractUser):
    date_of_birth = models.DateTimeField(blank=True, null=True)
    bio = models.CharField(max_length=500, blank=True, null=True)
    photo = models.ImageField(upload_to="users-photo/", blank=True, null=True)
    job = models.CharField(max_length=500, blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)


class Post(models.Model):
    """ post model for posts in my website """
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_post')
    # data fields
    discription = models.TextField(max_length=1000)

    # date
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    tags = TaggableManager()

    objects = models.Manager()

    class Meta:
        """ ORDERING """
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"])
        ]

    def __str__(self):
        """ str for class """
        return self.discription
