from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.shortcuts import render
from django.utils.functional import cached_property
from django.template.loader import render_to_string


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




class Sidebar(models.Model):

    STATUS = (
        (1,'隐藏'),
        (2,'展示')
    )

    DISPLAY_TYPE = (
        (1,'搜索'),
        (2,'最新文章'),
        (3,'最热文章'),
        (4,'最近评论'),
        (5,'文章归档'),
        (6,'HTML')
    )

    title = models.CharField(max_length=50,verbose_name='模块名称')
    display_type = models.PositiveIntegerField(default=1,choices=DISPLAY_TYPE,verbose_name="展示类型")
    content = models.CharField(max_length=500,blank=True,default='',verbose_name="内容", help_text='如果设置的不是HTML类型，可为空')
    sort = models.PositiveIntegerField(default=1,verbose_name='排序',help_text='序号越大越靠前')
    status = models.PositiveIntegerField(default=2,choices=STATUS,verbose_name='状态')
    add_date = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")


    class Meta:
        verbose_name="侧边栏"
        verbose_name_plural = verbose_name
        ordering = ['-sort']

    def __str__(self):
        return self.title

    @classmethod
    def get_sidebar(cls):
        return cls.objects.filter(status=2)

    @property
    def get_content(self):
        if self.display_type == 1:
            context = {

            }
            return render_to_string('search.html', context=context)
        elif self.display_type == 2:
            context = {

            }
            return render_to_string('new_post.html', context=context)
        elif self.display_type == 3:
            context = {

            }
            return render_to_string('hot_post.html', context=context)
        elif self.display_type == 4:
            context = {

            }
            return render_to_string('comment.html', context=context)
        elif self.display_type == 5:
            context = {

            }
            return render_to_string('archives.html', context=context)
        elif self.display_type == 6:
            return self.content


