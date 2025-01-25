from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from users.forms.account import LoginForm, RegisterModelForm, UserProfileForm, ChangePasswordForm, ChangeEmailForm, \
    ForgetPwdForm, ModifyPwdForm
from utils.send_emali import send_register_email
from users.models import UserProfile, EmailVerification
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import logout
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm





# Create your views here.



def login(request):
    if request.user.is_authenticated:
        return redirect('home')  #

    if request.method == 'GET':
        form = LoginForm(request)  # 传递 request 参数
        return render(request, 'account/login.html', {'form': form})

    form = LoginForm(request, data=request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = User.objects.filter(
            Q(username=username) | Q(email=username)
        ).first()

        if user is not None:
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                auth_login(request, user)
                return JsonResponse({'status': True, 'data':reverse('blog:index')})
            else:
                form.add_error('username', '用户名或密码错误')
        else:
            form.add_error('username', '用户不存在')

    return JsonResponse({'status': False, 'error': form.errors})







def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request, 'account/register.html', {'form': form})

    form = RegisterModelForm(data=request.POST, files=request.FILES)

    if form.is_valid():
        cleaned_data = form.cleaned_data
        user_data = {
            'username': cleaned_data['username'],
            'password': cleaned_data['password'],
            'email': cleaned_data['email'],
        }
        profile_data = {
            'nickname': cleaned_data['nickname'],
            'birthday': cleaned_data['birthday'],
            'image': cleaned_data['image'],
        }

        with transaction.atomic():
            user = User.objects.create_user(**user_data)
            # 邮件暂时无法发送，设置管理员权限
            user.is_staff = False
            user.save()
            UserProfile.objects.create(owner=user, **profile_data)


        send_register_email(user.email, 'register')
        return JsonResponse({'status': True, 'data': reverse('users:active')})
    else:
        return JsonResponse({'status': False, 'error': form.errors})





def active(request):
    return render(request, 'account/active.html')




def active_user(request,active_code):
    all_records =EmailVerification.objects.filter(code=active_code)
    if all_records:
        for record in all_records:
            email = record.email
            user=User.objects.get(email=email)
            user.is_staff=True
            user.save()
    else:
        return HttpResponse('链接有误')
    return redirect('users:login')





@login_required(login_url='login')
def user_home(request):
    return render(request, 'layout/user.html', {'page_template': 'user_home.html', 'active_menu': 'user-info',  # 标记为 '个人中心' 菜单
        'active_link': 'user_home'})





@login_required(login_url='login')
def user_profile(request):
    return render(request, 'user_profile.html', { 'active_menu': 'user-info',  'active_link': 'user_profile' })








@login_required(login_url='login')
def editor_users(request):
    user_profile = request.user.userprofile  # 获取当前用户的用户信息

    if request.method == 'POST':
        # 创建一个表单实例并绑定数据
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            # 如果表单有效，保存更新的用户资料
            form.save()
            messages.success(request, "信息修改成功！")
            return render(request, 'user_profile.html', { 'active_menu': 'user-info',  # 标记为 '个人中心' 菜单
        'active_link': 'user_profile'})
    else:
        # 如果是 GET 请求，渲染空表单
        form = UserProfileForm(instance=user_profile)

    return render(request, 'editor_users.html', { 'form': form, 'active_menu': 'user-info',  # 标记为 '个人中心' 菜单
        'active_link': 'user_profile'})






@login_required(login_url='login')
def account_safety(request):
    return render(request, 'account/account_safety.html', {'active_menu': 'user-info',  # 标记为 '个人中心' 菜单
        'active_link': 'account_safety'})




@login_required
def change_email(request):
    if request.method == 'POST':
        form = ChangeEmailForm(request.POST, user=request.user)
        if form.is_valid():
            # 更新邮箱
            new_email = form.cleaned_data['new_email']
            request.user.email = new_email
            request.user.save()

            messages.success(request, '邮箱地址已成功更换！')
            return render(request, 'account/account_safety.html', {'active_menu': 'user-info',  # 标记为 '个人中心' 菜单
        'active_link': 'account_safety'})
        else:
            # 表单无效，返回带错误信息的页面
            return render(request, 'account/change_email.html', {'form': form, 'active_menu': 'user-info',  # 标记为 '个人中心' 菜单
        'active_link': 'account_safety'})

    else:
        form = ChangeEmailForm(user=request.user)  # 初始化表单

    return render(request, 'account/change_email.html', {'form': form, 'active_menu': 'user-info',  # 标记为 '个人中心' 菜单
        'active_link': 'account_safety'})



@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)  # 传递当前用户

        if form.is_valid():
            # 获取新密码并更新
            new_password = form.cleaned_data['new_password']
            request.user.set_password(new_password)
            request.user.save()

            # 重新登录以更新会话
            update_session_auth_hash(request, request.user)

            messages.success(request, '密码修改成功！')
            return render(request, 'account/account_safety.html', {'active_menu': 'user-info', 'active_link': 'account_safety'})
        else:
            # 如果表单无效，将错误信息显示到页面
            return render(request, 'account/change_password.html', {'form': form, 'active_menu': 'user-info',  # 标记为 '个人中心' 菜单
        'active_link': 'account_safety'})

    else:
        form = ChangePasswordForm(user=request.user)  # 初始化时传递当前用户

    return render(request, 'account/change_password.html', {'form': form, 'active_menu': 'user-info',  # 标记为 '个人中心' 菜单
        'active_link': 'account_safety'})




def forgot_password(request):
    if request.method == 'GET':
        form = ForgetPwdForm()
    else:
        form = ForgetPwdForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            exists = User.objects.filter(email=email).exists()
            if exists:
                send_register_email(email, 'retrieve')
                # 返回 JSON 响应
                return JsonResponse({'status': True, 'data': reverse('users:success-page')})
            else:
                return JsonResponse({'status': False, 'error': {'email': ['该邮箱尚未注册，请前往注册！']}})
        else:
            # 返回表单错误
            return JsonResponse({'status': False, 'error': form.errors})

    return render(request, 'forgot_password.html', {'form': form})




def forget_pwd_url(request, active_code):
    if request.method == 'GET':
        form = ModifyPwdForm()
    else:
        form = ModifyPwdForm(request.POST)
        if form.is_valid():
            try:
                record = EmailVerification.objects.get(code=active_code)
                email = record.email
                user = User.objects.get(email=email)
                user.password = make_password(form.cleaned_data.get('password'))
                user.save()
                return JsonResponse({'status': True, 'data': reverse('users:reset_success')})
            except EmailVerification.DoesNotExist:
                return JsonResponse({'status': False, 'error': '无效的激活码'})
        else:
            return JsonResponse({'status': False, 'error': form.errors})

    return render(request, 'reset_pwd.html', {'form': form, 'active_code': active_code})





def success_page(request):
    return render(request, 'account/success-page.html')




def reset_success(request):
    return render(request, 'account/reset_success.html')




def logout_view(request):
    logout(request)
    return redirect('users:login')




