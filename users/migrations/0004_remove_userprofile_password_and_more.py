# Generated by Django 5.1.4 on 2024-12-10 04:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_remove_userprofile_nike_name_userprofile_nickname_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="password",
        ),
        migrations.RemoveField(
            model_name="userprofile",
            name="username",
        ),
    ]
