# Generated by Django 5.1.4 on 2025-01-14 00:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="category",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="blog.category",
                verbose_name="分类",
            ),
            preserve_default=False,
        ),
    ]
