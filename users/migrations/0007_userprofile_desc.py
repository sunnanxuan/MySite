# Generated by Django 5.1.4 on 2024-12-12 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0006_remove_userprofile_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="desc",
            field=models.TextField(
                blank=True, default="", max_length=200, verbose_name="个人简介"
            ),
        ),
    ]
