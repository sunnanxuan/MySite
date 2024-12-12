# Generated by Django 5.1.4 on 2024-12-09 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="address",
        ),
        migrations.AddField(
            model_name="userprofile",
            name="email",
            field=models.EmailField(default="", max_length=32, verbose_name="邮箱"),
        ),
    ]
