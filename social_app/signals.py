from django.db.models.signals import m2m_changed, post_delete, post_save
from .models import Post
from django.dispatch import receiver
from django.core.mail import send_mail


@receiver(m2m_changed, sender=Post.likes.through)
def change_likes_count(sender, instance, **kwargs):
    instance.total_likes = instance.likes.count()
    instance.save()

@receiver(post_delete, sender=Post)
def delete_post(sender, instance, **kwargs):
    author = instance.author
    subject = f'Your post has been deleted '
    message = f'Your post : {instance.discription}'
    send_mail(subject, message, 'mahdimalvandi6@gmail.com', [author.email],
              fail_silently=False)


