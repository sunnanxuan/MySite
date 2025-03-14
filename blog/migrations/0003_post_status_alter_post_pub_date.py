# Generated by Django 5.1.4 on 2025-01-14 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0002_post_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="status",
            field=models.CharField(
                choices=[("draft", "草稿"), ("published", "已发布")],
                default="draft",
                max_length=10,
                verbose_name="状态",
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="pub_date",
            field=models.DateTimeField(auto_now=True, verbose_name="修改时间"),
        ),
    ]
