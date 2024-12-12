
from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from users.forms.account import LoginForm, RegisterModelForm
#from utils.send_emali import send_register_email
from .models import UserProfile, EmailVerification
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import logout
from django.db import transaction



# Create your views here.



def login(request):
    if request.user.is_authenticated:
        return redirect('home')  #

    if request.method == 'GET':
        form = LoginForm(request)  # 传递 request 参数
        return render(request, 'login.html', {'form': form})

    form = LoginForm(request, data=request.POST)
    print(form.errors)
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
                return JsonResponse({'status': True, 'data':'/home/'})
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
        return render(request, 'register.html', {'form': form})

    form = RegisterModelForm(data=request.POST)
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
            user.is_staff = True
            user.save()
            UserProfile.objects.create(owner=user, **profile_data)

        # 这里可以替换为实际发送邮件的逻辑
        # send_register_email(user.email, 'register')
        return JsonResponse({'status': True, 'data': '/login/'})
    else:
        return JsonResponse({'status': False, 'error': form.errors})




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
    return redirect('login')




def logout_view(request):
    logout(request)
    return redirect('home')




def home(request):
    return render(request, 'home.html')