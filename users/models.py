from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.

class UserProfile(models.Model):
    USER_GENDER_TYPE = (
        ('male','男'),
        ('female','女'),
    )
    owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    nickname=models.CharField(verbose_name='昵称',max_length=23,blank=True,null=True)
    birthday=models.DateTimeField(verbose_name='生日',blank=True,null=True)
    gender=models.CharField(verbose_name='性别', choices=USER_GENDER_TYPE,max_length=6,default='male')
    image=models.ImageField(verbose_name='用户头像',upload_to='image/%Y/%m',default='image/default.jpg',max_length=255)
    desc=models.TextField(verbose_name='个人简介',max_length=200,blank=True,default='')




class EmailVerification(models.Model):
    Send_TYPE_CHOICES = (
        ('register','注册'),
        ('retrieve','找回密码'),
    )

    code=models.CharField('验证码',max_length=20)
    email=models.EmailField('邮箱',max_length=35)
    send_type=models.CharField(choices=Send_TYPE_CHOICES,max_length=10,default='register')

    class Meta:
        verbose_name='邮箱验证码'
        verbose_name_plural=verbose_name


    def __str__(self):
        return self.code