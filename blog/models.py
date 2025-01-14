from django.db import models
from django.contrib.auth.models import User, AbstractUser


# Create your models here.



"""

python manage.py makemigrations
python manage.py migrate

"""






class Category(models.Model):
    name = models.CharField(max_length=32, verbose_name="分类名称")
    desc = models.TextField(max_length=200, blank=True, default="", verbose_name="分类描述")
    add_date = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="修改时间")

    class Meta:
        verbose_name="博客分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name



class Tag(models.Model):
    name = models.CharField(max_length=10, verbose_name="文章标签")
    add_date = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="修改时间")

    class Meta:
        verbose_name = "文章标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name





class Post(models.Model):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = [
        (DRAFT, '草稿'),
        (PUBLISHED, '已发布'),
    ]

    title = models.CharField(max_length=61, verbose_name="文章标题")
    desc = models.TextField(max_length=200, blank=True, default="", verbose_name="文章描述")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="分类")
    content = models.TextField(verbose_name="文章详情")
    tags = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name="文章标签")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
    add_date = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    pub_date = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=DRAFT, verbose_name="状态")

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

