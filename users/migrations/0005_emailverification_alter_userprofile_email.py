# Generated by Django 5.1.4 on 2024-12-10 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_remove_userprofile_password_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="EmailVerification",
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
                ("code", models.CharField(max_length=20, verbose_name="验证码")),
                ("email", models.EmailField(max_length=35, verbose_name="邮箱")),
                (
                    "send_type",
                    models.CharField(
                        choices=[("register", "注册"), ("retrieve", "找回密码")],
                        default="register",
                        max_length=10,
                    ),
                ),
            ],
            options={
                "verbose_name": "邮箱验证码",
                "verbose_name_plural": "邮箱验证码",
            },
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="email",
            field=models.EmailField(max_length=32, verbose_name="邮箱（必填）"),
        ),
    ]
