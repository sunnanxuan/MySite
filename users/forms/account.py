from cProfile import label
from os.path import exists
from tempfile import template

from django.conf import settings
from django.core.validators import RegexValidator
from django import forms
from django.core.exceptions import ValidationError
from users import models
from users.forms.bootstrap import BootStrapForm
from utils import encrypt
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
        return encrypt.md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data['password']
        confirm_pwd = encrypt.md5(self.cleaned_data['confirm_password'])
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
        return encrypt.md5(pwd)




