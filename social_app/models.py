import os

from django.db import models
from django.contrib.auth.models import AbstractUser
from taggit.managers import TaggableManager
from django.urls import reverse

# Create your models here.


class User(AbstractUser):
    date_of_birth = models.DateTimeField(blank=True, null=True)
    bio = models.CharField(max_length=500, blank=True, null=True)
    photo = models.ImageField(upload_to="users-photo/", blank=True, null=True)
    job = models.CharField(max_length=500, blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    following = models.ManyToManyField('self', through="Following", related_name='followers', symmetrical=False)

    def get_absolute_url(self):
        return reverse('social:get user detail by username', args=[self.username])

class Post(models.Model):
    """ post model for posts in my website """
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_post')
    # data fields
    discription = models.TextField(max_length=1000)

    # date
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name="post_likes", blank=True)
    saved = models.ManyToManyField(User, related_name="post_saved", blank=True)
    total_likes = models.PositiveIntegerField(default=0)

    tags = TaggableManager()

    objects = models.Manager()

    class Meta:
        """ ORDERING """
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"]),
            models.Index(fields=["-total_likes"]),
        ]

    def __str__(self):
        """ str for class """
        return self.discription

    def delete(self, *args, **kwargs):
        for image in self.images.all():
            storage, path = image.image.storage, image.image.path
            storage.delete(path)
        super().delete(*args, **kwargs)

    def get_absolute_url(self, *args, **kwargs):
        return reverse('social:detail', args=[self.id])



class Comments(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    post_for = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', default='')


    def __str__(self):
        return self.text
    def get_absolute_url(self):
        return reverse('social:add_comment', args=[Post.pk])


class PostsImage(models.Model):
    image = models.ImageField(upload_to='posts-image/')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')

    def delete(self, *args, **kwargs):
        storage, path = self.image.storage, self.image.path
        os.remove(path)
        super().delete(*args, **kwargs)


class Following(models.Model):
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rel_to_set')
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rel_from_set')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        indexes = [ models.Index(fields=['-created_at'])]
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'


class Ticket(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_tickets')
    body = models.TextField(max_length=1000)
    subjects = [
        ("BG", "bug"),
        ("PR", "proposal"),
        ("CR", "critics"),
    ]
    subject = models.CharField(max_length=2, choices=subjects, default='BG')
    answer = models.TextField(max_length=1000)

    def __str__(self):
        return f'{self.subject} - {self.body}'