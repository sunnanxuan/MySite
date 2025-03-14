# Generated by Django 5.1.4 on 2025-01-17 23:12

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0006_comment"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="favorited_users",
            field=models.ManyToManyField(
                blank=True,
                related_name="favorited_posts",
                to=settings.AUTH_USER_MODEL,
                verbose_name="收藏用户",
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="liked_users",
            field=models.ManyToManyField(
                blank=True,
                related_name="liked_posts",
                to=settings.AUTH_USER_MODEL,
                verbose_name="点赞用户",
            ),
        ),
    ]
