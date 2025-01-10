from cProfile import label
from os.path import exists
from tempfile import template

from django import forms
from django.core.exceptions import ValidationError
from users.forms.bootstrap import BootStrapForm
from django.contrib.auth.models import User
from users.models import UserProfile


class RegisterModelForm(BootStrapForm, forms.ModelForm):
    username = forms.CharField(
        label='用户名',
        max_length=64,
    )

    password = forms.CharField(
        label='密码',
        max_length=64,
        min_length=8,
        error_messages={
            'min_length': '密码长度不能小于8个字符',
            'max_length': '密码长度不能大于64个字符'
        },
        widget=forms.PasswordInput()
    )

    confirm_password = forms.CharField(
        label='重复密码',
        max_length=64,
        min_length=8,
        error_messages={
            'min_length': '密码长度不能小于8个字符',
            'max_length': '密码长度不能大于64个字符'
        },
        widget=forms.PasswordInput()
    )

    email = forms.EmailField(
        label='邮箱',
        max_length=64,
    )

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'confirm_password', 'nickname', 'birthday', 'gender', 'image']

    def clean_username(self):
        username = self.cleaned_data['username']
        exists = User.objects.filter(username=username).exists()
        if exists:
            raise ValidationError('用户名已存在')
        return username

    def clean_password(self):
        pwd = self.cleaned_data['password']
        return pwd

    def clean_confirm_password(self):
        pwd = self.cleaned_data['password']
        confirm_pwd = self.cleaned_data['confirm_password']
        if pwd != confirm_pwd:
            raise ValidationError('密码不一致')
        return confirm_pwd

    def clean_email(self):
        email = self.cleaned_data['email']
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise ValidationError('邮箱已存在')
        return email

    def clean_image(self):
        image = self.cleaned_data['image']
        return image






class LoginForm(BootStrapForm, forms.Form):
    username = forms.CharField(label='邮箱或用户名',required=True)
    password = forms.CharField(label='密码', widget=forms.PasswordInput(render_value=True),required=True)


    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request


    def clean_username(self):
        username = self.cleaned_data['username']
        return username



    def clean_password(self):
        pwd = self.cleaned_data['password']
        return pwd








class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nickname', 'signature', 'gender', 'birthday', 'desc', 'image']







class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label="当前密码", required=True)
    new_password = forms.CharField(
        label='新密码',
        max_length=64,
        min_length=8,
        error_messages={
            'min_length': '密码长度不能小于8个字符',
            'max_length': '密码长度不能大于64个字符'
        },
        widget=forms.PasswordInput()
    )

    confirm_password = forms.CharField(
        label='确认新密码',
        max_length=64,
        min_length=8,
        error_messages={
            'min_length': '密码长度不能小于8个字符',
            'max_length': '密码长度不能大于64个字符'
        },
        widget=forms.PasswordInput()
    )

    def __init__(self, *args, **kwargs):
        # 在初始化时传入 user 对象
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise ValidationError("当前密码不正确。")
        return old_password

    def clean_confirm_password(self):
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')

        # 比较新密码和确认密码是否一致
        if new_password != confirm_password:
            raise ValidationError("新密码和确认密码不匹配。")
        return confirm_password







class ChangeEmailForm(forms.Form):
    new_email = forms.EmailField(
        label="新邮箱",
        required=True,
        error_messages={
            'required': '新邮箱地址不能为空。',
            'invalid': '请输入有效的邮箱地址。',
        }
    )
    password = forms.CharField(
        label="当前密码",
        widget=forms.PasswordInput,
        required=True,
        error_messages={'required': '密码不能为空。'}
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not self.user.check_password(password):
            raise ValidationError("当前密码不正确。")
        return password

    def clean_new_email(self):
        new_email = self.cleaned_data.get('new_email')
        if User.objects.filter(email=new_email).exists():
            raise ValidationError("该邮箱已被使用。")
        return new_email
