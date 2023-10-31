from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.


class User(AbstractUser):
    date_of_birth = models.DateTimeField(blank=True, null=True)
    bio = models.CharField(max_length=500, blank=True, null=True)
    photo = models.ImageField(upload_to="users-photo/", blank=True, null=True)
    job = models.CharField(max_length=500, blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)


class Post(models.Model):
    """ post model for posts in my website """
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_post' )

    reading_time = models.PositiveIntegerField(verbose_name="reading time")
    # data fields
    caption = models.CharField(max_length=150)
    text = models.TextField()

    # date
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    class Meta:
        """ ORDERING """
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["-publish"])
        ]

    def __str__(self):
        """ str for class """
        return self.author


