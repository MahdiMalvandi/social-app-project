# Generated by Django 4.2.6 on 2023-11-15 14:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social_app', '0016_post_total_likes_post_social_app__total_l_a271d6_idx'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(max_length=1000)),
                ('subject', models.CharField(choices=[('BG', 'bug'), ('PR', 'proposal'), ('CR', 'critics')], default='BG', max_length=2)),
                ('answer', models.TextField(max_length=1000)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_tickets', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
