from django.db.models.signals import m2m_changed
from .models import Post
from django.dispatch import receiver

@receiver(m2m_changed, sender=Post.likes.through)
def change_likes_count(sender, instance, **kwargs):
    instance.total_likes = instance.likes.count()
    instance.save()