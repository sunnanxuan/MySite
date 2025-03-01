# Generated by Django 5.1.4 on 2025-01-17 03:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0005_post_is_hot_post_pv"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField(verbose_name="评论内容")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="评论时间"),
                ),
                (
                    "is_approved",
                    models.BooleanField(default=True, verbose_name="是否审核通过"),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="blog.post",
                        verbose_name="所属文章",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="评论者",
                    ),
                ),
            ],
            options={
                "verbose_name": "评论",
                "verbose_name_plural": "评论",
                "ordering": ["-created_at"],
            },
        ),
    ]
