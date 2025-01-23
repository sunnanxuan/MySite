from django.db import models
from django.contrib.auth.models import User, AbstractUser
from utils.user_avatar_upload_to import user_avatar_upload_to


# Create your models here.



"""

python manage.py makemigrations
python manage.py migrate

"""





class UserProfile(models.Model):
    USER_GENDER_TYPE = (
        ('male','男'),
        ('female','女'),
    )
    owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    nickname=models.CharField(verbose_name='昵称',max_length=23,blank=True,null=True)
    birthday=models.DateTimeField(verbose_name='生日',blank=True,null=True)
    gender=models.CharField(verbose_name='性别', choices=USER_GENDER_TYPE,max_length=6,default='male')
    image=models.ImageField(verbose_name='用户头像',upload_to=user_avatar_upload_to,default='image/default.jpg',max_length=255)
    desc=models.TextField(verbose_name='个人简介',max_length=200,blank=True,default='')
    signature=models.CharField(verbose_name='个性签名',max_length=50,blank=True,default='')

    def __str__(self):
        return f"{self.owner.username}'s Profile"






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





class Follow(models.Model):
    follower = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE, verbose_name="关注者")
    followed = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE, verbose_name="被关注者")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="关注时间")

    class Meta:
        verbose_name = "关注"
        verbose_name_plural = "关注关系"
        unique_together = ('follower', 'followed')  # 防止重复关注

    def __str__(self):
        return f"{self.follower.username} 关注 {self.followed.username}"

    @classmethod
    def is_following(cls, follower, followed):
        """检查用户是否关注了另一个用户"""
        return cls.objects.filter(follower=follower, followed=followed).exists()

    @classmethod
    def follow(cls, follower, followed):
        """执行关注操作"""
        if not cls.is_following(follower, followed):
            return cls.objects.create(follower=follower, followed=followed)
        return None

    @classmethod
    def unfollow(cls, follower, followed):
        """取消关注操作"""
        cls.objects.filter(follower=follower, followed=followed).delete()




class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE, verbose_name="发信人")
    recipient = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE, verbose_name="收信人")
    content = models.TextField(verbose_name="消息内容")
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name="发送时间")
    is_read = models.BooleanField(default=False, verbose_name="是否已读")

    class Meta:
        verbose_name = "私信"
        verbose_name_plural = "私信"
        ordering = ['-sent_at']  # 按发送时间倒序排列

    def __str__(self):
        return f"{self.sender.username} to {self.recipient.username} at {self.sent_at}"

    @classmethod
    def send_message(cls, sender, recipient, content):
        """发送私信"""
        return cls.objects.create(sender=sender, recipient=recipient, content=content)

    @classmethod
    def get_unread_messages(cls, user):
        """获取未读的私信"""
        return cls.objects.filter(recipient=user, is_read=False)

    def mark_as_read(self):
        """将消息标记为已读"""
        self.is_read = True
        self.save()

    def mark_as_unread(self):
        """将消息标记为未读"""
        self.is_read = False
        self.save()


class SystemMessage(models.Model):
    content = models.TextField(verbose_name="消息内容")
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name="发送时间")
    is_read = models.BooleanField(default=False, verbose_name="是否已读")
    recipient = models.ForeignKey(User, related_name='system_messages', on_delete=models.CASCADE,
                                  verbose_name="接收用户")

    class Meta:
        verbose_name = "系统消息"
        verbose_name_plural = "系统消息"
        ordering = ['-sent_at']  # 按发送时间倒序排列

    def __str__(self):
        return f"System message to {self.recipient.username} at {self.sent_at}"

    def mark_as_read(self):
        """将消息标记为已读"""
        self.is_read = True
        self.save()




